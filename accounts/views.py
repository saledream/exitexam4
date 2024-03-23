from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect  
from .forms import SignUpForm, LoginForm  
from django.contrib.auth import authenticate, login ,logout
from django.urls import reverse  
from django.urls import reverse_lazy 
from django.contrib.auth.views import PasswordResetView, PasswordChangeDoneView, PasswordResetCompleteView,PasswordResetConfirmView  
from django.contrib.messages.views import SuccessMessageMixin 
from django.http import HttpResponse 
from django.contrib import messages 
from .models import User 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.views import LoginView 

def signup(request):
    
    if request.method == 'POST':

        form = SignUpForm(request.POST) 
        
        if form.is_valid():
            form.save() 
            messages.success(request,"registration is successful") 
            return redirect(reverse("account:login"))

        else:
            print(form.errors)
            
            for error in form.errors:
               messages.error(request,form.errors[error])
           
    form = SignUpForm()
    return render(request, 'accounts/signup.html',{'form':form})
 

def mylogin(request):

    if request.method == 'POST':
        form = LoginForm(request.POST) 
        print(form) 

        if form.is_valid():
            email = form.cleaned_data['email'] 
            password = form.cleaned_data['password'] 
            user = authenticate(request, email=email,password=password) 
            if user is not None:
                if user.user_type == 'student': 
                    login(request, user) 
                    return redirect(reverse('student_dashboard')) 

                elif user.user_type == "instructor":
                    login(request, user) 
                    return redirect("/admin/") 
                elif user.is_superuser or user.user_type == 'admin':
                    login(request,user) 
                    return redirect("/admin/") 
                
            else:        
                messages.error(request,"Invalid email or password") 

        else:
             for error in form.errors:
                    messages.error(request,form.errors[error]) 
    form = LoginForm() 
    
    return render(request, 'accounts/login.html',{'form':form})

@login_required
def mylogout(request):

    if request.user.user_type == 'instructor' or request.user.user_type == 'admin' or request.user.is_superuser:
       logout(request)
       return redirect("/accounts/logout/") 
    
    else:
         return redirect("/") 
    
    
@login_required
def dashboard(request):

    return render(request, 'registration/dashboard.html', {'section':'dashboard'})

def profileEdit(request):
    pass 



def viewProfile(request):
    pass 



def check_username(request):
      username = request.POST.get('username') 
      print(username) 
      try:
        user = User.objects.get(username=username)
        return HttpResponse("<div id='username' style='color:red;'>%s already exist </div>"%(username))
      except Exception as e:
           return HttpResponse("<div id='username' style='color:green;'>%s is available </div>"%(username))
      


def check_email(request):
      email = request.POST.get('email') 
      try:
        user = User.objects.get(email=email)
        return HttpResponse("<div id='email' style='color:red;'>%s already exist </div>"%(email)  )
      except Exception as e:
           return HttpResponse("<div id='email' style='color:green;'>%s is available </div>"%(email) )


class ResetPasswordView(SuccessMessageMixin,PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('password_reset_done')




      
  