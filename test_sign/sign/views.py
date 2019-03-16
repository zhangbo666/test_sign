from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.contrib import auth

from django.contrib.auth.decorators import login_required


# Create your views here.


# 发布会登录页
def index(request):

    return render(request,"index.html")


# 发布会页面
@login_required
def event_manage(request):

    username = request.session.get('user','')

    return render(request,"event_manage.html",{"user":username})


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

        print (username,password)
        if username == "" or password == "":

            return  render(request,"index.html",{"error":"用户账号或用户密码为空"})

        else:

            user = auth.authenticate(username=username, password=password)

            print (user)

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

            return render(request, 'show.html')


