def extract_csv_cpt_data(filepath, text_search):
    """Opens CPT csv files and finds the starting row based on the search word (e.g. 'H [m]')

    Parameters
    ----------
    filepath : str
        Location of .csv file
    text_search : str
        The keyword to find to signal the start of the data to extract

    Returns
    -------
    dataframe
        a dataframe containing all the values extracted from the keyword and beyond

    Examples
    --------
    >>> extract_csv_cpt_data(".\CPT123.csv", 'H [m]')
    """    

    import pandas as pd

    with open(filepath) as file:
        skip = next(filter(
            lambda x: x[1].startswith(text_search),
            enumerate(file)

        ))[0]

    try: 
        df = pd.read_csv(filepath, encoding= 'unicode_escape', skiprows=skip)
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding_errors="ignore", skiprows=skip)
    
    
    return df