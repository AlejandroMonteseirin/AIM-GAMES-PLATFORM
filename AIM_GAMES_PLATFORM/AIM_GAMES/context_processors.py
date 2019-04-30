from .models import Business
from django.shortcuts import get_object_or_404


def messagesCount(request):
    context_data = dict()
    count = 0
    if request.user.is_authenticated:
        user = request.user
        count = Message.objects.filter(recipient=user).count()
    context_data['message_count'] = count
    return context_data

def get_wallet(request):
    context_data = dict()
    wallet = None
    if request.user.is_authenticated:
       if request.session['currentUser'] == "business":
           # business = Business.objects.select_related('profile').get(id=profile.business.id)
           wallet = get_object_or_404(Business, profile=request.user.profile)
    context_data['wallet'] = wallet
    return context_data