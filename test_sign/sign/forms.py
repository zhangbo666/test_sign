#!/usr/bin/python
# encoding:utf-8

from django import forms

from sign.models import Event,Guest

'''
forms django表单

1、创建一个 forms.py 文件

   导入 from django import forms

   # 不能用表单读入数据，需要用下面创建class
   创建class xxx(forms.Form):

   字段1 = forms.CharField(label="名称",max_length=100)
   字段2 = forms.CharField(label="描述",widget=forms.Textarea) # 文本区域
   字段3 = forms.EmailField() # Email 类型
   字段4 = forms.BooleanField(required=False) # 布尔类型


   创建class xxx(forms.ModelForm):

        class Meta:

            model = 表名

            fields = ['name','describe','status']


2、引forms文件 路径包

   if request.method == 'POST':

      ProjectForm(request.POST)

       if form.is_valid():

           name = form.cleaned_data['name']


           describe = form.cleaned_data['describe']

           status   = form.cleaned_data['status']

           p_update = Project.objects.get(id=pid)

           p_update.name = name

           p_update.describe = describe

           p_update.status = status

           p_update.save()

           return HttpResponseRedirect("/project/")

   elif request.method == 'GET':

        if pid :

            form = ProjectForm()

            return render(request,'xxx.html',{'form':form})

3、html文件中，渲染form表单
   <form action="//" method="post">

       {{ form }}
       <input type="submit" value="submit">

   </form>

4、django forms 表单语法

   {{ form.as_p }}->换行

5、表单读入数据

   pro = Project.objects.get(id=pid)

   form = ProjectForm(instance=pro)

   return render(request,"project.html",{"type":"edit","form":form})

'''


# class ProjectForm(forms.Form):

# name = forms.CharField(label="名称",max_length=100)
# describe = forms.CharField(label="描述",widget=forms.Textarea)
# status = forms.BooleanField(label="状态",required=True)


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = ['name', 'limit', 'address','status']


