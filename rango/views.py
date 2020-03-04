from rango.models import Category, Page
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rango.forms import CategoryForm, PageForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query

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

    # setting server side cookies for improved security
    visitor_cookie_handler(request)
    response = render(request, 'rango/index.html', context=context_dict)
    # testing cookie functionality
    # Render request and send it to the home-page.
    return response

def about(request):
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    # testing cookie functionality [10.4]
    visitor_cookie_handler(request)
    context_dict = {}
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/about.html', context=context_dict)
    return response

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

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            # once form saved, redirect user back to home page.
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
            
    return render(request, 'rango/add_category.html', {'form' : form})


'''
we need to redirect the user to the show_category() 
view once the page has been created. This involves the use of the redirect() and
reverse() helper functions to redirect the user and to lookup the appropriate URL,
respectively.
'''
@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    if category is None:
        return redirect(reverse('rango:index'))

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
'''
NO LONGER REQUIRED BCOZ OF DJANGO-REG-REDUX

def register(request):
    registered = False
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        # if 2 forms are valid
        if (user_form.is_valid()) and (user_profile_form.is_valid()):
            user  = user_form.save()
            # hash (secure) the password
            user.set_password(user.password)
            user.save()

            profile = user_profile_form.save(commit=False)
            profile.user = user 

            # cheecking for picture to get from input form into userprofile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True 

        else:
            # invalid form params exception handling
            print(user_form.errors, user_profile_form.errors)

    else:
        # when not HTTP POST action, render blank forms for input
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
            context={'user_form':user_form, 
            'user_profile_form':user_profile_form, 'registered':registered})

NO LONGER REQUIRED DUE TO USE OF DJANGO-REG-REDUX

def user_login(request):
    if request.method == 'POST':
        
        when request is HTTP POST, pull all relevant info like username/pass
        from login form using request.POST.get('<variable>')
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username = username, password = password)

        if user:
            # is account active ?
            if user.is_active:
                # if valid account i.e active we login the user
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # inactive account no login
                return HttpResponse('Sorry...\nYour Rango Account is disabled.')
        else:
            # wrong creds
            print(f"Invalid login details : {username}, {password}")
            return HttpResponse("Login Details Invalid. Please try Again.")
    else:
        # when HTTP GET
        return render(request, 'rango/login.html')      
'''

@login_required #this is a decorator.
def login_check(request):
    return render(request, 'rango/login_check.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

# a safe way to handle cookies is via the server 
# this is a helper session cookie something function
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
    '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits

def search(request):
    result_list = []
    query = ''

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)
    
    return render(request, 'rango/search.html', {'result_list': result_list, 'query': query})