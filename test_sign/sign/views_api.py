__author__ = 'zhangbo'


from sign.models import Event,Guest

from django.http import HttpResponse,JsonResponse

from django.core.exceptions import ValidationError,ObjectDoesNotExist

from django.db.utils import IntegrityError

import time


# 添加发布会接口
def add_event(request):

    if request.method == "POST":

        eid = request.POST.get('eid','')
        name = request.POST.get('name','')
        limit = request.POST.get('limit','')
        status = request.POST.get('status','')
        address = request.POST.get('address','')
        start_time = request.POST.get('start_time','')


        if eid == "" or name =="" or limit == "" or \
           address == "" or start_time == "":

            return JsonResponse({"status":10021,"message":"parameter error"})

        try:

            int(eid)

        except ValueError:

            return JsonResponse({"status":10025,"message":"eid类型错误"})


        result = Event.objects.filter(id=eid)


        if result:

            return JsonResponse({"status":10022,"message":"event id already exists"})

        result = Event.objects.filter(name=name)

        if result:

            return JsonResponse({"status":10023,"message":"event name already exists"})

        if status == '':

            status = 1

        try:
            Event.objects.create(id=eid,name=name,limit=limit,status=status,
                                 start_time=start_time,address=address)

        except ValidationError:

            error = 'start_time format error'

            return JsonResponse({"status":10024,"message":error})

        return JsonResponse({"status":200,"message":"添加发布会成功"})

    else:

        return JsonResponse({"status":10031,"message":"请求方法错误"})


# 查询发布会接口
def get_event_list(request):

    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')

    if eid == '' and name == '':

        return JsonResponse({"status": 10021, "message": "参数不能为空"})

    if eid != '':

        event = {}

        try:

            int(eid)

        except ValueError:

            return JsonResponse({"status": 10025, "message": "eid类型错误"})


        try:

            result = Event.objects.get(id=eid)

        except ObjectDoesNotExist:

            return JsonResponse({"status": 10022, "message": "查询结果为空"})

        else:

            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time

            return JsonResponse({"status": 200, "message": "查询正常","data":event})

    if name != '':

        datas = []

        results = Event.objects.filter(name__contains=name)

        if results:

            for r in results:

                event = {}

                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time

                datas.append(event)

            return JsonResponse({"status": 200, "message": "查询正常","data":datas})

        else:

            return JsonResponse({"status": 10022, "message": "查询结果为空"})


# 添加嘉宾接口
def add_guest(request):

    if request.method == "POST":

        eid = request.POST.get('eid', '')
        realname = request.POST.get('realname', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')

        if eid == '' or realname == '' or phone == '' or email == '':

            return JsonResponse({"status": 10021, "message": "参数不能为空"})

        try:

            int(eid)

        except ValueError:

            return JsonResponse({"status": 10022, "message": "eid类型错误"})

        result = Event.objects.filter(id=eid)

        if not result:

            return JsonResponse({"status": 10023, "message": "该发布会查询为空"})

        event_limit = Event.objects.get(id=eid).limit
        guest_limit = Guest.objects.filter(event_id=eid)

        if len(guest_limit) >= event_limit:

            return JsonResponse({"status": 10024, "message": "该发布会已满，不能添加嘉宾"})

        # 发布会时间
        event_time = Event.objects.get(id=eid).start_time
        etime = str(event_time)
        timeArray = time.strptime(etime,"%Y-%m-%d %H:%M:%S")
        e_time = int(time.mktime(timeArray))

        # 系统当前时间
        now_time = str(time.time())
        ntime = now_time.split(".")[0]
        n_time = int(ntime)

        if n_time >= e_time:

            return JsonResponse({"status": 10025, "message": "该发布会时间已过期，不能添加嘉宾"})

        try:

            Guest.objects.create(realname=realname,phone=phone,email=email,sign=0,
                                event_id=eid)

            return JsonResponse({"status":200,"message":"添加嘉宾成功"})

        except IntegrityError:

            return JsonResponse({"status": 10026, "message": "嘉宾手机号重复"})

    else:

        return JsonResponse({"status":10031,"message":"请求方法错误"})


# 查询嘉宾接口
def get_guest_list(request):

    eid = request.GET.get('eid', '')
    phone = request.GET.get('phone', '')

    if eid == '':

        return JsonResponse({"status": 10021, "message": "eid为空"})

    try:

        int(eid)

    except ValueError:

        return JsonResponse({"status": 10022, "message": "eid类型错误"})

    if eid != '' and phone == '':

        datas = []

        results = Guest.objects.filter(event_id=eid)

        if results:

            for r in results:

                guest = {}

                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                datas.append(guest)

            return JsonResponse({"status": 200, "message": "查询正常","data":datas})

        else:

            return JsonResponse({"status": 10023, "message": "查询结果为空"})

    try:

        int(phone)

    except ValueError:

        return JsonResponse({"status": 10024, "message": "phone类型错误"})

    if eid != '' and phone != '':

        guests = {}

        try:

            result = Guest.objects.get(event_id=eid,phone=phone)

        except ObjectDoesNotExist:

            return JsonResponse({"status": 10025, "message": "查询结果为空"})

        else:
            guests['realname'] = result.realname
            guests['phone'] = result.phone
            guests['email'] = result.email
            guests['sign'] = result.sign

            return JsonResponse({"status": 200, "message": "查询正常","data":guests})



# 嘉宾签到接口
def user_sign(request):

    eid = request.POST.get('eid', '')
    phone = request.POST.get('phone', '')


    if eid == '' or phone == '':

        return JsonResponse({"status": 10021, "message": "参数不能为空"})

    try:

        int(eid)

    except ValueError:

        return JsonResponse({"status": 10022, "message": "eid类型错误"})

    result = Event.objects.filter(id=eid)
    if not result:

        return JsonResponse({"status": 10023, "message": "该发布会查询为空"})

    result = Event.objects.get(id=eid).status
    if not result:

        return JsonResponse({"status": 10024, "message": "该发布会未开启，不能进行签到"})

    # 发布会时间
    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time)
    timeArray = time.strptime(etime,"%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    # 系统当前时间
    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if n_time >= e_time:

        return JsonResponse({"status": 10025, "message": "该发布会时间已过期，不能添加嘉宾"})

    result = Guest.objects.filter(phone=phone)
    if not result:

        return JsonResponse({"status": 10026, "message": "用户手机号为空"})

    result = Guest.objects.filter(event_id=eid,phone=phone)
    if not result:

        return JsonResponse({"status": 10026, "message": "改手机号与本次发布会关系不对应"})

    result = Guest.objects.get(event_id=eid,phone=phone).sign
    if result:

        return JsonResponse({"status": 10027, "message": "该用户已签到"})

    else:

        Guest.objects.filter(event_id=eid, phone=phone).update(sign='1')

        return JsonResponse({"status": 200, "message": "success"})















