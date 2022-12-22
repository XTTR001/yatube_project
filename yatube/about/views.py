from django.shortcuts import render
from django.views.generic.base import TemplateView

class AboutAuthorView(TemplateView):  # TODO
    template_name = 'about/about.html'

class AboutTechView(TemplateView):  # TODO
    template_name = 'about/tech.html'
