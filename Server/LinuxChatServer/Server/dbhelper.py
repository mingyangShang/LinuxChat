# -*- coding:utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist

from models import User,Group,Members,Invite


class DBHelper(object):

    @staticmethod
    def register(user_name,user_pwd,user_sex,user_sign):

        if not user_name or len(user_name) == 0:
            return DBMsg(success=False,error=u"用户名不能为空")
        if not user_pwd or len(user_pwd) == 0:
            return DBMsg(success=False,error=u"密码不能为空")

        user = User.objects.filter(name=user_name)
        if len(user) != 0:
            return DBMsg(success=False,error=u"该用户名已存在")

        new_user = User(name=user_name,pwd=user_pwd,sex=user_sex,sign=user_sign)
        new_user.save()
        return DBMsg(success=True)

    @staticmethod
    def login(user_name,user_pwd):
        try:
            user = User.objects.get(name=user_name,pwd=user_pwd)
        except ObjectDoesNotExist:
            return DBMsg(success=False,error=u"用户名或密码不正确")
        else:
            return DBMsg(success=True,error="",msg=user)

    @staticmethod
    def query_user(user_name="",user_id=""):
        user = User()
        if user_id:
            user = User.objects.filter(_uid=user_id)
        elif user_name:
            user = User.objects.filter(name=user_name)
        else:
            return DBMsg(success=False,error=u"查询条件不能为空")

        if len(user) > 0:
            return DBMsg(success=True,msg=user[0])
        else:
            return DBMsg(success=False,error=u"查询结果为空")

    @staticmethod
    def create_group(group_owner,group_name="",group_members=[]):
        group = Group.objects.filter(name=group_name)
        if len(group) > 0:
            return DBMsg(success=False,error=u"该群组名称已存在")
        else:
            owner = User.objects.filter(_uid=group_owner)
            if owner and len(owner) > 0:
                owner = owner[0]
            else:
                return DBMsg(success=False,msg=u"创建者为非法用户")
            try:
                new_group = Group(name=group_name,owner=owner)
                new_group.save()
            except ValueError,valueError:
                print  valueError
                return DBMsg(success=False,error=u"创建者为非法用户")

            map(lambda userid:Members(gid=new_group,uid=owner).save(),group_members)
            return DBMsg(success=True,msg=new_group)

    @staticmethod
    def invite(from_user,to_user="",to_group="",reason=u"加个好友吧"):

        if to_user:
            return DBHelper.invite_friend(from_user,to_user,reason)
        elif to_group:
            return DBHelper.invite_group(from_user,to_group,reason)
        else:
            return DBMsg(success=False,error=u"参数不合法")

    @staticmethod
    def invite_friend(from_user_name,to_user_name,reason=u"加个好友吧"):
        try:
            user1 = User.objects.get(name=from_user_name)
            user2 = User.objects.get(name=to_user_name)

            new_invite_msg = Invite(from_user=user1,to_user=user2,invite_reason=reason)
            new_invite_msg.save()

        except ValueError:
            return DBMsg(success=False,error=u"邀请失败")
        return DBMsg(success=True,msg=u"已成功发送邀请,等待对方回复")


    # TODO 暂不处理加入群组需要验证的功能
    @staticmethod
    def invite_members(from_user,to_users,to_group):
        if to_users and to_users is list and len(to_users) > 0:
            return DBMsg(success=False,error=u"未选择要添加的组成员")

        group = Group.objects.filter(name=to_group)
        if len(group) == 0:
            return DBMsg(success=False,error=u"该群组不存在")
        else:
            map(lambda username:Members(gid=group[0],uid=User.objects.get(name=username)).save(),to_users)
            return DBMsg(success=True,msg=group)


    @staticmethod
    def accept_friend(from_user,to_user):
        if to_user and from_user:
            return DBHelper.accept_user_invite(from_user,to_user)
        else:
            return DBMsg(success=False,error=u"参数不合法")


    @staticmethod
    def accept_user_invite(from_user,to_user,accept):
        try:
            user1 = User.objects.get(name=from_user)
            user2 = User.objects.get(name=to_user)
            invite_msg = Invite.objects.get(from_user=user1,to_user=user2)
            invite_msg.status = Invite.STATUS_ACCEPTED
            invite_msg.save()
        except ValueError,error:
            print error
            return DBMsg(success=False,error=u"参数不合法")
        else:
            return DBMsg(success=True,msg=user2.name+u"同意了你的好友申请")

    @staticmethod
    def refuse_user_invite(from_user,to_user):
        try:
            user1 = User.objects.get(name=from_user)
            user2 = User.objects.get(name=to_user)
            invite_msg = Invite.objects.get(from_user=user1,to_user=user2)
            invite_msg.status = Invite.STATUS_REFUSED
            invite_msg.save()
        except ValueError,error:
            print error
            return DBMsg(success=False,error=u"参数不合法")
        else:
            return DBMsg(success=True,msg=user2.name+"拒绝了你的好友申请")


    @staticmethod
    def accept_group_invite(from_user,to_group):
        pass


class DBMsg(object):

    """
    @param success True or False
    @param error string
    """
    def __init__(self,success=True,error="",msg=""):
        self.success = success
        self.error = error
        self.msg = msg