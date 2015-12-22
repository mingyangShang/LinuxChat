# -*- coding:utf-8 -*-

import json

from django.shortcuts import render
from django.http import HttpResponse,HttpRequest


from dbhelper import DBHelper
# Create your views here.
def index(request):
    return HttpResponse("H你好ello World")

def index2(request):
    return HttpResponse("你好Index2")

def register(request):
    username = request.GET.__getitem__("name")
    pwd = request.GET.__getitem__("pwd")
    sex = request.GET.__getitem__("sex")
    sign = request.GET.__getitem__("sign")

    db_msg = DBHelper.register(user_name=username,user_pwd=pwd,user_sex=sex,user_sign=sign)
    if db_msg.success:
        return HttpResponseFactory.create(success=True)
    else:
        return HttpResponseFactory.create(success=False,error=db_msg.error)

def login(request):
    username = request.GET.__getitem__("name")
    pwd = request.GET.__getitem__("pwd")

    db_msg = DBHelper.login(user_name=username,user_pwd=pwd)
    if db_msg.success:
        return HttpResponseFactory.create(success=True,data=db_msg.msg.to_json())
    else:
        return HttpResponseFactory.create(success=False,error=db_msg.error)

def query_user(request):
    username = get_attr(request,"name")
    db_msg = DBHelper.query_user(user_name=username)
    if db_msg.success:
        return HttpResponseFactory.create(success=True,data=db_msg.msg.to_json())
    else:
        return HttpResponseFactory.create(success=False,error=db_msg.error)

def create_group(request):
    name = get_attr(request,"group_name")
    owner = get_attr(request,"owner")
    members = get_attr(request,"members")
    db_msg = DBHelper.create_group(group_owner=owner,group_name=name,group_members=members)
    if db_msg.success:
        return HttpResponseFactory.create(success=True,data=db_msg.msg.to_json())
    else:
        return HttpResponseFactory.create(success=False,error=db_msg.error)

def invite_friend(request):
    from_user = get_attr(request,"from")
    to_user = get_attr(request,"to")
    reason = get_attr(request,"reason")

    db_msg = DBHelper.invite_friend(from_user,to_user,reason)
    if db_msg.success:
        return HttpResponseFactory.create(success=True)
    else:
        return HttpResponseFactory.create(success=False,error=db_msg.error)

def reply_invite_friend(request):
    from_user = get_attr(request,"from")
    to_user = get_attr(request,"to")
    accept = get_attr(request,"accept")

    if accept:
        db_msg = DBHelper.accept_friend(from_user,to_user)
    else:
        db_msg = DBHelper.refuse_user_invite(from_user,to_user)
    if db_msg.success:
        return HttpResponseFactory.create(success=True,data=db_msg.msg)
    else:
        return HttpResponseFactory.create(success=False,data=db_msg.error)


def accept_friend(request):
    from_user = get_attr(request,"from")
    to_user = get_attr(request,"to")

    db_msg = DBHelper.accept_friend(from_user,to_user)
    if db_msg.success:
        return HttpResponseFactory.create(success=True,data=db_msg.msg)
    else:
        return HttpResponseFactory.create(success=False,error=db_msg.error)


def invite_members(request):
    from_user = get_attr(request,"from")
    to_users = get_attr(request,"to")
    to_group = get_attr(request,"group")

    db_msg = DBHelper.invite_members(from_user,to_users,to_group)
    if db_msg.success:
        return HttpResponseFactory.create(success=True,data=db_msg.msg.to_json())
    else:
        return HttpResponseFactory.create(success=False,data=db_msg.error)


class HttpResponseFactory(object):

    @staticmethod
    def create(success=True,error="",data=""):
        return HttpResponse(json.dumps({"success":success,"error":error,"data":data},ensure_ascii=False))


def get_attr(request,name):
    return request.GET.get(name)
