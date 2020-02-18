from django.core.management.base import BaseCommand
from django.utils import timezone
from checker.models import Problem, Document
from glob import glob
import os
from django.conf import settings
import json
from checker.utils import _read_config_file, _format_problem_text

class Command(BaseCommand):
    help = 'Reloads/Adds problems in the database'

    def handle(self, *args, **kwargs):
        problems = Problem.objects.all()
        
        # Short lambda for record update
        pb_filter = lambda number: Problem.objects.filter(number = number)

        for problem_dir in glob(os.path.join(settings.APP_DIR, 'problems', '[0-9]*')):
            problem_number = int(os.path.split(problem_dir)[-1])
            
            exists = len(pb_filter(problem_number)) != 0 

            text_path = os.path.join(settings.APP_DIR, 'problems', str(problem_number), 'text.json')
            example_path = os.path.join(settings.APP_DIR, 'problems', str(problem_number), 'examples')
            config_path = os.path.join(settings.APP_DIR, 'problems', str(problem_number), 'config.yml')
            examples = []

            if exists:
                # Update problem text
                if os.path.exists(text_path):
                    pb_filter(problem.number).update(
                        text =  _format_problem_text(open(text_path, 'r').read())
                    )

                # Update problem examples
                example_number = 0
                while os.path.exists(os.path.join(example_path, str(example_number) + '.in')):
                    examples.append([
                        open(os.path.join(example_path, str(example_number) + '.in')).read(),
                        open(os.path.join(example_path, str(example_number) + '.out')).read(),
                        open(os.path.join(example_path, str(example_number) + '.obs')).read(),
                    ])
                    example_number += 1

                pb_filter(problem.number).update(examples = json.dumps(examples))

                time_limit, mem_limit, source_limit, difficulty, name = _read_config_file(problem_number)

                pb_filter(problem.number).update(
                    time_limit = time_limit,
                    memory_limit = mem_limit,
                    source_limit = source_limit,
                    difficulty = difficulty,
                    name = name
                )
            else:
                example_number = 0
                while os.path.exists(os.path.join(example_path, str(example_number) + '.in')):
                    examples.append([
                        open(os.path.join(example_path, str(example_number) + '.in')).read(),
                        open(os.path.join(example_path, str(example_number) + '.out')).read(),
                        open(os.path.join(example_path, str(example_number) + '.obs')).read(),
                    ])
                    example_number += 1

                time_limit, mem_limit, source_limit, difficulty, name = _read_config_file(problem_number)

                Problem(
                    text = _format_problem_text(open(text_path, 'r').read()),
                    examples = json.dumps(examples),
                    time_limit = time_limit,
                    memory_limit = mem_limit,
                    source_limit = source_limit,
                    difficulty = difficulty,
                    name = name,
                    number = problem_number,
                ).save()

                for source in Document.objects.all():
                    if source.problemobj.number == number:
                        p.sources.add(source)
        
