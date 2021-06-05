from django.urls import path,include
from webapp.views import *

urlpatterns = [

    path('',index.as_view(),name="index"),
    path('superadmin/',superadmin.as_view(),name="superadmin"),
    path('superadminuser',superadminuser.as_view(),name="superadminuser"),
    path('superadminevent',superadminevent.as_view(),name="superadminevent"),
    path('superadminaddevent',superadminaddevent.as_view(),name="superadminaddevent"),
    path('superadmineventtype',superadmineventtype.as_view(),name="superadmineventtype"),
    path('superadminaddeventtype',superadminaddeventtype.as_view(),name="superadminaddeventtype"),
    path('admindeleteevent',admindeleteevent.as_view(),name="admindeleteevent"),
    path('admindeleteevents',admindeleteevents.as_view(),name="admindeleteevents"),
    path('editeventtype',editeventtype.as_view(),name="editeventtype"),
    path('superadminregister',superadminregister.as_view(),name="superadminregister"),
    path('superadmintransition',superadmintransition.as_view(),name="superadmintransition"),
    path('superadminlogin',superadminlogin.as_view(),name="superadminlogin"),
    path('superadminlogout',superadminlogout.as_view(),name="superadminlogin"),
    path('adminslider',adminslider.as_view(),name="adminslider"),

































    # new url
    path('superadmineditevent/<int:id>',superadmineditevent.as_view(),name="superadmineditevent"),
    path('eventview/<int:id>',eventview.as_view(),name="eventview"),
    path('events',events.as_view(),name="events"),
    path('contact',contact.as_view(),name="contact"),
    path('superadmincontact',superadmincontact.as_view(),name="superadmincontact"),
    path('superadmindelevent/<int:id>',superadmindelevent.as_view(),name="superadmindelevent"),
    path('superadminsetting',superadminsetting.as_view(),name="superadminsetting"),


    


















































































path('myevent',myevent.as_view(), name="myevent"),
path('login', login.as_view(),name="login"),
path('signup', signup.as_view(),name="signup"),
path('eventapp/<int:id>', eventapp.as_view(),name="eventapp"),
path('Progress', Progress.as_view(),name="Progress"),
path('uploadprogress', uploadprogress.as_view(),name="uploadprogress"),
path('logout', clientlogout.as_view(),name="clientlogout"),








path('clientlogin', clientlogin.as_view(),name="clientlogin"),
path('leaderboard', leaderboard.as_view(),name="leaderboard"),
path('leaderboarddata', leaderboarddata.as_view(),name="leaderboarddata"),
path('userprogress', userprogress.as_view(),name="userprogress"),
path('pagopar', pagopar.as_view(),name="pagopar"),
path('forgotpassword', forgotpassword.as_view(),name="forgotpassword"),
path('forget/<str:username>/<str:token>',forget.as_view(),name="forget"),



































































































































]
