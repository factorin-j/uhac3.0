from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView
from .forms import RegistrationForm, AccountCreateForm
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from .models import UserStream, Account
from django.views import View
from .sdk import client


class LoginRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # noinspection PyUnresolvedReferences
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)


# noinspection PyMethodMayBeStatic
class ConnectView(LoginRequiredView):
    def get(self, request):
        return redirect(client.create_auth_url())


# noinspection PyMethodMayBeStatic
class VerifyView(LoginRequiredView):
    def get(self, request):
        code = request.GET.get('code')
        user_stream = UserStream.objects.get(user=request.user)
        user_stream_id = user_stream.stream_id if user_stream else None
        client.authorize(code, user_stream_id)
        request.session['oauth.access_token'] = client.access_token
        return redirect('account_profile')


class RootView(View):
    def dispatch(self, request, *args, **kwargs):
        return redirect('login')


# noinspection PyMethodMayBeStatic
class AccountsProfileView(LoginRequiredView, DetailView):
    def get(self, request, *args, **kwargs):
        accounts = Account.objects.filter(user=request.user)
        client.access_token = request.session.get('oauth.access_token')
        data = client.api('/app/profile/')
        print(data)

        return render(request, 'accounts/profile.html', {
            'accounts': accounts
        })

    def get_context_data(self, **kwargs):
        context = super(AccountsProfileView, self).get_context_data(**kwargs)
        context['accounts'] = self.request.user.account
        return context


class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class AccountsCreateView(CreateView):
    form_class = AccountCreateForm
    success_url = reverse_lazy('account_profile')
    template_name = 'accounts/create.html'
