# biodatatools

biodatatools is a package that provides a collection of useful commands `biodatatools command ...`, and utility functions *biodatatools.utils* for bioinformatics analysis. 

All commands are version controlled based on `simplevc` for backward compatibility. All results are reproducible by specifying the exact command version (with a few exceptions due to the change of dependent packages and call to external tools in some commands). 

The naming convention of commands is described below. 


- check - Check for certain information or file integrity. Usually the output is not parseable
- convert - Convert file into a different format while the stored data should remain the same
- downsample - Downsample data. Input and output data type should be the same
- filter - Create a new file that retains data entries matching the criteria
- generate - Generate new file that usually serves a different purpose than the input data.
- merge - Merge multiple files storing the same data types into one file
- modify - Create a new file with certain values modified
- process - Process files from one data type into some other data type. There could be less information stored after processing
- summarize - Summarize data statistics

Certain biodatatools commands require external tools. These are not installed along with biodatatools by default. If users run a command without the required tools, biodatatools would raise an error about the missing tools. 



## All Commands
### convert_bedgraph_to_bigwig
*version: 20240501*
Convert bedgraph into bigwig files.
#### Parameters
- **-i**: Input bedgraph file
- **-g**: Chrom size file
- **-o**: Output bigwig file
- **-autosort**: [optional] Perform sorting on bedgraph file before running bedGraphToBigWig. Set to *false* if you are sure that your input files are sorted to reduce running time. [default: True]
- **-filter_chr**: [optional] Remove chromosomes in bedgraph file that are not present in chrom size file [default: False]
- **-nthread**: [optional] Number of threads used in sorting [default: 1]
### process_PROcap_bam_to_bigwig
*version: 20240423*
Convert GROcap/PROcap/GROseq/PROseq bam file to bigwig files (paired-end reads). Returns 4 bigwig files representing 5' and 3' end of the molecules on plus or minus strand. See PRO-cap design for more explanations about rna_strand.
#### Parameters
- **-i**: Input bam file
- **-g**: Chrom size file
- **-o**: Output bigwig file prefix
- **-paired_end**: Specify *true* if paired-end sequencing and *false* for single-end sequencing
- **-rna_strand**: Indicate whether RNA strand is forward or reverse. In paired-end, forward implies that the first bp of read 1 is 5'. reverse implies that the first bp of read 2 is 5'
### process_PROcap_bam_to_TSS_RNA_len
*version: 20240501*
Convert GROcap/PROcap/GROseq/PROseq bam file to bed files Returns 2 bed files with the 4th column as a comma separated list of RNA distances from TSS.
#### Parameters
- **-i**: Input bam file
- **-o**: output bed file prefix. Two files, _dpl.bed.bgz and _dmn.bed.bgz are output
- **-paired_end**: Specify *true* if paired-end sequencing and *false* for single-end sequencing
- **-rna_strand**: Indicate whether RNA strand is forward or reverse. In paired-end, forward implies that the first bp of read 1 is 5'. reverse implies that the first bp of read 2 is 5'
- **-min_rna_len**: [optional] Minimum RNA length to record [default: 0]
- **-max_rna_len**: [optional] Maximum RNA length to record [default: 100000]
- **-g**: [optional] Chrom size file. If provided, only chromosomes in the chrom size file are retained. [default: None]
### merge_PROcap_TSS_RNA_len
*version: 20240430*
Merge PROcap TSS RNA len files.
#### Parameters
- **-i**: Input files
- **-o**: Output file
### summarize_PROcap_TSS_RNA_len
*version: 20240501*
Summarize the PROcap TSS RNA len files into min, median, mean and max of RNA lengths.
#### Parameters
- **-i**: Input files
- **-o**: Output file
### generate_genebody_TSS_ratio_table
*version: 20240501*
Generate gene body TSS ratio table. For capped RNA reads, the 5' end should be much more dominant near the promoter TSS region than the transcript region.	The ratio of gene body reads to TSS reads serves as a quality measure for capped RNA sequencing experiments.
#### Parameters
- **-label**: Sample labels
- **-ibwpl**: Input bigwig file (plus/sense strand on chromosomes)
- **-ibwmn**: Input bigwig file (minus/antisense strand on chromosomes)
- **-iga**: Input gene annotations used in calculating the gene body TSS ratio. One may want to pre-filter the annotations to get a specific set of genes prior to running this command.
- **-o**: Output file
- **-mode**: [optional] Only accept heg or all. In heg mode, only the specified ratio of top highly expressed genes are used to calculate the ratio. In all mode, all genes are used to calculate the ratio. [default: heg]
- **-gb_dc_tss_forward_len**: [optional] Forward len of discarded part around TSS when obtaining the gene body region [default: 500]
- **-gb_dc_tss_reverse_len**: [optional] Reverse len of discarded part around TSS when obtaining the gene body region [default: 0]
- **-gb_dc_tts_forward_len**: [optional] Forward len of discarded part around TTS when obtaining the gene body region [default: 1]
- **-gb_dc_tts_reverse_len**: [optional] Reverse len of discarded part around TTS when obtaining the gene body region [default: 499]
- **-tss_forward_len**: [optional] Forward len of TSS region [default: 500]
- **-tss_reverse_len**: [optional] Reerse len of TSS region [default: 0]
- **-heg_top_ratio**: [optional] In heg mode, the specified ratio of top expressed genes used for calculating gene body TSS ratio [default: 0.1]
- **-heg_tss_forward_len**: [optional] Forward len of TSS region when considering the gene expression [default: 1000]
- **-heg_tss_reverse_len**: [optional] Reverse len of TSS region when considering the gene expression [default: 100]
### process_bed_overlapped_regions
*version: 20240501*
Process and merge bed overlapped regions. Two criteria, min overlap length and min overlap ratio are used to define overlap between two regions.
#### Parameters
- **-i**: Input bed files
- **-o**: Output bed file
- **-stranded**: [optional] If *true*, regions from different strands are never merged. [default: False]
- **-min_overlap_len**: [optional] Minimum overlap length in bp to connect two regions [default: 1]
- **-min_overlap_ratio**: [optional] Minimum overlap ratio (of the smaller region) to connect two regions [default: 0]
### modify_fasta_names
*version: 20240515*
Modify fasta entries' names
#### Parameters
- **-i**: Input fasta file
- **-o**: Output fasta file
- **-func**: Function to modify bigwig. Either a python function or a string to be evaluated as python lambda function. For example, to add a prefix, `lambda x: "PREFIX_" + x`
### generate_chrom_size
*version: 20240501*
Create a chrom size file from fasta
#### Parameters
- **-i**: Input fasta file
- **-o**: Output chrom size file
### modify_bigwig_values
*version: 20240423*
Modify bigwig values according to the func
#### Parameters
- **-i**: Input bigwig file
- **-o**: Output bigwig file
- **-func**: Function to modify bigwig. Either a python function or a string to be evaluated as python lambda function. For example, to convert all positive values into negative values, `lambda x: x * -1`
### filter_bigwig_by_chroms
*version: 20240501*
Filter bigwig entries by chromosomes
#### Parameters
- **-i**: Input bigwig file
- **-o**: Output bigwig file
- **-chroms**: Seleted chromosomes retained in the output
### merge_bigwig
*version: 20240501*
Merge multiple bigwig files into one file. If the bigWig file contains negative data values, threshold must be properly set. An option remove_zero is added to remove entries with zero values.
#### Parameters
- **-i**: Input bigwig files
- **-g**: chrom size file
- **-o**: output bigwig file
- **-threshold**: [optional] Threshold. Set to a very negative value, e.g. -2147483648, if your bigwig contains negative values. [default: None]
- **-adjust**: [optional] Adjust [default: None]
- **-clip**: [optional] Clip [default: None]
- **-max**: [optional] Max [default: False]
- **-remove_zero**: [optional] _ [default: False]
- **-autosort**: [optional] Perform sorting on bedgraph file before running bedGraphToBigWig. Set to *false* if you are sure that your input files are sorted to reduce running time. [default: True]
- **-filter_chr**: [optional] Remove chromosomes in bedgraph file that are not present in chrom.sizes file [default: False]
- **-nthread**: [optional] Number of threads used in sorting [default: 1]
### subsample_bigwig
*version: 20240501*
Subsample multiple bigwig files into target values. For example, if bwpl contains 100 counts and bwmn contains 200 counts, and n = 50, then sum of read counts in output_bwpl and output_mn will be 50 but the ratio of read counts is not kept at 1:2. This function assumes int value in bigwig value. This function supports positive / negative read counts.
#### Parameters
- **-ibws**: Input bigwig files
- **-obws**: Output bigwig files
- **-n**: Target number to subsample
- **-seed**: Random seed used in subsampling
### normalize_bigwig
*version: 20240501*
Normalize bigwig files. 
#### Parameters
- **-ibws**: Input bigwig files
- **-obws**: Output bigwig files
- **-mode**: [optional] Mode to normalize bigwig files. Only rpm is supported now. [default: rpm]
- **-nthread**: [optional] Number of threads used to create normalized bigwig files. [default: -1]
### subsample_bam
*version: 20240501*
Subsample a bam file into exact number of entries. Alignments of n total reads (including unmapped reads) will be retrieved.
#### Parameters
- **-i**: Input bam file
- **-o**: Output bam file
- **-n**: Target number to subsample
- **-seed**: Random seed used in subsampling
- **-nthread**: [optional] Number of threads for compression [default: 1]
### filter_bam_NCIGAR_reads
*version: 20240501*
Remove reads with any alignment that contain N in the CIGAR string. 
#### Parameters
- **-i**: Input bam file
- **-o**: Output bam file
- **-nthread**: [optional] Number of threads used in compression [default: 1]
### process_bigwigs_to_count_table
*version: 20240501*
Process bigwig into count table, either in a specific set of regions, or genomewide bins
#### Parameters
- **-sample_names**: Input sample names
- **-i**: Input bigwig files
- **-o**: Output count table file
- **-region_file**: [optional] A bed file containing regions to calculate bigwig counts [default: None]
- **-bin_size**: [optional] If regions not provided, generate genomewide counts binned in bin_size [default: None]
- **-g**: [optional] chrom size file. If provided, only use the selected chromosomes for genomewide counts [default: None]
### process_count_tables_to_correlation_table
*version: 20240501*
Process count tables into a correlation table. Currently Pearson correlation is used.
#### Parameters
- **-i**: Input files
- **-o**: Output file
- **-filter_func**: [optional] A function that takes in a pair of sample 1 and sample 2 count values to see if this pair should be retained or discarded [default: None]
- **-value_func**: [optional] A function that modifies count values [default: None]
- **-keys**: [optional] Only the selected samples are used to generate the correlation table [default: None]
### generate_union_TSS
*version: 20240501*
Generate a union TSS +x -y bp region for classifying distal / proximal regions.
#### Parameters
- **-i**: Input gff file
- **-o**: Output file
- **-forward_len**: Length to extend in the forward strand. Use 1 if only TSS is chosen. For TSS-500bp to TSS+250bp, the region is 750bp long and forward_len should be set to 250.
- **-reverse_len**: Length to extend in the reverse strand. For TSS-500bp to TSS+250bp, the region is 750bp long and reverse_len should be set to 500.
- **-filter_func**: [optional] Function to filter the transcripts [default: None]
### generate_union_transcripts
*version: 20240501*
Generate union transcripts regions.
#### Parameters
- **-i**: Input gff file
- **-o**: Output file
- **-filter_func**: [optional] Function to filter the transcripts [default: None]
### filter_geneannotations
*version: 20240501*
Filter genome annotations
#### Parameters
- **-i**: Input genome annotation file
- **-o**: Output genome annotation file
- **-filter_func**: [optional] Function to filter genome annotations [default: None]
- **-remove_overlapping_genes**: [optional] Remove overlapping genes [default: False]
- **-overlapping_genes_extension**: [optional] Expand the genes before finding overlapping genes for removal [default: 0]
### check_sequencing_files_md5
*version: 20240501*
Check sequencing files organized in a particular layout.
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

#### Parameters
- **-i**: Input folder