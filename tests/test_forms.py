import unittest
from io import BytesIO
from flask import Flask
from flask_wtf.csrf import generate_csrf
from werkzeug.datastructures import MultiDict, FileStorage
from app import create_app
from app.forms import SellForm, BountyForm

class TestForms(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = True  # Enable CSRF protection
        self.app.config['SECRET_KEY'] = 'test_secret_key'  # Set secret key for CSRF
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_sell_form(self):
        with self.app.test_request_context('/sell', method='POST', content_type='multipart/form-data'):
            csrf_token = generate_csrf()
            formdata = MultiDict({
                'csrf_token': csrf_token,
                'weapon_title': 'Test Weapon',
                'weapon_price': 100,
                'weapon_description': 'This is a test weapon.'
            })
            filedata = {
                'weapon_image': FileStorage(stream=BytesIO(b"fake image data"), filename='test.jpg', content_type='image/jpeg')
            }
            form = SellForm(formdata, weapon_image=filedata['weapon_image'])
            self.assertTrue(form.validate(), msg=f"Form errors: {form.errors}")

    def test_bounty_form(self):
        with self.app.test_request_context('/addbounty', method='POST', content_type='multipart/form-data'):
            csrf_token = generate_csrf()
            formdata = MultiDict({
                'csrf_token': csrf_token,
                'target': 'Test Target',
                'price': '1000',
                'tinfo': 'Test target information.',
                'category_menu': 'Dead'
            })
            filedata = {
                'weapon_image': FileStorage(stream=BytesIO(b"fake image data"), filename='test.jpg', content_type='image/jpeg')
            }
            form = BountyForm(formdata, weapon_image=filedata['weapon_image'])
            self.assertTrue(form.validate(), msg=f"Form errors: {form.errors}")

if __name__ == '__main__':
    unittest.main()
