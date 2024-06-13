<p align="center">
    <img
        src="https://gitlab.com/xonq/mycotools/-/raw/master/misc/pictogo.white.png"
    >
</p>

<br /><br />

# NOTE
This software is a beta release - kindly raise an issue for errors.

# PURPOSE
Bring broadscale comparative genomics to the masses. 

Mycotools is a compilation of computational biology tools and database
([MycotoolsDB/MTDB](https://github.com/xonq/mycotools/blob/master/MTDB.md)) software
that facilitate large-scale comparative genomics. MycotoolsDB dereplicates and locally
assimilates NCBI and MycoCosm (Joint Genome Institute) genomes into a database schema with uniform file curation, scalability, and automation as guiding principles. 

- Database initialization: `mtdb u --init <DIR>`
- Database updating: `mtdb u --update`
- The MycotoolsDB (MTDB) uniformly curates GenBank/MycoCosm and local `gff` formats into a consistent standard
- The `.mtdb` database format is a uniform input for analyses with 100,000s to as few as a single genome
- Mycotools [software suite](https://github.com/xonq/mycotools/blob/master/USAGE.md) includes modules to automate routine-complex
  comparative genomics, such as phylogenetic analysis

<p align="center">
    <img
        src="https://gitlab.com/xonq/mycotools/-/raw/master/misc/mtdb.png"
    >
</p>

<br />

# CITING

If Mycotools contribute to your analysis, please cite the preprint and mention
the version in-line. 

Konkel, Z., Slot, J. C. Mycotools: An Automated and Scalable Platform for
Comparative Genomics. bioRxiv 2023.09.08.556886; doi: https://doi.org/10.1101/2023.09.08.556886

---

<br />

# INSTALL

The installation guide will use miniconda3 as the environment manager. Please
reference their [install and initialization instructions](https://docs.conda.io/projects/miniconda/en/latest/).

<br />

## 1. Configuring miniconda3
Setup and prioritize channels for your miniconda installation. This step must be
completed for new and old installs.

```bash
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```

<br />

## 2. Installing mycotools
Make sure `conda` is active, usually by seeing `(base)` in in your shell.
If not, try `conda activate base` or `source activate base`. 

```bash
conda create -n mycotools mycotools
conda activate mycotools
mtdb -d
```

IF the above installation does not work, you can create a conda environment manually, activate it, then install mycotools via `python3 -m pip install mycotools`. 

<br />

Determine if you are going to link to an already installed database, or become
the administrator of a new one:

## 3a. USER: Integrate with already initialized MycotoolsDB
To link with an existing database, fill in `<PATH>` with the database path

```bash
mtdb -i <DB_PATH>
```

<br />

## 3b. ADMINISTRATOR: Initialize a local MycotoolsDB
```bash
mtdb update -i <DB_PATH>
```

<br /><br />

# USAGE

Once installed, you're good to proceed to the
[usage guide!](https://github.com/xonq/mycotools/blob/master/USAGE.md)


<br /><br />

# UPDATE
Mycotools is currently in an advanced beta state with frequent updates. It is
recommended to run the following in your conda environment if you are having
trouble with analyses:

```bash
conda update mycotools
```

<br /><br /><br />

### A NOTE ON THE CODE
Each standalone script is written with a `cli` function, designed to
handle running the script from the command line, as well as `main` function(s),
which are importable python modules. This enables Mycotools
to be a pipelining-friendly software suite, both from a command line and
python scripting standpoint.

Code edits should focus on stabilizing existing features and simplifying/decerasing the code base.
I try to implement code aligned with principles of the [functional
programming paradigm](https://docs.python.org/3/howto/functional.html) and
modifications should act in accord with this paradigm, i.e. sparing
implementation of new classes, limited necessary abstraction, no hidden state
changes, and function-based flow.


<img align="right" src="https://gitlab.com/xonq/mycotools/-/raw/master/misc/ablogo.png">

<br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
