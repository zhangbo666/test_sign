from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.contrib import auth

from django.contrib.auth.decorators import login_required

from sign.models import Event,Guest

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.shortcuts import get_object_or_404

from datetime import datetime

from sign.forms import EventForm,GuestForm


# Create your views here.


# 发布会登录页
def index(request):

    return render(request,"index.html")


# 发布会管理
@login_required
def event_manage(request):

    username = request.session.get('user','')

    # events = Event.objects.all()
    events = Event.objects.order_by('id') #按照id升序

    paginator = Paginator(events,5)

    paginator_count = paginator.count

    paginator_num_pages = paginator.num_pages

    l1 = []

    for n1 in range (1,paginator_num_pages+1):

        l1.append(n1)

    # 传一个页面数据get参数的值
    page = request.GET.get('page')
    # print (page)

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

    return render(request,"event_manage.html",{"user":username,"events":contacts,
                                               "type":"list","search_result":"result_data",
                                               "nums":l1,"page":page})

    # return render(request,"event_manage.html",{"user":username,"events":events})


# 发布会名称搜索
@login_required
def search_name(request):

    username = request.session.get('user','')

    search_name = request.GET.get('name','')

    events = Event.objects.filter(name__contains=search_name).order_by('id') #按照id升序

    if len(events) == 0:

        return render(request,"event_manage.html",{"user":username,"type":"list",
                                                   "search_result":"result_not",
                                                   "hint":"搜索发布会查询结果为空，请重新查询！！！"})

    paginator = Paginator(events,5)

    # 传一个页面数据
    page = request.GET.get('page')

    try:

        contacts = paginator.page(page)

    except PageNotAnInteger:

        contacts = paginator.page(1)

    except EmptyPage:

        contacts = paginator.page(paginator.num_pages)

    return render(request,"event_manage.html",{"user":username,"events":contacts,
                                               "type":"list","search_result":"result_data",
                                               "name":search_name})


# 添加发布会
@login_required
def add_event(request):

    if request.method == 'GET':

        return render(request,"event_manage.html",{"type":"add"})

    elif request.method == 'POST':

        event_name = request.POST.get("event_name","")

        event_address = request.POST.get("event_address","")

        event_status = request.POST.get("event_status","")

        event_limit = request.POST.get("event_limit","")

        if event_name == "":

            return render(request,"event_manage.html",{"type":"add","reset":"reset","event_name":"发布会名称不能为空"})

        elif event_address == "":

            return render(request,"event_manage.html",{"type":"add","event_address":"发布会地址不能为空"})

        elif event_limit == "":

            return render(request,"event_manage.html",{"type":"add","event_limit":"发布会参加人数不能为空"})

        else:

            Event.objects.create(name=event_name,address=event_address,status=event_status,limit=event_limit,
                                 start_time=datetime(2020,4,3,00,10,00))

            return HttpResponseRedirect("/event_manage/")

# 编辑发布会
@login_required
def edit_event(request, pid):

    if request.method == 'GET':

        if pid:

            pro = Event.objects.get(id=pid)

            form = EventForm(instance=pro)

            return render(request, "event_manage.html", {"type": "edit", "form": form, "pid": pid})

    elif request.method == 'POST':

        form = EventForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data['name']

            limit = form.cleaned_data['limit']

            address = form.cleaned_data['address']

            status = form.cleaned_data['status']

            p_update = Event.objects.get(id=pid)

            print (p_update)

            p_update.name = name

            p_update.limit = limit

            p_update.status = status

            p_update.address = address

            p_update.save()

    return HttpResponseRedirect("/event_manage/")


# 编辑发布会
# @login_required
# def edit_event(request, pid):
#
#     if request.method == 'GET':
#
#         if pid:
#
#             event_name = Event.objects.get(id=pid).name
#             event_address = Event.objects.get(id=pid).address
#             event_status = Event.objects.get(id=pid).status
#             event_limit = Event.objects.get(id=pid).limit
#
#             return render(request, "event_manage.html", {"type":"edit","pid":pid,
#                                                          "event_name":event_name,
#                                                          "event_address":event_address,
#                                                          "event_status":event_status,
#                                                          "event_limit":event_limit})
#
#     elif request.method == 'POST':
#
#         event_name = request.POST.get("event_name","")
#
#         event_address = request.POST.get("event_address","")
#
#         event_status = request.POST.get("event_status","")
#
#         event_limit = request.POST.get("event_limit","")
#
#         if event_name == "":
#
#             return render(request,"event_manage.html",{"type":"edit","event_name_error":"发布会名称不能为空",
#                                                        "event_address":event_address,
#                                                        "event_status":event_status,
#                                                        "event_limit":event_limit})
#
#         elif event_address == "":
#
#             return render(request,"event_manage.html",{"type":"edit","event_address_error":"发布会地址不能为空",
#                                                        "event_name": event_name,
#                                                        "event_status": event_status,
#                                                        "event_limit": event_limit})
#
#         elif event_limit == "":
#
#             return render(request,"event_manage.html",{"type":"edit","event_limit_error":"发布会参加人数不能为空",
#                                                        "event_name": event_name,
#                                                        "event_address": event_address,
#                                                        "event_status": event_status})
#         else:
#
#             event_info = Event.objects.get(id=pid)
#
#             event_info.name = event_name
#
#             event_info.address = event_address
#
#             event_info.status = event_status
#
#             event_info.limit = event_limit
#
#             event_info.save()
#
#             return HttpResponseRedirect("/event_manage/")





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

        if username == "" or password == "":

            return  render(request,"index.html",{"error":"username or password null"})

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

                return render(request,'index.html', {'error': "username or password error"})

    elif request.method == 'GET':

            return render(request, 'index.html')




# 嘉宾管理
@login_required
def guest_manage(request):

    username = request.session.get('user','')

    # guests = Guest.objects.all()
    guests = Guest.objects.order_by('id') #按照id升序

    paginator = Paginator(guests,5)

    # 传一个页面数据get参数的值
    page = request.GET.get('page')

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

    return render(request,"guest_manage.html",{"user":username,"guests":contacts,
                                               "type": "list", "search_result": "result_data",})


# 嘉宾手机号搜索
@login_required
def search_phone(request):

    username = request.session.get('user','')

    search_phone = request.GET.get('phone','')

    guests = Guest.objects.filter(phone__contains=search_phone).order_by('id') #按照id升序

    if len(guests) == 0:

        return render(request,"guest_manage.html",{"user":username,"type":"list",
                                                   "search_result":"result_not",
                                                   "hint":"搜索嘉宾查询结果为空，请重新查询！！！"})

    paginator = Paginator(guests,5)

    # 传一个页面数据
    page = request.GET.get('page')

    try:

        contacts = paginator.page(page)

    except PageNotAnInteger:

        contacts = paginator.page(1)

    except EmptyPage:

        contacts = paginator.page(paginator.num_pages)

    return render(request,"guest_manage.html",{"user":username,"guests":contacts,
                                               "type":"list","search_result":"result_data",
                                               "phone":search_phone})


# 添加嘉宾
@login_required
def add_guest(request):

    events = Event.objects.all().order_by('id')

    if request.method == 'GET':

        return render(request,"guest_manage.html",{"type":"add","events":events})

    elif request.method == 'POST':

        guest_name = request.POST.get("guest_name","")

        guest_phone = request.POST.get("guest_phone","")

        guest_email = request.POST.get("guest_email","")

        guest_status = request.POST.get("guest_status","")

        event_name = request.POST.get("event_name","")

        event_id = Event.objects.get(name=event_name)

        #发布会id
        event_id   = event_id.id

        if guest_name == "":

            return render(request,"guest_manage.html",{"type":"add","guest_name":"嘉宾姓名不能为空",
                                                       "events":events})

        elif guest_phone == "":

            return render(request,"guest_manage.html",{"type":"add","guest_phone":"嘉宾手机号不能为空",
                                                       "events":events})

        elif guest_email == "":

            return render(request,"guest_manage.html",{"type":"add","guest_email":"嘉宾邮箱不能为空",
                                                       "events":events})

        elif event_name == "":

            return render(request,"guest_manage.html",{"type":"add","event_name":"嘉宾关联发布会未选择"})

        else:

            Guest.objects.create(realname=guest_name,phone=guest_phone,email=guest_email,
                                 sign=guest_status,event_id=event_id,create_time=datetime(2020,3,7,1,10,00))

            return HttpResponseRedirect("/guest_manage/")


# 编辑嘉宾
@login_required
def edit_guest(request, pid):

    if request.method == 'GET':

        if pid:

            pro = Guest.objects.get(id=pid)

            form = GuestForm(instance=pro)

            return render(request, "guest_manage.html", {"type": "edit", "form": form, "pid": pid})

    elif request.method == 'POST':

        form = GuestForm(request.POST)

        if form.is_valid():

            realname = form.cleaned_data['realname']

            # phone = form.cleaned_data['phone']

            email = form.cleaned_data['email']

            sign = form.cleaned_data['sign']

            event = form.cleaned_data['event']

            p_update = Guest.objects.get(id=pid)

            print ("p_update---->",p_update)

            p_update.realname = realname

            # p_update.phone = phone

            p_update.email = email

            p_update.sign = sign

            p_update.event = event

            p_update.save()

        else:

            print ("form.errors----->",form.errors)

    return HttpResponseRedirect("/guest_manage/")




# 嘉宾签到页面
@login_required
def sign_index(request,event_id):

    event = get_object_or_404(Event,id = event_id)

    guest_list = Guest.objects.filter(event_id=event_id)  #某个发布会的签到人数

    guest_list = len(guest_list)

    sign_list = Guest.objects.filter(sign="1",event_id = event_id) #某个发布会的签到完成人数

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

    sign_list = Guest.objects.filter(sign="1",event_id = event_id) #某个发布会的签到完成人数

    sign_list = len(sign_list)

    phone = request.POST.get('phone','')

    result = Guest.objects.filter(phone=phone)

    error1 = "手机号错误或为空！！！"
    error2 = "当前手机号与本次发布会信息绑定不一致，无法进行签到！！！"
    error3 = "该用户已签到！！！"
    error4 = "该用户签到成功！！！"

    if not result:

        return render(request,'sign_index.html',{'event':event,
                                                 'error':'phone error.',
                                                 'guest_list':guest_list,
                                                 'sign_list':sign_list})

    result = Guest.objects.filter(phone=phone,event_id=event_id)

    if not result:

        return render(request,'sign_index.html',{'event':event,
                                                 'error':'phone mismatch.',
                                                 'guest_list':guest_list,
                                                 'sign_list':sign_list})

    result = Guest.objects.get(phone=phone,event_id=event_id)

    if result.sign:

        return render(request,'sign_index.html',{'event':event,
                                                 'error':'user has sign in.',
                                                 'guest_list':guest_list,
                                                 'sign_list':sign_list})

    else:

        Guest.objects.filter(event_id=event_id,phone=phone).update(sign = '1')

        sign_list = Guest.objects.filter(sign="1", event_id=event_id)  # 某个发布会的签到完成人数

        sign_list = len(sign_list)

        return render(request,'sign_index.html',{'event':event,
                                                 'error':'sign in success!',
                                                 'guest_list':guest_list,
                                                 'sign_list':sign_list,
                                                 'sign_user':result})



