Changing default values
=======================

.. _change_default_values:

Changing Default Parameters
------------

The pipeline uses a default config file in addition to the user defined one to specify tool parameters as well as cluster options. For full list of parameters you can change see: Default Config

To over ride these values you can either add a corresponding section in your config file or copy the whole default config to your run folder, change the values and add it as an extra config in the submission script. The second option may be preferable if you are changing many of the default parameters.

The order of overwriting parameters are as follows:

The order of overwriting parameters are as follows: 
1. Config specified in the snakefile (in this case the default config)
2. Config specified as snakemake argument with `--configfile` (in the order they are added)
3. Parameters specified directly in snakemake argument with `--config`

Option 1: Add corresponding section to your own config file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Case:** You want to change the probbability cut off threshold from 0.5 to 0.25 for **scHPL**

This section is found in the default config: 

.. code-block:: yaml
  scHPL:
    threads: 1
    classifier: 'svm'
    dimred: 'False'
    threshold: 0.5

Create a corresponding section in your config and change the threshold value to 0.25: 

.. code-block:: yaml
  # target directory 
  output_dir: <output directory for the annotation workflow>
  
  ### Description of some non-tool specific parameters 
  references:
        <reference_name>:
              experssion: <path counts>
              labels: <path labels>
              output_dir_benchmark: <path benchmarking folder>
              convert_ref_mm_to_hg: False
              ontology:
                    ontology_path: <path to ontology.csv>
                    ontology_column: <ontology_column to use>
              downsample:
                    value: 500
                    stratified: True
              min_cells_per_cluster: 100
  
  # path to query datasets (cell x gene raw counts)
  query_datasets:
        <query_name_1>: <path to counts 1>
        <query_name_2>: <path to counts 2>
        <query_name_3>: <path to counts 3>
  
  # classifiers to run
  tools_to_run:
        - tool1
        - tool2
  
  # consensus method
  consensus:
        tools: 
              - 'all'
        type:
              majority:
                    min_agree: <minimum agreemeent to use>
              CAWPE:
                    mode: <CAWPE MODE>
                    alpha: <alpha value>
  
  # benchmark parameters 
  benchmark:
        n_folds: <number of folds to use in the benchmarking>
  
  # additional parameters
  scHPL:
        threshold: 0.25 
        
**Option 2: Copy the whole default config and add it as an extra config file in the snakemake command**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this case your submission script would look like this:

.. code-block:: bash
  # path to snakefile and config 
  snakefile=<path to snakefile>
  config=<path to configfile>
  extra_config=<path to your new default config file>

  # run workflow 
  snakemake -s ${snakefile} --configfile ${config} ${extra_config} --cores 5

### Example of some non-tool specific paramters 

.. code-block:: bash
  # convert gene symbols in reference from mouse to human 
  convert_ref_mm_to_hg: False

  # TODO: add new example