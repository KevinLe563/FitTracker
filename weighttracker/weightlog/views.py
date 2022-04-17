import datetime
import operator
import time
import random
from webbrowser import get

from django import forms
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from weightlog.models import Weight
from weightlog.forms import WeightForm, ProfileForm, UpdateWeightForm

# Create your views here.

User = get_user_model()

@login_required
def index(request):
    """View for home page of site"""
    # homepage changed to chart page using redirect

    return redirect(reverse('chart', kwargs={'pk':7}))

class WeightListView(LoginRequiredMixin, generic.ListView):
    model = Weight
    #paginate_by = 10

    def get_queryset(self):
        return Weight.objects.filter(user=self.request.user)

    def get_context_data(self,**kwargs):
        context = super(WeightListView, self).get_context_data(**kwargs)
        context['my_user']=self.request.user
        return context

class UserProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "weightlog/edit_profile_form.html"
    form_class = ProfileForm

    # pass user into form args
    def get_form_kwargs(self):
        kwargs = super(UserProfileUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Return back to weight list page
    def get_success_url(self):
        return reverse_lazy('index')

    def get_context_data(self,**kwargs):
        context = super(UserProfileUpdate, self).get_context_data(**kwargs)
        context['my_user']=self.request.user
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_superuser:
            qs = qs.filter(pk=self.request.user.pk)
        return qs

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
        return reverse_lazy('chart', kwargs={'pk': 7})

    def get_context_data(self,**kwargs):
        context = super(WeightCreate, self).get_context_data(**kwargs)
        context['my_user']=self.request.user
        return context

    def get(self, request, *args, **kwargs):
        if Weight.objects.filter(user=self.request.user).filter(date=datetime.datetime.today()).exists():
            return redirect('chart', pk=7)
        return super().get(request, *args, **kwargs)

class WeightUpdate(LoginRequiredMixin, UpdateView):
    model = Weight
    template_name = "weightlog/weight_update_form.html"
    form_class = UpdateWeightForm

    # Return back to weight list page
    def get_success_url(self):
        return reverse_lazy('chart', kwargs={'pk': 7})

    def get_context_data(self,**kwargs):
        context = super(WeightUpdate, self).get_context_data(**kwargs)
        context['my_user']=self.request.user
        context['today_date']=datetime.date.today()
        return context

    def get_queryset(self, *args, **kwargs):
        return Weight.objects.filter(user=self.request.user)
    
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
        my_user = request.user
        # comma needed
        pk_tuple = kwargs['pk'],
        pk = pk_tuple[0]

        # data for table
        weights = Weight.objects.filter(user=request.user)
        if weights:
            qs = Weight.objects.filter(user=request.user)[:7]
            weights = Weight.objects.filter(id__in=qs)
        
        # personal stats
        user_weights_week = weights.filter(date__gte=(datetime.datetime.now() - datetime.timedelta(days=7)).date())
        if user_weights_week:
            mean = round(sum(weight.kg for weight in user_weights_week) / len(user_weights_week), 2)
            ordered = sorted(user_weights_week, key=operator.attrgetter('kg'))
            median = ordered[(len(user_weights_week) - 1) // 2].kg
        else:
            mean = 0
            median = 0

        today_weight = Weight.objects.filter(user=request.user).filter(date=datetime.date.today())

        context = {
            "my_user": my_user,
            "pk": pk,
            "weights": weights,
            'week_mean': mean,
            'week_median': median,
            'user_weights': user_weights_week,
            'today_weight': today_weight,
        }
        return render(request, 'index.html', context=context)

def chart_data(request, *args, **kwargs):
    pk = kwargs['pk']
    if pk <= 0:
        # return all user weights if invalid number is passed
        user_weights = Weight.objects.filter(user=request.user.id)
    else:
        user_weights = Weight.objects.filter(user=request.user.id).filter(date__gte=(datetime.datetime.now() - datetime.timedelta(days=pk)).date())
    chart_weight_value = user_weights.values_list('kg', flat=True).order_by('date')
    chart_weight_date = user_weights.values_list('date', flat=True).order_by('date')
    data = {
        "weight": list(chart_weight_value),
        "date": list(chart_weight_date),
    }
    return JsonResponse(data)


# REST API
# class ChartData(LoginRequiredMixin, APIView):
#     authentication_classes = []
#     permission_classes = []
#     def get(self, request, format=None):
#         labels = ["Red", "blue"]
#         default_items = [5, 2]
#         data = {
#             "labels": labels,
#             "default": default_items,
#         }
#         return Response(data)
