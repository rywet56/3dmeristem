path <- '/Users/manuel/SeaDrive/Shared with groups/ManuelProject0/Confocal-scRNA/paper/OLD/FinalDatasets/ALLGENES_ns_2_nt_5_alpha_0.1_epsilon_0.05_top_sccells_50_top_hvg_100.txt'
dge <- read.csv(path, row.names = 1)
dge <- as.data.frame(t(dge))

path <- "/Users/manuel/SeaDrive/Shared with groups/ManuelProject0/Confocal-scRNA/paper/OLD/FinalDatasets/PEP_spearman_enrDGEjose_allgenes_final.csv"
pep <- read.csv(file = path, row.names = 1)
ord <- order(pep$top_spear_cor, decreasing = TRUE)
ord_genes <- rownames(pep)[ord]

# ord_genes <- names(pep)[order(pep, decreasing = TRUE)]
# dge_top1000 <- dge[, ord_genes[1:1000]]
# path <- ""
# write.csv(x = dge_top1000, file = path)

# pepj <- pep


library(annotate)
library(org.At.tair.db)
genes <- ord_genes
symbols <- NULL
for(gene in genes){
  k <- getSYMBOL(gene, data='org.At.tair.db')
  symb <- as.character(k[length(k)])
  symbols <- c(symbols, symb)
}
symbols <- toupper(symbols)
pep_new <- pep[ord_genes, ]
pep_new$symbol <- symbols
pep_new$tair <- rownames(pep_new)
pep_new <- pep_new[, c("symbol", "tair", "top_spear_cor")]
pep_new$symbol <- as.character(sapply(X = pep_new$symbol, FUN = function(x){if(is.na(x)){"None"}else{x}}))
path <- "/Users/manuel/OneDrive/git_hub_repos/3dmeristem/datasets/pep.csv"
write.csv(x = pep_new, file = path)

# temp
####
getSYMBOL(genes[2], data='org.At.tair.db')

####

# p <- read.csv(path, row.names = 1)
# p[20:40,]
# pep[order(pep, decreasing = TRUE)][20:40]


# top_1000_genes <- pep_new[1:1000, "tair"]
top_1000_genes <- pep_new[pep_new$top_spear_cor > 0.13, "tair"]; length(top_1000_genes)
dge_top_1000_genes <- dge[,top_1000_genes]
dge_top_scaled <- scale(dge_top_1000_genes)
path <- "/Users/manuel/OneDrive/git_hub_repos/3dmeristem/datasets/dge_top_1000_genes.csv"
write.csv(x = dge_top_scaled, file = path)










