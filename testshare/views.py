from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.template.context_processors import request
from django.shortcuts import redirect
from testshare.models import User, UserProfile, Post,Profileposts
from testshare.forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from string import join,split
from random import randint
import cgi
def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!


    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render_to_response('index.html', {}, context)


def aboutus(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!


    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('aboutus.html', {}, context)


@login_required(login_url='/testshare/')
def updateinfo(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!


    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('updateinfo.html', {}, context)


@login_required(login_url='/testshare/')
def profile(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    username = UserProfile.objects.get(user=request.user)
    posts = Post.objects.filter(post_maker=username)
    today = datetime.now()
    toplabel = today.strftime('%B')

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    post_count=Post.objects.filter(post_maker=username).count()

    profilepostlist=[]
    for post in posts:
        profpost=Profileposts()
        profpost.post_info=post
        choice = int(randint(0,1))
        if choice ==1:
            leftPost = '<div class="col-sm-6 padding-right arrow-right wow fadeInLeft" data-wow-duration="1000ms" data-wow-delay="300ms">'
            leftPost = cgi.escape(leftPost,quote=True)
            profpost.alignment = leftPost
        else:
            rightPost = '<div class=\"col-sm-6\"> <br> </div> <div class=\"col-sm-6 padding-left arrow-left wow fadeInRight\" data-wow-duration=\"1000ms\" data-wow-delay=\"300ms\"\>'
            rightPost = cgi.escape(rightPost,quote=True)
            profpost.alignment = rightPost
        profilepostlist.append(profpost)
        print(profpost.alignment)
    print(profilepostlist)
    #randlist=[int(randint(0,1)) for i in xrange(post_count)]

    #zipped=zip(posts,randlist)
    #print(zipped)
    return render_to_response('profile.html', {'posts':profilepostlist,'label':toplabel}, context)


def about(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!


    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('about.html', {}, context)


def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    # context = RequestContext(request)

    # return render_to_response('index.html',{ } ,context)
    print('register called')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            userprofile=UserProfile(user=user)
            userprofile.save()
            return HttpResponseRedirect('/testshare/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'index.html',
        variables,
    )


def user_login(request):
    context = RequestContext(request)
    logout(request)

    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        print(username)
        print(password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print(request.POST.get('next'))
                if (request.POST.get('next') == ''):
                    return redirect('/testshare/aboutus/')
                return redirect(request.POST.get('next'))


        return render_to_response('index.html', context_instance=RequestContext(request))


@login_required(login_url='/testshare/')
def newsfeed(request):

    context = RequestContext(request)
    posts=Post.objects.all()
    if request.POST:
        print(request.POST.get('status'))
        post_maker=UserProfile.objects.get(user=request.user)
        post_text=request.POST.get('status')
        post_time=datetime.now()
        post=Post(post_maker=post_maker,post_text=post_text,post_time=post_time,post_sharecount=0)
        if request.FILES.get('post_photo'):
            uploaded_file = request.FILES.get('post_photo')
            print(uploaded_file.name)
            parts=uploaded_file.name.split(".")
            #print(parts)
            joinstring=""+post_maker.user.username+'_'+str(post_time)+'.'+parts[len(parts)-1]
            uploaded_file.name = joinstring
            post.post_photo = uploaded_file

        post.save()

    return render_to_response('newsfeed.html', {'posts':posts}, context)


# Use the login_required() decorator to ensure only those logged in can access the view.

@login_required(login_url='/testshare/')
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/testshare/')
