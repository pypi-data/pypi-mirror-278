import sys
import simplevc
simplevc.register(sys.modules[__name__])

from commonhelper import cluster_by_linkages
from genomictools import GenomicPos, GenomicCollection
import heapq

@vc
def _merge_overlapped_regions_20240501(*regions, min_overlap_len=1, min_overlap_ratio=0):
	'''
	Unlist all regions
	Create link between two regions if they overlap
	For each set of linked regions, merge them as one region
	
	min_overlap_ratio is calculated by the smaller region
	'''
	gc = sorted([GenomicPos(r) for rs in regions for r in rs])
	arr = []
	linkages = []
	for r in gc:
		linkages.append([r,r])
		while len(arr) > 0 and (arr[0][0] != r.name or arr[0][1] < r.start):
			heapq.heappop(arr)
		for trx in sorted(arr):
			tr = trx[2]
			overlap_len = min(r.stop, tr.stop) - max(r.start, tr.start) + 1
			if overlap_len >= min_overlap_len and overlap_len / min(len(r), len(tr)) >= min_overlap_ratio:
				linkages.append([r, tr])
		heapq.heappush(arr, (r.name, r.stop, r))
		
	clusters = list({id(cluster):cluster for cluster in cluster_by_linkages(linkages).values()}.values())
	return GenomicCollection([GenomicPos(next(iter(cluster_regions)).name, min(cr.start for cr in cluster_regions), max(cr.stop for cr in cluster_regions)) for cluster_regions in clusters])
