from django.core.management.base import BaseCommand
from django.utils import timezone
from checker.models import Problem, Document
from glob import glob
import os
from django.conf import settings
import json
from checker.utils import _read_config_file, _format_problem_text

class Command(BaseCommand):
    help = 'Reloads problems in the database'

    def handle(self, *args, **kwargs):
        all_sources = Document.objects.all()
        Problem.objects.all().delete()

        for i in [f.path for f in os.scandir(os.path.join(settings.APP_DIR, 'problems/')) if f.is_dir()]:
            examples = []
            number = int(i.split('/')[-1])

            p = Problem(number = number)

            text_path = os.path.join(i, 'text.json')
            if os.path.exists(text_path):
                p.text =  _format_problem_text(open(text_path, 'r').read())
            
            example_path = os.path.join(i, 'examples')
            example_number = 0
            while os.path.exists(os.path.join(example_path, str(example_number) + '.in')):
                examples.append([
                    open(os.path.join(example_path, str(example_number) + '.in')).read(),
                    open(os.path.join(example_path, str(example_number) + '.out')).read(),
                    open(os.path.join(example_path, str(example_number) + '.obs')).read(),
                ])
                example_number += 1

            p.examples = json.dumps(examples)

            difficulty = 0
            name = '' 
   
            _, _, _, difficulty, name = _read_config_file(number)

            p.difficulty = difficulty
            p.name = name
            print('name = {}'.format(name))

            p.save()
            for source in all_sources:
                if source.problemobj.number == number:
                    p.sources.add(source)
