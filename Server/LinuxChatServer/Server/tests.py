# coding:utf-8

from django.test import TestCase
import time

from models import User,Group


user = User(nick="shang",pwd="2121",sex="M",sign="sign")
user.save()


class ModelTestCase(TestCase):

    def setUp(self):
        print "setup"

    def test_user_insert(self):
        # User.objects.get(nick)
        user = User(nick="shang",pwd="2121",sex="M",sign="sign")
        user.save()
        print "success:" + str(user._uid)

    def test_friends(self):
        user1 = User(nick="shang",pwd="12")
        user1.save()
        user2 = User(nick="ming",pwd="W",sex="W")
        user2.save()
        user2.friends.add(user1)

    def group_insert(self):
        group = Group(name="owner",owner="dsd",create_time=time.time(),max_num=12)
        group.save()

