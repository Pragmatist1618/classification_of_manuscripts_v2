from django.urls import path
from rest_framework import routers

from .views import ManuscriptViewSet, ImagesViewSet, ImageInfoView, img_rotate

urlpatterns = [
    path('img/<int:pk>/', ImageInfoView.as_view(), name='manuscript-img-details'),
    path('img_rotate/<int:pk>/', img_rotate, name='img_rotate'),

]

# генерация url и их регистрация
router = routers.DefaultRouter()
# правый слэш на конце не ставится!
router.register('img', ImagesViewSet, basename='manuscript-img')
router.register('manuscript', ManuscriptViewSet, basename='manuscript-api')
urlpatterns += router.urls
