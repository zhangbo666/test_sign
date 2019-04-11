# !usr/bin/python
# encoding:utf-8




from django.test import TestCase

from django.contrib.auth.models import User



from django.test.utils import setup_test_environment

from sign.models import Event
from sign.models import Guest


class IndexPageTest(TestCase):

    '''测试index登录首页'''

    def test_index_page_renders_index_template(self):

        '''断言模版index.html响应'''

        response = self.client.get('/index/')

        # print ("response--->",response)
        # print (response.headers)
        # print (response.status_code)
        # print (response.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')


class LoginActionTest(TestCase):

    '''初始化数据库表数据'''
    def setUp(self):

        User.objects.create_user('admin','admin@qq.com','admin123456')

    '''测试登录账号数据'''
    def test_login_user(self):

        user = User.objects.get(username='admin')

        self.assertEqual(user.username,"admin")

        self.assertEqual(user.email,"admin@qq.com")

    '''测试用户名密码为空'''
    def test_login_action_username_password_null(self):

        response = self.client.post('/login_action/',{'username': '', 'password': ''})

        self.assertEqual(response.status_code,200)

        self.assertIn(b"username or password null",response.content)

    '''测试用户名密码错误'''
    def test_login_action_username_password_error(self):

        response = self.client.post('/login_action/',{'username': 'abc', 'password': '123'})

        self.assertEqual(response.status_code,200)

        self.assertIn(b"username or password error",response.content)

    '''测试登录动作'''
    def test_login_action_success(self):

        response = self.client.post('/login_action/',{'username':'admin','password':'admin123456'})

        # print (response.status_code)

        self.assertEqual(response.status_code,302)

class EventManageTest(TestCase):

    '''初始化数据库表数据和登录数据'''
    def setUp(self):

        User.objects.create_user('admin','admin@qq.com','admin123456')

        Event.objects.create(name='xiaomi5',limit=2000,address='beijing',status=1,start_time='2019-04-05 16:24:00')

        login_user = {'username':'admin','password':'admin123456'}

        self.client.post('/login_action/',data=login_user)

    '''测试添加发布会'''
    def test_add_event_data(self):

        event = Event.objects.get(name="xiaomi5")

        self.assertEqual(event.address,"beijing")

    '''测试发布会'''
    def test_event_mange_success(self):

        response = self.client.post('/event_manage/')

        self.assertEqual(response.status_code,200)

        self.assertIn(b"xiaomi5",response.content)

        self.assertIn(b"beijing",response.content)

    '''测试发布会搜索'''
    def test_event_mange_search_success(self):

        response = self.client.get('/search_name/',{"name":"xiaomi5"})

        self.assertEqual(response.status_code,200)

        self.assertIn(b"xiaomi5",response.content)

        self.assertIn(b"beijing",response.content)


class GuestManageTest(TestCase):

    '''初始化数据库表数据和登录数据'''
    def setUp(self):

        User.objects.create_user('admin','admin@qq.com','admin123456')

        Event.objects.create(id=1,name='xiaomi5',limit=2000,address='beijing',status=1,start_time='2019-04-05 16:24:00')

        Guest.objects.create(realname='zhangbo01',phone='18611220001',email='zhangbo01@qq.com',event_id=1,sign=0,create_time='2019-04-05 20:24:00')
        Guest.objects.create(realname='zhangbo02',phone='18611220002',email='zhangbo02@qq.com',event_id=1,sign=1,create_time='2019-04-05 20:24:00')

        login_user = {'username':'admin','password':'admin123456'}

        self.client.post('/login_action/',data=login_user)

    '''测试添加嘉宾'''
    def test_add_guest_data(self):

        guest1 = Guest.objects.get(realname="zhangbo01")
        guest2 = Guest.objects.get(realname="zhangbo02")

        self.assertEqual(guest1.phone,"18611220001")
        self.assertEqual(guest1.email,"zhangbo01@qq.com")
        self.assertFalse(guest1.sign)

        self.assertEqual(guest2.phone,"18611220002")
        self.assertEqual(guest2.email,"zhangbo02@qq.com")
        self.assertTrue(guest2.sign)

    '''测试嘉宾信息'''

    def test_event_mange_success(self):

        response = self.client.post('/guest_manage/')

        self.assertEqual(response.status_code,200)

        self.assertIn(b"zhangbo01",response.content)

        self.assertIn(b"18611220001",response.content)

    '''测试嘉宾搜索'''
    def test_guest_mange_search_success(self):

        response = self.client.post('/search_phone/',{"phone":"18611220001"})

        self.assertEqual(response.status_code,200)

        self.assertIn(b"zhangbo01",response.content)

        self.assertIn(b"18611220001",response.content)


class SignIndexActionTest(TestCase):

    '''初始化数据库表数据和登录数据'''
    def setUp(self):

        User.objects.create_user('admin','admin@qq.com','admin123456')

        Event.objects.create(id=1,name='xiaomi5',limit=2000,address='beijing01',status=1,start_time='2019-04-05 16:24:00')
        Event.objects.create(id=2,name='xiaomi6',limit=1000,address='beijing02',status=0,start_time='2019-04-05 17:24:00')

        Guest.objects.create(realname='zhangbo01', phone='18611220001', email='zhangbo01@qq.com', event_id=1, sign=1,create_time='2019-04-05 20:24:00')
        Guest.objects.create(realname='zhangbo02', phone='18611220002', email='zhangbo02@qq.com', event_id=2, sign=0,create_time='2019-04-05 20:30:00')

        login_user = {'username':'admin','password':'admin123456'}

        self.client.post('/login_action/',data=login_user)

    '''测试手机号为空或者输入错误'''
    def test_sign_index_action_phone_null(self):

        response1 = self.client.post('/sign_index_action/1/',{"phone":""})
        response2 = self.client.post('/sign_index_action/1/',{"phone":"18611220003"})

        self.assertEqual(response1.status_code,200)

        self.assertIn(b"phone error.",response1.content)

        self.assertEqual(response2.status_code,200)

        self.assertIn(b"phone error.",response2.content)

    '''测试手机号或发布会id不匹配 '''
    def test_sign_index_action_phone_or_event_id_error(self):

        response1 = self.client.post('/sign_index_action/1/',{"phone":"18611220002"})
        response2 = self.client.post('/sign_index_action/2/',{"phone":"18611220001"})

        self.assertEqual(response1.status_code,200)

        self.assertIn(b"phone mismatch.",response1.content)

        self.assertEqual(response2.status_code,200)

        self.assertIn(b"phone mismatch.",response2.content)

    '''测试用户已签到'''
    def test_sign_index_action_user_sign_has(self):

        response1 = self.client.post('/sign_index_action/1/',{"phone":"18611220001"})

        self.assertEqual(response1.status_code,200)

        self.assertIn(b"user has sign in.",response1.content)

    '''测试用户签到成功'''
    def test_sign_index_action_sign_success(self):

        response1 = self.client.post('/sign_index_action/2/',{"phone":"18611220002"})

        self.assertEqual(response1.status_code,200)

        self.assertIn(b"sign in success!",response1.content)