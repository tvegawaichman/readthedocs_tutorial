Usage
=====

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

**cell x gene matrix**

.. code-block:: console
  '',gene1,gene2,gene3
  cell1,1,24,30
  cell2,54,20,61
  cell3,0,12,0
  cell4,1,13,17


**cell x label matrix**

.. code-block:: console
  '',label 
  cell1,label1
  cell2,label1
  cell3,label3
  cell4,label2

Also, the input format for the reference could be a **Seurat** or **SingleCellExperiment** object. 
In the expression the path to the object should be specified (formats .rda, .rds). And in the labels the metadata column used for the labels.
If the format for the expression is .rda or .rds it assumes that the labels is a vector where it's the column name.
In the **Seurat** objects are compatible until v4. 
In the **SingleCellExperiment** it assumes that the raw counts is in the 'counts' assay.

3. Prepare query samples
----------------

The input format for the query samples could be a **cell x gene matrix** (.csv) of raw counts, seurat object or single cell experiment object with raw counts. 

The first column needs to be the cell names with an empty column name.

**cell x gene matrix**
.. code-block:: console
  '',gene1,gene2,gene3
  cell1,27,1,34
  cell2,0,12,56
  cell3,0,17,12
  cell4,54,20,61

Also, the input format for the reference could be a **Seurat** or **SingleCellExperiment** object. 
In the expression the path to the object should be specified (formats .rda, .rds). And in the labels the metadata column used for the labels.
In the **Seurat** objects are compatible until v4. 
In the **SingleCellExperiment** it assumes that the raw counts is in the 'counts' assay.

4. Prepare config file
----------------

