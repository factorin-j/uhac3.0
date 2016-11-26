from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import RegistrationForm
from .models import UserStream
from django.views import View
from .sdk import Client


class LoginRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # noinspection PyUnresolvedReferences
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)


# noinspection PyMethodMayBeStatic
class ConnectView(LoginRequiredView):
    def get(self, request):
        return redirect(Client.get_client().create_auth_url())


# noinspection PyMethodMayBeStatic
class VerifyView(LoginRequiredView):
    def get(self, request):
        code = request.GET.get('code')
        user_stream = UserStream.objects.get(user=request.user)
        user_stream_id = user_stream.stream_id if user_stream else None
        response = Client.get_client().authorize(code, user_stream_id)
        return HttpResponse(response.content)


class RootView(View):
    def dispatch(self, request, *args, **kwargs):
        return redirect('login')


# noinspection PyMethodMayBeStatic
class AccountsProfileView(LoginRequiredView, DetailView):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/profile.html')

    def get_context_data(self, **kwargs):
        context = super(AccountsProfileView, self).get_context_data(**kwargs)
        context['accounts'] = self.request.user.account
        return context


class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


# class AccountsCreateView(LoginRequiredView):
