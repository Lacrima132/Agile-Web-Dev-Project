import unittest
from tests import BaseTestCase
from app import db
from app.models import User, Post, Comments, Likes, Sell, Promote

class TestModels(BaseTestCase):

    def test_user_creation(self):
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.uid)
        self.assertEqual(user.username, 'testuser')

    def test_post_creation(self):
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        post = Post(title='Test Post', img='test.jpg', desc='This is a test post.', user=user)
        db.session.add(post)
        db.session.commit()
        self.assertIsNotNone(post.pid)
        self.assertEqual(post.user.username, 'testuser')

    def test_comment_creation(self):
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        post = Post(title='Test Post', img='test.jpg', desc='This is a test post.', user=user)
        db.session.add(post)
        db.session.commit()
        comment = Comments(comment='This is a test comment.', uid=user.uid, pid=post.pid)
        db.session.add(comment)
        db.session.commit()
        self.assertIsNotNone(comment.cid)
        self.assertEqual(comment.user.username, 'testuser')
        self.assertEqual(comment.pid, post.pid)

    def test_like_creation(self):
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        post = Post(title='Test Post', img='test.jpg', desc='This is a test post.', user=user)
        db.session.add(post)
        db.session.commit()
        like = Likes(uid=user.uid, pid=post.pid, liked=True)
        db.session.add(like)
        db.session.commit()
        self.assertIsNotNone(like.lid)
        self.assertTrue(like.liked)

    def test_sell_creation(self):
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        sell = Sell(title='Test Weapon', img='test.jpg', desc='This is a test weapon.', price=100, uid=user.uid)
        db.session.add(sell)
        db.session.commit()
        self.assertIsNotNone(sell.sid)
        self.assertEqual(sell.user.username, 'testuser')
        self.assertEqual(sell.title, 'Test Weapon')

    def test_promote_creation(self):
        user1 = User(username='testuser1', email='test1@example.com', password='password')
        user2 = User(username='testuser2', email='test2@example.com', password='password')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        promote = Promote(promoted_by=user1.uid, promoting_this_guy=user2.uid)
        db.session.add(promote)
        db.session.commit()
        self.assertIsNotNone(promote.id)
        self.assertEqual(promote.promoted_by, user1.uid)
        self.assertEqual(promote.promoting_this_guy, user2.uid)

    def test_user_email_uniqueness(self):
        user1 = User(username='testuser1', email='test@example.com', password='password')
        db.session.add(user1)
        db.session.commit()
        user2 = User(username='testuser2', email='test@example.com', password='password')
        db.session.add(user2)
        with self.assertRaises(Exception):
            db.session.commit()

if __name__ == '__main__':
    unittest.main()
