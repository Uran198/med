from django.conf.urls import url

from . import views

urlpatterns = [
    # Image upload

    url(r'^upload_image/$',
        views.UploadImage.as_view(),
        name='upload_image',
        ),
]
