import argparse
import json

from SeuratObject import SeuratObjectRDS
from sc_ssGSEA_helper import *

parser = argparse.ArgumentParser()

parser.add_argument(
	"--input_file",
	type=str,
	help="Input file",
	default='False'
)

parser.add_argument(
	"--gene_set_database_file",
	type=str,
	help="gene set database file(s)",
	default='False'
)

parser.add_argument(
	"--output_file_name",
	type=str,
	help="filename to use for output files",
	default='False'
)

parser.add_argument(
	"--n_threads",
	type=str,
	help="job CPU count",
	default = 1
)

parser.add_argument(
	"--cluster_data_label",
	type=str,
	help="Metadata label to use for aggregating cells",
	default="seurat_clusters"
)

parser.add_argument(
	"--chip_file",
	type=str,
	help="chip file",
	default = None
)

args = parser.parse_args()

## Load and parse Seurat RDS
so = SeuratObjectRDS(
	filepath = args.input_file
)
so.load_tokens()
so.parse_header()
so.parse_data(tabs = 0)

with open("full_test.json", 'w') as f:
	f.write(json.dumps(so.data))

## Get normalized metacells
metacell_df = get_metacells(so, args.cluster_data_label)


## Load gene sets
gs, gs_desc = read_gmt(args.gene_set_database_file)


## Run sc_ssGSEA
sc_ssGSEA_scores = run_ssgsea_parallel(
	metacell_df,
	gs,
	n_job = args.n_threads,
	file_path = None
)


## Save results
sc_ssGSEA_scores.to_csv(
	args.output_file_name+".tsv",
	sep = '\t'
)









