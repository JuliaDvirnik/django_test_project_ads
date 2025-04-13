from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal


class AdsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='alice', password='pass')
        self.user2 = User.objects.create_user(username='bob', password='pass')
        self.ad1 = Ad.objects.create(user=self.user1, title='Ad1', description='desc', category='items', condition='new')
        self.ad2 = Ad.objects.create(user=self.user2, title='Ad2', description='info', category='items', condition='used')

    def test_register_and_login(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': '12345testpass',
            'password2': '12345testpass'
        })
        self.assertEqual(response.status_code, 302)

    def test_create_ad(self):
        self.client.login(username='alice', password='pass')
        response = self.client.post(reverse('create_ad'), {
            'title': 'Test Ad',
            'description': 'Text',
            'category': 'items',
            'condition': 'used'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title='Test Ad').exists())

    def test_edit_ad_by_owner(self):
        self.client.login(username='alice', password='pass')
        response = self.client.post(reverse('edit_ad', args=[self.ad1.pk]), {
            'title': 'Updated',
            'description': 'Changed',
            'category': 'items',
            'condition': 'used'
        })
        print(response)
        self.assertEqual(response.status_code, 302)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Updated')

    def test_edit_invalid_category(self):
        self.client.login(username='alice', password='pass')
        response = self.client.post(reverse('edit_ad', args=[self.ad1.pk]), {
            'title': 'Updated',
            'description': 'Changed',
            'category': 'books',
            'condition': 'used'
        })
        print(response)
        self.assertEqual(response.status_code, 400)

    def test_edit_ad_forbidden_for_other(self):
        self.client.login(username='bob', password='pass')
        response = self.client.post(reverse('edit_ad', args=[self.ad1.pk]), {
            'title': 'Hacked'
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_ad(self):
        self.client.login(username='alice', password='pass')
        response = self.client.post(reverse('delete_ad', args=[self.ad1.pk]))
        self.assertFalse(Ad.objects.filter(pk=self.ad1.pk).exists())

    def test_ad_list_search(self):
        response = self.client.get(reverse('index'), {'q': 'Ad1'})
        self.assertContains(response, 'Ad1')
        self.assertNotContains(response, 'Ad2')

    def test_create_exchange(self):
        self.client.login(username='alice', password='pass')
        response = self.client.post(reverse('create_exchange'), {
            'ad_sender': self.ad1.pk,
            'ad_receiver': self.ad2.pk,
            'comment': 'deal'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_accept_Proposal(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1, ad_receiver=self.ad2, status='pending'
        )
        self.client.login(username='bob', password='pass')
        self.client.post(reverse('exchange_detail', args=[proposal.pk]), {
            'action': 'accept'
        })
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')

    def test_my_exchanges_filter(self):
        ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, status='pending')
        self.client.login(username='alice', password='pass')
        response = self.client.get(reverse('my_exchanges'), {'role': 'sender', 'status': 'pending'})
        self.assertContains(response, 'Ad1')
