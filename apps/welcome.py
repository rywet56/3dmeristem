import dash_core_components as dcc
import dash_html_components as html

p1 = "This website aims to provide community access to predicted 3D gene expression patterns in the developing floral meristem based on single cell RNA-seq. The data can be visualized interactively and downloaded. "
p2 = "Developmental trajectories of cells result from molecular changes at the levels of the chromatin and transcriptome. The spatial context of cells plays an important role in cell fate specification. For that reason, it is very important to understand gene expression patterns, the chromatin landscape and eventually gene-regulatory mechanisms that lead to cellular differentiation. At this point, only a few dozen marker genes involved in floral meristem organization are known and have been mapped to a 3D model [1]. The ultimate goal is to understand the activities of all genes in a spatial 3D context. "
p3 = "For that reason, it is very important to understand gene expression patterns, the chromatin landscape and " \
     "eventually gene-regulatory mechanisms, that lead to a well-defined biochemistry of an organisms, " \
     "in their spatial context. At this point, only a few dozen marker genes involved in floral meristem development " \
     "are known and have been mapped to a 3D model (reference). But in order to understand developmental processes, " \
     "the knowledge of a lot more and at best nearly all genes has to be understood in a spatial 3D context. "
p4 = "A computational framework was developed that allows the prediction of 3D gene expression patterns in the flower meristem based on knowledge of scRNA-seq data [2] and known marker genes whose 3D expression patterns have been mapped manually in a binary format  [1]. "
p5 = "The underlying workhorse is the application of Optimal Transport to reconstruct spatial expression patterns in a probabilistic sense, as implemented in novoSpaRc [3] . We improved this method by developing a range of pre-processing steps such as cell-selection and cell-enrichment, which help novoSpaRc to map single-cells to the 3D model in a probabilistic sense. Most notably, the extension of this method allows the prediction of spatial expression patterns with a very small set (~20) of marker genes. Furthermore, our approach can in principle be applied to the 3D/2D gene expression patterns in any organism."
p6 = html.Div([
    html.P(["This website provides interactive access to the predicted expression of the top 1,306 genes* and the probabilistic mapping of clusters in UMAP space from the scRNA-seq data onto the 3D flower meristem model."],
           className="text"),
    html.P(["* based on PEP (Predicted ExPression) score. This score was used to select the top 1,306 genes with high-confidence expression prediction with a PEP > 0.13."], className="text")
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


p9 = "This website provides access to the predicted gene expression of a 3D reconstructed floral meristem obtained by combining single-nuclei RNA-seq data with a 3D image-based reconstructed flower meristem [1], as described in Neumann et al.[2].  It also provides visual access to the physical location of the identified snRNA-seq cell clusters in the 3D reconstructed meristem. Chose 'Visualize Gene Expression' or 'Visualize Cell Cluster Location' to view the predicted 3D expression and the 3D cluster assignment of cells, respectively."


p10 = html.Div([
    html.P([
        "We provide a step-by-step tutorial on how to predict 3D gene expression profiles as well as how to visualize those in the GitHub repository ",
        html.A([html.B([html.U(['3D Gene Expression Prediction Tutorial'])], style={"color": "#77b300"})],
               href="https://github.com/Kaufmann-Lab/3DGEP_tutorial"),
        ". This repository describes the setup of the environment via the docker infrastructure and provides code (in the form of jupyter notebooks) as well as sample datasets to predicted 3D gene epxression profiles form snRNA-seq data.",

    ], className="text")
])

page_3 = html.Div([
    # SPACER
    html.Div([], className='colm', style={"flex": "1 1 0"
                                          # ,"background-color": "red"
                                          }
             ),
    html.Div([
        html.H1(["3D gene expression atlas of the A. Thaliana flower meristem"], className="header_1"),
        html.P([p9], className="text"),

        # html.H1(["Why this page?"], className="header_1"),
        # html.P([p1], className="text"),
        #
        # html.H1(["How to use this page ?"], className="header_1"),
        # p6,
        #
        # html.H1(["The biological question"], className="header_1"),
        # html.P([p2], className="text"), html.P([p3], className="text"),
        #
        # html.H1(["Our approach to answer this question"], className="header_1"),
        # html.P([p4], className="text"),
        #
        # html.H1(["The computational framework – novosparc +"], className="header_1"),
        # html.P([p5], className="text"),

        html.H1(["Data Access"], className="header_1"),
        p8,
        html.H1(["Tutorial"], className="header_1"),
        p10,
        # html.Div([
        #     html.Div([""], className="colm"),
        #     html.Div([
        #         html.A(["GET 3D EXPRESSION"], className="custom-button",
        #                href="https://raw.githubusercontent.com/rywet56/3dmeristem/main/datasets/ALLGENES_ns_2_nt_5_alpha_0.1_epsilon_0.05_top_sccells_50_top_hvg_100_1000genes.txt")
        #     ], className="colm"),
        #     html.Div([""], className="colm"),
        #     html.Div([
        #         html.A(["GET 3D CLUSTERS"], className="custom-button",
        #                href="https://raw.githubusercontent.com/rywet56/3dmeristem/main/datasets/3d_clusters.csv")
        #     ], className="colm"),
        #     html.Div([""], className="colm"),
        # ], className="rowm", style={"height": "4rem", "margin": "1.5rem 0 2rem 0"}),

        html.H1(["References"], className="header_1"),
        html.P([
            "[1] Refahi, Y.; Zardilis, A.; Michelin, G.; Wightman, R.; Leggio, B.; Legrand, J.; Faure, E.; Vachez, L.; Armezzani, A.; Risson, A. E.; Zhao, F.; Das, P.; Prunet, N.; Meyerowitz, E. M.; Godin, C.; Malandain, G.; Jönsson, H.; Traas, J. A Multiscale Analysis of Early Flower Development in Arabidopsis Provides an Integrated View of Molecular Regulation and Growth Control. Dev Cell 2021, 56 (4), 540-556.e8. https://doi.org/10.1016/j.devcel.2021.01.019.",
        ], className="text"),
        html.P(["[2] Neumann, M.; Xu, X.; Smaczniak, C.; Schumacher, J.; Yan, W.; Blüthgen, N.; Greb, T.; Jönsson, H.; Traas, J.; Kaufmann, K.; Muino, J. M. A 3D Gene Expression Atlas of the Floral Meristem Based on Spatial Reconstruction of Single Nucleus RNA Sequencing Data. Nat Commun 2022, 13 (1), 2838. https://doi.org/10.1038/s41467-022-30177-y."
        ], className="text"),
        # html.P([
        #     "[3] Nitzan, M., Karaiskos, N., Friedman, N., & Rajewsky, N. (2019). Gene expression cartography. Nature, "
        #     "576(7785), 132–137. https://doi.org/10.1038/s41586-019-1773-3"
        # ], className="text"),

    ], className='colm main_text_card', style={"flex": "4 4 0"
                                               # , "background-color": "blue"
                                               }
    ),
    html.Div([], className='colm', style={"flex": "1 1 0"
                                          # , "background-color": "red"
                                          }
             ),
], className="rowm")
