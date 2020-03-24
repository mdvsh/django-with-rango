import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
                    'learning_django.settings')
import django 
django.setup()
from rango.models import Category, Page

def populate():
    '''
    1. Create lists of dicts containing pages to add into each category
    2. Create dict of dicts for our categories to iterate through data
        structs and add data to model.
    '''
    python_pages = [
        {'title':'Official Python Tutorial', 'url':'http://docs.python.org/3/tutorial/', 'views':120},
        {'title':'How to Think like a Computer Scientist', 'url':'http://www.greenteapress.com/thinkpython/', 'views':101},
        {'title':'Learn Python in 10 Minutes', 'url':'http://www.korokithakis.net/tutorials/python/', 'views' : 82},
        {'title':'Real Python - Tricks', 'url':'	http://realpython.com/python-tricks/', 'views':87},
    ]

    django_pages = [
        {'title':'Official Django Tutorial', 'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/', 'views' :108},
        {'title':'Django Rocks', 'url':'http://www.djangorocks.com/', 'views' : 23},
        {'title':'How to Tango with Django', 'url':'http://www.tangowithdjango.com/', 'views' : 78},
        {'title':'Django Girls - Tutorial', 'url':'https://djangogirls.org/', 'views' : 68},
        
    ]

    other_pages = [
        {'title':'Bottle', 'url':'http://bottlepy.org/docs/dev/', 'views' : 43},
        {'title':'Flask', 'url':'http://flask.pocoo.org', 'views' : 12}
    ]

    react_pages = [
        {'title':'FB React Documentation', 'url':'https://reactjs.org/', 'views' : 102},
        {'title':'Tyler McGinnis React Course', 'url':'https://tylermcginnis.com/courses/react/', 'views' : 65},
        {'title':'Egghead.io React Course', 'url':'https://egghead.io/', 'views' : 0}
    ]

    ml_pages = [
        {'title':"Colah's ML Blog", 'url':'https://reactjs.org/', 'views' : 15},
        {'title':'Distill', 'url':'https://distill.pub/', 'views' : 5},
        {'title':'Deep Learning Notes | CS230 Stanford', 'url':'https://stanford.edu/~shervine/teaching/cs-230/cheatsheet-convolutional-neural-networks', 'views' : 0}
    ]

    cats = {'Python': {'pages': python_pages, 'views':128, 'likes':64}, 
            'Django': {'pages': django_pages, 'views':110, 'likes':32},
            'Other Frameworks': {'pages': other_pages, 'views':50, 'likes':8},
            'React': {'pages':react_pages, 'views':105, 'likes':16},
            'Machine Learning': {'pages':ml_pages, 'views':24, 'likes':24},
            }
    # cat is not for the 'meow' cat but for category :-)

    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes']) 
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category = c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views = 0):
    p = Page.objects.get_or_create(category = cat, title = title)[0]
    p.url = url 
    p.views = views 
    p.save()
    return p 

def add_cat(name, views = 0, likes = 0):
    c = Category.objects.get_or_create(name = name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c 

# start execution
if __name__ == '__main__':
    print("Initializing Rango population script...")
    populate()
