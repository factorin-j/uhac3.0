from django.views.generic import CreateView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from .models import UserStream, CriminalRecord
from django.shortcuts import redirect, render
from .forms import CriminalRecordForm, RegistrationForm
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
        return redirect('account_profile')


class IndexView(TemplateView):
    template_name = 'index.html'


# noinspection PyMethodMayBeStatic
class CriminalRecordView(LoginRequiredView, DetailView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, 'records/profile.html')

        print(dir(request.user))
        records = CriminalRecord.objects.filter(user=request.user)
        return render(request, 'records/list.html', {
            'records': records
        })

    def get_context_data(self, **kwargs):
        context = super(CriminalRecordView, self).get_context_data(**kwargs)
        context['records'] = self.request.user.criminalrecords
        return context


class CriminalRecordCreateView(CreateView):
    form_class = CriminalRecordForm
    success_url = reverse_lazy('records.list')
    template_name = 'records/create.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, 'records/profile.html')
        return super(CriminalRecordCreateView, self).dispatch(request, *args, **kwargs)


class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('api.login')
    template_name = 'registration/register.html'
