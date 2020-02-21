"""Here are all the test about user app"""

from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .forms import LoginForm


##########################################################################################
#   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   #
##########################################################################################



class LoginTestCase(TestCase):
    """Testing login page"""

    def setUp(self):
        self.username = "MyUsername"
        self.password = "MyPassword"
        self.email = "MyMail@mail.com"
        self.user = User.objects.create_user(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()

    def test_form_login(self):
        """We test that form is valid"""
        form = LoginForm({
            'username': self.username,
            'password': self.password
            })
        self.assertTrue(form.is_valid)

    def text_login_200(self):
        """We test that view returns right template with 200 status"""
        response = self.client.get(reverse('user:connexion'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparator/loggin.html')

    def test_authenticated_login_template(self):
        """We test that authenticated user see right template"""
        self.user = authenticate(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('user:connexion'))
        self.assertEqual(self.login, True)
        self.assertIn("Bienvenue {}".format(self.username), str(response.content))

    def test_authenticated_wrong_password_template(self):
        """We tes that wrong password does not connect user"""
        self.password = "wrong"
        self.user = authenticate(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(self.login, False)

    def test_password_error(self):
        """We test that wrong password raise an error"""
        self.password = "wrong"
        response = self.client.post('/user/connexion/', {
            'username': self.username,
            'password': self.password
        })
        self.assertIn("Identifiant ou mot de passe incorrect", str(response.content))

    def test_username_error(self):
        """We test that wrong username raise an error"""
        self.username = "wrong"
        response = self.client.post('/user/connexion/', {
            'username': self.username,
            'password': self.password
        })
        self.assertIn("Identifiant ou mot de passe incorrect", str(response.content))

    def test_redirect_connexion_if_valid(self):
        """We test that user is redirected to connexion is login is successfull"""
        response = self.client.post('/user/connexion/', {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user/connexion/")


class CreateUserTestCase(TestCase):
    """Testing create user page"""

    def setUp(self):
        self.newuser = "NewUser"
        self.newpw = "NewPassword"
        self.newemail = "NewEmail@mail.com"
        self.username = "MyUsername"
        self.password = "MyPassword"
        self.email = "MyMail@mail.com"
        self.user = User.objects.create_user(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()

    def test_returns_200(self):
        """We test that view returns right template with 200 status"""
        response = self.client.get(reverse('user:create_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparator/create_user.html')

    def test_redirect_index_if_authenticated(self):
        """We test that user is redirected to index if he's already authenticated"""
        self.user = authenticate(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('user:create_user'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_form_create_user(self):
        """We test that form il valid"""
        form = LoginForm({
            'username': self.username,
            'email': self.email,
            'password': self.password
            })
        self.assertTrue(form.is_valid)

    def test_create_user_template_302(self):
        """We test that user is redirected to account if creation is successfull"""
        response = self.client.post('/user/create/', {
            'username': self.newuser,
            'email': self.newemail,
            'password': self.newpw
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user/account/")

    def test_short_pw_raise_error(self):
        """We test to short password raise an error"""
        self.newpw = "Shortpw"
        response = self.client.post('/user/create/', {
            'username': self.newuser,
            'email': self.newemail,
            'password': self.newpw
        })
        error_message = "Le mot de passe doit contenir au moins 8 caract\\xc3\\xa8res"
        self.assertEqual(response.status_code, 200)
        self.assertIn(error_message, str(response.content))


class LogoutUserTestCase(TestCase):
    """Testing logout feature"""

    def test_redirect_index_when_logout(self):
        """Check 302 returns and url"""
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


class AccountTestCase(TestCase):
    """Testing account page"""

    def setUp(self):
        self.username = "MyUsername"
        self.password = "MyPassword"
        self.user = User.objects.create_user(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def test_returns_200_when_authenticated(self):
        """We test that view returns 200 and account template when user is auth"""
        self.user = authenticate(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('user:account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparator/account.html')

    def test_returns_302_if_not_authenticated(self):
        """We test that view redirect to connexion is user is not auth"""
        response = self.client.get(reverse('user:account'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user/connexion/")

class ModifyEmailTestCase(TestCase):
    """Testing modify email feature"""

    def setUp(self):
        self.username = "MyUsername"
        self.password = "MyPassword"
        self.email = "MyMail@mail.com"
        self.user = User.objects.create_user(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()

    def test_email_is_modified(self):
        self.user = authenticate(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        new_email = "test@test.com"
        response = self.client.post('/user/account/', {
            'email': new_email
        })
        test_user = User.objects.get(username=self.username)
        self.assertEqual(test_user.email, new_email)
        self.assertIn("Votre adresse email : {}".format(new_email), str(response.content))