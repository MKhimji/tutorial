from django import forms
from django.forms import ModelForm
from home.models import BlogPost, Comment



##whole point of using forms is to use the built in django functionality to
##help make the post request secure by using djangos built in features like 'cleaned_data"
##otherwise we could just write the forms directly iunto our html document but thats
##not a good way of doing it is and it takes longer and its harder

##Started off with this :
##
##class HomeForm(forms.Form):
##    post = forms.CharField()
##changed to below because were now linking this form to the the Post model. so
##use modelform instead of form

##attrs is a dictionary makes the form look better

##TextInput

##class TextInput[source]
##input_type: 'text'
##template_name: 'django/forms/widgets/text.html'
##Renders as: <input type="text" ...>


class BlogPostForm(forms.ModelForm):
    comment = forms.CharField(widget = forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder':'Enter your comments...'
            }

))


    class Meta:
        model = Comment
        exclude = ['comment_body',]



    

    
