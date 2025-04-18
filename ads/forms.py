from django import forms
from .models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'image_url': 'Ссылка на изображение',
            'category': 'Категория',
            'condition': 'Состояние',
        }


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
        labels = {
            'ad_sender': 'Отправитель',
            'ad_receiver': 'Получатель',
            'comment': 'Комментарий',
        }