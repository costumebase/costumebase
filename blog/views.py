from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from .models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
from django.views.generic.list import MultipleObjectMixin

from taggit.models import Tag



class SearchView(generic.View):
    def get(self, request, *args, **kwargs):
        try:

            queryset1 = Post.objects.all()
            query = request.GET.get('q')
            if query:
                queryset1 = queryset1.filter(Q(title__icontains=query)|Q(overview__icontains=query)).distinct()
                queryset = list(
                    sorted(
                        chain(queryset1),
                        key=lambda objects: objects.pk
                    ))
            context = {
                'queryset': queryset,
               

            }
            return render(request, 'search.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "Search based on title and details of post")
            return redirect("blog:blogview")



class BlogView(generic.ListView):
    model = Post
    paginate_by = 5
    template_name = 'blog-left-sidebar.html'
    context_object_name = 'queryset'


class BlogDetail(generic.DetailView):
    model = Post
    template_name = 'blog-detail.html'
    context_object_name = 'queryset'


    
class PostCategoryList(generic.ListView):
    model = Blog_Category
    template_name = 'catlist.html'   
    context_object_name = 'queryset'


class PostCategoryDetailView(generic.DetailView, MultipleObjectMixin):
    model = Blog_Category
    context_object_name = 'queryset'
    template_name = 'Post_category_detail.html'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        object_list = Post.objects.filter(category=self.object)
        context = super(PostCategoryDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context


# class PostTagView()

class TagIndexView(generic.ListView):
    model = Post
    paginate_by = 6
    template_name = 'tags.html'
    context_object_name = 'queryset'

    def get_queryset(self):
        tags = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(tags=tags)






    


