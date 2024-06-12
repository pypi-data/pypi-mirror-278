

# Custom functions
from .utils import (
    check_now,
    make_query, 
    search_sra, 
    fetch_meta, 
    convert_format,
    save_seq_metadata
    )

## gencube seqmeta ---------------------------------
def seqmeta(
    keywords,
    info,
    organism, 
    strategy, 
    source, 
    layout, 
    exclude, 
    metadata,
    ):
    # Print information of organism, strategy, source
    if info:
        print('info')
        
    else:
        # Check the current time
        now = check_now()
        
        # Input query
        query, out_file_name = make_query(organism, strategy, source, layout, keywords, exclude, now)

        # Search query in the SRA database
        search_ids = search_sra(query)['IdList']

        # Fetch metadata, re-format, and save study- and sample-level tables
        if metadata:
            out_fetch = fetch_meta(search_ids)
            df_study, df_sample = convert_format(out_fetch, query)
            save_seq_metadata(df_study, df_sample, out_file_name)
        else:
            print('  If you want to save the metadata of the searched datasets, please use the -m or --metadata option. \n')


