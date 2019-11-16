from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm, AddToCartForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile
import random
import string
import stripe

publishKey = settings.STRIPE_PUBLISHABLE_KEY

#def create_ref_code():
#    return ''.join(random.choice(string.ascii_lowercase + string.digits, k=4))

def random_string_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator():
    new_ref_code= random_string_generator()

    qs_exists= Order.objects.filter(ref_code=new_ref_code).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return new_ref_code


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    print(valid)
    return valid


#Could this be a model manager?
def get_user_address_default(request, user):
    address_qs = Address.objects.filter(user=user, default=True)
    if address_qs.exists():
        address = address_qs.first()
        return address
    else:
        address_qs = Address.objects.filter(user=user, default=False)
        if address_qs.exists():
            address = address_qs.first()
            return address
        return None


def get_user_orders(request, user):
	user_orders_qs = Order.objects.filter(user=user)
	if user_orders_qs.exists():
		return user_orders_qs
	return None


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "shoppingcart/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "Your shopping cart is empty")
            return redirect("shoppingcart:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('shoppingcart:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_city = form.cleaned_data.get(
                        'shipping_city')
                    shipping_state = form.cleaned_data.get(
                        'shipping_state')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_city, shipping_state, shipping_country, shipping_zip]):
                        print('OK is_valid_form')
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            city=shipping_city,
                            state=shipping_state,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.error(
                            self.request, "Please fill in the required shipping address fields")
                        return redirect('shoppingcart:checkout')


                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('shoppingcart:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_city = form.cleaned_data.get(
                        'billing_city')
                    billing_state = form.cleaned_data.get(
                        'billing_state')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_city, billing_state, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            city=billing_city,
                            state=billing_state,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('shoppingcart:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('shoppingcart:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('shoppingcart:checkout')
        except ObjectDoesNotExist:
            messages.info(self.request, "Your shopping cart is empty")
            return redirect("shoppingcart:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'publishKey': publishKey,
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "shoppingcart/payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("shoppingcart:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            print('token', token)
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)
                    print('retrieve customer')

                else:
                    print('create customer')
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:
                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                    amount=amount,  # cents
                    currency="usd",
                    customer=userprofile.stripe_customer_id
                    )
                else:
                    stripe.Customer.modify(
                    userprofile.stripe_customer_id, # cus_xxxyyyyz
                    source=token # tok_xxxx or src_xxxyyy
                    )
                    charge = stripe.Charge.create(
                    amount=amount,
                    currency='usd',
                    description='description',
                    #source=token
                    customer = userprofile.stripe_customer_id
                    )
                    print('payment charged')


                    # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()
                print('payment saved')

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()
                    print('order items')

                order.ordered = True
                order.payment = payment
                order.ref_code = unique_order_id_generator()
                order.save()
                print(unique_order_id_generator())
                print('order saved')
                messages.success(self.request, "Your order was successful!")
                return redirect("shoppingcart:order-review", ref_code=order.ref_code)



            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, err.get('message'))
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")


        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'shoppingcart/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "Your shopping cart is empty")
            return redirect("/")

class OrderReviewView(LoginRequiredMixin, View):


    def get(self, *args, **kwargs):
        ref_code = kwargs['ref_code']
        order = Order.objects.get(user=self.request.user, ordered=True, ref_code=ref_code)
        print(order)
        orderCategory_qs = order.items.first()
        orderCategory = orderCategory_qs.item.category
        advert_list = []

        advert_list = Item.objects.filter(category=orderCategory)
        print(advert_list)


        #result = order.items.values()             # return ValuesQuerySet object
        #list_result = [entry for entry in result]  # converts ValuesQuerySet into Python list
        #return list_result

        context = {
            'object': order,
            'advert_list': advert_list,

        }
        return render(self.request, 'shoppingcart/order_review.html', context)
        #except ObjectDoesNotExist:
        #    messages.warning(self.request, "order error")
        #    return redirect("/")

class OrderDetailView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        ref_code = kwargs['ref_code']
        order = Order.objects.get(user=self.request.user, ordered=True, ref_code=ref_code)

        context = {
            'object': order,
        }
        return render(self.request, 'shoppingcart/order_detail.html', context)


class ItemListHomeView(ListView):
    model = Item
    #paginate_by = 10
    template_name = "shoppingcart/products.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "shoppingcart/product.html"


@login_required
def add_to_cart(request, slug):
    form_class = AddToCartForm
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')


    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += quantity
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shoppingcart:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("shoppingcart:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("shoppingcart:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("shoppingcart:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shoppingcart:product", slug=slug)
    else:
        messages.info(request, "Your shopping cart is empty")
        return redirect("shoppingcart:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("shoppingcart:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shoppingcart:product", slug=slug)
    else:
        messages.info(request, "Your shopping cart is empty")
        return redirect("shoppingcart:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("shoppingcart:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("shoppingcart:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "Your shopping cart is empty")
                return redirect("shoppingcart:checkout")


class RefundSelectView(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        orders = get_user_orders(self.request, user)

        context = {
        'order_list': orders,
        }
        return render(self.request, "shoppingcart/refund_select.html", context)

class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()

        order_qs = Order.objects.filter(user=self.request.user, ref_code=self.kwargs['ref_code'])
        if order_qs.exists():
            order = order_qs.first()
        else:
            return redirect("shoppingcart:refund-select")

        context = {
            'form': form,
            'order': order
        }
        return render(self.request, "shoppingcart/request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():

            #ref_code = self.kwargs['ref_code']
            reason = form.cleaned_data.get('reason')
            message = form.cleaned_data.get('message')
            # edit the order
            try:
                order_qs = Order.objects.filter(user=self.request.user, ref_code=self.kwargs['ref_code'])
                if order_qs.exists():
                    order = order_qs.first()
                #order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = reason
                refund.message = message
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("contact-landing-page")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("shoppingcart:request-refund")
