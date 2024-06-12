from tabulate import tabulate   # to print table form output

# Custom functions
from .utils import (
    check_now,
    search_assembly, 
    json_to_dataframe,
    check_access_database,
    check_access_full_crossgenome,
    save_metadata,
    download_crossgenome,
    )
from .constants import (
    LS_GENCUBE_CROSSGENOME_LABEL,
    )

## gencube crossgenome ------------------------------
def crossgenome (
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
    
    # Search for keywords in the NCBI Assembly DB
    ls_search = search_assembly(keywords)

    if ls_search:
        # Convert JSON to DataFrame
        df_genome = json_to_dataframe (ls_search, level, refseq, ucsc, latest)
        
        # Check access to Ensembl Rapid Release & Zoonomia TOGA
        df_genome, dic_ensembl_meta, df_zoonomia = check_access_database (df_genome, mode = 'crossgenome')
        
        print(tabulate(df_genome[LS_GENCUBE_CROSSGENOME_LABEL], headers='keys', tablefmt='grid'))
        print('')
        
        # Check full accessibility
        df_full_crossgenome = check_access_full_crossgenome (df_genome, dic_ensembl_meta, df_zoonomia)
    
        # Save metadata
        if metadata:
            save_metadata(df_genome, 'crossgenome', keywords, level, now)
        
        # Save comparative genomics files
        if download:
            download_crossgenome(df_full_crossgenome, df_genome, dic_ensembl_meta, df_zoonomia, download, recursive)