from django.core.mail import send_mail
import random

def sendOtp(user):
    email = user
    # print(email)
    send_otp = str(random.randint(1000, 9999))
    htmlgen = "<p>Your OTP for Authentication is <strong> {} </strong> </p>".format(send_otp)
    send_mail('OTP request', send_otp, 'rakeshkumar.18172@marwadieducation.edu.in', [email], fail_silently=False, html_message=htmlgen)
    # print(send_otp)
    return send_otp
