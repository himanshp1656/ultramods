from django.http import JsonResponse
from django.shortcuts import render , HttpResponse , redirect , HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login , logout 
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views import View
from django.http import HttpResponseBadRequest
import openai,os
from dotenv import DotEnv
from requests import post
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from avan.settings import OPENAI_KEY
api_key= OPENAI_KEY
def chatbot(request):
    if api_key is not None and request.method=='POST':
            openai.api_key=api_key           
            User_input=request.POST.get('user_input')
            prompt = User_input
            response=openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=256,
                stop='.',
                temperature=0.5,
            )
            chatbot_response=response['choices'][0]['text']
            return render(request,'form.html',{'response':chatbot_response})
    # print('hello')
    return render(request,'form.html')
def search(request):
    query=request.GET['query']
    
    allposts=post.objects.filter(title__icontains=query)
    params={'allposts': allposts}
    return render(request,'search.html',params)

def donation(request):
    return render(request,'donation.html')
# Create your views here.
def home(request):
    return render(request, 'index.html')
def stripegateway(request):
    return render(request, 'stripe.html')
def free_wifi(request):
    return render(request, 'free_wifi.html')
def own_a_router(request):
    return render(request, 'own_a_router.html')
def subscription_plans(request):
    return render(request, 'subscription_plans.html')
def askinggateway(request):
    return render(request, 'askinggateway.html')

    
def handlesignup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1!=pass2:
            messages.error(request,'password and confirm password should be same')
            return HttpResponseRedirect('/home/')
        else:
            myuser=User.objects.create_user(username, email, pass1)               
            myuser.first_name=fname 
            myuser.save()
            messages.success(request, 'account is created succefully')
            return HttpResponseRedirect('/home/')
           
def handlelogin(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    print(username,password)
    User=authenticate(request,username=username , password=password)

    if User is not None:
        login(request, User)
        username=User.get_username
        messages.success(request, 'Loggedin succefully')
        return HttpResponseRedirect('/home/')
    else:
        messages.error(request,'wrong password or email')
        return HttpResponseRedirect('/home/')
    
        
    
def handlesignout(request):
    logout(request)
    messages.success(request, 'Loggedout succefully')
    return HttpResponseRedirect('/home/')
    return render(request, 'index.html')
def form(request):
    return render(request,'form.html')