from rango.models import Category, Page, UserProfile
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rango.forms import CategoryForm, PageForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from rango.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator

class IndexView(View):
    def get(self, request):
            category_list = Category.objects.order_by('-likes')[:5]
            pages_list = Page.objects.order_by('-views')[:5]
            '''
            the expression Category.objects.order_by('-likes')[:5] queries the Category
            model to retrieve the top five categories. the hyphen order it in descending
            '''
            context_dict = {}
            context_dict['categories'] = category_list
            context_dict['pages'] = pages_list
                # setting server side cookies for improved security
            visitor_cookie_handler(request)
            response = render(request, 'rango/index.html', context=context_dict)
            # testing cookie functionality
            # Render request and send it to the home-page.
            return response

class AboutView(View):
    def get(self, request):
            print(request.method)
            # prints out the user name, if no one is logged in it prints `AnonymousUser`
            print(request.user)
            # testing cookie functionality [10.4]
            visitor_cookie_handler(request)
            context_dict = {}
            context_dict['visits'] = request.session['visits']
            response = render(request, 'rango/about.html', context=context_dict)
            return response

class ShowCategoryView(View):
    def create_context_dict(self, category_name_slug):
        """
        A helper method that was created to demonstarte the power of class-based views.
        You can reuse this method in the get() and post() methods!
        """
        context_dict = {}

        try:
            category = Category.objects.get(slug=category_name_slug)
            pages = Page.objects.filter(category=category).order_by('-views')

            context_dict['pages'] = pages
            context_dict['category'] = category
        except Category.DoesNotExist:
            context_dict['pages'] = None
            context_dict['category'] = None
        
        return context_dict
    
    def get(self, request, category_name_slug):
        context_dict = self.create_context_dict(category_name_slug)
        return render(request, 'rango/category.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, category_name_slug):
        context_dict = self.create_context_dict(category_name_slug)
        query = request.POST['query'].strip()

        if query:
            context_dict['result_list'] = run_query(query)
            context_dict['query'] = query
        
        return render(request, 'rango/category.html', context_dict)

class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
        
        return render(request, 'rango/add_category.html', {'form': form})

class AddPageView(View):
    def get_category_name(self, category_name_slug):
        """
        A helper method that was created to demonstrate the power of class-based views.
        You can reuse this method in the get() and post() methods!
        """
        try:
            category = Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            category = None
        
        return category
    
    @method_decorator(login_required)
    def get(self, request, category_name_slug):
        form = PageForm()
        category = self.get_category_name(category_name_slug)

        if category is None:
            return redirect(reverse('rango:index'))
        
        context_dict = {'form': form, 'category': category}
        return render(request, 'rango/add_page.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, category_name_slug):
        form = PageForm(request.POST)
        category = self.get_category_name(category_name_slug)

        if category is None:
            return redirect(reverse('rango:index'))
        
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()

            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
        
        context_dict = {'form': form, 'category': category}
        return render(request, 'rango/add_page.html', context=context_dict)
        
class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserProfileForm()
        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
        
        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website,
                                'picture': user_profile.picture})
        
        return (user, user_profile, form)
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        
        return render(request, 'rango/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:profile',
                                    kwargs={'username': username}))
        else:
            print(form.errors)
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        
        return render(request, 'rango/profile.html', context_dict)

class LoginCheckView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'rango/login_check.html')

# for tracking page clickthroughs
class GotoView(View):
    def get(self, request):
        page_id = request.GET.get('page_id')
        try:
            the_page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('rango:index'))
        
        the_page.views = the_page.views + 1
        the_page.save()
        
        return redirect(the_page.url)        

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

'''
this decommissioning is part of chapter 15
def search(request):
    result_list = []
    query = ''

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)
    
    return render(request, 'rango/search.html', {'result_list': result_list, 'query': query})'''

