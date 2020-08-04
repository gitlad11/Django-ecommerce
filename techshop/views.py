from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.contrib import messages 
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from products.models import *
from Users.models import *
from Users.forms import LoginForm

def HomePage(request):
    Products = Product.objects.all()
    form = LoginForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username = data['Login'], password = data['Password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('HomePage')
                    messages.success(request, 'Login in')
                else:
                    return HttpResponse('account is disabled')
            else:
                return HttpResponse('Invalid login or password')
    else: form = LoginForm(request.POST)
        
    context = {'Products': Products, 'form': form}
    return render(request, 'content.html', context)

class ProductDetailView(DetailView, request):
    #model = Product
    form_class = LoginForm(request.POST)
    template_name = 'Product_detail.html'
    #context_object_name = 'Product'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product,slug=slug)
        return product

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        product = context['object']
        form = context['form_class']
        return context

    def form_valid(self, form):
        
        if request.method == 'POST':
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(username= data['Login'], password= data['Password'])
                if user is not None:
                    if user.is_active:
                        login(request, User)
                        return redirect('HomePage')
                    else: 
                        return HttpResponse('account is disabled')
        
        return form

def ProductDetail(request, slug=''):
     Details = get_object_or_404(Product,slug=slug)
     form = LoginForm(request.POST)
     if request.method == 'POST':
         if form.is_valid():
             data = form.cleaned_data
             user = authenticate(username= data['Login'], password = data['Password'])
             if user is not None:
                 if user.is_active:
                     login(request, user)
                     return redirect('HomePage')
                 else:
                     return HttpResponse('account is disabled')
             else: 
                 return HttpResponse('Invalid login or password')
     else: form = LoginForm(request.POST)

     context = {'Details': Details, 'form': form}
     return render(request, 'Product_detail.html', context)

class PaymentView():
    #������ ������������ ��������� ����� �� db
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user)
        context = {'order': order}
        return render(self.request, 'payment.html',context)
    
    #��������� ������ �� post ������ 
    def ordering(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user)
        amount = int(order.get_total() * 100)
        #������� ������� ������������ , � ���� ������ ����� ���������� ������� ������ 
        #yandex ,paypal , stripe
        payment = Payment()
        #������ ��������� payment ��������
        payment.user = self.request.user
        #���������� ����� ������ ����� ���� ������
        payment.amount = order.get_total()
        payment.save()       
        order.payment = payment
        order.save()
        
        messages.success(self.request, "Order was successful")
        return redirect('/')