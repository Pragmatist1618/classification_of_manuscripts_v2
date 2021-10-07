import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from urllib.parse import unquote
from backend.api.v1.models import Manuscript, Image
from backend.api.v1.serializers import ManuscriptGetSerializer


class Manuscript_list(View):
    def get(self, request, *args, **kwargs):
        context = {'title': 'Manuscript list', 'url_name': 'manuscript'}
        manuscript_list = Manuscript.objects.all()

        # фильтры по рукописям:
        if request.GET.get('type'):
            manuscript_list = manuscript_list.filter(type=request.GET.get('type'))

        if request.GET.get('storage'):
            manuscript_list = manuscript_list.filter(storage=request.GET.get('storage'))

        if request.GET.get('cipher'):
            manuscript_list = manuscript_list.filter(cipher=request.GET.get('cipher'))

        if request.GET.get('lec_type'):
            print(request.GET.get('lec_type'))
            manuscript_list = manuscript_list.filter(lec_type=request.GET.get('lec_type'))

        # преобразование qs в list с получением поля images
        manuscript_list = ManuscriptGetSerializer(manuscript_list, many=True).data

        # фильтры по изображениям
        if request.GET.get('lec_part_type'):
            for manuscript in manuscript_list:
                i = 0
                while i < len(manuscript['images']):
                    if manuscript['images'][i]['lec_part_type'] != request.GET.get('lec_part_type'):
                        manuscript['images'].remove(manuscript['images'][i])
                    else:
                        i += 1
        if request.GET.get('lec_month_type'):
            for manuscript in manuscript_list:
                i = 0
                while i < len(manuscript['images']):
                    if manuscript['images'][i]['lec_month_type'] != request.GET.get('lec_month_type'):
                        manuscript['images'].remove(manuscript['images'][i])
                    else:
                        i += 1

        # todo удалить из выборки рукописи без изображений
        context['manuscript_list'] = manuscript_list

        storages = []
        lec_types = []

        gospels = []
        part_of_folios = []
        lec_part_types = []

        for manuscript in manuscript_list:
            if not manuscript['storage'] in storages and manuscript['storage'] is not None:
                storages.append(manuscript['storage'])

            if not manuscript['lec_type'] in lec_types and manuscript['lec_type'] is not None:
                lec_types.append(manuscript['lec_type'])

            for img in manuscript['images']:
                if not img['gospel'] in gospels and img['gospel'] is not None:
                    gospels.append(img['gospel'])

                if not img['part_of_folio'] in part_of_folios and img['part_of_folio'] is not None:
                    part_of_folios.append(img['part_of_folio'])

                if not img['lec_part_type'] in lec_part_types and img['lec_part_type'] is not None:
                    lec_part_types.append(img['lec_part_type'])

        context['storages'] = storages
        context['lec_types'] = lec_types

        context['gospels'] = gospels
        context['part_of_folios'] = part_of_folios
        context['lec_part_types'] = lec_part_types

        LEC_MONTH_CHOICES = [
            "St",
            'Ok',
            'Nw',
            'Dec',
            "Ja",
            'Feb',
            'Mar',
            'Apr',
            "May",
            'Jun',
            'Jul',
            'Aug',
            'unknown',
        ]

        context['lec_month_choices'] = LEC_MONTH_CHOICES

        to_update_man = []
        to_update_img = []
        man_fields = ['storage', 'creation_date', 'cipher', 'man_description', 'bibliography']
        img_fields = ['creation_date', 'folio_number', 'part_of_folio', 'chapter', 'verse', 'verse_quote',
                      'image_name', 'img_description']
        for manuscript in manuscript_list:
            for man_field in man_fields:
                if 'уточнить' in manuscript[man_field].lower() or 'уточняется' in manuscript[man_field].lower():
                    if manuscript['id'] not in to_update_man:
                        to_update_man.append(manuscript['id'])
            for img in manuscript['images']:
                for img_field in img_fields:
                    if img[img_field]:
                        if 'уточнить' in img[img_field].lower() or 'уточняется' in img[img_field].lower():
                            if manuscript['id'] not in to_update_man:
                                to_update_man.append(manuscript['id'])
                            to_update_img.append(img['id'])

        context['to_update_man'] = to_update_man
        context['to_update_img'] = to_update_img

        # if request.GET.urlencode().split('=') != ['']:
        #     context['filter_key'] = unquote(request.GET.urlencode().split('=')[0]).replace('+', ' ')
        #     context['filter_value'] = unquote(request.GET.urlencode().split('=')[1]).replace('+', ' ')

        # print(get_manuscript_by_id(1))
        return render(request, "manuscript_list.html", context=context)


class Manuscript_item(View):
    def get(self, request, *args, **kwargs):
        url = request.build_absolute_uri(reverse('manuscript-api-detail',
                                                 kwargs={'pk': self.kwargs.get('pk')}))
        manuscript_api = requests.get(url).json()
        context = {
            'title': manuscript_api['cipher'],
            'manuscript': manuscript_api
        }
        return render(request, "manuscript_item.html", context=context)


class Manuscript_image(View):
    def get(self, request, *args, **kwargs):
        url = request.build_absolute_uri(reverse('manuscript-img-details',
                                                 kwargs={'pk': self.kwargs.get('pk')}))

        manuscript_img = requests.get(url).json()
        print(manuscript_img)

        context = {
            'title': manuscript_img['cipher'],
            'manuscript': manuscript_img
        }
        return render(request, "manuscript_img.html", context=context)

