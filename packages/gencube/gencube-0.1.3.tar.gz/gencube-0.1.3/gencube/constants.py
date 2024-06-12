# 기록 - 이후에 지우기
# human_hg38_reference (528)
# mouse_mm10_reference (527)
# chicken_galGal6_reference (501)
# pikePerch_HLsanLuc1_ (1) 베스
# tobaccoHawknoth_HLmanSex2 (5) 담배나방
# thaleCress_HLParaTha1 (4) 겨자나물
# redEaredSlideTurtle_HLtraScrEle1_ (1) 붉은귀거북이
# purpleSeaUrchin_HLstrPur5_ (1) 보라성게
# greenSeaturtle_HLcheMyd2_ (1) 녹색바다거북+

# For Entrez.email
EMAIL = "newhong@snu.ac.kr"

# NCBI server (README.txt - https://ftp.ncbi.nlm.nih.gov/genomes/all/README.txt)
NCBI_FTP_URL = 'https://ftp.ncbi.nlm.nih.gov/genomes/all'

# ENSEMBL
ENSEMBL_FTP_HOST = 'ftp.ensembl.org'
ENSEMBL_FTP_URL = 'http://ftp.ensembl.org/pub/'
ENSEMBL_RAPID_FTP_URL = ENSEMBL_FTP_URL + 'rapid-release/'
ENSEMBL_RM_FTP_URL = 'https://ftp.ebi.ac.uk/pub/databases/ensembl/repeats/unfiltered_repeatmodeler/species/'

# UCSC GenArk server (the Earth BioGenome Project, the Vertebrate Genomes Project, the Telomere-to-Telomere Consortium, and other related projects.)
GENARK_URL = 'https://hgdownload.soe.ucsc.edu/hubs/'

# VGP (Vertebrate Genome Project)

# Zoonomia (200 mammals project)
ZOONOMIA_URL = 'https://genome.senckenberg.de/download/TOGA/'

## Lists
LS_NCBI_ASSEMBLY_META_KEY = [
    'Synonym_GCA',
    'Synonym_GCF',
    'LatestAccession',
    'AssemblyName',
    'UCSCName',
    'GB_BioProjects',
    'BioSampleAccn',
    'Taxid',
    'Organism',
    'AssemblyType',
    'AssemblyStatus',
    'Coverage',
    'ReleaseLevel',
    'ReleaseType',
    'AsmReleaseDate_GenBank',
    'AsmUpdateDate',
    'SubmitterOrganization',
    'ContigN50',
    'ScaffoldN50',
    'Biosource',
    'PropertyList'
    ]
LS_NCBI_ASSEMBLY_META_LABEL = [
    'Genbank',
    'RefSeq',
    'Latest accession',
    'Assembly name',
    'UCSC',
    'Bioproject',
    'Biosample',
    'Taxid',
    'Organism',
    'Assembly type',
    'Level',
    '#Coverage',
    '#ReleaseLevel',
    '#ReleaseType',
    'Release',
    'Update',
    'Organization',
    '#ContigN50',
    '#ScaffoldN50',
    '#Biosource',
    '#PropertyList'
    ]
LS_GENCUBE_GENOME_LABEL = [
    'Assembly name', 
    'Taxid',
    'Release',
    'NCBI',
    'UCSC', 
    'GenArk',
    'Ensembl',
    ]
LS_GENCUBE_GENSET_LABEL = [
    'Assembly name', 
    'Taxid',
    'Release',
    'NCBI', 
    'UCSC', 
    'GenArk',
    'Ensembl',
    'Zoonomia',
    ]
LS_GENCUBE_SEQUENCE_LABEL = [
    'Assembly name', 
    'Taxid',
    'Release',
    'NCBI', 
    'UCSC', 
    'Ensembl',
    ]
LS_GENCUBE_ANNOTATION_LABEL = [
    'Assembly name', 
    'Taxid',
    'Release',
    'NCBI', 
    'UCSC', 
    'GenArk',
    ]
LS_GENCUBE_CROSSGENOME_LABEL = [
    'Assembly name', 
    'Taxid',
    'Release',
    'NCBI', 
    'UCSC', 
    'Ensembl',
    'Zoonomia',
    ]

LS_SRA_META_STUDY_KEY = [
    'EXPERIMENT.STUDY_REF.@accession', 
    'STUDY.@alias', 
    'SAMPLE.SAMPLE_LINKS.SAMPLE_LINK.XREF_LINK.LABEL', 
    'EXPERIMENT.STUDY_REF.IDENTIFIERS.EXTERNAL_ID.#text', 
    'STUDY.DESCRIPTOR.STUDY_TITLE', 
    'STUDY.DESCRIPTOR.STUDY_ABSTRACT', 
    'EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_CONSTRUCTION_PROTOCOL', 
    'SUBMISSION.@center_name', 
    'Organization.Contact.Address.Country', 
    'RUN_SET.RUN.@published'
    ]
LS_SRA_META_SAMPLE_KEY = [
    'EXPERIMENT.@accession', 
    'SAMPLE.@accession', 
    'EXPERIMENT.DESIGN.SAMPLE_DESCRIPTOR.IDENTIFIERS.EXTERNAL_ID.#text', 
    'SAMPLE.SAMPLE_NAME.TAXON_ID', 
    'EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_STRATEGY', 
    'EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_SOURCE', 
    'EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_SELECTION', 
    'EXPERIMENT.PLATFORM.ILLUMINA.INSTRUMENT_MODEL', 
    'EXPERIMENT.TITLE', 
    'SAMPLE.TITLE', 
    'EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_NAME',
    'RUN_SET.RUN.SRAFiles.SRAFile',
    'EXPERIMENT.DESIGN.DESIGN_DESCRIPTION', 
    'SAMPLE.SAMPLE_ATTRIBUTES.SAMPLE_ATTRIBUTE', 
    'EXPERIMENT.EXPERIMENT_ATTRIBUTES.EXPERIMENT_ATTRIBUTE'
    ]
LS_SRA_META_STUDY_LABEL = [
    'SRP', 
    'GSE', 
    'BioProject', 
    'BioProject_alt', 
    'Title', 
    'Abstract', 
    'Protocol', 
    'Submission', 
    'Country', 
    'Published'
    ]
LS_SRA_META_SAMPLE_LABEL = [
    'SRX', 
    'SRS', 
    'GSM', 
    'Taxon id', 
    'Strategy', 
    'Source', 
    'Selection', 
    'Instrument model', 
    'Experiment title', 
    'Sample title', 
    'Library name',
    'File information',
    'Design description', 
    'Sample attribute', 
    'Experiment attribute'
    ]

LS_ASSEMBLY_REPORT_LABEL = [
    'Sequence-Name', 
    'Sequence-Role', 
    'Assigned-Molecule', 
    'Assigned-Molecule-Location/Type', 
    'GenBank-Accn', 
    'Relationship', 
    'RefSeq-Accn', 
    'Assembly-Unit', 
    'Sequence-Length', 
    'UCSC-style-name'
    ]

# Dictionaries
DIC_ZOONOMIA = {
    'human': 'human_hg38_reference', 
    'mouse': 'mouse_mm10_reference', 
    'chicken': 'chicken_galGal6_reference', 
    'greenSeaturtle': 'greenSeaturtle_HLcheMyd2_reference', 
    'pikePerch': 'pikePerch_HLsanLuc1_reference', 
    'purpleSeaUrchin': 'purpleSeaUrchin_HLstrPur5_reference', 
    'redEaredSlideTurtle': 'redEaredSlideTurtle_HLtraScrEle1_reference', 
    'thaleCress': 'thaleCress_HLParaTha1_reference', 
    'tobaccoHawkmoth': 'tobaccoHawkmoth_HLmanSex2_reference'
    }
DIC_STRATEGY = {
    # Genomic
    'wgs': '"wgs"', # Whole Genome Sequencing
    'wga': '"wga"', # Whole Genome Amplification
    'wxs': '"wxs"', # Whole Exome Sequencing
    'targeted': '"targeted capture"', # Targeted Capture sequencing
    'synthetic_long_read': '"synthetic long read"', # Synthetic Long Read sequencing
    'gbs': '"gbs"', # Genotyping by Sequencing
    'rad': '"rad seq"', # Restriction Site Associated DNA Sequencing
    'tn': '"tn seq"', # Tn sequencing, potentially referring to Transposon Sequencing
    'clone_end': '"clone end"', # Clone End sequencing
    # Genomic or Transcriptomic
    'amplicon': '"amplicon"', # Amplicon sequencing
    'clone': '"clone"', # Cloning sequencing
    # Transcriptomic
    'rna': '"rna seq"', # RNA sequencing
    'mrna': '"mrna seq"', # messenger RNA sequencing
    'ncrna': '"ncrna seq"', # non-coding RNA sequencing
    'ribo': '"ribo seq"', # Ribosome profiling
    'rip': '"rip seq"', # RNA Immunoprecipitation sequencing
    'mirna': '"mirna seq"', # microRNA sequencing
    'ssrna': '"ssrna seq"', # single-stranded RNA sequencing
    'est': '"est"', # Expressed Sequence Tag sequencing
    'fl_cdna': '"fl cdna"', # Full-Length complementary DNA sequencing
    # Epigenomic - Chromatin Accessibility
    'atac': '"atac seq"', # Assay for Transposase-Accessible Chromatin sequencing
    'dnase': '"dnase hypersensitivity"', # DNase Hypersensitivity sequencing
    'faire': '"faire seq"', # Formaldehyde-Assisted Isolation of Regulatory Elements sequencing
    # Epigenomic - DNA-Protein Binding
    'chip': '"chip seq" OR "chip"', # Chromatin Immunoprecipitation Sequencing
    # Epigenomic - Methylome
    'mre': '"mre seq"', # Methylation-Sensitive Restriction Enzyme sequencing
    'bisulfite': '"bisulfite seq"', # Bisulfite sequencing
    'mbd': '"mbd seq"', # Methyl-CpG Binding Domain sequencing
    'medip': '"medip seq"', # Methylated DNA Immunoprecipitation sequencing
    # Epigenomic - Chromatin Interaction and Structural Analysis
    'hic': '"hi c"', # Hi-C sequencing for three-dimensional genome structure analysis
    'chiapet': '"chia pet"', # Chromatin Interaction Analysis by Paired-End Tag Sequencing
    'tethered': '"tethered chromatin conformation capture"' # Tethered Chromatin Conformation Capture
}
DIC_SOURCE = {
    'genomic': '"genomic"',
    'genomic_single_cell': '"genomic single cell"',
    'transcriptomic': '"transcriptomic"',
    'transcriptomic_single_cell': '"transcriptomic single cell"',
    'metagenomic': '"metagenomic"',
    'metatranscriptomic': '"metatranscriptomic"',
    'synthetic': '"synthetic"',
    'viral': '"viral rna"',
    'other': '"other"'
}

DIC_ORGANISM = {
    'human': '"homo sapiens"',
    'mouse': '"mus musculus"',
    'dog': '"canis lupus familiaris"',
    'dingo': '"canis lupus dingo"',
    'wolf': '"canis lupus"',
    # Pet animals
    'cat': '"felis catus"',
    # Farm animals
    'pig': '"sus scrofa"',
    'pig_domestic': '"sus scrofa domesticus"',
    'cow': '"bos taurus"',
    'dairy_cow': '"Bos indicus"',
    'chicken': '"gallus gallus"',
    'horse': '"equus caballus"',
    # Farm plants
    'rice': '"oryza sativa"',
    'wheat': '"triticum aestivum"',
    # Peto's paradox (Long-lived & cancer-free)
    'elephant': '"loxodonta africana"', # 아프리카 코끼리
    'whale': '"balaenoptera musculus"', # 흰수염고래
    'naked_mole_rat': '"heterocephalus glaber"',
    'blind_mole_rat': '"spalax ehrenbergi"',
    # Primates
    'gorilla': '"gorilla gorilla"',
    'rhesus_monkey': '"macaca mulatta"', # 리서스 원숭이
    'cynomolgus_monkey': '"macaca fascicularis"', # 시노몰거스 원숭이
    'baboon': '"papio"', # 바부인
    'chimpanzee': '"pan troglodytes"', # 침팬지
    'marmoset': '"callithrix jacchus"',  # 마모셋
    'macaque': '"macaca"',
    'capuchin_monkey': '"cebus capucinus"',  # Used in behavioral studies and neuroscience
    'squirrel_monkey': '"saimiri sciureus"',  # Used in neurobiology, behavioral biology, and pharmacology
    'bonobo': '"pan paniscus"',  # Close relation to chimpanzees, used in behavioral and social studies, genetics
    # Experimental models
    'yeast': '"saccharomyces cerevisiae"',
    'fruit_fly': '"drosophila melanogaster"',
    'nematode': '"caenorhabditis elegans"',
    'zebrafish': '"danio rerio"',
    'african clawed frog': '"xenopus laevis"',
    'rat': '"rattus norvegicus"',
    'guinea pig': '"cavia porcellus"',
    'rabbit': '"oryctolagus cuniculus"',
    # Etc
    'opossum': '"didelphis virginiana"'
}   