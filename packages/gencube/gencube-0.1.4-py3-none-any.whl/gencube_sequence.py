from tabulate import tabulate   # to print table form output

# Custom functions
from .utils import (
    check_now,
    search_assembly, 
    json_to_dataframe,
    check_access_database,
    check_access_full_sequence,
    save_metadata,
    download_sequence,
    )
from .constants import (
    LS_GENCUBE_SEQUENCE_LABEL,
    )

## gencube sequence ------------------------------
def sequence (
    keywords,
    level,
    refseq,
    ucsc,
    latest,
    metadata,
    download,
    recursive,
    ):

    # Check the current time
    now = check_now ()
    
    # Search keywords in NCBI Assembly DB
    ls_search = search_assembly(keywords)

    if ls_search:
        # Convert JSON to DataFrame
        df_genome = json_to_dataframe (ls_search, level, refseq, ucsc, latest)
        
        # Check access to NCBI RefSeq & Ensembl Rapid Release
        df_genome_plus, dic_ensembl_meta = check_access_database (df_genome, mode = 'sequence')
        
        print(tabulate(df_genome_plus[LS_GENCUBE_SEQUENCE_LABEL], headers='keys', tablefmt='grid'))
        print('')
        
        # Check full accessibility
        df_full_sequence = check_access_full_sequence (df_genome_plus, dic_ensembl_meta)
    
        # Save metadata
        if metadata:
            save_metadata(df_genome_plus, 'sequence', keywords, level, now)
        
        # Save sequence files
        if download:
            download_sequence(df_full_sequence, df_genome_plus, dic_ensembl_meta, download, recursive)
            



