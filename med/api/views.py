from django.views.generic import View
from django.http import JsonResponse

from braces.views import LoginRequiredMixin
from med.questions.forms import UploadImageForm


class UploadImage(LoginRequiredMixin, View):
    def post(self, request):
        response = {}
        # TODO:
        # It's strange to use forms here, maybe this method should live in
        # questions app or form should live in this one
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            response['location'] = form.file_url
        else:
            response['error'] = form.errors
        return JsonResponse(response)
