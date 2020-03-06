from django.test import TestCase
from rango.models import Category, Page
from django.urls import reverse
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase # for testing rendered page 
# from selenium.webdriver.firefox.webdriver import WebDriver # not covered in book i'll still do it xD
# Create your tests here.
# helper func.
def add_category(name, views=0, likes=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.likes = likes
    category.save()
    return category
# ensure that views are positive for every page in a category
class CategoryMethodTests(TestCase):
    def test_positive_views(self):
        category = add_category(name='test', views=-1, likes=0)
        category.save()
        self.assertEqual((category.views >= 0), True)
    def test_proper_slug_creation(self):
        """
        Checks to make sure that when a category is created, an
        appropriate slug is created.
        Example: "Random Category String" should be "random-category-string".
        """
        category = add_category(name='Lorem ipsum dolor')
        category.save()
        self.assertEqual(category.slug, 'lorem-ipsum-dolor')

class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
        If no categories exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])
    def test_index_view_with_categories(self):
        """
        Checks whether categories are displayed correctly when present.
        """
        add_category('Python', 1, 1)
        add_category('C++', 1, 1)
        add_category('Java', 1, 1)
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")
        self.assertContains(response, "C++")
        self.assertContains(response, "Java")
        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 3)
