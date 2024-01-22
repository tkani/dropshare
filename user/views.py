from django.contrib import messages
from django.views.static import serve
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.utils.safestring import SafeString
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, FileResponse
import mimetypes

from login.tokenvalidation import *
from django.conf import settings
from .file_encryptor import *
from dropshare.secret_data import *
import requests
import os

# Create your views here.
@session_token
@csrf_exempt
def datahouse(request):
    
    headers={'X-access-token':request.session['session_token']}

    # if request.method=='POST':
    #     expiry_date=request.POST['fileExpiryDate']
    #     file_type=request.POST.get('file_type')
    #     password=request.POST['file_password']
    #     print('file_type:noonkm',file_type)
    #     if 'files' in request.FILES:
    #         files = {'files':request.FILES['files']}
    #     else:
    #         files = {'files':'Default.jpg'}

    #     # print(expiry_date,files,password)
    #     url=site_url()+'data_house/'
    #     api_data={"expiry_date":expiry_date,
    #             "file_type":file_type,
    #             "password":password
    #         }
    #     response=requests.post(url,files=files,data=api_data,headers=headers)
    #     if response.status_code == 201:
    #         print(f"Response code: {response.status_code}")
    #         messages.success(request, f"File Uploaded!!")
    #     else:
    #         # Read and print the error message from the response content
    #         error_message = response.json().get('error', 'Unknown error')
    #         print(f"Error: {error_message}")
    #         messages.error(request, f"{error_message}")
    #     return redirect('/datahouse')

    url=site_url()+'data_house/'
    response=requests.get(url,headers=headers)
    if response.status_code == 201:

        print(f"Response code: {response.status_code}")
        response_data = json.loads(response.text)
    else:
        # Read and print the error message from the response content
        error_message = response.json().get('error', 'Unknown error')
        print(f"Error: {error_message}")
        messages.error(request, f"{error_message}")

        return render(request,'user/error.html')

    url=site_url()+'collab_folder/'
    response=requests.get(url,headers=headers)
    if response.status_code == 201:

        print(f"Response code: {response.status_code}")
        response_folder_data = json.loads(response.text)
    else:
        # Read and print the error message from the response content
        error_message = response.json().get('error', 'Unknown error')
        print(f"Error: {error_message}")
        messages.error(request, f"{error_message}")

        return render(request,'user/error.html')

    url=site_url()+'user_details/'
    response=requests.get(url,headers=headers)
    if response.status_code == 201:
        print(f"Response code: {response.status_code}")
        user_response_data = json.loads(response.text)
    else:
        messages.error(request, f"Invalid Credentials")
    return render(request,'user/datahouse.html',{'user_response_data':user_response_data,'response_folder_data':response_folder_data,'response_data': response_data['datahouse_Data'],'response_shared_users':response_data['shared_users'],'session':request.session["session_token"]})

    

@session_token
@csrf_exempt
def view_folder(request,folder_token):
    
    headers={'X-access-token':request.session['session_token']}

    if request.method=='GET':
        print(request.GET.get('password', None))
        password=request.GET.get('password', None)

        url=site_url()+'folder_view/'
        api_data={"password":password,
                "folder_token":folder_token,
            }
        response=requests.get(url,data=api_data,headers=headers)
        if response.status_code == 201:
            print(f"Response code: {response.status_code}")
            response_folder_data = json.loads(response.text)
            messages.success(request, f"File Uploaded!!")

            url=site_url()+'user_details/'
            response=requests.get(url,headers=headers)
            if response.status_code == 201:
                print(f"Response code: {response.status_code}")
                user_response_data = json.loads(response.text)
            else:
                messages.error(request, f"Invalid Credentials")

            return render(request,'user/folder_view.html',{"user_response_data":user_response_data,"folder_token":folder_token,"response_folder_data":response_folder_data,'session':request.session['session_token']})
        else:
            # Read and print the error message from the response content
            error_message = response.json().get('error', 'Unknown error')
            print(f"Error: {error_message}")
            messages.error(request, f"{error_message}")

            return render(request,'user/error.html')

@session_token
@csrf_exempt
def collab(request,folder_token):
    
    headers={'X-access-token':request.session['session_token']}

    if request.method=='GET':
        print(request.GET.get('password', None))
        password=request.GET.get('password', None)

        url=site_url()+'collab_folder_view/'
        api_data={"password":password,
                "folder_token":folder_token,
            }
        response=requests.get(url,data=api_data,headers=headers)
        if response.status_code == 201:
            print(f"Response code: {response.status_code}")
            response_folder_data = json.loads(response.text)
            messages.success(request, f"File Uploaded!!")

            url=site_url()+'user_details/'
            response=requests.get(url,headers=headers)
            if response.status_code == 201:
                print(f"Response code: {response.status_code}")
                user_response_data = json.loads(response.text)
            else:
                messages.error(request, f"Invalid Credentials")

            return render(request,'user/collab_folder_view.html',{"user_response_data":user_response_data,"folder_token":folder_token,"response_folder_data":response_folder_data,'session':request.session['session_token']})
        else:
            # Read and print the error message from the response content
            error_message = response.json().get('error', 'Unknown error')
            print(f"Error: {error_message}")
            messages.error(request, f"{error_message}")
            return redirect('/datahouse')
            # return render(request,'user/error.html')
        
# Create your views here.
@session_token
@csrf_exempt
def create_folder(request):
    
    headers={'X-access-token':request.session['session_token']}

    if request.method=='POST':
        print(request)
        folder_name=request.POST['folder_name']
        folder_password = request.POST['folder_password']

        url=site_url()+'create_folder/'
        api_data={"folder_name":folder_name,
                    "folder_password":folder_password
            }
        response=requests.post(url,data=api_data,headers=headers)
        if response.status_code == 201:
            print(f"Response code: {response.status_code}")
            messages.success(request, f"Folder Created!!")
        else:
            # Read and print the error message from the response content
            error_message = response.json().get('error', 'Unknown error')
            print(f"Error: {error_message}")
            messages.error(request, f"{error_message}")
        return redirect('/datahouse')


# @csrf_exempt
# def download_files(request,file_name,save_name):
#     file_path = os.path.join(settings.MEDIA_ROOT,'datahouse', file_name)
#     print(file_path)
#     # Check if the file exists
#     if file_path:
#         with open(file_path, 'rb') as file:
#             ciphertext = file.read()
#         decrypted_content = files_encryptor().decrypt(ciphertext)

#         response = FileResponse(io.BytesIO(decrypted_content))
#         response['Content-Disposition'] = f'attachment; filename="{save_name}"'
#         print(response)
#         return response
#     else:
#         return None