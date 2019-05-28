__author__ = 'zhangbo'


from sign.models import Event

from django.http import HttpResponse,JsonResponse

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

        result = Event.objects.filter(id=eid)

        if result:

            return JsonResponse({"status":10022,"message":"event id already exists"})

        result = Event.objects.filter(name=name)

        if result:

            return JsonResponse({"status":10023,"message":"event name already exists"})

        if status == '':

            status = 1

        return JsonResponse({"status":10024,"message":"time error"})

    else:

        return JsonResponse({"status":10031,"message":"请求方法错误"})