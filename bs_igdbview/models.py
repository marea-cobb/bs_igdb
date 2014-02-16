#!/usr/bin/python

#testing testing 1 2 3...


from django.db import models


#-------------------------------------------------------------------------------------------------
class Organism(models.Model):
    organism_id = models.AutoField(primary_key=True)
    organismcode = models.CharField(unique=True, max_length=10)
    genus = models.CharField(max_length=45)
    species = models.CharField(max_length=45)
    strain = models.CharField(max_length=45)
    isolate = models.CharField(max_length=45)
    source = models.CharField(max_length=100)

    # def __unicode__(self):
    # return str(self.organismcode)


class TimePoint(models.Model):
    time_point_id = models.AutoField(primary_key=True)
    time_code = models.TextField()


class Donor(models.Model):
    donor_id = models.AutoField(primary_key=True)
    organism = models.ForeignKey(Organism)
    animal = models.IntegerField()


class Immunogen(models.Model):
    immunogen_id = models.AutoField(primary_key=True)
    immunogen_code = models.TextField()


class CellType(models.Model):
    celltype_id = models.AutoField(primary_key=True)
    celltype = models.TextField()


class Sequence(models.Model):
    sequence_id = models.AutoField(primary_key=True)
    sequence_name = models.TextField()
    fasta_sequence = models.TextField()
    fasta_type = models.TextField()
    size = models.IntegerField()


class Sample(models.Model):
    sample_id = models.AutoField(primary_key=True)
    donor = models.ForeignKey(Donor)
    timepoint = models.ForeignKey(TimePoint)
    sample_step = models.IntegerField()
    immunogen = models.ForeignKey(Immunogen)
    organism = models.ForeignKey(Organism)
    cell_type = models.ForeignKey(CellType)
    sequence = models.ForeignKey(Sequence)


class AlignmentSummary(models.Model):
    alignment_id = models.AutoField(primary_key=True)
    v_gene = models.TextField()
    start_position = models.IntegerField()
    stop_position = models.IntegerField()
    length = models.IntegerField()
    matches = models.TextField()
    mismatches = models.TextField()
    gaps = models.TextField()
    percent_identity = models.DecimalField(max_digits=5, decimal_places=2)
    translation_query = models.TextField()


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    designation = models.CharField(unique=True, max_length=5)
    email = models.EmailField(unique=True)


class ClusterType(models.Model):
    cluster_type_id = models.AutoField(primary_key=True)
    cluster_algorithm = models.TextField()


class Cluster(models.Model):
    cluster_id = models.AutoField(primary_key=True)
    cluster_name = models.TextField()
    cluster_size = models.IntegerField()
    collapse = models.ForeignKey(Sequence)
    cluster_type = models.ForeignKey(ClusterType)


class IgBlastSummary(models.Model):
    summary_id = models.AutoField(primary_key=True)
    v_match = models.TextField()
    d_match = models.TextField()
    j_match = models.TextField()
    chain_type = models.TextField()
    stop_codon = models.TextField()
    vj_frame = models.TextField()
    productive = models.TextField()
    strand = models.TextField()


class JunctionSummary(models.Model):
    junction_id = models.AutoField(primary_key=True)
    v_end = models.TextField()
    vd_junction = models.TextField()
    d_region = models.TextField()
    dj_junction = models.TextField()
    j_start = models.TextField()


class IgBlastResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    db_queried = models.TextField()
    query = models.TextField()
    length = models.IntegerField()
    igblast_summary = models.ForeignKey(IgBlastSummary)
    junction_summary = models.ForeignKey(JunctionSummary)
    alignment_summary = models.ForeignKey(AlignmentSummary)
    sequence = models.ForeignKey(Sequence)

    def __unicode__(self):
        return self.query

class Library(models.Model):
    library_id = models.AutoField(primary_key=True)
    librarycode = models.CharField(unique=True, max_length=25, db_index=True)
    author = models.ForeignKey(Author)
    organism = models.ForeignKey(Organism)
    #lifestage = models.ForeignKey(Lifestage)
    #phenotype = models.ForeignKey(Phenotype)
    #collaborator = models.ForeignKey(Collaborator)
    #librarytype = models.ForeignKey(Librarytype)
    #protocol = models.ForeignKey(Protocol)
    # seqtech = models.ForeignKey(Seqtech)
    fastqname = models.CharField(max_length=1000)
    fastqalias = models.CharField(max_length=1000)
    librarysize = models.IntegerField()
    flowcell = models.CharField(max_length=45)
    downloaddate = models.DateField()
    notes = models.CharField(max_length=400)
    fastqpath = models.CharField(max_length=1025)

    # def __unicode__(self):
    # return str(self.librarycode)