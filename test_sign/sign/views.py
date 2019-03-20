from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.contrib import auth

from django.contrib.auth.decorators import login_required

from sign.models import Event,Guest


# Create your views here.


# 发布会登录页
def index(request):

    return render(request,"index.html")


# 发布会管理
@login_required
def event_manage(request):

    username = request.session.get('user','')

    events = Event.objects.all()

    return render(request,"event_manage.html",{"user":username,"events":events})


# 发布会名称搜索
@login_required
def search_name(request):

    username = request.session.get('user','')

    search_name = request.GET.get('name')

    print (search_name)

    events = Event.objects.filter(name__contains=search_name)

    return render(request,"event_manage.html",{"user":username,"events":events})


# 发布会退出
@login_required
def logout(request):

    auth.logout(request)

    return HttpResponseRedirect("/index/")


# 发布会登录
def login_action(request):

    if request.method == 'POST':

        username = request.POST.get('username','')
        password = request.POST.get('password','')

        if username == " " or password == " ":

            return  render(request,"index.html",{"error":"用户账号或用户密码为空"})

        else:

            user = auth.authenticate(username=username, password=password)

            if user is not None:

                # 验证登录
                auth.login(request,user)

                #session
                response = HttpResponseRedirect('/event_manage/')

                #将 session 信息记录到浏览器
                request.session['user'] = username

                return response

            else:

                return render(request,'index.html', {'error': "用户账号或用户密码输入错误"})

    elif request.method == 'GET':

            return render(request, 'index.html')




# 嘉宾管理
@login_required
def guest_manage(request):

    username = request.session.get('user','')

    guests = Guest.objects.all()

    print (guests)

    return render(request,"guest_manage.html",{"user":username,"guests":guests})


# 嘉宾手机号搜索
@login_required
def search_phone(request):

    username = request.session.get('user','')

    search_phone = request.GET.get('phone')

    print (search_phone)

    guests = Guest.objects.filter(phone__contains=search_phone)

    return render(request,"guest_manage.html",{"user":username,"guests":guests})