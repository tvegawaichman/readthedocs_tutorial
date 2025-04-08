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


## Lets start!! 
------------

To start create a folder to run the tutorial in and :code:`cd` into it

.. code-block:: console

  mkdir CoRAL_tutorial
  cd CoRAL_tutorial

Create a folder for the logs

.. code-block:: console

  mkdir logs


## Set up 
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
  
## Run the benchmarking pipeline 
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
