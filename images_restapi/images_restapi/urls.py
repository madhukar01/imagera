from django.conf.urls import url
from imagera import views as image_viewer

urlpatterns = [
    url(r'^imagelist/$', image_viewer.ImageListManager.as_view()),
    url(r'^imagedetail/$', image_viewer.ImageDetailManager.as_view()),
    url(r'^register/$', image_viewer.GenerateKey.as_view()),
    url(r'^regenerate/$', image_viewer.ChangeKey.as_view()),
]
