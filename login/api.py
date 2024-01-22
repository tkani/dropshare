import json

# -- Rest APi Framework --#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework import status as rest_status
from django.views.decorators.csrf import csrf_exempt

# -- Imports --#
from . models import *
from dropshare.secret_data import *
from . tokenvalidation import *
from user.models import *

class signup(APIView):
    @csrf_exempt
    # parser_classes = [JSONParser, MultiPartParser]
    def post(self,request):
        data = request.data
        profile_file = request.FILES.get('profile')
        
        # Validate the required fields in json_data
        required_fields = ['first_name','last_name', 'email_id', 'mobile_no', 'password', 'agreement']
        if not all(field in data for field in required_fields):
            missing_fields = [field for field in required_fields if field not in data]
            return Response({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=rest_status.HTTP_400_BAD_REQUEST)

        status='Active'
        # Create a new users instance and save it
        try:
            new_user = users(
                added_on=today(),
                first_name=data['first_name'],
                last_name=data['last_name'],
                email_id=data['email_id'],
                mobile_no=data['mobile_no'],
                password=my_hash(data['password']),
                secret_key=my_hash(data['secret_key']),
                hash_key=my_hash('random'),
                agreement=data['agreement'],
                status=status,
                last_change=last_change()
            )

            # Set other optional fields
            try:
                img_check_=image_check(profile_file)
                new_user.profile = img_check_['file']
                new_user.old_file_name = img_check_['old_name']
            except:
                new_user.profile = 'profile_images/Default.jpg'
                new_user.old_file_name = 'Default.jpg'
            # print(new_user)
            new_user.save()
            user_id = new_user.id
            print(user_id,'user_id')

            user_setting = setting(
                added_on=today(),
                user_id=user_id,
                storage=storage(),
                current_storage=0,
                plan_id=1,
                plan_name='Free Plan',
                plan_expiray_date=last_change(),
                file_status='Active',
                last_change=last_change()
                )

            user_setting.save()
            
            user_shared_folder = shared_folder(
                added_on=today(),
                from_user_id=user_id,
                to_user_id=new_user,
                folder_id=0,
                folder_files=0,
                folder_size=0,
                folder_original_name=my_hash('random'),
                folder_name='Shared Files',
                folder_password='',
                folder_status='Active',
                last_change=last_change()
                )
            user_shared_folder.save()

            return Response({"message": "User created successfully"}, status=rest_status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)

class sign_in(APIView):
    @csrf_exempt
    def post(self,request):
        data = request.data

        # Validate the required fields in the JSON payload
        required_fields = ['password','secret_key']
        if not all(field in data for field in required_fields):
            return Response({"error": "Missing required fields in JSON payload"}, status=rest_status.HTTP_400_BAD_REQUEST)

        password = my_hash(data['password'])
        secret_key = my_hash(data['secret_key'])

        # Retrieve the user from the database
        try:
            user = users.objects.get(password=password,secret_key=secret_key)

            user_data=json_fetch_one(user)
            payload={'id':user_data['id'],'email_id':user_data['email_id'],'password':user_data['password'],'secret_key':secret_key}

            # Use a secure method to create a token
            session_token = encode_token(payload)

            # Check the provided password against the stored password
            if user_data:
                return Response({"message": "Login successful",'session':session_token,'name':user_data['first_name']}, status=rest_status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=rest_status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": "User not found"}, status=rest_status.HTTP_404_NOT_FOUND)

        