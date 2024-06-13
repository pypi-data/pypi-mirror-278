from unittest import TestCase
from unittest.mock import patch, call, Mock
from tests.utils import FileMock
from filter_vcf.util.filterCarisLiquid import filter_caris_liquid_line

# line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
logger = Mock()


class TestCarisLiquidFilters(TestCase):
    def test_skips_nonexistent_line(self):
        line = None
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_skips_too_few_columns(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence"
        with self.assertRaises(RuntimeError):
            filter_caris_liquid_line(line, logger)

    #        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_skips_too_many_columns(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        with self.assertRaises(RuntimeError):
            filter_caris_liquid_line(line, logger)

    def test_skip_synonymous(self):
        line = "chr9	17446	.	A	T	.	base_qual;clustered_events;contamination;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=4,21|0,0;DP=26;ECNT=14;GERMQ=46;MBQ=37,0;MFRL=307,0;MMQ=22,60;MPOS=50;POPAF=7.3;TLOD=-1.11;TI=XM_011517658.2;GI=WASHC1;FC=Synonymous;PC=A207=;DC=c.621T>A;LO=EXON	GT:AD:AF:DP:F1R2:F2R1:SB	0/1:25,0:0.0385:25:14,0:11,0:4,21,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_skips_nonnumeric_tlod(self):
        line = "chr9	24914	.	G	A	.	base_qual;clustered_events;contamination;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=22,9|0,0;DP=33;ECNT=12;GERMQ=54;MBQ=37,0;MFRL=306,0;MMQ=25,60;MPOS=50;POPAF=7.3;TLOD=TEXT;TI=XM_011517658.2;GI=WASHC1;FC=Missense;PC=A43V;DC=c.128C>T;LO=EXON	GT:AD:AF:DP:F1R2:F2R1:SB	0/1:31,0:0.0315:31:16,0:15,0:22,9,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_tlod_small(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=3;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_tlod_absent(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), line)

    def test_tlod_not_float(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=3x;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_mbq_1_small(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=0,40;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), line)

    def test_mbq_2_small(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,0;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), line)

    def test_mbq_both_small(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=10,10;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_mbq_not_float(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=1X0,40;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_mmq_both_small(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=10,10;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_mmq_not_float(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=10,1X0;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_mpos_absent(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=60,60;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), line)

    def test_mpos_small(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=60,60;MPOS=5;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_mpos_not_float(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=60,60;MPOS=5X;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_af_absent(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), line)

    def test_af_small(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.0009:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)

    def test_af_not_float(self):
        line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,40;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.X09:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        self.assertEqual(filter_caris_liquid_line(line, logger), None)
