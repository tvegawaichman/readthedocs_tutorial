Choosing the consensus methods
==============================

.. _consensus:

scCoAnnotate offers two options for calculating the consensus between tools, Majority Vote and CAWPE (Cross-validation Accuracy Weighted Probabilistic Ensemble). The consensus method is specified in the config: 

.. code-block:: yaml

  # consensus method
  consensus:
        tools: 
              - 'all'
        type:
              majority:
                    # (ex: [2], [2,3,4])
                    min_agree: <minimum agreemeent to use>
              CAWPE:
                    #(ex: ['CAWPE_T'], ['CAWPE_T','CAWPE_CT'])
                    mode: <CAWPE MODE>
                    #(ex: [4], [2,3,4])
                    alpha: <alpha value>


The pipeline will generate one table and one html report per consensus method. 

Majority Vote 
------------

*TODO: describe method*

CAWPE 
------------

*TODO: describe method*
