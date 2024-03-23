from django.urls import path, include 
from . import views 

urlpatterns =[

    path("", views.dashboard, name="student_dashboard"),
    path("fetch/", views.fetch, name="fetch"),
    path("fetch/courses/", views.courses, name="courses"),
    path("fetch/courses/<int:pk>/", views.get_course, name="course"), 
    path("fetch/modules/<int:pk>/", views.get_module, name="module"),
    path("fetch/pages/<int:pk>/", views.get_page, name="page"),
    path("pageCompletion/<int:pk>/<str:complete>/", views.page_complete, name="page_complete"),
    path("alpine/", views.alpine, name="alpine"),    
]