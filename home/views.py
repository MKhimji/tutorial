from django.views.generic import TemplateView, FormView
from home.forms import HomeForm, BlogPostForm, addblogpostform
from django.shortcuts import render, redirect
from home.models import Post, Friend, BlogPost,Comment
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
##class based view
##TemplateView already has the get method built in so we just need to define an
##attribute  in this case 'template_name' and django automatically knows to render a template
##because the get  method renders a template.
##so we dont have to type  from dajango.shortcuts import render and then at the bottom
##write return render(request... as we would with a function based view like the views.py
##in accounts app


class HomeView(TemplateView):

    template_name = 'home/home.html'

##Render a form when the user makes a get request
    def get(self,request):

        all_posts = BlogPost.objects.all().order_by('-date')

##        for x in all_posts:
##            z = x.date
##            dt = datetime.datetime.date(z)
##            year = dt.strftime('%Y')
##            month = dt.strftime('%m')
##            day = dt.strftime('%d')





##        form = HomeForm()
##Get the post objects out of the database and order them

##        posts = Post.objects.all().order_by('-created')

##presents other people list, excluding ourselves








##        users = User.objects.exclude(id=request.user.id)
##        friend, created = Friend.objects.get_or_create(current_user=request.user)
##        friends = friend.users.all()

        args = {'allposts' : all_posts}
        return render(request, self.template_name, args)



    def post(self,request):
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)

            post.user = request.user
            post.save()
##Saving the data from the post request into the database. The only reason we can use form.save()
##is because we have associated the form with a model.
            text = form.cleaned_data['post']
            form = HomeForm()
            return redirect('home:home')

        args = {'form':form, 'text': text}
        return render(request, self.template_name, args)




def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend )
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('home:home')



##def view_blogpost(request,pk=None):
##   if pk:
##        blogpost = BlogPost.objects.get(author_id = pk)
##        args = {'bpost': blogpost}
##        return render(request, 'home/blog.html', args)


##    if request.method == "POST":
##        form = BlogPostForm(request.POST)
##        if form.is_valid():
##           post = form.save(commit = False)
##
##           post.user = request.user
##           post.save()
##
##           text = form.cleaned_data['post']
##
##           return redirect('home:home')
##        args = {'form':form, 'text': text}
##        return render(request, 'home/blog.html', args)
##
##    else:
##        form = BlogPostForm()
##        posts = Post.objects.all().order_by('-created')
##        args = {'form':form, 'posts': posts}
##        return render(request, 'home/blog.html', args)

class BlogPostView(TemplateView):
    template_name = 'home/blog.html'

    def get(self,request,year,month,day,slug):
        blogpost = BlogPost.objects.get(date__year=year, date__month=month, date__day=day,slug=slug)
        form = BlogPostForm()
        comments = Comment.objects.filter(comment_body_id=blogpost).order_by('-date')
        c = comments.count()


        args = {'bpost': blogpost,'form':form,'comments':comments,'c':c}
        return render(request,self.template_name, args)


    def post(self,request,year,month,day,slug):
        blogpost = BlogPost.objects.get(date__year=year, date__month=month, date__day=day,slug=slug)
        form = BlogPostForm(request.POST)
        if form.is_valid():
##            comment = Comment.objects.get(pk=9)
            comment = form.save(commit = False)
            comment.comment_body = blogpost
            comment.save()

            text = form.cleaned_data['comment']
            form = BlogPostForm()
            return redirect('home:home')

        args = {'form':form,'text':text}
        return render(request,self.template_name, args)




class add_blogpost(FormView):

    template_name = 'home/add_blogpost.html'
    form_class = addblogpostform
    success_url = '/home/'
        

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
    
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        

        

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )

    # def bpost(self,request):
    #     return BlogPost.objects.all()

        