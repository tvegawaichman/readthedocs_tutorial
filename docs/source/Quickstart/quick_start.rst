Quickstart
==========

.. _quickstart:

1-Clone repository and install dependencies
------------

Clone git repository in appropriate location:

.. code-block:: console

   git clone https://github.com/fungenomics/scCoAnnotate.git

Install R packages and python modules as specified in Installation and Dependencies[TODO] or use the apptainer[TODO]

If you are part of the Kleinman group you only need to load the module on Narval or Hydra:

2. Prepare reference
----------------

The input format for the references could be a **cell x gene matrix (.csv)** of raw counts and a **cell x label matrix (.csv)**.

Both the cell x gene matrix and cell x label matrix need the first column to be the cell names in matching order with an empty column name.

.. list-table:: Cell x Gene matrix
   :widths: 25 25 25 25
   :header-rows: 1
   :class: centered-table

   * - ''
     - Gene1
     - Gene2
     - Gene3
   * - cell1
     - 1
     - 24
     - 30
   * - cell2
     - 54
     - 20
     - 61
   * - cell3
     - 0
     - 12
     - 0
   * - cell4
     - 1
     - 13
     - 17

.. list-table:: Cell x Label data.frame
   :widths: 50 50
   :header-rows: 1
   :class: centered-table

   * - ''
     - label
   * - cell1
     - label1
   * - cell2
     - label1
   * - cell3
     - label3
   * - cell4
     - label2

Also, the input format for the reference could be a **Seurat** or **SingleCellExperiment** object. 
In the expression the path to the object should be specified (formats .rda, .rds). And in the labels the metadata column used for the labels.
If the format for the expression is .rda or .rds it assumes that the labels is a vector where it's the column name.
In the **Seurat** objects are compatible until v4. 
In the **SingleCellExperiment** it assumes that the raw counts is in the 'counts' assay.

3. Prepare query samples
----------------

The input format for the query samples could be a **cell x gene matrix** (.csv) of raw counts, seurat object or single cell experiment object with raw counts. 

The first column needs to be the cell names with an empty column name.

e:: Cell x Gene matrix
   :widths: 25 25 25 25
   :header-rows: 1
   :class: centered-table

   * - ''
     - Gene1
     - Gene2
     - Gene3
   * - cell1
     - 14
     - 2
     - 32
   * - cell2
     - 54
     - 17
     - 54
   * - cell3
     - 20
     - 8
     - 0
   * - cell4
     - 1
     - 23
     - 17

Also, the input format for the reference could be a **Seurat** or **SingleCellExperiment** object. 
In the expression the path to the object should be specified (formats .rda, .rds). And in the labels the metadata column used for the labels.
In the **Seurat** objects are compatible until v4. 
In the **SingleCellExperiment** it assumes that the raw counts is in the 'counts' assay.

4. Prepare config file
----------------

For each set of query samples a config file needs to be prepared with information about the samples, the reference, the tools you want to run and how to calculate the consensus. 

Multiple references can be specified with an unique **reference name**. Aditionally parameters could be specified inside each reference.
Additionally, an ontology could be specified to predict in a more granular label and group in a broader one.

Full list of available tools can be found here: [Available tools](#hammer-and-wrench-available-tools)      
Make sure that the names of the selected tools have the same capitalization and format as this list. 

The consensus method selected in **consensus_tools** can either be 'all' (which uses all the tools in **tools_to_run**) or a list of tools to include. 
The consensus could it be calculated with the majority vote, specifying the minimum of tool agreement or/and with CAWPE specifying the mode: CAWPE_CT (using the performance of each tool predicting an specific cell-type) or CAWPE_T (performance of each tool), and the alpha
At least one consensus type should be specified.
See: [Example Config](example.config.yml)

.. code-block:: yaml

  # target directory 
  output_dir: <output directory for the annotation workflow>

  ### Description of some non-tool specific parameters 
  references:
        <reference_name>:
              expression: <path to expression matrix, seurat object or single cell experiment>
              labels: <path to labels files>
              output_dir_benchmark: <output directory for the benchmarking workflow>
              # Convert gene symbols in reference from mouse to human
              # Accepted values: True, False
              convert_ref_mm_to_hg: False
              # The ontology permits to specify different level of labels granularity.
              # These parameters are optional
              ontology:
                    # Path to the csv containing the ontology path. Each column represents a different
                    # granularity of labels. The columns should be named.
                    ontology_path: <path to ontology.csv>
                    # The column name(s) of the granularity to use, from the ontology file.
                    # This parameter can take multiple column names, therefore they should be put in a list
                    # (ex: ['level']     ['level1', 'level2'])
                    ontology_column: <ontology_column to use>
              # Some references are too big and cannot be used efficiently
              # the following parameters permit to downsample the reference
              downsample:
                    # The number of cells to downsample to
                    # If the value is > 1, it specifies the number of cells to select (ex: 500 will select 500 cells)
                    # If the value is < 1, it is interpreted as a fraction of cells to keep (ex: 0.25 will select 25% of the cells)
                    value: 500
                    # Should the sample keep the same stratification as the complete dataset?
                    # Accepted values: True, False
                    stratified: True
              # The minimal number of cells that each cluster should have, in the reference
              # Clusters with less cells will be filtered out from the reference
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
                    # (ex: [2]     [2,3,4])
                    min_agree: <minimum agreemeent to use>
              CAWPE:
                    #(ex: ['CAWPE_T'], ['CAWPE_T','CAWPE_CT'])
                    mode: <CAWPE MODE>
                    #(ex: [4], [2,3,4])
                    alpha: <alpha value>
  
  # benchmark parameters 
  benchmark:
        n_folds: <number of folds to use in the benchmarking>

See: [Changing Default Parameters](##changing-default-parameters)

5. Prepare HPC submission script (OPTIONAL, UPDATE TO USE THE APPTAINER)
----------------

To run the snakemake pipeline on a HPC a submission script needs to be prepared 

See: [Example Bash Script](example.submit.sh)

.. code-block:: bash
  
  module load scCoAnnotate/2.0

  # path to snakefile and config 
  snakefile=<path to snakefile>
  config=<path to configfile>

  # unlock directory incase of previous errors
  snakemake -s ${snakefile} --configfile ${config} --unlock 

  # run workflow 
  snakemake -s ${snakefile} --configfile ${config} --cores 5
  
Depending on if you want to run the annotation workflow or the benchmarking workflow the snakefile needs to be path to either [snakefile.annotate](snakefile.annotate) or [snakefile.benchmark](snakefile.benchmark) 

**OBS!!** Make sure that the number of cores requested match the number of cores in the snakemake command for optimal use of resources