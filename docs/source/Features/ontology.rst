.. _ontology:

🌳 Ontology
==========

1. What's an ontology
------------

An ontology could be summarised as a hierarchical graph of hierarchy of nested granular classes within broader classes.
After predicting at one level of granularity results could be summarised an re-calculated at broader class following the graph structure.

TODO, put an image

As in this example cell-type1 and cell-type2 are part of the.... EXPLAIN

2. How to add an Ontology on CoRAL
------------

After mapping the reference labels to a query the labelss can be summarized to higher ontology levels.

The ontology file needs to be a .csv file where the first column is called label. This column needs to have a complete set of the unique labels in the reference data set.
Every other column can be named anything and contain any groupings of the labels in the first column.
**IMPORTANT** Be sure that your ontology follows a nested hierarchical structure.

.. list-table:: Ontology
   :widths: 40 30 30
   :header-rows: 1

   * - label
     - celltype1
     - celltype2
     - celltype3
     - celltype4
     - celltype5
   * - subclass
     - subclass1
     - subclass1
     - subclass2
     - subclass3
     - subclass3
   * - class
     - class1
     - class1
     - class1
     - class2
     - class2

The ontology does not effect the training and mapping, and is just used when computing the final consensus.

The ontology is specified in the reference section of the config file:

.. code-block:: yaml
  
  references:
      <reference_name>:
            ontology:
              # Path to the csv containing the ontology path. Each column represents a different granularity of labels. The columns should be named.
              ontology_path: <path to ontology.csv>
              # The column name(s) of the granularity to use, from the ontology file.
              # This parameter can take multiple column names, therefore they should be put in a list, in case of none specification of the column all the ontology columns in the file will be used.
              # (ex: ['level']     ['level1', 'level2'])
                ontology_column: <ontology_column to use>

3. How Ontology is computed on CoRAL
------------

For the W matrix (weight matrix), we calculate the performance after matching each granular class to the corresponding broad class and recalculating the classification metrics in aggregate.
For the P matrix, we calculate a cell's probability of being assigned to a broad class as the sum of the probabilities of its corresponding granular classes.
Then CoRAL scores are calculated following the same original equation. (SECTION WHAT IS CAWPE) 
