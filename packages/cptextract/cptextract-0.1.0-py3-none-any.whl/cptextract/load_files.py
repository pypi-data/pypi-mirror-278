import pathlib
from cptextract.extract.agsfunctions import *
from cptextract.extract.csvfunctions import *
from cptextract.extract.excelfunctions import *
#
class CPT_import:
    """
    A class used to represent a CPT Data extracted

    """
    # class level items
    version = 0.1
    depth_header = ['Test length[1]', 'Test Length (m)', 'Penetration Depth (m)', 'H [m]',  'Depth (m)', 'Depth [m]', 'Depth']
    qc_header = ['qc', 'cone resistance']
    fs_header = ['fs', 'local friction', 'friction resistance']  
    u2_header = ['u2', 'pore pressure', 'u (kPa)', 'u (mpa)']
    all=[]
    #cptdict = {}
    CPT_IDs = []
    # instance level
    def __init__(self, filepath):
        """
        Parameters
        ----------
        filepath : str
            CPT file local path

        New Attributes
        ----------
        file_extension : str
            file extension
        filename : str
            file name
        """        

        self.filepath = filepath
        self.file_extension = get_file_extension(self.filepath)
        self.filename = pathlib.Path(self.filepath).stem 
        self.CPT_ID = get_cptname(self.filename)
        self.engine = "None"


        self.log_msg = ""
        self.error_msg = ""
        self.warning_msg = ""

        self.CPT_IDs.append(self.CPT_ID)
        #Class level actions
        CPT_import.all.append(self)
        #print(f"{self.CPT_ID} added!")

    def add_msg(self, msg, msg_type):
        """save and complied error messages to the class instance

        Parameters
        ----------
        msg : str
            error message
        msg_type : str
            type of message
            -e: error
            -w: warning
        """
        if msg_type == 'e':
            self.error_msg = self.error_msg + msg
        elif msg_type == 'w':
            self.warning_msg = self.warning_msg + msg
        else:
            self.log_msg = self.log_msg + msg
            


    def test_open(self):
        """test opening the files before proceeding with the rest of the extraction procedure
        it assigns the self.engine or error msg if the file type is not supported
        
        New Attributes
        ----------
        engine : str
            the python library or package that can be used to open and access the file
        filename : str
            file name
        """ 

        error_text = f"{self.filename}{self.file_extension} file can't be open"

        if self.file_extension == '.ags':
            from python_ags4 import AGS4
            try: 
                AGS4.AGS4_to_dataframe(self.filepath)
                self.engine = 'AGS4'
            except:
                print(error_text)
                self.add_msg(error_text, 'e')
        
        elif self.file_extension == '.csv':
            import pandas as pd
            try: 
                pd.read_csv(self.filepath, encoding= 'unicode_escape')
                self.engine = 'pandas'
            except UnicodeDecodeError:
                pd.read_csv(self.filepath, encoding_errors="ignore")
                self.engine = 'pandas'
            except:
                try:
                    import pyexcel as pye
                    pye.get_sheet(self.filepath)
                    self.engine = 'pyexcel'
                except:
                    print(error_text)
                    self.add_msg(error_text, 'e')

        elif self.file_extension == '.xls':
            from xlrd import open_workbook, XLRDError
            try:
                open_workbook(self.filepath)
                self.engine = 'xlrd'
            except XLRDError:
                try:
                    import pyexcel as pye
                    pye.get_sheet(self.filepath)
                    self.engine = 'pyexcel'
                except:
                    print(error_text)
                    self.add_msg(error_text, 'e')

        elif self.file_extension == '.xlsx':
            import openpyxl
            try: 
                openpyxl.load_workbook(self.filepath)
                self.engine = 'openpyxl'
            except:
                try:
                    import pyexcel as pye
                    pye.get_sheet(self.filepath)
                    self.engine = 'pyexcel'
                except:
                    print(error_text)
                    self.add_msg(error_text, 'e')

        else:
            #self.engine = 'None'
            text = f"{self.filename}{self.file_extension} File Type not support!; "
            print(text)
            self.add_msg(text, 'e')

        #print(self.engine)

    def extractcptdata(self, depth_guessword):
        """extracts the cpt data based on the depth search string and assigns self.CPT_Data if successful
        if not self.data_found will be False

        Parameters
        ----------
        depth_guessword : list[str]
            a list of keywords to search through
                    
        New Attributes
        ----------
        CPT_Data : data frame
            CPT data table as extracted from the file
        data_found : Boolean 
            True if the depth guessword could find a match; False otherwise
        """        
        # if only one keyword is provided, put it into a list so that indexing works
        if isinstance(depth_guessword, str):
            depth_guessword = [depth_guessword]

        if self.file_extension == '.ags':
            self.CPT_Data = extract_ags_cpt_data(self.filepath)
            self.data_found = True

        elif self.file_extension == '.csv' and self.engine == 'pandas':
            
            for i in range(len(depth_guessword)):
                try:
                    self.CPT_Data = extract_csv_cpt_data(self.filepath, depth_guessword[i])
                except StopIteration: #typical error we get if no match found
                    self.data_found = False         
                else:
                    self.data_found = True
                    self.index_location = 0
                    break

        elif self.file_extension == '.xls' and self.engine == 'xlrd':
            result = ['empty']
            for i in range(len(depth_guessword)):
                try:
                    result = extract_xls_cpt_data(self.filepath, depth_guessword[i])
                    self.CPT_Data = result[0]
                except UnboundLocalError: #typical error we get if no match found
                    self.data_found = False
                else:
                    self.data_found = True
                    self.index_location = result[2]
                    break

        elif self.file_extension == '.xlsx' and self.engine == 'openpyxl':
            result = ['empty']
            for i in range(len(depth_guessword)):
                try:
                    result = extract_xlsx_cpt_data(self.filepath, depth_guessword[i])
                    self.CPT_Data = result[0]
                except UnboundLocalError: #typical error we get if no match found
                    self.data_found = False
                else:
                    self.data_found = True
                    self.index_location = result[2]
                    break
        else: 
            self.data_found = False
            print(f"No interpreter found for {self.CPT_ID}{self.file_extension}")
            pass

        if self.data_found:
            self.add_msg(f"{self.CPT_ID}{self.file_extension} successfully imported.; ", 'l')
        else:
            print(f"{self.CPT_ID}{self.file_extension} data not found")
                 
    def findcptdata(self, qc_guessword, fs_guessword, u2_guessword):
        """finds the index locations for depth, fs, qc and u2 columns and save as a dictionary in self.index_location

        Parameters
        ----------
        qc_guessword : list[str]
            a list of keywords to search through
        fs_guessword : list[str]
            a list of keywords to search through
        u2_guessword : list[str]
            a list of keywords to search through
        New Attributes
        ----------
        index_location : dict
            the index location of depth, qc, fs and u2
        """        
        dict1 = {}
        
        if self.file_extension != '.ags' and self.data_found:
            dict1['depth_index'] = self.index_location
            dict1['qc_index'] = find_header_dataframe(self.CPT_Data, qc_guessword)
            dict1['fs_index'] = find_header_dataframe(self.CPT_Data, fs_guessword)
            dict1['u2_index'] = find_header_dataframe(self.CPT_Data, u2_guessword)

            print(self.CPT_ID)
            print(dict1.values())
            self.index_location = dict1


    def compilecptdata(self):
        """Complies the depth, qc, fs and u2 columns in m and MPa units

        For ags files, this process is straighforward and taken directly from the SCPT GROUP. 

        For non-ags files, the following process to followed:
        [1] first check that the qc, fs and u2 location are known
        [2] scrap each of the qc, fs and u2 columns for any units defined. They are typical found in the header itself of the row below
        [3] use the find_first_num_row function to skip any gaps that may exist between the header and the numeric data. this usually happens when the units are defined in 2nd row
        [4] if the data is as it should be, only numeric data is left. converting the columns to float helps to validate this assumption
        [5] any unit conversion is applied before compiling the CPT data 
        
        New Attributes
        ----------
        depth_series : pandas series
            data contained in the depth column 
        qc_series : pandas series
            data contained in the tip resistance column 
        fs_series : pandas series
            data contained in the friction resistnance column 
        u2_series : pandas series
            data contained in the u2 pore pressure column 
        okay_calc : Boolean
            True indicate the extraction process was executed without critical errors and the extracted attributes can be used. 
        CPT_dataframe : data frame
            trimmed down copy of CPT_DATA containing only the headers and the depth, qc, fs and u2 columns in m and MPa units, respectively
        """        
        self.depth_series = []
        self.qc_series = []
        self.fs_series = []
        self.u2_series = []
        self.okay_calc = False

        #index_dict = self.index_location
        if self.file_extension != '.ags' and self.data_found:
            if 99 in list(self.index_location.values()): # if columns headers cant be found
                self.add_msg(f"{self.CPT_ID}{self.file_extension} could not detect column headers!; ", 'e')
                pass
            else:
                # find units in the tables
                self.qc_units = identify_units(self.CPT_Data.iloc[:,self.index_location['qc_index']])
                self.fs_units = identify_units(self.CPT_Data.iloc[:,self.index_location['fs_index']])
                self.u2_units = identify_units(self.CPT_Data.iloc[:,self.index_location['u2_index']])

                # initialise series with no trimming 
                self.depth_series = self.CPT_Data.iloc[:,self.index_location['depth_index']]
                self.qc_series = self.CPT_Data.iloc[:,self.index_location['qc_index']]
                self.fs_series = self.CPT_Data.iloc[:,self.index_location['fs_index']]
                self.u2_series = self.CPT_Data.iloc[:,self.index_location['u2_index']]

                starting_index = find_first_num_row(self.qc_series)
                try:
                    # remove any text in the top of the data beside the header
                    self.CPT_dataframe = self.CPT_Data.iloc[starting_index:,list(self.index_location.values())].astype('float')
                except ValueError:
                    # make sure all data remaining is numeric only
                    error_text = f"{self.CPT_ID}{self.file_extension} non-numeric data present!; "
                    print(error_text)
                    self.add_msg(error_text, 'e')
                    self.add_msg(f"{self.CPT_ID}{self.file_extension} not extracted!; ", 'l')
                else:
                    # compile trimmed CPT data 
                    self.depth_series = self.CPT_Data.iloc[starting_index:,self.index_location['depth_index']]
                    qc_result = auto_convert(self.CPT_Data.iloc[starting_index:,self.index_location['qc_index']], self.qc_units, 150)
                    self.qc_series = qc_result[0]
                    self.add_msg(qc_result[1], 'w')
                    self.CPT_dataframe.iloc[:, 1] = self.qc_series

                    fs_result = auto_convert(self.CPT_Data.iloc[starting_index:,self.index_location['fs_index']], self.fs_units, 15)
                    self.fs_series = fs_result[0]
                    self.add_msg(fs_result[1], 'w')
                    self.CPT_dataframe.iloc[:, 2] = self.fs_series

                    u2_result = auto_convert(self.CPT_Data.iloc[starting_index:,self.index_location['u2_index']], self.u2_units, 15)
                    self.u2_series = u2_result[0]
                    self.add_msg(u2_result[1], 'w')
                    self.CPT_dataframe.iloc[:, 3] = self.u2_series
                    self.okay_calc = True
                    self.add_msg(f"{self.CPT_ID}{self.file_extension} successfully extracted.; ", 'l')
                
        elif self.file_extension == '.ags' and self.data_found:
                self.depth_series = self.CPT_Data['SCPT_DPTH']
                self.qc_series = self.CPT_Data['SCPT_RES']
                self.fs_series = self.CPT_Data['SCPT_FRES']
                self.u2_series = self.CPT_Data['SCPT_PWP2']
                self.CPT_dataframe = self.CPT_Data.loc[:,['SCPT_DPTH', 'SCPT_RES','SCPT_FRES','SCPT_FRES']]
                self.add_msg(f"{self.CPT_ID}{self.file_extension} successfully extracted.; ", 'l')
                self.okay_calc = True

    def auto_extract(self):
        """does all the CPT extraction steps in one go
        """        
        self.test_open()
        self.extractcptdata(CPT_import.depth_header)
        self.findcptdata(qc_guessword = CPT_import.qc_header, fs_guessword=CPT_import.fs_header, 
                      u2_guessword=CPT_import.u2_header)
        self.compilecptdata()


    
    @classmethod
    def all_from_folder(cls, folderpath, accepted_extensions):
        """class method to import directly from a folder and creates the individual class instances

        Parameters
        ----------
        folderpath : str
            local path to folder
        accepted_extensions : list[str]
            a list of accepted file extensions
        """        
        # PLACEHOLDER for default file extensions

        # PLACEHOLDER file path error handling
        all_paths = get_filepaths(folderpath)

        for filepaths in all_paths:
            if get_file_extension(filepaths) in accepted_extensions:

                CPT_import(filepaths)
                
            else:
                pass

   

    def __repr__(self):
        return f"CPT_import('{self.CPT_ID}', '{self.file_extension}')"


def get_cptname(filename):
    """This function will extract the CPTID from the file names.
    this function takes the last words in the file directory and infers a CPT name
    two types of CPT names can pe present: CPT_XXXX or CPT1234

    Parameters
    ----------
    filename : str
        filepath

    Returns
    -------
    str
        the CPT name
    """
    import os

    try:

        #this is for _ named CPTs
        temp2 = filename.split('_')
        cptname = temp2[0] + '_' + temp2[1]

    except IndexError:

        #this is for non _ named CPTs
        temp2 = filename
        cptname = os.path.splitext(temp2)[0] 

    return cptname


def get_file_extension(filepath):
    """identify the file extensionb

    Parameters
    ----------
    filepath : str
        location of the file

    Returns
    -------
    str
        file extension in lowercase
    """
    import pathlib

    file_extension = pathlib.Path(filepath).suffix
    return file_extension.lower() # always return lowercase letter of file extension


def get_filepaths(directory):
    """ This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up.

    Parameters
    ----------
    directory : atr
        folder path

    Returns
    -------
    list
        a list of filepaths within the directory
    Examples
    --------
    >>> get_filepaths("./data")
    """
    import os
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.
        

def find_header_dataframe(df, headers):
    """finds the index location where the dataframe headers matches the keyword

    Parameters
    ----------
    df : dataframe
        a dataframe containing the raw CPT data
    headers : list[str]
        a list of header possible header labels

    Returns
    -------
    int
        the index location of the matching header
    """
    if isinstance(headers, str):
        headers = [headers]

    df_headers = list(df.columns)
    header_index = 99 #default value if non found
    for x in range(len(df_headers)):
        
        header_text = df_headers[x].lower()

        # find matching headers to keyword
        if bool([ele for ele in headers if(ele.lower() in header_text)]):
            header_index = x # retuns the column index
            break 

    return header_index


def find_first_num_row(input_list, limit=10):
    """ 
    this function checks that only numbers are added to the
    data frame in globaldict. basically helps ignore where the units are defined on the 
    second row
    """
    startrow = 0
    i = 0
    while i < limit:
        checkstartrow = input_list[i]
        try:
            float(checkstartrow)
            startrow = i
            break

        except ValueError:
            i += 1

    if i > 5:
        print(str(i) + " starting row unclear! Please check")

    return startrow


def identify_units(df_series):
    """identify units from the column header and content

    Parameters
    ----------
    df_series : data frame
        pandas series containing the data e.g. qc

    Returns
    -------
    str
        unit of the provided series data in kPa or Mpa. If none provided, listed as Not Defined
    """    
    # make case insensitive
    series_unit = "Not Defined"
    header = df_series.name.lower()
    
    # if header label has kpa
    if 'mpa' in header:
        series_unit = "mpa"
    elif 'kpa' in header:
        series_unit = "kpa"
    else:
        try: #what happens if no units defined anywhere. this:
            if any(df_series.str.contains('mpa', case=False)==True):
                series_unit = "mpa"
            elif any(df_series.str.contains('kpa', case=False)==True):
                series_unit = "kpa"
                #print("Warning 003: " + CPT_id + file_type + '. ' + col_id + '. Program has automatically converted the units from kPa to MPa.')
            else:
                series_unit = "Not Defined"
        except AttributeError:
            series_unit = "Not Defined"

    return series_unit


def auto_convert(df, unit, limit):
    """does the unit conversion from kPa to MPa.
    Also does an second check of the data with respect to max limits in the data. 
    The cone sensors typically have max measurement limits. If the data exceeds this, it is likely 
    that the units were in kPa

    Parameters
    ----------
    df : pandas series
        column data
    unit : str
        current units of the series provided
    limit : float
        CPT cone sensor limit

    Returns
    -------
    list
        a list containing 
        -[0] a dataframe with the units converted 
        -[1] warning message
    """    
    msg = ""
    header = df.name
    # identified units were kpa
    if unit == 'kpa':
        df = df * 0.001

    # sometimes, units are mislabelled. 
    if df.max() > limit and unit == 'mpa':
        df = df * 0.001
        msg = f"{header} units have been mislabelled! Please check!; "  
        #print(header)

    # where it is not defined, infer units from data
    if df.max() > limit and unit == 'Not Defined':
        df = df * 0.001
        msg = f"{header} units inferred as kpa.; " 

    return [df, msg]


def visualise_dict(d,lvl=0):
    """prints the dictionary structure in a table of contents style

    Parameters
    ----------
    d : dict
        The dictionary to analyse
    lvl : int, optional
        level of nesting to view, by default 0
    """
    # go through the dictionary alphabetically 
    for k in sorted(d):

        # print the table header if we're at the beginning
        if lvl == 0 and k == sorted(d)[0]:
            print('{:<25} {:<15} {:<10}'.format('KEY','LEVEL','TYPE'))
            print('-'*79)

        indent = '  '*lvl # indent the table to visualise hierarchy
        t = str(type(d[k]))

        # print details of each entry
        print("{:<25} {:<15} {:<10}".format(indent+str(k),lvl,t))

        # if the entry is a dictionary
        if type(d[k])==dict:
            # visualise THAT dictionary with +1 indent
            visualise_dict(d[k],lvl+1)