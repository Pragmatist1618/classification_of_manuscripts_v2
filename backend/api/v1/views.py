import json

from PIL import Image as img_pil
from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend

from classification_of_manuscripts_v2.settings import MEDIA_URL, BASE_DIR

from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Manuscript, Image
from .serializers import ManuscriptGetSerializer, ManuscriptSetSerializer, ImageSerializer, ImageInfoSerializer


# используем viewsets т.к. нужны: `create()`, `retrieve()`, `update()`,
#     `partial_update()`, `destroy()` and `list()` actions
# 'manuscript-api'
class ManuscriptViewSet(viewsets.ModelViewSet):
    # определяем набор данных
    queryset = Manuscript.objects.all()
    # права доступа
    permission_classes = [
        permissions.AllowAny,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('storage', 'creation_date', 'creation_date_bgn', 'creation_date_end', 'cipher', 'type', 'lec_type')


    # подключаем сериалайзер
    # метод выбора сериалайзера
    def get_serializer_class(self):
        # если мы получаем набор данных или один элемент
        # то используем сериалайзер с получением изображений
        if self.action == 'list' or self.action == 'retrieve':
            return ManuscriptGetSerializer
        # для прочих действий изображения не нужны
        return ManuscriptSetSerializer


# 'manuscript-img'
class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['manuscript','creation_date', 'creation_date', 'creation_date_bgn', 'creation_date_end',
                        'folio_number', 'part_of_folio', 'lec_part_type', 'lec_month_type', 'gospel', 'chapter',
                        'verse', 'verse_quote', 'image_name', 'img_description']

    # TODO img_fields = ['creation_date', 'folio_number', 'part_of_folio', 'chapter', 'verse', 'verse_quote',
    #               'image_name', 'img_description']



# manuscript and img-pk
# нследуемся от api-view т.к нам необходим только метод get
class ImageInfoView(APIView):
    def get(self, request, pk):
        # получаем сущность
        image = get_object_or_404(Image, id=pk)
        # получаем id рукописи
        # manuscript_id = image.manuscript

        serializer = ImageInfoSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)



def img_rotate(request, pk):
    if request.method == 'POST':
        img = get_object_or_404(Image, id=pk)

        im = img_pil.open(img.image)
        # im.show()

        im_rotate = im.rotate(90, expand=True)
        # im_rotate.show()

        im_rotate.save(BASE_DIR + '/backend' + MEDIA_URL + str(img.image))
        im.close()

        return HttpResponse(json.dumps({'message': []}))
