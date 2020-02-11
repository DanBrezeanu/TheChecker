from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse

from checker.models import Document, Problem, Profile

from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from checker.forms import DocumentForm, UserRegistration, ImageUpload
from django.conf import settings

from django.core.files.storage import default_storage
from django.utils.encoding import smart_str

import sys
import os
import datetime
import threading
import json

from .evaluator import evaluate_source

from django.contrib.auth.decorators import login_required, user_passes_test

from .image_processor import Thumbnail


format_name = lambda request, date: os.path.join(request.POST['problemnumber'], '--'.join([date, str(request.FILES['docfile'])]))

def home(request):
    return render(request, 'home.html')

def file_upload(request, dateandtime):
    save_path = os.path.join(settings.MEDIA_ROOT, format_name(request, dateandtime))
    print(save_path)
    path = default_storage.save(save_path, request.FILES['docfile'])
    return default_storage.path(path)

def upload(request):
    open('/home/pi/checker/src/myproject/celemailoguri.txt', 'w').write('in upload\n')
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    else:
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                date_object = datetime.datetime.now()
                dateandtime = date_object.strftime("%H:%M:%S-%d-%m-%y")

                file_upload(request, dateandtime)

                print(request.POST)
                newdoc = Document(docfile = format_name(request, dateandtime),
                                problemobj = Problem.objects.filter(number = int(request.POST['problemnumber'][0]))[0],
                                date = date_object,
                        )
                newdoc.save()
                
                request.user.profile.sent_sources.add(newdoc)
                Problem.objects.filter(number = int(request.POST['problemnumber'][0]))[0].sources.add(newdoc)
                fname = format_name(request, dateandtime)
                print(fname)
                open('/home/pi/checker/src/myproject/celemailoguri.txt', 'a').write('starting thread\n')
                threading.Thread(target=evaluate_source, args=(fname, request.user), kwargs={}).start()

                # Redirect to the document list after POST
                return HttpResponseRedirect(reverse('sources'))
        else:
            form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
   


    # Render list page with the documents and the form
    return render(request, 'list.html', {'form': form})


def entry(request, id = 0, filename = 'NULL'):
    entry = Document.objects.filter(docfile=os.path.join(str(id), filename))[0]
    html_results = []
    code_to_text = {0: 'OK', 1: 'Wrong Answer', 3: 'Time Limit Excedeed', 4: 'Memory Limit Excedeed', 134: 'Program aborted', 136: 'Floating Point Exception', 139: 'Segementation Fault'}
    tests_time = json.loads(entry.tests_time)

    for idx, result in enumerate(json.loads(entry.tests_result)):
        html_results.append([
            idx,
            entry.test_value if result == 0 else 0,
            tests_time[idx],
            code_to_text[result],
        ])

    
    print(html_results)
    return render(request, 'example.html', {'entry': entry, 'result': html_results})

def sources(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    else:
        documents = request.user.profile.sent_sources.all()[::-1]
        
        difficulties = [doc.problemobj.difficulty for doc in documents][::-1]

        print(request.user.username)
        print(difficulties)
        return render(request, 'sources.html', {'documents': zip(documents, difficulties)})

def rawfile(request, id = 0, filename = 'NULL'):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))

    has_permission = any([source.docfile.split('/')[-1] == filename for source in request.user.profile.sent_sources.all()])
    if has_permission:
        # filecontent = syntax_highlight(open(os.path.join(settings.MEDIA_ROOT, str(id), filename)).read())
        return render(request, 'rawfile.html', {'filecontent': open(os.path.join(settings.MEDIA_ROOT, str(id), filename)).read()})
    else:
        return render(request, 'permission_denied.html')

def list_problems(request):
    entries = Problem.objects.all()[::-1]
    problem_scores = [-1 for i in range(len(entries))]

    if not request.user.is_anonymous:
        user = User.objects.get(username = request.user.username)

        for source in user.profile.sent_sources.all():
            if source.score > problem_scores[source.problemobj.number]:
                problem_scores[source.problemobj.number] = source.score

    return render(request, 'problems.html', {'entries': zip(entries, problem_scores)})

def problem(request, id = 0):
    entry = Problem.objects.filter(number = id)[0]
    examples = json.loads(entry.examples)
    
    bestsource = None
    max_score = -1

    if not request.user.is_anonymous:
        for source in request.user.profile.sent_sources.all():
            if source.problemobj.number == id and source.score > max_score:
                bestsource = source
                max_score = source.score

    return render(request, 'problem.html', {'entry': entry, 'examples': examples, 'bestsource': bestsource})

def download_example(request, problem = 0, id = 0, inout = ''):
    file_path = os.path.join(settings.APP_DIR, 'problems', str(problem), 'examples', str(id) + '.' + inout)

    if os.path.exists(file_path):
        file_content = open(file_path, 'r').read()

        response = HttpResponse(file_content, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename={}_{}.{}'.format(problem, id, inout)
        response['X-Sendfile'] = file_path

        return response
    else:
        raise Http404

def official_solution(request, id = 0):
    print('got here')

    if request.user.is_anonymous:
        return render(request, 'permission_denied.html')

    if id not in [pb.number for pb in request.user.profile.problems_solved.all()]:
        return render(request, 'permission_denied.html')

    solution_content = open(os.path.join(settings.APP_DIR, 'problems', str(id), 'solution.cpp'), 'r').read()
    
    return render(request, 'rawfile.html', {'filecontent': solution_content})

def problem_submissions(request, id = 0):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    else:
        documents = [(pb, pb.problemobj.difficulty) for pb in request.user.profile.sent_sources.all() if pb.problemobj.number == id][::-1]

    return render(request, 'problem_submissions.html', {'documents': documents})

    
    
@login_required
def view_profile(request):
    # if request.method == 'POST':
    #     form = ImageUpload(request.POST, request.FILES)
    #     print(form.errors)
    #     if form.is_valid():
    #         user = User.objects.get(username = request.user.username)
    #         user.profile.image = form.cleaned_data['image']
    #         user.save()

    #         print('got it boi')

    #         return HttpResponseRedirect(reverse('profile'))
    # else:
    #     form = ImageUpload()

    return render(request, 'registration/profile.html')

@user_passes_test(lambda user: user.is_anonymous)
def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():

            print(request.POST)
            new_user = User.objects.create_user(
                    username = request.POST['username'],
                    email = request.POST['email'],
                    password = request.POST['password']
                )
            new_user.save()

            new_profile = Profile(
                user = new_user,
                coins = 100
            )
            new_profile.save()

            user = authenticate(username = request.POST['username'],
                         password = request.POST['password'])

            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UserRegistration()

    return render(request, 'registration/register.html', {'form': form})

