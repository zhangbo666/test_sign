from django.db import models

# Create your models here.

# 创建发布会
class Event(models.Model):

    #发布会标题
    name = models.CharField(max_length=100)

    #发布会参加人数
    limit = models.IntegerField()

    #发布会状态
    status = models.BooleanField()

    #发布会地址
    address = models.CharField(max_length=200)

    #发布会时间
    start_time = models.DateTimeField()

    #发布会创建时间
    create_time = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ['-id']


    #python3.5
    def __str__(self):

        return self.name

    #python2.7
    # def __unicode__(self):
    #
    #     return self.name



# 创建嘉宾类
class Guest(models.Model):

    #关联发布会id
    event = models.ForeignKey(Event,on_delete=models.CASCADE)

    #姓名
    realname = models.CharField(max_length=64)

    #手机号
    phone = models.CharField(max_length=16)

    #邮箱
    email = models.EmailField()

    #签到状态
    sign = models.BooleanField()

    #创建时间（自动获取当前时间)
    create_time = models.DateTimeField(auto_now=True)

    class Meta:

        unique_together = ("event","phone")

        ordering = ['-id']

    #python3.5
    def __str__(self):

        return self.realname

    #python2.7
    # def __unicode__(self):
    #
    #     return self.realname









