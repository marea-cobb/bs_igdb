from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.views.generic import View, ListView
from bs_igdbview.models import *
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger


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
    return render_to_response('bs_igdb/result_list.html', {"results": results})


def junction(request):
    junction_list = JunctionSummary.objects.all()
    paginatior = Paginator(junction_list, 25)
    page = request.GET.get('page')
    try:
        junctions = paginatior.page(page)
    except PageNotAnInteger:
        junctions = paginatior.page(1)
    except EmptyPage:
        contacts = paginatior.page(paginatior.num_pages)
    return render_to_response('bs_igdb/junction_list.html', {"junctions": junctions})


def summary(request):
    order_by = request.GET.get('order_by', 'summary_id')
    summary_list = IgBlastSummary.objects.all().order_by(order_by)
    paginatior = Paginator(summary_list, 25)
    page = request.GET.get('page')
    try:
        summaries = paginatior.page(page)
    except PageNotAnInteger:
        summaries = paginatior.page(1)
    except EmptyPage:
        contacts = paginatior.page(paginatior.num_pages)
    return render_to_response('bs_igdb/summary_list.html', {"summaries": summaries})


def sequence(request):
    sequence_list = Sequence.objects.all()
    paginatior = Paginator(sequence_list, 25)
    page = request.GET.get('page')
    try:
        sequences = paginatior.page(page)
    except PageNotAnInteger:
        sequences = paginatior.page(1)
    except EmptyPage:
        contacts = paginatior.page(paginatior.num_pages)
    return render_to_response('bs_igdb/sequence_list.html', {"sequences": sequences})


def alignment(request):
    alignment_list = AlignmentSummary.objects.all()
    paginatior = Paginator(alignment_list, 25)
    page = request.GET.get('page')
    order_by = request.GET.get('order_by', 'defaultOrderField')
    AlignmentSummary.objects.all().order_by(order_by)
    try:
        alignments = paginatior.page(page)
    except PageNotAnInteger:
        alignments = paginatior.page(1)
    except EmptyPage:
        contacts = paginatior.page(paginatior.num_pages)
    return render_to_response('bs_igdb/alignment_list.html', {"alignments": alignments})




def getSequenceByName(request, sequence_name):
    for seq in sequence_name:
        resultobj = Sequence.objects.filter(sequence_name=seq)
        resid=resultobj[0].result_id
        return resid





class Manager(object):

    def get_query_set(self):
        return QuerySet(self.model, using=self._db)

    def all(self):
        return self.get_query_set()

    def count(self):
        return self.get_query_set().count()

    def filter(self, *args, **kwargs):
        return self.get_query_set().filter(*args, **kwargs)



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


    # return HttpResponse(template.render(c))