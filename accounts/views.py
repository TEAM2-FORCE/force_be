from django.shortcuts import render
from django.shortcuts import redirect

BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'

def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email " + \
            "https://www.googleapis.com/auth/userinfo.profile"
    client_id = '569562316946-jn23hdqjtkkosssbgrt06hpo2bat4ujp.apps.googleusercontent.com'
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
    

def google_callback(request):
    client_id = '569562316946-jn23hdqjtkkosssbgrt06hpo2bat4ujp.apps.googleusercontent.com'
    client_secret = get_secret('CLIENT_SECRET')
    code = request.GET.get('code')
    state = "random_state"

    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    
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
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    #### 2-1. 에러 발생 시 400 에러 반환
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    
    # ### 2-2. 성공 시 이메일/소셜ID 가져오기
    # user = response.json()
    # email = user.get('email')
    # sub = user.get('sub')

    # # 전달 받은 social_id로 user가 있는지 확인
    # if User.objects.filter(social_id=sub).exists():
    #     user_info = User.objects.get(social_id=sub)

    #     # 소셜 로그인만 하고 회원가입은 안한 사람은 False로, 회원가입까지 한 사람은 True로 return
    #     if user_info.is_active == False:
    #         token = get_tokens_for_user(user_info)
    #         return JsonResponse({
    #             'token':token,
    #             'is_active':user_info.is_active
    #         }, status=200)
    #     else:
    #         token = get_tokens_for_user(user_info)
    #         return JsonResponse({
    #             'token':token,
    #             'is_active':user_info.is_active
    #         })
        
    # # 아예 회원가입 안한 사람
    # else:
        
    #     new_user_info = User.objects.create(
    #         social_id = sub,
    #         email = email
    #     )
    #     new_user_info.save()
    #     token = get_tokens_for_user(new_user_info)
    #     return JsonResponse({
    #         'token':token,
    #         'is_active':new_user_info.is_active
    #     })

    #### 2-2. 성공 시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    #return JsonResponse({'access': access_token, 'email':email})

    

    #### 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
    try:
        # 전달받은 이메일로 등록된 유저가 있는지 탐색
        user = User.objects.get(email=email)

        # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
        social_user = SocialAccount.objects.get(user=user)

        # 있는데 구글계정이 아니어도 에러
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

        # 이미 Google로 제대로 가입된 유저 => 로그인 & 해당 유저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

        refresh = RefreshToken.for_user(user)
        # accept_json = accept.json()
        # accept_json.pop('user', None)

        return JsonResponse({'access_token': str(refresh.access_token)})

    except User.DoesNotExist:
        # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
        
    

    
################################
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
    