.. _tools:

🧰 Documentation of the tools available in CoRAL
====================================================

scClassify
------------

Documentation written by: Bhavyaa Chandarana

Date written: 2023-07

scClassify workflow was generated using the tutorial below:
https://www.bioconductor.org/packages/release/bioc/vignettes/scClassify/inst/doc/scClassify.html

* scCoAnnotate input reference and query have cells as the rows, genes as columns. scClassify (and the Seurat function used for normalization, see below) requires genes on the rows and cells on the columns. Therefore, I used `WGCNA::transposeBigData()` (function optimized for large sparse matrices) to transpose the inputs before normalization and training/prediction.

* scClassify documentation defines "log-transformed" data as "size-factor normalized" data ([source](https://www.bioconductor.org/packages/devel/bioc/vignettes/scClassify/inst/doc/scClassify.html#2_Setting_up_the_data)). Function documentation for both `train_scClassify()` and `predict_scClassify()` specify that reference and query data must be "log-transformed" ([source](https://www.bioconductor.org/packages/release/bioc/manuals/scClassify/man/scClassify.pdf)) Therefore, I am normalizing both query and reference with `Seurat::NormalizeData()` (default parameters), which performs log normalization with scale factor 10000 ([source](https://satijalab.org/seurat/reference/normalizedata))

* scClassify train and predict functions `train_scClassify()` and `predict_scClassify()` both allow parallelization with package `BiocParallel`. If greater than one thread was requested by the user, I turn parallelization mode on with parallel = TRUE, and set the `BiocParallel` parameter to `BiocParallel::MulticoreParam()` with workers equal to number of requested threads (based on code in [this issue](https://github.com/SydneyBioX/scClassify/issues/14)) Otherwise I have set parallelization to FALSE and the `BiocParallel` parameter to `BiocParallel::SerialParam()` (which is the default value of the parameter in the functions - [source](https://www.bioconductor.org/packages/release/bioc/manuals/scClassify/man/scClassify.pdf)).

* scClassify train function `train_scClassify()` can either return a list output for the model, or an R object of class `scClassifyTrainModel`, based on boolean argument `returnList`. Both types work as input for prediction with `predict_scClassify()`. However, in order to use `scClassify::cellTypeTree()` to extract and output the tree produced by scClassify during training, the input must be the R object of class `scClassifyTrainModel`. Therefore, I have chosen to set `returnList` in `train_scClassify()` to FALSE (default: TRUE), and use the resulting object for `cellTypeTree()`. (Function documentation [source](https://www.bioconductor.org/packages/release/bioc/manuals/scClassify/man/scClassify.pdf))

* `scClassify::plotCellTypeTree()` produces a ggplot object. Therefore, I am using `ggplot2::ggsave()` to save it as a png file. (Function documentation [source](https://www.bioconductor.org/packages/release/bioc/manuals/scClassify/man/scClassify.pdf))


scPred
------------

Documentation written by: Alva Annett    

Date written: 2023-07   

Normalization and parameters based on this tutorial:   
https://powellgenomicslab.github.io/scPred/articles/introduction.html

* Both reference and query is normalized using `Seurat::NormalizeData()`.     
Needs computed PCA space. Dims set to 1:30 according to tutorial.

* Default model `SVMradial`. Option to switch model should be set up in snakemake.  

SingleR
------------

Documentation written by: Alva Annett    
Date written: 2023-07  

Normalization and parameters based on this tutorial:
http://www.bioconductor.org/packages/devel/bioc/vignettes/SingleR/inst/doc/SingleR.html#3_Using_single-cell_references

* Both reference and query is normalized using `scuttle::logNormCounts()`. Both reference and query is converted to SingleCellExperiment objects before normalization.   

* Deviation from default parameters: `de.method = de.method="wilcox"` Method for generating marker genes for each class in reference. Wilcox is recomended when single cell data is used as reference

singleCellNet
------------

Documentation written by: Rodrigo Lopez Gutierrez

Date written: 2023-08-01

singleCellNet workflow was generated following the tutorial below:
https://pcahan1.github.io/singleCellNet/

Input for `singleCellNet` is raw counts for both reference and query. The reference is normalized within the `scn_train()` function. The query is currently not normalized. In the tutorial example they used raw query data. Furthermore, according to the tutorial, the classification step is robust to the normalization and transformation steps of the query data sets. They claim that one can even directly use raw data to query and still obtains accurate classification. This could be tested in the future with our data to see if normalized queries perform better.

Normal parameters were used in both the training and prediction functions, with the expection of the following parameters:
* In `scn_train()`, we used parameter `nTrees = 500` compared to the default `nTrees = 1000`. This parameter changes the number of trees for the random forest classifier. The value selected is based on Hussein's thesis and is changed to improve the speed of `singleCellNet`. It is mentioned that additional training parameters may need to be adjusted depending on the quality of the reference data. Additionally, tutorial mentions that classifier performance may increase if the values for `nTopGenes` and `nTopGenePairs` are increased.
* In `scn_predict()`, we used parameter `nrand = 0` compared to the default `nrand = 50`. This parameter changes the number of randomized single cell RNA-seq profiles which serve as positive controls that should be mostly classified as `rand` (unknown) category. If left at default value, then this would generate extra cells that might complicate downstream consolidation of the consensus predictions for each cell. Therefore, the selected value is used to avoid complication. 

Correlation
------------

Documentation written by: Rodrigo Lopez Gutierrez   

Date written: 2023-08-02   

The Correlation tool runs a correlation-based cell type prediction on a sample of interest, given the mean gene expression per label for a reference.
The function to label by Spearman correlation was originally generated by Selin Jessa and Marie Coutelier.
Path to original file on Narval compute cluster: `/lustre06/project/6004736/sjessa/from_narval/HGG-oncohistones/stable/code/scripts/predict_celltype_cor.R`

Input for `Correlation` is raw counts for both reference and query. Both the reference and the query are normalized using `Seurat::NormalizeData()`.

Training script generates a matrix with the mean gene expression for each label in the reference.
Prediction script calculates a correlation between each cell in the query and each label in mean gene expression matrix generated in the training script. Then we assign each cell the most highly correlated label. 
* `label_correlation()` function has a parameter `threshold_common_genes` which sets the percentage of query dataset genes required to be in the reference dataset in order to proceed. This parameter is currently not utilized as the preprocessing done in the beginning of the snakefile is extracting only the common genes between the reference and the queries.

Currently only outputting a table with each cell, the most highly correlated label, and the corresponding correlation score for that label. In the future we could export the full correlation matrix, if necessary.

scLearn
------------

Documentation written by: Bhavyaa Chandarana, updated by Tomas Vega Waichman

Date written: 2023-08-04 

scLearn workflow was generated using the following tutorial: https://github.com/bm2-lab/scLearn#single-label-single-cell-assignment

* scCoAnnotate input reference and query have cells as the rows, genes as columns. scLearn requires genes on the rows and cells on the columns. Therefore, I used `WGCNA::transposeBigData()` (function optimized for large sparse matrices) to transpose the inputs before normalization and training/prediction.

* In order to avoid cell filtering, the reference and query matrix were normalized using Seurat::NormalizeData. The authors original log normalized in this way in this way but with a custom function (using a scale.factor = 10000 and then log(ref + 1)). Because of this, the scLearn function argument for `species` is not used. This allows us to use this method with species other than human or mouse (only two arguments accepted)

* Used default value `10` for argument `bootstrap_times` in training function. According to tool documentation, this can be increased to improve accuracy for unassigned cells(?) but increase train time.

* Default parameters were used for tool prediction 

* Added some outputs: for training, added a table with the genes selected for the model. For prediction, added an output with the whole data frame containing the probabilities for each cell.


ACTINN
------------

Documentation written by: Alva Annett    

Date written: 2023-08-08    

ACTINN code is based on `actinn_format.py` and `actinn_predict.py` originally found here: https://github.com/mafeiyang/ACTINN

* ACTINN has been split into testing and predicting. To do this, filtering of outlier genes based on expression across all query samples and reference had to be removed. The rest of the code has not been changed from the original ACTINN implementation, other than rearrangements and removal of some parts related to processing multiple samples at the same time.

* ACTINN is run with default parameters from original implementation. Normalization is based on original implementation and paper (cells scaled to total expression value, times 10 000, log2(x+1) normalized)

scAnnotate
------------

Documentation written by: Tomas Vega Waichman    

Date written: 2023-08-11   

The scAnnotate workflow was generated following the tutorial provided below:
https://cran.r-project.org/web/packages/scAnnotate/vignettes/Introduction.html

* Training and test steps of scAnnotate cannot be separated.
* Genes in references and query should match.
* The tool allows normalization inside their function using the parameter `lognormalized = F`. I normalized in the same way as they do on their script, but using the NormalizeData function from the Seurat package, via the “LogNormalize” method and a scale factor of 10,000. This is to allow the script to be easier to modify in the future (e.g. in case we allow an option for pre-normalized data). Since the data is normalized already by Seurat I set `lognormalized = T`.
* scAnnotate has two separate workflows with different batch effect removal steps based on the size of the training data.  The `correction ="auto"` allows to automatically detect the needed for the dataset. They suggest using Seurat for dataset with at most one rare cell population (at most one cell population less than 100 cells) and using Harmony for dataset with at least two rare cell populations (at least two cell populations less than 100 cells).
* The `threshold` value goes between 0-1 and the cell with lower probability than the threshold are set to "unassigned"

scID
------------

Documentation written by: Tomas Vega Waichman    

Date written: 2023-08-12    

The scID workflow was generated following the tutorials provided below:
* https://github.com/BatadaLab/scID/blob/master/vignettes/Mapping_example.md
* https://github.com/BatadaLab/scID

scID has some issues for installation: 
 * Needs module `gdal/3.5.1` 
 * MAST is needed. If you are not able to install it, use this approach:

.. code-block:: bash

  wget https://bioconductor.org/packages/release/bioc/src/contrib/MAST_1.26.0.tar.gz
  R CMD INSTALL MAST_1.26.0.tar.gz


* Training and test steps of scID cannot be separated.
* I used their `scID:::counts_to_cpm(counts_gem = query)` function that they provided (hidden, code in their github). Could be replaced with any normalization without log-transformation (they said this in the tutorial below: Any library-depth normalization (e.g. TPM, CPM) is compatible with scID, but not log-transformed data.)
* All parameters are the default except the normalization that is set in F since I normalized outside the function. But there exist some parameters that would be nice to explore as the `estimate_weights_from_target`.
* It's very slow (takes ~ 2hs for the 5k cells query and 5k cell reference), but we have to test if it's related with the number of labels (number of comparison) or the size of the dataset.

scNym
------------

Documentation written by: Tomas Vega Waichman    

Date written: 2023-08-14 

The scNym workflow was generated following the tutorial provided below:
https://github.com/calico/scnym/tree/master
  
scNym takes advantage of the query to train the model, so the training and test steps should not be separated.

* Query and training are concatenated into the same object. Any cell with the annotation "Unlabeled" will be treated as part of the target dataset and used for semi-supervised and adversarial training. It uses part of the query dataset to train the model.
* Data inputs for scNym should be log(CPM + 1) normalized counts, where CPM is Counts Per Million and log is the natural logarithm.
* They added the step of filtering genes that are not expressed, so I added it, but I ignored the step of filtering cells.
* This tool uses a threshold to assign labels to cells, and cells not passing this threshold have value “Unknown”.
* It needs more research in multi-domain.
* Additional output: `whole_df_output.csv` has the entire dataframe output with the score for the query test (mark as label == “Unlabeled”).
* I used the configuration as `new_identity_discovery` since: "This configuration is useful for experiments where new cell type discoveries may occur. It uses pseudolabel thresholding to avoid the assumption above. If new cell types are present in the target data, they correctly receive low
confidence scores."

CellTypist
------------

Documentation written by: Tomas Vega Waichman    

Date written: 2023-08-16

The CellTypist workflow was generated following the tutorials provided below:

Training:
* https://celltypist.readthedocs.io/en/latest/celltypist.train.html
* https://github.com/Teichlab/celltypist#supplemental-guidance-generate-a-custom-model

Predicting:
* https://celltypist.readthedocs.io/en/latest/notebook/celltypist_tutorial_ml.html

CellTypist allows separation between training and reference, and allows parallelization.
They provide their own pre-trained models.
CellTypist requires a logarithmised and normalised expression matrix stored in the `AnnData` (log1p normalised expression to 10,000 counts per cell) [link](https://github.com/Teichlab/celltypist#supplemental-guidance-generate-a-custom-model)

Training:
* I use `check_expression = True` to check that the expression is okay.
* `celltypist.train` has the option `(feature_selection = True)` in order to do a feature_selection, but it is not implemented.
* The output is the model and and from the model we get the top markers for each cell type using the function `model.extract_top_markers()`. A table with the top 10 genes per cell-type is returned too (top10_model_markers_per_celltype.csv).

Predicting:
* From tutorial: "By default, CellTypist will only do the prediction jobs to infer the identities of input cells, which renders the prediction of each cell independent. To combine the cell type predictions with the cell-cell transcriptomic relationships, CellTypist offers a majority voting approach based on the idea that similar cell subtypes are more likely to form a (sub)cluster regardless of their individual prediction outcomes. To turn on the majority voting classifier in addition to the CellTypist predictions, pass in `majority_voting = True`. If `majority_voting = True` all the predict column will be the majority_voting results otherwise it use the predicted_labels where each query cell gets its inferred label by choosing the most probable cell type among all possible cell types in the given model." [link](https://celltypist.readthedocs.io/en/latest/notebook/celltypist_tutorial_ml.html)
* `majority_voting parameter` should be specified in the configfile.
* I use the multilabel prediction, since we want to know if a cell cannot be classified very clearly… Description: "For the built-in models, we have collected a large number of cell types; yet, the presence of unexpected (e.g., low-quality or novel cell types) and ambiguous cell states (e.g., doublets) in the query data is beyond the prediction that CellTypist can achieve with a 'find-a-best-match' mode. To overcome this, CellTypist provides the option of multi-label cell type classification, which assigns 0 (i.e., unassigned), 1, or >=2 cell type labels to each query cell. It allows the use of a `threshold` to label cells that are below that probability as "Unnasigned". It allows to have intermediate labels as combination in the format of `celltype1|celltype2`."
  
* Output: 4 `.csv`, the prediction for each cell (depending if we choose majority_voting or not will be the majority_voting or not), 
  * `decision_matrix.csv`: Decision matrix with the decision score of each cell     belonging to a given cell type.
  * `probability_matrix.csv`: Probability matrix representing the probability each cell belongs to a given cell type (transformed from decision matrix by the sigmoid function).
  * `predicted_labels.csv`: The prediction for each cell, if majority_voting was true it has the information of the majority_voting labels AND the predicted_labels.
  * Generates some embedding plots.
  * An `.h5ad` object that has all the previous information (with the embeddings too) in a `.h5ad` object.

Seurat
------------

Documentation written by: Tomas Vega Waichman    

Date written: 2024-05-23

The Seurat workflow was generated following the tutorial provided below:
https://satijalab.org/seurat/articles/integration_mapping#cell-type-classification-using-an-integrated-reference

This methods is a integration method. So it integrate the reference with the query and use a kNN approach to transfer the labels from the nearest neighborg from the ref to the query. 
* Input for `Seurat` is raw counts for both reference and query. Both the reference and the query are normalized using `Seurat::NormalizeData()`.
* Training and prediction were separated. The training part is actually a preprocessing of the reference, were is normalized and PCA are calculated. The PC are uses to calculate the distances between ref and query cells.
* The number of PC computed could be specified by the user (`nPC_computed`, default 50).
* The number of PC used to the kNN could be specified by the user (`nPC_used`, default 30).
* Then in the prediction script the query is processed and the labels transfered.

