from django.contrib import admin
from .models import Paper,likes, External_User, Internal_User, surveys , Creater ,Speaker_user,User_do

# Register your models here.

admin.site.register(Paper)
admin.site.register(likes)
admin.site.register(External_User)
admin.site.register(Internal_User)
admin.site.register(Speaker_user)
admin.site.register(User_do)
admin.site.register(surveys)
admin.site.register(Creater)