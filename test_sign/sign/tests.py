from django.test import TestCase

# Create your tests here.

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

    '''测试登录动作'''

    def test_login_action_success(self):

        self.client.post('/login_action/')