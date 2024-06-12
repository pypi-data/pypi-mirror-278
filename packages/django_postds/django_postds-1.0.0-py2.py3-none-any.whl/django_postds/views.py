from django.shortcuts import render, get_object_or_404
from _data import postds

from django_postds.models import Portfolio, BlogPost
from django.views import generic
from hitcount.views import HitCountDetailView

from .forms import SearchForm

num_pagination = 6

c = postds.context


def portfolio_details(request, id: int):
    c.update({
        "obj": get_object_or_404(Portfolio, pk=id),
        "breadcrumb": {
            "title": c['portfolio']['title'],
        },
    })
    return render(request, c["template_name"] + '/' + c['filenames']['portfolio_details'], c)


class BlogListView(generic.ListView):
    template_name = c["template_name"] + '/' + c['filenames']['blog']
    paginate_by = num_pagination

    def get_queryset(self):
        # https://stackoverflow.com/questions/56067365/how-to-filter-posts-by-tags-using-django-taggit-in-django
        return BlogPost.objects.filter(status=1).order_by('-updated_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(c)
        context.update({
            "breadcrumb": {
                "title": "Blog",
            },
        })
        return context


class BlogCategoryListView(generic.ListView):
    template_name = c["template_name"] + '/' + c['filenames']['blog']
    paginate_by = num_pagination

    def get_queryset(self):
        return BlogPost.objects.filter(status=1).filter(category__filter=self.kwargs['category_filter']).order_by('-updated_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(c)
        context.update({
            "breadcrumb": {
                "title": "Category: " + self.kwargs['category_filter'],
            },
        })
        return context


class BlogDetailView(HitCountDetailView):
    model = BlogPost
    template_name = c["template_name"] + '/' + postds.context['filenames']['blog_details']
    context_object_name = 'object'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(c)
        context.update(
            {
                'breadcrumb': {
                    'title': 'Blog Detail'
                },
            }
        )
        return context


def make_page_bundle(page_range, n=5):
    # 전체 페이지를 n 개수의 묶음으로 만든다.
    # pagination에 사용
    l = [i for i in page_range]
    return [l[i:i + n] for i in range(0, len(l), n)]


class BlogSearchWordListView(generic.ListView):
    template_name = c["template_name"] + '/' + c['filenames']['blog']
    paginate_by = num_pagination

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
        else:
            q = ''
        return BlogPost.objects.filter(content__contains='' if q is None else q).filter(status=1).order_by(
            '-updated_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pages_devided = make_page_bundle(context['paginator'].page_range)

        # 현재 페이지에 해당하는 묶음을 page_bundle로 전달한다.
        for page_bundle in pages_devided:
            if context['page_obj'].number in page_bundle:
                context['page_bundle'] = page_bundle

        context.update(c)
        return context


class BlogTagListView(generic.ListView):
    template_name = c["template_name"] + '/' + c['filenames']['blog']
    paginate_by = num_pagination

    def get_queryset(self):
        # https://stackoverflow.com/questions/56067365/how-to-filter-posts-by-tags-using-django-taggit-in-django
        return BlogPost.objects.filter(tags__name__in=[self.kwargs['tag']]).filter(status=1).order_by('-updated_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(c)
        context.update({
            "breadcrumb": {
                "title": "Tag: " + self.kwargs['tag'],
            },
        })
        return context


