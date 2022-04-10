import datetime
import operator
import time
import random
from webbrowser import get

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from weightlog.models import Weight
from weightlog.forms import WeightForm

# Create your views here.

User = get_user_model()

@login_required
def index(request):
    """View for home page of site"""
    my_user = request.user
    # filter so that it only gets a certain number (ie 5)
    user_weights_week = Weight.objects.filter(user=request.user).filter(date__gte=(datetime.datetime.now() - datetime.timedelta(days=7)).date())
    if user_weights_week:
        mean = sum(weight.kg for weight in user_weights_week) / len(user_weights_week)
        ordered = sorted(user_weights_week, key=operator.attrgetter('kg'))
        medium = ordered[(len(user_weights_week) - 1) // 2].kg
    else:
        mean = 0
        medium = 0
    context = {
        'week_mean': mean,
        'week_medium': medium,
        'user_weights': user_weights_week,
        'my_user': my_user,
    }

    return render(request, 'index.html', context=context)

class WeightListView(LoginRequiredMixin, generic.ListView):
    model = Weight
    #paginate_by = 10

    def get_queryset(self):
        return Weight.objects.filter(user=self.request.user)

    def get_context_data(self,**kwargs):
        context = super(WeightListView, self).get_context_data(**kwargs)
        context['my_user']=self.request.user
        return context

class WeightDetailView(LoginRequiredMixin, generic.DetailView):
    model = Weight
    template_name = 'weightlog/weight_detail.html'

    def get_context_data(self,**kwargs):
        pk = self.kwargs['pk']
        context = super(WeightDetailView, self).get_context_data(**kwargs)
        context['my_user']=self.request.user
        context['weight'] = Weight.objects.filter(id=pk).filter(user=self.request.user)
        return context

class WeightCreate(LoginRequiredMixin, CreateView):
    model = Weight
    form_class = WeightForm
    
    # Gets form arguments
    def get_form_kwargs(self):
        kwargs = super(WeightCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Set user to be current user on weight object
    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(WeightCreate, self).form_valid(form)

    # Return back to weight list page
    def get_success_url(self):
        return reverse_lazy('weights')

    def get_context_data(self,**kwargs):
        context = super(WeightCreate, self).get_context_data(**kwargs)
        context['my_user']=self.request.user
        return context

class WeightUpdate(LoginRequiredMixin, UpdateView):
    model = Weight
    template_name_suffix = "_update_form"
    fields = ['note', 'kg']

    # Return back to weight list page
    def get_success_url(self):
        return reverse_lazy('weights')

    def get_context_data(self,**kwargs):
        context = super(WeightUpdate, self).get_context_data(**kwargs)
        context['my_user']=self.request.user
        return context
    
class WeightDelete(LoginRequiredMixin, DeleteView):
    model = Weight
    success_url = reverse_lazy('weights')

    def get_context_data(self,**kwargs):
        context = super(WeightDelete, self).get_context_data(**kwargs)
        context['my_user']=self.request.user
        return context

class lineChart(LoginRequiredMixin, generic.View):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return render(request, 'linechart.html')

# def chart_data(request, *args, **kwargs):
#     data = {
#         "sale": 100,
#         "customers": 10,
#     }
#     return JsonResponse(data)

class ChartData(LoginRequiredMixin, APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        # user_weights_week = Weight.objects.filter(user=request.user.id).filter(date__gte=(datetime.datetime.now() - datetime.timedelta(days=7)).date())
        # chart_weight_value = user_weights_week.values_list('kg', flat=True).order_by('-date')
        # chart_weight_date = user_weights_week.values_list('date', flat=True).order_by('-date')
        labels = ["Red", "blue"]
        default_items = [5, 2]
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)
