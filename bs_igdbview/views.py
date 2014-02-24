from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.db.models.query import QuerySet
from django.views.generic import View, ListView, DetailView
from django.views.generic.list import ListView
from bs_igdbview.models import *
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
import re


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
    order_by = request.GET.get('order_by', 'result_id')
    result_list = IgBlastResult.objects.all().order_by(order_by)
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
    order_by = request.GET.get('order_by', 'junction_id')
    junction_list = JunctionSummary.objects.all().order_by(order_by)
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
    order_by = request.GET.get('order_by', 'sequence_id')
    sequence_list = Sequence.objects.all().order_by(order_by)
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
    order_by = request.GET.get('order_by', 'alignment_id')
    alignment_list = AlignmentSummary.objects.all().order_by(order_by)
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


# Filter functions
#-----------------------------------------------------------------------------------------------------

def summary_filter(request):
    selection = request.GET.get('att')
    filter_on = request.GET.get('s')
    if selection == 'V+Match':
        summary_list = IgBlastSummary.objects.all().filter(v_match=filter_on)
    elif selection == 'D+Match':
        summary_list = IgBlastSummary.objects.all().filter(d_match=filter_on)
    elif selection == 'J+Match':
        summary_list = IgBlastSummary.objects.all().filter(j_match=filter_on)
    elif selection == 'Chain+Type':
        summary_list = IgBlastSummary.objects.all().filter(chain_type=filter_on)
    elif selection == 'Stop+Codon':
        summary_list = IgBlastSummary.objects.all().filter(stop_codon=filter_on)
    elif selection == 'V-J+Frame':
        summary_list = IgBlastSummary.objects.all().filter(vj_frame=filter_on)
    elif selection == 'Productive':
        summary_list = IgBlastSummary.objects.all().filter(productive=filter_on)
    elif selection == 'Strand':
        summary_list = IgBlastSummary.objects.all().filter(strand=filter_on)

    paginatior = Paginator(summary_list, 25)
    page = request.GET.get('page')
    order_by = request.GET.get('order_by', 'defaultOrderField')
    IgBlastSummary.objects.all().order_by(order_by)
    try:
        summaries = paginatior.page(page)
    except PageNotAnInteger:
        summaries = paginatior.page(1)
    except EmptyPage:
        contacts = paginatior.page(paginatior.num_pages)
    return render_to_response('bs_igdb/summary_list.html', {"summaries": summaries})


def result_filter(request):
    selection = request.GET.get('att')
    filter_on = request.GET.get('s')
    if selection == 'DB+Queried':
        result_list = IgBlastResult.objects.all().filter(db_queried=filter_on)
    elif selection == 'Query':
        result_list = IgBlastResult.objects.all().filter(query=filter_on)
    elif selection == 'Length':
        result_list = IgBlastResult.objects.all().filter(length=filter_on)
    elif selection == 'Summary+ID':
        result_list = IgBlastResult.objects.all().filter(igblast_summary_id=filter_on)
    elif selection == 'Junction+ID':
        result_list = IgBlastResult.objects.all().filter(junction_summary_id=filter_on)
    elif selection == 'Alignment+ID':
        result_list = IgBlastResult.objects.all().filter(alignment_summary_id=filter_on)
    elif selection == 'Sequence+ID':
        result_list = IgBlastResult.objects.all().filter(sequence_id=filter_on)

    paginatior = Paginator(result_list, 25)
    page = request.GET.get('page')
    order_by = request.GET.get('order_by', 'defaultOrderField')
    IgBlastSummary.objects.all().order_by(order_by)
    try:
        results = paginatior.page(page)
    except PageNotAnInteger:
        results = paginatior.page(1)
    except EmptyPage:
        contacts = paginatior.page(paginatior.num_pages)
    return render_to_response('bs_igdb/result_list.html', {"results": results})


def alignment_filter(request):
    selection = request.GET.get('att')
    filter_on = request.GET.get('s')
    if selection == 'V Gene':
        alignment_list = AlignmentSummary.objects.all().filter(v_gene=filter_on)
    elif selection == 'Start Position':
        alignment_list = AlignmentSummary.objects.all().filter(start_position=filter_on)
    elif selection == 'Stop Position':
        alignment_list = AlignmentSummary.objects.all().filter(stop_position=filter_on)
    elif selection == 'Length':
        alignment_list = AlignmentSummary.objects.all().filter(length=filter_on)
    elif selection == 'Matches':
        alignment_list = AlignmentSummary.objects.all().filter(matches=filter_on)
    elif selection == 'Mismatches':
        alignment_list = AlignmentSummary.objects.all().filter(mismatches=filter_on)
    elif selection == 'Gaps':
        alignment_list = AlignmentSummary.objects.all().filter(gaps=filter_on)
    elif selection == 'Percent Identity':
        alignment_list = AlignmentSummary.objects.all().filter(percent_identity=filter_on)
    elif selection == 'Translation Query':
        alignment_list = AlignmentSummary.objects.all().filter(translation_query=filter_on)

    paginatior = Paginator(alignment_list, 25)
    page = request.GET.get('page')
    order_by = request.GET.get('order_by', 'defaultOrderField')
    IgBlastSummary.objects.all().order_by(order_by)
    try:
        alignments = paginatior.page(page)
    except PageNotAnInteger:
        alignments = paginatior.page(1)
    except EmptyPage:
        contacts = paginatior.page(paginatior.num_pages)
    return render_to_response('bs_igdb/alignment_list.html', {"alignments": alignments})


def alignment_filter2(request):
    selection = request.GET.get('att')
    filter_on = request.GET.get('s')
    if selection == 'V Gene':
        alignment_list = AlignmentSummary.objects.all().filter(v_gene=filter_on)
    elif selection == 'Start Position':
        alignment_list = AlignmentSummary.objects.all().filter(start_position=filter_on)
    elif selection == 'Stop Position':
        alignment_list = AlignmentSummary.objects.all().filter(stop_position=filter_on)
    elif selection == 'Length':
        alignment_list = AlignmentSummary.objects.all().filter(length=filter_on)
    elif selection == 'Matches':
        alignment_list = AlignmentSummary.objects.all().filter(matches=filter_on)
    elif selection == 'Mismatches':
        alignment_list = AlignmentSummary.objects.all().filter(mismatches=filter_on)
    elif selection == 'Gaps':
        alignment_list = AlignmentSummary.objects.all().filter(gaps=filter_on)
    elif selection == 'Percent Identity':
        alignment_list = AlignmentSummary.objects.all().filter(percent_identity=filter_on)
    elif selection == 'Translation Query':
        alignment_list = AlignmentSummary.objects.all().filter(translation_query__icontains=filter_on)
        # alignment_list = AlignmentSummary.objects.all().extra(where=["translation_query LIKE %s"], params=[filter_on])

                                                                     # 'SUBSTRING(translation_query,1,1)="%s"' % filter_on])
        # extra(where["%s LIKE CONCAT ('%%', translation_query, '%%')"], params=filter_on])

            # translation_query=filter_on)
    paginatior = Paginator(alignment_list, 25)
    page = request.GET.get('page')
    order_by = request.GET.get('order_by', 'defaultOrderField')
    IgBlastSummary.objects.all().order_by(order_by)
    try:
        alignments = paginatior.page(page)
    except PageNotAnInteger:
        alignments = paginatior.page(1)
    except EmptyPage:
        contacts = paginatior.page(paginatior.num_pages)
    return render_to_response('bs_igdb/alignment_list.html', {"alignments": alignments})


#-----------------------------------------------------------------------------------------------------

def full_search(request):
    try:
        results = paginatior.page(page)
    except PageNotAnInteger:
        results = paginatior.page(1)
    except EmptyPage:
        contacts = paginatior.page(paginatior.num_pages)
    return render_to_response('bs_igdb/full_search.html', {"results": results})




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

