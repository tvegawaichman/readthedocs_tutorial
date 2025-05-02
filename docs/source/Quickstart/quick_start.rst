.. _quickstart:

🚀 Quickstart
==========

1. Clone repository and get the apptainers that contain all the dependencies
------------

Clone git repository in an appropiate location:

.. code-block:: console

   git clone https://github.com/fungenomics/scCoAnnotate.git

Download apptainer/docker image:

.. code-block:: console

  #Apptainer
  curl -L -o CoRAL.sif "https://www.dropbox.com/scl/fi/xyx3d1hbpqssjqaboqdqw/CoRAL.sif?rlkey=l56av1fb2ccd7p721rez3j4u6&st=cp7f1ec8&dl=0"

  # Docker
  docker pull kleinmanlab/coral:celltypist_models
 
Now that we get the code and all the dependencies, let's start to prepare the input files

2. Prepare Inputs
----------------

Reference
^^^^^^^^^^

The input format for the references could be a **cell x gene matrix (.csv)** of raw counts and a **cell x label matrix (.csv)**, a **Seurat** or a **SingleCellExperiment** object.

Both the **cell x gene matrix** and **cell x label matrix** need the first column to be the cell names in matching order with an empty column name.

.. raw:: html

    <div style="display: flex; gap: 40px; align-items: flex-start;">

.. container:: table-left

  .. list-table:: Cell x Gene matrix
     :widths: 25 25 25 25
     :header-rows: 1
  
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
  
.. container:: table-right

  .. list-table:: Cell x Label data.frame
     :widths: 50 50
     :header-rows: 1
  
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

.. raw:: html

    </div>

The **Seurat** or **SingleCellExperiment** object needs to be saved as .rda or .rds and have a column in the metadata with the labels.
**Seurat** objects are compatible until v4. 
For **SingleCellExperiment** it assumes that the raw counts is in the 'counts' assay.

Query Samples
^^^^^^^^^^

The input format for the query samples could be a **cell x gene matrix (.csv)** of raw counts and a **cell x label matrix (.csv)**, a **Seurat** or a **SingleCellExperiment** object

The first column needs to be the cell names with an empty column name.

.. list-table:: Cell x Gene matrix
   :widths: 25 25 25 25
   :header-rows: 1

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


The **Seurat** or **SingleCellExperiment** object needs to be saved as .rda or .rds.
**Seurat** objects are compatible until v4. 
For **SingleCellExperiment** it assumes that the raw counts is in the 'counts' assay.

3. Prepare the config file
----------------

For each run a .yml config file needs to be prepared with information about the reference data, query samples and methods.
Multiple references can be specified with an unique **reference name** and multiple query samples can be specified with an unique **sample name**.

Full list of available tools can be found here: [AvailableTools]TODO      
Make sure that the names of the selected tools have the same capitalization and format as this list. 
The consensus method selected in **consensus_tools** can either be 'all' (which uses all the tools in **tools_to_run**) or a list of tools to include. 

The consensus can be calculated as the majority vote, specifying the minimum of tool agreement or/and with CAWPE specifying the mode: CAWPE_CT (using the performance of each tool predicting an specific cell-type) or CAWPE_T (performance of each tool). CAWPE only works if the benchmarking pipeline has been run.

At least one consensus type should be specified.

**Minimal config file for cross validation:**

.. code-block:: yaml

  # mode
  mode: "benchmark"
  
  # target directory 
  output_dir: <output directory for the annotation pipeline>
  
  ### Description of some non-tool specific parameters 
  references:
        <reference_name_1>:
              expression: <path to expression matrix, seurat object or single cell experiment>
              labels: <path to labels files>
              output_dir_benchmark: <output directory for the benchmarking pipeline>
  
  # methods to run
  tools_to_run:
        - tool1
        - tool2
  
  benchmark:
        n_folds: <number of folds to use in the benchmarking>
  
  # consensus method
  consensus:
        tools: 
              - 'all'
        type:
              majority:
                    # ex: [3], [3, 4, 5]
                    min_agree: [<minimum agreemeent to use>]

**Minimal config file for pretraining the models:**
Be aware that some tools cannot be pretrained: :code:`scAnnotate`,:code:`scID` , :code:`scNym`

.. code-block:: yaml

  # mode
  mode: "pretrain"

  # target directory 
  output_dir: <output directory for the annotation pipeline>

  ### Description of some non-tool specific parameters 
  references:
      <reference_name_1>:
            expression: <path to expression matrix, seurat object or single cell experiment>
            labels: <path to labels files>
            output_dir_benchmark: <output directory for the benchmarking pipeline>

  # methods to run
  tools_to_run:
        - tool1
        - tool2

**Minimal config file for annotation:**

.. code-block:: yaml
  
  # mode
  mode: "annotate"
  
  # target directory 
  output_dir: <output directory for the annotation pipeline>
  
  ### Description of some non-tool specific parameters 
  references:
        <reference_name_1>:
              expression: <path to expression matrix, seurat object or single cell experiment>
              labels: <path to labels files>
              output_dir_benchmark: <output directory for the benchmarking pipeline>
              pretrain_models: <path to pretrained models>
  
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


For more details about each the config files of each mode, see: See: [Changing Default Parameters](##changing-default-parameters) TODO

4. Prepare HPC submission script (OPTIONAL)
----------------

To run the snakemake pipeline on a HPC a submission script needs to be prepared

See: [Example Bash Script](example.submit.sh)

.. code-block:: bash
  
  #!/bin/sh
  #SBATCH --job-name=CoRAL
  #SBATCH --account= 
  #SBATCH --output=logs/%x.out
  #SBATCH --error=logs/%x.err
  #SBATCH --ntasks=1
  #SBATCH --cpus-per-task=5
  #SBATCH --time=24:00:00
  #SBATCH --mem-per-cpu=60GB 
  
  # apptainer image
  image=<path to apptainer immage>
  
  # snakefile 
  snakefile=<path to snakefile.master>
  
  # config 
  config=<path to config file>
  
  # unlock directory in case of previous errors
  apptainer exec --contain --cleanenv --pwd "$PWD" $image snakemake -s ${snakefile} --configfile ${snakefile} --unlock 
  
  # run CoRAL  
  apptainer exec --contain --cleanenv --pwd "$PWD" $image snakemake -s ${snakefile} --configfile ${config}  --cores 5
  
**IMPORTANT** Make sure that the number of cores requested match the number of cores in the snakemake command for optimal use of resources.
