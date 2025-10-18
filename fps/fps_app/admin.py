from django.contrib import admin
from .models import *


# Register your models here.

class SurveyAdmin(admin.ModelAdmin):
    list_display = ("name_of_survey",)


class Type_question_Admin(admin.ModelAdmin):
    list_display = ("type_question",)


class Answer_Admin(admin.ModelAdmin):
    list_display = ("answer",)


class Answer_Option_Admin(admin.ModelAdmin):
    list_display = ("answer_option",)


class Question_Admin(admin.ModelAdmin):
    list_display = ("id_survey", "id_type_question", "id_group", "question", "mandatory",)


class Multimedia_Admin(admin.ModelAdmin):
    list_display = ("multimedia",)


class User_Admin(admin.ModelAdmin):
    list_display = ("email",)


class Survey_User_Admin(admin.ModelAdmin):
    list_display = ("id_survey", "id_user",)


class User_Answer_Admin(admin.ModelAdmin):
    list_display = ("id_user", "id_answer",)


class Question_Answer_Admin(admin.ModelAdmin):
    list_display = ("id_question", "id_answer",)


class Question_Multimedia_Admin(admin.ModelAdmin):
    list_display = ("id_question", "id_multimedia",)


class Survey_Question_Admin(admin.ModelAdmin):
    list_display = ("id_survey", "id_question",)


class Question_Answer_Option_Admin(admin.ModelAdmin):
    list_display = ("id_question", "id_answer_option",)


class Group_Admin(admin.ModelAdmin):
    list_display = ("group_name",)


class Respondent_Admin(admin.ModelAdmin):
    list_display = ("id_of_respondent",)


class Display_Answers_Admin(admin.ModelAdmin):
    list_display = ("id_survey", "id_user", "id_question", "id_answer", "id_respondent",)

class Hotlink_Admin(admin.ModelAdmin):
    list_display = ("hotlink",)

class Question_Hotlink_Admin(admin.ModelAdmin):
    list_display = ("id_question", "id_hotlink",)

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Type_question, Type_question_Admin)
admin.site.register(Answer, Answer_Admin)
admin.site.register(Answer_Option, Answer_Option_Admin)
admin.site.register(Group, Group_Admin)
admin.site.register(Question, Question_Admin)
admin.site.register(Multimedia, Multimedia_Admin)
admin.site.register(User, User_Admin)
admin.site.register(Survey_User, Survey_User_Admin)
admin.site.register(User_Answer, User_Answer_Admin)
admin.site.register(Question_Answer, Question_Answer_Admin)
admin.site.register(Question_Multimedia, Question_Multimedia_Admin)
admin.site.register(Survey_Question, Survey_Question_Admin)
admin.site.register(Question_Answer_Option, Question_Answer_Option_Admin)
admin.site.register(Respondent, Respondent_Admin)
admin.site.register(Display_Answers, Display_Answers_Admin)
admin.site.register(Hotlink, Hotlink_Admin)
admin.site.register(Question_Hotlink, Question_Hotlink_Admin)

