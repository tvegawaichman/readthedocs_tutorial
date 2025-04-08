📙 Tutorial
==========

.. _tutorial:

This is a tutorial for the three sub-pipelines included in CoRAL.

The tutorial uses a small reference and query data set from the developing mouse brain. The tutorial first goes through the benchmarking pipeline, then the training pipeline and finally the annotation pipeline, using example config files and run scripts. For more detailed descriptions of input formats and parameters see the subsequent sections!

Whenever you see an Excersise button like this, click it for some extra challenges!!

.. raw:: html

   <details>
     <summary>Exercise</summary>
     Hello!! ✨
   </details>
   


Lets start!! 
------------

To start create a folder to run the tutorial in and :code:`cd` into it

.. code-block:: console

  mkdir CoRAL_tutorial
  cd CoRAL_tutorial

Create a folder for the logs

.. code-block:: console

  mkdir logs


Set up 
----------------

**1. Clone git repository**

.. code-block:: console

  git clone https://github.com/fungenomics/CoRAL.git

You should now have a folder called :code:`CoRAL` which contains all the code from the git repository 

**2. Download apptainer image and test data set**
Download the apptainer image (this could take ~10minutes to download) 

.. code-block:: console

  curl -L -o CoRAL.sif "https://www.dropbox.com/scl/fi/xyx3d1hbpqssjqaboqdqw/CoRAL.sif?rlkey=l56av1fb2ccd7p721rez3j4u6&st=cp7f1ec8&dl=0"

Or get the docker image from docker hub: https://hub.docker.com/r/kleinmanlab/coral

You should now have a :code:`.sif` file called :code:`CoRAL.sif`. This is the apptainer image that contains everything needed to run CoRAL! 

Download and unzip small data set 

.. code-block:: console

  curl -L -o ToyData.zip "https://www.dropbox.com/scl/fo/bjuwdkbnu80dq697k075k/ANHb3rB3FGwVmEot55HK4SI?rlkey=sovugor26l3k50zcopo4j4bcm&st=kzy07rhk&dl=0"
  unzip ToyData.zip

You should now have 4 folders called :code:`Reference`, :code:`Query`, :code:`ConfigFiles` and :code:`Scripts`, that contains data and files used in this tutorial

**3. Check if you have apptainer installed**

.. code-block:: console

  apptainer --version
  
If you are on a HPC cluster you can check if apptainer is available as a module. If it is installed as a module, load the module in your run scripts before the pipeline command! 

.. code-block:: console

  module spider apptainer 

If you don't have apptainer installed follow the instructions here to install:

https://apptainer.org/docs/admin/main/installation.html 

**4. You should now have everything needed to run the tutorial** 

- Cloned :code:`CoRAL` git repository with all the code
- :code:`CoRAL.sif` file (Apptainer image)
- :code:`Reference`, :code:`Query`, :code:`ConfigFiles`, and :code:`Scripts` folders
- Apptainer installed

Make sure you have everything by running :code:`ls`

At this point you should have the following files and folders in :code:`CoRAL_tutorial`

.. code-block:: console

  CoRAL
  CoRAL.sif
  ConfigFiles
  Query
  Reference
  Scripts
  logs
  
Run the benchmarking pipeline 
--------------------------------

**1. Set up the config file** 

The first thing you need to do is check the config file for the benchmarking pipeline

.. code-block:: console
  
  cat ConfigFiles/benchmark.yml
  
The confign file specifies which pipeline to run

.. code-block:: console
  
  # pipeline to run 
  mode: 'benchmark'

Where the reference data set files are stored and where to write the output 

.. code-block:: console

  # reference parameters 
  references:
     test_reference:
        expression: Reference/expression.csv
        labels: Reference/labels.csv
        output_dir_benchmark: Out/Benchmark/

Which methods to run. In this tutorial we start by running 5 methods (SingleR, scClassify, SciBet, Correlation and Symphony), but there are many more methods available in the pipeline. 

.. code-block:: console

  # methods to run
  tools_to_run:
        - SingleR
        - scClassify
        - SciBet
        - Correlation
        - Symphony
        
How many folds to run in the cross validation 

.. code-block:: console

  # benchmark parameters 
  benchmark:
    n_folds: 5

And how to compute the consensus 

.. code-block:: console

  # consensus prameters 
  consensus:
        tools:
              - 'all'
        type:
              majority:
                   min_agree: [2]

The config file is already prepared but you do need to update the paths to be the full paths to the files (both input and output paths need to be updated)! You can find the full path to your folder by running :code:`realpath` in the command line. 

**2. Set up run script**

Check the run script file for the benchmarking pipeline

.. code-block:: console

  cat Scripts/run_benchmark.sh
  
If you've set up the tutorial folder correctly you don't have to change anything here, except if you are running on a HPC. Then you need to edit the slurm (or other scheduler) parameters at the top of the file. Don't forget to load the apptainer module or install apptainer on your own! If you are loading the apptainer module you need to add it to your run script before the pipeline command: :code:`module load apptainer` (exchnage apptainer for the name of the module on your cluster!)

The script first sets up the paths to the config file, apptainer image and snakefile 

.. code-block:: console

  # path to snakefile, config and apptainer image 
  snakefile=${PWD}/"CoRAL/snakefile.master"
  config=${PWD}/"ConfigFiles/benchmark.yml"
  image=${PWD}/"CoRAL.sif"

Second, the script runs the snakemake pipeline using the apptainer image 

.. code-block:: console

  # run benchmarking pipeline 
  apptainer exec --contain --cleanenv --pwd "$PWD" $image snakemake -n -s ${snakefile} --configfile ${config} --cores 1 --rerun-incomplete --keep-going

The :code:`-n` flag here specifies that you want to do a :code:`dry run`. This means that the pipeline will tell you which steps it is going to run without actually running anything. You should always do this before running to make sure that all of your files are in order and that there are no errors. 

Execute a dry run like this in the command line:

.. code-block:: console
  
  ./Scripts/run_benchmark.sh
  
This should print the following information, which tells you that the pipeline will split the data into 5 folds and then run testing and training 5 times for each method selected! 

Make sure that the number of folds and the methods match your config file! 

.. code-block:: console

  job                    count
  -------------------  -------
  all                        1
  benchmark_all              1
  consensus                  5
  knit_report                1
  predict_Correlation        5
  predict_SciBet             5
  predict_SingleR            5
  predict_Symphony           5
  predict_scClassify         5
  subset_folds               1
  train_Correlation          5
  train_SciBet               5
  train_SingleR              5
  train_Symphony             5
  train_scClassify           5
  total                     59
  
.. raw:: html

  <details>
    <summary>Exercise</summary>
    Change the number of folds or remove a method from the config file. How does the dry run output change?
  </details>
  

**3. Run the pipeline** 

Now that you've made sure that the dry run works you are ready to run the benchmarkig pipeline! Remove the :code:`-n` flag from your script:

.. code-block:: console

  # run benchmarking pipeline 
  apptainer exec --contain --cleanenv --pwd "$PWD" $image snakemake -s ${snakefile} --configfile ${config} --cores 1 --rerun-incomplete --keep-going
  
Now you're ready to run the benchmarking pipeline! 

Run script in command line

.. code-block:: console
  
  ./Scripts/run_benchmark.sh
  
or submitt as a job 

.. code-block:: console
  
  sbatch ./Scripts/run_benchmark.sh

Another important flag is :code:`--cores`. This parameter lets you parallelize the pipeline. If you add :code:`--cores 5`, 5 steps will be run in paralell instead of 1. Make sure the number of cores match the slurm (or other scheduler) parameters in your run script if you are submitting the job for optimal use of resources. 

.. raw:: html

  <details>
    <summary>Exercise</summary>
    Change the number of cores from 1 to 5 in the snakemake command and the slurm header. The pipeline should finish 5 times as fast!!
  </details>
  
  
**4. Monitor pipeline** 

Check pipleine progress in the logs:

.. code-block:: console
  
  cat logs/CoRAL.benchmark.err
  
When the pipeline is done it should print :code:`59 of 59 steps (100%) done` in the log file! 

**5. Check output files** 

The most important files outputed by the pipeline is: 
- The :code:`.html` report generated as the final step in the pipeline in :code:`Out/Benchmark/test_reference/report/`. This report contains plots and information about the cross-validation.
- The perfomance metrics found in :code:`Out/Benchmark/test_reference/report/metrics_label.csv`. This file has F1, precission and recall for each method and class in the reference data. 

.. raw:: html

  <details>
    <summary>Exercise</summary>
    Find the section in the documentation where all the available methods are listed. Add a few more to your config file and do a dry run 
    again. Does the pipeline try to rerun all the methods or just the new methods? 
  </details>
  

Run the training pipeline 
----------------------------

**1. Set up the config file** 

Now that you have run the benchmarking pipeline you can run the training pipeline. The first thing you need to do is check the config file for the train pipeline

.. code-block:: console

  cat ConfigFiles/train.yml

The only thing that is different is the :code:`mode` and that you need to add a parameter for the output directory: :code:`output_dir`

.. code-block:: console

  # pipeline to run 
  mode: 'pretrain'

  # output directory 
  output_dir: Out/Train

Make sure to update all the paths to the full paths!!!

**2. Set up run script**

Check the run script file for the train pipeline

.. code-block:: console

  cat Scripts/run_train.sh


It's exactly the same as the benchmarking but now you specify `train.yml` as the config file

.. code-block:: console

  config=${PWD}/ConfigFiles/train.yml

Before running the pipeline perform a dry run with the :code:`-n` flag like before

.. code-block:: console

  ./Scripts/run_train.sh

The output of the dry run should look like this. The pipeline will run one training step per method specified in the config

.. code-block:: console

  job                  count
  -----------------  -------
  all                      1
  preprocess               1
  pretrain_all             1
  train_Correlation        1
  train_SciBet             1
  train_SingleR            1
  train_Symphony           1
  train_scClassify         1
  total                    8

Now that you've made sure that the dry run works you are ready to run the training pipeline! Remove the :code:`-n` flag from your script: 

.. code-block:: console

  # run benchmarking pipeline 
  apptainer exec --contain --cleanenv --pwd "$PWD" $image snakemake -s ${snakefile} --configfile ${config} --cores 1 --rerun-incomplete --keep-going

Run script in command line 

.. code-block:: console
  
  ./Scripts/run_train.sh
  
or submitt as a job 

.. code-block:: console
  
  sbatch ./Scripts/run_train.sh
  
**4. Monitor pipeline** 

Check pipleine progress in the logs:

.. code-block:: console

  cat logs/CoRAL.train.err

When the pipeline is done it should print :code:`8 of 8 steps (100%) done` in the log file! 

.. raw:: html

  <details>
    <summary>Exercise</summary>
    Find the section in the documentation where all the available methods are listed. Add a few more to your config file and do a dry run 
    again. Does the pipeline try to rerun all the methods or just the new methods? 
  </details>
  

**5. Check output files** 

The most important files outputed by the pipeline is the model files for each method. These are the models used in the annotation pipeline. 

.. code-block:: console

  Out/Train/model/test_reference/Correlation/Correlation_model.Rda
  Out/Train/model/test_reference/SciBet/SciBet_model.Rda
  Out/Train/model/test_reference/SingleR/SingleR_model.Rda
  Out/Train/model/test_reference/Symphony/Symphony_model.Rda
  Out/Train/model/test_reference/scClassify/scClassify_model.Rda

Run the annotation pipeline
--------------------------------

**1. Set up the config file** 

Now you are finally ready to run the annotation pipeline!! The first thing you need to do is check the config file for the annotation pipeline

.. code-block:: console

  cat ConfigFiles/annotate.yml

The mode has now changed to annotate and the output directory has been updated 

.. code-block:: yaml

  # pipeline to run 
  mode: 'annotate'

  # output directory 
  output_dir: Out/Annotate


In the reference section everything is the same except :code:`pretrain_models`, which is now filled out with the path to the models you trained in the previous section. 

.. code-block:: yaml

  # reference parameters 
  references:
     test_reference:
        expression: Reference/expression.csv
        labels: Reference/labels.csv
        output_dir_benchmark: Out/Benchmark
        pretrain_models: Out/Train/models/test_reference

A section has also been added with the query samples. In this case we have added 3 samples from a cortical developmental mouse atlas from embryonic day 16 (ct_e16), post-natal day 0 (ct_p0), and post natal day 6 (ct_p6). 

.. code-block:: yaml

  # paths to query data sets 
  query_datasets:
        ct_e16: Query/ct_e16/expression.csv
        ct_p0: Query/ct_p0/expression.csv
        ct_p6: Query/ct_p6/expression.csv

Make sure to update all the paths to the full paths!!!

Finally the consensus section has been updated to include paramters for CAWPE (weighted ensemble voting) and majority vote. CAWPE only works if you have run the benchmarking, since it needs the accuracy metrics from the benchmarking to weight the conseunsus. 

.. code-block:: yaml

  # consensus prameters 
  consensus:
        tools:
              - 'all'
        type:
              majority:
                   min_agree: [2]
              CAWPE:
                   mode: ['CAWPE_T']
                   alpha: [4]
                   metric: 'F1'

**2. Set up run script**

Check the run script file for the train pipeline

.. code-block:: console

  cat Scripts/run_annotate.sh

It's exactly the same as the benchmarking but now you specify :code:`annotate.yml` as the config file. 

.. code-block:: console

  config=${PWD}/ConfigFiles/annotate.yml

Before running the pipeline perform a dry run with the :code:`-n` flag like before

.. code-block:: console
  
  ./Scripts/run_annotate.sh

The output of the dry run should look like this. The pipeline will run one prediction step per method and sample specified in the config

.. code-block:: console

  job                    count
  -------------------  -------
  all                        1
  annotate_all               1
  consensus                  3
  knit_report                3
  ontology                   1
  predict_Correlation        3
  predict_SciBet             3
  predict_SingleR            3
  predict_Symphony           3
  predict_scClassify         3
  preprocess                 1
  total                     25

.. raw:: html
  
  <details>
    <summary>Exercise</summary>
    You can add more values in the list of min_agree and alpha. What happens if you change alpha to [2, 4] or min_agree or [2, 3]. Do a dry
     run to find out!!
  </details>
  

Now that you've made sure that the dry run works you are ready to run the annotation pipeline! Remove the `-n` flag from your script: 

.. code-block:: console

  # run benchmarking pipeline 
  apptainer exec --contain --cleanenv --pwd "$PWD" $image snakemake -s ${snakefile} --configfile ${config} --cores 1 --rerun-incomplete --keep-going

Run script in command line 

.. code-block:: console

  ./Scripts/run_annotate.sh

or submitt as a job 

.. code-block:: console

  sbatch ./Scripts/run_annotate.sh

**4. Monitor pipeline** 

Check pipleine progress in the logs:

.. code-block:: console

  cat logs/CoRAL.annotate.err

When the pipeline is done it should print :code:`25 of 25 steps (100%) done` in the log file! 

**5. Check output files** 

The most important files outputed by the pipeline is: 
- The html reports for each sample and reference found in the reports folder: :code:`Out/Annotate/ct_p6/report/`
- The :code:`.csv` files with all the prediction results from the individual methods and the consensus:
  :code:`Out/Annotate/ct_p6/test_reference/majority/Prediction_Summary_label.tsv`
  :code:`Out/Annotate/ct_p6/test_reference/CAWPE/Prediction_Summary_label.tsv`
- The :code:`.csv` file with the CAWPE scores: :code:`Out/Annotate/ct_p6/test_reference/CAWPE/CAWPE_T_4_label_scores.csv`

Additional features 
----------------------

**1. Add an celltype otology for your reference dataset in the benchmarking pipeline** 

In many cases you might have groups of related cell types in your reference data set that you want to merge together. You might have 5 types of neurons but you don't care which type of neuron your cell is, you just care if it's a neuron or not. In this case you can add a cell type ontology file for you're reference data set. You can find an example of this file in :code:`Reference/ontology.csv`

To see the content of this file run:

.. code-block:: console

  cat Reference/ontology.csv


This :code:`.csv` file maps each label in the reference to a higher level category, like Neuron, Astrocyte or Immune. 

Open your config file :code:'ConfigFiles/benchmark.yml' and add the ontology file to the reference section like this (add the full path):

.. code-block:: yaml
  
  # reference parameters 
  references:
     test_reference:
        expression: expression.csv
        labels: Reference/labels.csv
        output_dir_benchmark: Out/Benchmark
        ontology:
           ontology_path: Reference/ontology.csv

Now perform a dryrun like before (add the :code:`-n` flag in your pipeline command and run the script in the command line) 

The output of the drydun should look like this:

.. code-block:: console

  job              count
  -------------  -------
  all                  1
  benchmark_all        1
  consensus            5
  knit_report          2
  total                9

The pipeline is not reruning any of the training and prediction, it's just recomputing the consensus and generating new reports for the different levels of ontology. 


Now remove the :code:`-n` flag and rerun the pipeline. When it's done, check the reports folder again and you will see that there is a report for each ontology level! 

.. raw:: html

  <details>
    <summary>Exercise</summary>
    Compare the reports from the different ontology levels. Is the performace better or worse for the higher level ontology?
  </details>
  

**2. Add an celltype otology for your reference dataset in the annotateion pipeline** 

Now that you've added the ontology in the benchmarking pipeline you can do the same for the annotation pipeline. Do the same steps as for the benchmarking: 

- Add the ontology in the config file
- Perform a dry run (the pipeline should not rerun any of the prediction steps, just the consensus and report steps)
- Run the workflow again
- Check the reports folder

.. raw:: html

  <details>
    <summary>Exercise</summary>
    Compare the reports from the different ontology levels. Is the performace better or worse for the higher level ontology?
  </details>
  

**3. Use Seurat or SingleCellExperiment objects as input instead of .csv** 

It is possible to input :code:`Seurat` (v3 or v4) or :code:`SingleCellExperiment` objects instead of :code:`.csv` files for both the reference and the query data sets. The objects need to be saved as :code:`.Rda` or :code:`.Rds`. 

If you had a reference data set saved as :code:`Reference.Rda` in the Reference folder you would specify it like this in the config file: 

.. code-block:: yaml

  # reference parameters 
  references:
     test_reference:
        expression: Reference/Reference.Rda 
        labels: 'celltype'
        output_dir_benchmark: Out/Benchmark

Notice that the :code:`labels:` parameter is now a column name in the meta data of the object instead of a :code:`.csv` file. The column can be named anything and it's specified in the same way for Seurat or SingleCellExperiment.

If you have your query samples saved as Seurat or SingleCellExperiment you would specify them like this:

.. code-block:: yaml

  # paths to query data sets 
  query_datasets:
        ct_e16: Query/ct_e16/expression.Rda
        ct_p0: Query/ct_p0/expression.Rda
        ct_p6: Query/ct_p6/expression.Rda

You could also have a mix of :code:`.Rda`, :code:`.Rds` and :code:`.csv`! 

.. code-block:: yaml

  # paths to query data sets 
  query_datasets:
        ct_e16: Query/ct_e16/expression.Rds
        ct_p0: Query/ct_p0/expression.Rda
        ct_p6: Query/ct_p6/expression.csv

.. raw:: html

  <details>
    <summary>Exercise</summary>
    If you are very ambitious you can try to save the .csv files as seurat objects and rerun the pipeline with these! 
    
  </details>
  

Tutorial Over!! 
------------------

Good job! For more information about each pipline, snakemake, parameters and other things see the rest of this documentation. 

.. raw:: html

  <details>
    <summary>Exercise</summary>
    Use your own data!! :) 
    
  </details>
  
