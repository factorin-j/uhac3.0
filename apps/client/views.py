from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views import View
from .sdk import Client
from .forms import RegistrationForm


# noinspection PyMethodMayBeStatic
class ConnectView(View):
    def get(self, request):
        return redirect(Client.get_client().create_auth_url())


# noinspection PyMethodMayBeStatic
class VerifyView(View):
    def get(self, request):
        code = request.GET.get('code')
        response = Client.get_client().authorize(code)  # , 'this_is_my_stream_id')
        return HttpResponse(response.content)


class LoginRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # noinspection PyUnresolvedReferences
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)


# noinspection PyMethodMayBeStatic
class UserView(LoginRequiredView):
    def get(self, request):
        return HttpResponse('It works!' + str(request.user))


# noinspection PyMethodMayBeStatic
class AccountProfile(LoginRequiredView):
    def get(self, request):
        print(request.user)
        return HttpResponse('Logged in: ' + str(request.user))


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
