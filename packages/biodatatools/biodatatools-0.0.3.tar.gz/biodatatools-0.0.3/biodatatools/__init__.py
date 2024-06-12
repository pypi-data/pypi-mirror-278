import sys
import simplevc
simplevc.register(sys.modules[__name__], "0.0.3")

from commonhelper import convert_to_bool


def check_binaries_validity(*binary_names): # Change to decorator in the future
	import shutil
	missing_binary_names = [binary_name for binary_name in binary_names if shutil.which(binary_name) is None]
	if len(missing_binary_names) > 0:
		raise Exception("The following binaries are not found: " + ",".join(binary_names))
	
def bash_command(cmd):
	import subprocess
	p = subprocess.run(cmd, shell=True, executable='/bin/bash')
	if p.returncode != 0:
		raise Exception("Bash command fails: " + cmd)
	
#  
# Common file conversions
#  
@vt(
	description="Convert bedgraph into bigwig files", 
	helps=dict(
		i="Input bedgraph file", g="chrom size file", o="output bigwig file",
		autosort="Perform sorting on bedgraph file before running bedGraphToBigWig",
		filter_chr="Remove chromosomes in bedgraph file that are not present in chrom.sizes file", 
		nthread="Number of threads used in sorting")
)
@vc
def _convert_bedgraph_to_bigwig_20240423(i:str, g:str, o:str, autosort:convert_to_bool=False, filter_chr:convert_to_bool=False, nthread:int=1):
	'''
	Convert bedgraph into bigwig files. Auto sort and filter bedgraphs prior to calling bedGraphToBigWig
	:param i: Input bedgraph file
	:param g: chrom.size file
	:param o: Output bw file
	:param autosort: Perform sorting on bedgraph file before running bedGraphToBigWig
	:param filter_chr: Remove chromosomes in bedgraph file that are not present in chrom.sizes file
	'''
	import os
	import tempfile
	from biodata.delimited import DelimitedReader, DelimitedWriter
	check_binaries_validity("zcat", "sort", "bedGraphToBigWig")
	tmpfiles = []
	if filter_chr:
		inputfile = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
		tmpfiles.append(inputfile)
		with DelimitedReader(g) as dr:
			chromosomes = set([d[0] for d in dr])
		with DelimitedReader(i) as dr, DelimitedWriter(inputfile) as dw:
			for d in dr:
				if d[0] in chromosomes:
					dw.write(d)
		i = inputfile
	
	if autosort:
		inputfile = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
		tmpfiles.append(inputfile)
		if nthread > 1:
			added_param = f"--parallel={nthread} "
		else:
			added_param = ""
		if i.endswith(".gz"):
			bash_command(f"zcat {i} | sort -k1,1 -k2,2n {added_param}> {inputfile}")
		else:
			bash_command(f"sort -k1,1 -k2,2n {added_param}{i} > {inputfile}")
		i = inputfile
		
	bash_command(f"bedGraphToBigWig {i} {g} {o}")
	for tmpfile in tmpfiles:
		os.unlink(tmpfile)
@vt(
	description="Convert bedgraph into bigwig files.", helps=dict(
		i="Input bedgraph file", g="Chrom size file", o="Output bigwig file",
		autosort="Perform sorting on bedgraph file before running bedGraphToBigWig. Set to *false* if you are sure that your input files are sorted to reduce running time.",
		filter_chr="Remove chromosomes in bedgraph file that are not present in chrom size file", 
		nthread="Number of threads used in sorting")
)
@vc
def _convert_bedgraph_to_bigwig_20240501(i:str, g:str, o:str, autosort:convert_to_bool=True, filter_chr:convert_to_bool=False, nthread:int=1):
	import os
	import tempfile
	from biodata.delimited import DelimitedReader, DelimitedWriter
	
	check_binaries_validity("zcat", "sort", "bedGraphToBigWig")
	tmpfiles = []
	if filter_chr:
		inputfile = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
		tmpfiles.append(inputfile)
		with DelimitedReader(g) as dr:
			chromosomes = set([d[0] for d in dr])
		with DelimitedReader(i) as dr, DelimitedWriter(inputfile) as dw:
			for d in dr:
				if d[0] in chromosomes:
					dw.write(d)
		i = inputfile
	
	if autosort:
		inputfile = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
		tmpfiles.append(inputfile)
		if nthread > 1:
			added_param = f"--parallel={nthread} "
		else:
			added_param = ""
		if i.endswith(".gz"):
			bash_command(f"zcat {i} | sort -k1,1 -k2,2n {added_param}> {inputfile}")
		else:
			bash_command(f"sort -k1,1 -k2,2n {added_param}{i} > {inputfile}")
		i = inputfile
		
	bash_command(f"bedGraphToBigWig {i} {g} {o}")
	for tmpfile in tmpfiles:
		os.unlink(tmpfile)


# 
# PRO-cap/seq specific tools
#

@vt(description="Convert GROcap/PROcap/GROseq/PROseq bam file to bigwig files (paired-end reads). Returns 4 bigwig files representing 5' and 3' end of the molecules on plus or minus strand. See PRO-cap design for more explanations about rna_strand.", 
	helps=dict(i="Input bam file", g="Chrom size file", o="Output bigwig file prefix",
			paired_end="Specify *true* if paired-end sequencing and *false* for single-end sequencing",
			rna_strand="Indicate whether RNA strand is forward or reverse. In paired-end, forward implies that the first bp of read 1 is 5'. reverse implies that the first bp of read 2 is 5'"
			)
		)
@vc
def _process_PROcap_bam_to_bigwig_20240423(i:str, g:str, o:str, paired_end : convert_to_bool, rna_strand : str):
	import os
	import tempfile
	from mphelper import ProcessWrapPool
	
	check_binaries_validity("samtools", "bedtools", "zcat", "sort", "bedGraphToBigWig")
	
	tmpfiles = [tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name for _ in range(4)]
	bg5_pl, bg5_mn, bg3_pl, bg3_mn = tmpfiles
	thread = 16
	pwpool = ProcessWrapPool(4)
	if paired_end:
		tmpfiles_bam = [tempfile.NamedTemporaryFile(mode='w+', suffix=".bam", delete=False).name for _ in range(2)]
		bam5, bam3 = tmpfiles_bam		
		if rna_strand == "forward":
			bam5_pid = pwpool.run(bash_command, args=[f"samtools view -f 66 --write-index -@ {thread} -o {bam5} {i}"])
			bam3_pid = pwpool.run(bash_command, args=[f"samtools view -f 130 --write-index -@ {thread} -o {bam3} {i}"])
		elif rna_strand == "reverse":
			bam5_pid = pwpool.run(bash_command, args=[f"samtools view -f 130 --write-index -@ {thread} -o {bam5} {i}"])
			bam3_pid = pwpool.run(bash_command, args=[f"samtools view -f 66 --write-index -@ {thread} -o {bam3} {i}"])
		else:
			raise Exception()
		# Be careful of the strand. We assumed F1R2 setup 
		bgpl_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {bam5} -5 -strand + -bg > {bg5_pl}"], dependencies=[bam5_pid])
		bgmn_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {bam5} -5 -strand - -bg | awk {{'printf (\"%s\\t%s\\t%s\\t-%s\\n\", $1, $2, $3, $4)'}} > {bg5_mn}"], dependencies=[bam5_pid])
		bg3pl_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {bam3} -5 -strand - -bg > {bg3_pl}"], dependencies=[bam3_pid])
		bg3mn_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {bam3} -5 -strand + -bg | awk {{'printf (\"%s\\t%s\\t%s\\t-%s\\n\", $1, $2, $3, $4)'}} > {bg3_mn}"], dependencies=[bam3_pid])
	else:
		tmpfiles_bam = [] # No bam files needed
		bgpl_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {i} -5 -strand + -bg > {bg5_pl}"])
		bgmn_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {i} -5 -strand - -bg | awk {{'printf (\"%s\\t%s\\t%s\\t-%s\\n\", $1, $2, $3, $4)'}} > {bg5_mn}"])
		bg3pl_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {i} -3 -strand + -bg > {bg3_pl}"])
		bg3mn_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {i} -3 -strand - -bg | awk {{'printf (\"%s\\t%s\\t%s\\t-%s\\n\", $1, $2, $3, $4)'}} > {bg3_mn}"])
		
	pwpool.run(_convert_bedgraph_to_bigwig_20240423, args=[bg5_pl, g, o + "_5pl.bw"], kwargs=dict(autosort=True, filter_chr=True), dependencies=[bgpl_pid])
	pwpool.run(_convert_bedgraph_to_bigwig_20240423, args=[bg5_mn, g, o + "_5mn.bw"], kwargs=dict(autosort=True, filter_chr=True), dependencies=[bgmn_pid])
	pwpool.run(_convert_bedgraph_to_bigwig_20240423, args=[bg3_pl, g, o + "_3pl.bw"], kwargs=dict(autosort=True, filter_chr=True), dependencies=[bg3pl_pid])
	pwpool.run(_convert_bedgraph_to_bigwig_20240423, args=[bg3_mn, g, o + "_3mn.bw"], kwargs=dict(autosort=True, filter_chr=True), dependencies=[bg3mn_pid])
	pwpool.get(wait=True)
	pwpool.close()
	for tmpfile in tmpfiles + tmpfiles_bam:
		os.unlink(tmpfile)

@vt(description="Convert GROcap/PROcap/GROseq/PROseq bam file to bed files Returns 2 bed files with the 4th column as a comma separated list of RNA distances from TSS", 
	helps=dict(i="Input bam file", o="output bed file prefix. Two files, _dpl.bed.gz and _dmn.bed.gz are output",
			paired_end="True: paired-end sequencing; False: single-end sequencing",
			rna_strand="Indicate whether RNA strand is forward or reverse. In paired-end, forward represents that first read is 5'.",
			min_rna_len="Minimum RNA length to record",
			max_rna_len="Maximum RNA length to record"
			)
		)
@vc
def _process_PROcap_bam_to_TSS_RNA_len_20240423(i, o, paired_end, rna_strand, min_rna_len=0, max_rna_len=100000): 
	'''
	'''
	import pysam
	from commonhelper import nested_default_dict
	from biodata.baseio import BaseWriter
	from biodata.bed import BEDPE
	
	def _to_position(alignment):
		position = alignment.reference_end if alignment.is_reverse else (alignment.reference_start + 1)
		strand = "-" if alignment.is_reverse else "+"
		return (alignment.reference_name, position, strand)

	if not paired_end:
		raise Exception("Single-end not supported yet.")
	saved_reads = {}
	TSS_counter = nested_default_dict(3, list)
	with pysam.AlignmentFile(i) as samfh: 
		for alignment in samfh:
			if alignment.query_name in saved_reads:
				prev_alignment = saved_reads.pop(alignment.query_name)
				alignment1 = prev_alignment if prev_alignment.is_read1 else alignment
				alignment2 = prev_alignment if prev_alignment.is_read2 else alignment
				p1 = _to_position(alignment1) # read1: Pol
				p2 = _to_position(alignment2) # read2: TSS
				
				b = BEDPE(p1[0], p1[1] - 1, p1[1], p2[0], p2[1] - 1, p2[1], strand1 = p1[2], strand2 = p2[2])
				if (b.chrom1 == b.chrom2
					and (   (b.strand1 == "+" and b.strand2 == "-" and b.start1 <= b.start2 and b.stop1 <= b.stop2 and min_rna_len <= b.stop2 - b.start1 <= max_rna_len)
						 or (b.strand1 == "-" and b.strand2 == "+" and b.start2 <= b.start1 and b.stop2 <= b.stop1 and min_rna_len <= b.stop1 - b.start2 <= max_rna_len))):
					
					
					d = b.stop2 - b.start1 if b.strand1 == "+" else b.stop1 - b.start2
					if rna_strand == "forward":
						strand = b.strand1
						if strand == "+":
							TSS_counter[strand][b.chrom1][b.genomic_pos1.start].append(d)
						else:
							TSS_counter[strand][b.chrom1][b.genomic_pos1.stop].append(d)
					elif rna_strand == "reverse":
						strand = b.strand2
						if strand == "+":
							TSS_counter[strand][b.chrom1][b.genomic_pos2.stop].append(d)
						else:
							TSS_counter[strand][b.chrom1][b.genomic_pos2.start].append(d)
					else:
						raise Exception()

			else:
				saved_reads[alignment.query_name] = alignment
		for output_file, strand in zip([f"{o}_dpl.bed.gz", f"{o}_dmn.bed.gz"], ["+", "-"]):
			with BaseWriter(output_file) as bwd:
				regions = TSS_counter[strand]
				for r in sorted(regions.keys()):
					positions = regions[r]
					for p in sorted(positions.keys()):
						v = sorted(positions[p])
						bwd.write(f"{r}\t{p - 1}\t{p}\t{','.join(list(map(str, v)))}\n")
@vt(description="Convert GROcap/PROcap/GROseq/PROseq bam file to bed files Returns 2 bed files with the 4th column as a comma separated list of RNA distances from TSS.", 
	helps=dict(i="Input bam file", o="output bed file prefix. Two files, _dpl.bed.bgz and _dmn.bed.bgz are output",
			paired_end="Specify *true* if paired-end sequencing and *false* for single-end sequencing",
			rna_strand="Indicate whether RNA strand is forward or reverse. In paired-end, forward implies that the first bp of read 1 is 5'. reverse implies that the first bp of read 2 is 5'",
			min_rna_len="Minimum RNA length to record",
			max_rna_len="Maximum RNA length to record",
			g="Chrom size file. If provided, only chromosomes in the chrom size file are retained."
			)
		)
@vc
def _process_PROcap_bam_to_TSS_RNA_len_20240501(i, o, paired_end, rna_strand, min_rna_len=0, max_rna_len=100000, g:str=None): 
	'''
	'''
	import pysam
	from commonhelper import nested_default_dict
	from biodata.baseio import BaseWriter
	from biodata.bed import BEDPE
	from biodata.delimited import DelimitedReader
	def _to_position(alignment):
		position = alignment.reference_end if alignment.is_reverse else (alignment.reference_start + 1)
		strand = "-" if alignment.is_reverse else "+"
		return (alignment.reference_name, position, strand)

	if not paired_end:
		raise Exception("Single-end not supported yet.")
	if g is not None:
		target_chromosomes = DelimitedReader.read_all(lambda ds: set(d[0] for d in ds), g)
	else:
		target_chromosomes = None
	saved_reads = {}
	TSS_counter = nested_default_dict(3, list)
	with pysam.AlignmentFile(i) as samfh: 
		for alignment in samfh:
			if target_chromosomes is not None and alignment.reference_name not in target_chromosomes:
				continue
			if alignment.query_name in saved_reads:
				prev_alignment = saved_reads.pop(alignment.query_name)
				alignment1 = prev_alignment if prev_alignment.is_read1 else alignment
				alignment2 = prev_alignment if prev_alignment.is_read2 else alignment
				p1 = _to_position(alignment1) # read1: Pol
				p2 = _to_position(alignment2) # read2: TSS
				
				b = BEDPE(p1[0], p1[1] - 1, p1[1], p2[0], p2[1] - 1, p2[1], strand1 = p1[2], strand2 = p2[2])
				if (b.chrom1 == b.chrom2
					and (   (b.strand1 == "+" and b.strand2 == "-" and b.start1 <= b.start2 and b.stop1 <= b.stop2 and min_rna_len <= b.stop2 - b.start1 <= max_rna_len)
						 or (b.strand1 == "-" and b.strand2 == "+" and b.start2 <= b.start1 and b.stop2 <= b.stop1 and min_rna_len <= b.stop1 - b.start2 <= max_rna_len))):
					
					
					d = b.stop2 - b.start1 if b.strand1 == "+" else b.stop1 - b.start2
					if rna_strand == "forward":
						strand = b.strand1
						if strand == "+":
							TSS_counter[strand][b.chrom1][b.genomic_pos1.start].append(d)
						else:
							TSS_counter[strand][b.chrom1][b.genomic_pos1.stop].append(d)
					elif rna_strand == "reverse":
						strand = b.strand2
						if strand == "+":
							TSS_counter[strand][b.chrom1][b.genomic_pos2.stop].append(d)
						else:
							TSS_counter[strand][b.chrom1][b.genomic_pos2.start].append(d)
					else:
						raise Exception()

			else:
				saved_reads[alignment.query_name] = alignment
		for output_file, strand in zip([f"{o}_dpl.bed.bgz", f"{o}_dmn.bed.bgz"], ["+", "-"]):
			with BaseWriter(output_file) as bwd:
				regions = TSS_counter[strand]
				for r in sorted(regions.keys()):
					positions = regions[r]
					for p in sorted(positions.keys()):
						v = sorted(positions[p])
						if strand == "-":
							v = sorted([e * -1 for e in v])
						bwd.write(f"{r}\t{p - 1}\t{p}\t{','.join(list(map(str, v)))}\n")						
@vt(
	description="Merge PROcap TSS RNA len files.",
	helps=dict(
		i="Input files", 
		o="Output file"
	)
)
@vc
def _merge_PROcap_TSS_RNA_len_20240430(i:list[str], o:str):
	from biodata.bed import BEDGraph, BEDGraphReader, BEDGraphWriter
	brs = [BEDGraphReader( f, dataValueType=lambda s: list(map(int, s.split(",")))) for f in i]
	with BEDGraphWriter(o, dataValueFunc=lambda v: ",".join(list(map(str, sorted(v))))) as bw:
		finished = False
		while not finished:
			min_region = None
			for br in brs:
				r = br.peek()
				if r is None:
					continue
				if min_region is None or min_region > r.genomic_pos:
					min_region = r.genomic_pos
			if min_region is not None:
				vs = []
				for br in brs:
					if br.peek() is not None and br.peek().genomic_pos == min_region:
						r = br.read()
						vs.extend(r.dataValue)
				bw.write(BEDGraph(min_region.name, min_region.zstart, min_region.ostop, vs))
			else:
				finished = True

@vt(
	description="Summarize the PROcap TSS RNA len files into min, median, mean and max of RNA lengths.",
	helps=dict(
		i="Input files", 
		o="Output file"
	)
)
@vc
def _summarize_PROcap_TSS_RNA_len_20240501(i:list[str], o:str):
	from biodata.baseio import BaseWriter
	from biodata.bed import BEDXReader
	import numpy as np
	dists = []
	for f in i:
		with BEDXReader(f, ["dist"], [lambda a: list(map(lambda x: abs(int(x)), a.split(",")))]) as br:
			for b in br:
				dists.extend(b.dist)
	with BaseWriter(o) as bw:
		bw.write(f"min\t{np.min(dists)}\n")
		bw.write(f"median\t{np.median(dists)}\n")
		bw.write(f"mean\t{np.mean(dists)}\n")
		bw.write(f"max\t{np.max(dists)}\n")

@vt(
	description="Generate gene body TSS ratio table. For capped RNA reads, the 5' end should be much more dominant near the promoter TSS region than the transcript region.	The ratio of gene body reads to TSS reads serves as a quality measure for capped RNA sequencing experiments.",
	helps=dict(
		label="Sample labels",
		ibwpl="Input bigwig file (plus/sense strand on chromosomes)",
		ibwmn="Input bigwig file (minus/antisense strand on chromosomes)",
		iga="Input gene annotations used in calculating the gene body TSS ratio. One may want to pre-filter the annotations to get a specific set of genes prior to running this command.",
		o="Output file",
		mode="Only accept heg or all. In heg mode, only the specified ratio of top highly expressed genes are used to calculate the ratio. In all mode, all genes are used to calculate the ratio.",
		gb_dc_tss_forward_len="Forward len of discarded part around TSS when obtaining the gene body region",
		gb_dc_tss_reverse_len="Reverse len of discarded part around TSS when obtaining the gene body region",
		gb_dc_tts_forward_len="Forward len of discarded part around TTS when obtaining the gene body region",
		gb_dc_tts_reverse_len="Reverse len of discarded part around TTS when obtaining the gene body region",
		tss_forward_len="Forward len of TSS region",
		tss_reverse_len="Reerse len of TSS region",
		heg_top_ratio="In heg mode, the specified ratio of top expressed genes used for calculating gene body TSS ratio",
		heg_tss_forward_len="Forward len of TSS region when considering the gene expression",
		heg_tss_reverse_len="Reverse len of TSS region when considering the gene expression",
	)
)
@vc
def _generate_genebody_TSS_ratio_table_20240501(
		label:list[str], ibwpl:list[str], ibwmn:list[str],
		iga:str,
		o:str,
		mode:str="heg", 
		gb_dc_tss_forward_len:int=500, gb_dc_tss_reverse_len:int=0, 
		gb_dc_tts_forward_len:int=1, gb_dc_tts_reverse_len:int=499,
		tss_forward_len:int=500, tss_reverse_len:int=0,
		heg_top_ratio:float=0.1,
		heg_tss_forward_len:int=1000, heg_tss_reverse_len:int=100,
		
	):
	import itertools
	from biodata.baseio import get_text_file_extension
	from biodata.bigwig import BigWigIReader
	from biodata.delimited import DelimitedWriter
	from biodata.gff import GFF3Reader, GTFReader
	import genomictools
	from genomictools import GenomicPos
	
	
	from .utils import geneannotation
	if not (len(label) == len(ibwpl) == len(ibwmn)):
		raise Exception()
	reader = GFF3Reader if get_text_file_extension(iga) == "gff3" else GTFReader
	gffs = reader.read_all(lambda gffs: [gff for gff in gffs if gff.feature == "transcript"], iga)

	ibwpl = [BigWigIReader(f) for f in ibwpl]
	ibwmn = [BigWigIReader(f) for f in ibwmn]
	with DelimitedWriter(o) as dw:
		dw.write(["Sample", "Gene body counts", "Gene body length", "TSS counts", "TSS length", "Gene body ratio"])		
		if mode == "all":
			gff_pls = list(filter(lambda gff: gff.strand == "+", gffs))
			gff_mns = list(filter(lambda gff: gff.strand == "-", gffs))
			gb_pl = list(genomictools.substract(
				genomictools.union(gff_pls),
				geneannotation._get_TSS_20240501(gff_pls, gb_dc_tss_forward_len, gb_dc_tss_reverse_len),
				geneannotation._get_TTS_20240501(gff_pls, gb_dc_tts_forward_len, gb_dc_tts_reverse_len), 
			))
			gb_mn = list(genomictools.substract(
				genomictools.union(gff_mns),
				geneannotation._get_TSS_20240501(gff_mns, gb_dc_tss_forward_len, gb_dc_tss_reverse_len),
				geneannotation._get_TTS_20240501(gff_mns, gb_dc_tts_forward_len, gb_dc_tts_reverse_len), 
			))
			tss_pl = list(genomictools.union(geneannotation._get_TSS_20240501(gff_pls, tss_forward_len, tss_reverse_len)))
			tss_mn = list(genomictools.union(geneannotation._get_TSS_20240501(gff_mns, tss_forward_len, tss_reverse_len)))
			
			gb_lengths = sum(map(lambda b: len(b.genomic_pos), itertools.chain(gb_pl, gb_mn)))
			tss_lengths = sum(map(lambda b: len(b.genomic_pos), itertools.chain(tss_pl, tss_mn)))
			for label, bwpl, bwmn in zip(label, ibwpl, ibwmn):
				tss_counts = sum(bwpl.value(r, method="abssum") for r in tss_pl) + sum(bwmn.value(r, method="abssum") for r in tss_mn)
				gb_counts = sum(bwpl.value(r, method="abssum") for r in gb_pl) + sum(bwmn.value(r, method="abssum") for r in gb_mn)
				if tss_lengths == 0 or tss_counts == 0 or gb_lengths == 0:
					dw.write([label, gb_counts, gb_lengths, tss_counts, tss_lengths, float("nan")])
				else:
					dw.write([label, gb_counts, gb_lengths, tss_counts, tss_lengths, (gb_counts / gb_lengths) / ((tss_counts / tss_lengths) + (gb_counts / gb_lengths))])
		elif mode == "heg":
			for label, bwpl, bwmn in zip(label, ibwpl, ibwmn):
				# Only select highly expressed genes
				gene_count_dict = geneannotation._generate_bigwig_values_by_attributes_20240501(
					gffs, "gene_id", bwpl, bwmn,
					region_func = lambda gff: GenomicPos(
						gff.genomic_pos.name, 
						(gff.genomic_pos.start - heg_tss_reverse_len) if gff.strand == "+" else (gff.genomic_pos.stop - (heg_tss_forward_len - 1)), 
						(gff.genomic_pos.start + (heg_tss_forward_len - 1)) if gff.strand == "+" else (gff.genomic_pos.stop + heg_tss_reverse_len)
					),
					value_method = "abssum",
					merge_method = "max"
				)
				selected_gene_ids = set(map(lambda x: x[0], sorted(gene_count_dict.items(), reverse=True, key=lambda x: x[1])[:int(heg_top_ratio * len(gene_count_dict))]))
				filtered_gffs = list(filter(lambda gff: gff.attribute["gene_id"] in selected_gene_ids, gffs))
				
				# Define the gene body and TSS regions
				gff_pls = list(filter(lambda gff: gff.strand == "+", filtered_gffs))
				gff_mns = list(filter(lambda gff: gff.strand == "-", filtered_gffs))
				gb_pl = list(genomictools.substract(
					genomictools.union(gff_pls),
					geneannotation._get_TSS_20240501(gff_pls, gb_dc_tss_forward_len, gb_dc_tss_reverse_len),
					geneannotation._get_TTS_20240501(gff_pls, gb_dc_tts_forward_len, gb_dc_tts_reverse_len), 
				))
				gb_mn = list(genomictools.substract(
					genomictools.union(gff_mns),
					geneannotation._get_TSS_20240501(gff_mns, gb_dc_tss_forward_len, gb_dc_tss_reverse_len),
					geneannotation._get_TTS_20240501(gff_mns, gb_dc_tts_forward_len, gb_dc_tts_reverse_len), 
				))
				tss_pl = list(genomictools.union(geneannotation._get_TSS_20240501(gff_pls, tss_forward_len, tss_reverse_len)))
				tss_mn = list(genomictools.union(geneannotation._get_TSS_20240501(gff_mns, tss_forward_len, tss_reverse_len)))
				
				gb_lengths = sum(map(lambda b: len(b.genomic_pos), itertools.chain(gb_pl, gb_mn)))
				tss_lengths = sum(map(lambda b: len(b.genomic_pos), itertools.chain(tss_pl, tss_mn)))
				
				# Generate counts and output ratio
				tss_counts = sum(bwpl.value(r, method="abssum") for r in tss_pl) + sum(bwmn.value(r, method="abssum") for r in tss_mn)
				gb_counts = sum(bwpl.value(r, method="abssum") for r in gb_pl) + sum(bwmn.value(r, method="abssum") for r in gb_mn)

				if tss_lengths == 0 or tss_counts == 0 or gb_lengths == 0:
					dw.write([label, gb_counts, gb_lengths, tss_counts, tss_lengths, float("nan")])
				else:
					dw.write([label, gb_counts, gb_lengths, tss_counts, tss_lengths, (gb_counts / gb_lengths) / ((tss_counts / tss_lengths) + (gb_counts / gb_lengths))])
			
		else:
			raise Exception("Unknown mode")
		

#
# Others
#
@vt(
	description="Process and merge bed overlapped regions. Two criteria, min overlap length and min overlap ratio are used to define overlap between two regions.",
	helps=dict(
		i="Input bed files",
		o="Output bed file",
		stranded="If *true*, regions from different strands are never merged.",
		min_overlap_len="Minimum overlap length in bp to connect two regions",
		min_overlap_ratio="Minimum overlap ratio (of the smaller region) to connect two regions",		
	)
)
@vc
def _process_bed_overlapped_regions_20240501(i:list[str], o:str, stranded:convert_to_bool=False, min_overlap_len:int=1, min_overlap_ratio:float=0):
	import itertools
	from genomictools import GenomicCollection
	from biodata.bed import BED3, BED3Reader, BED3Writer, BED, BEDReader, BEDWriter
	from .utils import genomic
	if stranded:
		regions = list(itertools.chain.from_iterable([BEDReader.read_all(list, f) for f in i]))
		pl_regions = [r for r in regions if r.strand == "+"]
		mn_regions = [r for r in regions if r.strand == "-"]
		merged_pl_regions = genomic._merge_overlapped_regions_20240501(pl_regions, min_overlap_len=min_overlap_len, min_overlap_ratio=min_overlap_ratio)
		merged_mn_regions = genomic._merge_overlapped_regions_20240501(mn_regions, min_overlap_len=min_overlap_len, min_overlap_ratio=min_overlap_ratio)
		pl_beds = [BED(r.name, r.zstart, r.ostop, strand=r.strand) for r in merged_pl_regions]
		mn_beds = [BED(r.name, r.zstart, r.ostop, strand=r.strand) for r in merged_mn_regions]
		BEDWriter.write_all(GenomicCollection(pl_beds + mn_beds), o)
	else:
		regions = list(itertools.chain.from_iterable([BED3Reader.read_all(list, f) for f in i]))
		merged_regions = genomic._merge_overlapped_regions_20240501(regions, min_overlap_len=min_overlap_len, min_overlap_ratio=min_overlap_ratio)
		beds = [BED3(r.name, r.zstart, r.ostop) for r in merged_regions]
		BED3Writer.write_all(GenomicCollection(beds), o)

@vt(
	description="Modify fasta entries' names", 
	helps=dict(i="Input fasta file", o="Output fasta file", func="Function to modify bigwig. Either a python function or a string to be evaluated as python lambda function. For example, to add a prefix, `lambda x: \"PREFIX_\" + x`")
)
@vc
def _modify_fasta_names_20240515(i:str, o:str, func:str):
	'''
	Extract all intervals that overlap with the selected regions
	'''
	from biodata.fasta import FASTAReader, FASTAWriter
	if isinstance(func, str):
		func = eval(func, {}) # While unsafe to use eval, disable access to global variables to make it a little bit safer..
	with FASTAReader(i) as fr, FASTAWriter(o) as fw:
		for f in fr:
			f.name = func(f.name)
			fw.write(f)
@vt(
	description="Create a chrom size file from fasta", 
	helps=dict(i="Input fasta file", o="Output chrom size file")
)			
@vc
def _generate_chrom_size_20240501(i:str, o:str):
	from biodata.delimited import DelimitedWriter
	from biodata.fasta import FASTAReader
	with FASTAReader(i) as fr, DelimitedWriter(o) as dw:
		for f in fr:
			dw.write([f.name, len(f.seq)])
	
			
@vt(description="Modify bigwig values according to the func", 
	helps=dict(
		i="Input bigwig file",
		o="Output bigwig file", 
		func="Function to modify bigwig. Either a python function or a string to be evaluated as python lambda function. For example, to convert all positive values into negative values, `lambda x: x * -1`")
	)
@vc
def _modify_bigwig_values_20240423(i:str, o:str, func:str):
	'''
	'''
	import pyBigWig
	from commonhelper import safe_inverse_zip

	if isinstance(func, str):
		func = eval(func, {}) # While unsafe to use eval, disable access to global variables to make it a little bit safer..
	input_bw = pyBigWig.open(i)
	def _get_pyBigWig_all_interval_generator(bw):
		for chrom in bw.chroms():
			if bw.intervals(chrom) is not None:
				for interval in bw.intervals(chrom):
					yield (chrom, *interval)
	output_bw = pyBigWig.open(o, "w")
	output_bw.addHeader(list(input_bw.chroms().items()))
	all_intervals = list(_get_pyBigWig_all_interval_generator(input_bw))
	chroms, starts, ends, values = safe_inverse_zip(all_intervals, 4)
	values = list(map(func, values))
	output_bw.addEntries(list(chroms), list(starts), ends=list(ends), values=list(values))
	output_bw.close()
	input_bw.close()

@vt(
	description="Filter bigwig entries by chromosomes",
	helps=dict(
		i="Input bigwig file",
		o="Output bigwig file",
		chroms="Seleted chromosomes retained in the output"
	) 
)
@vc
def _filter_bigwig_by_chroms_20240501(i:str, o:str, chroms:list[str]):
	import pyBigWig
	from commonhelper import safe_inverse_zip

	input_bw = pyBigWig.open(i)
	output_bw = pyBigWig.open(o, "w")
	output_bw.addHeader(list(input_bw.chroms().items()))
	all_intervals = []
	for chrom in input_bw.chroms():
		if chrom in chroms and input_bw.intervals(chrom) is not None:
			for interval in input_bw.intervals(chrom):
				all_intervals.append([chrom, *interval])

	chroms, starts, ends, values = safe_inverse_zip(all_intervals, 4)
	output_bw.addEntries(list(chroms), list(starts), ends=list(ends), values=list(values))
	output_bw.close()
	input_bw.close()
@vt(
	description="Merge multiple bigwig files into one file. If the bigWig file contains negative data values, threshold must be properly set. An option remove_zero is added to remove entries with zero values.",
	helps=dict(
		i="Input bigwig files", g="chrom size file", o="output bigwig file",
		threshold="Threshold. Set to a very negative value, e.g. -2147483648, if your bigwig contains negative values.",
		adjust="Adjust",
		clip="Clip",
		max="Max",
		autosort="Perform sorting on bedgraph file before running bedGraphToBigWig. Set to *false* if you are sure that your input files are sorted to reduce running time.",
		filter_chr="Remove chromosomes in bedgraph file that are not present in chrom.sizes file", 
		nthread="Number of threads used in sorting"
	)
)
@vc
def _merge_bigwig_20240501(i:list[str], g:str, o:str, 
									threshold:float=None, adjust:float=None, clip:float=None, max:convert_to_bool=False, remove_zero:convert_to_bool=False,
									autosort=True, filter_chr=False, nthread=1):
	import os
	import tempfile
	
	check_binaries_validity("bigWigMerge", "sort", "bedGraphToBigWig")
	if len(i) <= 1:
		raise Exception("At least two input bigwig files are required for merging")
	bigWigMerge_cmd = "bigWigMerge"
	if threshold is not None:
		bigWigMerge_cmd += f" -threshold={threshold}"
	if adjust is not None:
		bigWigMerge_cmd += f" -adjust={adjust}"
	if clip is not None:
		bigWigMerge_cmd += f" -clip={clip}"
	if max:
		bigWigMerge_cmd += " -max"
	
	bw_files = " ".join(i)
	
	tmpfile_bgo = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
	if remove_zero:
		tmpfile = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
		bash_command(f"{bigWigMerge_cmd} {bw_files} {tmpfile}")
		bash_command("awk '{ if ($4 != 0) print $0 }' " + tmpfile + " > " + tmpfile_bgo)
		os.unlink(tmpfile)
	else:
		bash_command(f"{bigWigMerge_cmd} {bw_files} {tmpfile_bgo}")
	_convert_bedgraph_to_bigwig_20240501(tmpfile_bgo, g, o, autosort, filter_chr, nthread)
	os.unlink(tmpfile_bgo)
	
@vt(
	description="Subsample multiple bigwig files into target values. For example, if bwpl contains 100 counts and bwmn contains 200 counts, and n = 50, then sum of read counts in output_bwpl and output_mn will be 50 but the ratio of read counts is not kept at 1:2. This function assumes int value in bigwig value. This function supports positive / negative read counts.", 
	helps=dict(
		ibws="Input bigwig files",
		obws="Output bigwig files",
		n="Target number to subsample",
		seed="Random seed used in subsampling",
		)
)
@vc	
def _subsample_bigwig_20240501(ibws : list[str], obws : list[str], n : int, seed : int):
	from collections import Counter
	import random
	import pyBigWig
	def intervals_generator(bw):
		for chrom in bw.chroms():
		# This condition avoids problems if a chromosome info is included but the region is not
			if bw.intervals(chrom) is not None:
				for interval in bw.intervals(chrom):
					yield (chrom, *interval)

	random.seed(seed)
	
	ibws = [pyBigWig.open(bw) if isinstance(bw, str) else bw for bw in ibws]
	
	sorted_dicts = {}
	for idx, bw in enumerate(ibws):
		sorted_dicts[idx] = {k:i for i, k in enumerate(bw.chroms().keys())}
		
	all_locs = []
	all_abscounts = []
	all_counts = []
	for idx, bw in enumerate(ibws):
		loc, counts = list(zip(*[((idx, i[0], p + 1, i[3]>=0), i[3]) for i in intervals_generator(bw) for p in range(i[1], i[2])]))
		abscounts = list(map(lambda c: abs(int(c)), counts))
		all_locs.extend(loc)
		all_abscounts.extend(abscounts)
		all_counts.extend(counts)
	
	downsampled_rc = Counter(random.sample(all_locs, counts=all_abscounts, k=n))
	keys = sorted(downsampled_rc.keys(), key=lambda k: (k[0], sorted_dicts[k[0]][k[1]], k[2]))

	chroms = [[] for _ in range(len(ibws))]
	starts = [[] for _ in range(len(ibws))]
	ends = [[] for _ in range(len(ibws))]
	values = [[] for _ in range(len(ibws))]
	for k in keys:
		idx, chrname, p, is_positive = k
		cnt = downsampled_rc[k]
		chroms[idx].append(chrname)
		starts[idx].append(p - 1)
		ends[idx].append(p)
		values[idx].append(cnt * (1.0 if is_positive else -1.0))

	for idx, (ibw, obw_file) in enumerate(zip(ibws, obws)):
		obw = pyBigWig.open(obw_file, "w")
		obw.addHeader(list(ibw.chroms().items()))
		obw.addEntries(chroms[idx], starts[idx], ends[idx], values[idx])
		obw.close()	

@vt(
	description="Normalize bigwig files. ",
	helps=dict(
		ibws="Input bigwig files",
		obws="Output bigwig files",
		mode="Mode to normalize bigwig files. Only rpm is supported now.",
		nthread="Number of threads used to create normalized bigwig files."
	)
)
@vc
def _normalize_bigwig_20240501(ibws:list[str], obws:list[str], mode:str="rpm", nthread:int=-1): 
	import pyBigWig
	from mphelper import ProcessWrapPool, ProcessWrapState
	if len(ibws) != len(obws):
		raise Exception()
	if len(ibws) == 0:
		raise Exception()
	total = 0
	for ibw in ibws:
		with pyBigWig.open(ibw) as bw:
			total += abs(bw.header()["sumData"])
	if nthread == -1:
		nthread = len(ibws)
	pool = ProcessWrapPool(nthread)
	for ibw, obw in zip(ibws, obws):
		if mode == "rpm":
			pool.run(_modify_bigwig_values_20240423, kwargs={"i":ibw, "o":obw, "func":f"lambda i: i/{total}*1000000"})
		else:
			raise Exception()
	pool.get(wait=True)
	pool.close()
	for f in pool.futures.values():
		if f.state != ProcessWrapState.COMPLETE:
			raise Exception()
	
			
@vt(
	description="Subsample a bam file into exact number of entries. Alignments of n total reads (including unmapped reads) will be retrieved.", 
	helps=dict(
		i="Input bam file",
		o="Output bam file",
		n="Target number to subsample",
		seed="Random seed used in subsampling",
		nthread="Number of threads for compression"
	)
)
@vc
def _subsample_bam_20240501(i : str, o : str, n : int, seed : int, nthread : int = 1):
	import random
	import pysam
	
	ibam = pysam.AlignmentFile(i, "rb")
	all_read_names = sorted(set(read.qname for read in ibam.fetch(until_eof=True)))
	ibam.close()
	random.seed(seed)
	random.shuffle(all_read_names)
	if len(all_read_names) < n:
		raise Exception(f"Cannot subsample {n} reads from {len(all_read_names)} total reads.")
	selected = set(all_read_names[:n])
	ibam = pysam.AlignmentFile(i, "rb")
	obam = pysam.AlignmentFile(o, "wb", template=ibam, threads=nthread)
	for read in ibam.fetch(until_eof=True):
		if read.qname in selected:
			obam.write(read)
	obam.close()
	ibam.close()
@vt(
	description="Remove reads with any alignment that contain N in the CIGAR string. ",
	helps=dict(
		i="Input bam file",
		o="Output bam file",
		nthread="Number of threads used in compression"
	)
)
@vc
def _filter_bam_NCIGAR_reads_20240501(i : str, o : str, nthread : int = 1):
	import random
	import pysam
	ibam = pysam.AlignmentFile(i, "rb")
	to_remove = set(read.qname for read in ibam.fetch(until_eof=True) if 'N' in read.cigarstring)
	ibam.close()
	ibam = pysam.AlignmentFile(i, "rb")
	obam = pysam.AlignmentFile(o, "wb", template=ibam, threads=nthread)
	for read in ibam.fetch(until_eof=True):
		if read.qname not in to_remove:
			obam.write(read)
	obam.close()
	ibam.close()


@vt(
	description="Process bigwig into count table, either in a specific set of regions, or genomewide bins", 
	helps=dict(
		sample_names="Input sample names",
		i="Input bigwig files",
		o="Output count table file",
		region_file="A bed file containing regions to calculate bigwig counts",
		bin_size="If regions not provided, generate genomewide counts binned in bin_size",
		g="chrom size file. If provided, only use the selected chromosomes for genomewide counts",
	)
)
@vc
def _process_bigwigs_to_count_table_20240501(
		sample_names:list[str], i:list[str], o:str, 
		region_file:str=None, bin_size:int=None, g:str=None):
	from collections import defaultdict
	from biodata.bed import BED3Reader
	from biodata.bigwig import BigWigIReader
	from biodata.delimited import DelimitedReader, DelimitedWriter
	from genomictools import GenomicCollection
		
	def intervals_generator(bw, chroms=None):
		if chroms is None:
			chroms = bw.chroms()
		for chrom in chroms:
			if bw.intervals(chrom) is not None:
				for interval in bw.intervals(chrom):
					yield (chrom, *interval)
	if len(sample_names) != len(i):
		raise Exception("Number of sample names do not match number of bigwig files")				
	bws = [BigWigIReader(f) for f in i]
	if region_file is not None:
		regions = BED3Reader.read_all(GenomicCollection, region_file)
		with DelimitedWriter(o) as dw:
			dw.write([""] + sample_names)
			for r in regions:
				dw.write([str(r)] + [bw.value(r, "sum") for bw in bws])
	elif bin_size is not None:
		if g is None:
			chroms = None
		else:
			chroms = DelimitedReader.read_all(lambda ds: [d[0] for d in ds], g)
		covs = []
		for bw in bws:
			cov = defaultdict(int)
			for chrom, zstart, ostop, score in intervals_generator(bw.bw, chroms):
				for idx in range(zstart // bin_size, (ostop - 1) // bin_size + 1):
					l = min((idx + 1) * bin_size, ostop) - max(idx * bin_size, zstart)
					cov[chrom, idx] += l * score
			covs.append(cov)
		union_keys = sorted(set.union(*[set(cov.keys()) for cov in covs]))
		with DelimitedWriter(o) as dw:
			dw.write([""] + sample_names)
			for k in union_keys:
				dw.write([f"{k[0]}:{k[1]*bin_size+1}-{(k[1]+1)*bin_size}"] + [cov[k] if k in cov else 0 for cov in covs])
	else:
		raise Exception()		
	
@vt(
	description="Process count tables into a correlation table. Currently Pearson correlation is used.",
	helps=dict(
		i="Input files",
		o="Output file",
		filter_func="A function that takes in a pair of sample 1 and sample 2 count values to see if this pair should be retained or discarded",
		value_func="A function that modifies count values",
		keys="Only the selected samples are used to generate the correlation table"
	)
)
@vc
def _process_count_tables_to_correlation_table_20240501(i:list[str], o:str, filter_func=None, value_func=None, keys=None):
	import itertools
	from commonhelper import safe_inverse_zip
	from biodata.delimited import DelimitedReader, DelimitedWriter
	import math
	import numpy as np
	import scipy.stats
	tables = None
	for f in i:
		with DelimitedReader(f) as dr:
			header = dr.read()[1:]
			if keys is None:
				keys = header
			tmp_tables = safe_inverse_zip([list(map(float, d[1:])) for d in dr], len(keys))
			indice = [header.index(k) for k in keys]
			tmp_tables = [tmp_tables[idx] for idx in indice]
			if tables is None:
				tables = [list(t) for t in tmp_tables]
			else:
				for idx in range(len(keys)):
					tables[idx].extend(tmp_tables[idx])
	
	if filter_func is not None:
		filter_func = eval(filter_func, {})
	if value_func is not None:
		value_func = eval(value_func, {"math":math})
	with DelimitedWriter(o) as dw:
		dw.write(["Sample-1", "Sample-2", "Correlation"])
		for s1, s2 in itertools.combinations(range(len(keys)), 2):
			s1_values = []
			s2_values = []
			for a, b in zip(tables[s1], tables[s2]):
				if filter_func is None or filter_func(a, b):
					s1_values.append(a if value_func is None else value_func(a))
					s2_values.append(b if value_func is None else value_func(b))
			dw.write([keys[s1], keys[s2], scipy.stats.pearsonr(s1_values, s2_values)[0]])
			
			
#
# Gene annotation related tools
#
@vt(
	description="Generate a union TSS +x -y bp region for classifying distal / proximal regions.",
	helps=dict(
		i="Input gff file",
		o="Output file",
		forward_len="Length to extend in the forward strand. Use 1 if only TSS is chosen. For TSS-500bp to TSS+250bp, the region is 750bp long and forward_len should be set to 250.",
		reverse_len="Length to extend in the reverse strand. For TSS-500bp to TSS+250bp, the region is 750bp long and reverse_len should be set to 500.",
		filter_func="Function to filter the transcripts"
		)
)
@vc	
def _generate_union_TSS_20240501(
		i:str, o:str, forward_len:int, reverse_len:int, filter_func:str=None):
	from biodata.baseio import get_text_file_extension
	from biodata.bed import BED3Writer
	from biodata.gff import GFF3Reader, GTFReader
	import genomictools
	from genomictools import GenomicCollection
	from .utils import geneannotation
	
	if get_text_file_extension(i) == "gff3":
		gr = GFF3Reader(i)
	else:
		gr = GTFReader(i)
	if isinstance(filter_func, str):
		filter_func = eval(filter_func, {})
	regions = GenomicCollection(genomictools.union(geneannotation._get_TSS_20240501(gr, forward_len, reverse_len, filter_func=filter_func)))
	gr.close()	
	BED3Writer.write_all(regions, o)
	
@vt(
	description="Generate union transcripts regions.",
	helps=dict(
		i="Input gff file",
		o="Output file",
		filter_func="Function to filter the transcripts"
		)
		)
@vc	
def _generate_union_transcripts_20240501(
		i:str, o:str, filter_func:str=None):
	from biodata.baseio import get_text_file_extension
	from biodata.bed import BED3Writer
	from biodata.gff import GFF3Reader, GTFReader
	import genomictools
	from genomictools import GenomicCollection
	from .utils import geneannotation
	if get_text_file_extension(i) == "gff3":
		gr = GFF3Reader(i)
	else:
		gr = GTFReader(i)
	if isinstance(filter_func, str):
		filter_func = eval(filter_func, {})
	regions = GenomicCollection(genomictools.union(geneannotation._get_transcripts_20240501(gr, filter_func=filter_func)))
	gr.close()	
	BED3Writer.write_all(regions, o)
@vt(
	description="Filter genome annotations",
	helps=dict(
		i="Input genome annotation file",
		o="Output genome annotation file",
		filter_func="Function to filter genome annotations",
		remove_overlapping_genes="Remove overlapping genes",
		overlapping_genes_extension="Expand the genes before finding overlapping genes for removal"
	)
)
@vc
def _filter_geneannotations_20240501(
		i:str, o:str, 
		filter_func:str=None,
		remove_overlapping_genes:convert_to_bool=False,
		overlapping_genes_extension:int=0
	):
	from biodata.baseio import get_text_file_extension
	from biodata.bed import BED3Writer
	from biodata.gff import GFF3Reader, GTFReader, GFF3Writer, GTFWriter
	from .utils import geneannotation
	
	if get_text_file_extension(i) == "gff3":
		gr = GFF3Reader(i)
	else:
		gr = GTFReader(i)
	if get_text_file_extension(o) == "gff3":
		gw = GFF3Writer(o)
	else:
		gw = GTFWriter(o)
	if isinstance(filter_func, str):
		filter_func = eval(filter_func, {})
	if remove_overlapping_genes:
		gffs = list(gr)
		gffs = geneannotation._filter_out_overlapping_genes_20240501(gffs, overlapping_genes_extension)
	else: 
		gffs = gr
	for gff in gffs:
		if filter_func is None or filter_func(gff):
			gw.write(gff)
	gr.close()
	gw.close()
	
@vt(
	description="""Check sequencing files organized in a particular layout.
Your input i should be the raw_data directory as specified below

The directory has a layout as:
 
```
raw_data/
|___ LibraryName1/
|_______ MD5.txt
|_______ L1_1.fq.gz
|_______ L1_2.fq.gz
|___ LibraryName2/
|_______ MD5.txt
|_______ L2_1.fq.gz
|_______ L2_2.fq.gz
```
""",
	helps=dict(
		i="Input folder"
	)
)
@vc
def _check_sequencing_files_md5_20240501(i):
	import os
	import glob
	import subprocess
	from biodata.baseio import BaseReader
	
	check_binaries_validity("md5sum")
	
	print(f"Checking {i}")
	nd = 0
	n = 0
	m = 0
	for d in glob.glob(f"{i}/**/"):
		if not os.path.exists(f"{d}MD5.txt"):
			continue
		nd += 1
		with BaseReader(f"{d}MD5.txt") as br:
			for b in br:
				md5, fname = b.split()
				try:
					n += 1
					if not os.path.exists(f"{d}{fname}"):
						print(f"Warning! File does not exist: {d}{fname}")
						continue
					cal_md5 = subprocess.check_output(f"md5sum {d}{fname}", shell=True).decode().split()[0]
					if cal_md5 != md5:
						print(f"Warning! Data in {d}{fname} has error.")
						continue
					m += 1
				except:
					print(f"Warning! Error when running md5sum in {d}{fname}")
	print(f"MD5 check is done in {nd} directories.")
	print(f"Correct files: {m}/{n}") 
if __name__ == "__main__":
	main()

