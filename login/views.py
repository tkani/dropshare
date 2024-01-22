from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.static import serve
from django.http.response import JsonResponse
from django.utils.safestring import SafeString
from django.views.decorators.csrf import csrf_exempt
import requests
import json

# === Imports ====
from login.apps import *
from dropshare.secret_data import *
from . tokenvalidation import *


@csrf_exempt
def sign_in(request):
    if request.method=='POST':
        password=request.POST['password']
        secret_key=request.POST['secret_key']
        url=site_url()+'sign_in/'
        data={"password":password,
            "secret_key":secret_key
            }
        response=requests.post(url,data=data)
        if response.status_code == 200:
            print(f"Response code: {response.status_code}")
            response_data = json.loads(response.text)
            first_name = response_data.get('name')
            request.session["session_token"] = response_data.get('session')
            messages.success(request, f"Welcome to Dropshare {first_name}")
            return redirect('/datahouse')
        else:
            messages.error(request, f"Invalid Credentials")

    return render(request,'login/sign-in.html')

@csrf_exempt
def sign_up(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email_id']
        mobile_no=request.POST['mobile_no']
        password=request.POST['password']
        secret_key=request.POST['secret_key']
        if 'profile' in request.FILES:
            profile = {'profile':request.FILES['profile']}
        else:
            profile = {'profile':'Default.jpg'}
            
        if 'agreement' in request.POST:
            agreement = 'Agree'
        else:
            agreement='Disgree'
        
        url=site_url()+'signup/'
        api_data={"first_name":first_name,
                "last_name":last_name,
                "email_id":email,
                "mobile_no":mobile_no,
                "password":password,
                "secret_key":secret_key,
                "agreement":agreement
            }
        response=requests.post(url,files=profile,data=api_data)
        if response.status_code == 201:
            print(f"Response code: {response.status_code}")
            messages.success(request, f"Welcome to Dropshare {first_name}")
            return redirect('/sign_in')
        else:
            # Read and print the error message from the response content
            error_message = response.json().get('error', 'Unknown error')
            print(f"Error: {error_message}")
            messages.error(request, f"{error_message}")
            return redirect('/sign_up')
    return render(request,'login/sign-up.html')

@csrf_exempt
def sign_out(request):
    request.session.clear()
    return redirect('sign_in')