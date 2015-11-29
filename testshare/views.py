from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpRequest
from django.core.context_processors import csrf
from django.template.context_processors import request
from django.shortcuts import redirect
from testshare.models import User, UserProfile, Post,Profileposts,Block,Location
from testshare.forms import RegistrationForm,UpdateProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from string import join,split
from random import randint
from django.core.urlresolvers import reverse
import cgi
from urllib2 import urlopen
from contextlib import closing
import json
from ipware.ip import get_ip
import math
import sys
import requests
from django.db.models import Q
def get_ip_add():
	r = requests.get(r'http://jsonip.com')
	ip= r.json()['ip']
	print 'Your IP is', ip
	return ip

def get_location(ip):
    """
    determines location using http:freegeoip.net API

    Args:
        ip(str): a valid global ipv4 address

    Returns:
        location_data(dict): a JSON format containing necessary attributes of a location based on the given ip

            Example:

            {
            u'city': u'', u'region_code': u'',
            u'region_name': u'', u'ip': u'2607:f8b0:4006:80f::200e',
            u'time_zone': u'', u'longitude': -98.5,
            u'metro_code': 0, u'latitude': 39.76,
            u'country_code': u'US', u'country_name': u'United States',
            u'zip_code': u''
            }

    Raises:

        if location can not be determined,prints "Location can not be determined successfully"

    """

    url='http://freegeoip.net/json/'
    url=url+ str(ip)
    try:
        with closing(urlopen(url)) as response:
            location_data = json.loads(response.read())
            print(location_data)

            return location_data
    except:
        print("Location could not be determined automatically")

def get_ip_address(request):

    """
    returns the remote address of the client request

    Args:
        request(Request): a Request variable,whose remote address has to be determined

    Returns:
        ip_address(str): a string representing a valid ipv4 address


    """

    ip_address = get_ip(request)
    if ip_address is not None:
        print "we have an IP address for user"
    else:
        print "we don't have an IP address for user"
    return ip_address

def get_proximity_range(location_data,x_range,y_range):
    """
    returns the range of the latitude and longitude in between which a user can see others posts

    Args:
        location_data(dict):

            a JSON format dictionary containing necessary attributes of a location based on the given ip

            Example:

            {
            u'city': u'', u'region_code': u'',
            u'region_name': u'', u'ip': u'2607:f8b0:4006:80f::200e',
            u'time_zone': u'', u'longitude': -98.5,
            u'metro_code': 0, u'latitude': 39.76,
            u'country_code': u'US', u'country_name': u'United States',
            u'zip_code': u''
            }

        x_range(double):
            range of longitude

        y_range(double):
            range of latitude

    Returns:

        proximity_range(dict):

            a dictionary containing the [min,max] of [latitude,logitude]

            example:
                {
                'min_lat':-22.36 ,
                'max_lat':86.35,
                'min_long':-98.23,
                'max_long':127.12
                }
    """

    proximity_range={
        'min_lat':-90.00 ,
        'max_lat':90.00,
        'min_long':-180.00,
        'max_long':180.00
    }

    proximity_range['min_lat']=math.ceil(location_data['latitude']-y_range)
    proximity_range['max_lat']=math.ceil(location_data['latitude']+y_range)
    proximity_range['min_long']=math.ceil(location_data['longitude']-x_range)
    proximity_range['max_long']=math.ceil(location_data['longitude']+x_range)

    if(proximity_range['min_lat']<-90.00):
        proximity_range['min_lat']=-90.00
    if(proximity_range['max_lat']>90.00):
        proximity_range['max_lat']=90.00
    if(proximity_range['min_long']<-180.00):
        proximity_range['min_long']=-180.00
    if(proximity_range['max_long']>180.00):
        proximity_range['max_long']=-90.00

    return proximity_range


def get_valid_range(request,x_range,Y_range):
    """
    returns the proximity range of the client

    :param request:a Request variable
           x_range:a double,range of longitude
           y_range:a double,range of latitude
    :return:proximity_range_client(dict):
        a dictionary containing the [min,max] of [latitude,logitude]

            example:
                {
                'min_lat':-22.36 ,
                'max_lat':86.35,
                'min_long':-98.23,
                'max_long':127.12
                }
    """

    return get_proximity_range(get_location(get_ip_address(request)),x_range,y_range)

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!


    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse(newsfeed))
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

    if request.method=='POST':
        #print(request.POST.get('email'))
        #print(request.POST.get('aboutme'))
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile.about_me=request.POST.get('aboutme')
        userprofile.user.email=request.POST.get('email')

        if request.FILES.get('profile_photo'):
            uploaded_file = request.FILES.get('profile_photo')
            #print(uploaded_file.name)
            parts=uploaded_file.name.split(".")
            #print(parts)
            joinstring=""+request.user.username+'_'+'.'+parts[len(parts)-1]
            uploaded_file.name = joinstring
            userprofile.picture= uploaded_file

        userprofile.save()
        return HttpResponseRedirect(reverse('profile',kwargs={'user_id':request.user.id}))
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('updateinfo.html', {}, context)


@login_required(login_url='/testshare/')
def profile(request,user_id):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    #username = UserProfile.objects.get(user=request.user)
    username = UserProfile.objects.get(user=User.objects.get(id=user_id))
    requested_user_prof=UserProfile.objects.get(user=request.user)
    block_possible_1=Block.objects.filter(blocker=username,blocked=requested_user_prof)
    block_possible_2=Block.objects.filter(blocked=username,blocker=requested_user_prof)
    if len(block_possible_1)+len(block_possible_2)>0:
        return  HttpResponseRedirect(reverse('nopermission'))
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
        #print(profpost.alignment)
    #print(profilepostlist)
    #print(username.about_me)
    #randlist=[int(randint(0,1)) for i in xrange(post_count)]

    #zipped=zip(posts,randlist)
    #print(zipped)
    blocks=[]
    #print(request.user.id ,int(user_id))
    if request.user.id == int(user_id):
        #print("yes")
        blocks=Block.objects.filter(blocker=username)
    #print(blocks)
    return render_to_response('profile.html', {'posts':profilepostlist,'label':toplabel,'userprofile':username,'blocks':blocks}, context)

@login_required(login_url='/testshare/')
def profile_by_name(request,user_name):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    #username = UserProfile.objects.get(user=request.user)
    username = UserProfile.objects.get(user=User.objects.get(username=user_name))
    requested_user_prof=UserProfile.objects.get(user=request.user)
    block_possible_1=Block.objects.filter(blocker=username,blocked=requested_user_prof)
    block_possible_2=Block.objects.filter(blocked=username,blocker=requested_user_prof)
    if len(block_possible_1)+len(block_possible_2)>0:
        return  HttpResponseRedirect(reverse('nopermission'))

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
     #   print(profpost.alignment)
    #print(profilepostlist)
    #print(username.about_me)
    #randlist=[int(randint(0,1)) for i in xrange(post_count)]

    #zipped=zip(posts,randlist)
    #print(zipped)
    blocks=[]
    #print(request.user.username ,str(user_name))
    if request.user.username == str(user_name):
     #   print("yes")
        blocks=Block.objects.filter(blocker=username)
    #print(blocks)

    return render_to_response('profile.html', {'posts':profilepostlist,'label':toplabel,'userprofile':username,'blocks':blocks}, context)

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
    #print('register called')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_temp = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            userprofile=UserProfile(user=user_temp)
            userprofile.save()
        #    print(userprofile.user.username)
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            #print(request.POST.get('next'))
            return redirect('/testshare/newsfeed/')


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
        #print(username)
        #print(password)
        if user is not None:
            if user.is_active:
                login(request, user)
         #       print(request.POST.get('next'))
                if (request.POST.get('next') == ''):
                    return redirect('/testshare/newsfeed/')
                return redirect(request.POST.get('next'))


        return render_to_response('index.html', context_instance=RequestContext(request))


@login_required(login_url='/testshare/')
def newsfeed(request):
    #print(get_location(''))
    """
    req_loc=get_random_location()
    print('The request location data is')
    print('Location name ',req_loc.location_name,' longitude ',req_loc.location_long,' latitude ',req_loc.location_lat,' ')
    minlat=(req_loc.location_lat)-10.00
    maxlat=(req_loc.location_lat)+10.00
    minlong=(req_loc.location_long)-10.00
    maxlong=(req_loc.location_long)+10.00


    """
    context = RequestContext(request)
    #remote host part
    req_loc_dict=get_location(get_ip_address(request))
    if str(req_loc_dict['region_name'])== '':
        req_loc_dict['region_name']=req_loc_dict['country_name']

    req_loc= Location(location_name=str(req_loc_dict['region_name']),location_lat=req_loc_dict['latitude'],location_long=req_loc_dict['longitude'])
    proximity_range=get_proximity_range(req_loc_dict,10,10)
    minlat=proximity_range['min_lat']
    maxlat=proximity_range['max_lat']
    minlong=proximity_range['min_long']
    maxlong=proximity_range['max_long']
    place=req_loc.location_name
    place_lat=req_loc.location_lat
    place_long=req_loc.location_long
    print('minlat ',minlat,'maxlat',maxlat,'minlong',minlong,'maxlong ',maxlong)
    posts=Post.objects.all()
    allblocklist=[]
    allblocklist=find_blocks(request)
    #loc_range=is_near(req_loc.location_lat,req_loc.location_long)
    #print(loc_range)
    #posts=Post.objects.filter(post_location__location_lat__lte=loc_range[0],post_location__location_lat__gte=loc_range[1],post_location__location_long__lte=loc_range[2],post_location__location_long__gte=loc_range[3]).exclude(Q(post_maker__in=allblocklist))
    #|Q(post_location__location_lat__lt= req_loc.location_lat,post_location__location_long__lt= req_loc.location_long))
    #posts=Post.objects.exclude(Q(post_maker__in=allblocklist))
#    posts=Post.objects.filter(post_location__location_lat__lte=req_loc.location_lat, post_location__location_long__lte=req_loc.location_long).exclude(Q(post_maker__in=allblocklist))
    posts=Post.objects.filter(post_location__location_lat__lte=maxlat,post_location__location_lat__gte=minlat, post_location__location_long__lte=maxlong,post_location__location_long__gte=minlong).exclude(Q(post_maker__in=allblocklist))

    if request.POST:
     #   print(request.POST.get('status'))
        #get random location
        req_loc.save()

        post_location=req_loc
        #print(post_location.location_name)
        post_maker=UserProfile.objects.get(user=request.user)
        post_text=request.POST.get('status')
        post_time=datetime.now()
        post=Post(post_maker=post_maker,post_text=post_text,post_time=post_time,post_sharecount=0,post_location=post_location)
        if request.FILES.get('post_photo'):
            uploaded_file = request.FILES.get('post_photo')
      #      print(uploaded_file.name)
            parts=uploaded_file.name.split(".")
            #print(parts)
            joinstring=""+post_maker.user.username+'_'+str(post_time)+'.'+parts[len(parts)-1]
            uploaded_file.name = joinstring
            post.post_photo = uploaded_file

        post.save()

    return render_to_response('newsfeed.html', {'posts':posts,'place':place,'place_lat':place_lat,'place_long':place_long}, context)


# Use the login_required() decorator to ensure only those logged in can access the view.

@login_required(login_url='/testshare/')
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/testshare/')

@login_required(login_url='/testshare/')
def spread(request,post_id):
    spreadedpost=Post.objects.get(pk=post_id)
    spreadedpost.post_sharecount+=1
    spreadedpost.save()

    req_loc_dict=get_location(get_ip_address(request))
    if str(req_loc_dict['region_name'])== '':
        req_loc_dict['region_name']=req_loc_dict['country_name']

    req_loc= Location(location_name=str(req_loc_dict['region_name']),location_lat=req_loc_dict['latitude'],location_long=req_loc_dict['longitude'])
    req_loc.save()
    newpost=Post()
    newpost.post_location=req_loc
    print(newpost.post_location.location_name)
    newpost.post_maker=UserProfile.objects.get(user=request.user)
    newpost.post_text=spreadedpost.post_text
    newpost.post_photo=spreadedpost.post_photo
    newpost.post_sharecount=0
    newpost.post_sharedfrom=spreadedpost
    newpost.post_time=datetime.now()

    newpost.save()
    return HttpResponseRedirect(reverse('newsfeed'))

@login_required(login_url='/testshare/')
def post(request,post_id):
    context=RequestContext(request)
    post=Post.objects.get(id=post_id)

    username=post.post_maker
    requested_user_prof=UserProfile.objects.get(user=request.user)
    block_possible_1=Block.objects.filter(blocker=username,blocked=requested_user_prof)
    block_possible_2=Block.objects.filter(blocked=username,blocker=requested_user_prof)
    if len(block_possible_1)+len(block_possible_2)>0:
        return  HttpResponseRedirect(reverse('nopermission'))

    return render_to_response('post.html', {'post':post}, context)


@login_required(login_url='/testshare/')
def block(request,user_id):
    context=RequestContext(request)
    who_blocked=UserProfile.objects.get(user=request.user)
    who_got_blocked=UserProfile.objects.get(user=User.objects.get(id=user_id))
    block_when=datetime.now()
    block= Block(blocker=who_blocked,blocked=who_got_blocked,block_time=block_when)
    block.save()
    return HttpResponseRedirect(reverse('profile',kwargs={'user_id':request.user.id}))

@login_required(login_url='/testshare/')
def unblock(request,user_id):
    context=RequestContext(request)
    who_blocked=UserProfile.objects.get(user=request.user)
    who_got_blocked=UserProfile.objects.get(user=User.objects.get(id=user_id))

    blockrecord= Block.objects.filter(blocker=who_blocked,blocked=who_got_blocked)
    blockrecord.delete()
    return HttpResponseRedirect(reverse('profile',kwargs={'user_id':request.user.id}))

@login_required(login_url='/testshare/')
def find_blocks(request):
    request_user_profile=UserProfile.objects.get(user=request.user)
    #print(request_user_profile.user.username)

    not_block_list=[]
    not_block_list_1=[]
    not_block_list_2=[]

    temp_block_list_1=Block.objects.filter(Q(blocker=request_user_profile)).values_list('blocked',flat=True)
    temp_block_list_2=Block.objects.filter(Q(blocked=request_user_profile)).values_list('blocker',flat=True)
    not_block_list_1.extend(temp_block_list_1)
    not_block_list_2.extend(temp_block_list_2)

    not_block_list=not_block_list_1+not_block_list_2
    return not_block_list

def nopermission(request):
       # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!


    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('nopermission.html', {}, context)


def get_random_ip():

    sitelist=['google.com','youtube.com','goal.com','backpack.com']
    choice = int(randint(0,len(sitelist)-1))

    return sitelist[choice];

def get_random_location():

    location_dict= get_location(get_random_ip())
    print(location_dict)
    if str(location_dict['region_name'])== '':
        location_dict['region_name']=location_dict['country_name']

    location= Location(location_name=str(location_dict['region_name']),location_lat=location_dict['latitude'],location_long=location_dict['longitude'])
    location.save()
    return location

def is_near(latitude,longitude):
    range_loc=[]
    range_loc.append(latitude+10.00)
    range_loc.append(latitude-10.00)
    range_loc.append(longitude+10.00)
    range_loc.append(longitude-10.00)
    return range_loc

