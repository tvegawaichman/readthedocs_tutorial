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

To start create a folder to run the tutorial in and `cd` into it

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

You should now have a folder called `CoRAL` which contains all the code from the git repository 

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
  
If you are on a HPC cluster you can check if apptainer is available as a module. If it is installed as a moudle, load the module in your run scripts before the pipeline command! 

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