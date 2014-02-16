# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organism'
        db.create_table(u'bs_igdbview_organism', (
            ('organism_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organismcode', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('genus', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('species', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('strain', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('isolate', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'bs_igdbview', ['Organism'])

        # Adding model 'TimePoint'
        db.create_table(u'bs_igdbview_timepoint', (
            ('time_point_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'bs_igdbview', ['TimePoint'])

        # Adding model 'Donor'
        db.create_table(u'bs_igdbview_donor', (
            ('donor_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organism', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.Organism'])),
            ('animal', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'bs_igdbview', ['Donor'])

        # Adding model 'Immunogen'
        db.create_table(u'bs_igdbview_immunogen', (
            ('immunogen_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('immunogen_code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'bs_igdbview', ['Immunogen'])

        # Adding model 'CellType'
        db.create_table(u'bs_igdbview_celltype', (
            ('celltype_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('celltype', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'bs_igdbview', ['CellType'])

        # Adding model 'Sequence'
        db.create_table(u'bs_igdbview_sequence', (
            ('sequence_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sequence_name', self.gf('django.db.models.fields.TextField')()),
            ('fasta_sequence', self.gf('django.db.models.fields.TextField')()),
            ('fasta_type', self.gf('django.db.models.fields.TextField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'bs_igdbview', ['Sequence'])

        # Adding model 'Sample'
        db.create_table(u'bs_igdbview_sample', (
            ('sample_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('donor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.Donor'])),
            ('timepoint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.TimePoint'])),
            ('sample_step', self.gf('django.db.models.fields.IntegerField')()),
            ('immunogen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.Immunogen'])),
            ('organism', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.Organism'])),
            ('cell_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.CellType'])),
            ('sequence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.Sequence'])),
        ))
        db.send_create_signal(u'bs_igdbview', ['Sample'])

        # Adding model 'AlignmentSummary'
        db.create_table(u'bs_igdbview_alignmentsummary', (
            ('alignment_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('v_gene', self.gf('django.db.models.fields.TextField')()),
            ('start_position', self.gf('django.db.models.fields.IntegerField')()),
            ('stop_position', self.gf('django.db.models.fields.IntegerField')()),
            ('length', self.gf('django.db.models.fields.IntegerField')()),
            ('matches', self.gf('django.db.models.fields.TextField')()),
            ('mismatches', self.gf('django.db.models.fields.TextField')()),
            ('gaps', self.gf('django.db.models.fields.TextField')()),
            ('percent_identity', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('translation_query', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'bs_igdbview', ['AlignmentSummary'])

        # Adding model 'Author'
        db.create_table(u'bs_igdbview_author', (
            ('author_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('designation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
        ))
        db.send_create_signal(u'bs_igdbview', ['Author'])

        # Adding model 'ClusterType'
        db.create_table(u'bs_igdbview_clustertype', (
            ('cluster_type_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cluster_algorithm', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'bs_igdbview', ['ClusterType'])

        # Adding model 'Cluster'
        db.create_table(u'bs_igdbview_cluster', (
            ('cluster_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cluster_name', self.gf('django.db.models.fields.TextField')()),
            ('cluster_size', self.gf('django.db.models.fields.IntegerField')()),
            ('collapse', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.Sequence'])),
            ('cluster_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.ClusterType'])),
        ))
        db.send_create_signal(u'bs_igdbview', ['Cluster'])

        # Adding model 'IgBlastSummary'
        db.create_table(u'bs_igdbview_igblastsummary', (
            ('summary_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('v_match', self.gf('django.db.models.fields.TextField')()),
            ('d_match', self.gf('django.db.models.fields.TextField')()),
            ('j_match', self.gf('django.db.models.fields.TextField')()),
            ('chain_type', self.gf('django.db.models.fields.TextField')()),
            ('stop_codon', self.gf('django.db.models.fields.TextField')()),
            ('vj_frame', self.gf('django.db.models.fields.TextField')()),
            ('productive', self.gf('django.db.models.fields.TextField')()),
            ('strand', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'bs_igdbview', ['IgBlastSummary'])

        # Adding model 'JunctionSummary'
        db.create_table(u'bs_igdbview_junctionsummary', (
            ('junction_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('v_end', self.gf('django.db.models.fields.TextField')()),
            ('vd_junction', self.gf('django.db.models.fields.TextField')()),
            ('d_region', self.gf('django.db.models.fields.TextField')()),
            ('dj_junction', self.gf('django.db.models.fields.TextField')()),
            ('j_start', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'bs_igdbview', ['JunctionSummary'])

        # Adding model 'IgBlastResult'
        db.create_table(u'bs_igdbview_igblastresult', (
            ('result_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('db_queried', self.gf('django.db.models.fields.TextField')()),
            ('query', self.gf('django.db.models.fields.TextField')()),
            ('length', self.gf('django.db.models.fields.IntegerField')()),
            ('igblast_summary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.IgBlastSummary'])),
            ('junction_summary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.JunctionSummary'])),
            ('alignment_summary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.AlignmentSummary'])),
            ('sequence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.Sequence'])),
        ))
        db.send_create_signal(u'bs_igdbview', ['IgBlastResult'])

        # Adding model 'Library'
        db.create_table(u'bs_igdbview_library', (
            ('library_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('librarycode', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25, db_index=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.Author'])),
            ('organism', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bs_igdbview.Organism'])),
            ('fastqname', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('fastqalias', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('librarysize', self.gf('django.db.models.fields.IntegerField')()),
            ('flowcell', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('downloaddate', self.gf('django.db.models.fields.DateField')()),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('fastqpath', self.gf('django.db.models.fields.CharField')(max_length=1025)),
        ))
        db.send_create_signal(u'bs_igdbview', ['Library'])


    def backwards(self, orm):
        # Deleting model 'Organism'
        db.delete_table(u'bs_igdbview_organism')

        # Deleting model 'TimePoint'
        db.delete_table(u'bs_igdbview_timepoint')

        # Deleting model 'Donor'
        db.delete_table(u'bs_igdbview_donor')

        # Deleting model 'Immunogen'
        db.delete_table(u'bs_igdbview_immunogen')

        # Deleting model 'CellType'
        db.delete_table(u'bs_igdbview_celltype')

        # Deleting model 'Sequence'
        db.delete_table(u'bs_igdbview_sequence')

        # Deleting model 'Sample'
        db.delete_table(u'bs_igdbview_sample')

        # Deleting model 'AlignmentSummary'
        db.delete_table(u'bs_igdbview_alignmentsummary')

        # Deleting model 'Author'
        db.delete_table(u'bs_igdbview_author')

        # Deleting model 'ClusterType'
        db.delete_table(u'bs_igdbview_clustertype')

        # Deleting model 'Cluster'
        db.delete_table(u'bs_igdbview_cluster')

        # Deleting model 'IgBlastSummary'
        db.delete_table(u'bs_igdbview_igblastsummary')

        # Deleting model 'JunctionSummary'
        db.delete_table(u'bs_igdbview_junctionsummary')

        # Deleting model 'IgBlastResult'
        db.delete_table(u'bs_igdbview_igblastresult')

        # Deleting model 'Library'
        db.delete_table(u'bs_igdbview_library')


    models = {
        u'bs_igdbview.alignmentsummary': {
            'Meta': {'object_name': 'AlignmentSummary'},
            'alignment_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'gaps': ('django.db.models.fields.TextField', [], {}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'matches': ('django.db.models.fields.TextField', [], {}),
            'mismatches': ('django.db.models.fields.TextField', [], {}),
            'percent_identity': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'start_position': ('django.db.models.fields.IntegerField', [], {}),
            'stop_position': ('django.db.models.fields.IntegerField', [], {}),
            'translation_query': ('django.db.models.fields.TextField', [], {}),
            'v_gene': ('django.db.models.fields.TextField', [], {})
        },
        u'bs_igdbview.author': {
            'Meta': {'object_name': 'Author'},
            'author_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'designation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'bs_igdbview.celltype': {
            'Meta': {'object_name': 'CellType'},
            'celltype': ('django.db.models.fields.TextField', [], {}),
            'celltype_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'bs_igdbview.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'cluster_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'cluster_name': ('django.db.models.fields.TextField', [], {}),
            'cluster_size': ('django.db.models.fields.IntegerField', [], {}),
            'cluster_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.ClusterType']"}),
            'collapse': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.Sequence']"})
        },
        u'bs_igdbview.clustertype': {
            'Meta': {'object_name': 'ClusterType'},
            'cluster_algorithm': ('django.db.models.fields.TextField', [], {}),
            'cluster_type_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'bs_igdbview.donor': {
            'Meta': {'object_name': 'Donor'},
            'animal': ('django.db.models.fields.IntegerField', [], {}),
            'donor_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organism': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.Organism']"})
        },
        u'bs_igdbview.igblastresult': {
            'Meta': {'object_name': 'IgBlastResult'},
            'alignment_summary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.AlignmentSummary']"}),
            'db_queried': ('django.db.models.fields.TextField', [], {}),
            'igblast_summary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.IgBlastSummary']"}),
            'junction_summary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.JunctionSummary']"}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'result_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.Sequence']"})
        },
        u'bs_igdbview.igblastsummary': {
            'Meta': {'object_name': 'IgBlastSummary'},
            'chain_type': ('django.db.models.fields.TextField', [], {}),
            'd_match': ('django.db.models.fields.TextField', [], {}),
            'j_match': ('django.db.models.fields.TextField', [], {}),
            'productive': ('django.db.models.fields.TextField', [], {}),
            'stop_codon': ('django.db.models.fields.TextField', [], {}),
            'strand': ('django.db.models.fields.TextField', [], {}),
            'summary_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'v_match': ('django.db.models.fields.TextField', [], {}),
            'vj_frame': ('django.db.models.fields.TextField', [], {})
        },
        u'bs_igdbview.immunogen': {
            'Meta': {'object_name': 'Immunogen'},
            'immunogen_code': ('django.db.models.fields.TextField', [], {}),
            'immunogen_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'bs_igdbview.junctionsummary': {
            'Meta': {'object_name': 'JunctionSummary'},
            'd_region': ('django.db.models.fields.TextField', [], {}),
            'dj_junction': ('django.db.models.fields.TextField', [], {}),
            'j_start': ('django.db.models.fields.TextField', [], {}),
            'junction_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'v_end': ('django.db.models.fields.TextField', [], {}),
            'vd_junction': ('django.db.models.fields.TextField', [], {})
        },
        u'bs_igdbview.library': {
            'Meta': {'object_name': 'Library'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.Author']"}),
            'downloaddate': ('django.db.models.fields.DateField', [], {}),
            'fastqalias': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'fastqname': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'fastqpath': ('django.db.models.fields.CharField', [], {'max_length': '1025'}),
            'flowcell': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'library_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'librarycode': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
            'librarysize': ('django.db.models.fields.IntegerField', [], {}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'organism': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.Organism']"})
        },
        u'bs_igdbview.organism': {
            'Meta': {'object_name': 'Organism'},
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'isolate': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'organism_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organismcode': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'strain': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'bs_igdbview.sample': {
            'Meta': {'object_name': 'Sample'},
            'cell_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.CellType']"}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.Donor']"}),
            'immunogen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.Immunogen']"}),
            'organism': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.Organism']"}),
            'sample_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sample_step': ('django.db.models.fields.IntegerField', [], {}),
            'sequence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.Sequence']"}),
            'timepoint': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bs_igdbview.TimePoint']"})
        },
        u'bs_igdbview.sequence': {
            'Meta': {'object_name': 'Sequence'},
            'fasta_sequence': ('django.db.models.fields.TextField', [], {}),
            'fasta_type': ('django.db.models.fields.TextField', [], {}),
            'sequence_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence_name': ('django.db.models.fields.TextField', [], {}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        u'bs_igdbview.timepoint': {
            'Meta': {'object_name': 'TimePoint'},
            'time_code': ('django.db.models.fields.TextField', [], {}),
            'time_point_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['bs_igdbview']