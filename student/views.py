from django.shortcuts import render, get_object_or_404 
from django.http import HttpResponse 
from accounts.models import User 
from EECommittee.models import Course, Department 
from instructor.models import Module, Page, Exam_Model, Test, PageCompletion
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse 
from instructor.models import CourseProgress 

# Create your views here.

@login_required
def dashboard(request):
    
        print(User.objects.all())
        modelsExams = Exam_Model.objects.filter(dept__name="computer science") 

        return render(request, 'student/index.html',{'users':User.objects.all(),"modelExam":modelsExams})


def fetch(request): 
      courses = Course.objects.all() 

      return render(request,"partials/courses.html",{'courses':courses})
       
@login_required
def courses(request): 
      user = request.user 
      print(user.department) 
      courses = Course.objects.filter(dept=user.department)
      courses_progress= [] 
      for course in courses:
           try:
              
              cp = CourseProgress.objects.get(course=course)
              progress = cp.progress 

           except CourseProgress.DoesNotExist:
                progress = 0 
           courses_progress.append([course,progress]) 

      return render(request,"partials/courses.html",{'courses':courses_progress}) 
       

      
@login_required
def get_course(request,pk): 
      
      modules = None 
      try:
         course = get_object_or_404(Course,id=pk)
      
         modules = course.modules.all() 
      except Exception as e:
          print(" what is going on")

      return render(request,"partials/modules.html",{'modules':modules}) 
       
@login_required
def get_module(request,pk): 
      
      module = None 
      try:
         module = get_object_or_404(Module,id=pk)
      
      except Exception as e:
          print(" what is going on")

      return render(request,"partials/pages.html",{'module':module}) 

def get_page(request,pk): 
      
      page = None 
      completed = False 
      try:
         
         page = Page.objects.get(id=pk)
         completed = PageCompletion.objects.get(page=page) 
         completed = True 

      except Page.DoesNotExist:
          page = None 

      except PageCompletion.DoesNotExist:
           completed = False 

      return render(request,"partials/page.html",{'page':page,'completed':completed}) 

def alpine(request):
     
     return render(request,"partials/alpine.html",{"love":'you'})

def page_complete(request,pk,complete):
     
     print(pk,complete) 
     page = None 

     try:
           page = Page.objects.get(id=pk)  
           print(page, "oooooooooo", request.user) 
           if page is not None and complete.lower() == 'true':
                 
                 try:
                      page_complete = PageCompletion.objects.get(page=page)
                      print(page_complete)
                      print(page) 
                      print("-------------------")
                 except PageCompletion.DoesNotExist: 
                        marked = PageCompletion.objects.create(page=page, student=request.user) 
                        marked.save()
                        print("saved successs!!!!!") 

           elif page is not None and complete.lower() == 'false':
                unmark = PageCompletion.objects.filter(page=page)
                for page in unmark:
                     page.delete()  

                print("successs!! delete")

           return HttpResponse("marked")
     
     except Page.DoesNotExist:
         pass 
    
     return HttpResponse("unmarked")
                                           