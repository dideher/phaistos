from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class MainPageView(LoginRequiredMixin, View):

    def post(self, request):
        # for now, just redirect to the employee-list view
        return HttpResponseRedirect(reverse_lazy("employees:employee-list"))

    def get(self, request):
        # for now, just redirect to the employee-list view
        return HttpResponseRedirect(reverse_lazy("employees:employee-list"))
