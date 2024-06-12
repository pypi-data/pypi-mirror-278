import sys
import simplevc
simplevc.register(sys.modules[__name__])

from collections import defaultdict
from biodata.bed import BED

import genomictools
from genomictools import GenomicCollection

@vc
def _get_TSS_20240501(gffs, forward_len, reverse_len, bed_name_attribute="transcript_id", filter_func=None):
	'''
	Get regions relative to the transcription start sites (TSSes).Do not confuse TSS with TTS.
	
	:param gffs: gencode gffs / gtfs
	:param forward_len: Length to extend in the forward strand. Use 1 if only TSS is chosen. For TSS-500bp to TSS+250bp, the region is 750bp long and forward_len should be set to 250. 
	:param reverse_len: Length to extend in the reverse strand. For TSS-500bp to TSS+250bp, the region is 750bp long and reverse_len should be set to 500.
	:return: Genomic collection of BED with transcript ID as name.
	'''
	return GenomicCollection(map(lambda gff3: BED(gff3.genomic_pos.name, 
												  ((gff3.genomic_pos.start - reverse_len) if gff3.strand == "+" else (gff3.genomic_pos.stop - (forward_len - 1))) - 1,
												  ((gff3.genomic_pos.start + (forward_len - 1)) if gff3.strand == "+" else (gff3.genomic_pos.stop + reverse_len)), 
												  gff3.attribute[bed_name_attribute],
												  None,
												  gff3.strand
												 ), 
								 filter(lambda gff3: gff3.feature == "transcript" and (True if filter_func is None else filter_func(gff3)), gffs)))
@vc
def _get_TTS_20240501(gffs, forward_len, reverse_len, bed_name_attribute="transcript_id", filter_func=None):
	'''
	Get regions relative to the transcription termination sites (TTSes).Do not confuse TSS with TTS.
	
	:param gffs: gencode gffs / gtfs
	:param forward_len: Length to extend in the forward strand. Use 1 if only TTS is chosen.  
	:param reverse_len: Length to extend in the reverse strand. 
	:return: Genomic collection of BED with transcript ID as name.
	'''
	return GenomicCollection(map(lambda gff3: BED(gff3.genomic_pos.name, 
												  ((gff3.genomic_pos.stop - reverse_len) if gff3.strand == "+" else (gff3.genomic_pos.start - (forward_len - 1))) - 1,
												  ((gff3.genomic_pos.stop + (forward_len - 1)) if gff3.strand == "+" else (gff3.genomic_pos.start + reverse_len)), 
												  gff3.attribute[bed_name_attribute],
												  None,
												  gff3.strand
												 ), 
								 filter(lambda gff3: gff3.feature == "transcript" and (True if filter_func is None else filter_func(gff3)), gffs)))
@vc
def _get_transcripts_20240501(gffs, bed_name_attribute="transcript_id", filter_func=None):
	'''
	Extract transcript regions. 

	:param gffs: gencode gffs
	:return: Genomic collection of BED with transcript ID as name. 
	
	'''
	return GenomicCollection(map(lambda gff3: BED(gff3.genomic_pos.name, gff3.genomic_pos.start - 1, gff3.genomic_pos.stop, gff3.attribute[bed_name_attribute], None, gff3.strand),
								 filter(lambda gff3: gff3.feature == "transcript" and (True if filter_func is None else filter_func(gff3)), gffs)))


@vc
def _filter_out_overlapping_genes_20240501(gffs, extension=0):
	'''
	From all gencode entries, extract genes and find genes that are not overlapping with any other genes.
	Output all selected entries with attribute gene_id and the gene_id should be in the list of extracted genes. 
	'''
	def _no_overlap_generator(gc):
		yield from filter(lambda r: len(list(gc.find_overlaps(r))) == 1, gc)
	
	gene_gffs = GenomicCollection([gff for gff in gffs if gff.feature=="gene"])
	if extension == 0:
		gene_ids = set(gff.attribute["gene_id"] for gff in _no_overlap_generator(gene_gffs))
	else:
		extended_gene_gffs = GenomicCollection([BED(gff.seqname, gff.start - extension, gff.end + extension, name=gff.attribute["gene_id"]) for gff in gene_gffs]) 
		gene_ids = set(bed.name for bed in _no_overlap_generator(extended_gene_gffs))
	return GenomicCollection(filter(lambda gff: "gene_id" in gff.attribute and gff.attribute["gene_id"] in gene_ids, gffs))

@vc
def _generate_bigwig_values_by_attributes_20240501(gffs, attribute_name, bw, bwmn=None, filter_func=None, region_func=None, value_method="sum", merge_method=None):
	if bwmn is not None:
		stranded = True
		bwpl = bw
	else:
		stranded = False
	
	count_dict = defaultdict(list)
	for gff in filter(lambda gff: attribute_name in gff.attribute and (True if filter_func is None else filter_func(gff)), gffs):
		r = gff if region_func is not None else region_func(gff)
		if stranded:
			if gff.strand == "+":
				count = bwpl.value(r, method=value_method)
			else:
				count = bwmn.value(r, method=value_method)
		else:
			count = bw.value(r, method=value_method)
		count_dict[gff.attribute[attribute_name]].append(count)
	if merge_method is None:
		return dict(count_dict)
	else:
		if merge_method == "sum":
			merge_func = sum
		elif merge_method == "abssum":
			merge_func = lambda x: sum(map(abs, x))
		elif merge_method == "max":
			merge_func = max
		elif merge_method == "absmax":
			merge_func = lambda x: max(map(abs, x))
		else:
			raise Exception("Unsupported merge method") 
		return {k: merge_func(v) for k, v in count_dict.items()}
	
