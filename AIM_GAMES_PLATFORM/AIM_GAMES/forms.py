from django.forms import ModelForm, forms, CharField,URLField, URLInput,Textarea,DateTimeField, ModelMultipleChoiceField,EmailInput, NumberInput, TextInput, MultipleChoiceField,EmailField, ModelMultipleChoiceField,CheckboxSelectMultiple, DateField, DateInput,SelectDateWidget,ChoiceField,RadioSelect,BooleanField, IntegerField
from django.contrib.auth.forms import UserCreationForm
from AIM_GAMES.models import *
from django.contrib.auth.models import User, Group
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime,timedelta
import re


class BusinessForm(ModelForm):
    terms = BooleanField(required = True,label = 'terms')
    imAdult = BooleanField(required = True,label = 'imAdult')

    class Meta:
        model = Business
        exclude = ('lastPayment', 'subscriptionModel', 'coins')

    def __init__(self, *args, **kwargs):
        super(BusinessForm, self).__init__(*args, **kwargs)
        self.fields['profile'].required = False
        data = kwargs.get('data')
        # 'prefix' parameter required if in a modelFormset
        self.instance.profile = Profile()
        self.profile_form = ProfileForm(instance=self.instance and self.instance.profile, prefix=self.prefix, data=data)

    def clean(self):
        if not self.profile_form.is_valid():
            raise forms.ValidationError(_("Profile not valid"))

    def save(self, commit=False):
        print('save: BusinessForm')
        obj = super(BusinessForm, self).save(commit=commit)
        obj.profile = self.profile_form.save()
        group = Group.objects.get(name='Business')
        obj.profile.user.groups.add(group)
        #obj.profile.dateOfBirth = datetime.date(year=today.year, month=today.month, day=today.day)  
        obj.save()
        return obj


class FreelancerForm(ModelForm):
    profession = CharField(widget=TextInput(), label=_("profession"))
    terms = BooleanField(required = True,label = 'terms')
    imAdult = BooleanField(required = True,label = 'imAdult')
    class Meta:
        model = Freelancer
        exclude = ()

    def __init__(self, *args, **kwargs):
        print('__init__ FreelancerForm')
        super(FreelancerForm, self).__init__(*args, **kwargs)
        self.fields['profile'].required = False
        data = kwargs.get('data')
        # 'prefix' parameter required if in a modelFormset
        self.instance.profile = Profile()
        self.profile_form = ProfileForm(instance=self.instance and self.instance.profile, prefix=self.prefix, data=data)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'validate'

    def clean(self):
        print('clean: FreelancerForm')
        if not self.profile_form.is_valid():
            raise forms.ValidationError(_("Profile not valid"))

    def save(self, commit=False):
        print('save: FreelancerForm')
        obj = super(FreelancerForm, self).save(commit=commit)
        obj.profile = self.profile_form.save()
        group = Group.objects.get(name='Freelancer')
        obj.profile.user.groups.add(group)      
        obj.save()
        cur,cre = Curriculum.objects.get_or_create(freelancer= obj,verified=False)
        HTML5Showcase.objects.get_or_create(curriculum= cur,embedCode="")
        return obj


class ProfileForm(ModelForm):
    name = CharField(widget=TextInput(), label=_("Name"))
    surname = CharField(widget=TextInput(), label=_("Surname"))
    email = EmailField(widget=EmailInput(), label=_("Email"))
    city = CharField(widget=TextInput(), label=_("City"))
    postalCode = CharField(widget=NumberInput(), label=_("Postal Code"))
    idCardNumber = CharField(widget=TextInput(), label=_("IDCard Number"))
    phoneNumber = CharField(widget=NumberInput(), label=_("Phone Number"))
    photo = URLField(widget=URLInput(), label=_("Photo URL:"), required=False)

    class Meta:
        model = Profile
        exclude = ('dateOfBirth',)

    def __init__(self, *args, **kwargs):
        print('__init__ ProfileForm')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        data = kwargs.get('data')
        # 'prefix' parameter required if in a modelFormset
        self.instance.user = User()
        self.user_form = UserForm(instance=self.instance and self.instance.user, prefix=self.prefix, data=data)

    def clean_phoneNumber(self):
        print('clean: ProfileForm: PhoneNumber')
        data = self.cleaned_data['phoneNumber']
        if not data.isdigit() or len(data) != 9:
            raise ValidationError(_("Phone Number must be a number"))
        return data

    def clean_postalCode(self):
        data = self.cleaned_data['postalCode']
        if not data.isdigit() or not data.__len__() == 5:
            raise ValidationError(_("validatePostal"))
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if Profile.objects.filter(email=data):
            raise ValidationError(_("emailUnique"))
        return data

    def clean_idCardNumber(self):
        data = self.cleaned_data['idCardNumber']
        word = 'TRWAGMYFPDXBNJZSQVHLCKE'
        numbers = "1234567890"
        validate = False
        if (len(data) == 9):
            chara = data[8].upper()
            dni = data[:8]
            if (len(dni) == len([n for n in dni if n in numbers])):
                if word[int(dni) % 23] == chara:
                    validate = True
        if not validate:
            raise ValidationError(_("ID Card Number not valid"))
        return data

    """ def clean_dateOfBirth(self):
        #print('clean: ProfileForm: dateOfBityh')
        #data = self.cleaned_data['dateOfBirth']
        #from_date = datetime.now() - timedelta(days=18*365)
        #print(str(from_date))
        #print(str(data))
        #if data > datetime.date(from_date):
        #    raise ValidationError(_("You must be over 18 to sign up"))

        data = datetime.date(year=today.year, month=today.month, day=today.day)
        return data """

    def clean(self):
        print('clean: ProfileForm')
        if not self.user_form.is_valid():
            raise forms.ValidationError(_("User not valid"))

    def save(self, commit=False):
        print('save: ProfileForm')
        obj = super(ProfileForm, self).save(commit=commit)
        obj.user = self.user_form.save()
        #datetime.date(year=today.year, month=today.month, day=today.day)
        obj.dateOfBirth = datetime.now()
        obj.save()
        return obj


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']


class ThreadForm(ModelForm):
    title = CharField(widget=TextInput(), label=_('Title'))
    description = CharField(widget=Textarea(), label=_('Description'),)
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), label=_('Tags'), required=False,)
    images = CharField(widget=Textarea(), required=False, label=_('Image URLs'),)
    files = CharField(widget=Textarea(), required=False, label=_('Attachment URLs'),)

    class Meta:
        model = Thread
        exclude = ('business', 'pics', 'attachedFiles')

    def clean_images(self):
        """Split the tags string on whitespace and return a list"""
        print('clean: ThreadForm: Images')
        return self.cleaned_data['images'].strip().split()

    def clean_files(self):
        """Split the tags string on whitespace and return a list"""
        print('clean: ThreadForm: Files')
        return self.cleaned_data['files'].strip().split()

    def __init__(self, *args, **kwargs):
        print('__init__ ThreadForm')
        super(ThreadForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'validate'

    def clean(self):
        print('clean: ThreadForm')
        val = URLValidator()
        urls = self.cleaned_data['images']
        try:
            for url in urls:
                val(url)

            urls = self.cleaned_data['files']
            for url in urls:
                val(url)
        except ValidationError:
            raise ValidationError(_("Please, enter valid URLS separated by comas in the images and files field"))
        return self.cleaned_data

    def save(self,business):
        print('save: ProfileForm')
        obj = super(ThreadForm, self).save(commit=False)
        pics = []
        attached_files = []
        for image in self.cleaned_data['images']:
            url = URL.objects.filter(uri=image)
            if not url:
                url = URL()
                url.uri = image
                url.save()
            else:
                url = url[0]
            pics.append(url)
        for file in self.cleaned_data['files']:
            url = URL.objects.filter(uri=file)
            if not url:
                url = URL()
                url.uri = file
                url.save()
            else:
                url = url[0]
            attached_files.append(url)

        obj.business = business[0]
        obj.save()
        self.save_m2m()
        obj.attachedFiles.set(attached_files)
        obj.pics.set(pics)
        return obj


class ResponseForm(ModelForm):

    class Meta:
        model = Response
        exclude = ('business','thread')


class LinkForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        print('__init__ LinkForm')
        super(LinkForm, self).__init__(*args, **kwargs)
        data = kwargs.get('data')
        print('xd')

    class Meta:
        model = Link
        exclude = ('curriculum',)


class GraphicEngineExperienceForm(ModelForm):

    class Meta:
        model = GraphicEngineExperience
        exclude = ['curriculum']


class AptitudeForm(ModelForm):
    aptitude = CharField(widget=Textarea(attrs={'class': 'materialize-textarea'}), label=_('Aptitudes'),)

    class Meta:
        model = Aptitude
        exclude = ['curriculum']


class ProfessionalExperienceForm(ModelForm):
    """ startDate = DateField(widget=SelectDateWidget()) """
    center = CharField(widget=Textarea(attrs={'class': 'materialize-textarea'}), label=_('Center'),)
    formation = CharField(widget=Textarea(attrs={'class': 'materialize-textarea'}), label=_('Formation'),)

    class Meta:
        model = ProfessionalExperience
        exclude = ['curriculum']


class FormationForm(ModelForm):
    center = CharField(widget=Textarea(attrs={'class': 'materialize-textarea'}), label=_('Center'),)
    formation = CharField(widget=Textarea(attrs={'class': 'materialize-textarea'}), label=_('Formation'),)

    class Meta:
        model = Formation
        exclude = ['curriculum']


class html5showcaseForm(ModelForm):
    embedCode = CharField(widget=Textarea(attrs={'class': 'materialize-textarea'}), label=_('embedCode'),)

    class Meta:
        model = HTML5Showcase
        exclude = ['curriculum']

    def clean_embedCode(self):
        data = self.cleaned_data['embedCode']
        regex = re.compile('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        result = regex.match(data)
        if not result:
            raise ValidationError(_("Please, enter a valid URL"))
        return data


class JobOfferForm(ModelForm):

    class Meta:
        model = JobOffer
        exclude = ['business']


class ChallengeForm(ModelForm):

    class Meta:
        model = Challenge
        exclude = ['business', 'freelancers']


class ChallengeResponseForm(ModelForm):
    title = CharField(widget=Textarea(attrs={'class': 'materialize-textarea col l6'}), label=_('title'), )
    class Meta:
        model = ChallengeResponse
        exclude = ('freelancer','challenge')


class EventForm(ModelForm):
    location = CharField(widget=Textarea(attrs={'class': 'materialize-textarea'}), label=_('location'),)
    title = CharField(widget=Textarea(attrs={'class': 'materialize-textarea'}), label=_('title'),)
    description = CharField(widget=Textarea(attrs={'class': 'materialize-textarea'}), label=_('description'),)
    messageOnJoin = CharField(widget=Textarea(attrs={'class': 'materialize-textarea'}), label=_('Predefined message for joining'), )
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), label=_('Tags'), required=False,)
    moment = DateField(widget=DateInput(), label=_("moment"))

    class Meta:
        model = Event
        exclude = ['manager', 'freelancers','companies']

    def clean_moment(self):
        print('clean: EventForm: moment')
        data = self.cleaned_data['moment']
        from_date = datetime.now()
        print(str(from_date))
        print(str(data))
        if data < datetime.date(from_date):
            raise ValidationError(_("Select a date that has not passed"))
        return data


class MessageForm(ModelForm):

    class Meta:
        model = Message
        exclude = ['sender', 'timestamp', 'readed']


class ReplyForm(ModelForm):

    class Meta:
        model = Message
        exclude = ['sender','recipient', 'subject', 'timestamp', 'readed']


class BuyCoinsForm(forms.Form):
    quantity = IntegerField(label=_('Quantity'))

    def __init__(self,  *args, **kwargs):
        self.buss = kwargs.pop('buss_id', None)
        super(BuyCoinsForm, self).__init__(*args, **kwargs)

    def clean_quantity(self):
        print('clean: BuyCoinsForm: quantity')
        quantity = self.cleaned_data['quantity']
        business = Business.objects.get(pk=self.buss)
        total = business.coins + quantity
        system_variable = SystemVariables.objects.first()
        if business.subscriptionModel and business.subscriptionModel.maxCoins < total or \
                business.subscriptionModel is None and system_variable.defaultMaxCoins < total:
            raise ValidationError(_("You can not buy more coins that the coins your wallet can hold"))
        return quantity

class BroadcastForm(ModelForm):
    
    class Meta:
        model = Message
        fields = ['text']