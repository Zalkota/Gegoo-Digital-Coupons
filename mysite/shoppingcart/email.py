#mail
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_purchase_success_email(emailRecipient, user):

	subject = ' Your Bumper Sticker order of'
	sender = 'dominic@modwebservices.com'
	receiver = emailRecipient
	context = ({'email': emailRecipient, 'user': user})
	html_content = render_to_string('account/email/shoppingcart/purchase_success_email.html', context)
	message = render_to_string('account/email/shoppingcart/purchase_success_email.html', context)
	send_mail(subject,
              message,
              sender,
              [receiver],
              fail_silently=False,
              html_message=html_content)
