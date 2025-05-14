.. _tools:

Documentation of the tools available in CoRAL
====================================================

ACTINN
------------

**Cite**: *Ma, F. & Pellegrini, M. ACTINN: automated identification of cell types in single cell RNA sequencing. Bioinformatics 36, 533–538 (2020).* 

**Documentation/Github**: https://github.com/mafeiyang/ACTINN

**Description**:
ACTINN is a neural network with three hidden layers (each containing 100, 50 and 25 nodes, respectively. ACTINN implementation is based on the actinn_format.py and actinn_predict.py scripts originally found in their github.
ACTINN has been split into testing and predicting. To do this, filtering of outlier genes based on expression across all query samples and reference had to be removed. Additionally, ACTINN code was modified to provide always the probability matrix of the query cells and the class annotation according to the class with the maximum probability (same as original), with an addition of an rejection option (default threshold 0.5). 
The rest of the code has not been changed from the original ACTINN implementation, other than rearrangements and removal of some parts related to processing multiple samples at the same time. Also,  minor changes have been made to asses compatibility between tensorflow versions.  ACTINN is run by default parameters from original implementation.

**Modifiable parameters**:
:code:`threshold` (default 0.5): Minimal probability for supporting annotation.

CellBlast
------------

**Cite**: *Cao, Z.-J., Wei, L., Lu, S., Yang, D.-C. & Gao, G. Searching large-scale scRNA-seq databases via unbiased cell embedding with Cell BLAST. Nat. Commun. 11, 3458 (2020).* 

**Documentation/GitHub**:  https://cblast.readthedocs.io/en/latest/

**Description**:
CellBLAST uses a neural network-based generative model to find a low-dimensional cell embedding space with intra-reference batch effect corrected by adversarial alignment. Then query cells are projected into the same space and classification is done by the majority vote of the significantly closest reference cells.  The implementation was done following the tutorial in the documentation website.

**Modifiable parameters**:
CellBlast is run by default with parameters from original implementation.
:code:`n_models` (default: n_models: 4): The number of models to run in the training step 
:code:`threshold` (default: 0.5, corresponds to the majority_threshold parameter from CellBlast):  Minimal  majority fraction for supporting annotation.

CellTypist
------------

**Cite**: *Dominguez Conde et al., Cross-tissue immune cell analysis reveals tissue-specific features in humans. Science 376, eabl5197 (2022).*

**Documentation/GitHub**: https://celltypist.readthedocs.io/en/latest/

**Description**: Celltypist uses a  logistic regression–based framework with a stochastic gradient descent learning. We implement CellTypist prediction using the multi-label classification framework (mode = 'prob match').

**Modifiable parameters**:
:code:`majority_voting` (default: True): To refine the predicted labels by running the majority voting classifier after over-clustering. We use the True as default value to improve the performance prediction. 
:code:`feature_selection` (default: True):  Whether to perform two-pass data training where the first round is used for selecting important features/genes using SGD learning. If True, the training time will be longer.  We use the True as default value to improve the performance prediction.
:code:`threshold` (default 0.5, corresponds to the p_thres parameter from CellTypist): Probability threshold for the multi-label classification

Correlation
------------

**Cite**: NA

**Documentation/GitHub**: https://github.com/fungenomics/CoRAL/tree/main/Scripts/Correlation

**Description**: Correlation method use a similary-based labeling by measuring the Spearman correlation between mean transcriptomic profiles per class (class centroids) on the reference and each query cells. 

**Modifiable parameters**: NA

scAnnotate
------------

**Cite**:  *Ji, X. et al. scAnnotate: an automated cell-type annotation tool for single-cell RNA-sequencing data. Bioinform. Adv. 3, vbad030 (2023).*

**Documentation/GitHub**: https://cran.r-project.org/web/packages/scAnnotate/index.html

**Description**: scAnnotate is an ensemble of classifiers based on a mixture model for the expression level of a single gene, combined through a weighted average. 
The scAnnotation function allows a threshold parameter but since in the documentation the authors didn’t provide any wrapper function to get the probability matrices, we used them as binary output. The implementation was done following the tutorial in the documentation website.

**Modifiable parameters**:
:code:`threshold` (default 0.5): Minimal probability for supporting annotation.

scANVI
------------

**Cite**: *Xu, C. et al. Probabilistic harmonization and annotation of single-cell transcriptomics data with deep generative models. Mol. Syst. Biol. 17, e9620 (2021).*

**Documentation/GitHub**: https://docs.scarches.org/en/latest/scanvi_surgery_pipeline.html

**Description**: scANVI is a variational autoencoder with a built-in classifier used to predict cell-type labels based on their position in the latent space. 
The implementation was done following the tutorial in the documentation website.

**Modifiable parameters**:
scANVI is run by default with parameters from original implementation.
:code:`threshold` (default 0.5): Minimal probability for supporting annotation.

scClassify
------------

**Cite**:   *Lin, Y. et al. scClassify: sample size estimation and multiscale classification of cells using single and multiple reference. Mol. Syst. Biol. 16, e9389 (2020).*

**Documentation/GitHub**: https://www.bioconductor.org/packages/release/bioc/vignettes/scClassify/inst/doc/scClassify.html

**Description**: scClassify is a classifier based on ensemble learning and cell type hierarchies constructed from annotated references. At each branch node, an ensemble classifier is built from several weighted kNN model with a different combination of similarity metric and gene selection methods.
The implementation was done following the tutorial in the documentation website.

**Modifiable parameters**:
scClassify is run by default with parameters from original implementation.
:code:`topN` (default: 50):  Top number of features selected.
:code:`weightsCal` (default: False): To calculate the weights for the model 
:code:`hopach_kmax` (default: 5): Integer between 1 and 9 specifying the maximum number of children at each node in the HOPACH tree. 
:code:`algorithm` (default: "WKNN"): KNN method to use, other possible values are "KNN" and "DWKNN".
:code:`similarity` (default: "pearson"): Similarity measure to use, other possible values are:  "spearman", "cosine", "jaccard", "kendall", "binomial", "weighted_rank" and "manhattan".
:code:`prob_threshold` (default: 0.7): Probability threshold for KNN method.
:code:`cor_threshold_static` (default: 0.5): Static correlation threshold. 
:code:`cor_threshold_high` (default: 0.7): Highest correlation threshold.

scHPL
------------

**Cite**: *Michielsen, L., Reinders, M. J. T. & Mahfouz, A. Hierarchical progressive learning of cell identities in single-cell data. Nat. Commun. 12, 2799 (2021).*

**Documentation/GitHub**: https://schpl.readthedocs.io/en/latest/

**Description**: scHPL is hierarchical classifier that finds relationships between cell populations across datasets to construct a hierarchical classification tree. For each node in the tree either a linear SVM, kNN, or one-class SVM is trained to then predict the labels of a new unlabeled dataset. 
Since this method considers multiple reference datasets as input to infer the hierarchical cell-type tree, but we implemented it using only one dataset at a time, we followed the authors' advice (https://github.com/lcmmichielsen/scHPL/issues/7) and trained the method using a flat tree.
The implementation was done following the tutorial in the documentation website.

**Modifiable parameters**:
:code:`classifier` (default: “svm”): Classifier to use, other possible values are: “svm_occ” and “knn”.
:code:`dimred` (default: “False”): If PCA should be run before training classifier.
:code:`threshold` (default 0.5): Minimal probability for supporting annotation.

SciBet
------------

**Cite**: *Li, C. et al. SciBet as a portable and fast single cell type identifier. Nat. Commun. 11, 1818 (2020).*

**Documentation/GitHub**: https://github.com/PaulingLiu/scibet

**Description**: SciBet is a probability classifier that fits a multinomial model for each cell type from the reference to assign unlabeled cells according to the cell type model with the highest likelihood.
The implementation was done following the tutorial in the documentation website.

**Modifiable parameters**:
SciBet is run by default with parameters from original implementation.

scID
------------

**Cite**: *Boufea, K., Seth, S. & Batada, N. N. scID Uses Discriminant Analysis to Identify Transcriptionally Equivalent Cell Types across Single-Cell RNA-Seq Data with Batch Effect. iScience 23, 100914 (2020).*

**Documentation/GitHub**: https://batadalab.github.io/scID/

**Description**: scID uses Fisher’s linear discriminant analysis (LDA) to distinguish the characteristic genes of cell-types from reference. Then using those set of genes query cells are assigned to the most similar cell-type.
The implementation was done following the tutorial in the documentation website.

**Modifiable parameters**:
scID is run by default with parameters from original implementation.
:code:`logFC` (default: 0.5): LogFC threshold for extracting markers from reference cell-types

scLearn
------------

**Cite**: *Duan, B. et al. Learning for single-cell assignment. Sci Adv 6, (2020).*

**Documentation/GitHub**: https://github.com/bm2-lab/scLearn

**Description**: scLearn finds the optimal transformation using the reference data to project both reference and query cells; then, labels are transferred by measuring similarities between reference and query cells in that space.
The implementation was done following the tutorial in the documentation website using ‘threshold_use’ = TRUE, to get the rejected cells for missing cell-types on the reference.

**Modifiable parameters**:
:code:`bootstrap_times` (default: 10): Times for bootstrapping.