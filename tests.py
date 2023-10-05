import os
os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from models import DEFAULT_IMAGE_URL, User, Post
from app import app, db
from unittest import TestCase


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_root_redirect(self):
        '''Test for root redirect to users page'''

        with app.test_client() as c:
            resp = c.get("/")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

    def test_show_new_user_form(self):
        """Test for get request for new user form"""

        with app.test_client() as c:
            resp = c.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Got New User Form', html)

    def test_create_new_user(self):
        """Test creating new user form post request"""

        with app.test_client() as c:
            resp = c.post(
                "/users/new",
                data={
                    'first_name': 'test1_first',
                    'last_name': 'test1_last',
                    'image_url': ''},
                follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Got users page', html)
            self.assertIn('test1_first', html)


    def test_delete_user(self):
        """Test delete user button post request"""

        with app.test_client() as c:
            resp = c.post(
                f"/users/{self.user_id}/delete",
                follow_redirects=True,
            )

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Got users page', html)
            self.assertNotIn("test1_first</a>", html)



class PostViewTestCase(TestCase):
    """Test views for Blogly posts."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        test_post = Post(
            title="Test title",
            content="this is test content",
            user_id=test_user.id
        )

        db.session.add(test_post)
        db.session.commit()

        self.test_post_id = test_post.id
        self.test_user_id = test_post.user_id


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_posts_list(self):
        """ test that list of posts shows up on user page  """

        with app.test_client() as c:
            resp = c.get(f"/users/{self.test_user_id}")

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn("Test title", html)


    def test_show_new_post_form(self):
        """Test for get request for new post form"""

        with app.test_client() as c:
            resp = c.get(f"/users/{self.test_user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Got New Post Form', html)


    def test_create_new_post(self):
        """Test creating new post from form post request"""

        with app.test_client() as c:
            resp = c.post(
                f"/users/{self.test_user_id}/posts/new",
                data={
                    'post_title': 'Test title',
                    'post_content': 'this is test content',
                    'user_id': self.test_user_id},
                follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('got profile page', html)
            self.assertIn('Test title', html)


    def test_edit_post(self):
        """ Test editing a post """

        with app.test_client() as c:
            resp = c.post(
                f"/posts/{self.test_post_id}/edit",
                data={
                    'post_title': 'Changed post title',
                    'post_content': 'this is updated test content',
                    },
                follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('post view', html)
            self.assertIn('Changed post title', html)
            self.assertNotIn('this is test content', html)


    def test_delete_post(self):
        """ Test delete post """

        with app.test_client() as c:
            resp = c.post(
                f"/posts/{self.test_post_id}/delete",
                follow_redirects=True,
            )

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('got profile page', html)
            self.assertNotIn("Test title", html)
            #TODO: add a test post that should still be there, Actually make second test in setup