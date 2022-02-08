from math import ceil
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from store.models import Item
import stripe
from django.views.decorators.csrf import csrf_exempt
import techat.settings as settings
from django.http import JsonResponse, HttpResponse

class ItemListView(ListView):
    model = Item
    template_name = 'store/store_home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'items'
    ordering = ['-date_posted']
    paginate_by = 6

class ItemDetailView(DetailView):
    model = Item


@csrf_exempt
def create_checkout_session(request, id):
    item = Item.objects.get(pk=id)
    
    if request.method == 'GET':
        domain_url = 'https://www.digitalstream.dev/store/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            if item.discount_price > 0:
                amount = int(item.discount_price)*100 + int(ceil(item.discount_price*0.02*100))
                checkout_session = stripe.checkout.Session.create(
                    success_url=domain_url + 'success/'+ str(id) + '/?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=domain_url + 'item/' + str(id) +"/",
                    payment_method_types=['card'],
                    mode='payment',
                    shipping_address_collection={
                    'allowed_countries': ['US', 'CA'],
                    },
                    line_items=[
                        {
                            'name': str(item.title),
                            'quantity': int(item.inventory),
                            'currency': 'usd',
                            'amount': amount,
                            'images': [
                                str(item.featured_image.url),
                                str(item.sub_image1.url),
                                str(item.sub_image2.url),
                                str(item.sub_image3.url),
                                str(item.sub_image4.url),
                                str(item.sub_image5.url),
                            ]
                        }
                    ]
                )
            else:
                amount = int(item.price)*100 + int(ceil(item.price*0.02*100))
                checkout_session = stripe.checkout.Session.create(
                    success_url=domain_url + 'success/'+ str(id) + '/?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=domain_url + 'item/' + str(id) +"/",
                    payment_method_types=['card'],
                    mode='payment',
                    shipping_address_collection={
                    'allowed_countries': ['US', 'CA'],
                    },
                    line_items=[
                        {
                            'name': str(item.title),
                            'quantity': int(item.inventory),
                            'currency': 'usd',
                            'amount': amount,
                            'images': [
                                str(item.featured_image.url),
                                str(item.sub_image1.url),
                                str(item.sub_image2.url),
                                str(item.sub_image3.url),
                                str(item.sub_image4.url),
                                str(item.sub_image5.url),
                            ]
                        }
                    ]
                )
        
            #return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        return redirect(checkout_session.url, code=303)

def success(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.inventory = item.inventory - 1
    item.save()
    return render(request, 'store/success.html')

class CancelledView(TemplateView):
    template_name = 'store/cancelled.html'


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = [
        'title', 'price', 'discount_price', 'description' ,'additional_info', 'featured_image',
        'sub_image1','sub_image2','sub_image3','sub_image4','sub_image5',
        'inventory']

    def form_valid(self, form):
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item

    fields = [
        'title', 'price', 'discount_price', 'description' ,'additional_info', 'featured_image',
        'sub_image1','sub_image2','sub_image3','sub_image4','sub_image5',
        'inventory']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if item:
            return True
        return False

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/'

    def test_func(self):
        item = self.get_object()
        if item:
            return True
        return False

def terms(request):
    return render(request, 'store/terms.html')