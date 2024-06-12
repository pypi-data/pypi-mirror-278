import sys
import simplevc
simplevc.register(sys.modules[__name__])

import pysam
@vc
def _get_bam_total_reads_20240501(i):
	ibam = pysam.AlignmentFile(i, "rb")
	all_read_names = set(read.qname for read in ibam.fetch(until_eof=True))
	ibam.close()
	return len(all_read_names)