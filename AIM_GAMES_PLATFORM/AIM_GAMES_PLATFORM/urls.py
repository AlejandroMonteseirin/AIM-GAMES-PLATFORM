"""AIM_GAMES_PLATFORM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from AIM_GAMES.views import *
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

#Aqui ponemos las rutas
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('paypal', include('paypal.standard.ipn.urls')),
    path('pagar_paypal', pagarPaypal, name='pagarPaypal' ),
    path('pagar_paypal_curriculum/', pagarPaypal_Curriculum, name='pagarPaypal_Curriculum' ),
    path('pagar_paypal_subscripcion/<int:subscriptionId>/<int:businessId>', pagar_paypal_subscripcion, name='pagar_paypal_subscripcion' ),
    path('subscription', subscriptionChoose, name='subscriptionChoose'),
    path('buyCoins/<int:quantity>', pagar_paypal_coins, name='buyCoins'),
    path('manage_subscription', manage_subscription, name='manage_subscription'),
    path('payment_done', payment_done, name='payment_done'),
    path('payment_canceled', payment_canceled, name='payment_canceled'),
    path('paypal_ipn/<int:businessId>', paypal_ipn,name='paypal_ipn'),
    path('paypal_subscription_ipn/<int:businessId>/<int:subscriptionId>', paypal_subscription_ipn,name='paypal_subscription_ipn'),
    path('paypal_curriculum_ipn/<int:curriculumId>', paypal_curriculum_ipn,name='paypal_curriculum_ipn'),
    path('paypal_coins_ipn/<int:business_id>/<int:quantity>', paypal_coins_ipn,name='paypal_coins_ipn'),
    path('login_redir',login_redir),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
    path("logout/", auth_views.LogoutView.as_view(),{'next_page': settings.LOGOUT_REDIRECT_URL}, name="logout"),
    path('freelancer/create/',FreelancerCreate.as_view(),name='signupFreelancer'),
    path('business/create/',BusinessCreate.as_view(),name='signupBusiness'),
    path('thread/create/',ThreadCreate.as_view(),name='threadCreate'),
    path('thread/detail/<int:thread_id>',threadDetail, name='threadDetail'),
    path('thread/business/list/', threadList, name='threadList'),
    path('joboffer/user/list/', jobOfferList, name='jobOfferList'),
    path('curriculum/business/list/', curriculumList, name='curriculumList'),
    #static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    path('freelancer/detail/<int:id>',freelancerDetail),
    path('freelancer/mycurriculum/<str:id>',freelancerDetail),
    path('setlanguage/<str:language>', setlanguage),
    path('response/create/<int:threadId>',response_create, name='responseCreate'),
    path('freelancer/link/create',linkCreate),
    path('freelancer/aptitude/create',aptitudeCreate),
    path('freelancer/graphicEngineExperience/create',graphicEngineExperienceCreate),
    path('freelancer/professionalExperience/create',professionalExperienceCreate),
    path('freelancer/formation/create',formationCreate),
    path('freelancer/html5showcase/edit/<int:id>',html5Edit),
    path('freelancer/link/edit/<int:id>',linkEdit),
    path('freelancer/graphicEngineExperience/edit/<int:id>',graphicEngineExperienceEdit),
    path('freelancer/aptitude/edit/<int:id>',aptitudeEdit),
    path('freelancer/professionalExperience/edit/<int:id>',professionalExperienceEdit),
    path('freelancer/formation/edit/<int:id>',formationEdit),
    path('business/joboffer/create',jobOfferCreate),
    path('business/joboffer/edit/<int:id>',jobOfferEdit),
    path('business/joboffer/delete/<int:id>',jobOfferDelete),
    path('business/thread/delete/<int:id>',threadDelete),
    path('business/thread/edit/<int:pk>',ThreadUpdate.as_view(),name='threadUpdate'),
    path('freelancer/html5showcase/delete/<int:id>',html5Delete),
    path('freelancer/link/delete/<int:id>',linkDelete),
    path('freelancer/graphicEngineExperience/delete/<int:id>',graphicEngineExperienceDelete),
    path('freelancer/aptitude/delete/<int:id>',aptitudeDelete),
    path('freelancer/professionalExperience/delete/<int:id>',professionalExperienceDelete),
    path('freelancer/formation/delete/<int:id>',formationDelete),
    path('jobOffer/detail/<int:id>',jobOfferDetail),
    path('challenge/list/', challengeList, name='challengeList'),
    path('challenge/business/list/', challengeBusinessList, name='challengeBusinessList'),
    path('business/challenge/create',challengeCreate),
    path('challenge/detail/<int:challenge_id>',challengeDetail),
    path('freelancer/curriculum/verify/<int:id>',curriculumVerify),
    path('freelancer/curriculum/unverify/<int:id>',curriculumUnverify),
    path('curriculum/manager/list/', curriculumListManager),
    path('500/', handler500, name='500'),
    path('404/', handler404, name='404'),
    path('terms-and-conditions', termsAndConditions),
    path('terminos-y-condiciones', terminosYCondiciones),
    path('privacy-policy', privacyPolicy),
    path('politica-privacidad', politicaPrivacidad),
    path('event/list/',eventList,name='eventList'),
    path('event/create/',eventCreate,name='eventCreate'),
    path('event/detail/<int:event_id>',eventDetail,name='eventDetail'),
    path('event/edit/<int:event_id>',eventEdit,name='eventEdit'),
    path('event/join/<int:event_id>',eventJoin,name='eventJoin'),
    path('event/disjoin/<int:event_id>',eventDisjoin,name='eventDisjoin'),
    path('event/delete/<int:event_id>',eventDelete,name='eventDelete'),
    path('userDownloadData',downloadData),
    path('deleteUser',deleteUser),
    path('message/list/',message_list),
    path('message/show/<int:id>',message_show),
    path('message/create/', message_create),
    path('message/reply/<int:msgid>', message_reply),
    path('chat/<int:userId>', chat,name='chatDisplay'),
    path('chat/update/<int:userId>', chatUpdate,name='chatUpdate'),
    path('chat/message/new', message_new,name='chatDisplay'),
    path('chat/user/<int:userId>', chatUser,name='chatUser'),
    path('chats', chats,name='chats'),
    path('search', global_search),
    path('broadcast/create', broadcastCreate,name='broadcast'),

]
