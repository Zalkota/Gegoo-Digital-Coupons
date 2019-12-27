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
