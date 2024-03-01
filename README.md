# Differential Expression Analysis Wrapper
This repository contains a wrapper.py script that automates the execution of the Kallisto/Sleuth pipeline for differential expression analysis.

## Running the Wrapper Script
Clone this repository, ensure that all dependencies are installed, ensure that your data is in the proper format (or utilize the Sample Test Data), and then run the following command:
```
python3 wrapper.py -o <OUTPUT-DIRECTORY> -a <NCBI-ACCESSION> -e <EMAIL> -d <SEQUENCING-DATA-DIRECTORY> -l <DESIRED-LOG-FILE-NAME> -s <SUBFAMILY>
```
* Output Directory: Directory where all outputted files and folders will be stored.

* NCBI Accession: The accession number needed to build the appropriate transcriptome index.

* Email: Your email address (needed for NCBI searches)

* Sequencing Data Directory: The directory name where your sequencing data is stored.

* Desired Log File Name: Whatever you would like to name your log file.

* Subfamily: The subfamily associated with your sequencing data.

Ex. The command I used when running wrapper.py with the Sample Test Data:
```
python3 wrapper.py -o PipelineProject_Madeline_Hakala -a  NC_006273.2 -e mhakala@luc.edu -d sampleData -l PipelineProject.log -s Betaherpesvirinae
```

## Required Dependencies
* Linux: kallisto, ncbi-blast+

* Python: biopython, pandas

* R: sleuth, dplyr

## Full Test Data
Human herpesvirus 5 (HCMV) transcriptomes from two donors, both 2 days and 6 days post-infection (Cheng et al., 2017). Transcriptomes were obtained by searching in SRA Explorer by SRR number and saving the resulting curl commands. The individual commands were then combined into one shell script and updated to ensure that files were downloaded in the required format to run the wrapper.py script. 

SRR Numbers: SRX2896360, SRX2896363, SRX2896374, SRX2896375

To download the full test data yourself in the required format, run the following command:
```
ssh downloadChengData.sh
```
Note: If you are using your own sequencing data, ensure it is in the following format:

* Data --> Sample --> FwdRead RevRead

* Sample names should be "SUBJECT-CONDITION". The forward read should end in "_1", and the reverse read should end in "_2".

## Sample Test Data
To test the wrapper.py script with shortened data, utilize "sampleData". This folder contains shortened versions of the full test data's fasta files.