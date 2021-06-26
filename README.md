# 3D Flower Meristem at stage 4

## Content
1) Repo Description
2) Web App
3) Available Files
4) References

## 1) Repo Description
This repository stores files for a web-app (built with Dash, Plotly and CSS in Python)  
that is deployed via Heroku on https://threed-flower-meristem.herokuapp.com, summarizing the main results of our recent paper "A 3D gene expression atlas of a floral meristem based on spatial mapping of single nucleus RNA sequencing data" in < Journal > [1]. Additionally, all relevant files to recreate those results are made available and described in the section 'Available Files', below.

## 2) Web App
The web-app allows to view the predicted (via NovoSpaRc [2]) gene expression profiles of a selected (via PEP-score) set of ~ 1,000 genes in a 3D model of the developing A. Thaliana flower meristem at stage 4 [1]. See picture below.   
Next to that, also the UMAP clustering (from scRNA-seq data at stage 4) can be viewed in the 3D model, which has been obtained by a probabilistic mapping of single cells to cells in 3D model via NovoSpaRc [1].   

<p align="center">
  <img src="https://user-images.githubusercontent.com/43107602/115282708-cd5ce080-a14a-11eb-94c4-e2c2f03e11fc.png"        height="391.75" width="375">
 </p>

## 3) Available Files
### umap_clusters.csv
    The UMAP coordinates of scRNA-seq cells and their cluster assignment.

### pep.csv
    Predicted Expression Performance (PEP) score for all genes in ‘dge_top_1000_genes.csv’ with TAIR ID and gene symbol.

### dge_top_1000_genes.csv
    matrix of shape cells x genes, containing predicted 3D gene expression profiles over all cells in 3D flower meristem model. Only genes with a PEP > 0.13 are included.

### confocal_states0-FilterWUSCLVtop100.csv
    matrix of shape cells x genes, containing binary expression profiles of 28 marker genes over all cells in 3D flower meristem model [ref]. Binary expression was obtained via manual annotation [ref]. matrix also contains 3D coordinates of cells, cell volume and cell ID.

### cluster_anno.csv
    cell/tissue – type annotation of scRNA-seq cell clusters in UMAP space.

### ALLGENES_ns_2_nt_5_alpha_0.1_epsilon_0.05_top_sccells_50_top_hvg_100_1000genes.txt
    matrix of shape cells x genes, containing predicted 3D gene expression profiles over all cells in 3D flower meristem model. Same as ‘dge_top_1000_genes.csv’, except that no predicted genes were selected based on PEP score.

### 3d_clusters.csv
    Probabilistic assignment of clusters 0-12 to all cells in the 3D flower meristem model.

# 4) References
[1] Neumann Manuel, Xu Xiaocai., ...   
[2] novosparc   
[3] Refahi, Y., Zardilis, A., Michelin, G., Wightman, R., Leggio, B., Legrand, J., Faure, E., Vachez, L., Armezzani, A., Risson, A.-E., Zhao, F., Das, P., Prunet, N., Meyerowitz, E., Godin, C., Malandain, G., Jönsson, H., & Traas, J. (2020). A multiscale analysis of early flower development in Arabidopsis provides an integrated view of molecular regulation and growth control. BioRxiv, 2020.09.25.313312.   



