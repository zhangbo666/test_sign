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
        user = User.objects.get(username='admin')

    '''测试登录动作'''
    def test_login_action_success(self):

        response = self.client.post('/login_action/',{'username':'admin','password':'admin123456'})

        # print (response.status_code)

        self.assertEqual(response.status_code,302)