from django.http import HttpResponse
from django.views.generic import View, ListView
from bs_igdbview.models import *
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# class Dashboard(View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse()
#
#
# class ListLibraryView(ListView):
#     model = Library
#     template_name = 'bs_igdb/library_list.html'


def index(request):
    result_list = IgBlastResult.objects.all()
    template_name = 'bs_igdb/index.html'
    template = loader.get_template(template_name)
    c = Context({
        'result_list': result_list,
    })
    return HttpResponse(template.render(c))


def dashboard(request):
    result_list = IgBlastResult.objects.all()
    template_name = 'bs_igdb/dashboard.html'
    template = loader.get_template(template_name)
    c = Context({
        'result_list': result_list,
    })
    return HttpResponse(template.render(c))


def result(request):
    result_list = IgBlastResult.objects.all()
    paginatior = Paginator(result_list, 25)

    page = request.GET.get('page')
    try:
        results = paginatior.page(page)
    except PageNotAnInteger:
        results = paginatior.page(1)
    except EmptyPage:
        contacts = paginatior.page(paginatior.num_pages)



    # try:
    #     page = int(request.GET.get('page', '1'))
    # except ValueError:
    #     page = 1
    #
    # try:
    #     results = paginatior.page(page)
    #     template_name = 'bs_igdb/result_list.html'
    #     template = loader.get_template(template_name)
    #     c = Context({
    #         'results': results,
    #     })
    # except (EmptyPage, InvalidPage):
    #     results = paginatior.page(paginatior.num_pages)

    return render_to_response('bs_igdb/result_list.html', {"results": results})

    # return HttpResponse(template.render(c))