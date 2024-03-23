from django.db import models
from django.contrib.humanize.templatetags import humanize 
from tinymce.models import HTMLField 
from ckeditor_uploader.fields import RichTextUploadingField 
from django.conf import settings 
from EECommittee.models import Course, Department  
from django.forms import ModelForm
from django.utils import timezone 
from django import forms
from django.utils.safestring import mark_safe 

User = settings.AUTH_USER_MODEL 

class Module(models.Model):

    name = models.CharField(max_length=255) 
    overview = RichTextUploadingField() 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules") 
    instructor = models.ForeignKey(User, on_delete=models.CASCADE,related_name="modules") 
    created_date = models.DateTimeField(auto_now_add=True) 
    updated_date = models.DateTimeField(auto_now=True) 
    
    def get_created_date(self):
        return humanize.naturaltime(self.created_date) 
    
    def get_updated_date(self):
        return humanize.naturaltime(self.updated_date) 
    
    def __str__(self) -> str:
          return self.name 
    
class Page(models.Model):
    title = models.CharField(max_length=255) 
    notes = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now_add=True) 
    updated_date = models.DateTimeField(auto_now=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="pages") 
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages') 
    completionQuestion = models.CharField(max_length=255) 
    completionQuestionAns = models.CharField(max_length=255) 
    answerHint = models.CharField(max_length=255) 
    noteStatus = models.CharField(max_length=255, choices=(('drafted','drafted'),('published','published'))) 

    
    def get_created_date(self):
        return humanize.naturaltime(self.created_date) 
    
    def get_updated_date(self):
        return humanize.naturaltime(self.updated_date) 
class PageCompletion(models.Model):

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='completed_page') 
    student = models.ForeignKey(User,on_delete=models.CASCADE, related_name='completed_page')
    completion_date = models.DateTimeField(auto_now_add=True)

    def get_completion_date(self):
        return humanize.naturaltime(self.completion_date) 
    
class Exam_Model(models.Model):
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="models") 
    title = models.CharField(max_length=50)
    

    def __str__(self):
        return self.title 
    
class Test(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="tests") 
    title = models.CharField(max_length=50)

    
    def __str__(self):
        return self.title 

class ModelExamForm(ModelForm):
   
    class Meta:
        model = Exam_Model
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs = {'class':'form-control'}),
        }

class TestForm(ModelForm):
    class Meta:
        model = Test 
        fields = '__all__'
        

class ExamResult(models.Model):

    exam = models.ForeignKey(Exam_Model, on_delete=models.CASCADE, related_name='results') 
    score = models.IntegerField(default=0) 
    student = models.ForeignKey(User, on_delete=models.CASCADE,related_name='exam_result')
    exam_type = models.CharField(max_length=20) 

class CourseProgress(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_progress") 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="progress") 
    progress = models.PositiveIntegerField(default=0) 

   
class ModelQuestion(models.Model):
      modeExam = models.ForeignKey(Exam_Model, on_delete=models.CASCADE,related_name="question")
      instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
      qno = models.AutoField(primary_key=True)
      question = RichTextUploadingField()
      optionA = models.CharField(max_length=255)
      optionB = models.CharField(max_length=255)
      optionC = models.CharField(max_length=255)
      optionD = models.CharField(max_length=255)
      answer = models.CharField(max_length=255)
      ans_description = models.TextField()
   
      def __str__(self):
        return self.question  
    
      def question_field(self):
        text = ""
        if len(self.question) > 30:
           text = self.question[:30] + " ..."

        else:
            text = self.question    

        return mark_safe(text)

      def answer_field(self):
        text = ""
        if len(self.answer) > 30:
           text = self.answer[:30] + " ..."

        else:
            text = self.answer    

        return mark_safe(text)
      def ans_description_field(self):
        text = ""
        if len(self.ans_description) > 30:
           text = self.ans_description[:30] + " ..."

        else:
            text = self.ans_description    

        return mark_safe(text)


class TestQuestion(models.Model):
      testExam = models.ForeignKey(Test, on_delete=models.CASCADE,related_name="test")
      instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
      qno = models.AutoField(primary_key=True)
      question = RichTextUploadingField()
      optionA = models.CharField(max_length=255)
      optionB = models.CharField(max_length=255)
      optionC = models.CharField(max_length=255)
      optionD = models.CharField(max_length=255)
      answer = models.CharField(max_length=255)
      ans_description = models.TextField()
   
      def __str__(self):
         return self.question  
    
      def question_field(self):
        text = ""
        if len(self.question) > 30:
           text = self.question[:30] + " ..."

        else:
            text = self.question    

        return mark_safe(text)

      def answer_field(self):
        text = ""
        if len(self.answer) > 30:
           text = self.answer[:30] + " ..."

        else:
            text = self.answer    

        return mark_safe(text)
      def ans_description_field(self):
        text = ""
        if len(self.ans_description) > 30:
           text = self.ans_description[:30] + " ..."

        else:
            text = self.ans_description    

        return mark_safe(text)

class ModelQuestionForm(ModelForm):
      class Meta:
        model = ModelQuestion
        fields = "__all__" 
        exclude = ['qno']  

class TestQuestionForm(ModelForm):
    class Meta:
        model = ModelQuestion
        fields = "__all__" 
        exclude = ['qno']  