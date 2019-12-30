from django.conf import settings

# <**************************************************************************>
# <*****                         EMAILS                                 *****>
# <**************************************************************************>


def send_subscription_cancelation_email(emailRecipient, user):
    if not settings.DEBUG:
        subject = 'Mod Technologies Subscription Cancellation Notice'
        sender = settings.EMAIL_ADDRESS_FROM
        receiver = emailRecipient
        context = ({'email': emailRecipient, 'user': user})
        html_content = render_to_string('mail/mail_cancellation.html', context)
        message = render_to_string('mail/mail_cancellation.html', context)
        send_mail(subject,
                message,
                sender,
                [receiver],
                fail_silently=False,
                html_message=html_content)

def send_payment_refund_email(emailRecipient, user, selected_amount):
    if not settings.DEBUG:
        subject = 'Mod Technologies Subscription Notice'
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

def send_payment_success_email(emailRecipient, user):
    if not settings.DEBUG:
    	subject = 'Mod Technologies Subscription Notice'
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
