from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag


def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
        
    left_index = (int(page) - 3)
    if left_index < 1:
        left_index = 1
    
    right_index = (int(page) + 4)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
        
    custom_range = range(left_index,right_index)
    
    return custom_range, projects


def searchProjects(request):
    query = ''
    
    if request.GET.get('query'):
        query = request.GET.get('query')
        
    tags = Tag.objects.filter(name__icontains=query)
    
    projects = Project.objects.distinct().filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(owner__name__icontains=query) |
        Q(tags__in=tags)
    )
    
    return projects, query
