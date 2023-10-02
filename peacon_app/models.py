from django.db import models
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Paper(models.Model):
	PK_ID = models.AutoField(primary_key=True)
	Paper_name = models.CharField(max_length=1000,null=True)
	Paper_owner = models.CharField(max_length=1000,null=True)
	Paper_like = models.IntegerField(default=0,null=True)
	Paper_image = models.CharField(max_length=50,default='default.jpg')
	Paper_type = models.CharField(max_length=100,null=True)
	Paper_details = models.TextField(null=True)
	Paper_PDF = models.CharField(max_length=50,null=True)
	Paper_img1 = models.CharField(max_length=50,default='default.jpg',null=True)
	Paper_img2 = models.CharField(max_length=50,default='default.jpg',null=True)
	Paper_reward = models.CharField(max_length=50,null=True)
	Paper_download = models.IntegerField(default=0,null=True)

class likes(models.Model):
	papers = models.ForeignKey(Paper,related_name='papers',on_delete = models.CASCADE,null=True)
	user = models.CharField(max_length=10,null=True)

class External_User(models.Model):
	PK_Exuser = models.AutoField(primary_key=True)
	Exuser_type = models.CharField(max_length=100,null=True)
	Exuser_name = models.CharField(max_length=100,null=True)
	Exuser_lastname = models.CharField(max_length=100,null=True)
	Exuser_position = models.CharField(max_length=100,null=True)
	Exuser_Ageny = models.CharField(max_length=100,null=True)#ชื่อหนวยงานหรือสถาบัน
	Exuser_email = models.CharField(max_length=50,null=True)
	Exuser_tel = models.CharField(max_length=12,null=True)
	Exuser_address = models.TextField(null=True)
	Exuser_password = models.CharField(max_length=25,null=True)

class Internal_User(models.Model):
	PK_Inuser = models.AutoField(primary_key=True)
	Inuser_id = models.CharField(max_length=100,null=True)
	Inuser_name = models.CharField(max_length=100,null=True)
	Inuser_lastname = models.CharField(max_length=100,null=True)
	Inuser_position = models.CharField(max_length=100,null=True)
	Inuser_Ageny = models.CharField(max_length=100,null=True)#ชื่อหนวยงานหรือสถาบัน
	Inuser_email = models.CharField(max_length=50,null=True)
	Inuser_tel = models.CharField(max_length=12,null=True)
	Inuser_address = models.TextField(null=True)
	def __str__(self):
		return f'{self.Inuser_id}'

class surveys(models.Model):
    survey_id = models.CharField(max_length=100,null=True)
    survey_score1 = models.IntegerField(default=0,null=True)
    survey_score2 = models.IntegerField(default=0,null=True)
    survey_score3 = models.IntegerField(default=0,null=True)
    survey_score4 = models.IntegerField(default=0,null=True)
    survey_score5 = models.IntegerField(default=0,null=True)
    survey_score6 = models.IntegerField(default=0,null=True)
    survey_score7 = models.IntegerField(default=0,null=True)
    survey_avgscore = models.IntegerField(default=0,null=True)
    survey_comment = models.TextField(null=True)

class Creater(models.Model):
	PK_Creater = models.AutoField(primary_key=True)
	Creater_type = models.CharField(max_length=100,null=True)
	Creater_name = models.CharField(max_length=100,null=True)
	Creater_lastname = models.CharField(max_length=100,null=True)
	Creater_own = models.ForeignKey(Paper,related_name='Creater_user',on_delete=models.CASCADE,null=True)

class Speaker_user(models.Model):
	PK_Exuser = models.AutoField(primary_key=True)
	Speaker_type = models.CharField(max_length=100,null=True)
	Speaker_name = models.CharField(max_length=100,null=True)
	Speaker_lastname = models.CharField(max_length=100,null=True)
	Speaker_position = models.CharField(max_length=1000,null=True)
	Speaker_Ageny = models.CharField(max_length=100,null=True)#ชื่อหนวยงานหรือสถาบัน
	Speaker_email = models.CharField(max_length=100,null=True)
	Speaker_line = models.CharField(max_length=50,null=True)
	Speaker_tel = models.CharField(max_length=12,null=True)
	Speaker_address = models.TextField(null=True)
	Speaker_password = models.CharField(max_length=25,null=True)
	Speaker_Status = models.CharField(max_length=25,null=True)
	Speaker_Userid =  models.CharField(max_length=25,null=True)

class User_do(models.Model):
	PK_listnum = models.AutoField(primary_key=True)
	user_name = models.CharField(max_length=100,null=True)
	user_lastname = models.CharField(max_length=100,null=True)
	user_type = models.CharField(max_length=1,null=True)
	user_tel = models.CharField(max_length=12,null=True)
	user_logindate = models.DateField(auto_now_add=True)