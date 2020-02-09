from django.urls import path, include
from . import views
from checker.models import Problem, Document
from django.conf import settings
import os
import json
from django.conf.urls.static import static
from .evaluator import _read_config_file


urlpatterns = [
	path('upload/', views.upload, name='list'),
	path('sources/', views.sources, name='sources'),
	path('', views.home, name='home'),
	path('<int:id>/<str:filename>/', views.entry, name='entry'),
	path('<int:id>/<str:filename>/raw/', views.rawfile, name='entry'),
	path('problem/<int:id>/', views.problem, name = 'problem'),
	path('problem/<int:id>/official_solution/', views.official_solution, name = 'official_solution'),
	path('problem/<int:id>/submissions/', views.problem_submissions, name = 'problem_submissions'),
	path('problem/', views.list_problems, name = 'list_problems'),
	path('example/<int:problem>/<int:id>/<slug:inout>/', views.download_example, name='download_example'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/profile/', views.view_profile, name='profile'),
	path('accounts/register/', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)