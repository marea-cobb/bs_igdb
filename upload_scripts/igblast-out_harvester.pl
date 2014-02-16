#!/Users/mareac/perl5/perlbrew/perls/perl-5.16.0/bin/perl
#
# harvest igblast-result data and output an annotated fasta file
#
#

#use 5.16.3;
use strict;
use DBI;


$/ = "\n";


#igblast_out file
open INFILE1, "$ARGV[0]" 
	or die "Cannot open $ARGV[0].\n";

#input fasta
open INFILE2, "$ARGV[1]" 
	or die "Cannot open $ARGV[1].\n";

my $line;
my $Query;
my $endSection;
my $endTable;
my $endAlignment;
my $queryLength;
my $familyUsage;
my $rearr;
my $alignLength;
my $percentIdent;
my $coverage;
my $alignmentBlockTop = 0;
my $translation;
my @junctions;
my @igblast_summary;
my @truncated;
my $db_query;

my $database = 'bs_igdb';
my $user = 'mcobb';
my $password = 'mcobb';
my $dsn = 'dbi:';
my $host = 'localhost';
my $port = '5423';
my $dbh = 'dbi:PgPP:dbname=$database; host=$host';


my $dbh = DBI->connect("dbi:PgPP:dbname=$database;host=$host;port=$port", $user, $password);
print "Connected to db\n";

sub insert_Junction_Summary{
    my $stmt = $dbh->prepare('INSERT INTO bs_igdbview_junctionsummary (v_end, vd_junction, d_region, dj_junction, j_start) VALUES (?, ?, ?, ?, ?)');
    $stmt->execute($_[0], $_[1], $_[2], $_[3], $_[4]);
    my $new_id = $dbh->last_insert_id(undef, undef, 'bs_igdbview_junctionsummary', undef);
    return $new_id;
}


sub insert_Igblast_Summary {
    my $stmt = $dbh->prepare('INSERT INTO bs_igdbview_igblastsummary (v_match, d_match, j_match, chain_type, stop_codon, vj_frame, productive, strand) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
    $stmt->execute($_[0], $_[1], $_[2], $_[3], $_[4], $_[5], $_[6], $_[7]);
    my $new_id = $dbh->last_insert_id(undef, undef, 'bs_igdbview_igblastsummary', undef);
    return $new_id;
}


sub insert_Alignment_Summary {
#    print "$_[0]\n";
    my $stmt = $dbh->prepare('INSERT INTO bs_igdbview_alignmentsummary (v_gene, start_position, stop_position, length, matches, mismatches, gaps, percent_identity, translation_query) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
    $stmt->execute($_[0], $_[1], $_[2], $_[3], $_[4], $_[5], $_[6], $_[7], $_[8]);
    my $new_id = $dbh->last_insert_id(undef, undef, 'bs_igdbview_alignmentsummary', undef);
    return $new_id;
}


sub insert_Sequence {
    my $length = length($_[1]);
    my $stmt = $dbh->prepare('INSERT INTO bs_igdbview_sequence (sequence_name, fasta_sequence, fasta_type, size) VALUES (?, ?, ?, ?)');
    $stmt->execute($_[0], $_[1], 'fasta', $length);
    my $new_id = $dbh->last_insert_id(undef, undef, 'bs_igdbview_sequence', undef);
    return $new_id;
}


sub insert_Igblast_Result {
    my $stmt = $dbh->prepare('INSERT INTO bs_igdbview_igblastresult (db_queried, query, length, igblast_summary_id, junction_summary_id, alignment_summary_id, sequence_id) VALUES (?, ?, ?, ?, ?, ?, ?)');
    $stmt->execute($_[0], $_[1], $_[2], $_[3], $_[4], $_[5], $_[6]);
    print "Results have been inserted"
#    my $new_id = $dbh->last_insert_id(undef, undef, 'bs_igdbview_sequence', undef);
#    return $new_id;
}


sub main {

    while (defined ($line = <INFILE1>))
    {
        if ($line =~ m|^Database: (\S*\D*)|)
        {
            $db_query = $1;
            }
        elsif ($line =~ m|^Query= (\S*)|s)
        {
            $Query = $1;
            $endSection = 0;
            $endAlignment = 0;
            $endTable = 0;
            while (!$endSection and defined ($line = <INFILE1>))
            {
                if ($line =~ m|^Length=(\d+)|)
                {	$queryLength = $1;	}
                elsif ($line =~ m|Effective search space used|)
                {	$endSection = 1;	}
                elsif ($line =~ m|rearrangement summary for query sequence|)
                {
                    $line = <INFILE1>;
                    chomp $line;
                    $familyUsage = $line;
                    @igblast_summary = split('\t', $familyUsage);
                }
                elsif ($line =~ m|junction details based on top germline gene|)
                {
                    $line = <INFILE1>;
                    chomp $line;
                    $rearr =  $line;
                    @junctions = split('\t', $rearr);
                }
                elsif ($line =~ m|^Alignment summary between query and top germline V gene hit|)
                {
                    while (!$endTable and defined ($line = <INFILE1>))
                    {
                        if ($line =~ m|^FR1|)
					    {	$truncated[0] = $line;	}
					    elsif ($line =~ m|^CDR1|)
					    {	$truncated[1] = $line;	}
					    elsif ($line =~ m|^FR2|)
                        {	$truncated[2] = $line;	}
                        elsif ($line =~ m|^CDR2|)
                        {	$truncated[3] = $line;	}
                        elsif ($line =~ m|^FR3|)
                        {	$truncated[4] = $line;	}
                        elsif ($line =~ m|^CDR3|)
                        {	$truncated[5] = $line;	}
                        elsif ($line =~ m|^Total\t\S+\t\S+\t|)
                        {
                            if ($line =~ m|^Total\t\S+\t\S+\t(\d+)\t\S+\t\S+\t\S+\t(\d+\.*\d*)|)
                            {
                                $alignLength = $1;
                                $percentIdent = $2;
                                $coverage = sprintf ("%.1f", $alignLength / $queryLength * 100);
                                $endTable = 1;
                            }
                            else {die "Error at $Query summary.";}
                        }
                        elsif ($line =~ m|Effective search space used|)
                        {	$endSection = 1;	}
                    }
                }
                elsif ($line =~ m|^Alignments$|)
                {
                    $translation = '';
                    while (!$endAlignment and defined ($line = <INFILE1>))
                    {
                        if ($line =~ m|^$|)
                        {
                            $line = <INFILE1>;
                            $alignmentBlockTop = 1;
                        }
                        elsif ($alignmentBlockTop and ($line =~ m|^\s+|))
                        {
                            chomp $line;
                            $line =~ s|\s+||g;
                            $translation .= $line;
                            $alignmentBlockTop = 0;
                        }
                        elsif ($line =~ m|^Lambda|)
                        {
                            $endAlignment = 1;
                        }
                    }
                }
                elsif ($line =~ m|^\*\*\*\*\* No hits found \*\*\*\*\*$| )
                {
                    $familyUsage = "invalid_query_seq";
                    $rearr = '';
                    $coverage = 0;
                    $translation = '';
                    $percentIdent = 0;
                }
            }

#            print "\>$Query\t$familyUsage\tjunctnn:$rearr\tpcov:$coverage\tpid:$percentIdent\ttransl:$translation\n";
            if (defined ($line = <INFILE2>) and ($line =~ m|^>$Query|))
            {
                $line = <INFILE2>;
                my $sequence_id = insert_Sequence($Query, $line);
                my $junction_id = insert_Junction_Summary(@junctions);
                my $igblast_id = insert_Igblast_Summary(@igblast_summary);

                foreach (@truncated) {
                    my @summary = split('\t', $_);
                    push (@summary, $translation);
                    my $alignment_id = insert_Alignment_Summary(@summary);
                    insert_Igblast_Result($db_query, $Query, $alignLength, $igblast_id, $junction_id, $alignment_id, $sequence_id    );
            }
            }
            else {die "Error at $Query FASTA entry transfer.";}
        }
    }

    close INFILE1;
    close INFILE2;
}

main();
