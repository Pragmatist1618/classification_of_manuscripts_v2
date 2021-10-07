from django.urls import path
from .views import Manuscript_list, Manuscript_item, Manuscript_image

urlpatterns = [
    path('', Manuscript_list.as_view(), name='manuscript'),
    path('<int:pk>/', Manuscript_item.as_view(), name='manuscript-item'),
    path('img/<int:pk>/', Manuscript_image.as_view(), name='manuscript-img'),

]