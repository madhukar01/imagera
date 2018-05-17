from django.conf.urls import url
from imagera import views as image_viewer

urlpatterns = [
    url(r'^imagelist/$', image_viewer.imageListManager.as_view()),
    url(r'^imagedetail/$', image_viewer.imageDetailManager.as_view()),
    url(r'^register/$', image_viewer.generateKey.as_view()),
    url(r'^regenerate/$', image_viewer.changeKey.as_view()),
]