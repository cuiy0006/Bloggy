from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post, Category, Tag
import markdown
from django.views.generic import ListView, DetailView
from comments.forms import CommentForm
from comments.models import Comment, CommentExtension
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
#region Functions are replaced by Views
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def fullWidthIndex(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/full-width-index.html', context={'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body, 
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc'
                                  ])
    return render(request, 'blog/detail.html', context={'post': post})

def fullWidthDetial(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body, 
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc'
                                  ])
    return render(request, 'blog/full-width-detail.html', context={'post': post})

def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def tag(request, pk):
    tg = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tg).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
#endregion

#for View, model -> DB model, template_name -> render this template, context_object_name -> parameters passed in
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5
    def get_queryset(self):
        return super().get_queryset().order_by('-created_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('paginator')
        paginator_data = pagination_data(paginator, page, is_paginated)
        context.update(paginator_data)
        return context

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate).order_by('-created_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('paginator')
        paginator_data = pagination_data(paginator, page, is_paginated)
        context.update(paginator_data)
        return context

class ArchiveView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5
    def get_queryset(self):
        return super().get_queryset().filter(created_time__month=self.kwargs.get('month'),
                                             created_time__year=self.kwargs.get('year')
                                             ).order_by('-created_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('paginator')
        paginator_data = pagination_data(paginator, page, is_paginated)
        context.update(paginator_data)
        return context

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5
    def get_queryset(self):
        tg = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tg).order_by('-created_time')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('paginator')
        paginator_data = pagination_data(paginator, page, is_paginated)
        context.update(paginator_data)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        #set self.object = get_object()
        response = super().get(request, *args, **kwargs)
        return response

    def get_object(self, queryset=None):
        # in get(), called self.object = get_object()
        # in get_object(), called filter(pk=pk)
        # go read source code
        md = markdown.Markdown(extensions=[
                                  'markdown.extensions.extra',
                                  'markdown.extensions.codehilite',
                                  'markdown.extensions.toc'
                              ])
        post = super().get_object(queryset=None)
        post.increase_views()
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.exclude(pk__in = CommentExtension.objects.values_list('comment__pk', flat=True))\
                        .order_by('-created_time')
        comment_descendant_lst = CommentExtension.objects.filter(comment__post=self.object).order_by('-comment__created_time')
        comment_descendant_dic = {}

        md = markdown.Markdown(extensions=[
                                  'markdown.extensions.extra',
                                  'markdown.extensions.codehilite',
                                  'markdown.extensions.toc'
                              ])
        for item in comment_list:
            item.text = md.convert(item.text)
        
        #paginator
        paginator = Paginator(comment_list, 10)
        page = self.request.GET.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        is_paginated = paginator.num_pages > 1

        for item in comment_descendant_lst:
            item.comment.text = md.convert(item.comment.text)
            if item.under.pk in comment_descendant_dic:
                comment_descendant_dic[item.under.pk].append(item)
            else:
                comment_descendant_dic[item.under.pk] = [item]

        context.update({
            'form':form,
            'comment_list':comments,
            'comment_descendant_dic':comment_descendant_dic,
            'page_obj':comments,
            'is_paginated':is_paginated,
            'paginator': paginator
        })
        return context

#region helper functions
def pagination_data(paginator, page, is_paginated):
    if not is_paginated:
        return {}
    
    left = []
    right = []

    #whether display '...' #1 ... 2 3 4 ... 5 not allowed
    left_has_more = False
    right_has_more = False

    #whether display 1st or last page. If left/right already contains first/last, do not display it again
    first = False
    last = False

    # The NO user requested
    page_number = page.number
    # NO of pages after division
    total_pages = paginator.num_pages
    # get page index list like [1, 2, 3, 4] total 4 pages
    page_range = paginator.page_range

    right = page_range[page_number:page_number+2]
    left = page_range[page_number-3 if page_number-3 > 0 else 0: 
                      page_number-1 if page_number-1 > 0 else 0]

    if len(right) != 0:
        if right[-1] < total_pages:
            last = True
        if right[-1] < total_pages - 1:
            right_has_more = True
    if len(left) != 0:
        if left[0] > 1:
            first = True
        if left[0] > 2:
            left_has_more = True
    data = {'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last}
    return data
#endregion