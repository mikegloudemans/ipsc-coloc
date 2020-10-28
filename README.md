# i2QTL Colocalization Analysis

Analysis performed by Mike Gloudemans
Updated 1/21/2020

## Summary

This repository contains the scripts required to generate the colocalization scores described in the paper.
Most figure-level analysis is outside of the scope of this repository; the aim of this repository is merely
to show how the colocalization scores were generated using FINEMAP and the eCAVIAR formula, and to hopefully
give an idea of how similar analyses could be run.

The top-level project directory should contain the folders `bin`, `data`, `output`, `tmp`, and `scripts`. All scripts must be
run from this top-level directory, or they'll be unable to locate the required files.

The file `pipe.sh` gives a step-by-step pipeline outlining all necessary steps.

### Components within `scripts` folder

#### `scripts/auxiliary`

QC and/or other analyses not directly used in the generation of colocalization results.

#### `scripts/colocalization`

Scripts to launch the main colocalization portion of the analysis.

#### `scripts/post_coloc`

A few post-processing steps, to combine the results into one big table after running colocalization
analysis.

#### `scripts/pre_coloc`

Some formatting steps required to shape the raw QTL and GWAS data into the format required for running
colocalization analysis.

## Required Tools

The following analyses were performed using other publicly available tools. To fully complete the
analyses, you will have to install or link these tools within the `bin` subfolder, or modify the
`pipe.sh` script to include the paths to the directories where these tools are installed.

* The tools for downloading and munging the publicly available GWAS summary statistics
are available at https://github.com/mikegloudemans/gwas-download/. (The UKBB, PhenomeScanner, and
GWAS Catalog corpora are not explicitly included, but straightforward tools exist for downloading
summary statistics in bulk from these other sources.)
* The analysis performed in this paper uses an integration of the publicly available tools [FINEMAP](http://www.christianbenner.com/) (Benner et al. 2016)
and [eCAVIAR](http://zarlab.cs.ucla.edu/tag/ecaviar/) (Hormozdiari et al. 2016). My pipeline that uses these methods is available in a basic form
at https://bitbucket.org/mgloud/production_coloc_pipeline/src, where you'll find further instructions for setting up the general colocalization analysis
framework. An extended and hopefully easier-to-use pipeline with a greater variety of options and analyses, closer to what was used for this
paper, will soon be available at https://github.com/mikegloudemans/ensemble_coloc_pipeline.
* Graphical visualization of colocalizations was performed using [LocusCompare](https://locuscompare.com) (Liu et al. 2019)
but this tool is not strictly required to reproduce the results in this paper.

## Required Data

This project makes uses of a variety of data tables, some already publicly available
and some internally generated. I'm currently exploring ways to just link all or most of the required
data files here as a single download. Until then, please contact me directly (see _Contact_ section below) and I'll share 
the relevant files directly, ASAP.

90% of the analysis, including the core colocalization analysis can be completed using just the following
data files:

### Getting started
TODO TODO TODO

* eQTL files were obtained through the i2QTL Consortium and should be obtained directly from the owners
of that project.
* GWAS summary statistics for the LocusCompare portion of the analysis are publicly available; consistently-formatted versions of these and other GWAS can be [downloaded directly](https://github.com/mikegloudemans/gwas-download).

* An hg38-formatted version of the [1000 Genomes VCF](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/)
is required for computing allele frequencies in a reference population.

### All required data

To run all the scripts listed here, the `data` folder technically needs to contain all of the following files:

* `data/1KG`: 1KG VCF for hg19, publicly available for download as described above.
* `data/gwas`: GWAS summary statistics for all traits of interest. (Download process described above)
* `data/qtls`: The QTL summary association statistics for all molecular traits measured in iPSC.
This folder should additional contain subdirectories for each iPSC molecular QTL of interest, including
`trans_eqtl` if that is one you wish to run.

## Contact

For any questions about this colocalization processing pipeline, 
please contact Mike Gloudemans (mgloud@stanford.edu). I'll be glad to help you get these analyses up and running!

