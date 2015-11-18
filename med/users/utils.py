import os


def upload_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return "avatars/{pk}{ext}".format(pk=instance.pk, ext=ext)
