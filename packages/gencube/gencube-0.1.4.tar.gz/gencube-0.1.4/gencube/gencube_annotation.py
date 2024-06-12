from tabulate import tabulate   # to print table form output

# Custom functions
from .utils import (
    check_now,
    search_assembly, 
    json_to_dataframe,
    check_access_database,
    check_access_full_annotation,
    save_metadata,
    download_annotation,
    convert_chr_label_annotation,
    )
from .constants import (
    LS_GENCUBE_ANNOTATION_LABEL,
    )

## gencube annotation ------------------------------
def annotation (
    keywords,
    level,
    refseq,
    ucsc,
    latest,
    metadata,
    download,
    chr_style,
    recursive,
    ):

    # Check the current time
    now = check_now ()
    
    # Search for keywords in the NCBI Assembly DB
    ls_search = search_assembly(keywords)

    if ls_search:
        # Convert JSON to DataFrame
        df_genome = json_to_dataframe (ls_search, level, refseq, ucsc, latest)
        
        # Check_access to NCBI (Genbank & RefSeq) & Ensembl Rapid Release
        df_genome_plus, dic_genark_meta = check_access_database (df_genome, mode = 'annotation')
        
        print(tabulate(df_genome_plus[LS_GENCUBE_ANNOTATION_LABEL], headers='keys', tablefmt='grid'))
        print('')
        
        # Check full accessibility
        df_full_annotation = check_access_full_annotation (df_genome_plus, dic_genark_meta)
    
        # Save metadata
        if metadata:
            save_metadata(df_genome_plus, 'annotation', keywords, level, now)
        
        # Save annotation files
        if download:
            dic_download = download_annotation(df_full_annotation, df_genome_plus, dic_genark_meta, download, recursive)
            # Change chromosome label style
            convert_chr_label_annotation (df_genome_plus, dic_download, chr_style)



