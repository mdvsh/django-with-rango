from django.shortcuts import render
from rango.models import Category, Page
from django.http import HttpResponse
from django.shortcuts import redirect
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.urls import reverse

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    '''
    the expression Category.objects.order_by('-likes')[:5] queries the Category
    model to retrieve the top five categories. the hyphen order it in descending
    '''
    context_dict = {}
    context_dict['boldmessage'] = 'Desh ke gaddaron ko...\n Goli maaron saalon ko !!!'
    context_dict['categories'] = category_list
    context_dict['pages'] = pages_list

    # Render request and send it to the home-page.
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
    
    # render response and return it to homepage
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            # once form saved, redirect user back to home page.
            return redirect('/')
        else:
            print(form.errors)
            
    return render(request, 'rango/add_category.html', {'form' : form})


'''
we need to redirect the user to the show_category() 
view once the page has been created. This involves the use of the redirect() and
reverse() helper functions to redirect the user and to lookup the appropriate URL,
respectively.
'''
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)