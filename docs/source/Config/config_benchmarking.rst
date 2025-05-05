.. config_benchmarking:

🧮 Cross-Validation pipeline
=================================

What is the Cross-Validation pipeline?
----------------

The cross-validation pipeline is one of the back bones of CoRAL. It consist in the Individual method performance assessment.
To evaluate the performance of individual methods on the annotated reference dataset (reference) while avoiding overfitting and data leakage, we perform an :code:`nfolds` cross-validation experiment. 
During the sampling process reference cells are stratified by classes to ensure representation of all classes within each fold. 
The performance of each method is measured using metrics for multi-class classification. 

Briefly, for each method (m), performance is calculated for each class (c) in each fold. The class performance across folds is then summarized by the mean. 
Finally, the overall performance of each method is computed as the mean performance across all classes (macro performance). 
This final metric is robust to class imbalance.

This pipeline also allows to measure the quality of the reference when all tools fails to predict any class.

The output of this pipeline is a report with the cross-validatio results and also the metrics necessary to compute CoRAL score.

Configuration File for Cross-Validation
----------------

.. code-block:: yaml
  
  # mode
  mode: "benchmark"
  
  seed: <seed to use for reproducibility on the K fold generation>
  
  benchmark:
    n_folds:  <number of folds to use>
    
  ### Description of some non-tool specific parameters 
  references:
        <reference_name_1>:
              expression: 
              labels: 
              batch: 
              output_dir_benchmark: 
              convert_ref_mm_to_hg: False
              min_cells_per_cluster: 50
              downsample:
                value: 10
                stratified: True
              ontology:
                ontology_path:
                ontology_column:
        <reference_name_2>:
              output_dir_benchmark: 
              ontology:
                ontology_path:
                ontology_column:
  # methods to run
  tools_to_run:
        - tool1
        - tool2
  
  # consensus method
  consensus:
        tools: 
              - 'all'
        type:
              majority:
                    # ex: [3], [3, 4, 5]
                    min_agree: [<minimum agreemeent to use>]

Features
^^^^^^^^^^
- *mode*: 
  In this case will be :code:`benchmark`.

- *seed*:
  Seed to use for the K fold splitting part to seek reproducibility.

- *benchmark*:

   - *n_folds*: 
    Numeric (default 5). Number of folds to use in the cross-validation step. 
   
- *reference*:

  - *expression*: 
    Path to expression matrix, seurat object or single cell experiment.
    
  - *labels*: 
    Path to labels files or column with label metadata. 
    
  - *batch*: 
    Path to batch files or column with batch metadata. 
    This information is used in tools that use the integration stratergy: 
    
  - *ontology*:
  
    - *ontology_path*: 
      Path to the csv containing the ontology path.
      Each column represents a different granularity of labels.
      The columns should be named.
      
    - *ontology_column*: 
      This parameter can take multiple column names, therefore they should be put in a list, in case of none specification of the column all the ontology columns in the file will be used. 
  - *output_dir_benchmark*:  
    Path to benchmarking pipeline ran in the :ref:`config_benchmarking` pipeline where the weight for CoRAL were calculated. Only needed if CAWPE mode is specified as a consensus method.
    
    
  **This features are use to modify your reference before running the training**:
  
    - *convert_ref_mm_to_hg*: 
      Logical. 
      Whether the reference use mouse symbol and should be converted to human before training. 
      
    - *min_cells_per_cluster*: 
      Numeric (default 50).
      Minimal number of cells per class to keep to train. 
      Classes with lower number of cells will be removed from the training and predicting step.
    
    - *downsample*:
    
      - *value*: 
        Numeric. 
        This determinate the proportion (if value < 1) or the number of cells (if value > 1) to downsample. 
        Default is 0 (no downsampling)
        
      - *stratified*: 
        This argument allows stratifying the downsampling according to attributes of the dataset. 
        The logic is the same as the group_by function in tidyverse. 
        The cells will be group by the atributes specified in brackets ([]) separated by commas (,), and the downsampling specified in :code:`value` will applied. If :code:'stratified' argument is not specified or is empty, the downsampling will be performed without any stratification.
        
- *tools_to_run*: 
  List of method to run. See :ref:`tools` to find available tools.
  
- *consensus*: 
  See :ref:`consensus_methods` for more details.
  
  - *tools*: 
    Tools to use in the consensus. Use code:`all` for include all the tools, a list with the specified tool otherwise.
    
  - *type*: 
    Type of consensus to use.
    
    - *majority*: 
      To use relative majority consensus. In this step for the consensus metric is computed but not use after for CoRAL.
      
      - *min_agree*: 
        List. 
        Minimal agreement to use, every cell whit less than this value will be automaticly called **No Consensus**. 
        More than one threshold could be specified.