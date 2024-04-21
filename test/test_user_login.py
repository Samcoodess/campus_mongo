
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

class TestWebsiteLogin (StaticLiveServerTestCase):
    driver = None
    port = 8888

    @classmethod
    def setUpClass(cls):
        ContentType.objects.clear_cache()
        super().setUpClass()
        cls.driver = webdriver.Chrome (executable_path='path/to/chromed river')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Create a test an active user
        self.user_password = 'mypassword'
        self.user = User.objects.create_user('myuser', 'myuser@mydomain.com', self.
        user_password)
        self.user.is_active = True
        self.user.save()

    def test_admin_login(self):
        driver = self.driver
        url = self.live_server_url + '/accounts/login/' driver.get(url)
        # Input the username
        username_elem = driver.find_element_by_name('username') username_elem.clear()
        username_elem.send_keys(self.user.username)
        # Input the password
        password_elem = driver.find_element_by_name('password') password_elem.clear()
        password_elem.send_keys(self.user_password)
        # Press submit button
        driver.find_element_by_xpath("//input[@type='submit']").click()
        # If successfully logged in, you will be redirected to an authenticated landing page self.assertEqual(driver.current_url, url, msg="Something went wrong")