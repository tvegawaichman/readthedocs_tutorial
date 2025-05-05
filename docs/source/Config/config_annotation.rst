.. config_annotation:

What is annotation?
=================================

The annotation pipeline can be run in two ways: from scratch or using pretrained models.

Running the annotation from scratch will train the reference for all the specified tools and predict on all specified queries using the intersection of features found between each reference and the queries. All tools will be automaticly use :code:`gene_selection = intersection`

Running the annotation pipeline with pretrained models will directly perform predictions on all the queries, using the feature set from the reference used for pretraining and filling with zeros for any missing genes to match the original reference feature space. All tools will be automaticly use :code:`gene_selection = complete`

One report per query/consensus mode, containing all the reference and consensus will be generated.

Configuration File for Annotation
----------------

.. code-block:: yaml
  
  # mode
  mode: "annotate"
  
  # target directory 
  output_dir: <output directory for the annotation pipeline>
  
  ### Description of some non-tool specific parameters 
  references:
        <reference_name_1>:
              expression: 
              labels: 
              batch: 
              output_dir_benchmark: 
              #pretrain_models: 
              convert_ref_mm_to_hg: False
              min_cells_per_cluster: 50
              downsample:
                value: 10
                stratified: True
              ontology:
                ontology_path
                ontology_column
        <reference_name_2>:
              output_dir_benchmark: 
              pretrain_models: 
              ontology:
                ontology_path
                ontology_column
  
  # path to query datasets (cell x gene raw counts, seurat or single cell experiment)
  query_datasets:
        <query_name_1>: <path to counts 1>
        <query_name_2>: <path to counts 2>
        <query_name_3>: <path to counts 3>
  
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
              CAWPE:
                    # ex: ['CAWPE_T'], ['CAWPE_T','CAWPE_CT']
                    mode: [<CAWPE mode>]

Features
^^^^^^^^^^
- *mode*: 
  In this case will be :code:`annotation`.

- *gene_threshold*: 
  Numeric (default 0.25).
  Minimal proportion of overlaping between reference and query to train and predict.
  **Note** only used when :code:`gene_selection` is run with intersection.
  
- *output_dir*: 
  Output directory for the annotation pipeline.
  
- *reference*:

  - *expression*: 
    Path to expression matrix, seurat object or single cell experiment.
    Not necessary if pretrain_models path were specified.
    
  - *labels*: 
    Path to labels files or column with label metadata. 
    Not necessary if :code:`pretrain_models` path were specified.
    
  - *batch*: 
    Path to batch files or column with batch metadata. 
    Not necessary if :code:`pretrain_models` path were specified.
    This information is used in tools that use the integration stratergy (TOOLS)
    
  - *pretrain_models*: 
    Path to pretrained models. 
    Models not found in the path will be train from scratch. 
    Any modification specified in the config file to the reference will be applied if :code:`pretrain_models` were specified. 
    
  - *ontology*:
  
    - *ontology_path*: 
      Path to the csv containing the ontology path.
      Each column represents a different granularity of labels.
      The columns should be named.
      
    - *ontology_column*: 
      This parameter can take multiple column names, therefore they should be put in a list, in case of none specification of the column all the ontology columns in the file will be used. 
  - *output_dir_benchmark*:  
    Path to benchmarking pipeline ran in the :ref:`config_benchmarking` pipeline where the weight for CoRAL were calculated. Only needed if CAWPE mode is specified as a consensus method.
    
  - **This features are use to modify your reference before running the training**:
  
    - *convert_ref_mm_to_hg*: 
      Logical. 
      Whether the reference use mouse symbol and should be converted to human before training. 
      **Note** only used when no pretrain model is specified (run from scratch).
      
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
        
- *query_datasets*: 
  Path to query samples.
  
- *tools_to_run*: 
  List of method to run. See :ref:`tools` to find available tools.
  
- *consensus*: 
  See :ref:`consensus_methods` for more details.
  
  - *tools*: 
    Tools to use in the consensus. Use code:`all` for include all the tools, a list with the specified tool otherwise.
    
  - *type*: 
    Type of consensus to use.
    
    - *majority*: 
      To use relative majority consensus.
      
      - *min_agree*: 
        List. 
        Minimal agreement to use, every cell whit less than this value will be automaticly called **No Consensus**. 
        More than one threshold could be specified.
        
    - *CAWPE*: To use consensus with weighted ensemble voting. This will use the performance on the :ref:`config_benchmarking` step to weight the contribution of each tool to each prediction. 
      - *mode*: CAWPE mode to use. More than one mode could be specified. See :ref:`consensus_methods`.
      - *alpha*: Numeric list. Hyperparameter for CAWPE calculation. More than one alpha can be specified. See :ref:`consensus_methods` for more details.
      
