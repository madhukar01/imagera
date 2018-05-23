from django.conf.urls import url
from imagera import views as image_viewer

urlpatterns = [
    url(r'^imagelist/$', image_viewer.image_list_manager.as_view()),
    url(r'^imagedetail/$', image_viewer.image_detail_manager.as_view()),
    url(r'^register/$', image_viewer.generate_key.as_view()),
    url(r'^regenerate/$', image_viewer.change_key.as_view()),
]
