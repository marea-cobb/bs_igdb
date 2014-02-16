from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from bs_igdbview.models import *

from django import forms
from django.forms.models import BaseInlineFormSet
from django.db import models


#-------------------------------------------------------------------------------------------------
class OrganismAdmin(admin.ModelAdmin):
    list_display = ('organism_id', 'organismcode', 'genus', 'species', 'strain', 'isolate', 'source')
admin.site.register(Organism, OrganismAdmin)


class TimePointAdmin(admin.ModelAdmin):
    list_display = ('time_point_id', 'time_code')
admin.site.register(TimePoint, TimePointAdmin)


class DonorAdmin(admin.ModelAdmin):
    list_display = ('donor_id', 'organism', 'animal')
admin.site.register(Donor, DonorAdmin)


class ImmunogenAdmin(admin.ModelAdmin):
    list_display = ('immunogen_id', 'immunogen_code')
admin.site.register(Immunogen, ImmunogenAdmin)


class CellTypeAdmin(admin.ModelAdmin):
    list_display = ('celltype_id', 'celltype')
admin.site.register(CellType, CellTypeAdmin)


class SampleAdmin(admin.ModelAdmin):
    list_display = ('sample_id', 'donor', 'timepoint', 'sample_step', 'immunogen', 'organism', 'cell_type', 'sequence')
admin.site.register(Sample, SampleAdmin)


class SequenceAdmin(admin.ModelAdmin):
    list_display = ('sequence_id', 'sequence_name', 'fasta_sequence', 'fasta_type', 'size')
admin.site.register(Sequence, SequenceAdmin)


class AlignmentSummaryAdmin(admin.ModelAdmin):
    list_display = ('alignment_id', 'start_position', 'stop_position', 'length', 'matches', 'mismatches', 'gaps', 'percent_identity', 'translation_query')
admin.site.register(AlignmentSummary, AlignmentSummaryAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_id', 'firstname', 'lastname', 'designation', 'email')
admin.site.register(Author, AuthorAdmin)


class IgBlastSummaryAdmin(admin.ModelAdmin):
    list_display = ('summary_id', 'v_match', 'd_match', 'j_match', 'chain_type', 'stop_codon', 'vj_frame', 'productive', 'strand')
admin.site.register(IgBlastSummary, IgBlastSummaryAdmin)


class JunctionSummaryAdmin(admin.ModelAdmin):
    list_display = ('junction_id', 'v_end', 'vd_junction', 'd_region', 'dj_junction', 'j_start')
admin.site.register(JunctionSummary, JunctionSummaryAdmin)


class IgBlastResultAdmin(admin.ModelAdmin):
    list_display = ('result_id', 'db_queried', 'query', 'length', 'igblast_summary', 'junction_summary', 'alignment_summary', 'sequence')
admin.site.register(IgBlastResult, IgBlastResultAdmin)


class LibraryAdmin(admin.ModelAdmin):
    list_display = ('library_id', 'librarycode', 'author', 'organism', 'fastqname', 'fastqalias', 'librarysize', 'flowcell', 'downloaddate', 'notes', 'fastqpath')
admin.site.register(Library, LibraryAdmin)