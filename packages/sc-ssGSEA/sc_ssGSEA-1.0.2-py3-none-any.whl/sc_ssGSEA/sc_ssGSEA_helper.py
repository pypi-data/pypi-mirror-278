#!/usr/bin/env python3
#NB - all of these import statements should specify their versions and be executed in a separate script at Docker build time.

import pandas as pd
import numpy as np
from numpy import absolute, in1d, nan, full
from numpy.random import seed
from warnings import warn
from multiprocessing.pool import Pool
from scipy.sparse import csr_matrix
from typing import List, Optional, Tuple, TypedDict, Union
import sys

from SeuratObject import SeuratObjectRDS


## CLR normalization function
def clr(vec: List[float]) -> List[float]:
    """
    https://www.geo.fu-berlin.de/en/v/soga-r/Advances-statistics/Feature-scales/Logratio_Transformations/index.html
    
    https://github.com/satijalab/seurat/blob/HEAD/R/preprocessing.R
    return(log1p(x = x / (exp(x = sum(log1p(x = x[x > 0]), na.rm = TRUE) / length(x = x)))))
    """
    denom = np.exp(sum([np.log1p(x) for x in vec[vec>0]])/len(vec))
    
    return [np.log1p(x/denom) for x in vec]
    

## Build normalized metacells
def get_metacells(
    so: SeuratObjectRDS,
    group_col_name: str
) -> pd.DataFrame:
    """
    Interpreter for the SeuratObjectRDS.data field since it needs to be
    cleaned up still. 
    """
    ## Parse counts matrix and row names
    
    ## I'm so sorry. I will have enough time to fix this someday.
    i_vec = so.data[0][0]["assays"]["val"][0][0]["counts"]["val"][0]["i"]["val"]["val"]
    p_vec = so.data[0][0]["assays"]["val"][0][0]["counts"]["val"][1]["p"]["val"]["val"]
    x_vec = so.data[0][0]["assays"]["val"][0][0]["counts"]["val"][4]["x"]["val"]["val"]
    
    nrow, ncol = so.data[0][0]["assays"]["val"][0][0]["counts"]["val"][2]["Dim"]["val"]["val"]

    dimnames = so.data[0][0]["assays"]["val"][0][0]["counts"]["val"][3]["Dimnames"]
    rownames = dimnames["val"][0]
    colnames = dimnames["val"][1]
    
    nz_row = []
    nz_col = []
    nz_val = []
    
    xi_cursor = 0
    
    for col_cursor in range(2, len(p_vec)):
        n_vals_in_col = p_vec[col_cursor] - p_vec[col_cursor - 1]
        
        for _ in range(n_vals_in_col):
            nz_row.append(i_vec[xi_cursor])
            nz_col.append(col_cursor - 1)
            nz_val.append(x_vec[xi_cursor])
            
            xi_cursor += 1
            
    sparse_mat = csr_matrix((nz_val, (nz_row, nz_col)))
    
    ## Normalize
    for i in range(0, sparse_mat.shape[0]):
        dense_row = sparse_mat[i,:].toarray()[0]
        
        if all(dense_row == 0):
            continue
        
        norm_dense_row = clr(dense_row)
        
        for j in range(len(norm_dense_row)):
            if norm_dense_row[j] != 0:
                sparse_mat[i,j] = norm_dense_row[j]
    
    ## Parse metadata grouping
    
    ## Seurat parser currently stores dataframe colnames in subsequent entries because it reduces 
    ## recursive parsing depth too quickly. Needs to be fixed, and then this code will be more intuitive
    #md_indx = None

    md_data = so.data[0][2]["meta.data"]["val"]
    md_colnames = so.data[0][7]["names"]["val"]
    md_rownames = so.data[0][6]["row.names"]["val"]
    
    group_col_indx = md_colnames.index(group_col_name)
    
    group_s = pd.Series(
        md_data[group_col_indx]["val"],
        index = md_rownames
    )
    
    ## Build metacells
    levels = group_s.unique()
    
    mc_d = {}
    
    for level in levels:
        colnames_with_level = group_s[group_s == level].index.tolist()
        
        level_inds = [
            group_s.index.tolist().index(colname)
            for colname in colnames_with_level
        ]
        
        mc_d[f"sc-ssGSEA-group_{level}"] = sparse_mat[:,level_inds].T.mean(axis = 0).tolist()[0]
        
    mc_df = pd.DataFrame(mc_d, index = rownames)
    
    return mc_df


# ssGSEA code from PheNMF repository
def single_sample_gsea(
    gene_score,
    gene_set_genes,
    plot=True,
    title=None,
    gene_score_name=None,
    annotation_text_font_size=16,
    annotation_text_width=88,
    annotation_text_yshift=64,
    html_file_path=None,
    plotly_html_file_path=None,
):

    gene_score = gene_score.dropna()
    gene_score_sorted = gene_score.sort_values(ascending=False)

    in_ = in1d(gene_score_sorted.index, gene_set_genes.dropna(), assume_unique=True)
    in_sum = in_.sum()

    if in_sum == 0:
        warn("Gene scores did not have any of the gene-set genes.")
        return

    gene_score_sorted_values = gene_score_sorted.values
    gene_score_sorted_values_absolute = absolute(gene_score_sorted_values)

    in_int = in_.astype(int)
    hit = (
        gene_score_sorted_values_absolute * in_int
    ) / gene_score_sorted_values_absolute[in_].sum()

    miss = (1 - in_int) / (in_.size - in_sum)
    y = hit - miss
    cumulative_sums = y.cumsum()
    
    # KS scoring
    max_ = cumulative_sums.max()
    min_ = cumulative_sums.min()
    if absolute(min_) < absolute(max_):
        score = max_
    else:
        score = min_

    return score

def read_chip(chip):
    chip_df=pd.read_csv(chip, sep='\t', index_col=0, skip_blank_lines=True)
    return chip_df

def convert_to_gene_symbol(chip, exp):
    joined_df = chip.join(exp, how='inner')
    joined_df.reset_index(drop=True, inplace=True)
    annotations = joined_df[["Gene Symbol", "Gene Title"]].drop_duplicates().copy()
    joined_df.drop("Gene Title", axis = 1, inplace = True)

    # Collapse the expression of duplicate genes using the sum of expression
    collapsed_df = joined_df.groupby(["Gene Symbol"]).sum()
    return collapsed_df

def write_gct(out_matrix, filename, gs_desc):
    # Add "Description" column 
    out_matrix.insert(0, "Description", gs_desc)

    text_file = open(filename + ".gct", "w")
    text_file.write('#1.2\n' + str(len(out_matrix)) + "\t" +
                        str(len(out_matrix.columns)-1) + "\n")

    # Save GCT file
    out_matrix.to_csv(text_file, sep="\t", index_label = "NAME", mode='a')
    print("Saved scGSEA score result in .gct format")
    
def read_gmt(gs_db, thres_min=2, thres_max=2000):
    with open(gs_db) as f:
        temp=f.read().splitlines()
    max_Ng=len(temp)
    # temp_size_G will contain size of each gene set
    temp_size_G=list(range(max_Ng))
    for i in range(max_Ng):
        temp_size_G[i]=len(temp[i].split("\t")) - 2
    max_size_G=max(temp_size_G)
    gs=pd.DataFrame(np.nan, index=range(max_Ng), columns=range(max_size_G))
    temp_names=list(range(max_Ng))
    temp_desc=list(range(max_Ng))
    gs_count=0
    for i in range(max_Ng):
        gene_set_size=len(temp[i].split("\t")) - 2
        gs_line=temp[i].split("\t")
        gene_set_name=gs_line[0]
        gene_set_desc=gs_line[1]
        gene_set_tags=list(range(gene_set_size))
        for j in range(gene_set_size):
            gene_set_tags[j]=gs_line[j + 2]
        if np.logical_and(gene_set_size >= thres_min, gene_set_size <= thres_max):
            temp_size_G[gs_count]=gene_set_size
            gs.iloc[gs_count]=gene_set_tags + \
                list(np.full((max_size_G - temp_size_G[gs_count]), np.nan))
            temp_names[gs_count]=gene_set_name
            temp_desc[gs_count]=gene_set_desc
            gs_count=gs_count + 1
    Ng=gs_count
    gs_names=list(range(Ng))
    gs_desc=list(range(Ng))
    size_G=list(range(Ng))
    gs_names=temp_names[0:Ng]
    gs_desc=temp_desc[0:Ng]
    size_G=temp_size_G[0:Ng]
    gs.dropna(how='all', inplace=True)
    gs.index=gs_names
    return gs, gs_desc
#    return {'N_gs': Ng, 'gs': gs, 'gs_names': gs_names, 'gs_desc': gs_desc, 'size_G': size_G, 'max_N_gs': max_Ng}

def read_gmts(gs_dbs):
    gs = pd.DataFrame()
    gs_desc = []
    with open(gs_dbs, "r") as file:
        for gs_db in file:
            gs_db = gs_db.rstrip('\n')
            gs_temp, gs_desc_temp = read_gmt(gs_db)
            gs = pd.concat([gs, gs_temp], ignore_index=False)
            gs_desc.extend(gs_desc_temp)
    return gs, gs_desc

## utilities from ccal
def split_df(df, axis, n_split):

    if not (0 < n_split <= df.shape[axis]):
        raise ValueError(
            "Invalid: 0 < n_split ({}) <= n_slices ({})".format(n_split, df.shape[axis])
        )
    n = df.shape[axis] // n_split
    dfs = []
    for i in range(n_split):
        start_i = i * n
        end_i = (i + 1) * n

        if axis == 0:
            dfs.append(df.iloc[start_i:end_i])
        elif axis == 1:
            dfs.append(df.iloc[:, start_i:end_i])
    i = n * n_split

    if i < df.shape[axis]:
        if axis == 0:
            dfs.append(df.iloc[i:])
        elif axis == 1:
            dfs.append(df.iloc[:, i:])
    return dfs

def multiprocess(callable_, args, n_job, random_seed=20121020):
    seed(random_seed)
    with Pool(n_job) as process:
        return process.starmap(callable_, args)

## From ccal (credit Kwat, Pablo)
def _single_sample_gseas(gene_x_sample, gene_sets):
    print("Running single-sample GSEA with {} gene sets ...".format(gene_sets.shape[0]))

    score__gene_set_x_sample = full((gene_sets.shape[0], gene_x_sample.shape[1]), nan)
    for sample_index, (sample_name, gene_score) in enumerate(gene_x_sample.items()):
        for gene_set_index, (gene_set_name, gene_set_genes) in enumerate(
            gene_sets.iterrows()
        ):
            score__gene_set_x_sample[gene_set_index, sample_index] = single_sample_gsea(
                gene_score, gene_set_genes, plot=False
            )
    score__gene_set_x_sample = pd.DataFrame(
        score__gene_set_x_sample, index=gene_sets.index, columns=gene_x_sample.columns
    )
    return score__gene_set_x_sample

## Alex's function for parallelization
def run_ssgsea_parallel(
    gene_x_sample,
    gene_sets,
    n_job = 1,
    file_path = None
):
    """
    Wrapper around Kwat's ssGSEA except it parallelizes based on samples instead
    of gene sets. The PheNMF uses case assumes #samples >>> #gene sets

        gene_x_sample (pd.DataFrame): Matrix of genes by samples
        gene_sets (pd.DataFrame): CCAL-style GMT representation
        n_job (int): Number of processors to use
        file_path (str|None): Path to store ssGSEA results if desired
    """

    """
    if n_job <= gene_x_sample.shape[1]:
        print("Parallelizing scGSEA across cell clusters")
        score__gene_set_x_sample = pd.concat(
            multiprocess(
                _single_sample_gseas,
                (
                    (gene_x_sample_, gene_sets)
                    for gene_x_sample_ in split_df(gene_x_sample, 1, min(gene_x_sample.shape[1], n_job))
                ),
                n_job,
            ), sort = False, axis = 1
        )
        
    else:
        print("Parallelizing scGSEA across gene sets")
        score__gene_set_x_sample = pd.concat(
            multiprocess(
                _single_sample_gseas,
                (
                    (gene_x_sample, gene_sets_)
                    for gene_sets_ in split_df(gene_sets, 0, min(gene_sets.shape[0], n_job))
                ),
                n_job,
            ), sort = False, axis = 0
        )
    """
    score__gene_set_x_sample = _single_sample_gseas(
        gene_x_sample,
        gene_sets
    )

    ## Assure columns come out in same order they came in
    score__gene_set_x_sample = score__gene_set_x_sample[gene_x_sample.columns]

    if file_path is not None:
        score__gene_set_x_sample.to_csv(file_path, sep = '\t')

    return score__gene_set_x_sample
