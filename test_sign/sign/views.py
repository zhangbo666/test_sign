from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.contrib import auth

from django.contrib.auth.decorators import login_required

from sign.models import Event,Guest

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.shortcuts import get_object_or_404


# Create your views here.


# 发布会登录页
def index(request):

    return render(request,"index.html")


# 发布会管理
@login_required
def event_manage(request):

    username = request.session.get('user','')

    events = Event.objects.all()

    paginator = Paginator(events,3)

    # 传一个页面数据get参数的值
    page = request.GET.get('page')

    print (page)

    try:

        # 获取page参数的值
        contacts = paginator.page(page)

        print ("contacts---------->1",contacts)

    except PageNotAnInteger:

        contacts = paginator.page(1)

        print ("contacts---------->2",contacts)

    except EmptyPage:

        contacts = paginator.page(paginator.num_pages)

        print ("contacts---------->3",contacts)

    print("contacts---------->4", contacts)

    return render(request,"event_manage.html",{"user":username,"events":contacts})

    # return render(request,"event_manage.html",{"user":username,"events":events})


# 发布会名称搜索
@login_required
def search_name(request):

    username = request.session.get('user','')

    search_name = request.GET.get('name','')

    events = Event.objects.filter(name__contains=search_name)


    if len(events) == 0:

        return render(request,"event_manage.html",{"user":username,"hint":"搜索'发布会'查询结果为空"})

    paginator = Paginator(events,2)

    # 传一个页面数据
    page = request.GET.get('page')

    try:

        contacts = paginator.page(page)

    except PageNotAnInteger:

        contacts = paginator.page(1)

    except EmptyPage:

        contacts = paginator.page(paginator.num_pages)

    return render(request,"event_manage.html",{"user":username,"events":contacts,"name":search_name})




# 发布会管理系统退出
@login_required
def logout(request):

    auth.logout(request)

    return HttpResponseRedirect("/index/")


# 发布会管理系统登录
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

    paginator = Paginator(guests,5)

    # 传一个页面数据get参数的值
    page = request.GET.get('page')

    print (page)

    try:

        contacts = paginator.page(page)

        print ("contacts---------->1",contacts)

    except PageNotAnInteger:

        contacts = paginator.page(1)

        print ("contacts---------->2",contacts)

    except EmptyPage:

        contacts = paginator.page(paginator.num_pages)

        print ("contacts---------->3",contacts)

    print ("contacts---------->4",contacts)

    return render(request,"guest_manage.html",{"user":username,"guests":contacts})


# 嘉宾手机号搜索
@login_required
def search_phone(request):

    username = request.session.get('user','')

    search_phone = request.GET.get('phone','')

    guests = Guest.objects.filter(phone__contains=search_phone)

    if len(guests) == 0:

        return render(request,"guest_manage.html",{"user":username,"hint":"搜索'手机号'查询结果为空"})

    paginator = Paginator(guests,5)

    # 传一个页面数据
    page = request.GET.get('page')

    try:

        contacts = paginator.page(page)

    except PageNotAnInteger:

        contacts = paginator.page(1)

    except EmptyPage:

        contacts = paginator.page(paginator.num_pages)

    return render(request,"guest_manage.html",{"user":username,"guests":contacts,"phone":search_phone})


# 嘉宾签到页面
@login_required
def sign_index(request,event_id):

    event = get_object_or_404(Event,id = event_id)

    guest_list = Guest.objects.filter(event_id=event_id)  #某个发布会的签到人数

    guest_list = len(guest_list)

    sign_list = Guest.objects.filter(sign="1",event_id = event_id) # 某个发布会的签到完成人数

    sign_list = len(sign_list)

    return render(request,"sign_index.html",{"event":event,
                                             "guest_list":guest_list,
                                             "sign_list":sign_list})


# 嘉宾签到处理
@login_required
def sign_index_action(request,event_id):

    event = get_object_or_404(Event,id = event_id)

    guest_list = Guest.objects.filter(event_id=event_id)  #某个发布会的签到人数

    guest_list = len(guest_list)

    sign_list = Guest.objects.filter(sign="1",event_id = event_id) # 某个发布会的签到完成人数

    sign_list = len(sign_list)

    phone = request.POST.get('phone','')

    result = Guest.objects.filter(phone=phone)

    if not result:

        return render(request,'sign_index.html',{'event':event,
                                                 'error':'手机号错误或为空！！！',
                                                 'guest_list':guest_list,
                                                 'sign_list':sign_list})

    result = Guest.objects.filter(phone=phone,event_id=event_id)

    if not result:

        return render(request,'sign_index.html',{'event':event,
                                                 'error':'当前手机号与本次发布会信息绑定不一致，无法进行签到！！！',
                                                 'guest_list':guest_list,
                                                 'sign_list':sign_list})

    result = Guest.objects.get(phone=phone,event_id=event_id)

    if result.sign:

        return render(request,'sign_index.html',{'event':event,
                                                 'error':'该用户已签到！！！',
                                                 'guest_list':guest_list,
                                                 'sign_list':sign_list})

    else:

        Guest.objects.filter(event_id=event_id,phone=phone).update(sign = '1')

        sign_list = Guest.objects.filter(sign="1", event_id=event_id)  # 某个发布会的签到完成人数

        sign_list = len(sign_list)

        return render(request,'sign_index.html',{'event':event,
                                                 'error':'该用户签到成功！！！',
                                                 'guest_list':guest_list,
                                                 'sign_list':sign_list,
                                                 'sign_user':result,})



