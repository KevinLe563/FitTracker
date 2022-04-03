from urllib import request
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from weightlog.models import Weight
from weightlog.forms import WeightForm

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
    fields = '__all__'
    
class WeightDelete(LoginRequiredMixin, DeleteView):
    model = Weight
    success_url = reverse_lazy('weights')