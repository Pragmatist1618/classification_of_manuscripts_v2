from django.shortcuts import render
from django.views.generic.base import View


class Home(View):
    def get(self, request, *args, **kwargs):
        context = {'title': 'Home page', 'url_name': 'index'}
        return render(request, "index.html", context=context)
