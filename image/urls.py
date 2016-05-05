from django.conf.urls import patterns,include,url

urlpatterns = patterns('',url(r'^generate/','image.views.get_image_mask'))
