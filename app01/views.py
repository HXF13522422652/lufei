from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from app01 import models
import hashlib
import time
class AuthView(APIView):
    authentication_classes = []

    def get(self, request):
        """
        接收用户名和密码
        :param request:
        :return:
        """
        ret = {'code': 1000, 'msg': None}

        user = request.query_params.get('user')
        pwd = request.query_params.get('pwd')

        obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
        if not obj:
            ret['code'] = 1001
            ret['msg'] = "用户名或密码错误"
            return Response(ret)
        # 创建随机字符串
        ctime = time.time()
        key = "%s|%s" % (user, ctime)
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        token = m.hexdigest()

        # 保存到数据
        obj.token = token
        obj.save()

        ret['token'] = token
        return Response(ret)

class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token=request.query_params.get('token')
        obj=models.UserInfo.objects.filter(token=token).first()
        if obj:
            return (obj.username,obj)
        raise APIException('用户认证失败')
class HostView(APIView):
    authentication_classes = [MyAuthentication,]
    def get(self,request,*args,**kwargs):
        self.dispatch
        return Response('课程表')






















