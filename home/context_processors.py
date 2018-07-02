from home.models import BlogPost

def blogposts_processor(request):
    blogposts = BlogPost.objects.all()
    q=blogposts.dates('date', 'month')
    s = [(i.strftime('%b'),i.strftime('%Y')) for i in q]

    return {'blogposts': blogposts,'s':s}

# for i in y:
#     i.strftime('%b'),i.strftime('%Y')


# s = [(i.strftime('%b'),i.strftime('%Y')) for i in y]
# e = set(s)