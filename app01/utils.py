#!/usr/bin/env python
# coding:utf-8
#My_Name:Mrs_HAN 韩晓飞
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request
from rest_framework.exceptions import APIException
from app01 import models
class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token=request.query_params.get('token')
        obj=models.UserInfo.objects.filter(token=token).first()
        if obj:
            return (obj.username,obj)
        raise APIException('用户认证失败')