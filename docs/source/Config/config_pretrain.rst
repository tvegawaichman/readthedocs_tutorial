.. config_annotation:

🏋️ Pretrain pipeline
=================================

What is the pretrain pipeline?
----------------

The pretrain pipeline consist in only pretrain the models.
This is very useful when you are predicting for many queries and you want to use the same models in the future for saving time.
All the configuration file will be focus in the reference preparation.

Configuration File for Pretrain
----------------

.. code-block:: yaml
  
  # mode
  mode: "pretrain"
  
  # target directory 
  output_dir: <output directory for the pretrain pipeline>
  
  ### Description of some non-tool specific parameters 
  references:
        <reference_name_1>:
              expression: 
              labels: 
              batch: 
              convert_ref_mm_to_hg: False
              min_cells_per_cluster: 50
              downsample:
                value: 10
                stratified: True
        <reference_name_2>:
              expression: 
              labels: 
              batch: 
              convert_ref_mm_to_hg: True
              min_cells_per_cluster: 100
              downsample:
                value: 10
                stratified: True
  
  # methods to pretrain
  tools_to_run:
        - tool1
        - tool2
  

Features
^^^^^^^^^^
- *mode*: 
  In this case will be :code:`pretrain`.

- *output_dir*: 
  Output directory for the pretrain models.
  
- *reference*:

  - *expression*: 
    Path to expression matrix, seurat object or single cell experiment.
    
  - *labels*: 
    Path to labels files or column with label metadata. 
    
  - *batch*: 
    Path to batch files or column with batch metadata. 
    This information is used in tools that use the integration stratergy: :code:`CellBlast`, :code:`Seurat`, :code:`scPoli`, :code:`Symphony`, :code:`scANVI`.
    
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
  List of method to train. 
  Be aware that some tools cannot be pretrained: :code:`scAnnotate`, :code:`scID` , :code:`scNym`. See :ref:`tools` to find available tools.
  