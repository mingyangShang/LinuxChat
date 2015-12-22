from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name="index"),
    url(r'^index$',views.index2,name="index2"),
    url(r'^user/register',views.register,name="register"),
    url(r'^user/login',views.login,name="login"),
    url(r'^group/create',views.create_group,name="create_group"),
    url(r'^user/invite',views.invite_friend,name="invite_friend"),
    url(r'^user/accept',views.accept_friend,name="accept_friend"),
    url(r'^group/invite',views.invite_members,name="invite_members"),
    url(r'^user/invite/reply',views.reply_invite_friend,name="reply_invite"),
    url(r'^group/invite',views.invite_members,name="invite_members")
]
