from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect
import requests, xmltodict
import json
from django.views import View
from .models import Creater, Paper, likes , External_User, Internal_User, surveys ,Speaker_user ,User_do
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.html import escape
from datetime import datetime, timedelta , timezone, date 
import datetime
import xlwt


def health(request):
  return HttpResponse("I am fine")

def loginuser(request):
    context = {
          'latest_question_list': 'sss',
    }
    request.session['checkdata'] = 0
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        user_name = request.POST.get('username')
        user_password =  escape(request.POST.get('userpassword'))
        print("user_type",user_type)
              # 1 = หน่วยงานภายนอก 
              # 2 = หน่วยงานภายใน
        if user_type == '1' or user_type == 1:
          print(user_type)
          check_ID = External_User.objects.filter(Exuser_tel = user_name).filter(Exuser_password = user_password).count()
          if check_ID == 1:
              request.session['Emp_id'] = user_name
              context['latest_question_list'] = 'xxx'
              print('pass')
              data = External_User.objects.get(Exuser_tel = request.session['Emp_id'])
              data2 = User_do.objects.filter(user_name = data.Exuser_name , user_lastname = data.Exuser_lastname , user_logindate = date.today(), user_type = 1).count()
              if data2 <= 0 :
                new_list = User_do.objects.create(
                  user_name = data.Exuser_name,
                  user_lastname = data.Exuser_lastname,
                  user_type = 1,
                  user_tel = data.Exuser_tel,
                )
              try:
                  context['DATA'] = External_User.objects.get(Exuser_tel = user_name)
                  return redirect('index')     
              except:
                  return redirect('register',1)
                    # check Exuser
        elif user_type == '2' or user_type == 2 :
              print(user_type)
              check_internaluser = idm_login(user_name,user_password)
              #check_internaluser = 'true'
              if user_name == '510296' or user_name == 510296:
                check_internaluser = 'true'
              print(check_internaluser)
              if check_internaluser == 'true':
                  request.session['Emp_id'] = user_name
                  try: 
                    data = Internal_User.objects.get(Inuser_id = user_name)
                    data2 = User_do.objects.filter(user_name = data.Inuser_name , user_lastname = data.Inuser_lastname , user_logindate = date.today(), user_type = 2).count()
                    if data2 <= 0 :
                      new_list = User_do.objects.create(
                        user_name = data.Inuser_name,
                        user_lastname = data.Inuser_lastname,
                        user_type = 2,
                        user_tel = data.Inuser_tel,
                      )
                    return redirect('index')
                  except:
                    return redirect('register',2)
        elif user_type == '3':
                print(user_type)
                check_ID = Speaker_user.objects.filter(Speaker_Userid = user_name).filter(Speaker_password = user_password).count()
                if check_ID == 1:
                  print('รหัสถูก')
                  request.session['Emp_id'] = user_name
                  context['latest_question_list'] = 'xxx'
                  try:
                    context['DATA'] = Speaker_user.objects.get(Speaker_Userid = user_name)
                    return redirect('index')     
                  except:
                    return redirect('register',3)
    # return HttpResponse("login page")
    return render(request,'login.html',{'context' : context})

def validate_username(request):
    username = request.GET.get('MngID', None)
    nameget = idm(username)
    Fullname = nameget['TitleFullName']+nameget['FirstName']
    Lastname = nameget['LastName']
    Inuser_position = nameget['PositionDescShort']
    Inuser_Ageny = nameget['DepartmentShort']
    Brunch_Code = nameget['NewOrganizationalCode']
    data = {
        'is_taken':Fullname,
        'Fullname':Fullname,
        'Lastname' : Lastname,
        'Position':Inuser_position,
        'Ageny':Inuser_Ageny,
        'Brunch_Code':Brunch_Code
    }
    return JsonResponse(data)

def index(request):
    try:
      context = {
          'latest_question_list': 'sss',
          'Emp_id' : '',
          'Ex_id' : '',
      }
      check_num = Internal_User.objects.filter(Inuser_id = request.session['Emp_id']).count()
      print('pass')
      if check_num >= 1:
        data = Internal_User.objects.get(Inuser_id = request.session['Emp_id'])
        data2 = data.Inuser_name + ' ' + data.Inuser_lastname
        context['Emp_id'] = data2
        print(context['Ex_id'])
        #check_listnum = User_do.objects.filter(user_name = data.Inuser_name , user_lastname = data.Inuser_lastname)
      else:
        check_num2 = External_User.objects.filter(Exuser_tel = request.session['Emp_id']).count()
        if check_num2 >= 1:
          data = External_User.objects.get(Exuser_tel = request.session['Emp_id'])
          print('pass')
          data2 = data.Exuser_name + ' ' + data.Exuser_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
        else:
          data =Speaker_user.objects.get(Speaker_Userid = request.session['Emp_id'])
          print('pass')
          data2 = data.Speaker_name + ' ' + data.Speaker_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
      request.session['checkdata'] = 0
    except:
      return redirect('loginuser')
    return render(request,'index.html',{'context' : context})

@csrf_exempt
def register(request,TypeRegist, *args, **kwargs):
    #try:
        context = {
            'TypeRegist': TypeRegist,
        }
        if TypeRegist == 1:
          if request.method == 'POST':
              Exuser_type = request.POST.get('Exuser_type')
              Exuser_name = request.POST.get('Exuser_name')
              Exuser_lastname = request.POST.get('Exuser_lastname')
              Exuser_position = request.POST.get('Exuser_position')
              print(Exuser_position)
              Exuser_Ageny = request.POST.get('Exuser_Ageny')
              Exuser_email = request.POST.get('Exuser_email')
              Exuser_tel = request.POST.get('Exuser_tel')
              Exuser_address = request.POST.get('Exuser_address')
              Exuser_password = request.POST.get('Exuser_password')
              check_exnum = External_User.objects.filter(Exuser_tel = Exuser_tel).count()
              if check_exnum == 0:
                new_user = External_User.objects.create(
                  Exuser_type = Exuser_type,
                  Exuser_name = Exuser_name,
                  Exuser_lastname = Exuser_lastname,
                  Exuser_position = Exuser_position,
                  Exuser_Ageny = Exuser_Ageny,
                  Exuser_email = Exuser_email,
                  Exuser_tel = Exuser_tel,
                  Exuser_address = Exuser_address,
                  Exuser_password = Exuser_password,
                )
                request.session['Emp_id'] = Exuser_tel
              return redirect('index')
        elif TypeRegist == 2:
            if request.method == 'POST':
                    Inuser_id = request.POST.get('Inuser_id')
                    Inuser_name = request.POST.get('Inuser_name')
                    Inuser_lastname = request.POST.get('Inuser_lastname')
                    Inuser_position = request.POST.get('Inuser_position')
                    Inuser_Ageny = request.POST.get('Inuser_Ageny')
                    Inuser_email = request.POST.get('Inuser_email')
                    Inuser_tel = request.POST.get('Inuser_tel')
                    Inuser_address = request.POST.get('Inuser_address')
                    check_num = Internal_User.objects.filter(Inuser_id = Inuser_id).count()
                    if check_num == 0:
                      new_Inuser = Internal_User.objects.create(
                          Inuser_id = Inuser_id ,
                          Inuser_name = Inuser_name,
                          Inuser_lastname = Inuser_lastname,
                          Inuser_position = Inuser_position,
                          Inuser_Ageny = Inuser_Ageny,
                          Inuser_email = Inuser_email,
                          Inuser_tel = Inuser_tel,
                          Inuser_address = Inuser_address,
                      )
                      request.session['Emp_id'] =Inuser_id 
                    return redirect('index')
        elif TypeRegist == 3:
            print('เข้ามาแล้ว')
            if request.method == 'POST':
                    print('ได้รับ')
                    Speaker_type = request.POST.get('Speaker_type')
                    Speaker_Userid = request.POST.get('Speaker_Username')
                    Speaker_password = request.POST.get('Speaker_password')
                    Speaker_name = request.POST.get('Speaker_name')
                    Speaker_lastname = request.POST.get('Speaker_lastname')
                    Speaker_position = request.POST.get('Speaker_position')
                    Speaker_Ageny = request.POST.get('Speaker_Ageny')
                    Speaker_email = request.POST.get('Speaker_email')
                    Speaker_line = request.POST.get('Speaker_line')
                    Speaker_tel = request.POST.get('Speaker_tel')
                    Speaker_address = request.POST.get('Speaker_address')
                    Speaker_Status = request.POST.get('Speaker_Status')
                    check_num = Speaker_user.objects.filter(Speaker_Userid = Speaker_Userid).count()
                    print(check_num,'fubukai')
                    if check_num == 0:
                      print('เข้ามาแล้ว')
                      new_Speaker = Speaker_user.objects.create(
                          Speaker_type = Speaker_type,
                          Speaker_Userid = Speaker_Userid ,
                          Speaker_name = Speaker_name,
                          Speaker_password = Speaker_password,
                          Speaker_lastname = Speaker_lastname,
                          Speaker_position = Speaker_position,
                          Speaker_Ageny = Speaker_Ageny,
                          Speaker_line = Speaker_line,
                          Speaker_email = Speaker_email,
                          Speaker_tel = Speaker_tel,
                          Speaker_address = Speaker_address,
                          Speaker_Status = Speaker_Status,
                      )
                      print('สมัครเสร็จสิ้น')
                      request.session['Emp_id'] = Speaker_Userid
                    return redirect('index')
    #except :
      #if request.method == 'POST':
            #return redirect('index')  
        return render(request,'register.html',{'context' : context})

def idm_login(Emp_id, Emp_pass):
    print('--------------------')
    
    url="https://idm.pea.co.th/webservices/idmservices.asmx?WSDL"
    headers = {'content-type': 'text/xml'}
    xmltext ='''<?xml version="1.0" encoding="utf-8"?>
                 <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <IsValidUsernameAndPassword_SI xmlns="http://idm.pea.co.th/">
                        <WSAuthenKey>{0}</WSAuthenKey>
                        <Username>{1}</Username>
                        <Password>{2}</Password>
                        </IsValidUsernameAndPassword_SI>
                    </soap:Body>
                </soap:Envelope>'''
    wskey = '07d75910-3365-42c9-9365-9433b51177c6'
    body = xmltext.format(wskey,Emp_id,Emp_pass)
    response = requests.post(url,data=body,headers=headers)
    print(response.status_code)
    o = xmltodict.parse(response.text)
    jsonconvert=dict(o)
    # print(o)
    authen_response = jsonconvert["soap:Envelope"]["soap:Body"]["IsValidUsernameAndPassword_SIResponse"]["IsValidUsernameAndPassword_SIResult"]["ResultObject"]
    return authen_response

def idm(Emp_id):
    url="https://idm.pea.co.th/webservices/EmployeeServices.asmx?WSDL"
    headers = {'content-type': 'text/xml'}
    xmltext ='''<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <GetEmployeeInfoByEmployeeId_SI xmlns="http://idm.pea.co.th/">
                        <WSAuthenKey>{0}</WSAuthenKey>
                        <EmployeeId>{1}</EmployeeId>
                        </GetEmployeeInfoByEmployeeId_SI>
                </soap:Body>
                </soap:Envelope>'''
    wsauth = 'e7040c1f-cace-430b-9bc0-f477c44016c3'
    body = xmltext.format(wsauth,Emp_id)
    response = requests.post(url,data=body,headers=headers)
    o = xmltodict.parse(response.text)
    # print(o)
    jsonconvert=o["soap:Envelope"]['soap:Body']['GetEmployeeInfoByEmployeeId_SIResponse']['GetEmployeeInfoByEmployeeId_SIResult']['ResultObject']
    employeedata = dict(jsonconvert)
    # print(employeedata['FirstName'])
    # print(employeedata['NewOrganizationalCode'])
    return employeedata


def virtual(request,Room):
    try:
      context = {
          'latest_question_list': Room,
          'Emp_id' : '',
          'Ex_id' : '',
      }
      check_num = Internal_User.objects.filter(Inuser_id = request.session['Emp_id']).count()
      print('pass')
      if check_num >= 1:
        data = Internal_User.objects.get(Inuser_id = request.session['Emp_id'])
        data2 = data.Inuser_name + ' ' + data.Inuser_lastname
        context['Emp_id'] = data2
        print(context['Ex_id'])
      else:
        check_num2 = External_User.objects.filter(Exuser_tel = request.session['Emp_id']).count()
        if check_num2 >= 1:
          data = External_User.objects.get(Exuser_tel = request.session['Emp_id'])
          print('pass')
          data2 = data.Exuser_name + ' ' + data.Exuser_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
        else:
          data =Speaker_user.objects.get(Speaker_Userid = request.session['Emp_id'])
          print('pass')
          data2 = data.Speaker_name + ' ' + data.Speaker_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
    except :
      return redirect('loginuser')
    return render(request,'virtual.html',{'context' : context})

def about(request):
    try:
      context = {
          'latest_question_list': "About",
          'Emp_id' : '',
          'Ex_id' : '',
      }
      check_num = Internal_User.objects.filter(Inuser_id = request.session['Emp_id']).count()
      print('pass')
      if check_num >= 1:
        data = Internal_User.objects.get(Inuser_id = request.session['Emp_id'])
        data2 = data.Inuser_name + ' ' + data.Inuser_lastname
        context['Emp_id'] = data2
        print(context['Ex_id'])
      else:
        check_num2 = External_User.objects.filter(Exuser_tel = request.session['Emp_id']).count()
        if check_num2 >= 1:
          data = External_User.objects.get(Exuser_tel = request.session['Emp_id'])
          print('pass')
          data2 = data.Exuser_name + ' ' + data.Exuser_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
        else:
          data =Speaker_user.objects.get(Speaker_Userid = request.session['Emp_id'])
          print('pass')
          data2 = data.Speaker_name + ' ' + data.Speaker_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
    except :
      return redirect('loginuser')
    return render(request,'about.html',{'context' : context})

@csrf_exempt
def paper(request,Group):
    #try:
        if Group == 1:
            name = "Power and Energy"
        elif Group == 2:
            name = "Innovation and Technology"
        elif Group == 3:
            name = "New Business and Marketing"
        elif Group == 4:
            name = "Human Resource / Financial / Accounting / Strategy"
        elif Group == 5:
            name = "Sharing Idea"
        context = {
          'title': name,
          'Emp_id' : '',
        }
        print(request.session['Emp_id'])
        check_num = Internal_User.objects.filter(Inuser_id = request.session['Emp_id']).count()
        print('pass')
        if check_num >= 1:
          data = Internal_User.objects.get(Inuser_id = request.session['Emp_id'])
          data2 = data.Inuser_name + ' ' + data.Inuser_lastname
          context['Emp_id'] = data2
        else:
          check_num2 = External_User.objects.filter(Exuser_tel = request.session['Emp_id']).count()
          if check_num2 >= 1:
            data = External_User.objects.get(Exuser_tel = request.session['Emp_id'])
            print('pass','fubukai',data)
            data2 = data.Exuser_name + ' ' + data.Exuser_lastname
            print(data2)
            context['Emp_id'] = data2
            print(context['Emp_id'])
          else:
            data =Speaker_user.objects.get(Speaker_Userid = request.session['Emp_id'])
            print('pass','else',data)
            data2 = data.Speaker_name + ' ' + data.Speaker_lastname
            print(data2)
            context['Emp_id'] = data2
            print(context['Emp_id'])
        paper = {
            'paper' : ' ',
        }
        paper = Paper.objects.all().order_by('Paper_reward')
        Emp_id = request.session['Emp_id'] #หลังจากต่อ IDM
        if request.method =='POST':
                print('fubukai',Emp_id)
                papers = request.POST.get('papers')
                get_paper = Paper.objects.get(PK_ID = papers)
                print(papers,get_paper)
                if likes.objects.filter(papers = get_paper ,user = Emp_id):
                    print('fubukai if',Emp_id)
                    delete_like = likes.objects.filter(papers = get_paper ,user = Emp_id).delete()
                    new_paper = Paper.objects.get(PK_ID = papers)
                    print(new_paper,'+')
                    new_paper.Paper_like -= 1 
                    new_paper.save()
                else:
                    print('fubukai else',Emp_id)
                    update_like = likes.objects.create(
                      papers = Paper.objects.get(PK_ID = papers),
                      user = Emp_id
                    )
                    new_paper = Paper.objects.get(PK_ID = papers)
                    print(new_paper,'-')
                    new_paper.Paper_like += 1 
                    new_paper.save()
    #except :
      #return redirect('loginuser')
        return render(request,'paper.html',{'context' : context,'paper' : paper})

def agenda(request,Date):
    try:
      context = {
          'Emp_id' : '',
          'Ex_id' : '',
          'date' : Date,
      }
      check_num = Internal_User.objects.filter(Inuser_id = request.session['Emp_id']).count()
      print('pass')
      if check_num >= 1:
        data = Internal_User.objects.get(Inuser_id = request.session['Emp_id'])
        data2 = data.Inuser_name + ' ' + data.Inuser_lastname
        context['Emp_id'] = data2
        print(context['Ex_id'])
      else:
        check_num2 = External_User.objects.filter(Exuser_tel = request.session['Emp_id']).count()
        if check_num2 >= 1:
          data = External_User.objects.get(Exuser_tel = request.session['Emp_id'])
          print('pass')
          data2 = data.Exuser_name + ' ' + data.Exuser_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
        else:
          data =Speaker_user.objects.get(Speaker_Userid = request.session['Emp_id'])
          print('pass')
          data2 = data.Speaker_name + ' ' + data.Speaker_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
    except :
        return redirect('loginuser')
    return render(request,'agenda.html',{'context' : context})

def survey(request):
      context = {
          'title': "survey",
          'Emp_id' : '',
          'Ex_id' : '',
      }
      check_num = Internal_User.objects.filter(Inuser_id = request.session['Emp_id']).count()
      print('pass')
      if check_num >= 1:
        data = Internal_User.objects.get(Inuser_id = request.session['Emp_id'])
        data2 = data.Inuser_name + ' ' + data.Inuser_lastname
        context['Emp_id'] = data2
        print(context['Ex_id'])
      else:
        check_num2 = External_User.objects.filter(Exuser_tel = request.session['Emp_id']).count()
        if check_num2 >= 1:
          data = External_User.objects.get(Exuser_tel = request.session['Emp_id'])
          print('pass')
          data2 = data.Exuser_name + ' ' + data.Exuser_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
        else:
          data =Speaker_user.objects.get(Speaker_Userid = request.session['Emp_id'])
          print('pass')
          data2 = data.Speaker_name + ' ' + data.Speaker_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
      if request.method == 'POST':
            survey_score1 = request.POST.get('survey_score1')
            survey_score2 = request.POST.get('survey_score2')
            survey_score3 = request.POST.get('survey_score3')
            survey_score4 = request.POST.get('survey_score4')
            survey_score5 = request.POST.get('survey_score5')
            survey_score6 = request.POST.get('survey_score6')
            survey_score7 = request.POST.get('survey_score7')
            survey_comment = request.POST.get('survey_comment')
            new_survey = surveys.objects.create(
              survey_id = context['Emp_id'],
              survey_score1 = survey_score1,
              survey_score2 = survey_score2,
              survey_score3 = survey_score3,
              survey_score4 = survey_score4,
              survey_score5 = survey_score5,
              survey_score6 = survey_score6,
              survey_score7 = survey_score7,
              survey_comment = survey_comment,
            )
            return redirect('index')
      return render(request,'survey.html',{'context' : context})

def contact(request):
    try:
      
      context = {
          'title': "contact",
          'Emp_id' : '',
          'Ex_id' : '',
      }
      check_num = Internal_User.objects.filter(Inuser_id = request.session['Emp_id']).count()
      print('pass')
      if check_num >= 1:
        data = Internal_User.objects.get(Inuser_id = request.session['Emp_id'])
        data2 = data.Inuser_name + ' ' + data.Inuser_lastname
        context['Emp_id'] = data2
        print(context['Ex_id'])
      else:
        check_num2 = External_User.objects.filter(Exuser_tel = request.session['Emp_id']).count()
        if check_num2 >= 1:
          data = External_User.objects.get(Exuser_tel = request.session['Emp_id'])
          print('pass')
          data2 = data.Exuser_name + ' ' + data.Exuser_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
        else:
          data =Speaker_user.objects.get(Speaker_Userid = request.session['Emp_id'])
          print('pass')
          data2 = data.Speaker_name + ' ' + data.Speaker_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
    except :
      return redirect('loginuser')
    return render(request,'contact.html',{'context' : context})

def detail_paper(request,papers):
    try:
      get_paper = Paper.objects.get(PK_ID = papers)
      context = {
          'Paper_No': papers,
          'Emp_id' : '',
          'Ex_id' : '',
      }
      check_num = Internal_User.objects.filter(Inuser_id = request.session['Emp_id']).count()
      print('pass')
      if check_num >= 1:
        data = Internal_User.objects.get(Inuser_id = request.session['Emp_id'])
        data2 = data.Inuser_name + ' ' + data.Inuser_lastname
        context['Emp_id'] = data2
        print(context['Ex_id'])
      else:
        check_num2 = External_User.objects.filter(Exuser_tel = request.session['Emp_id']).count()
        if check_num2 >= 1:
          data = External_User.objects.get(Exuser_tel = request.session['Emp_id'])
          print('pass')
          data2 = data.Exuser_name + ' ' + data.Exuser_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
        else:
          data =Speaker_user.objects.get(Speaker_Userid = request.session['Emp_id'])
          print('pass')
          data2 = data.Speaker_name + ' ' + data.Speaker_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
    except :
      return redirect('loginuser')
    return context

@csrf_exempt
def detail(request,Papers):
    try:
      context = {
          'title': "contact",
          'Owner' : "",
          'Papers_name' : "",
          'Papers_num': "",
          'Papers_PDF' : "",
          'Emp_id' : '',
          'Ex_id' : '',
      }
      check_num = Internal_User.objects.filter(Inuser_id = request.session['Emp_id']).count()
      print('pass')
      if check_num >= 1:
        data = Internal_User.objects.get(Inuser_id = request.session['Emp_id'])
        data2 = data.Inuser_name + ' ' + data.Inuser_lastname
        context['Emp_id'] = data2
        print(context['Ex_id'])
      else:
        check_num2 = External_User.objects.filter(Exuser_tel = request.session['Emp_id']).count()
        if check_num2 >= 1:
          data = External_User.objects.get(Exuser_tel = request.session['Emp_id'])
          print('pass')
          data2 = data.Exuser_name + ' ' + data.Exuser_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
        else:
          data =Speaker_user.objects.get(Speaker_Userid = request.session['Emp_id'])
          print('pass')
          data2 = data.Speaker_name + ' ' + data.Speaker_lastname
          print(data2)
          context['Emp_id'] = data2
          print(context['Emp_id'])
      try:
          get_paper = Paper.objects.get(PK_ID = Papers)
          print('fubukai', get_paper)
          get_owner = Creater.objects.filter(Creater_own = get_paper)
          print(get_owner)
          print('fubukai',get_paper.Paper_download)
          get_paper.Paper_download = get_paper.Paper_download + 1
          get_paper.save()
          context['Papers_name'] = get_paper.Paper_name
          context['Papers_num'] = get_paper.Paper_download
          context['Papers_PDF'] = get_paper.Paper_PDF
          context['Paper_type'] = get_paper.Paper_type
          context['Paper_details'] = get_paper.Paper_details
          context['Owner'] = get_owner
      except:
          print('pass', context['Owner'])
    except :
      return redirect('loginuser')
    return render(request,'detail.html',{'context' : context})

def check(request):
  context = Speaker_user.objects.all()
  return render(request,'check.html',{'context' : context})

def check2(request):
  Emp_id = request.session['Emp_id']
  if Emp_id == 281606 or Emp_id ==  466311 or Emp_id ==  497074 or Emp_id == 510951 or Emp_id == '281606' or Emp_id ==  '466311' or Emp_id ==  '497074' or Emp_id == '510951' :
    context = External_User.objects.all()
    context2 = Internal_User.objects.all()
    return render(request,'check2.html',{'context' : context,'context2' : context2})
  else:
    return redirect('loginuser')


@csrf_exempt
def reset_password(request):
    context = {
          'latest_question_list': 'sss',
    }
    request.session['checkdata'] = 0
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        user_name = request.POST.get('username')
        user_password =  escape(request.POST.get('userEmail'))
        print("user_type",user_type,user_name,user_password)
              # 1 = หน่วยงานภายนอก 
              # 2 = หน่วยงานภายใน
        if user_type == '1' or user_type == 1:
          print(user_type)
          check_ID = External_User.objects.filter(Exuser_tel = user_name).filter(Exuser_password = user_password).count()
          if check_ID == 1:
              request.session['Emp_id'] = user_name
              context['latest_question_list'] = 'xxx'
              print('pass','เปลี่ยนรหัสผ่าน')
              data = External_User.objects.get(Exuser_tel = request.session['Emp_id'])
              data.Exuser_password = escape(request.POST.get('userpassword'))
              print(request.POST.get('userpassword'))
              data.save()
              try:
                  context['DATA'] = External_User.objects.get(Exuser_tel = user_name)
                  return redirect('index')     
              except:
                  return redirect('register',1)
                    # check Exuser
        elif user_type == '2' or user_type == 2 :
              print(user_type)
              check_internaluser = idm_login(user_name,user_password)
              #check_internaluser = 'true'
              print(check_internaluser)
              if check_internaluser == 'true':
                  request.session['Emp_id'] = user_name
                  try: 
                    data = Internal_User.objects.get(Inuser_id = user_name)
                    data2 = User_do.objects.filter(user_name = data.Inuser_name , user_lastname = data.Inuser_lastname , user_logindate = date.today(), user_type = 2).count()
                    if data2 <= 0 :
                      new_list = User_do.objects.create(
                        user_name = data.Inuser_name,
                        user_lastname = data.Inuser_lastname,
                        user_type = 2,
                        user_tel = data.Inuser_tel,
                      )
                    return redirect('index')
                  except:
                    return redirect('register',2)
        elif user_type == '3':
                print(user_type)
                check_ID = Speaker_user.objects.filter(Speaker_Userid = user_name).filter(Speaker_password = user_password).count()
                if check_ID == 1:
                  print('รหัสถูก')
                  request.session['Emp_id'] = user_name
                  context['latest_question_list'] = 'xxx'
                  try:
                    context['DATA'] = Speaker_user.objects.get(Speaker_Userid = user_name)
                    return redirect('index')     
                  except:
                    return redirect('register',3)
    return render(request,'reset.html')

def game(request):
  Emp_id = request.session['Emp_id']
  if Emp_id == 281606 or Emp_id ==  466311 or Emp_id ==  497074 or Emp_id == 510951 or Emp_id == '281606' or Emp_id ==  '466311' or Emp_id ==  '497074' or Emp_id == '510951' :
    context = User_do.objects.all()
    return render(request,'game.html',{'context' : context})
  else:
    return redirect('loginuser')

def export_users_xls2(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="User.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('วันที่ 30')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['ชื่อ','นามสกุล','หน่วยงาน','เบอร์โทรศัพท์','อีเมลล์','ที่อยู่']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    data_row = []
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    row1 = User_do.objects.filter(user_logindate = '2021-11-30').values_list('user_name','user_lastname','user_type')
    for i in row1:
      try:
        data = External_User.objects.get(Exuser_name = i[0] ,Exuser_lastname = i[1])
        print(data,'1')
        data_row.append((data.Exuser_name,data.Exuser_lastname,'หน่วยงานภายนอก',data.Exuser_tel,data.Exuser_email,data.Exuser_address))
      except:
        data = Internal_User.objects.get(Inuser_name = i[0] ,Inuser_lastname = i[1])
        print(data,'2')
        data_row.append((data.Inuser_name,data.Inuser_lastname,'หน่วยงานภายใน',data.Inuser_tel,data.Inuser_email,data.Inuser_address,data.Inuser_id))
    for row in data_row:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    
    ws = wb.add_sheet('วันที่ 1')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['ชื่อ','นามสกุล','หน่วยงาน']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    row1 = User_do.objects.filter(user_logindate = '2021-12-01').values_list('user_name','user_lastname','user_type')
    
    data_row = []
    for i in row1:      
      try:
        data = External_User.objects.get(Exuser_name = i[0] ,Exuser_lastname = i[1])
        print(data,'1')
        data_row.append((data.Exuser_name,data.Exuser_lastname,'หน่วยงานภายนอก',data.Exuser_tel,data.Exuser_email,data.Exuser_address))
      except:
        data = Internal_User.objects.get(Inuser_name = i[0] ,Inuser_lastname = i[1])
        print(data,'2')
        data_row.append((data.Inuser_name,data.Inuser_lastname,'หน่วยงานภายใน',data.Inuser_tel,data.Inuser_email,data.Inuser_address,data.Inuser_id))
    for row in data_row:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
                    
    wb.save(response)
    return response

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="User.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('วันที่ 30')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['ลำดับ','รหัสพนักงาน','ชื่อ','นามสกุล','ต่ำแหน่ง','หน่วยงาน','อีเมลล์','เบอร์โทรศัพท์','ที่อยู่']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    data_row = []
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    row1 = Internal_User.objects.all().values_list('PK_Inuser',	'Inuser_id', 'Inuser_name' ,'Inuser_lastname','Inuser_position', 'Inuser_Ageny' ,'Inuser_email', 'Inuser_tel' ,'Inuser_address')
    for row in row1:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
  
    wb.save(response)
    return response