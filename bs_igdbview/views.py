from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.db.models.query import QuerySet
from django.views.generic import View, ListView, DetailView
from django.views.generic.list import ListView
from bs_igdbview.models import *
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from utils import build_orderby_urls, integer_filters
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


# Basic table views
#----------------------------------------------------------------------------------------------------
def result(request):
    order_by = request.GET.get('order_by', 'result_id')
    result_list = IgBlastResult.objects.all().order_by(order_by)
    paginator = Paginator(result_list, 25)

    page = request.GET.get('page')

    # Calls utils method to append new filters or order_by to the current url
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


def junction(request):
    order_by = request.GET.get('order_by', 'junction_id')
    junction_list = JunctionSummary.objects.all().order_by(order_by)
    paginator = Paginator(junction_list, 25)
    page = request.GET.get('page')

    # Calls utils method to append new filters or order_by to the current url
    filter_urls = build_orderby_urls(request.get_full_path(), ["v_end", "vd_junction", "d_region", "dj_junction",
                                                               "j_start"])
    try:
        junctions = paginator.page(page)
    except PageNotAnInteger:
        junctions = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/junction_list.html', {"junctions": junctions, "filter_urls": filter_urls})


def summary(request):
    order_by = request.GET.get('order_by', 'summary_id')
    summary_list = IgBlastSummary.objects.all().order_by(order_by)
    paginator = Paginator(summary_list, 25)
    page = request.GET.get('page')

    # Calls utils method to append new filters or order_by to the current url
    filter_urls = build_orderby_urls(request.get_full_path(), ["v_match", "d_match", "j_match", "chain_type",
                                                               "stop_codon", "vj_frame", "productive", "strand"])
    try:
        summaries = paginator.page(page)
    except PageNotAnInteger:
        summaries = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/summary_list.html', {"summaries": summaries, "filter_urls": filter_urls})


def sequence(request):
    order_by = request.GET.get('order_by', 'sequence_id')
    sequence_list = Sequence.objects.all().order_by(order_by)
    paginator = Paginator(sequence_list, 25)
    page = request.GET.get('page')

    # Calls utils method to append new filters or order_by to the current url
    filter_urls = build_orderby_urls(request.get_full_path(), ["sequence_id", "sequence_name", "sequence", "sequence_type",
                                                               "size"])
    try:
        sequences = paginator.page(page)
    except PageNotAnInteger:
        sequences = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/sequence_list.html', {"sequences": sequences, "filter_urls": filter_urls})


def alignment(request):
    order_by = request.GET.get('order_by', 'alignment_id')
    alignment_list = AlignmentSummary.objects.all().order_by(order_by)
    paginator = Paginator(alignment_list, 25)
    page = request.GET.get('page')

    # Calls utils method to append new filters or order_by to the current url
    filter_urls = build_orderby_urls(request.get_full_path(), ["alignment_id", "v_gene", "start_position",
                                                               "stop_position", "length", "matches", "mismatches",
                                                               "gaps", "percent_identity", "translation_query"])
    try:
        alignments = paginator.page(page)
    except PageNotAnInteger:
        alignments = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/alignment_list.html', {"alignments": alignments, "filter_urls": filter_urls})


# Filter functions
#-----------------------------------------------------------------------------------------------------
def result_filter(request):
    selection = request.GET.get('att')
    filter_on = request.GET.get('s')
    check = request.GET.get('check')
    if check == "on":
        if selection == 'DB Queried':
            result_list = IgBlastResult.objects.all().filter(db_queried__regex=filter_on)
        elif selection == 'Query':
            result_list = IgBlastResult.objects.all().filter(query__regex=filter_on)
        elif selection == 'Length':
            lengths = integer_filters(IgBlastResult.objects.values_list('length'), filter_on, selection)
            result_list = IgBlastResult.objects.filter(length__in=lengths)
        elif selection == 'Summary ID':
            summaries = integer_filters(IgBlastResult.objects.values_list('igblast_summary_id'), filter_on, selection)
            result_list = IgBlastResult.objects.filter(igblast_summary_id__in=summaries)
        elif selection == 'Junction ID':
            junctions = integer_filters(IgBlastResult.objects.values_list('junction_summary_id'), filter_on, selection)
            result_list = IgBlastResult.objects.filter(junctin_summary_id__in=junctions)
        elif selection == 'Alignment ID':
            alignments = integer_filters(IgBlastResult.objects.values_list('alignment_summary_id'), filter_on, selection)
            result_list = IgBlastResult.objects.filter(alignment_summary_id__in=alignments)
        elif selection == 'Sequence ID':
            sequences = integer_filters(IgBlastResult.objects.values_list('sequence_id'), filter_on, selection)
            result_list = IgBlastResult.objects.filter(sequence_id__in=sequences)
        else:
            result_list = IgBlastResult.objects.all()
    else:
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
        else:
            result_list = IgBlastResult.objects.all()

    order_by = request.GET.get('order_by', 'result_id')
    result_list = result_list.order_by(order_by)
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
    check = request.GET.get('check')
    if check == "on":
        if selection == 'V Match':
            summary_list = IgBlastSummary.objects.all().filter(v_match__regex=filter_on)
        elif selection == 'D Match':
            summary_list = IgBlastSummary.objects.all().filter(d_match__regex=filter_on)
        elif selection == 'J Match':
            summary_list = IgBlastSummary.objects.all().filter(j_match__regex=filter_on)
        elif selection == 'Chain Type':
            summary_list = IgBlastSummary.objects.all().filter(chain_type__regex=filter_on)
        elif selection == 'Stop Codon':
            summary_list = IgBlastSummary.objects.all().filter(stop_codon__regex=filter_on)
        elif selection == 'V-J Frame':
            summary_list = IgBlastSummary.objects.all().filter(vj_frame__regex=filter_on)
        elif selection == 'Productive':
            summary_list = IgBlastSummary.objects.all().filter(productive__regex=filter_on)
        elif selection == 'Strand':
            summary_list = IgBlastSummary.objects.all().filter(strand__regex=filter_on)
        else:
            summary_list = IgBlastSummary.objects.all()
    else:
        if selection == 'V Match':
            summary_list = IgBlastSummary.objects.all().filter(v_match=filter_on)
        elif selection == 'D Match':
            summary_list = IgBlastSummary.objects.all().filter(d_match=filter_on)
        elif selection == 'J Match':
            summary_list = IgBlastSummary.objects.all().filter(j_match=filter_on)
        elif selection == 'Chain Type':
            summary_list = IgBlastSummary.objects.all().filter(chain_type=filter_on)
        elif selection == 'Stop Codon':
            summary_list = IgBlastSummary.objects.all().filter(stop_codon=filter_on)
        elif selection == 'V-J Frame':
            summary_list = IgBlastSummary.objects.all().filter(vj_frame=filter_on)
        elif selection == 'Productive':
            summary_list = IgBlastSummary.objects.all().filter(productive=filter_on)
        elif selection == 'Strand':
            summary_list = IgBlastSummary.objects.all().filter(strand=filter_on)
        else:
            summary_list = IgBlastSummary.objects.all()
    
    order_by = request.GET.get('order_by', 'summary_id')
    summary_list = summary_list.order_by(order_by)
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
    check = request.GET.get('check')
    if check == "on":
        if selection == 'V End':
            junction_list = JunctionSummary.objects.all().filter(v_end__regex=filter_on)
        elif selection == 'VD Region':
            junction_list = JunctionSummary.objects.all().filter(vd_junction__regex=filter_on)
        elif selection == 'D Region':
            junction_list = JunctionSummary.objects.all().filter(d_region__regex=filter_on)
        elif selection == 'DJ Junction':
            junction_list = JunctionSummary.objects.all().filter(dj_junction__regex=filter_on)
        elif selection == 'J Start':
            junction_list = JunctionSummary.objects.all().filter(j_start__regex=filter_on)
        else:
            junction_list = JunctionSummary.objects.all()
    else:
        if selection == 'V End':
            junction_list = JunctionSummary.objects.all().filter(v_end=filter_on)
        elif selection == 'VD Region':
            junction_list = JunctionSummary.objects.all().filter(vd_junction=filter_on)
        elif selection == 'D Region':
            junction_list = JunctionSummary.objects.all().filter(d_region=filter_on)
        elif selection == 'DJ Junction':
            junction_list = JunctionSummary.objects.all().filter(dj_junction=filter_on)
        elif selection == 'J Start':
            junction_list = JunctionSummary.objects.all().filter(j_start=filter_on)
        else:
            junction_list = JunctionSummary.objects.all()

    order_by = request.GET.get('order_by', 'junction_id')
    junction_list = junction_list.order_by(order_by)
    filter_urls = build_orderby_urls(request.get_full_path(), ["v_end", "vd_junction", "d_region", "dj_junction",
                                                               "j_start"])
    paginator = Paginator(junction_list, 25)
    page = request.GET.get('page')

    try:
        junctions = paginator.page(page)
    except PageNotAnInteger:
        junctions = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/junction_list.html', {"junctions": junctions, "filter_urls": filter_urls})


def sequence_filter(request):
    selection = request.GET.get('att')
    filter_on = request.GET.get('s')
    check = request.GET.get('check')
    if check == "on":
        if selection == 'Sequence Id':
            sequence_list = Sequence.objects.all().filter(sequence_id__regex=filter_on)
        elif selection == 'Sequence Name':
            sequence_list = Sequence.objects.all().filter(sequence_name__regex=filter_on)
        elif selection == 'Sequence':
            sequence_list = Sequence.objects.all().filter(fasta_sequence__regex=filter_on)
        elif selection == 'Sequence Type':
            sequence_list = Sequence.objects.all().filter(sequence_type__regex=filter_on)
        elif selection == 'Size':
            sizes = integer_filters(Sequence.objects.values_list('size'), filter_on, selection)
            sequence_list = Sequence.objects.filter(size__in=sizes)
        else:
            sequence_list = Sequence.objects.all()
    else:
        if selection == 'Sequence Id':
            sequence_list = Sequence.objects.all().filter(sequence_id=filter_on)
        elif selection == 'Sequence Name':
            sequence_list = Sequence.objects.all().filter(sequence_name=filter_on)
        elif selection == 'Sequence':
            sequence_list = Sequence.objects.all().filter(fasta_sequence=filter_on)
        elif selection == 'Sequence Type':
            sequence_list = Sequence.objects.all().filter(sequence_type=filter_on)
        elif selection == 'Size':
            sequence_list = Sequence.objects.all().filter(size=filter_on)
        else:
            sequence_list = Sequence.objects.all()

    filter_urls = build_orderby_urls(request.get_full_path(), ["sequence_id", "sequence_name", "sequence", "sequence_type",
                                                               "size"])
    order_by = request.GET.get('order_by', 'sequence_id')
    sequence_list = sequence_list.order_by(order_by)
    paginator = Paginator(sequence_list, 25)
    page = request.GET.get('page')

    try:
        sequences = paginator.page(page)
    except PageNotAnInteger:
        sequences = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('bs_igdb/sequence_list.html', {"sequences": sequences, "filter_urls": filter_urls})


def alignment_filter(request):
    selection = request.GET.get('att')
    filter_on = request.GET.get('s')
    check = request.GET.get('check')
    if check == "on":
        if selection == 'Start Position':
            starts = integer_filters(AlignmentSummary.objects.values_list('start_position'), filter_on, selection)
            alignment_list = AlignmentSummary.objects.filter(start_position__in=starts)
        elif selection == 'Stop Position':
            stops = integer_filters(AlignmentSummary.objects.values_list('stop_position'), filter_on, selection)
            alignment_list = AlignmentSummary.objects.filter(stop_position__in=stops)
        elif selection == 'Length':
            lengths = integer_filters(AlignmentSummary.objects.values_list('length'), filter_on, selection)
            alignment_list = AlignmentSummary.objects.filter(lengths__in=lengths)
        elif selection == 'Matches':
            alignment_list = AlignmentSummary.objects.all().filter(matches__regex=filter_on)
        elif selection == 'Mismatches':
            alignment_list = AlignmentSummary.objects.all().filter(mismatches__regex=filter_on)
        elif selection == 'Gaps':
            alignment_list = AlignmentSummary.objects.all().filter(gaps__regex=filter_on)
        elif selection == 'Percent Identity':
            percents = integer_filters(AlignmentSummary.objects.values_list('percent_identity'), filter_on, selection)
            alignment_list = AlignmentSummary.objects.filter(percent_identity__in=percents)
        elif selection == 'Translation Query':
            alignment_list = AlignmentSummary.objects.all().filter(translation_query__regex=filter_on)
        else:
            alignment_list = AlignmentSummary.objects.all()
    else:
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
        else:
            alignment_list = AlignmentSummary.objects.all()

    order_by = request.GET.get('order_by', 'alignment_id')
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


# -----------------------------------------------------------------------------------------------------

def search(request):
    return render_to_response('bs_igdb/search.html')



    # def full_search(request):
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
    #     return render_to_response('bs_igdb/full_search.html', {"results": results})

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
