import argparse
import sys
import os
import shutil
import Bio
from Bio import Entrez, SeqIO
import pandas as pd

def check_arg(args = None):
	'''Parses command line arguments.'''
	parser = argparse.ArgumentParser(description = 'Python wrapper for differential expression analysis using the Kallisto-Sleuth pipeline.')
	parser.add_argument('-o', '--outputDirectory',
		help = 'Directory where all outputed files and folders will be stored',
		required = 'True'
		)	
	parser.add_argument('-a', '--NCBIaccession',
		help = 'NCBI Accession Number',
		required = 'True'
		)
	parser.add_argument('-e', '--email',
		help = 'Your Email Address',
		required = 'True'
		)
	parser.add_argument('-d', '--sequencingDataDirectory',
		help = 'Directory with sequencing data',
		required = 'True'
		)
	parser.add_argument('-l', '--logFileName',
		help = 'Desired Log File Name',
		required = 'True'
		)
	parser.add_argument('-s', '--subfamily',
		help = 'Subfamily',
		required = 'True'
		)
	return parser.parse_args(args)

def initializeOutputDirectory(directory):
  '''Initializes a directory where all outputted files, folders, etc will be stored.'''
  if os.path.exists(directory): # if the directory with that name already exists, remove it
    shutil.rmtree(directory)
  os.makedirs(directory) # then make the directory and move into it
  os.chdir(directory)
  
def createLog(logFileName):
  '''Creates an empty log file where run info will be stored.'''
  logFile = open(logFileName, 'w')
  return logFile

def getReferenceTranscriptome(accession, email):
  '''Gets the reference transcriptome using NCBI accession.'''
  Entrez.email = email # setting email
  handle = Entrez.efetch(db = 'nucleotide', id = accession, rettype = 'gb', retmode = 'text') # search handle for the specified accession 
  records = SeqIO.parse(handle, format = 'genbank') # parsing the handle
  reference = []
  for record in records:  # for each record (records is set up as a list, so even though there is only one here, treat it like a list)
    cds_features = [feature for feature in record.features if feature.type == 'CDS'] # extract CDS features
  for feature in cds_features: # for each CDS feature
    seq = Bio.Seq.Seq(feature.extract(record.seq)) # extract the sequence and the protein id
    id = feature.qualifiers['protein_id'][0]
    reference.append(Bio.SeqRecord.SeqRecord(seq, id = id)) # append them to the reference list
  numCDS = len(cds_features)
  referenceFile = f'{accession}-transcriptomeRecord.fasta'
  SeqIO.write(reference, referenceFile, 'fasta') # write the reference CDS's to the reference fasta file
  return {'referenceFilePath': referenceFile, 'numCDS': numCDS}

def makeIndex(referenceTranscriptome):
  '''Makes the transcriptome reference index using the reference transcriptome.'''
  indexFilename = 'index.idx'
  kallistoIndexCommand = f'kallisto index -i {indexFilename} {referenceTranscriptome["referenceFilePath"]}' # kallisto command to make index
  os.system(kallistoIndexCommand) # run kallisto index command
  logFile.write(f'The HCMV genome (NC_006273.2) has {referenceTranscriptome["numCDS"]} CDS.') # write the # of CDS's to the output file
  logFile.write('\n------------------------------')
  return indexFilename
  
def kallistoRun(data, index):
  '''Runs Kallisto using sequencing data and the index file.'''
  for pairDir in os.listdir(f'../{data}'): # for each forward/reverse pair in the sequencing data directory
    baseFileName = os.listdir(f'../{data}/{pairDir}')[0][:-10] # get the base file name, which is everything before the 1 or 2
    forward = f'../{data}/{pairDir}/{baseFileName}1.fastq.gz' # define which is fwd and which is rev
    reverse = f'../{data}/{pairDir}/{baseFileName}2.fastq.gz'
    kallistoOutputDir = f'kallistoOutput/{pairDir}'
    os.makedirs(kallistoOutputDir) # make the output directory for kallisto results
    kallistoRun = f'time kallisto quant -i {index} -o {kallistoOutputDir} -b 30 -t 4 {forward} {reverse}' # kallisto command
    os.system(kallistoRun) # run kallisto
  logFile.write('\nsample  condition  min_tpm  med_tpm  mean_tpm  max_tpm') # write column names to the log file
  for sample in os.listdir('kallistoOutput'):
    df = pd.read_table(f'kallistoOutput/{sample}/abundance.tsv')
    min_tpm = df['tpm'].min()
    med_tpm = df['tpm'].median()
    mean_tpm = df['tpm'].mean()
    max_tpm = df['tpm'].max()
    logFile.write(f'\n{sample}  {sample.split("-")[1]}  {min_tpm}  {med_tpm}  {mean_tpm}  {max_tpm}') # write kalisto output to the log file
  logFile.write('\n------------------------------\n')
  with open('kallistoMetadata.txt', 'w') as f: # create metadata file to use for sleuth run
    f.write('sample  condition  path\n')
    for sample in os.listdir('kallistoOutput'):
      f.write(f'{sample}  {sample.split("-")[1]}  kallistoOutput/{sample}\n')

def callSleuthRscript(sleuthRscript):
  '''Function to call the sleuth script, which is an Rscript.'''
  callingSleuth = f'Rscript {sleuthRscript}'
  os.system(callingSleuth)
  with open('resultsFDR05.txt', 'r') as f: # write results (stored in resultsFDR05.txt) to the log file
    text = f.readlines()
    for line in text:
      tempLine = line.split()
      tempLineAsString = '  '.join(tempLine)
      logFile.write(f'{tempLineAsString}\n')
  logFile.write('------------------------------\n')
  mostDiffExpressedCDS = text[1].split()[0]
  return mostDiffExpressedCDS

def blast(mostDiffExpressedCDS, subfamily):
  '''Blast the most differentially expressed CDS to find which other virus strains have genes encoding it.'''
  Entrez.email = email
  outputFile = f'{mostDiffExpressedCDS}.fasta'
  handle = Entrez.efetch(db = 'protein', id = mostDiffExpressedCDS, rettype = 'gb', retmode = 'text') # handle to search for most DE CDS
  records = SeqIO.parse(handle, format = 'genbank') # parsing the handle
  for record in records: # for each record (even though there is only one, it is formatted as a list)
    protein = SeqIO.SeqRecord(record.seq, id = record.id) # define protein as the SeqRecord of that record
  SeqIO.write(protein, outputFile, 'fasta') # write protein to an output fasta file
  download = f'datasets download virus genome taxon {subfamily} --refseq --include genome' # downloads an NCBI dataset of a specified subfamily
  os.system(download)
  unzip = 'unzip ncbi_dataset.zip' # unzips the dataset
  os.system(unzip)
  makeBlastDb = f'makeblastdb -in ncbi_dataset/data/genomic.fna -out {subfamily} -title {subfamily} -dbtype nucl' # makes a database to be used w/ blast using the downloaded genomic.fna file and specified subfamily
  os.system(makeBlastDb) # run command to make the db for blast
  blastCommand = f'tblastn -query {outputFile} -db {subfamily} -out {mostDiffExpressedCDS}BlastResults.csv -outfmt "6 sacc pident length qstart qend sstart send bitscore evalue stitle"'
  os.system(blastCommand) # runs above blast command to query the protein fasta (outputFile) against the subfamily database (using tblastn because the goal is to query a protein against a nucleotide db)
  logFile.write('sacc  pident  length  qstart  qend  sstart  send  bitscore  evalue  stitle\n')
  with open(f'{mostDiffExpressedCDS}BlastResults.csv', 'r') as r:
    blastResults = r.readlines()
    for i in range(10): # writting top 10 results to the log file
      tempResult = blastResults[i].split('\t')
      tempResultAsString = "  ".join(tempResult)
      logFile.write(f'{tempResultAsString}')

# retrieving command line arguments and assigning to variables
args = check_arg(sys.argv[1:])
outputDir = args.outputDirectory
accession = args.NCBIaccession
email = args.email
dataDirectory = args.sequencingDataDirectory
logFileName = args.logFileName
subfamily = args.subfamily

initializeOutputDirectory(outputDir)
logFile = createLog(logFileName)
refTranscriptome = getReferenceTranscriptome(accession, email)
index = makeIndex(refTranscriptome)
kallisto = kallistoRun(dataDirectory, index)
sleuth = callSleuthRscript('../sleuth.R')
blastRun = blast(sleuth, subfamily)
