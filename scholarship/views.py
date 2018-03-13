from django.shortcuts import render
from .filters import ScholarshipFilter
from .models import Scholarship

def scholarship_list(request):
    f = ScholarshipFilter(request.GET, queryset=Scholarship.objects.all())
    return render(request, 'scholarship/index.html', {'filter': f})
