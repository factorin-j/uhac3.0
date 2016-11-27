from django.views.generic import CreateView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from .models import UserStream, CriminalRecord
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import CriminalRecordForm
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


# noinspection PyMethodMayBeStatic
class SearchView(TemplateView):
    template_name = 'search.html'

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name') or None
        last_name = request.POST.get('last_name') or None
        if first_name and last_name:
            # noinspection PyBroadException
            try:
                user = User.objects.get(first_name=first_name, last_name=last_name)
                return redirect('/records/' + user.id)
            except Exception:
                return render(request, 'index.html', {'error': 'User not found'})

        if first_name and not last_name:
            # noinspection PyBroadException
            try:
                users = User.objects.filter(first_name=first_name)
                return render(request, 'records/list.html', {'users': users})
            except Exception:
                return render(request, 'index.html', {'error': 'No user found using first name'})

        if first_name and last_name:
            # noinspection PyBroadException
            try:
                users = User.objects.filter(last_name=last_name)
                return render(request, 'records/list.html', {'users': users})
            except Exception:
                return render(request, 'index.html', {'error': 'No user found using last name'})


class IndexView(TemplateView):
    template_name = 'index.html'


# noinspection PyMethodMayBeStatic
class CriminalRecordView(LoginRequiredView, DetailView):
    def get(self, request, *args, **kwargs):
        records = CriminalRecord.objects.filter(user=request.user)
        return render(request, 'records/profile.html', {
            'records': records
        })

    def get_context_data(self, **kwargs):
        context = super(CriminalRecordView, self).get_context_data(**kwargs)
        context['records'] = self.request.user.criminalrecords
        return context


class CriminalRecordCreateView(CreateView):
    form_class = CriminalRecordForm
    success_url = reverse_lazy('account_profile')
    template_name = 'records/create.html'
