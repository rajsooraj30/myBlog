from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Contact
from blog.models import Post
from django.contrib.auth.models import User


def home(request):
    twoPost = Post.objects.all().order_by('-views')[:2]
    context = {'twoPost': twoPost}
    return render(request, "home/index.html", context)


def about(request):
    return render(request, "home/about.html")


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        description = request.POST['description']

        if len(name) < 2 or len(email) < 2 or len(phone) < 10 or len(description) < 2:
            messages.error(request, "Invalid values entered Please recheck and enter the values")

        else:
            cont_act = Contact(name=name, email=email, phone=phone, description=description)
            cont_act.save()
            messages.success(request, "Your issue has been registered we will get back to you")
        print(name, email, phone, description)

    return render(request, "home/contact.html")


def search(request):
    query = request.GET.get("query")

    if len(query) == 0:
        return render(request, "home/search.html", {'error': 'No values entered to search...'})

    elif len(query) > 50:
        return render(request, "home/search.html", {'error': 'searched query too long...'})
    allPosts_title = Post.objects.filter(title__icontains=query)
    allPosts_content = Post.objects.filter(content__icontains=query)
    allPosts = allPosts_content | allPosts_title

    context = {'allPosts': allPosts}
    return render(request, "home/search.html", context)


def handleSignUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        # perform validations
        if len(username) < 2 or len(username) > 15:
            messages.error(request, 'Length of username must be greater than 2 and less than 15')

        if len(firstname) < 2 or len(firstname) > 15:
            messages.error(request, 'Length of firstname must be greater than 2 and less than 15')

        if not (('@' in email) and ('.' in email)):
            messages.error(request, 'email must contain @ and .')

        if password != confirmpassword:
            messages.error(request, 'password is not same as confirm password')

        else:
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = firstname
            myuser.last_name = lastname
            myuser.save()
            messages.success(request, "your account has been successfully created")

        return redirect('home')

    else:
        return HttpResponse("404 Page not found")


def handleLogin(request):
    if request.method == 'POST':
        login_user = request.POST['loginusername']
        login_pass = request.POST['loginpassword']
        user = authenticate(username= login_user, password= login_pass)

        if user is not None:
            login(request,user)
            messages.success(request,"successfully loged in ")
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials please try again")
            return redirect('home')

    else:
        return HttpResponse("404 Page not found")


def handleLogout(request):
    logout(request)
    messages.success(request,"successfully logged out")
    return redirect('home')
