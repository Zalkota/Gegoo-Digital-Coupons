
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_contact_email_admin(context):
	if not settings.DEBUG:
		subject = 'GEGOO SUPPORT EMAIL'
		sender = settings.EMAIL_ADDRESS_FROM
		# receiver = settings.SUPPORT_EMAIL_ADDRESS_TO #TODO
		context = ({'email': emailRecipient})
		html_content = render_to_string('mail/mail_success.html', context)
		message = render_to_string('mail/mail_success.html', context)
		send_mail(subject,
	              message,
	              sender,
	              [receiver],
	              fail_silently=False,
	              html_message=html_content)

def send_contact_email_user(emailRecipient, email):
	if not settings.DEBUG:
		subject = 'GEGOO SUPPORT EMAIL'
		sender = settings.EMAIL_ADDRESS_FROM
		receiver = emailRecipient
		context = ({'email': emailRecipient, 'user': user})
		html_content = render_to_string('mail/mail_success.html', context)
		message = render_to_string('mail/mail_success.html', context)
		send_mail(subject,
	              message,
	              sender,
	              [receiver],
	              fail_silently=False,
	              html_message=html_content)

def send_contact_form_submission(name, email, message):
	subject = 'Contact Request from Realistic Landscapes'
	sender = email
	receiver = settings.SUPPORT_EMAIL_ADDRESS_TO #TODO
	context = ({'email': email, 'name': name, 'message': message})
	html_content = render_to_string('mail/mail_contact.html', context)
	message = render_to_string('mail/mail_contact.html', context)
	send_mail(subject,
              message,
              sender,
              [receiver],
              fail_silently=False,
              html_message=html_content)


## Invoice Email
# def send_invoice_email(sender, created, instance, **kwargs):
# 	print('email_sent=', instance.email_sent)
#
# 	if created == True and instance.email_sent == False:
# 		invoice = instance
# 		try:
# 			invoice.email_sent = True
# 			invoice.ref_code = unique_order_id_generator()
# 			invoice.save()
# 		except:
# 			None
# 		user = instance.user
# 		emailRecipient = instance.user.email
# 		amount = instance.amount
# 		description = instance.description
# 		print(emailRecipient)
# 		subject = 'New Invoice from Mod Technologies'
# 		sender = 'Dominic'
# 		receiver = emailRecipient
# 		context = ({'email': emailRecipient, 'user': user, 'amount': amount, 'description': description})
# 		html_content = render_to_string('mail/email_invoice_new.html', context)
# 		message = render_to_string('mail/email_invoice_new.html', context)
# 		send_mail(subject,
# 	              message,
# 	              sender,
# 	              [receiver],
# 	              fail_silently=False,
# 	              html_message=html_content)
# 	else:
# 		print('EMAIFAIL')
