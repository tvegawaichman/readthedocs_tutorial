🧬 Feature Space
==========

.. _feature_space:

For each tool the feature space can be set to either :code:`intersection` or :code:`complete`.
**Intersection** means that the intersect of genes between reference and all query samples in the config file is used for the training and testing.
**Compelete** means that the complete fetaure space of the reference is used, and the feature space of the query is modified to match (extra genes removed and missing genes set to 0). 
When pretrained models are used for annotation task, :code:`complete` is the default mode for all the tools.
When training and annotation are done together, :code:`intersection` is the default mode for all the tools.
Additionally, the feature space can be specified for each method manually in the following way:

.. code-block:: yaml

  SVMlinear:
    gene_selection: "intersection"
  
or

.. code-block:: yaml

  SVMlinear:
      gene_selection: "complete"

TODO: **SCHEMA OF THIS**