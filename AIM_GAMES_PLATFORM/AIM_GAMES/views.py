
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_list_or_404
from paypal.standard.forms import PayPalPaymentsForm,PayPalSharedSecretEncryptedPaymentsForm
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView, UpdateView
from .models import *
from .models import Freelancer, Business, Thread, Response, Link, JobOffer, Curriculum, Profile, Aptitude,\
    SubscriptionModel, SystemVariables
from .forms import *
from django.db.models import Q
from datetime import datetime, timezone
from django.contrib import auth
from django.contrib import sessions
from django.contrib.auth.models import Group
from django.http import Http404,HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.db.models import Avg, Count, Min, Sum, Value, CharField, Aggregate
import random
from urllib.parse import urlparse, quote
from itertools import chain
import pytz
from django.utils import timezone

from django.utils.translation import gettext as _
from django.utils import translation
from django.utils import timezone as timezoneDjango

def index(request):
    # esto es como el controlador/servicios
    try:
        request.session['currentUser'] = checkUser(request)
    except:
        request.session['currentUser'] ='none'

    return render(request, 'index.html')


def setlanguage(request, language):
    request.session['language'] = language
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def subscriptionChoose(request):
    user = request.user.id
    business = findByPrincipal(request)
    from_date = datetime.now() - timedelta(minutes=30)
    utc = pytz.UTC
    if business.lastPayment is not None and business.lastPayment.replace(tzinfo=utc) > from_date.replace(tzinfo=utc):
        trans = True
    else:
        trans = False
    subscriptionModels = SubscriptionModel.objects.all()
    return render(request, 'subscription/subscription.html', {'businessId': user, 'subscriptions': subscriptionModels,
                                                              'trans': trans})


def manage_subscription(request):

    if checkUser(request) != 'business':
        return handler500(request)
    business = findByPrincipal(request)
    if request.method == 'POST':
        form = BuyCoinsForm(request.POST, buss_id=business.id)
        if form.is_valid():
            return redirect('/buyCoins/' + str(form.cleaned_data['quantity']))
    else:
        form = BuyCoinsForm(buss_id=business.id)
    sysvar = SystemVariables.objects.first()
    return render(request, 'subscription/manage_subscription.html',
                  {'form': form, 'buss': business, 'directPurchaseCoinsPrice': sysvar.directPurchaseCoinsPrice})


def pagar_paypal_coins(request, quantity):
    host = request.get_host()
    sysvar = SystemVariables.objects.first()
    amount = quantity*sysvar.directPurchaseCoinsPrice
    business = findByPrincipal(request)
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': amount,
        'item_name': 'AIM-GAMES Coins',
        'currency_code': 'EUR',
        'notify_url': 'https://aim-games-4.herokuapp.com/paypal_coins_ipn/' + str(business.id) + '/' + str(quantity),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'pagarPaypal.html', {'form': form})


def pagarPaypal(request):
    host = request.get_host()
    businessId = request.session['buss']
    print(businessId)
    #local notify url
    #'notify_url': 'https://dbda170f.ngrok.io/paypal_ipn/'+str(businessId),
    
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '71',
        'item_name': 'Subscripcion AIM-GAMES',
        'currency_code': 'EUR',
        'notify_url': 'https://aim-games-4.herokuapp.com/paypal_ipn/'+str(businessId),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_canceled')),
        }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'pagarPaypal.html', {'form':form})


def pagar_paypal_subscripcion(request, subscriptionId, businessId):
    host = request.get_host()
    # https://overiq.com/django-paypal-subscriptions-with-django-paypal/
    print(businessId)
    # local notify url
    # 'notify_url': 'http://86e53f2e.ngrok.io/paypal_subscription_ipn/'+str(businessId),
    subs = SubscriptionModel.objects.filter(id=subscriptionId)[0]
    paypal_dict = {
        'cmd': '_xclick-subscriptions',
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'a3': str(subs.price),               # monthly price
        'p3': 1,                             # duration of each unit (depends on unit)
        't3': 'M',                           # duration unit ("M for Month")
        'src': '1',  # make payments recur
        'sra': '1',  # reattempt payment on payment error
        'item_name': str(subs.name_eng),
        'currency_code': 'EUR',
        # 'notify_url': 'https://aim-games-3.herokuapp.com/paypal_subscription_ipn/' + str(businessId),
        'notify_url': 'https://aim-games-4.herokuapp.com/paypal_subscription_ipn/' + str(businessId) + '/'
                      + str(subscriptionId),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    business = findByPrincipal(request)
    business.lastPayment = datetime.now()
    business.save()
    return render(request, 'pagarPaypal.html', {'form': form})

def pagarPaypal_Curriculum(request):
    host = request.get_host()
    freelancer = findByPrincipal(request)
    curriculum = freelancer.curriculum
    #local notify url
    #'notify_url': 'https://dbda170f.ngrok.io/paypal_ipn/'+str(businessId),
    
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '10',
        'item_name': 'Curriculum destacado en AIM-GAMES',
        'currency_code': 'EUR',
        'notify_url': 'https://aim-games-4.herokuapp.com/paypal_curriculum_ipn/'+str(curriculum.id),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_canceled')),
        }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'pagarPaypal.html', {'form':form})


@csrf_exempt
def paypal_ipn(request,businessId):
    print("ipn recieved")
    print(request.POST)
    updatedNumber = Business.objects.filter(id=businessId).update(lastPayment=datetime.now())
    print(updatedNumber)
    return JsonResponse({'ok': 'hoooh!'})

@csrf_exempt
def paypal_subscription_ipn(request, businessId, subscriptionId):
    print("ipn recieved")
    print(request.POST)
    print('Searching User '+str(businessId))
    prof = Profile.objects.filter(user__pk=businessId)
    business = Business.objects.filter(profile__pk=prof[0].id)[0]
    print('Found Business ' + str(business))
    print(str(request.POST.get('txn_type')))
    if request.POST.get('txn_type') == 'subscr_payment':
        print("Subcription Payment")
        if request.POST.get('payment_status') == 'Completed':
            print("Completed")
            subscription = get_object_or_404(SubscriptionModel, pk=subscriptionId)
            business.lastPayment = None
            print(business.lastPayment)
            if business.subscriptionModel is None or business.subscriptionModel.name != subscription.name:
                business.subscriptionModel = subscription
            business.coins = business.coins + subscription.coinsGain
            if business.coins > subscription.maxCoins:
                business.coins = subscription.maxCoins
            business.save()

    elif request.POST.get('txn_type') == 'subscr_cancel':
        print("Canceled")
        business.subscriptionModel = None
        business.lastPayment = None
        business.save()
    elif request.POST.get('txn_type') == 'subscr_signup':
        print("Confirmed")
    elif request.POST.get('subscr_failed ') == 'subscr_failed':
        print("Failed")

    return JsonResponse({'ok': 'hoooh!'})

@csrf_exempt
def paypal_coins_ipn(request, business_id, quantity):
    print("ipn recieved")
    print(request.POST)
    business = Business.objects.get(pk=business_id)
    if business.subscriptionModel is not None:
        if business.subscriptionModel.maxCoins > business.coins+quantity:
            business.coins += quantity
        else:
            business.coins = business.subscriptionModel.maxCoins
    else:
        sysvar = SystemVariables.objects.first()
        if sysvar.defaultMaxCoins > business.coins + quantity:
            business.coins += quantity
        else:
            business.coins = sysvar.defaultMaxCoins
    business.save()
    return JsonResponse({'ok': 'hoooh!'})

@csrf_exempt
def paypal_curriculum_ipn(request,curriculumId):
    print("ipn recieved")
    print(request.POST)
    updatedCurriculum = Curriculum.objects.filter(id=curriculumId).update(featured=True)
    print(updatedCurriculum)
    return JsonResponse({'ok': 'hoooh!'})


def payment_done(request):
    # esto es como el controlador/servicios
    return render(request, 'payment_done.html')


def payment_canceled(request):
    # esto es como el controlador/servicios
    return render(request, 'payment_canceled.html')


def login_redir(request):
    if request.user.is_superuser:
        res = redirect('admin/')
    else:
        res = redirect('index')

    try:
        request.session['currentUser'] = checkUser(request)
    except:
        request.session['currentUser'] ='none'

    return res


class FreelancerView(FormView):
    template_name = 'accounts/signup.html'
    form_class = FreelancerForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print('form_valid')
        return super().form_valid(form)


class BusinessView(FormView):
    template_name = 'accounts/signup.html'
    form_class = BusinessForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        return super().form_valid(form)


class FreelancerCreate(CreateView):
    form_class = FreelancerForm
    template_name = 'accounts/signup.html'
    success_url = '/accounts/login'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print('FreelancerCreate: form_valid')

        return super().form_valid(form)


class BusinessCreate(CreateView):
    form_class = BusinessForm
    template_name = 'accounts/signup.html'
    success_url = '/accounts/login'

    def __init__(self, *args, **kwargs):
        super(BusinessCreate, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print('BusinessCreate: form_valid')

        #
        buss = form.save()
        print(buss)

        self.request.session['buss'] = buss.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # This method is called before the view es generate and add the context
        # It should return the context

        context = super(BusinessCreate,self).get_context_data(**kwargs)
        context['type'] = 'business'
        return context


class ThreadUpdate(UpdateView):

    images = ""
    files = ""
    initial = {'images' : images, 'files' : files}
    model = Thread
    form_class = ThreadForm
    template_name = 'thread/form.html'
    success_url = '/accounts/login'

    def get_initial(self):
        initial = super(ThreadUpdate, self).get_initial()
        thread = self.get_object()
        for pic in thread.pics.all():
            initial['images'] += pic.uri+" "
        for attachedFile in thread.attachedFiles.all():
            initial['files'] += attachedFile.uri+" "

        return initial

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if checkUser(self.request) != 'business':
            return handler500(self.request)
        print('ThreadUpdate: form_valid')

        prof = Profile.objects.filter(user__pk=self.request.user.id)
        buss = Business.objects.filter(profile__pk=prof[0].id)
        thread = form.save(buss)
        self.request.session['alreadyResponse'] = True
        return threadDetail(self.request, thread.id)

    def get_context_data(self, **kwargs):
        # This method is called before the view es generate and add the context
        # It should return the context

        context = super(ThreadUpdate,self).get_context_data(**kwargs)
        context['edit'] = 'edit'
        return context

    def dispatch(self, request, *args, **kwargs):
        if checkUser(self.request) == 'business' and self.get_object().business.id == self.request.user.profile.business.id:
            return super(ThreadUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return handler500(request)


class ThreadCreate(CreateView):
    form_class = ThreadForm
    template_name = 'thread/form.html'
    success_url = '/accounts/login'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if checkUser(self.request) != 'business':
            return handler500(self.request)
        print('ThreadCreate: form_valid')

        prof = Profile.objects.filter(user__pk=self.request.user.id)
        buss = Business.objects.filter(profile__pk=prof[0].id)
        busi = buss[0]
        price = SystemVariables.objects.all()[0].threadPrice
        if busi.coins - price >= 0:
            thread = form.save(buss)
            busi.coins -= price
            busi.save()
            self.request.session['alreadyResponse'] = True
            return threadDetail(self.request, thread.id)
        else:
            return handler500(self.request)



    def get_context_data(self, **kwargs):
        # This method is called before the view es generate and add the context
        # It should return the context
        context = super(ThreadCreate, self).get_context_data(**kwargs)
        price = SystemVariables.objects.all()[0].threadPrice
        context['price'] = price
        context['buss'] = findByPrincipal(self.request)

        return context

    def dispatch(self, request, *args, **kwargs):
        if checkUser(self.request) == 'business':
            return super(ThreadCreate, self).dispatch(request, *args, **kwargs)
        else:
            return handler500(request)


def threadDetail(request, thread_id):
    if checkUser(request)!='business' and checkUser(request)!='manager':
        return handler500(request)
    thread = get_object_or_404(Thread, pk=thread_id)
    responses = thread.response_set.all()
    pics = thread.pics
    owner =False
    alreadyResponse = request.session.pop('alreadyResponse', None)
    if checkUser(request)=='business':
        business = findByPrincipal(request)
        if business.id == thread.business.id:
            owner = True
        if business.subscriptionModel == None:
            return handler500(request)
    return render(request, 'thread/threadDetail.html', {'thread': thread, 'responses': responses,'pics':pics,
                                                        'owner':owner, 'alreadyResponse':alreadyResponse})


def jobOfferDetail(request, id):
        jobOffer = get_object_or_404(JobOffer, pk=id)
        pics = jobOffer.images.split(",")
        for pic in pics:
            pic.strip()
        owner = False
        alreadyResponse = request.session.pop('alreadyResponse', None)
        if checkUser(request)=='business':
            business = findByPrincipal(request)
            if business.id == jobOffer.business.id:
                owner = True
            if business.subscriptionModel is None:
                return handler500(request)
        return render(request, 'jobOfferDetail.html', {'jobOffer': jobOffer, 'pics' : pics,'owner':owner, 'alreadyResponse': alreadyResponse})


def findByPrincipal(request):
    freelancer = None
    business = None
    if request.user.is_authenticated:
        user = request.user
        try:
            profile = user.profile
        except:
            print('admin logged')
        try:
            freelancer = Freelancer.objects.select_related('profile').get(id=profile.freelancer.id)
            return freelancer
        except:
            print('Principal is not a freelancer.')
        try:
            business = Business.objects.select_related('profile').get(id=profile.business.id)
            return business
        except:
            print('Principal is not a business.')
        try:
            manager = Manager.objects.select_related('profile').get(id=profile.manager.id)
            return manager
        except:
            print('Principal is not a manager.')
        
    return None

def freelancerDetail(request, id):
    userString = checkUser(request)
    if userString == 'none':
        return handler500(request)
    elif userString=='freelancer':
        if id == '-':
            freelancer = findByPrincipal(request)
        else:
            freelancer = get_object_or_404(Freelancer,pk=id)
            user = findByPrincipal(request)        
            if user.id != freelancer.id:
                return handler500(request)
    else:
        if id=='-':
            return handler500(request)
        else:
            freelancer = get_object_or_404(Freelancer,pk=id)
    
    curriculum = freelancer.curriculum
    links = curriculum.link_set.all()
    formation = curriculum.formation_set.all()
    professionalExperience = curriculum.professionalexperience_set.all()
    graphicEngineExperience = curriculum.graphicengineexperience_set.all()
    aptitude = curriculum.aptitude_set.all()
    try:
        HTML5Showcase = curriculum.HTML5Showcase
    except:
        HTML5Showcase = None

    if checkUser(request) == 'business' and findByPrincipal(request).subscriptionModel is None:
        return handler500(request)

    alreadyResponse = request.session.pop('alreadyResponse', None)
    return render(request, 'freelancer/detail.html', {'freelancer': freelancer,'links':links,'formations':formation,
                          'professionalExperiences':professionalExperience,'HTML5Showcase':HTML5Showcase,
                          'graphicEngineExperiences':graphicEngineExperience,'aptitudes':aptitude, 'alreadyResponse':alreadyResponse})

class GroupConcat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(expressions)s)'

    def __init__(self, expression, delimiter, **extra):
        output_field = extra.pop('output_field', CharField())
        delimiter = Value(delimiter)
        super(GroupConcat, self).__init__(
            expression, delimiter, output_field=output_field, **extra)

    def as_postgresql(self, compiler, connection):
        self.function = 'STRING_AGG'
        return super(GroupConcat, self).as_sql(compiler, connection)


def threadSearch(request):
    if checkUser(request)!='business' and checkUser(request)!='manager':
        return handler500(request)
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        strtags = search.replace('[^A-Za-z0-9 ]+', '').split(' ')
        q=Thread.objects.annotate(str_tags=GroupConcat('tags__title', ' ')).filter((Q(business__profile__name__icontains=search)|
            Q(title__icontains=search)|
            Q(description__icontains=search))|
            Q(str_tags__icontains=search))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for thread in list(q):
            print(thread.str_tags)
        
    else:
        q=Thread.objects.all()

    try:
        businessThread = get_object_or_404(Business,profile=request.user.profile)
    except:
        businessThread = None

    return q, businessThread

def threadList(request):
    threads, businessThread = threadSearch(request)
    alreadyResponse = request.session.pop('alreadyResponse', None)
    return render(request, 'thread/threadList.html',{'threads':threads,'businessThread':businessThread, 'alreadyResponse': alreadyResponse})

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def find_numbers_after_index(text, index):
    isnumber = True
    next_index = index + 1
    size = 0
    result = 0
    while isnumber:
        if is_number(text[next_index]):
            size = size + 1
            next_index = next_index + 1
            if next_index >= len(text):
                isnumber = False
        else:
            isnumber = False
    if size>0:
        result = int(text[index:index+size+1])

    return result
            
def jobOfferSearch(request):
    if checkUser(request)!='freelancer' and checkUser(request)!='business' and checkUser(request)!='manager':
        return handler500(request)
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        
        try:
            salary = 0
            minsal = "minsal:"
            if minsal in search:
                index = search.find(minsal) + len(minsal)
                salary = find_numbers_after_index(search,index)
            minsal = minsal + str(salary)
            search = search.replace(minsal, '')
            search = search.replace('  ', ' ')
            search = search.strip()
            q=JobOffer.objects.filter( (Q(business__profile__name__icontains=search)|
            Q(position__icontains=search)|
            Q(experienceRequired__icontains=search)|
            Q(ubication__icontains=search)|
            Q(description__icontains=search))&Q(salary__gte=salary))
            jobOffers= get_list_or_404(q)
        except:
            jobOffers=()
    else:
        q=JobOffer.objects.all()
    jobOffers= q
    if checkUser(request) == 'business' and get_object_or_404(Business,profile=request.user.profile).subscriptionModel is None:
        sub = False
    else:
        sub = True
    
    return q, sub
def jobOfferList(request):
    jobOffers, sub = jobOfferSearch(request)
    alreadyResponse = request.session.pop('alreadyResponse', None)
    return render(request, 'jobOfferList.html',{'jobOffers':jobOffers, 'sub': sub, 'alreadyResponse':alreadyResponse})

def curriculumSearch(request):
    if checkUser(request)!='business':
        return handler500(request)
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        lista= set()
        pe=ProfessionalExperience.objects.filter( Q(center__icontains=search)
        |Q(formation__icontains=search)).select_related('curriculum').order_by('-curriculum__featured')
        fo=Formation.objects.filter( Q(center__icontains=search)
        |Q(formation__icontains=search)).select_related('curriculum').order_by('-curriculum__featured')
        ap=Aptitude.objects.filter(aptitude__icontains=search).select_related('curriculum').order_by('-curriculum__featured')
        gee=GraphicEngineExperience.objects.filter(graphicEngine__title__icontains=search).select_related('curriculum').order_by('-curriculum__featured')
        
        
        for p in pe:
            lista.add(p.curriculum.id)
        for f in fo:
            lista.add(f.curriculum.id)
        for a in ap:
            lista.add(a.curriculum.id)
        for g in gee:
            lista.add(g.curriculum.id)

        q=Curriculum.objects.filter(id__in=lista).order_by('-featured')
    else:
        q=Curriculum.objects.all()
        q = q.order_by('-featured')
    curriculums= q
    aptitudes={}
    for c in curriculums:
        aptitudesList=Aptitude.objects.filter(curriculum=c.id)
        aptitudes[c.id]=list(aptitudesList)
    try:
        if get_object_or_404(Business,profile=request.user.profile).subscriptionModel is None:
            sub = False
        else:
            sub = True
    except AttributeError:
        return handler500(request)

    return curriculums, aptitudes, sub

def curriculumList(request):
    curriculums, aptitudes, sub = curriculumSearch(request)
    alreadyResponse = request.session.pop('alreadyResponse', None)
    return render(request, 'curriculumList.html',{'curriculums':curriculums,'aptitudes':aptitudes, 'sub': sub, 'alreadyResponse':alreadyResponse})

def checkUser(request):
    freelancer = None
    business = None
    manager = None
    if request.user.is_authenticated:
        user = request.user
        try:
            profile = user.profile
        except:
            return 'admin'
        try:
            freelancer = Freelancer.objects.select_related('profile').get(id=profile.freelancer.id)
        except:
            print('Principal is not a freelancer.')
        try:
            business = Business.objects.select_related('profile').get(id=profile.business.id)
        except:
            print('Principal is not a business.')
        try:
            manager = Manager.objects.select_related('profile').get(id=profile.manager.id)
        except:
            print('Principal is not a manager.')
    if freelancer!=None:
        return 'freelancer'
    elif business !=None:
        return 'business'
    elif manager !=None:
        return 'manager'
    else:
        return 'none'

def _get_queryset(klass):
    """
    Return a QuerySet or a Manager.
    Duck typing in action: any class with a `get()` method (for
    get_object_or_404) or a `filter()` method (for get_list_or_404) might do
    the job.
    """
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass

def response_create(request, threadId):
    if checkUser(request) == 'business':
        if request.method=="POST":
            form = ResponseForm(request.POST)
            if form.is_valid():
                response = form.save(commit=False)
                userprofile = Profile.objects.get(user=request.user)
                businessPrincipal = Business.objects.get(profile=userprofile)
                response.business=businessPrincipal
                thread = Thread.objects.get(id=threadId)
                response.thread = thread
                response.save()
                request.session['alreadyResponse'] = True
                return redirect('/thread/detail/' + str(threadId))
        else:
            form = ResponseForm()
        return render(request,'thread/responseCreate.html',{'form':form})
    else:
        return handler500(request)

def linkCreate(request):
    if checkUser(request)=='freelancer':
        freelancer = findByPrincipal(request)
        if request.method == 'POST':
            form = LinkForm(request.POST)
            if form.is_valid():                
                link = form.save(commit=False)
                link.curriculum = freelancer.curriculum
                link.save()
                print('link saved')
                request.session['alreadyResponse'] = True
                return redirect('/freelancer/detail/'+str(freelancer.id))
            else:
                return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add link')})
        else:
            form = LinkForm()
            return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add link')})
    else:
        return handler500(request)

def aptitudeCreate(request):
    if checkUser(request)=='freelancer':
        freelancer = findByPrincipal(request)
        if request.method == 'POST':
            form = AptitudeForm(request.POST)
            if form.is_valid():                
                obj = form.save(commit=False)
                obj.curriculum = freelancer.curriculum
                obj.save()
                print('Aptitude saved')
                request.session['alreadyResponse'] = True
                return redirect('/freelancer/detail/'+str(freelancer.id))
            else:
                return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add aptitude')})
        else:
            form = AptitudeForm()
            return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add aptitude')})
    else:
        return handler500(request)

def graphicEngineExperienceCreate(request):
    if checkUser(request)=='freelancer':
        freelancer = findByPrincipal(request)
        if request.method == 'POST':
            form = GraphicEngineExperienceForm(request.POST)
            if form.is_valid():                
                obj = form.save(commit=False)
                obj.curriculum = freelancer.curriculum
                obj.save()
                print('Graphic engine experience saved')
                request.session['alreadyResponse'] = True
                return redirect('/freelancer/detail/'+str(freelancer.id))
            else:
                return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add graphic engine experience')})
        else:
            form = GraphicEngineExperienceForm()
            return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add graphic engine experience')})
    else:
        return handler500(request)

def professionalExperienceCreate(request):
    if checkUser(request)=='freelancer':
        freelancer = findByPrincipal(request)
        if request.method == 'POST':
            form = ProfessionalExperienceForm(request.POST)
            if form.is_valid():                
                obj = form.save(commit=False)
                obj.curriculum = freelancer.curriculum
                obj.save()
                print('Professional Experience saved')
                request.session['alreadyResponse'] = True
                return redirect('/freelancer/detail/'+str(freelancer.id))
            else:
                return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add professional experience')})
        else:
            form = ProfessionalExperienceForm()
            return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add professional experience')})
    else:
        return handler500(request)

def formationCreate(request):
    if checkUser(request)=='freelancer':
        freelancer = findByPrincipal(request)
        if request.method == 'POST':
            form = FormationForm(request.POST)
            if form.is_valid():                
                obj = form.save(commit=False)
                obj.curriculum = freelancer.curriculum
                obj.save()
                print('formation saved')
                request.session['alreadyResponse'] = True
                return redirect('/freelancer/detail/'+str(freelancer.id))
            else:
                return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add formation')})
        else:
            form = FormationForm()
            return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add formation')})
    else:
        return handler500(request)

def jobOfferCreate(request):
    if checkUser(request)=='business':
        business = findByPrincipal(request)
        price = SystemVariables.objects.all()[0].jobOfferPrice
        if request.method == 'POST':
            form = JobOfferForm(request.POST)
            if form.is_valid():
                if business.coins - price >= 0:
                    obj = form.save(commit=False)
                    obj.business = business
                    obj.save()
                    print('job offer saved')
                    business.coins = business.coins - price
                    business.save()
                    request.session['alreadyResponse'] = True
                return redirect('/joboffer/user/list/')
            else:
                return render(request,'business/standardForm.html',{'form':form,'title':_('Add Job Offer')})
        else:
            form = JobOfferForm()
            return render(request,'business/standardForm.html',{'form':form,'title':_('Add Job Offer'), 'buss': business, 'price': price})
    else:
        return handler500(request)

def jobOfferEdit(request,id):
    if checkUser(request)=='business':
        business = findByPrincipal(request)
        instance = get_object_or_404(JobOffer, id=id)
        if instance.business.id != business.id:
            return handler500(request)
        form = JobOfferForm(request.POST or None, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.business = business
            obj.save()
            request.session['alreadyResponse'] = True
            return redirect('/jobOffer/detail/'+ str(id))
        else:
            return render(request,'business/standardForm.html',{'form':form,'title':_('Edit Job Offer'), 'edit':'edit'})
    else:
        return handler500(request)

def jobOfferDelete(request,id):
    if checkUser(request)=='business':
        business = findByPrincipal(request)
        instance = get_object_or_404(JobOffer, id=id)
        if instance.business.id != business.id:
            return handler500(request)
        instance.delete()
        request.session['alreadyResponse'] = True
        return redirect('/joboffer/user/list/')
    else:
        return handler500(request)

def html5Edit(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

    instance = get_object_or_404(HTML5Showcase, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = html5showcaseForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        request.session['alreadyResponse'] = True
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Edit HTML5Showcase')})

def formationEdit(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

    instance = get_object_or_404(Formation, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = FormationForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        request.session['alreadyResponse'] = True
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Edit Formation')})

def professionalExperienceEdit(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

    instance = get_object_or_404(ProfessionalExperience, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = ProfessionalExperienceForm(request.POST or None, instance=instance,initial={'startDate': instance.startDate.strftime("%Y-%m-%d"),'endDate': instance.endDate.strftime("%Y-%m-%d")})
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        request.session['alreadyResponse'] = True
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Edit ProfessionalExperience')})

def aptitudeEdit(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

    instance = get_object_or_404(Aptitude, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = AptitudeForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        request.session['alreadyResponse'] = True
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Edit Aptitude')})

def graphicEngineExperienceEdit(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

    instance = get_object_or_404(GraphicEngineExperience, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = GraphicEngineExperienceForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        request.session['alreadyResponse'] = True
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Edit Graphic Engine Experience')})

def linkEdit(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

    instance = get_object_or_404(Link, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = LinkForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        request.session['alreadyResponse'] = True
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Edit Link')})

def html5Delete(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

    instance = get_object_or_404(HTML5Showcase, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.embedCode=""
    instance.save()
    request.session['alreadyResponse'] = True
    return redirect('/freelancer/detail/'+str(freelancer.id))

def formationDelete(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)
    instance = get_object_or_404(Formation, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    request.session['alreadyResponse'] = True
    return redirect('/freelancer/detail/'+str(freelancer.id))

def professionalExperienceDelete(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)
    instance = get_object_or_404(ProfessionalExperience, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    request.session['alreadyResponse'] = True
    return redirect('/freelancer/detail/'+str(freelancer.id))

def aptitudeDelete(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)
    instance = get_object_or_404(Aptitude, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    request.session['alreadyResponse'] = True
    return redirect('/freelancer/detail/'+str(freelancer.id))

def graphicEngineExperienceDelete(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)
    instance = get_object_or_404(GraphicEngineExperience, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    request.session['alreadyResponse'] = True
    return redirect('/freelancer/detail/'+str(freelancer.id))

def linkDelete(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)
    instance = get_object_or_404(Link, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    request.session['alreadyResponse'] = True
    return redirect('/freelancer/detail/'+str(freelancer.id))


def challengeSearch(request):
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        try:
            q=Challenge.objects.filter(Q(business__profile__name__icontains=search)|Q(title__icontains=search))
            challenges = get_list_or_404(q)
        except:
            challenges=()
    else:
        q=Challenge.objects.all()
    challenges= q
    if checkUser(request) == 'business' and get_object_or_404(Business,profile=request.user.profile).subscriptionModel is None:
        sub = False
    else:
        sub = True

    return challenges, sub
def challengeList(request):
    challenges, sub = challengeSearch(request)
    alreadyResponse = request.session.pop('alreadyResponse', None)
    return render(request, 'challenge/challengeList.html',{'challenges':challenges, 'sub': sub, 'alreadyResponse':alreadyResponse})

def challengeCreate(request):
    if checkUser(request)=='business':
        business = findByPrincipal(request)
        price = SystemVariables.objects.all()[0].challengePrice
        if request.method == 'POST':
            form = ChallengeForm(request.POST)
            if form.is_valid():
                if business.coins - price >= 0:
                    obj = form.save(commit=False)
                    obj.business = business
                    obj.save()
                    print('Challenge saved')
                    business.coins = business.coins - price
                    business.save()
                    request.session['alreadyResponse'] = True
                return redirect('/challenge/list/')
            else:
                return render(request,'business/standardForm.html',{'form':form,'title':_('Add Challenge')})
        else:
            form = ChallengeForm()
            return render(request,'business/standardForm.html',{'form':form,'title':_('Add Challenge'), 'buss': business, 'price': price})
    else:
        return render(request, 'index.html')

def challengeDetail(request, challenge_id):
    lookResponses = False
    form = None
    saved = False
    alreadyResponse = False
    challenge = get_object_or_404(Challenge, pk=challenge_id)
    responsesChallenge = challenge.challengeresponse_set.all()
    opened = False
    if checkUser(request) == 'freelancer':
        if request.method == "POST":
            form = ChallengeResponseForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                challenge = Challenge.objects.get(id=challenge_id)
                obj.freelancer = findByPrincipal(request)
                obj.challenge = challenge
                obj.save()
                saved = True
                alreadyResponse = True
            else:
                opened=True
        else:
            for r in responsesChallenge:
                if r.freelancer == findByPrincipal(request):
                    alreadyResponse = True

            form = ChallengeResponseForm()
    else:
        if challenge.business == findByPrincipal(request):
            lookResponses = True
        if findByPrincipal(request) is not None:
            if findByPrincipal(request).subscriptionModel is None:
                return handler500(request)
    return render(request, 'challenge/challengeDetail.html', {'form': form, 'saved':saved, 'challenge': challenge,
                                                'responsesChallenge': responsesChallenge, 'lookResponses':lookResponses,
                                                'alreadyResponse': alreadyResponse, 'saved':saved, 'opened':opened})

def curriculumVerify(request, id):
    userString = checkUser(request)
    if userString!='manager':
        return handler500(request)
    curriculum = get_object_or_404(Curriculum, pk=id)
    curriculum.verified = True
    curriculum.save()
    request.session['alreadyResponse'] = True
    return redirect('/freelancer/detail/' + str(curriculum.freelancer.id))

def curriculumUnverify(request, id):
    userString = checkUser(request)
    if userString!='manager':
        return handler500(request)
    curriculum = get_object_or_404(Curriculum, pk=id)
    curriculum.verified = False
    curriculum.save()
    request.session['alreadyResponse'] = True
    return redirect('/freelancer/detail/' + str(curriculum.freelancer.id))


def curriculumListManager(request):
    if checkUser(request)!='manager':
        return handler500(request)
    curriculums = Curriculum.objects.all()
    aptitudes={}
    for c in curriculums:
        aptitudesList=Aptitude.objects.filter(curriculum=c.id)
        aptitudes[c.id]=list(aptitudesList)
    return render(request, 'curriculumList.html',{'curriculums':curriculums,'aptitudes':aptitudes})


def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def termsAndConditions(request):
    return render(request, "terms-and-conditions.html")

def privacyPolicy(request):
    return render(request, "privacy-policy.html")    

def terminosYCondiciones(request):
    return render(request, "terminos-y-condiciones.html")

def politicaPrivacidad(request):
    return render(request, "politica-privacidad.html")   

def eventSearch(request):
    if not request.user.is_authenticated:
        return handler500(request)
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        q=Event.objects.annotate(str_tags=GroupConcat('tags__title', ' ')).filter( Q(location__icontains=search)|
            Q(title__icontains=search)|
            Q(tags__title__icontains=search))
    else:
        q=Event.objects.all()
    events= q
    if checkUser(request) == 'business' and get_object_or_404(Business,profile=request.user.profile).subscriptionModel is None:
        sub = False
    else:
        sub = True

    return events, sub

def eventList(request):
    events, sub = eventSearch(request)
    alreadyResponse = request.session.pop('alreadyResponse', None)
    return render(request, 'event/eventList.html', {'events':events, 'sub': sub, 'alreadyResponse': alreadyResponse})

def eventCreate(request):
    if checkUser(request)=='manager':
        manager = findByPrincipal(request)
        if request.method == 'POST':
            form = EventForm(request.POST)
            
            if form.is_valid(): 
                tags = form.cleaned_data['tags']            
                obj = form.save(commit=False)
                obj.manager = manager
                obj.save()
                for tag in tags:
                    obj.tags.add(tag)
                print('Event saved')
                request.session["alreadyResponse"] = True
                return redirect('/event/list/')
            else:
                return render(request,'event/standardForm.html',{'form':form})
        else:
            form = EventForm()
            return render(request,'event/standardForm.html',{'form':form})
    else:
        return handler500(request)

def eventDetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    freelancers= event.freelancers.all()
    companies= event.companies.all()
    manager = findByPrincipal(request)
    alreadyResponse = False
    if checkUser(request)!='manager':
        user = findByPrincipal(request)
        if(user in freelancers or user in companies):
            joining=True
        else:
            joining=False
    else:
        joining=False
    if checkUser(request) == 'business' and findByPrincipal(request).subscriptionModel is None:
        return handler500(request)

    alreadyResponse = request.session.pop('alreadyResponse',None)
    return render(request, 'event/eventDetail.html', {'event': event,'freelancers':freelancers,'companies':companies, 'joining':joining, 'alreadyResponse': alreadyResponse})

def eventEdit(request, event_id): 
    if checkUser(request)!='manager':
        return handler500(request)

    instance = get_object_or_404(Event, id=event_id)
    manager = findByPrincipal(request)
    form = EventForm(request.POST or None, instance=instance)
    if form.is_valid():
        tags = form.cleaned_data['tags']
        obj = form.save(commit=False)
        obj.manager = manager
        obj.save()
        obj.tags.set(())
        for tag in tags:
            obj.tags.add(tag)
        request.session["alreadyResponse"] = True
        return redirect('/event/detail/'+str(event_id))
    return render(request,'event/standardForm.html',{'form':form})

def eventJoin(request, event_id): 
    userRole=checkUser(request)
    manager = random.choice(Manager.objects.all())
    manager = manager.profile.user
    recipientUser = request.user.profile.user
    if userRole!='business' and userRole!='freelancer':
        return handler500(request)
    instance = get_object_or_404(Event, id=event_id)
    user = findByPrincipal(request)

    form = EventForm(instance=instance)
    obj = form.save(commit=False)
    if obj.messageOnJoin is not None:
        message = Message(
            sender=manager,
            recipient=recipientUser,
            subject="dummy",
            text=obj.messageOnJoin,
        )
        message.save()
    if userRole=='freelancer':
        obj.freelancers.add(user)
    else:
        obj.companies.add(user)
    obj.save()
    request.session['alreadyResponse'] = True
    return redirect('/event/detail/'+str(event_id))

def eventDisjoin(request, event_id): 
    userRole=checkUser(request)
    if userRole!='business' and userRole!='freelancer':
        return handler500(request)
    instance = get_object_or_404(Event, id=event_id)
    user = findByPrincipal(request)

    form = EventForm(instance=instance)
    obj = form.save(commit=False)
    if userRole=='freelancer':
        obj.freelancers.remove(user)
    else:
        obj.companies.remove(user)
    obj.save()
    request.session['alreadyResponse'] = True
    return redirect('/event/detail/'+str(event_id))

def eventDelete(request, event_id):
    if checkUser(request)!='manager':
        return handler500(request) 
    instance = get_object_or_404(Event, id=event_id)
    manager = findByPrincipal(request)
    instance.delete()
    request.session['alreadyResponse'] = True
    return redirect('/event/list/')

def downloadData(request):
    print("entre!")
    datos=findByPrincipal(request).getData()
    print(datos)

    filename = "AIM-GAMES-PLATFORM_yourdata.txt"
    content = str(datos)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def deleteUser(request):
    user=request.user
    user.delete()
    auth.logout(request)
    return redirect('/')    


def message_list(request):
    if not request.user.is_authenticated:
        return handler500(request)
    user = request.user
    messages = Message.objects.filter(recipient=user).order_by('readed', '-timestamp')
    if checkUser(request) == 'business' and get_object_or_404(Business,profile=request.user.profile).subscriptionModel is None:
        sub = False
    else:
        sub = True
    return render(request, 'message/list.html', {'messages': messages, 'sub': sub})

def message_show(request, id):
    message = get_object_or_404(Message, id=id)
    user = request.user 
    if not (user == message.sender or user == message.recipient):
        return handler500(request)
    if message.readed is False:
        count = int(request.session["message_count"])
        if count>0:
            count = count - 1
            request.session["message_count"] = count
        message.readed = True
        message.save()
    if checkUser(request) == 'business' and get_object_or_404(Business,profile=request.user.profile).subscriptionModel is None:
        sub = False
    else:
        sub = True
    return render(request, 'message/show.html', {'message': message, 'sub': sub})

def message_create(request):
    if checkUser(request) == 'business' and findByPrincipal(request).subscriptionModel is None:
        return handler500(request)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.sender = request.user
            obj.save()
            print('Message saved')
            return redirect('/message/list/')
        else:
            return render(request,'message/create.html',{'form':form,'title':_('Create Message')})
    else:
        form = MessageForm()
        return render(request,'message/create.html',{'form':form,'title':_('Create Message')})

def message_reply(request, msgid):
    if checkUser(request) == 'business' and findByPrincipal(request).subscriptionModel is None:
        return handler500(request)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            message = get_object_or_404(Message, id=msgid)
            obj = form.save(commit=False)
            obj.sender = request.user
            recipient = message.sender
            subject = message.subject
            obj.recipient = recipient
            obj.subject = "RE: " + subject
            obj.save()
            print('Message saved')
            return redirect('/message/list/')
        else:
            return render(request,'message/create.html',{'form':form,'title':'Response Message'})
    else:
        form = ReplyForm()
        return render(request,'message/create.html',{'form':form,'title':'Response Message'})

def threadDelete(request, id): 
    if checkUser(request)!='business':
        return handler500(request)
    instance = get_object_or_404(Thread, id=id)
    business = findByPrincipal(request)
    if instance.business.id != business.id:
        return redirect('/thread/business/list/')
    instance.delete()
    request.session['alreadyResponse'] = True
    return redirect('/thread/business/list/')

def chat(request,userId):
    if not request.user.is_authenticated:
        return handler500(request)
    user2 = get_object_or_404(User, pk=userId)
    user1 = request.user
    messages = list(Message.objects.filter(
        Q(sender=user1,recipient=user2) | Q(sender=user2,recipient=user1),
        ).order_by('-timestamp'))
    messages.reverse()
    updatedNumber = Message.objects.filter(
        Q(sender=user2,recipient=user1,readed=False),
        ).update(readed=True)
    return render(request, 'message/chat.html',{'messages': messages, 'user2':user2,'user1':user1})

def chatUpdate(request,userId):
    if not request.user.is_authenticated:
        return handler500(request)
    user2 = get_object_or_404(User, pk=userId)
    user1 = request.user
    messagesQueryset = Message.objects.filter(
        Q(sender=user2,recipient=user1,readed=False),
        ).order_by('timestamp')
    results = [ob.as_json(user1.username) for ob in messagesQueryset]
    hola =  messagesQueryset.update(readed=True)
    return JsonResponse({'new_messages': results})

@csrf_exempt
def message_new(request):
    if request.method=="POST":
        user1 = request.user
        text = request.POST.get("text", "")
        userId = int(request.POST.get("recipientId", ""))
        recipientUser = User.objects.get(pk=userId)
        print('esto esta hechisimo')
        message = Message(
            sender = user1,
            recipient = recipientUser,
            subject = "dummy",
            text = text,
        )
        message.save()
    return JsonResponse({})

def chatUser(request,userId):
    #userId = User.objects.get(pk=userId)
    userId = get_object_or_404(User, pk=userId)
    return render(request, 'message/chatUser.html',{'user2':userId})

def chats(request):
    if not request.user.is_authenticated:
        return handler500(request)
    aux = list(User.objects.exclude(Q(id=request.user.id)|Q(username='root')))
    users = [[] for x in range(len(aux))]
    for i in range(0,len(aux)):
        messagesQueryset = Message.objects.filter(
        Q(sender=aux[i],recipient=request.user,readed=False),
        ).order_by('-timestamp')
        users[i].append(aux[i])
        messages = list(messagesQueryset)
        users[i].append(len(messages))
        if len(messages) > 0:
            users[i].append(messages[0])
    return render(request, 'message/chats.html',{'users':users})

def global_search(request):
    values = {}
    try:
        usertype = checkUser(request)
        if usertype=='freelancer' or usertype=='business' or usertype=='manager':
            jobOffers, joboffer_sub = jobOfferSearch(request)
            values = {**values, **{'jobOffers': jobOffers, 'joboffer_sub': joboffer_sub}}
        if usertype=='business':
            curriculums, aptitudes, curriculum_sub = curriculumSearch(request)
            values = {**values, **{'curriculums': curriculums,'aptitudes': aptitudes, 'curriculum_sub': curriculum_sub}}
        if usertype=='business' or usertype=='manager':
            threads, businessThread = threadSearch(request)
            values = {**values, **{'threads': threads, 'businessThread':businessThread}}
        if request.user.is_authenticated:
            events, sub_events = eventSearch(request)
            values = {**values, **{'events': events, 'sub_events':sub_events}}
        challenges, sub_challenges = challengeSearch(request)
        values = {**values, **{'challenges': challenges, 'sub_challenges':sub_challenges}}
    except:
        result = values
    result = render(request, 'search.html', values) 
    return result

def broadcastCreate(request):
    if not request.user.is_authenticated:
        return handler500(request)
    if checkUser(request)=='manager':
        user = request.user
        if request.method == 'POST':
            form = BroadcastForm(request.POST)
            if form.is_valid():                
                message = form.save(commit=False)
                text = message.text
                users = User.objects.exclude(pk=user.id)
                for u in users:
                    newMessage = Message(sender = user,recipient = u,subject = "dummy",text = text)
                    newMessage.save()
                print('broadcast done')
                return redirect('/chats')
            else:
                return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add broadcast')})
        else:
            form = BroadcastForm()
            return render(request,'freelancer/standardForm.html',{'form':form,'title':_('Add broadcast')})
    else:
        return handler500(request)

    #return render(request, 'search.html', {'jobOffers': jobOffers, 'joboffer_sub': joboffer_sub, 'curriculums': curriculums,
    # 'aptitudes': aptitudes, 'curriculum_sub': curriculum_sub, 'threads': threads, 'businessThread':businessThread})
