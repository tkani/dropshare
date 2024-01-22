
import time
import jwt
import json

from django.utils.functional import wraps
from django.shortcuts import get_object_or_404,redirect
from rest_framework import status as rest_status
from django.http import HttpResponseForbidden, HttpResponseServerError


from . models import *
from dropshare.secret_data import *

def file_encode_token(payload):
	expiration_time = time.time() + (3600*20)
	payload['expiry'] = expiration_time
	secret_key=token_secret_key()
	encoded_token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
	return encoded_token

def file_decode_token(encoded_token):
	try:
		secret_key=token_secret_key()
		decoded_payload = jwt.decode(encoded_token, secret_key, algorithms=['HS256'])
		return {'message':decoded_payload}
	except jwt.ExpiredSignatureError:
	    print({'error':"Token has expired."})
	    return {'error':"Token has expired."}
	except jwt.InvalidTokenError:
	    print({'error':"Invalid token."})
	    return {'error':"Invalid token."}

def encode_token(payload):
	expiration_time = time.time() + (3600*20)
	payload['expiry'] = expiration_time
	secret_key=token_secret_key()
	encoded_token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
	return encoded_token

def decode_token(encoded_token):
	try:
		secret_key=token_secret_key()
		decoded_payload = jwt.decode(encoded_token, secret_key, algorithms=['HS256'])
		return decoded_payload
	except jwt.ExpiredSignatureError:
	    print("Token has expired.")
	    return redirect("/")
	except jwt.InvalidTokenError:
	    print("Invalid token.")
	    return redirect("/")


def session_token(_function):
	@wraps(_function)
	def wrapper_function(request, *args, **kwargs):
		if "session_token" not in request.session:
			return redirect("/sign_in/")

		token = request.session["session_token"]
		try:
			decoded_token = decode_token(token)
		except jwt.ExpiredSignatureError:
			print("Token has expired.")
			return redirect("/sign_in/")
		except jwt.InvalidTokenError:
			print("Invalid token.")
			return redirect("/sign_in/")

		user_id = decoded_token["id"]
		password = decoded_token["password"]
		secret_key = decoded_token["secret_key"]
		expiry_time = decoded_token["expiry"]

		if time.time() > expiry_time:
			request.session.clear()
			print("Token has expired.")
			return redirect("/sign_in/")

		payload=decoded_token
		payload.pop("expiry", None)
		request.session["session_token"]=encode_token(payload)

		try:
			result = users.objects.get(id=user_id, password=password, secret_key=secret_key)
			result_data = json_fetch_one(result)
		except users.DoesNotExist:
			print("User not found.")
			return redirect("/sign_in/")

		if not result_data:
			return redirect("/sign_in/")

		password_hash = result_data["password"]
		return _function(request, *args, **kwargs)

	return wrapper_function


def auth_token_required(request):
	
	try:
		token = None
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
			request.session['session_token'] = token
		elif 'session_token' in request.session:
			token = request.session['session_token']

		if not token:
			return {"message":"Token not provided.","status":rest_status.HTTP_403_FORBIDDEN}
		try:
			decoded_token = decode_token(token)
		except jwt.ExpiredSignatureError:
			return {"message":"Token has expired.","status":rest_status.HTTP_403_FORBIDDEN}
		except jwt.InvalidTokenError:
			return {"message":"Invalid token.","status":rest_status.HTTP_403_FORBIDDEN}

		if "id" not in decoded_token or "secret_key" not in decoded_token or "password" not in decoded_token or "expiry" not in decoded_token:
			return {"message":"Invalid token format.","status":rest_status.HTTP_403_FORBIDDEN}

		user_id = decoded_token["id"]
		password = decoded_token["password"]
		expiry_time = decoded_token["expiry"]
		secret_key = decoded_token["secret_key"]

		if time.time() > expiry_time:
			request.session.clear()
			print("Token has expired.")
			return {"message":"Token has expired.","status":rest_status.HTTP_403_FORBIDDEN}
		
		payload=decoded_token
		payload.pop("expiry", None)
		request.session["session_token"]=encode_token(payload)

		try:
			result = users.objects.get(id=user_id, password=password, secret_key=secret_key)
			result_data = json_fetch_one(result)
		except users.DoesNotExist:
			return {"message":"User not found.","status":rest_status.HTTP_403_FORBIDDEN}

		if result_data:
			response_data = {
				'id': user_id,
				'email_id': result_data['email_id'],
				'name': result_data['first_name'],
				'password': result_data['password'],
				'secret_key': result_data['secret_key'],
				'profile': str(result_data['profile']),
				'session' : request.session["session_token"]
				}
			return {'message':response_data, "status":rest_status.HTTP_200_OK}
		else:
			return {"message":"Invalid credentials.","status":rest_status.HTTP_403_FORBIDDEN}
	except Exception as e:
		return {"message":"Invalid credentials.","status":rest_status.HTTP_403_FORBIDDEN}

