from python_ags4 import AGS4

def extract_ags_cpt_data(filepath):
    """Loads the SCPT data table from ags file

    Parameters
    ----------
    filepath : str
        The location of the .ags file

    Returns
    -------
    dataframe 
        Pandas dataframe. 
    """
    tables, headings = AGS4.AGS4_to_dataframe(filepath)

    return AGS4.convert_to_numeric(tables['SCPT'] )

def extract_ags_location_data(filepath):
    """Loads the LOCA data table from ags file

    Parameters
    ----------
    filepath : str
        The location of the .ags file

    Returns
    -------
    dataframe 
        Pandas dataframe. 
    """
    tables, headings = AGS4.AGS4_to_dataframe(filepath)

    return AGS4.convert_to_numeric(tables['LOCA'])

def extract_ags_scpg_data(filepath):
    """Loads the SCPG data table from ags file

    Parameters
    ----------
    filepath : str
        The location of the .ags file

    Returns
    -------
    dataframe 
        Pandas dataframe. 
    """
    tables, headings = AGS4.AGS4_to_dataframe(filepath)

    return AGS4.convert_to_numeric(tables['SCPG'])