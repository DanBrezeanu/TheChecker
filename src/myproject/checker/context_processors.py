from checker.models import Problem
from django.contrib.auth.models import User

def percentage_solved(request):
    return {
       "percentage_solved": 0 if request.user.is_anonymous else int(len(request.user.profile.problems_solved.all()) / len(Problem.objects.all()) * 100)
    }