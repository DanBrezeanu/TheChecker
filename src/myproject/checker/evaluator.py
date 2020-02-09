from checker.models import Document, Problem, Handler
from django.conf import settings

from glob import glob
import shutil

from subprocess import Popen, PIPE
import os, sys
import json
import re

import enum
from ttictoc import TicToc

from .utils import _read_config_file, _diff 

class Status(enum.Enum):
    OK = 0
    WRONG_ANSWER = 1
    NOT_RUN = 2
    TLE = 3
    MLE = 4
    SLE = 5
    SIGSEGV = 139
    SIGFPE = 136
    SIGABRT = 134
    SIGINT = 124
    
    def __int__(self):
        return self.value


def evaluate_source(filename, user):
    stdout = ''
    score = 0
    test_value = 0
    tests_result = []
    tests_time = []

    stderr, has_compiled, output_location = _start_eval(os.path.join(settings.MEDIA_ROOT, filename))

    if has_compiled:
        stdout, score, test_value, tests_result, tests_time = _run_tests(output_location, filename.split('/')[0])

    _update_database_entry(filename, stdout, stderr, has_compiled, score, test_value, json.dumps(tests_result), json.dumps(tests_time), user)


def _start_eval(filename):
    output_location = '/'.join(filename.split('/')[:-1] + ['output'])
    print(filename)
    process = Popen(['g++', filename, '-Wall', '-std=c++11', '-o', output_location], stdout=PIPE, stderr=PIPE)
    _, stderr = process.communicate()

    stderr = stderr.decode('utf-8').replace(filename + ':', '')

    print(stderr, end='------\n')

    return stderr, os.path.exists(output_location), output_location

def _update_database_entry(filename, stdout, stderr, has_compiled, score, test_value, tests_result, tests_time, user):
    h = Handler.get_instance()
    h.acquire_mutex()

    try:
        entry = Document.objects.filter(docfile=filename)

        entry.update(finished = True)
        entry.update(stdout = stdout)
        entry.update(stderr = stderr)
        entry.update(score = score)
        entry.update(test_value = test_value)
        entry.update(tests_result = tests_result)
        entry.update(tests_time = tests_time)

        if score == 100:
            if entry[0].problemobj.number in [pb.number for pb in user.profile.problems_tried.all()]:
                user.profile.problems_tried.remove(entry[0].problemobj)

            if entry[0].problemobj.number not in [pb.number for pb in user.profile.problems_solved.all()]:
                user.profile.problems_solved.add(entry[0].problemobj)
                user.profile.coins = user.profile.coins + 5
                user.profile.save()
        else:
            if entry[0].problemobj.number not in [pb.number for pb in user.profile.problems_tried.all()]:
                user.profile.problems_tried.add(entry[0].problemobj)
    except:
        print('thrown error while updating db')
    finally:
        h.release_mutex()

    if score > entry[0].problemobj.bestscore:
        print('it is')
        Problem.objects.filter(number = entry[0].problemobj.number).update(bestscore = score)
    
    print(entry[0].problemobj.bestscore)

def _run_tests(output, problem):
    score = 0
    stdout = ''
    sandbox_directory = '/'.join(output.split('/')[:-2]) + '/sandbox/'
    all_tests = glob(settings.APP_DIR + '/problems/{}/tests/{}_*.in'.format(problem, problem))
    test_value = 100.0 / len(all_tests)

    tests_result = []
    tests_time = []

    os.chown(output, 33, 33)
    shutil.copy2(output, sandbox_directory)

    for testname in all_tests:
        os.chown(testname, 33, 33)
        os.chdir(settings.BASE_DIR)
        print('CURRENT_DIRECTORY=' + os.path.abspath('./'))
        shutil.copy2(testname, os.path.join(settings.BASE_DIR, '{}.in'.format(problem)))
        status, test_time, stdout = _run_exec(sandbox_directory, output, problem)

        tests_time.append(test_time)

        if status == Status.OK:
            if os.path.exists(sandbox_directory + '{}.out'.format(problem)):
                result_ok = _diff(sandbox_directory + '/{}.out'.format(problem), testname.split('.')[0] + '.out')

                if result_ok:
                    score += test_value

                tests_result.append(int(Status.OK) if result_ok else int(Status.WRONG_ANSWER))
            else:
                print('does not exist' + output_directory + '/{}.out'.format(problem))
        else:
            tests_result.append(int(status))

    try:
        os.remove(output)
        os.remove(sandbox_directory + '{}.out'.format(problem))
        os.remove(sandbox_directory + 'output')
        os.remove('./{}.in'.format(problem))
        os.remove('./{}.out'.format(problem))
    except:
        pass

    return stdout, score, test_value, tests_result, tests_time 

def _run_exec(sandbox_directory, output, problem):
    t = TicToc()
    status = Status.NOT_RUN

    time_limit, mem_limit, _, _, _ = _read_config_file(problem)
    script_location = sandbox_directory + 'exec_script.sh'
    exec_location = sandbox_directory + output.split('/')[-1]
    
    print('script = {}\nexec = {}'.format(script_location, exec_location))

    t.tic()
    process = Popen([script_location, exec_location], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    elapsed = t.toc()

    if os.path.exists('./{}.out'.format(problem)):
        shutil.copy('./{}.out'.format(problem), sandbox_directory)
    else:
        status = Status.WRONG_ANSWER

    return_code = int(re.findall(r'\d+', stdout.decode('utf-8'))[0])
    print('return_code = {}'.format(return_code))

    if return_code == int(Status.SIGINT):
        status = Status.TLE
    elif return_code == int(Status.SIGSEGV):
        status = Status.SIGSEGV
        print("SEG FAULT")
    elif return_code == int(Status.SIGFPE):
        status = Status.SIGFPE
    elif return_code == int(Status.SIGABRT):
        status = Status.SIGABRT

    if status == Status.NOT_RUN and elapsed > time_limit:
            status = Status.TLE

    # Test for MLE
    
    if status == Status.NOT_RUN and return_code == 0:
        status = Status.OK

    return status, round(elapsed, 3), stdout






    
