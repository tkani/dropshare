import json
import io

# -- Rest APi Framework --#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework import status as rest_status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status as rest_status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse
from django.core.files.uploadedfile import TemporaryUploadedFile

# -- Imports --#
from . models import *
from login.models import *
from dropshare.secret_data import *
from login.tokenvalidation import *
from .file_encryptor import FileEncryptor

class collab_folder(APIView):
    @csrf_exempt
    def get(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']
            try:
                shared_folder_db = shared_folder.objects.filter(to_user_id=auth_data['id'],folder_status='Active').all()
                others_shared_folder_data = list(shared_folder_db.values())

                for i in others_shared_folder_data:
                    if i['folder_password']!='':
                        i['folder_password']=i['folder_password']
                        i.update({'file_secure':'Protected'})
                    else:
                        i.update({'file_secure':'Public'})
                    
                    payload={'id':i['id'],'folder_name':str(i['folder_name']),'folder_original_name':str(i['folder_original_name']),'folder_password':i['folder_password'],'user_id':auth_data['id'],'folder_id':i['folder_id']}
                    access_token=file_encode_token(payload)
                    i.update({'access_token': access_token})

                    shared_datahouse_db = shared_datahouse.objects.filter(to_user_id=auth_data['id'],folder_id=i['folder_id'], file_status='Active')
                    shared_datahouse_db = list(shared_datahouse_db.values())
                    i.update({'shared_datahouse':shared_datahouse_db})
    

                folder_db = folder.objects.filter(user_id=auth_data['id'],folder_status='Active').all()
                folder_data = list(folder_db.values())

                for i in folder_data:
                    if i['folder_password']!='':
                        i['folder_password']=i['folder_password']
                        i.update({'file_secure':'Protected'})
                    else:
                        i.update({'file_secure':'Public'})
                    print(i)
                    payload={'id':i['id'],'folder_name':str(i['folder_name']),'folder_original_name':str(i['folder_original_name']),'folder_password':i['folder_password'],'user_id':auth_data['id'],'folder_id':i['id']}
                    access_token=file_encode_token(payload)
                    i.update({'access_token': access_token})

                    datahouse_db = datahouse.objects.filter(user_id=auth_data['id'],folder_id=i['id'], file_status='Active')
                    
                    datahouse_db = list(datahouse_db.values())
                    i.update({'datahouse':datahouse_db})

                    shared_folder_db = shared_folder.objects.filter(from_user_id=auth_data['id'],folder_id=i['id'],folder_status='Active').all()
                    shared_folder_data = list(shared_folder_db.values())
                    for m in shared_folder_data:
                        try:
                            shared_folder_user_data = users.objects.get(
                                id=m['to_user_id_id'],
                                status='Active'
                            ) 
                            shared_folder_user_data=json_fetch_one(shared_folder_user_data)
                            m.update({'user_id':shared_folder_user_data['id'],'user_first_name': shared_folder_user_data['first_name'],'user_email_id':shared_folder_user_data['email_id'],'user_profile':str(shared_folder_user_data['profile'])})
                        except Exception as e:
                            print(e)
                            m.update({'user_id':'user_id','user_first_name': 'first_name','user_email_id':'email_id','user_profile':'profile'})
                    i.update({'shared_folder_data':shared_folder_data})

                # shared_folder_db = shared_folder.objects.filter(from_user_id=auth_data['id'],folder_id=0,folder_status='Active').all()
                # shared_folder_data = list(shared_folder_db.values())
                # for i in shared_folder_data:
                #     if i['folder_password']!='':
                #         i['folder_password']=i['folder_password']
                #         i.update({'file_secure':'Protected'})
                #     else:
                #         i.update({'file_secure':'Public'})
                #     print(i)
                #     payload={'id':i['id'],'folder_name':str(i['folder_name']),'folder_original_name':str(i['folder_original_name']),'folder_password':i['folder_password'],'user_id':auth_data['id'],'folder_id':0}
                #     access_token=file_encode_token(payload)
                #     i.update({'access_token': access_token})
                shared_folder_data=others_shared_folder_data
                return Response({"shared_folder_data": shared_folder_data,'folder_data':folder_data}, status=rest_status.HTTP_201_CREATED)
            except Exception as e:
                print('error message: ',str(e))
                return Response({"error":'Contact Admin'}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": str(auth_token['message'])}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

class folder_view(APIView):
    @csrf_exempt
    def get(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']

            data = request.data
            folder_token=data['folder_token']
            password=my_hash(data['password'])

            access_token=file_decode_token(folder_token)

            if 'message' in access_token:
                access_token=access_token['message']
                folder_id=access_token['folder_id']
                folder_original_name=access_token['folder_original_name']
                
                if access_token['folder_password']=='':
                    try:
                        shared_folder_db = shared_folder.objects.filter(folder_original_name=folder_original_name,to_user_id=auth_data['id'],folder_status='Active',folder_id=folder_id)
                        shared_folder_data = list(shared_folder_db.values())

                        for j in shared_folder_data:
                            shared_datahouse_db = shared_datahouse.objects.filter(to_user_id=auth_data['id'],folder_id=j['folder_id'], file_status='Active')
                            shared_datahouse_db = list(shared_datahouse_db.values()) 
                            for i in shared_datahouse_db:
                                if i['file_secure']=='Protected':
                                    i['file_name']='Secured'
                                payload={'id':i['id'],'file_name':str(i['file_name']),'file_original_name':str(i['file_original_name']),'file_secure':i['file_secure'],'user_id':auth_data['id']}
                                access_token=file_encode_token(payload)
                                
                                shared_users=[]
                                try:
                                    shared_datahouse_data = users.objects.get(
                                        id=i['from_user_id'],
                                        status='Active'
                                    ) 
                                    shared_datahouse_data=json_fetch_one(shared_datahouse_data)
                                    shared_datahouse_data=shared_datahouse_data['first_name']
                                except Exception as e:
                                    print(e)
                                    shared_datahouse_data={'user':'Unable to find'}
                                # shared_datahouse_data = (list(shared_datahouse_data.values('datahouse_id','to_user_id__email_id','to_user_id__first_name','to_user_id__profile', 'to_user_id')))

                                # print(shared_datahouse_data)
                                i.update({'shared_users': shared_datahouse_data})
                                i.update({'access_token': access_token})
                            j.update({'shared_folder':shared_datahouse_db})
                        return Response({"folder_Data": shared_folder_data}, status=rest_status.HTTP_201_CREATED)
                    except Exception as e:
                        print('error message: ',str(e))
                        return Response({"error":'Contact Admin'}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                elif access_token['folder_password'] == (password):
                    try:
                        shared_folder_db = shared_folder.objects.filter(folder_original_name=folder_original_name,to_user_id=auth_data['id'],folder_status='Active',folder_id=folder_id)
                        shared_folder_data = list(shared_folder_db.values())

                        for j in shared_folder_data:
                            shared_datahouse_db = shared_datahouse.objects.filter(to_user_id=auth_data['id'],folder_id=j['folder_id'], file_status='Active')
                            shared_datahouse_db = list(shared_datahouse_db.values()) 
                            for i in shared_datahouse_db:
                                if i['file_secure']=='Protected':
                                    i['file_name']='Secured'
                                payload={'id':i['id'],'file_name':str(i['file_name']),'file_original_name':str(i['file_original_name']),'file_secure':i['file_secure'],'user_id':auth_data['id']}
                                access_token=file_encode_token(payload)
                                
                                shared_users=[]
                                try:
                                    shared_datahouse_data = users.objects.get(
                                        id=i['from_user_id'],
                                        status='Active'
                                    ) 
                                    shared_datahouse_data=json_fetch_one(shared_datahouse_data)
                                    shared_datahouse_data=shared_datahouse_data['first_name']
                                except Exception as e:
                                    print(e)
                                    shared_datahouse_data={'user':'Unable to find'}
                                # shared_datahouse_data = (list(shared_datahouse_data.values('datahouse_id','to_user_id__email_id','to_user_id__first_name','to_user_id__profile', 'to_user_id')))

                                # print(shared_datahouse_data)
                                i.update({'shared_users': shared_datahouse_data})
                                i.update({'access_token': access_token})
                            j.update({'shared_folder':shared_datahouse_db})
                        return Response({"folder_Data": shared_folder_data}, status=rest_status.HTTP_201_CREATED)
                    except Exception as e:
                        print('error message: ',str(e))
                        return Response({"error":'Contact Admin'}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'error': 'Invalid Password'}, status=rest_status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': access_token['error']}, status=rest_status.HTTP_404_NOT_FOUND)

class collab_folder_view(APIView):
    @csrf_exempt
    def get(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']

            data = request.data
            folder_token=data['folder_token']
            password=my_hash(data['password'])

            access_token=file_decode_token(folder_token)

            if 'message' in access_token:
                access_token=access_token['message']
                folder_id=access_token['folder_id']
                folder_original_name=access_token['folder_original_name']
                
                if access_token['folder_password']=='':
                    try:
                        file_data=False
                        folder_db = folder.objects.get(folder_original_name=folder_original_name,folder_status='Active',id=folder_id, user_id=auth_data['id'])
                        folder_data = json_fetch_one(folder_db)
                        if folder_data!=[]:
                            file_data=True
                        shared_folder_db = shared_folder.objects.filter(folder_original_name=folder_original_name,folder_status='Active',folder_id=folder_id,to_user_id=auth_data['id'])
                        shared_folder_data = list(shared_folder_db.values())
                        if shared_folder_data!=[]:
                            file_data=True
                        if file_data==True:
                            datahouse_db = datahouse.objects.filter(folder_id=folder_id, file_status='Active').all()
                            datahouse_db = list(datahouse_db.values())

                            for i in datahouse_db:
                                if i['file_secure']=='Protected':
                                    i['file_name']='Secured'
                                payload={'id':i['id'],'file_name':str(i['file_name']),'file_original_name':str(i['file_original_name']),'file_secure':i['file_secure'],'user_id':auth_data['id']}
                                access_token=file_encode_token(payload)
                                
                                shared_users=[]
                                try:
                                    shared_datahouse_data = users.objects.get(
                                        id=i['user_id'],
                                        status='Active'
                                    ) 
                                    shared_datahouse_data=json_fetch_one(shared_datahouse_data)
                                    shared_datahouse_data=shared_datahouse_data['first_name']
                                except Exception as e:
                                    print(e)
                                    shared_datahouse_data={'user':'Unable to find'}
                                
                                try:
                                    user_shared_datahouse_data = shared_datahouse.objects.filter(
                                        datahouse_id=i['id'],
                                        file_status='Active'
                                    )
                                    user_shared_datahouse_data = list(user_shared_datahouse_data.values())
                                    for j in user_shared_datahouse_data:
                                        user_data = users.objects.get(
                                        id=j['to_user_id'],
                                        status='Active'
                                        ) 
                                        user_data = json_fetch_one(user_data)
                                        j.update({'first_name':user_data['first_name'],'email_id':user_data['email_id']})
                                except Exception as e:
                                    print(e)
                                    user_shared_datahouse_data={'user':'Unable to find'}
                                # shared_datahouse_data = (list(shared_datahouse_data.values('datahouse_id','to_user_id__email_id','to_user_id__first_name','to_user_id__profile', 'to_user_id')))

                                # print(shared_datahouse_data)
                                i.update({'shared_users': shared_datahouse_data})
                                i.update({'user_shared_datahouse_data': user_shared_datahouse_data})
                                i.update({'access_token': access_token})
                        return Response({"folder_Data": datahouse_db}, status=rest_status.HTTP_201_CREATED)
                    except Exception as e:
                        print('error message: ',str(e))
                        return Response({"error":'Contact Admin'}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                elif access_token['folder_password'] == (password):
                    try:
                        file_data=False
                        try:
                            folder_db = folder.objects.get(folder_original_name=folder_original_name,folder_status='Active',id=folder_id,user_id=auth_data['id'])
                            folder_data = json_fetch_one(folder_db)
                            if folder_data!=None:
                                file_data=True
                        except:
                            pass
                        try:
                            shared_folder_db = shared_folder.objects.get(folder_original_name=folder_original_name,folder_status='Active',folder_id=folder_id,to_user_id=auth_data['id'])
                            shared_folder_data = json_fetch_one(shared_folder_db)
                            if shared_folder_data!=[]:
                                file_data=True
                        except:
                            pass
                        if file_data==True:
                            datahouse_db = datahouse.objects.filter(folder_id=folder_id, file_status='Active').all()
                            datahouse_db = list(datahouse_db.values())

                            for i in datahouse_db:
                                if i['file_secure']=='Protected':
                                    i['file_name']='Secured'
                                payload={'id':i['id'],'file_name':str(i['file_name']),'file_original_name':str(i['file_original_name']),'file_secure':i['file_secure'],'user_id':auth_data['id']}
                                access_token=file_encode_token(payload)
                                
                                shared_users=[]
                                try:
                                    shared_datahouse_data = users.objects.get(
                                        id=i['user_id'],
                                        status='Active'
                                    ) 
                                    shared_datahouse_data=json_fetch_one(shared_datahouse_data)
                                    shared_datahouse_data=shared_datahouse_data['first_name']
                                except Exception as e:
                                    print(e)
                                    shared_datahouse_data={'user':'Unable to find'}
                                # shared_datahouse_data = (list(shared_datahouse_data.values('datahouse_id','to_user_id__email_id','to_user_id__first_name','to_user_id__profile', 'to_user_id')))

                                # print(shared_datahouse_data)
                                i.update({'shared_users': shared_datahouse_data})
                                i.update({'access_token': access_token})
                            return Response({"folder_Data": datahouse_db}, status=rest_status.HTTP_201_CREATED)
                        else:

                            return Response({"error":'No Data'}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                    except Exception as e:
                        print('error message: ',str(e))
                        return Response({"error":'Contact Admin'}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'error': 'Invalid Password'}, status=rest_status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': access_token['error']}, status=rest_status.HTTP_404_NOT_FOUND)
            
class create_folder(APIView):
    @csrf_exempt
    # parser_classes = [JSONParser, MultiPartParser]
    def post(self,request):
        try:
            auth_token=auth_token_required(request)
            if auth_token['status']==200:
                auth_data=auth_token['message']
                data = request.data
                password = data['folder_password']
                if password == "":
                    folder_secure = 'Private'
                else:
                    password=my_hash(password)
                    folder_secure = 'Protected'
                new_user_folder = folder(
                    added_on=today(),
                    user_id=auth_data['id'],
                    folder_original_name=my_hash('random'),
                    folder_name=data['folder_name'],
                    folder_files=0,
                    folder_users=0,
                    folder_size=0,
                    folder_password=password,
                    folder_secure=folder_secure,
                    folder_status='Active',
                    last_change=last_change()
                    )
                new_user_folder.save()

                return Response({"message": "Folder Created!!"}, status=rest_status.HTTP_201_CREATED)
            else:
                return Response({"error": "Invalid Login"}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

            
class data_house(APIView):
    @csrf_exempt
    # parser_classes = [JSONParser, MultiPartParser]
    def post(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']
            data = request.data
            if 'files' not in request.FILES:
                return Response({'error': 'No file provided'}, status=400)
            
            file_chunks = request.FILES.getlist('files')
            total_chunks = int(request.POST.get('total_chunks', 0))
            current_chunk = int(request.POST.get('chunk_index', 0))
            if str_date(data['expiry_date']) >= free_plan_date():
                data['expiry_date']= free_plan_date()

            file_size = float(data['tot_file_size']) / (1024.0 * 1024.0)
            user_setting_db = setting.objects.get(user_id=auth_data['id'])
            user_setting=json_fetch_one(user_setting_db)

            new_storage=float(user_setting['current_storage']) + float(file_size)
            if new_storage > float(user_setting['storage']):
                return Response({'error': 'Storage less than file size'}, status=400)

            password = data['password']
            chunk_file_id = data['chunk_file_id']
            chunk_filename = data['file_name']
            ext=str(chunk_filename).rsplit(".",1)[1]

            data['user_id']=auth_data['id']
            if data['folder_token']!='0':
                folder_token=(data['folder_token'])
                access_token=file_decode_token(folder_token)
                if 'message' in access_token:
                    access_token=access_token['message']
                    folder_id=access_token['folder_id']
                    data['folder_id'] = folder_id
            else:
                data['folder_id']=0
            required_fields = ['folder_id', 'expiry_date', 'password', 'files', 'chunk_file_id']
            if not all(field in data for field in required_fields):
                missing_fields = [field for field in required_fields if field not in data]
                return Response({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=rest_status.HTTP_400_BAD_REQUEST)

            # Directory to save temporary files
            temp_upload_dir = os.path.join(server_path(),'Chunk_files')

            # Process or save the current file chunk
            for chunk in file_chunks:
                # Assuming unique file name for each chunk, adjust as needed
                temp_file_path = os.path.join(temp_upload_dir, f'{chunk_file_id}_pe_{current_chunk}.part')
                
                # Save the chunk to a temporary location
                with open(temp_file_path, 'ab') as temp_file:
                    # if isinstance(chunk, TemporaryUploadedFile):
                    temp_file.write(chunk.read())
                    # else:
                        # temp_file.write(chunk)

            # If it's the last chunk, process the complete file
            print(current_chunk,'--',total_chunks-1)
            if (current_chunk) == total_chunks - 1:
                complete_file_path = os.path.join(temp_upload_dir, f'{chunk_file_id}_cm_{chunk_filename}')

                # Concatenate all the chunks into the complete file
                with open(complete_file_path, 'wb') as complete_file:
                    for i in range(total_chunks):
                        chunk_file_path = os.path.join(temp_upload_dir, f'{chunk_file_id}_pe_{i}.part')
                        with open(chunk_file_path, 'rb') as chunk_file:
                            complete_file.write(chunk_file.read())

                final_size = os.path.getsize(complete_file_path)
                # Clean up temporary files
                for i in range(total_chunks):
                    chunk_file_path = os.path.join(temp_upload_dir, f'{chunk_file_id}_pe_{i}.part')
                    os.remove(chunk_file_path)

                if (password=='') or (password==None) or ('password' not in data):
                    file_password=auth_data['secret_key']
                else:
                    file_password=my_hash(data['password'])

                status='Active'
                file_secure=data['file_type']

                new_datahouse_instance = datahouse(
                    added_on=today(),
                    user_id=data['user_id'],
                    chunk_file_id=data['chunk_file_id'],
                    folder_id=data['folder_id'],
                    expiry_date=data['expiry_date'],
                    file_password=(file_password),
                    file_status=status,
                    last_change=last_change(),
                    file_secure=file_secure,
                    )
                try:
                    file_name_str = f"{my_hash('random')}.{ext}"
                    main_path =  f"datahouse/{file_name_str}"
                    new_datahouse_instance.file_name = main_path
                    new_datahouse_instance.file_original_name = chunk_filename
                    new_datahouse_instance.file_size = final_size/ (1024.0 * 1024.0)

                    new_datahouse_instance.save()
                    user_setting_db.current_storage=new_storage
                    user_setting_db.save()
                    
                    with open(os.path.join(server_path(),'datahouse',str(file_name_str)), 'wb') as main_file:
                        with open(complete_file_path, 'rb') as chunk_file:
                            main_file.write(chunk_file.read())
                    os.remove(complete_file_path)

                    file_path=os.path.join('media','datahouse',str(file_name_str))
                    files_encryptor().custom_encrypt_method(file_path)
                    return Response({"message": "File Uploaded!!"}, status=rest_status.HTTP_201_CREATED)
                except Exception as e:
                        print(e)
                        return Response({"error": str(e)}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': f'Chunk {current_chunk} received successfully'})
        else:
            return Response({"error": str(auth_token['message'])}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

    @csrf_exempt
    def get(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']
            try:
                datahouse_db = datahouse.objects.filter(user_id=auth_data['id'],folder_id=0).all()
                datahouse_data = list(datahouse_db.values())
                shared_users=[]
                for i in datahouse_data:
                    if i['file_secure']=='Protected':
                        i['file_name']='Secured'
                    
                    payload={'id':i['id'],'file_name':str(i['file_name']),'file_original_name':str(i['file_original_name']),'file_secure':i['file_secure'],'user_id':auth_data['id']}
                    access_token=file_encode_token(payload)
                    shared_datahouse_data = shared_datahouse.objects.filter(
                        from_user_id=auth_data['id'],
                        datahouse_id=i['id'],
                        file_status='Active'
                    ).select_related('to_user_id')
                    shared_datahouse_data = shared_users.append(list(shared_datahouse_data.values('datahouse_id','to_user_id__email_id','to_user_id__first_name','to_user_id__profile', 'to_user_id')))
                    
                    i.update({'access_token': access_token})
 
                return Response({"datahouse_Data": datahouse_data,"shared_users":shared_users}, status=rest_status.HTTP_201_CREATED)
            except Exception as e:
                print('error message: ',str(e))
                return Response({"error":'Contact Admin'}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": str(auth_token['message'])}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

    @csrf_exempt
    def put(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']
            data = request.data
            print(data)
            file_id=data['file_id']
            datas=json.loads(data['data'])
            password=(datas['password'])
            file_type=(datas['file_type'])
            file_key=(datas['file_key'])
            print(file_key,type(file_key),file_type)
            if file_type == 'Private':
                if password != "":
                    password=my_hash(password)
                    new_file_type = 'Protected'
                    try:
                        if int(file_key) == 0:
                            datahouse_db = datahouse.objects.get(user_id=auth_data['id'],id=file_id)
                            datahouse_data = json_fetch_one(datahouse_db)
                            datahouse_db.file_password=password
                            datahouse_db.file_secure=new_file_type
                            datahouse_db.last_change=last_change()
                            datahouse_db.save()
                            payload={'id':file_id,'file_name':str(datahouse_data['file_name']),'file_original_name':datahouse_data['file_original_name'],'file_secure':new_file_type,'user_id':auth_data['id']}
                            access_token=file_encode_token(payload)
                            return Response({'message': 'File Security Changed!!','file_id':file_id,'file_original_name':datahouse_data['file_original_name'],'new_file_type':new_file_type,'access_token':access_token}, status=rest_status.HTTP_201_CREATED)
                        elif int(file_key) == 1:
                            datahouse_db = shared_datahouse.objects.get(to_user_id=auth_data['id'],id=file_id)
                            datahouse_data = json_fetch_one(datahouse_db)
                            datahouse_db.file_password=password
                            datahouse_db.file_secure=new_file_type
                            datahouse_db.last_change=last_change()
                            datahouse_db.save()
                            payload={'id':file_id,'file_name':str(datahouse_data['file_name']),'file_original_name':datahouse_data['file_original_name'],'file_secure':new_file_type,'user_id':auth_data['id']}
                            access_token=file_encode_token(payload)
                            return Response({'message': 'File Security Changed!!','file_id':file_id,'file_original_name':datahouse_data['file_original_name'],'new_file_type':new_file_type,'access_token':access_token}, status=rest_status.HTTP_201_CREATED)
                        else:
                            return Response({"error": str('Invalid File Key')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                    except Exception as e:
                        print('error message: ',e)
                        return Response({"error": str('Invalid File')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"error": str('Enter the password')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif file_type == 'Protected':
                if password != "":
                    password=my_hash(password)
                    new_file_type = 'Public'
                    try:
                        if int(file_key) == 0:
                            datahouse_db = datahouse.objects.get(user_id=auth_data['id'],id=file_id)
                            datahouse_data = json_fetch_one(datahouse_db)
                            if (datahouse_data['file_password']==password) or (password==auth_data['password'] and datahouse_data['user_id']==auth_data['id']):
                                datahouse_db.file_secure=new_file_type
                                datahouse_db.last_change=last_change()
                                datahouse_db.save()
                                file_name = str(datahouse_data['file_name']).split('/')[1]
                                payload={'id':file_id,'file_name':str(datahouse_data['file_name']),'file_original_name':datahouse_data['file_original_name'],'file_secure':new_file_type,'user_id':auth_data['id']}
                                access_token=file_encode_token(payload)
                                return Response({'message': 'File Security Changed!!','file_name':file_name,'file_original_name':datahouse_data['file_original_name'],'file_id':file_id,'new_file_type':new_file_type,'access_token':access_token}, status=rest_status.HTTP_201_CREATED)
                            else:
                                return Response({"error": str('Invalid password')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                        elif int(file_key) == 1:
                            datahouse_db = shared_datahouse.objects.get(to_user_id=auth_data['id'],id=file_id)
                            datahouse_data = json_fetch_one(datahouse_db)
                            if (datahouse_data['file_password']==password):
                                datahouse_db.file_secure=new_file_type
                                datahouse_db.last_change=last_change()
                                datahouse_db.save()
                                file_name = str(datahouse_data['file_name']).split('/')[1]
                                payload={'id':file_id,'file_name':str(datahouse_data['file_name']),'file_original_name':datahouse_data['file_original_name'],'file_secure':new_file_type,'user_id':auth_data['id']}
                                access_token=file_encode_token(payload)
                                return Response({'message': 'File Security Changed!!','file_name':file_name,'file_original_name':datahouse_data['file_original_name'],'file_id':file_id,'new_file_type':new_file_type,'access_token':access_token}, status=rest_status.HTTP_201_CREATED)
                            else:
                                return Response({"error": str('Invalid password')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            return Response({"error": str('Invalid File Key')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                    except Exception as e:
                        print('error message: ',e)
                        return Response({"error": str('Invalid File')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"error": str('Enter the password')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif file_type == 'Public':
                new_file_type = 'Private'
                try:
                    if int(file_key) == 0:
                        datahouse_db = datahouse.objects.get(user_id=auth_data['id'],id=file_id)
                        datahouse_db.file_secure=new_file_type
                        datahouse_db.last_change=last_change()
                        datahouse_db.save()
                    elif int(file_key)==1:
                        datahouse_db = shared_datahouse.objects.get(to_user_id=auth_data['id'],id=file_id)
                        datahouse_db.file_secure=new_file_type
                        datahouse_db.last_change=last_change()
                        datahouse_db.save()
                    else:
                        return Response({"error": str('Invalid File Key')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                    return Response({'message': 'File Security Changed!!','file_id':file_id,'new_file_type':new_file_type}, status=rest_status.HTTP_201_CREATED)
                except Exception as e:
                    print('error message: ',e)
                    return Response({"error": str('Invalid File')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": str('Invalid File Type')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": str(auth_token['message'])}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

class get_secured_file(APIView):
    @csrf_exempt
    def post(self,request):
        auth_token=auth_token_required(request)
        print(auth_token)
        if auth_token['status']==200:
            auth_data=auth_token['message']
            data = request.data
            datas=json.loads(data['data'])
            file_id=data['file_id']
            password=my_hash(datas['password'])
            
            file_key=datas['file_key']
            print(file_key,'************************************')
            if int(file_key) == 0:
                datahouse_db = datahouse.objects.filter(user_id=auth_data['id'],id=file_id)
                datahouse_data = list(datahouse_db.values())

                if datahouse_data:
                    print(datahouse_data)
                    if datahouse_data[0]['file_password']==password:
                        file_name = datahouse_data[0]['file_name'].split('/')[1]
                        save_name = datahouse_data[0]['file_original_name']
                        payload={'id':file_id,'file_name':str(datahouse_data[0]['file_name']),'file_original_name':str(datahouse_data[0]['file_original_name']),'file_secure':datahouse_data[0]['file_secure'],'user_id':auth_data['id']}
                        access_token=file_encode_token(payload)
                        return Response({"file_name": file_name,"save_name":save_name,'access_token':access_token}, status=rest_status.HTTP_201_CREATED)
                    else:
                        return Response({"error": str('Invalid Password')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"error": str('Invalid File')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif int(file_key) == 1:
                datahouse_db = shared_datahouse.objects.filter(to_user_id=auth_data['id'],id=file_id)
                datahouse_data = list(datahouse_db.values())
                print(password,datahouse_data)
                if datahouse_data:
                    if datahouse_data[0]['file_password']==password:
                        file_name = datahouse_data[0]['file_name'].split('/')[1]
                        save_name = datahouse_data[0]['file_original_name']
                        payload={'id':file_id,'file_name':str(datahouse_data[0]['file_name']),'file_original_name':str(datahouse_data[0]['file_original_name']),'file_secure':datahouse_data[0]['file_secure'],'user_id':auth_data['id']}
                        access_token=file_encode_token(payload)
                        print({"file_name": file_name,"save_name":save_name,'access_token':access_token})
                        return Response({"file_name": file_name,"save_name":save_name,'access_token':access_token}, status=rest_status.HTTP_201_CREATED)
                    else:
                        return Response({"error": str('Invalid Password')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"error": str('Invalid File')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": str(auth_token['message'])}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

class get_shared_folder(APIView):
    @csrf_exempt
    def post(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']
            data = request.data

            folder_id=data['folder_id']
            data = request.data
            datas=json.loads(data['data'])
            email_id=datas['email_id']
            password=datas['password']
            folder_key=datas['folder_key']
            if folder_key == 0:
                print(password)
                folder_db = folder.objects.get(user_id=auth_data['id'],id=folder_id, folder_status='Active')
                folder_data = json_fetch_one(folder_db)
                try:
                    user_db = users.objects.get(email_id=email_id,status='Active')
                    user_data = json_fetch_one(user_db)
                    if password == "":
                        password = folder_data['folder_password']
                        folder_secure = 'Private'
                    else:
                        password=my_hash(datas['password'])
                        folder_secure = 'Protected'
                    shared_folder_db = shared_folder.objects.filter(from_user_id=auth_data['id'],to_user_id=user_data['id'],folder_id=folder_id, folder_status='Active')
                    shared_folder_db = list(shared_folder_db.values())

                    if shared_folder_db==[]:
                        if folder_data:
                            shared_folder_instance = shared_folder(
                                added_on=today(),
                                from_user_id=auth_data['id'],
                                to_user_id=user_db,
                                folder_id=folder_data['id'],
                                folder_original_name=folder_data['folder_original_name'],
                                folder_name=folder_data['folder_name'],
                                folder_size=folder_data['folder_size'],
                                folder_files=folder_data['folder_files'],
                                folder_password=password,
                                folder_status='Active',
                                last_change=last_change(),
                                )
                            print(folder_secure,'secure')

                            shared_folder_instance.save()

                            return Response({"profile_image": str(user_data['profile']),"name":user_data['first_name'],"email_id":user_data['email_id'],'to_user_id':user_data['id']}, status=rest_status.HTTP_201_CREATED)
                            
                        else:
                            print(f" No File Exit.")
                            return Response({"error": str('No File Exist')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        print(f"{user_data['first_name']} File Already Exit.")
                        return Response({"error": str('File Already Shared')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    print(e,f'Invalid {email_id} User')  
                    return Response({"error": str('Invalid User')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            # elif file_key == 1:
            #     print(password)
            #     datahouse_db = shared_datahouse.objects.get(to_user_id=auth_data['id'],id=file_id, file_status='Active')
            #     datahouse_data = json_fetch_one(datahouse_db)
            #     if datahouse_data['file_secure'] != 'Protected':
            #         try:
            #             user_db = users.objects.get(email_id=email_id,status='Active')
            #             user_data = json_fetch_one(user_db)
            #             if password == "":
            #                 password = datahouse_data['file_password']
            #                 file_secure = 'Private'
            #             else:
            #                 password=my_hash(datas['password'])
            #                 file_secure = 'Protected'
            #             shared_datahouse_db = shared_datahouse.objects.filter(from_user_id=auth_data['id'],to_user_id=user_data['id'],datahouse_id=file_id, file_status='Active')
            #             shared_datahouse_db = list(shared_datahouse_db.values())

            #             if shared_datahouse_db==[]:
            #                 if datahouse_data:
            #                     shared_datahouse_instance = shared_datahouse(
            #                         added_on=today(),
            #                         from_user_id=auth_data['id'],
            #                         to_user_id=user_db,
            #                         folder_id=0,
            #                         file_original_name=datahouse_data['file_original_name'],
            #                         file_name=datahouse_data['file_name'],
            #                         file_size=datahouse_data['file_size'],
            #                         expiry_date=datahouse_data['expiry_date'],
            #                         file_password=password,
            #                         file_status=datahouse_data['file_status'],
            #                         last_change=last_change(),
            #                         datahouse_id=datahouse_data['datahouse_id'],
            #                         file_secure=file_secure
            #                         )
            #                     print(file_secure,'secure')
            #                     user_setting_db = setting.objects.get(user_id=user_data['id'])
            #                     user_setting=json_fetch_one(user_setting_db)
            #                     # print('user_setting',user_setting)

            #                     new_storage=float(user_setting['current_storage']) + float(datahouse_data['file_size'])
            #                     # print(new_storage,file_check['file_size'])
            #                     if new_storage <= float(user_setting['storage']):
            #                         shared_datahouse_instance.save()
            #                         user_setting_db.current_storage=new_storage
            #                         user_setting_db.save()

            #                         return Response({"profile_image": str(user_data['profile']),"name":user_data['first_name'],"email_id":user_data['email_id'],'to_user_id':user_data['id']}, status=rest_status.HTTP_201_CREATED)
            #                     else:
            #                         print(f"{user_data['first_name']} reached the storage limit.")
            #                         return Response({"error": "You have reached the storage limit."}, status=rest_status.HTTP_403_FORBIDDEN)
            #                 else:
            #                     print(f" No File Exit.")
            #                     return Response({"error": str('No File Exist')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            #             else:
            #                 print(f"{user_data['first_name']} File Already Exit.")
            #                 return Response({"error": str('File Already Shared')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            #         except Exception as e:
            #             print(e,f'Invalid {email_id} User')  
                else:
                    return Response({"error": str('Unlock file from protected state!!')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({"error": str(auth_token['message'])}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @csrf_exempt
    def delete(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']
            data = request.data

            file_id=data['file_id']
            data = request.data
            datas=json.loads(data['data'])
            to_user_id=datas['to_user_id']
            try:
                shared_datahouse_db = shared_datahouse.objects.filter(from_user_id=auth_data['id'],datahouse_id=file_id).select_related('to_user_id')
                shared_datahouse_data = list(shared_datahouse_db.values('id','file_size','to_user_id__email_id','to_user_id'))
                for i in shared_datahouse_data:
                    if int(i['to_user_id']) == int(to_user_id):
                        shared_datahouse_instance = get_object_or_404(shared_datahouse, id=i['id'])
                        shared_datahouse_instance.delete()
                        user_setting_db = setting.objects.get(user_id=auth_data['id'])
                        user_setting=json_fetch_one(user_setting_db)
                        new_storage=float(user_setting['current_storage']) - float(shared_datahouse_instance.file_size)
                        if new_storage <0:
                            user_setting_db.current_storage=new_storage
                        else:
                            user_setting_db.current_storage=0
                        user_setting_db.save()
                        
                        return Response({'message': 'Shared File deleted successfully','to_user_id':to_user_id}, status=rest_status.HTTP_201_CREATED)
                    else:
                        return Response({"error": str('Invalid Password')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                print('error message: ',e)
                return Response({"error": str('Invalid File')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": str(auth_token['message'])}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)


class get_shared_file(APIView):
    @csrf_exempt
    def post(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']
            data = request.data

            file_id=data['file_id']
            data = request.data
            datas=json.loads(data['data'])
            email_id=datas['email_id']
            password=datas['password']
            file_key=datas['file_key']
            if file_key == 0:
                print(password)
                datahouse_db = datahouse.objects.get(user_id=auth_data['id'],id=file_id, file_status='Active')
                datahouse_data = json_fetch_one(datahouse_db)
                try:
                    user_db = users.objects.get(email_id=email_id,status='Active')
                    user_data = json_fetch_one(user_db)
                    if password == "":
                        password = datahouse_data['file_password']
                        file_secure = 'Private'
                    else:
                        password=my_hash(datas['password'])
                        file_secure = 'Protected'
                    shared_datahouse_db = shared_datahouse.objects.filter(from_user_id=auth_data['id'],to_user_id=user_data['id'],datahouse_id=file_id, file_status='Active')
                    shared_datahouse_db = list(shared_datahouse_db.values())

                    if shared_datahouse_db==[]:
                        if datahouse_data:
                            shared_datahouse_instance = shared_datahouse(
                                added_on=today(),
                                from_user_id=auth_data['id'],
                                to_user_id=user_db,
                                folder_id=0,
                                file_original_name=datahouse_data['file_original_name'],
                                file_name=datahouse_data['file_name'],
                                file_size=datahouse_data['file_size'],
                                expiry_date=datahouse_data['expiry_date'],
                                file_password=password,
                                file_status=datahouse_data['file_status'],
                                last_change=last_change(),
                                datahouse_id=datahouse_data['id'],
                                file_secure=file_secure
                                )
                            print(file_secure,'secure')
                            user_setting_db = setting.objects.get(user_id=user_data['id'])
                            user_setting=json_fetch_one(user_setting_db)
                            # print('user_setting',user_setting)

                            new_storage=float(user_setting['current_storage']) + float(datahouse_data['file_size'])
                            # print(new_storage,file_check['file_size'])
                            if new_storage <= float(user_setting['storage']):
                                shared_datahouse_instance.save()
                                user_setting_db.current_storage=new_storage
                                user_setting_db.save()

                                return Response({"profile_image": str(user_data['profile']),"name":user_data['first_name'],"email_id":user_data['email_id'],'to_user_id':user_data['id']}, status=rest_status.HTTP_201_CREATED)
                            else:
                                print(f"{user_data['first_name']} reached the storage limit.")
                                return Response({"error": "You have reached the storage limit."}, status=rest_status.HTTP_403_FORBIDDEN)
                        else:
                            print(f" No File Exit.")
                            return Response({"error": str('No File Exist')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        print(f"{user_data['first_name']} File Already Exit.")
                        return Response({"error": str('File Already Shared')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    print(e,f'Invalid {email_id} User')  
                    return Response({"error": str('Invalid User')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif file_key == 1:
                print(password)
                datahouse_db = shared_datahouse.objects.get(to_user_id=auth_data['id'],id=file_id, file_status='Active')
                datahouse_data = json_fetch_one(datahouse_db)
                if datahouse_data['file_secure'] != 'Protected':
                    try:
                        user_db = users.objects.get(email_id=email_id,status='Active')
                        user_data = json_fetch_one(user_db)
                        if password == "":
                            password = datahouse_data['file_password']
                            file_secure = 'Private'
                        else:
                            password=my_hash(datas['password'])
                            file_secure = 'Protected'
                        shared_datahouse_db = shared_datahouse.objects.filter(from_user_id=auth_data['id'],to_user_id=user_data['id'],datahouse_id=file_id, file_status='Active')
                        shared_datahouse_db = list(shared_datahouse_db.values())

                        if shared_datahouse_db==[]:
                            if datahouse_data:
                                shared_datahouse_instance = shared_datahouse(
                                    added_on=today(),
                                    from_user_id=auth_data['id'],
                                    to_user_id=user_db,
                                    folder_id=0,
                                    file_original_name=datahouse_data['file_original_name'],
                                    file_name=datahouse_data['file_name'],
                                    file_size=datahouse_data['file_size'],
                                    expiry_date=datahouse_data['expiry_date'],
                                    file_password=password,
                                    file_status=datahouse_data['file_status'],
                                    last_change=last_change(),
                                    datahouse_id=datahouse_data['datahouse_id'],
                                    file_secure=file_secure
                                    )
                                print(file_secure,'secure')
                                user_setting_db = setting.objects.get(user_id=user_data['id'])
                                user_setting=json_fetch_one(user_setting_db)
                                # print('user_setting',user_setting)

                                new_storage=float(user_setting['current_storage']) + float(datahouse_data['file_size'])
                                # print(new_storage,file_check['file_size'])
                                if new_storage <= float(user_setting['storage']):
                                    shared_datahouse_instance.save()
                                    user_setting_db.current_storage=new_storage
                                    user_setting_db.save()

                                    return Response({"profile_image": str(user_data['profile']),"name":user_data['first_name'],"email_id":user_data['email_id'],'to_user_id':user_data['id']}, status=rest_status.HTTP_201_CREATED)
                                else:
                                    print(f"{user_data['first_name']} reached the storage limit.")
                                    return Response({"error": "You have reached the storage limit."}, status=rest_status.HTTP_403_FORBIDDEN)
                            else:
                                print(f" No File Exit.")
                                return Response({"error": str('No File Exist')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            print(f"{user_data['first_name']} File Already Exit.")
                            return Response({"error": str('File Already Shared')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                    except Exception as e:
                        print(e,f'Invalid {email_id} User')  
                else:
                    return Response({"error": str('Unlock file from protected state!!')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({"error": str(auth_token['message'])}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @csrf_exempt
    def delete(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']
            data = request.data

            file_id=data['file_id']
            data = request.data
            datas=json.loads(data['data'])
            to_user_id=datas['to_user_id']
            try:
                shared_datahouse_db = shared_datahouse.objects.filter(from_user_id=auth_data['id'],datahouse_id=file_id).select_related('to_user_id')
                shared_datahouse_data = list(shared_datahouse_db.values('id','file_size','to_user_id__email_id','to_user_id'))
                for i in shared_datahouse_data:
                    if int(i['to_user_id']) == int(to_user_id):
                        shared_datahouse_instance = get_object_or_404(shared_datahouse, id=i['id'])
                        shared_datahouse_instance.delete()
                        user_setting_db = setting.objects.get(user_id=auth_data['id'])
                        user_setting=json_fetch_one(user_setting_db)
                        new_storage=float(user_setting['current_storage']) - float(shared_datahouse_instance.file_size)
                        if new_storage <0:
                            user_setting_db.current_storage=new_storage
                        else:
                            user_setting_db.current_storage=0
                        user_setting_db.save()
                        
                        return Response({'message': 'Shared File deleted successfully','to_user_id':to_user_id}, status=rest_status.HTTP_201_CREATED)
                    else:
                        return Response({"error": str('Invalid Password')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                print('error message: ',e)
                return Response({"error": str('Invalid File')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": str(auth_token['message'])}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

class delete_folder(APIView):
    @csrf_exempt
    def delete(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']
            data = request.data
            # print(data)
            file_id=data['file_id']
            datas=json.loads(data['data'])
            password=my_hash(datas['password'])
            file_key=datas['file_key']
            try:
                try:
                    user_db = users.objects.get(id=auth_data['id'],secret_key=password,status='Active')
                    user_data = json_fetch_one(user_db)
                    print(user_data)
                except:
                    return Response({"error": str('Invalid File Password')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                try:
                    if int(file_key) == 0:
                        try:
                            folder_db=folder.objects.get(user_id=auth_data['id'],id=file_id)
                            folder_db=json_fetch_one(folder_db)
                        except:
                            return Response({"error": str('Invalid Folder')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

                        if folder_db:
                            # Get the datahouse instance or return a 404 response if not found
                            folder_instance = get_object_or_404(folder, user_id=auth_data['id'], id=file_id)

                            # Delete the folder instance
                            folder_instance.delete()

                            # Get the datahouse instance or return a 404 response if not found
                            shared_folder_instance = get_object_or_404(shared_folder, id=file_id)

                            # Delete the shared_folder instance
                            shared_folder_instance.delete()

                            try:
                                datahouse_db = datahouse.objects.filter(file_status='Active',folder_id=file_id)
                                datahouse_db = json_fetch_all(datahouse_db)
                                for i in datahouse_db:
                                    # Get the user's setting instance
                                    user_setting_db = setting.objects.get(user_id=i['user_id'])
                                    user_setting = json_fetch_one(user_setting_db)

                                    # Update the user's storage setting
                                    new_storage = float(user_setting['current_storage']) - float(i['file_size'])
                                    if new_storage <0:
                                        user_setting_db.current_storage=new_storage
                                    else:
                                        user_setting_db.current_storage=0
                                    user_setting_db.save()

                                    # Get the datahouse instance or return a 404 response if not found
                                    datahouse_delete = get_object_or_404(datahouse, id=i['id'])

                                    # Delete the folder instance
                                    datahouse_delete.delete()
                            except:
                                pass
                            try:
                                shared_datahouse_db = shared_datahouse.objects.filter(file_status='Active',folder_id=file_id)
                                shared_datahouse_db = json_fetch_all(shared_datahouse_db)
                                for i in shared_datahouse_db:
                                    # Get the user's setting instance
                                    user_setting_db = setting.objects.get(user_id=i['to_user_id'])
                                    user_setting = json_fetch_one(user_setting_db)

                                    # Update the user's storage setting
                                    new_storage = float(user_setting['current_storage']) - float(i['file_size'])
                                    if new_storage <0:
                                        user_setting_db.current_storage=new_storage
                                    else:
                                        user_setting_db.current_storage=0
                                    user_setting_db.save()

                                    # Get the datahouse instance or return a 404 response if not found
                                    datahouse_delete = get_object_or_404(shared_datahouse, id=i['id'])

                                    # Delete the folder instance
                                    datahouse_delete.delete()
                            except:
                                pass
                         
                            return Response({'message': 'File deleted successfully','file_id':file_id}, status=rest_status.HTTP_201_CREATED)
                        else:
                            return Response({"error": str('Invalid Folder')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    print('error message: ',e)
                    return Response({"error": str('Invalid File')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error": str('Not Authorised to delete File')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": str(auth_token['message'])}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class delete_file(APIView):
    @csrf_exempt
    def delete(self,request):
        auth_token=auth_token_required(request)
        if auth_token['status']==200:
            auth_data=auth_token['message']
            data = request.data
            # print(data)
            file_id=data['file_id']
            datas=json.loads(data['data'])
            password=my_hash(datas['password'])
            file_key=datas['file_key']
            try:
                try:
                    user_db = users.objects.get(id=auth_data['id'],secret_key=password,status='Active')
                    user_data = json_fetch_one(user_db)
                    print(user_data)
                except:
                    return Response({"error": str('Invalid File Password')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                try:
                    if int(file_key) == 0:
                    
                        # Get the datahouse instance or return a 404 response if not found
                        datahouse_instance = get_object_or_404(datahouse, user_id=auth_data['id'], id=file_id)

                        # Delete the datahouse instance
                        datahouse_instance.delete()

                        # Get the user's setting instance
                        user_setting_db = setting.objects.get(user_id=auth_data['id'])
                        user_setting = json_fetch_one(user_setting_db)

                        # Update the user's storage setting
                        new_storage = float(user_setting['current_storage']) - float(datahouse_instance.file_size)
                        if new_storage <0:
                            user_setting_db.current_storage=new_storage
                        else:
                            user_setting_db.current_storage=0
                        user_setting_db.save()

                        return Response({'message': 'File deleted successfully','file_id':file_id}, status=rest_status.HTTP_201_CREATED)
                    elif int(file_key)==1:
                        
                        # Get the datahouse instance or return a 404 response if not found
                        datahouse_instance = get_object_or_404(shared_datahouse, to_user_id=auth_data['id'], id=file_id)

                        # Delete the datahouse instance
                        datahouse_instance.delete()

                        # Get the user's setting instance
                        user_setting_db = setting.objects.get(user_id=auth_data['id'])
                        user_setting = json_fetch_one(user_setting_db)

                        # Update the user's storage setting
                        new_storage = float(user_setting['current_storage']) - float(datahouse_instance.file_size)
                        if new_storage <0:
                            user_setting_db.current_storage=new_storage
                        else:
                            user_setting_db.current_storage=0
                        user_setting_db.save()

                        return Response({'message': 'File deleted successfully','file_id':file_id}, status=rest_status.HTTP_201_CREATED)
                    else:
                        return Response({"error": str('Invalid File Key')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
                except Exception as e:
                    print('error message: ',e)
                    return Response({"error": str('Invalid File')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error": str('Not Authorised to delete File')}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": str(auth_token['message'])}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

class api_download_files(APIView):
    @csrf_exempt
    def get(self,request):
        image_token = request.GET.get('image_token', None)
        # print(data)
        # image_token=data['image_token']
        access_token=file_decode_token(image_token)
        print(access_token,'#################access_token')
        if 'message' in access_token:
            access_token=access_token['message']
            file_name=access_token['file_name']
            save_name=access_token['file_original_name']
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            print(file_path)

            if access_token['file_secure']=='Public':

                # Check if the file exists
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        ciphertext = file.read()
                    decrypted_content = files_encryptor().decrypt(ciphertext)
                    response = FileResponse(io.BytesIO(decrypted_content))
                    response['Content-Disposition'] = f'attachment; filename="{save_name}"'
                    print(response)
                    return response
            elif access_token['file_secure'] == 'Private':
                print('asfmsaodnfkjndsjangjkadsn')
                try:
                    auth_token=auth_token_required(request)
                    if auth_token['status']==200:
                        auth_data=auth_token['message']
                        if access_token['user_id'] == auth_data['id']:
                            # Check if the file exists
                            if os.path.exists(file_path):
                                with open(file_path, 'rb') as file:
                                    ciphertext = file.read()
                                decrypted_content = files_encryptor().decrypt(ciphertext)
                                response = FileResponse(io.BytesIO(decrypted_content))
                                response['Content-Disposition'] = f'attachment; filename="{save_name}"'
                                print(response)
                                return response
                        else:
                            return Response({'error': 'Invalid User.'}, status=rest_status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({'error': 'Invalid User.'}, status=rest_status.HTTP_404_NOT_FOUND)
                except:
                    return Response({'error': 'Invalid User.'}, status=rest_status.HTTP_404_NOT_FOUND)
            elif access_token['file_secure'] == 'Protected':
                expiry_time = access_token["expiry"]

                if time.time() > expiry_time:
                    return redirect("/datahouse/")
                else:
                    # Check if the file exists
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as file:
                            ciphertext = file.read()
                        decrypted_content = files_encryptor().decrypt(ciphertext)
                        response = FileResponse(io.BytesIO(decrypted_content))
                        response['Content-Disposition'] = f'attachment; filename="{save_name}"'
                        print(response)
                        return response
                        # http://127.0.0.1:8000/api_download_files/?image_token=
            else:
                return Response({'error': 'Invalid File Type.'}, status=rest_status.HTTP_404_NOT_FOUND)
        else:
                return Response({'error': access_token['error']}, status=rest_status.HTTP_404_NOT_FOUND)


class user_details(APIView):
    @csrf_exempt
    def get(self,request):
        auth_token=auth_token_required(request)
        auth_token=auth_token['message']
        return Response({'name': auth_token['name'],'email_id':auth_token['email_id'],'profile':auth_token['profile']}, status=rest_status.HTTP_201_CREATED)
