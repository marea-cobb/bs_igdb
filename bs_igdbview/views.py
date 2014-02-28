from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.db.models.query import QuerySet
from django.views.generic import View, ListView, DetailView
from django.views.generic.list import ListView
from bs_igdbview.models import *
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from utils import build_orderby_urls
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
    paginator = Paginator(result_list, 25)

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/result_list.html', {"results": results})


def junction(request):
    order_by = request.GET.get('order_by', 'junction_id')
    junction_list = JunctionSummary.objects.all().order_by(order_by)
    paginator = Paginator(junction_list, 25)
    page = request.GET.get('page')
    try:
        junctions = paginator.page(page)
    except PageNotAnInteger:
        junctions = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/junction_list.html', {"junctions": junctions})


def summary(request):
    order_by = request.GET.get('order_by', 'summary_id')
    summary_list = IgBlastSummary.objects.all().order_by(order_by)
    paginator = Paginator(summary_list, 25)
    page = request.GET.get('page')
    try:
        summaries = paginator.page(page)
    except PageNotAnInteger:
        summaries = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/summary_list.html', {"summaries": summaries})


def sequence(request):
    order_by = request.GET.get('order_by', 'sequence_id')
    sequence_list = Sequence.objects.all().order_by(order_by)
    paginator = Paginator(sequence_list, 25)
    page = request.GET.get('page')
    try:
        sequences = paginator.page(page)
    except PageNotAnInteger:
        sequences = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/sequence_list.html', {"sequences": sequences})


def alignment(request):
    order_by = request.GET.get('order_by', 'alignment_id')
    alignment_list = AlignmentSummary.objects.all().order_by(order_by)
    paginator = Paginator(alignment_list, 25)
    page = request.GET.get('page')
    order_by = request.GET.get('order_by', 'defaultOrderField')
    AlignmentSummary.objects.all().order_by(order_by)
    try:
        alignments = paginator.page(page)
    except PageNotAnInteger:
        alignments = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/alignment_list.html', {"alignments": alignments})


# Filter functions
#-----------------------------------------------------------------------------------------------------
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

    order_by = request.GET.get('order_by', 'defaultOrderField')
    result_list = result_list.objects.all().order_by(order_by)
    paginator = Paginator(result_list, 25)
    page = request.GET.get('page')
    filter_urls = build_orderby_urls(request.get_full_path(), ["db_queried", "query", "length",
                                                               "igblast_summary_id", "junction_summary_id",
                                                               "alignment_summary_id", "sequence_id"])
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/result_list.html', {"results": results, "filter_urls": filter_urls})


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
    order_by = request.GET.get('order_by', 'defaultOrderField')
    summary_list = summary_list.objects.all().order_by(order_by)
    filter_urls = build_orderby_urls(request.get_full_path(), ["v_match", "d_match", "j_match", "chain_type",
                                                               "stop_codon", "vj_frame", "productive", "strand"])
    paginator = Paginator(summary_list, 25)
    page = request.GET.get('page')

    try:
        summaries = paginator.page(page)
    except PageNotAnInteger:
        summaries = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/summary_list.html', {"summaries": summaries, "filter_urls": filter_urls})


def junction_filter(request):
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
    order_by = request.GET.get('order_by', 'defaultOrderField')
    summary_list = summary_list.objects.all().order_by(order_by)
    filter_urls = build_orderby_urls(request.get_full_path(), ["v_match", "d_match", "j_match", "chain_type",
                                                               "stop_codon", "vj_frame", "productive", "strand"])
    paginator = Paginator(summary_list, 25)
    page = request.GET.get('page')

    try:
        summaries = paginator.page(page)
    except PageNotAnInteger:
        summaries = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/summary_list.html', {"summaries": summaries, "filter_urls": filter_urls})


# def alignment_filter(request):
#     selection = request.GET.get('att')
#     filter_on = request.GET.get('s')
#     if selection == 'V Gene':
#         alignment_list = AlignmentSummary.objects.all().filter(v_gene=filter_on)
#     elif selection == 'Start Position':
#         alignment_list = AlignmentSummary.objects.all().filter(start_position=filter_on)
#     elif selection == 'Stop Position':
#         alignment_list = AlignmentSummary.objects.all().filter(stop_position=filter_on)
#     elif selection == 'Length':
#         alignment_list = AlignmentSummary.objects.all().filter(length=filter_on)
#     elif selection == 'Matches':
#         alignment_list = AlignmentSummary.objects.all().filter(matches=filter_on)
#     elif selection == 'Mismatches':
#         alignment_list = AlignmentSummary.objects.all().filter(mismatches=filter_on)
#     elif selection == 'Gaps':
#         alignment_list = AlignmentSummary.objects.all().filter(gaps=filter_on)
#     elif selection == 'Percent Identity':
#         alignment_list = AlignmentSummary.objects.all().filter(percent_identity=filter_on)
#     elif selection == 'Translation Query':
#         alignment_list = AlignmentSummary.objects.all().filter(translation_query=filter_on)
#
#     paginator = Paginator(alignment_list, 25)
#     page = request.GET.get('page')
#     order_by = request.GET.get('order_by', 'defaultOrderField')
#     IgBlastSummary.objects.all().order_by(order_by)
#     try:
#         alignments = paginator.page(page)
#     except PageNotAnInteger:
#         alignments = paginator.page(1)
#     except EmptyPage:
#         contacts = paginator.page(paginator.num_pages)
#     return render_to_response('bs_igdb/alignment_list.html', {"alignments": alignments})


def alignment_filter2(request):
    alignment_list = AlignmentSummary.objects.all()
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

    order_by = request.GET.get('order_by', 'defaultOrderField')
    alignment_list = alignment_list.order_by(order_by)

    filter_urls = build_orderby_urls(request.get_full_path(), ["alignment_id", "v_gene", "start_position",
                                                               "stop_position", "length", "matches", "mismatches",
                                                               "gaps", "percent_identity", "translation_query"])
    paginator = Paginator(alignment_list, 25)
    page = request.GET.get('page')

    try:
        alignments = paginator.page(page)
    except PageNotAnInteger:
        alignments = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/alignment_list.html', {"alignments": alignments, "filter_urls": filter_urls})


#-----------------------------------------------------------------------------------------------------

def full_search(request):
    search_list = AlignmentSummary.objects.all()
    paginator = Paginator(search_list, 25)
    page = request.GET.get('page')
    order_by = request.GET.get('order_by', 'defaultOrderField')
    IgBlastSummary.objects.all().order_by(order_by)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/full_search.html', {"results": results})

#
# def full_search_filter(request):
#     if request.GET.getlist('att'):
#         checks = request.GET.getlist('att')
#         for each in checks:
#             print unicode(each)
#
#             # print request.GET.items()
#
#     # sum_filter = request.GET.get('sum_att')
#     # print sum_filter
#     # sum_value = request.GET.get('summary')
#     # print sum_value
#     search_list = AlignmentSummary.objects.all()
#     paginator = Paginator(search_list, 25)
#     page = request.GET.get('page')
#     order_by = request.GET.get('order_by', 'defaultOrderField')
#     IgBlastSummary.objects.all().order_by(order_by)
#     try:
#         results = paginator.page(page)
#     except PageNotAnInteger:
#         results = paginator.page(1)
#     except EmptyPage:
#         contacts = paginator.page(paginator.num_pages)
#     return render_to_response('bs_igdb/full_search_filter.html', {"results": results, "filter_urls": filter_urls})
