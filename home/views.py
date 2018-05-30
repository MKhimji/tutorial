from home.forms import BlogPostForm
from django.shortcuts import render, redirect
from home.models import BlogPost,Comment, Like
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
from django.views.generic.list import ListView



#There is a reason for redirect : Prevents form submission twice if the user accidentally refreshes page.
def home(request):
    if request.method == 'GET':
        all_posts = BlogPost.objects.all().order_by('-date')   
        paginator = Paginator(all_posts,10)
        page = request.GET.get('page', 1)   
        try:
        # paginator is a subset of all_posts
        # try and assign all_posts to paginator.page(page)(i.e in blocks of 10)
            all_posts = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            all_posts = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            all_posts = paginator.page(paginator.num_pages)
        
        args = {'allposts' : all_posts,'paginator':paginator}
        return render(request, 'home/home.html', args)  


def blog(request,year,month,day,slug):
    
    if request.method == 'GET':

        blogpost = BlogPost.objects.get(date__year=year, date__month=month, date__day=day,slug=slug)
        
        form = BlogPostForm()
        comments = Comment.objects.filter(comment_body_id=blogpost).order_by('-date') #Link comments to blogpost // comment_body is foreignkey to blogpost model
        c = comments.count()
        
        likes_count = blogpost.votes.filter(vote=+1).count()
        dislikes_count = blogpost.votes.filter(vote=-1).count()

        # likes_count =  blogpost.votes.likes().count()
        # dislikes_count = blogpost.votes.dislikes().count()

        args = {'bpost': blogpost,'form':form,'comments':comments,'c':c,'likes_count':likes_count,'dislikes_count':dislikes_count}
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

def djangoarticles(request):
    if request.method == 'GET':
        djangoarticles = BlogPost.objects.all()  
        args = {'djangoarticles' : djangoarticles}
        return render(request, 'home/djangoarticles.html', args)



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
        


        #django < 1.7

        # return HttpResponse(
        #     json.dumps({
        #         "result": result,
        #         "like_count": obj.votes.likes().count(),
        #         "dislike_count": obj.votes.dislikes().count(),
        #         "sum_rating": obj.votes.sum_rating()
        #     }),
        #     content_type="application/json"
        # )





        #or if related_query_name specified in model then we can filter blogposts via Like :
        # Like.objects.filter(blogposts__title__contains='Git')


        # total_likes = BlogPost.objects.aggregate(Count('likes', distinct = 'True')) #this is for all blogposts tho also will still need if logic somehwere.
       
        # b = BlogPost.objects.values('id').annotate(Count('likes', distinct = 'True'))

        #can use blogpost = BlogPost.objects.get(date__year=year, date__month=month, date__day=day,slug=slug)
        
        # or BlogPost.objects.get(title_exact="Git")  - use in cmd to mess wit blogost instance



        #  Like.objects.get(content_type=ContentType.objects.get_for_model(BlogPost), object_id=blogpost.id, user=x[4])
             
        #both these ways return an object <Like : mo L> 
       
        # # z = Like(content_object=blogpost, like_or_dislike = 'L', user=x[4])
        # # z.save()
        # or Like.objects.create(content_object=BlogPost, like_or_dislike = Like.LIKE, user=user)
        #  p = Like.objects.create(content_type=ContentType.objects.get_for_model(BlogPost), object_id=blogpost.id, user=x[4]) - diesbt specify like or dislike but creates like

        #Like.objects.filter(blogposts__user=user) use blogposts or comments, i.e. the related query name in the first part of the field lookup in this case oit is blogposts

    
       
                
            


    


# def blogpostlikes(request,year,month,day,slug):

#     blogpost = BlogPost.objects.get(date__year=year, date__month=month, date__day=day,slug=slug)

#     user=request.user

#     total_likes = blogpost.likes.filter(like_or_dislike=Like.LIKE)
#     who_liked = otal_likes.values_list('user__username', flat=True)#this returning query set need to make list
#     total_likes_count = total_likes.count()

#     total_dislikes = blogpost.likes.filter(like_or_dislike=Like.DISLIKE)
#     who_disliked = total_dislikes.values_list('user__username', flat=True)#returns query set need to make list
#     total_dislikes_count = total_dislikes.count()


#     if user.username in who_liked and user.username not in who_disliked: #then only the dislike button should be available to click (do this on html page) and if they dislike it:
#        # Like.objects.create...if they createa  dislke then we need to remove them frm who_liked and lessen its count by 1 and add them to who_dislked and add the dislike coiunt by 1
#         who_liked = who_liked.remove(user.username)
#         total_likes_count = total_likes_count -1
#         who_disliked = who_disliked.append(user.username)
#         total_dislikes_count = total_dislikes_count + 1
#     elif user.username not in who_liked and user.username in who_disliked: #then only the like button should be available to click (do this on html page) and if they like it:
#         who_liked = who_liked.append(user.username)
#         total_likes_count = total_likes_count + 1
#         who_disliked.remove(user.username)
#         total_dislikes_count = total_dislikes_count -1



#         data = {
#             'is_liked': y.exists()
#         }
#         if data['is_liked']:
#             data['error_message'] = 'You have already liked this blogpost.'
#         return JsonResponse(data)

    
