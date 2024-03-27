from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Profile, Skill


def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
        
    left_index = (int(page) - 3)
    if left_index < 1:
        left_index = 1
    
    right_index = (int(page) + 4)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
        
    custom_range = range(left_index,right_index)
    
    return custom_range, profiles


def searchProfiles(request):
    query = ''
    
    if request.GET.get('query'):
        query = request.GET.get('query')
        
    skills = Skill.objects.filter(name__icontains=query)
    
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=query) |
        Q(intro__icontains=query) |
        Q(skill__in=skills)
        )
    
    return profiles, query