
from django.shortcuts import render, redirect
from . models import JobListing
from .forms import JobListingForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView, CreateView,
    UpdateView,
    DeleteView
)



class PostListView(ListView):
    model = JobListing
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

class PostDetailView(DetailView):
    model = JobListing
    template_name = 'post_detail.html' # <app>/<model>_<viewtype>.html


class PostCreateView(CreateView):
    model = JobListing
    template_name = 'post_form.html'
    ordering = ['-created_at']
    form_class = JobListingForm
    
    def form_valid(self, form):
        form.instance.company = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'login'

    model = JobListing
    template_name = 'post_form.html'
    form_class = JobListingForm

    def form_valid(self, form):
        form.instance.company = self.request.user
        messages.success(self.request, f'Your Post has been updated!')
        return super().form_valid(form)          
  
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.company:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/login/'
    redirect_field_name = 'login'

    model = JobListing
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.company:
            return True
        return False
    
from django.db.models import Q

class PostSearchView(ListView):
    model = JobListing
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        location = self.request.GET.get('location')
        min_annual_income = self.request.GET.get('min_annual_income')
        max_annual_income = self.request.GET.get('max_annual_income')

        queryset = JobListing.objects.all()
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
        
        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_annual_income:
            queryset = queryset.filter(annual_income__gte=min_annual_income)
        if max_annual_income:
            queryset = queryset.filter(annual_income__lte=max_annual_income)
        
        messages.success(self.request, f'Your Search result are here...')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_locations'] = JobListing.objects.values_list('location', flat=True).distinct()
        return context



