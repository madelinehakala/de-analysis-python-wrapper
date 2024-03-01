mkdir data
cd data
mkdir donor1-2dpi
mkdir donor1-6dpi
mkdir donor3-2dpi
mkdir donor3-6dpi
curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR566/000/SRR5660030/SRR5660030_1.fastq.gz -o donor1-2dpi/SRR5660030_GSM2653763_Donor_1_WT_2dpi_SS_Human_betaherpesvirus_5_RNA-Seq_1.fastq.gz
curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR566/000/SRR5660030/SRR5660030_2.fastq.gz -o donor1-2dpi/SRR5660030_GSM2653763_Donor_1_WT_2dpi_SS_Human_betaherpesvirus_5_RNA-Seq_2.fastq.gz
curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR566/003/SRR5660033/SRR5660033_1.fastq.gz -o donor1-6dpi/SRR5660033_GSM2653766_Donor_1_WT_6dpi_SS_Human_betaherpesvirus_5_RNA-Seq_1.fastq.gz
curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR566/003/SRR5660033/SRR5660033_2.fastq.gz -o donor1-6dpi/SRR5660033_GSM2653766_Donor_1_WT_6dpi_SS_Human_betaherpesvirus_5_RNA-Seq_2.fastq.gz
curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR566/004/SRR5660044/SRR5660044_1.fastq.gz -o donor3-2dpi/SRR5660044_GSM2653777_Donor_3_WT_2dpi_SS_Human_betaherpesvirus_5_RNA-Seq_1.fastq.gz
curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR566/004/SRR5660044/SRR5660044_2.fastq.gz -o donor3-2dpi/SRR5660044_GSM2653777_Donor_3_WT_2dpi_SS_Human_betaherpesvirus_5_RNA-Seq_2.fastq.gz
curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR566/005/SRR5660045/SRR5660045_1.fastq.gz -o donor3-6dpi/SRR5660045_GSM2653778_Donor_3_WT_6dpi_SS_Human_betaherpesvirus_5_RNA-Seq_1.fastq.gz
curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR566/005/SRR5660045/SRR5660045_2.fastq.gz -o donor3-6dpi/SRR5660045_GSM2653778_Donor_3_WT_6dpi_SS_Human_betaherpesvirus_5_RNA-Seq_2.fastq.gz