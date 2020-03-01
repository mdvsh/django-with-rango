'''
WORKFLOW

1. If you haven’t already got one, create a forms.py module within your Django
app’s directory ( rango ) to store form-related classes.
2. Create a ModelForm class for each model that you wish to represent as a form.
3. Customise the forms as you desire.
4. Create or update a view to handle the form...
• including displaying the form,
• saving the form data, and
• flagging up errors which may occur when the user enters incorrect data (or
no data at all) in the form.
5. Create or update a template to display the form.
6. Add a urlpattern to map to the new view (if you created a new one).
'''
from django import forms
from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text='Enter Category Name.')
    views = forms.IntegerField(widget = forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget = forms.HiddenInput(), required=False)

    class Meta:
        # An inline class to provide additional information on the form.
        model = Category
        # Provide an association between the ModelForm and a model
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text='Please Enter Title of the Page')
    url = forms.URLField(max_length=200, help_text='Please Enter URL of the Page.')
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)

    class Meta:
        # Provide an association between the ModelForm and a model
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values; we may not want to include them.
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        model = Page
        exclude = ('category',)
        # or specify the fields to include (don't include the category field).
        #fields = ('title', 'url', 'views')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        
        return cleaned_data
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    class Meta:
        model = User 
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

