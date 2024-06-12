import argparse

# Sub-modules
from .__init__ import __version__
from .gencube_genome import genome
from .gencube_geneset import geneset
from .gencube_sequence import sequence
from .gencube_annotation import annotation
from .gencube_crossgenome import crossgenome
from .gencube_seqmeta import seqmeta

# Custom functions
from .utils import (
    join_variables_with_newlines,
    )
# Constant variables
from .constants import (
    DIC_ORGANISM, 
    DIC_STRATEGY, 
    DIC_SOURCE
    )

def main():
    # Define parent parser
    parser = argparse.ArgumentParser(
        prog='gencube', description=f"gencube v{__version__}"
        )
    # Initiate subparsers
    subparsers = parser.add_subparsers(
        dest='command'
        )

    ## ---------------------------------------------
    ## gencube genome
    ## ---------------------------------------------
    # gencube genome subparser
    genome_desc = 'Search, download, and modify chromosome labels for genomes'
    parser_genome = subparsers.add_parser(
        'genome', description=genome_desc, help=genome_desc, add_help=True, 
        formatter_class=argparse.RawTextHelpFormatter
        )
    # gencube genome arguments
    parser_genome.add_argument(
        'keywords',
        nargs='*',
        help=(
            'Taxonomic names to search for genomes. You can provide various forms \n'
            'such as species names or accession numbers.  \n'
            "Examples: 'homo sapiens', human, GCF_000001405.40, GCA_000001405.29, GRCh38, hg38 \n"
            '\n'
            'Multiple names can be combined and will be merged in the search results.\n'
            'To specify multiple names, separate them with spaces.'
            )
        )
    parser_genome.add_argument(
        '-v', '--level',
        metavar='level',
        default='complete,chromosome',
        required=False,
        help=(
            'Specify the genome assembly level (default: complete,chromosome)\n'
            'complete   : Fully assembled genomes\n'
            'chromosome : Assembled at the chromosome level\n'
            'scaffold   : Assembled into scaffolds, but not to the chromosome level\n'
            'contig     : Contiguous sequences without gaps\n'
            '\n'
            )
        )
    parser_genome.add_argument(
        '-r', '--refseq', 
        action='store_true', 
        required=False,
        help='Show genomes that have RefSeq accession (GCF_* format).'
        )
    parser_genome.add_argument(
        '-u', '--ucsc', 
        action='store_true', 
        required=False,
        help='Show genomes that have UCSC names'
        )
    parser_genome.add_argument(
        '-l', '--latest', 
        action='store_true', 
        required=False,
        help='Show the latest version of the genomes.'
        )
    parser_genome.add_argument(
        '-m', '--metadata',
        action='store_true', 
        required=False,
        help='Save metadata for the searched genomes.'
        )
    parser_genome.add_argument(
        '-d', '--download',
        action='store_true', 
        required=False,
        help='Download "fasta" formatted genome file.'
        )
    parser_genome.add_argument(
        '-f', '--fasta',
        metavar='types',
        default='refseq',
        required=False,
        help=(
            'Type of "fasta" formatted genome file (default: refseq).\n'
            'Default is from the RefSeq database.\n'
            'If not available, download from the GenBank database.\n'
            'genbank    : soft-masked genome by NCBI GenBank\n'
            'refseq     : soft-masked genome by NCBI RefSeq\n'
            'genark     : soft-masked genome by UCSC GenArk\n'
            'ensembl    : soft-masked genome by Ensembl\n'
            'ensembl_hm : hard-masked genome by Ensembl\n'
            'ensembl_um : unmasked genome by Ensembl\n'
            )
        )
    parser_genome.add_argument(
        '-c','--chr_style',
        metavar='type', 
        default='ensembl', 
        choices=['ensembl', 'gencode', 'ucsc', 'raw'],
        required=False,
        help=(
            'Chromosome label style used in the download file (default: ensembl)\n'
            'ensembl : 1, 2, X, MT. Unknowns use GenBank IDs.\n'
            'gencode : chr1, chr2, chrX, chrM. Unknowns use GenBank IDs.\n'
            'ucsc    : chr1, chr2, chrX, chrM. Uses UCSC-specific IDs for unknowns.\n'
            '          (!! Limited use if UCSC IDs are not issued.)\n'
            'raw     : Uses raw file labels without modification. Format depends on the database:\n'
            '         - NCBI GenBank: CM_* or other-form IDs\n'
            '         - NCBI RefSeq : NC_*, NW_* or other-form IDs\n'
            '         - GenArk      : GenBank or RefSeq IDs\n'
            '         - Ensembl     : Ensembl IDs\n'
            )
        )
    parser_genome.add_argument(
        '-p','--compresslevel',
        metavar='1-9', 
        default='6', 
        choices=['1', '2', '3', '4', '5', '6', '7', '8', '9'],
        required=False,
        help=(
            'Compression level for output data (default: 6).\n'
            'Lower numbers are faster but have lower compression.'
            )
        )
    parser_genome.add_argument(
        '--recursive',
        action='store_true', 
        required=False,
        help='Download file regardless of their presence only if integrity check is not possible.'
        )

    ## ---------------------------------------------
    ## gencube geneset
    ## ---------------------------------------------
    # gencube geneset subparser
    geneset_desc = 'Search, download, and modify chromosome labels for genesets (gene annotations)'
    parser_geneset = subparsers.add_parser(
        'geneset', description=geneset_desc, help=geneset_desc, add_help=True, 
        formatter_class=argparse.RawTextHelpFormatter
        )
    # gencube geneset arguments
    parser_geneset.add_argument(
        'keywords',
        nargs='*',
        help=(
            'Taxonomic names to search for genomes. You can provide various forms \n'
            'such as species names or accession numbers.  \n'
            'Examples: homo_sapiens, human, GCF_000001405.40, GCA_000001405.29, GRCh38, hg38 \n'
            '\n'
            'Multiple names can be combined and will be merged in the search results.\n'
            'To specify multiple names, separate them with spaces.'
            )
        )
    parser_geneset.add_argument(
        '-v', '--level',
        metavar='level',
        default='complete,chromosome',
        required=False,
        help=(
            'Specify the genome assembly level (default: complete,chromosome)\n'
            'complete   : Fully assembled genomes\n'
            'chromosome : Assembled at the chromosome level\n'
            'scaffold   : Assembled into scaffolds, but not to the chromosome level\n'
            'contig     : Contiguous sequences without gaps\n'
            '\n'
            )
        )
    parser_geneset.add_argument(
        '-r', '--refseq', 
        action='store_true', 
        required=False,
        help='Show genomes that have RefSeq accession (GCF_* format).'
        )
    parser_geneset.add_argument(
        '-u', '--ucsc', 
        action='store_true', 
        required=False,
        help='Show genomes that have UCSC names'
        )
    parser_geneset.add_argument(
        '-l', '--latest', 
        action='store_true', 
        required=False,
        help='Show the latest version of the genomes.'
        )
    parser_geneset.add_argument(
        '-m', '--metadata',
        action='store_true', 
        required=False,
        help='Save metadata for the searched genomes.'
        )
    parser_geneset.add_argument(
        '-d', '--download',
        metavar='types',
        required=False,
        help=(
            'Type of gene set\n'
            'refseq_gtf    : RefSeq gene set (GTF format)\n'
            'refseq_gff    : RefSeq gene set (GFF)\n'
            'gnomon        : RefSeq Gnomon gene prediction (GFF)\n'
            'cross         : RefSeq Cross-species alignments (GFF)\n'
            'same          : RefSeq Same-species alignments (GFF)\n'
            'agustus       : GenArk Augustus gene prediction (GFF)\n'
            'xenoref       : GenArk XenoRefGene (GFF)\n'
            'genark_ref    : GenArk RefSeq gene models (GFF)\n'
            'genark_toga   : ??????????'
            'ensembl_gtf   : Ensembl gene set (GTF)\n'
            'ensembl_gff   : Ensembl gene set (GFF)\n'
            'toga_gtf      : Zoonomia TOGA gene set (GTF)\n'
            'toga_bed      : Zoonomia TOGA gene set (BED)\n'
            'toga_pseudo   : Zoonomia TOGA processed pseudogenes (BED)\n'
            )
        )
    parser_geneset.add_argument(
        '-c','--chr_style',
        metavar='type', 
        default='ensembl', 
        choices=['ensembl', 'gencode', 'ucsc', 'raw'],
        required=False,
        help=(
            'Chromosome label style used in the download file (default: ensembl)\n'
            'ensembl : 1, 2, X, MT. Unknowns use GenBank IDs.\n'
            'gencode : chr1, chr2, chrX, chrM. Unknowns use GenBank IDs.\n'
            'ucsc    : chr1, chr2, chrX, chrM. Uses UCSC-specific IDs for unknowns.\n'
            '          (!! Limited use if UCSC IDs are not issued.)\n'
            'raw     : Uses raw file labels without modification. Format depends on the database:\n'
            '         - NCBI GenBank: CM_* or other-form IDs\n'
            '         - NCBI RefSeq : NC_*, NW_* or other-form IDs\n'
            '         - GenArk      : GenBank or RefSeq IDs\n'
            '         - Ensembl     : Ensembl IDs\n'
            )
        )
    parser_geneset.add_argument(
        '--recursive',
        action='store_true', 
        required=False,
        help='Download files regardless of their presence only if integrity check is not possible.'
        )
    
    ## ---------------------------------------------
    ## gencube sequence
    ## ---------------------------------------------
    # gencube sequence subparser
    sequence_desc = 'Search and download sequence data'
    parser_sequence = subparsers.add_parser(
        'sequence', description=sequence_desc, help=sequence_desc, add_help=True, 
        formatter_class=argparse.RawTextHelpFormatter
        )
    # gencube sequence arguments
    parser_sequence.add_argument(
        'keywords',
        nargs='*',
        help=(
            'Taxonomic names to search for genomes. You can provide various forms \n'
            'such as species names or accession numbers.  \n'
            'Examples: homo_sapiens, human, GCF_000001405.40, GCA_000001405.29, GRCh38, hg38 \n'
            '\n'
            'Multiple names can be combined and will be merged in the search results.\n'
            'To specify multiple names, separate them with spaces.'
            )
        )
    parser_sequence.add_argument(
        '-v', '--level',
        metavar='level',
        default='complete,chromosome',
        required=False,
        help=(
            'Specify the genome assembly level (default: complete,chromosome)\n'
            'complete   : Fully assembled genomes\n'
            'chromosome : Assembled at the chromosome level\n'
            'scaffold   : Assembled into scaffolds, but not to the chromosome level\n'
            'contig     : Contiguous sequences without gaps\n'
            '\n'
            )
        )
    parser_sequence.add_argument(
        '-r', '--refseq', 
        action='store_true', 
        required=False,
        help='Show genomes that have RefSeq accession (GCF_* format).'
        )
    parser_sequence.add_argument(
        '-u', '--ucsc', 
        action='store_true', 
        required=False,
        help='Show genomes that have UCSC names'
        )
    parser_sequence.add_argument(
        '-l', '--latest', 
        action='store_true', 
        required=False,
        help='Show the latest version of the genomes.'
        )
    parser_sequence.add_argument(
        '-m', '--metadata',
        action='store_true', 
        required=False,
        help='Save metadata for the searched genomes.'
        )
    parser_sequence.add_argument(
        '-d', '--download',
        metavar='types',
        required=False,
        help=(
            'Download "fasta" formatted sequence file. \n'
            '1. Nucleotide sequences:\n'
            '   refseq_rna              : Accessioned RNA sequences annotated on the genome assembly.\n'
            '   refseq_rna_from_genomic : RNA features based on the genome sequence.\n'
            '   refseq_cds_from_genomic : CDS features based on the genome sequence.\n'
            '   refseq_pseudo           : Pseudogene and other gene regions without transcribed RNA or translated protein products.\n'
            '   ensembl_cdna            : Ensembl cDNA sequences of transcripts.\n'
            '   ensembl_cds             : Ensembl coding sequences (CDS).\n'
            '   ensembl_repeat          : Ensembl repeat modeler sequences.\n'
            '\n'
            '2. Protein sequences:\n'
            '   refseq_pep              : Accessioned protein sequences annotated on the genome assembly.\n'
            '   refseq_pep_cds          : CDS features translated into protein sequences.\n'
            '   ensembl_pep             : Ensembl protein sequences.\n'
            )
        )
    parser_sequence.add_argument(
        '--recursive',
        action='store_true', 
        required=False,
        help='Download files regardless of their presence only if integrity check is not possible.'
        )
    
    ## ---------------------------------------------
    ## gencube annotation
    ## ---------------------------------------------
    # gencube annotation subparser
    annotation_desc = 'Search and download various genome annotations, such as gaps and repeats'
    parser_annotation = subparsers.add_parser(
        'annotation', description=annotation_desc, help=annotation_desc, add_help=True, 
        formatter_class=argparse.RawTextHelpFormatter
        )
    # gencube annotation arguments
    parser_annotation.add_argument(
        'keywords',
        nargs='*',
        help=(
            'Taxonomic names to search for genomes. You can provide various forms \n'
            'such as species names or accession numbers.  \n'
            'Examples: homo_sapiens, human, GCF_000001405.40, GCA_000001405.29, GRCh38, hg38 \n'
            '\n'
            'Multiple names can be combined and will be merged in the search results.\n'
            'To specify multiple names, separate them with spaces.'
            )
        )
    parser_annotation.add_argument(
        '-v', '--level',
        metavar='level',
        default='complete,chromosome',
        required=False,
        help=(
            'Specify the genome assembly level (default: complete,chromosome)\n'
            'complete   : Fully assembled genomes\n'
            'chromosome : Assembled at the chromosome level\n'
            'scaffold   : Assembled into scaffolds, but not to the chromosome level\n'
            'contig     : Contiguous sequences without gaps\n'
            '\n'
            )
        )
    parser_annotation.add_argument(
        '-r', '--refseq', 
        action='store_true', 
        required=False,
        help='Show genomes that have RefSeq accession (GCF_* format).'
        )
    parser_annotation.add_argument(
        '-u', '--ucsc', 
        action='store_true', 
        required=False,
        help='Show genomes that have UCSC names'
        )
    parser_annotation.add_argument(
        '-l', '--latest', 
        action='store_true', 
        required=False,
        help='Show the latest version of the genomes.'
        )
    parser_annotation.add_argument(
        '-m', '--metadata',
        action='store_true', 
        required=False,
        help='Save metadata for the searched genomes.'
        )
    parser_annotation.add_argument(
        '-d', '--download',
        metavar='types',
        required=False,
        help=(
            'Download annotation file.\n'
            'gaps          : Genomic gaps (GenBank)\n'
            'ontology      : Functional annotations (RefSeq)\n'
            'repeatmasker  : Repeated elements annotated by RepeatMasker (RefSeq or GenArk)\n'
            'repeatmodeler : Repeated elements annotated by RepeatModeler (GenArk)\n'
            
            'gc :  (GenArk)\n'
            'sr'
            'td'
            'wm'
            'gaps'
            'rmsk'
            'cpg'
            )
        )
    parser_annotation.add_argument(
        '-c','--chr_style',
        metavar='type', 
        default='ensembl', 
        choices=['ensembl', 'gencode', 'ucsc', 'raw'],
        required=False,
        help=(
            'Chromosome label style used in the download file (default: ensembl)\n'
            'ensembl : 1, 2, X, MT. Unknowns use GenBank IDs.\n'
            'gencode : chr1, chr2, chrX, chrM. Unknowns use GenBank IDs.\n'
            'ucsc    : chr1, chr2, chrX, chrM. Uses UCSC-specific IDs for unknowns.\n'
            '          (!! Limited use if UCSC IDs are not issued.)\n'
            'raw     : Uses raw file labels without modification. Format depends on the database:\n'
            '         - NCBI GenBank: CM_* or other-form IDs\n'
            '         - NCBI RefSeq : NC_*, NW_* or other-form IDs\n'
            '         - GenArk      : GenBank or RefSeq IDs\n'
            '         - Ensembl     : Ensembl IDs\n'
            )
        )
    parser_annotation.add_argument(
        '--recursive',
        action='store_true', 
        required=False,
        help='Download files regardless of their presence only if integrity check is not possible.'
        )
    
    ## ---------------------------------------------
    ## gencube crossgenome
    ## ---------------------------------------------
    # gencube crossgenome subparser
    crossgenome_desc = 'Search and download comparative genomics data, such as homology, alignments, and orthologs'
    parser_crossgenome = subparsers.add_parser(
        'crossgenome', description=crossgenome_desc, help=crossgenome_desc, add_help=True, 
        formatter_class=argparse.RawTextHelpFormatter
        )
    # gencube geneset arguments
    parser_crossgenome.add_argument(
        'keywords',
        nargs='*',
        help=(
            'Taxonomic names to search for genomes. You can provide various forms \n'
            'such as species names or accession numbers.  \n'
            'Examples: homo_sapiens, human, GCF_000001405.40, GCA_000001405.29, GRCh38, hg38 \n'
            '\n'
            'Multiple names can be combined and will be merged in the search results.\n'
            'To specify multiple names, separate them with spaces.'
            )
        )
    parser_crossgenome.add_argument(
        '-v', '--level',
        metavar='level',
        default='complete,chromosome',
        required=False,
        help=(
            'Specify the genome assembly level (default: complete,chromosome)\n'
            'complete   : Fully assembled genomes\n'
            'chromosome : Assembled at the chromosome level\n'
            'scaffold   : Assembled into scaffolds, but not to the chromosome level\n'
            'contig     : Contiguous sequences without gaps\n'
            '\n'
            )
        )
    parser_crossgenome.add_argument(
        '-r', '--refseq', 
        action='store_true', 
        required=False,
        help='Show genomes that have RefSeq accession (GCF_* format).'
        )
    parser_crossgenome.add_argument(
        '-u', '--ucsc', 
        action='store_true', 
        required=False,
        help='Show genomes that have UCSC names'
        )
    parser_crossgenome.add_argument(
        '-l', '--latest', 
        action='store_true', 
        required=False,
        help='Show the latest version of the genomes.'
        )
    parser_crossgenome.add_argument(
        '-m', '--metadata',
        action='store_true', 
        required=False,
        help='Save metadata for the searched genomes.'
        )
    parser_crossgenome.add_argument(
        '-d', '--download',
        metavar='types',
        required=False,
        help=(
            'ensembl_homology   : Homology data from Ensembl, detailing gene orthology relationships across species.\n'
            'toga_homology      : Homology data from TOGA, providing predictions of orthologous genes based on genome alignments.\n'
            'toga_align_codon   : Codon alignment data from TOGA, showing aligned codon sequences between reference and query species.\n'
            'toga_align_protein : Protein alignment data from TOGA, detailing aligned protein sequences between reference and query species.\n'
            'toga_inact_mut     : List of inactivating mutations from TOGA, identifying mutations that disrupt gene function.\n'
            )
        )
    parser_crossgenome.add_argument(
        '--recursive',
        action='store_true', 
        required=False,
        help='Download files regardless of their presence only if integrity check is not possible.'
        )
    
    ## ---------------------------------------------
    ## gencube seqmeta
    ## ---------------------------------------------
    # gencube seqmeta subparser
    seq_desc = 'Search and fetch metadata of experimental seqeuncing data'
    parser_seqmeta = subparsers.add_parser(
        'seqmeta', description=seq_desc, help=seq_desc, add_help=True,
        formatter_class=argparse.RawTextHelpFormatter
        )
    parser_seqmeta.add_argument(
        'keywords',
        nargs='*',
        help=(
            'Keywords to search for sequenceing-based experimental data. You can provide various forms \n'
            'Examples: tissue name, cell line, disease name, etc \n'
            '          liver, k562, cancer, breast_cancer'
            '\n'
            'Multiple keywords can be combined and will be merged in the search results.\n'
            'To specify multiple names, separate them with spaces.'
            'Logical operator of each keyword can be defined using -p option.'
            )
        )
    # gencube seqmeta arguments
    parser_seqmeta.add_argument(
        '--info', 
        action='store_true', 
        help='Show full information about organism, strategy, source and layout \n '
        )
    parser_seqmeta.add_argument(
        '-o', '--organism',
        metavar='string', 
        default='',
        help=(
            'Scientific name or common name \n' +
            'Example: homo_sapiens or human \n\n'
            'Available common names:\n' +
            join_variables_with_newlines(list(DIC_ORGANISM.keys())) +
            '\n '
            )
        )
    parser_seqmeta.add_argument(
        '-st', '--strategy',
        metavar='string', 
        default='',
        help=(
            'Available strategies \n' +
            join_variables_with_newlines(list(DIC_STRATEGY.keys())) +
            '\n '
            )
        )
    parser_seqmeta.add_argument(
        '-sr', '--source',
        metavar='string', 
        default='',
        help=(
            'Available sources \n' +
            join_variables_with_newlines(list(DIC_SOURCE.keys())) +
            '\n '
            )
        )
    parser_seqmeta.add_argument(
        '-l', '--layout',
        metavar='string', 
        default='', 
        help=(
            'Available layout: paired, single (default: paired, single) \n '
            )
        )
    parser_seqmeta.add_argument(
        '-ex', '--exclude',
        metavar='keywords', 
        default='', 
        help=(
            'Exclude the results for the keywords used in this option  \n '
            )
        )
    parser_seqmeta.add_argument(
        '-m', 
        '--metadata', 
        action='store_true', 
        help='Save integrated metadata \n '
        )
    
    ## Define return values
    args = parser.parse_args()

    # Gencube genome
    if args.command == 'genome':
        if not args.keywords:
            parser_genome.print_help()
        else:
            genome(
                keywords=args.keywords, 
                level=args.level, 
                refseq=args.refseq, 
                ucsc=args.ucsc, 
                latest=args.latest, 
                metadata=args.metadata,
                download=args.download,
                fasta=args.fasta,
                chr_style=args.chr_style,
                compresslevel=args.compresslevel,
                recursive=args.recursive,
                )
    # Gencube geneset
    elif args.command == 'geneset':
        if not args.keywords:
            parser_geneset.print_help()
        else:
            geneset(
                keywords=args.keywords, 
                level=args.level, 
                refseq=args.refseq, 
                ucsc=args.ucsc, 
                latest=args.latest,
                metadata=args.metadata,
                download=args.download,
                chr_style=args.chr_style,
                recursive=args.recursive,
                )
    # Gencube sequence
    elif args.command == 'sequence':
        if not args.keywords:
            parser_sequence.print_help()
        else:
            sequence(
                keywords=args.keywords, 
                level=args.level, 
                refseq=args.refseq, 
                ucsc=args.ucsc, 
                latest=args.latest,
                metadata=args.metadata,
                download=args.download,
                recursive=args.recursive,
                )
    # Gencube annotation
    elif args.command == 'annotation':
        if not args.keywords:
            parser_annotation.print_help()
        else:
            annotation(
                keywords=args.keywords, 
                level=args.level, 
                refseq=args.refseq, 
                ucsc=args.ucsc, 
                latest=args.latest,
                metadata=args.metadata,
                download=args.download,
                chr_style=args.chr_style,
                recursive=args.recursive,
                )
    # Gencube crossgenome
    elif args.command == 'crossgenome':
        if not args.keywords:
            parser_crossgenome.print_help()
        else:
            crossgenome(
                keywords=args.keywords, 
                level=args.level, 
                refseq=args.refseq, 
                ucsc=args.ucsc, 
                latest=args.latest,
                metadata=args.metadata,
                download=args.download,
                recursive=args.recursive,
                )
    # Gencube seqmeta
    elif args.command == 'seqmeta':
        if not args.keywords and not args.organism and not args.strategy and not args.source and not args.layout and not args.exclude:
            parser_seqmeta.print_help()
        else:
            seqmeta(
                keywords=args.keywords, 
                info=args.info,
                organism=args.organism, 
                strategy=args.strategy, 
                source=args.source, 
                layout=args.layout, 
                exclude=args.exclude, 
                metadata=args.metadata,
        )
    else:
        parser.print_help()
