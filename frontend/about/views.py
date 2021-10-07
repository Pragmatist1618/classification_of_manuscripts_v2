from django.shortcuts import render
from django.views.generic.base import View


class About(View):
    def get(self, request, *args, **kwargs):
        context = {'title': 'About', 'url_name': 'about'}
        return render(request, "about.html", context=context)