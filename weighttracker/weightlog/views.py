from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from weightlog.models import Weight

# Create your views here.

@login_required
def index(request):
    """View for home page of site"""
    my_user = request.user
    # filter so that it only gets a certain number (ie 5)
    user_weights = Weight.objects.filter(user=request.user)
    context = {
        'user_weights': user_weights,
        'my_user': my_user,
    }

    return render(request, 'index.html', context=context)