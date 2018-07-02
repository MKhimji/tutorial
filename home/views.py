from home.forms import BlogPostForm
from django.shortcuts import render, redirect
from home.models import BlogPost,Comment,Like
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.views import View
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.dates import YearArchiveView, MonthArchiveView
from django.db.models.functions import Extract
from django.db.models.functions import TruncMonth, TruncYear



#have some overlapping views in blog and home,x,t 

#There is a reason for redirect : Prevents form submission twice if the user accidentally refreshes page.
def home(request):
    if request.method == 'GET':
        all_posts = BlogPost.objects.all().order_by('-date')  
        

        paginator = Paginator(all_posts,10)
        # need to see what happe ns when u take the 1 out below after 'page'. request.GET is a querydict which is a subclass of a dictionary,
        #  it has methods such as .get().get(item) https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.QueryDict. So request.GET is a
        # dictionary like object  containing HTTP GET Parameters . So we are setting the page variable to represent a key value pair, 'page' being the key and 1 being the value
        
        # t = BlogPost.objects.annotate(year=Extract('date', 'year')).values_list('date', flat=True)
        x = BlogPost.objects.annotate(year_stamp=Extract('date', 'year')).values_list('year_stamp', flat=True) #With extract you can only get the year month day as number 
        #so need to find a way to extract month as a 3 letter word. Is there a way i can just translate the blogpost month to a 2 digit month and then use django 
        #templating language to comnvert month into word
        t = list(x.distinct())
        #doing it this way means ill have to add this to every view. how would i even add it to a page in accounts as blogpost model is a home model.

             
        
        
        page = request.GET.get('page',1)   
        try:
            all_posts = paginator.page(page) 
            # //may need to change this afterwards. solution implement from medium.com/... 
            # is different to how django docs do it. feeling it amy slowdatabse with large number of blogposts down as i am 
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            all_posts = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            all_posts = paginator.page(paginator.num_pages)
        
        args = {'allposts' : all_posts,'paginator':paginator,'t':t}
        return render(request, 'home/home.html', args)  


def blog(request,year,month,day,slug):
    
    if request.method == 'GET':

        blogpost = BlogPost.objects.get(date__year=year, date__month=month, date__day=day,slug=slug)
        
        form = BlogPostForm()
        comments = Comment.objects.filter(comment_body_id=blogpost).order_by('-date') #Link comments to blogpost // comment_body is foreignkey to blogpost model
        c = comments.count()
        
        likes_count = blogpost.votes.filter(vote=+1).count()
        dislikes_count = blogpost.votes.filter(vote=-1).count()

        x = BlogPost.objects.annotate(year_stamp=Extract('date', 'year')).values_list('year_stamp', flat=True)
        t = list(x.distinct())

        args = {'bpost': blogpost,'form':form,'comments':comments,'c':c,'likes_count':likes_count,'dislikes_count':dislikes_count,'x':x,'t':t}
        return render(request,'home/blog.html',args)    

    if request.method == 'POST':

        blogpost = BlogPost.objects.get(date__year=year, date__month=month, date__day=day,slug=slug)

        form = BlogPostForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.comment_body = blogpost
            comment.save()
            text = form.cleaned_data['comment']
            form = BlogPostForm()
            return redirect(request.build_absolute_uri())
            
    else:
        form = BlogPostForm()

        args = {'form':form,'text':text}
        return render(request, 'home/blog.html', args)       


class BlogPostYearArchiveView(YearArchiveView):
    queryset = BlogPost.objects.all()
    date_field = "date"
    make_object_list = True
    allow_future = True
    


class BlogPostMonthArchiveView(MonthArchiveView):
    queryset = BlogPost.objects.all()
    date_field = "date"
    make_object_list = True
    allow_future = True




class VotesView(View):
    model = None  # Data Model - Articles or Comments
    vote_type = None # Vote type Like/Dislike
    

    
    def post(self,request, year, month, day, slug):
        
        obj = self.model.objects.get(date__year=year, date__month=month, date__day=day,slug=slug)
    
        try:
            x = Like.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
            if x.vote is not self.vote_type:
                x.vote = self.vote_type
                x.save(update_fields = ['vote'])
                result = True
            else:
                x.delete()
                result = False
        except Like.DoesNotExist:   
            obj.votes.create(user=request.user, vote=self.vote_type) #or  Like.objects.create(content_type=ContentType.objects.get_for_model(BlogPost), object_id=blogpost.id, user=x[4])
            result = True
      
       #django > 1.7
       
        data = {
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }

        return JsonResponse(data)
        




        
           
