from django.db import models


# Create your models here.

class Survey(models.Model):
    id_of_survey = models.CharField(max_length=255, default="")
    name_of_survey = models.CharField(max_length=255)
    file_content = models.CharField(max_length=255, default="")
    file_extension = models.CharField(max_length=10, default="")
    allow_file_upload_with_answers = models.BooleanField(default=False)


class Group(models.Model):
    group_name = models.CharField(max_length=255)


class Type_question(models.Model):
    type_question = models.CharField(max_length=255)


class Answer(models.Model):
    answer = models.CharField(max_length=255)


class Answer_Option(models.Model):
    answer_option = models.CharField(max_length=255)


class Question(models.Model):
    id_survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    id_type_question = models.ForeignKey(Type_question, on_delete=models.CASCADE)
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    mandatory = models.BooleanField(default=False)


class Multimedia(models.Model):
    multimedia = models.CharField(max_length=300)


class User(models.Model):
    email = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)

class Survey_User(models.Model):
    id_survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)


class User_Answer(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class Question_Answer(models.Model):
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class Question_Multimedia(models.Model):
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_multimedia = models.ForeignKey(Multimedia, on_delete=models.CASCADE)


class Survey_Question(models.Model):
    id_survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Question_Answer_Option(models.Model):
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_answer_option = models.ForeignKey(Answer_Option, on_delete=models.CASCADE)


class Respondent(models.Model):
    id_of_respondent = models.CharField(max_length=10)


class Display_Answers(models.Model):
    id_survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    id_respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)


class Hotlink(models.Model):
    hotlink = models.CharField(max_length=400)

class Question_Hotlink(models.Model):
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_hotlink = models.ForeignKey(Hotlink, on_delete=models.CASCADE)