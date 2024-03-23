from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.forms.models import ModelChoiceField
from django.http import HttpRequest
from .models import Exam_Model, Module, Page,ExamResult, PageCompletion, ModelQuestion, TestQuestion, Test   
from accounts.models import User 
from EECommittee.models import Course 


class ModuleModelAdmin(admin.ModelAdmin):
     list_display = ('name','instructor','course','updated_date') 
     model = Module 
     list_filter = ('course','instructor__username')
     search_fields = ('course__name','instructor__username','name')

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          return  qs.filter(instructor=request.user)
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'instructor':
               kwargs['queryset'] = User.objects.filter(username=request.user) 

          if db_field.name == 'course':
                kwargs['queryset'] = Course.objects.filter(instructor=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
     
 
admin.site.register(Module, ModuleModelAdmin) 

class PageModelAdmin(admin.ModelAdmin):
     list_display = ('title','module','updated_date','noteStatus') 
     model = Page  
     list_filter = ('module',)
     search_fields = ('title','status')

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          return  qs.filter(instructor=request.user) 
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'instructor':
               kwargs['queryset'] = User.objects.filter(username=request.user) 
          if db_field.name == 'module':
                kwargs['queryset'] = Module.objects.filter(instructor=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Page, PageModelAdmin)

class ModelExamModelAdmin(admin.ModelAdmin):
     list_display = ('title','dept') 
     model = Exam_Model 
     list_filter = ('dept',)
     search_fields = ('title','dept')

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          return  qs.filter(dept=request.user.department)
        
     # def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
     #      if db_field.name == 'author':
     #           kwargs['queryset'] = User.objects.filter(username=request.user) 

     #      if db_field.name == 'course':
     #            kwargs['queryset'] = Course.objects.filter(instructor=request.user) 

     #      return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Exam_Model, ModelExamModelAdmin)

class TestExamModelAdmin(admin.ModelAdmin):
     list_display = ('title','course') 
     model = Test 
     # list_filter = [('course__name',admin.RelatedOnlyFieldListFilter),('instructor__username',admin.RelatedFieldListFilter)]
     search_fields = ('title','course')
     list_filter = ['course__name',]

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          return  qs.filter(author=request.user)
     
admin.site.register(Test, TestExamModelAdmin)


class ResultModelAdmin(admin.ModelAdmin):
     list_display = ('student','exam','exam_type','score') 
     model = ExamResult  
     list_filter = ('student__username','exam__title')
     search_fields = ('student','exam','exam_type','score')

admin.site.register(ExamResult, ResultModelAdmin)


class PageCompletionModelAdmin(admin.ModelAdmin):
     list_display = ('student','page','completion_date') 
     model = PageCompletion  
     list_filter = ('student__username','page__title')
     search_fields = ('student','page')

admin.site.register(PageCompletion, PageCompletionModelAdmin) 



class ModelQuestionModelAdmin(admin.ModelAdmin):
     list_display = ('instructor','question_field','answer_field','ans_description_field') 
     model = ModelQuestion 
     list_filter = ('instructor__username',)
     search_fields = ('instructor',) 

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          return  qs.filter(instructor=request.user)
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'instructor':
               kwargs['queryset'] = User.objects.filter(username=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(ModelQuestion, ModelQuestionModelAdmin) 

class TestQuestionModelAdmin(admin.ModelAdmin):
     list_display = ('instructor','question_field','answer_field','ans_description_field') 
     model = TestQuestion 
     list_filter = ('instructor__username',)
     search_fields = ('instructor',) 

     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          return  qs.filter(instructor=request.user)
     
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
          
          if db_field.name == 'instructor':
               kwargs['queryset'] = User.objects.filter(username=request.user) 

          return super().formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(TestQuestion, TestQuestionModelAdmin) 






