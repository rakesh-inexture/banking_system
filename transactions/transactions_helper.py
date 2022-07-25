from django.contrib import messages


class Messages():
    def errors_msg(self, request, ):
        messages.error(request, f'Sorry, Your Account have not sufficient balance to transfer of this amount')

    def success_msg(self, request):
        messages.success(request)
