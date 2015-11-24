from django.views.generic import View
from django.core.files.storage import get_storage_class
from django.http import JsonResponse

from braces.views import LoginRequiredMixin
from med.questions.forms import UploadImageForm


class UploadImage(LoginRequiredMixin, View):
    def post(self, request):
        response = {}
        form = UploadImageForm(request.POST, request.FILES)
        storage = get_storage_class()()
        if form.is_valid():
            f = request.FILES['file']
            filename = storage.get_available_name(f.name)
            with storage.open(filename, 'wb') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)
            response['location'] = storage.url(filename)
        else:
            response['error'] = form.errors
        return JsonResponse(response)
