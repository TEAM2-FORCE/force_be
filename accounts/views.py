from django.shortcuts import render
from django.shortcuts import redirect

BASE_URL = 'https://vebeserver.o-r.kr/'
LOCAL_URL = 'http://localhost:8000/'

GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback'

# TEST = LOCAL_URL + 'accounts/google/callback/'

def google_login(request):
     scope = "https://www.googleapis.com/auth/userinfo.email " + \
             "https://www.googleapis.com/auth/userinfo.profile"
     client_id = '1084783697214-fg1r9e3q4glg96hl5t15ghmsr1piicko.apps.googleusercontent.com'
#     client_id = '569562316946-jn23hdqjtkkosssbgrt06hpo2bat4ujp.apps.googleusercontent.com'
     return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

################################
from pathlib import Path
from json import JSONDecodeError
from django.http import JsonResponse
import requests
from .models import *
from allauth.socialaccount.models import SocialAccount

from django.core.exceptions import ImproperlyConfigured
from rest_framework import status
from rest_framework import response
import os
import json

from rest_framework_simplejwt.tokens import RefreshToken

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, 'secrets.json') 

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)
    

def get_redirect_url(request):
    host = request.META.get('HTTP_REFERER')
    
    if host == 'http://localhost:3000/':
        redirect_uri = 'http://localhost:3000/oauth2redirect'
    else:
        redirect_uri = 'https://vebe.netlify.app/oauth2redirect'

    return redirect_uri

def google_callback(request):
    client_id = '1084783697214-fg1r9e3q4glg96hl5t15ghmsr1piicko.apps.googleusercontent.com'
    client_secret = get_secret('CLIENT_SECRET')
    code = request.GET.get('code')
   # body = json.loads(request.body.decode('utf-8'))
   # code = body['code']
  #  state = 'state_parameter_passthrough_value'
    state = "random_state"
    redirect_uri = GOOGLE_CALLBACK_URI

   

    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}&state={state}")
    
    #### 1-1. json으로 변환 & 에러 부분 파싱
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    print(token_req_json)

    #### 1-2. 에러 발생 시 종료
    if error is not None:
        raise JSONDecodeError(error)

    #### 1-3. 성공 시 access_token 가져오기
    access_token = token_req_json.get('access_token')
    

    #### 2. 가져온 access_token으로 이메일값을 구글에 요청
    profile_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = profile_req.status_code

    #### 2-1. 에러 발생 시 400 에러 반환
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    

    #### 2-2. 성공 시 이메일 가져오기
    profile_req_json = profile_req.json()
    email = profile_req_json.get('email')
    

    #### 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
    try:
        # 전달받은 이메일로 등록된 유저가 있는지 탐색
        user = User.objects.get(email=email)

        # print("로그인 유저 이메일", user.email)

        refresh = RefreshToken.for_user(user)
        # print("token",refresh)
        response_data = {'access_token': str(refresh.access_token)}

        return JsonResponse(response_data)


        
        return response
        
    except User.DoesNotExist:
        # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급

        new_user_info = User(email=email).save()
        # print(new_user_info.email)

        refresh = RefreshToken.for_user(new_user_info)
        response_data = {'access_token': str(refresh.access_token)}

        return JsonResponse(response_data)

# #################################
from rest_framework.views import APIView
from rest_framework.response import Response

class GoogleProfileName(APIView):
    def get(self, request):
        user = request.user  # 현재 로그인한 사용자
        user_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return Response(user_data)
