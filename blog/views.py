from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, BlogComment
from django.contrib import messages
from .templatetags import extras


# Create your views here.


def blogHome(request):
    allPosts = Post.objects.all().order_by('-timestamp')
    context = {'allPosts': allPosts}
    return render(request, 'blog/index.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views+1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        print(reply)
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    print(replyDict)

    context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, 'blog/blogPost.html', context)


def postComment(request):

    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        parentSno = request.POST.get("parentSno")
        post = Post.objects.get(sno=postSno)

        #validation
        if comment == "" or comment.isspace():
            messages.error(request, "Please enter a comment before submitting")
            return redirect(f"/blog/{post.slug}")

        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno = parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")
