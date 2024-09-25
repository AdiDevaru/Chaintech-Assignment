from django.shortcuts import render, redirect
from django.urls import reverse_lazy

#login-auth libraries
from django.contrib.auth.views import LoginView 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login 

#generic class-views
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from .forms import UserEditForm
from .models import Quote


#USER AUTH
class CustomLoginView(LoginView):
    template_name = 'playground/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self) -> str:
        return reverse_lazy('home')

class RegisterUser(FormView):
    form_class = UserCreationForm
    template_name = 'playground/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterUser, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterUser, self).get(*args, **kwargs)


#QUOTE PAGE
class QuoteList(ListView):
    template_name = 'playground/home.html'
    context_object_name = 'quotes'
    model = Quote
    
class QuoteCreate(LoginRequiredMixin, CreateView):
    model = Quote
    fields = ['body']
    success_url = reverse_lazy('home')
    template_name = 'playground/quote_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateView, self).form_valid(form)

class QuoteUpdate(LoginRequiredMixin, UpdateView):
    model = Quote
    fields = ['body']
    success_url = reverse_lazy('home')
    
class QuoteDelete(LoginRequiredMixin, DeleteView):
    model = Quote
    success_url = reverse_lazy('home')
    template_name = 'playground/quote_delete.html'
    
    
#USER PROFILE
class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = 'playground/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

class UserEditView(LoginRequiredMixin, FormView):
    template_name = 'playground/edit_profile.html'
    form_class = UserEditForm
    success_url = reverse_lazy('profile')  

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user  
        return kwargs

    def form_valid(self, form):
        form.save()  
        return super().form_valid(form)