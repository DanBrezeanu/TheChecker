from checker.models import Problem
from django.contrib.auth.models import User

def percentage_solved(request):
   if not request.user.is_anonymous:
      problems_solved = []
      for src in request.user.profile.sources.all():
         if src.problemobj.number not in problems_solved and src.score == 100:
            problems_solved.append(src.problemobj.number)

   return {
       "percentage_solved": 0 if request.user.is_anonymous else int(len(problems_solved) / len(Problem.objects.all()) * 100)
   }