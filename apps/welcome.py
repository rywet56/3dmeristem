import dash_core_components as dcc
import dash_html_components as html

text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in"
p1 = "We (Kaufmann Lab) want to provide the flower development community access to the predicted and so far, " \
     "unknown 3D gene expression patterns in the developing floral meristem. This data is available in an interactive " \
     "way and can also be downloaded in order to access it programmatically. "
p2 = "Developmental processes, that means the developmental trajectory a cell traverse, are the result of precise " \
     "molecular changes at the level of the chromatin, genome and transcriptome. The spatial context of cells plays " \
     "an important role in all those processes in the way that global patterns of effector molecules determine a " \
     "cells relative position and therefore it’s role within the developing organism. In the context of A. thaliana " \
     "flower development, the cell wall composition of cells on the outermost layer of the meristem are subject to a " \
     "constant remodeling, allowing the directed growth rates from cells within the meristem influence the expansion " \
     "of the overall meristem in defined directions. The identity of those inner cells are themselves defined by the " \
     "action of molecular machines (proteins), controlled by signaling pathways which are established through the " \
     "fine-tuned regulation of gene expression. In that sense, gene regulation controls the developing morphology and " \
     "function of the flower meristem "
p3 = "For that reason, it is very important to understand gene expression patterns, the chromatin landscape and " \
     "eventually gene-regulatory mechanisms, that lead to a well-defined biochemistry of an organisms, " \
     "in their spatial context. At this point, only a few dozen marker genes involved in floral meristem development " \
     "are known and have been mapped to a 3D model (reference). But in order to understand developmental processes, " \
     "the knowledge of a lot more and at best nearly all genes has to be understood in a spatial 3D context. "
p4 = "Unfortunately, the experimental access to this type of data through confocal imaging and 3D reconstruction is " \
     "limited due to the difficulty of obtaining promotor constructs for all genes as well as screening them in a " \
     "high-throughput way. To that end we (Kaufmann Lab) developed a computational framework (reference) that allows " \
     "the prediction of 3D gene expression patterns in the flower meristem, only with the knowledge of scRNA-seq data " \
     "and a handful of marker genes whose 3D expression patterns has been mapped manually in a binary format (" \
     "reference). "
p5 = "The underlying workhorse is the application of Optimal Transport to reconstruct spatial expression patterns in " \
     "a probabilistic sense, as implemented in novoSpaRc (reference). We improved this method by developing a range " \
     "of pre-processing steps such as cell-selection and cell-enrichment, which help novoSpaRc to map single-cells to " \
     "the 3D model in a probabilistic sense. Most notably, the extension of this method (called novosparc +) improves " \
     "upon the original novoSpaRc method in the way that it allows the prediction of spatial expression patterns with " \
     "a very small set (~20) of marker genes. Furthermore, novosparc + can in principle be applied to the 3D/2D gene " \
     "expression patterns in any organism (more in the section “Beyond the floral meristem”)."
p6 = html.Div([
    html.P(["This website provides the two main results of our paper “paper title”, that is the predicted expression "
            "of the top 1,000 genes* and the probabilistic mapping of clusters in UMAP space from the scRNA-seq data "
            "onto the 3D flower meristem model, in an interactive way. In order to access the predicted expression "
            "profiles of the top 1,000 genes click on the 3D meristem Button. For accessing the scRNA-seq UMAP "
            "clusters whose single cells were mapped onto the 3D Meristem, click the 3D clusters button."],
           className="text"),
    html.P(["* The confidence in our predictions, that means how confident we are that our prediction is indeed close "
            "to the “true” expression profiles, is evaluated with the PEP (Predicted ExPression) score. This score "
            "was used to select the top 1,000 genes for whose prediction we have a high confidence."], className="text")
])

p7 = html.Div([
    html.P(["The novosparc + tool can in principle be applied to the 2D/3D reconstruction of gene expression profiles "
            "in any organism. The successful reconstruction requires a set of high-quality marker genes as well as a "
            "single-cell RNA-seq dataset that fits the time point of the marker gene expression profiles. "
            "Furthermore, it is strongly recommended to scan the parameter space in order to identify a set of "
            "parameter combinations that are able to predict the 3D expression profiles of marker gene with high "
            "accuracy (AUC => 0.9), as described in our paper [reference]. This optimization (parameter sweep) for "
            "different organs, stages and organisms is crucial since the morphology and as a result the gene "
            "expression patterns differ greatly among them."], className="text")
])

p8 = html.Div([
    html.P([
        "The predicted 3D expression as well as the 3D cluster mapping can be accessed by either Forking the GitHub "
        "repository ",
        html.A([html.B([html.U(['3D Meristem'])], style={"color": "#77b300"})],
               href="https://github.com/rywet56/3dmeristem"),
        " or by clicking on the button 'GET 3D Expression' and 'GET 3D Clusters' below.",

    ], className="text")
])

page_3 = html.Div([
    # SPACER
    html.Div([], className='colm', style={"flex": "1 1 0"
                                          # ,"background-color": "red"
                                          }
             ),
    html.Div([
        html.H1(["Why this page?"], className="header_1"),
        html.P([p1], className="text"),

        html.H1(["How to use this page ?"], className="header_1"),
        p6,

        html.H1(["The biological question"], className="header_1"),
        html.P([p2], className="text"), html.P([p3], className="text"),

        html.H1(["Our approach to answer this question"], className="header_1"),
        html.P([p4], className="text"),

        html.H1(["The computational framework – novosparc +"], className="header_1"),
        html.P([p5], className="text"),

        html.H1(["Beyond the floral meristem - other organisms"], className="header_1"),
        p7,

        html.H1(["Data Access"], className="header_1"),
        p8,
        html.Div([
            html.Div([""], className="colm"),
            html.Div([
                html.A(["GET 3D EXPRESSION"], className="custom-button",
                       href="https://raw.githubusercontent.com/rywet56/3dmeristem/main/datasets/ALLGENES_ns_2_nt_5_alpha_0.1_epsilon_0.05_top_sccells_50_top_hvg_100_1000genes.txt")
            ], className="colm"),
            html.Div([""], className="colm"),
            html.Div([
                html.A(["GET 3D CLUSTERS"], className="custom-button",
                       href="https://raw.githubusercontent.com/rywet56/3dmeristem/main/datasets/3d_clusters.csv")
            ], className="colm"),
            html.Div([""], className="colm"),
        ], className="rowm", style={"height": "4rem", "margin": "1.5rem 0 2rem 0"}),

        html.H1(["References"], className="header_1"),
        html.P([
            "[1] Refahi, Y., Zardilis, A., Michelin, G., Wightman, R., Leggio, B., Legrand, J., Faure, E., Vachez, "
            "L., Armezzani, A., Risson, A.-E., Zhao, F., Das, P., Prunet, N., Meyerowitz, E., Godin, C., Malandain, "
            "G., Jönsson, H., & Traas, J. (2020). A multiscale analysis of early flower development in Arabidopsis "
            "provides an integrated view of molecular regulation and growth control. BioRxiv, 2020.09.25.313312. "
            "https://doi.org/10.1101/2020.09.25.313312",
        ], className="text"),
        html.P([
            "[2] Nitzan, M., Karaiskos, N., Friedman, N., & Rajewsky, N. (2019). Gene expression cartography. Nature, "
            "576(7785), 132–137. https://doi.org/10.1038/s41586-019-1773-3",
        ], className="text"),
        html.P([
            "[3] our publication"
        ], className="text"),

    ], className='colm main_text_card', style={"flex": "4 4 0"
                                               # , "background-color": "blue"
                                               }
    ),
    html.Div([], className='colm', style={"flex": "1 1 0"
                                          # , "background-color": "red"
                                          }
             ),
], className="rowm")
