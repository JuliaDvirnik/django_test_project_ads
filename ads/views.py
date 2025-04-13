from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import AdForm, ExchangeOfferForm
from .models import Ad, ExchangeOffer


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})
# todo а что если форма не валидна? упадет?


@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать это объявление.")

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/ad_form.html', {'form': form, 'edit': True})


@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление.")

    if request.method == 'POST':
        ad.delete()
        return redirect('index')

    return render(request, 'ads/confirm_delete.html', {'ad': ad})


@login_required
def create_exchange(request):
    ad_receiver_id = request.GET.get('receiver')
    ad_sender_id = request.GET.get('sender')

    initial = {}
    if ad_receiver_id:
        initial['ad_receiver'] = ad_receiver_id
    if ad_sender_id:
        initial['ad_sender'] = ad_sender_id

    if request.method == 'POST':
        form = ExchangeOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.status = 'pending'
            offer.save()
            return redirect('exchange_detail', pk=offer.pk)
    else:
        form = ExchangeOfferForm(initial=initial)

    user_ads = Ad.objects.filter(user=request.user)
    all_ads = Ad.objects.exclude(user=request.user)
    return render(request, 'exchanges/exchange_form.html', {
        'form': form,
        'user_ads': user_ads,
        'all_ads': all_ads,
    })


@login_required
def exchange_detail(request, pk):
    offer = get_object_or_404(ExchangeOffer, pk=pk)
    return render(request, 'exchanges/exchange_detail.html', {'offer': offer})


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
# todo а что если форма не валидна? упадет?


def ad_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    condition = request.GET.get('condition', '')

    ads = Ad.objects.all()

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads.order_by('-created_at'), 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {
        'page_obj': page_obj,
        'query': query,
        'category': category,
        'condition': condition,
        'condition_choices': Ad._meta.get_field('condition').choices,
        'category_choices': Ad._meta.get_field('category').choices
    })

