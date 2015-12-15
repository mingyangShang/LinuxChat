# coding:utf-8
from __future__ import unicode_literals

from django.db import models
import uuid

from custom_fields import TimestampField
# Create your models here.


class User(models.Model):

    sex_choice = (
        ('M','man'),
        ('W','woman')
    )
    _uid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    nick = models.CharField(max_length=20,default="")
    pwd = models.CharField(max_length=32,default="")
    sex = models.CharField(max_length=1,default='M',choices=sex_choice)
    sign = models.CharField(max_length=40,default="")

    friends = models.ManyToManyField("self",db_table="Friends")

# class Friends(models.Model):
#
#     uid = models.ForeignKey(User,on_delete=models.CASCADE)
#     friend_id = models.ForeignKey(User,on_delete=models.CASCADE)

class Group(models.Model):

    _gid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User,related_name="owner",related_query_name="owner")
    create_time = TimestampField()
    max_num = models.IntegerField(default=10)

    members = models.ManyToManyField(User,through="Members")

class Members(models.Model):

    gid = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="groupid",related_query_name="groupid")
    uid = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userid",related_query_name="userid")

class MsgType(models.Model):


    type_choice = (
        ('text', '普通文本'),
        ('img', '图片'),
        ('file', '文件'),
        ('link', '链接'),
        ('code', '代码'),
        ('face', '表情'),
    )

    _tid = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20,choices=type_choice,default='text')

class Msg(models.Model):

    _mid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(User,related_name="from_user",related_query_name="from_user")
    to_user = models.ForeignKey(User,related_name="to_user",related_query_name="to_user")
    to_group = models.ForeignKey(Group,related_name="to_group",related_query_name="to_group")
    type = models.ForeignKey(MsgType)
    text_content = models.TextField()
    file_content = models.FileField()
    image_content = models.ImageField()

class Demo(models.Model):
    demo = models.CharField(max_length=20)