from tests import BaseTestCase
from flask import url_for
from io import BytesIO

class TestRoutes(BaseTestCase):
    def test_home_page(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('routes.home'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'BOUNTIFY', response.data)  # Adjusted expected content

    def test_signup_page(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('auth.sign_up'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Sign Up', response.data)
    
    def test_login_page(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('auth.login'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Log In', response.data)
    
    def test_create_post(self):
        with self.app.test_request_context():
            self.client.post(url_for('auth.sign_up'), data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password',
                'password2': 'password'
            })
            self.client.post(url_for('auth.login'), data={
                'email': 'test@example.com',
                'password': 'password'
            })
            response = self.client.post(url_for('routes.discussion'), data={
                'title': 'Test Post',
                'desc': 'This is a test post.',
                'image': (BytesIO(b"fake image data"), 'test.jpg')
            }, follow_redirects=True)
            self.assertIn(b'Discussion Post Uploaded!', response.data)
    
    def test_logout(self):
        with self.app.test_request_context():
            self.client.post(url_for('auth.sign_up'), data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password',
                'password2': 'password'
            })
            self.client.post(url_for('auth.login'), data={
                'email': 'test@example.com',
                'password': 'password'
            })
            response = self.client.get(url_for('auth.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Log In', response.data)
