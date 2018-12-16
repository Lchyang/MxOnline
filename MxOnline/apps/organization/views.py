from django.shortcuts import render
from django.views.generic.base import View

from .models import CourseOrg, CityDict

# Create your views here.


class OrgView(View):
    def get(self, request):
        all_org = CourseOrg.objects.all()
        all_city = CityDict.objects.all()
        return render(request, 'org-list.html', {
            'all_org':all_org,
            'all_city':all_city,
        })
