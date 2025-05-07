🙋‍♀ FAQ 🙋‍♂️
===============

🐍 Snakemake Tips and Tricks 
------------

- Dryrun snakemake pipeline before submitting job 

.. code-block:: bash

  snakemake -s ${snakefile} --configfile ${config} -n


- Unlock working directory before running (in case previous run crashed) by adding this to your script

.. code-block:: bash

  snakemake -s ${snakefile} --configfile ${config} --unlock 

- Add `--rerun-incomplete` if snakemake finds incomplete files from a previous run that was not successfully removed 

.. code-block:: bash

  snakemake -s ${snakefile} --configfile ${config} --rerun-incomplete 

- Add `--keep-going` to allow independent rules to keep running when something fails 

.. code-block:: bash

  snakemake -s ${snakefile} --configfile ${config} --keep-going


- Update time stamp on files to avoid rerunning rules if code has changed 

.. code-block:: bash

  snakemake -s ${snakefile} --configfile ${config} -c1 -R $(snakemake -s ${snakefile} --configfile     ${config} -c1 --list-code-changes) --touch 

- Generate a report with information about the snakemake workflow 

.. code-block:: bash
  
  snakemake -s ${snakefile} --configfile ${config} --report ${report}
