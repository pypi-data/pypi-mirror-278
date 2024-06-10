import sys
import os
import io
import gzip
import pandas as pd
import numpy as np 
from pymongo import MongoClient
import re


# local imports 
import annobee.config as config

def err_handler(err):
    """
    Handle exceptions and print detailed error log to the console.

    Parameters
    ----------
    err : Exception
        The exception object.

    Returns
    -------
    None
        This function does not return any value.
    """

    print ("Exception has occured:", err)
    print ("Exception type:", type(err))
    err_type, err_obj, traceback = sys.exc_info()
    if traceback != None:
        line_num = traceback.tb_lineno
        fname = os.path.split(traceback.tb_frame.f_code.co_filename)[1]
        print(f"in {fname}")
    else: line_num = "not found"
    print ("\nERROR:", err, "on line number:", line_num)
    print ("traceback:", traceback, "-- type:", err_type)

def db_connect(dbname):
    """
    Connect to a MongoDB database.

    Parameters
    ----------
    dbname : str
        The name of the database to connect to.

    Returns
    -------
    pymongo.database.Database
        The database object.
    """
    try:
        # Create a MongoClient object, which will connect to the MongoDB server running on localhost by default.
        client = MongoClient()
        db = client[dbname]
        return db
    except Exception as err:
        err_handler(err)

def read_vcf(path):
    """
    Read a VCF (Variant Call Format) file.

    Parameters
    ----------
    path : str
        The file path to the VCF file.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the data read from the VCF file.
    """
    if path[-3:] == ".gz": 
        with io.TextIOWrapper(gzip.open(path,'r')) as f:
            lines = [l for l in f if not l.startswith('##')]
    else:
        with open(path,"r") as f:
            lines = [l for l in f if not l.startswith('##')]
    try:
        return pd.read_csv(
            io.StringIO(''.join(lines)),
            dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
                'QUAL': str, 'FILTER': str, 'INFO': str},
            sep='\t', index_col=False
        ).rename(columns={'#CHROM': 'CHROM'})
    except UnicodeDecodeError:
        return pd.read_csv(
            io.StringIO(''.join(lines)),
            dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
                'QUAL': str, 'FILTER': str, 'INFO': str},
            sep='\t', index_col=False,  encoding = "ISO-8859-1"
        ).rename(columns={'#CHROM': 'CHROM'})
    except Exception as err:
        err_handler(err)

def is_iterable(var):
    """
    Check if a variable is iterable.

    Parameters
    ----------
    var : any
        The variable to check.

    Returns
    -------
    bool
        True if the variable is iterable, False otherwise.
    """
    try:
        iter(var)
        return True
    except TypeError:
        return False

def check_value(val):
    '''
    Check if value field is empty, nan, None, 'nan', 'None', , or an empty string, if not, notes as error

    Parameters
    ----------
    val : any
        The value to check.

    Returns
    -------
    bool
        True if the value is valid, False otherwise.
    '''
    if val == None: 
        return False
    if type(val) == list:
        if len(val) == 0: return False
        elif (len(val) == 1) and((check_value(val[0])==None) or (val[0] == '.')): return False
        else: return True
    if isinstance(val, float) and np.isnan(val):
        return False
    if val != None and val and val != 'nan' and val != 'None': 
        if isinstance(val, str):
            if len(val) == 0: return False
            elif(val == '' or val =='N/A' or val.strip() == "."): return False
            else: return True
        return True

    return False

def save_as_vcf(variant_list, out_path): 
    """
    Save a list of variants as a VCF (Variant Call Format) file.

    Parameters
    ----------
    variant_list : list of dict
        A list of variant dictionaries containing the variant information.
    out_path : str
        The file path to save the VCF file.

    Returns
    -------
    None
        This function does not return any value.
    """
     
    vcf_output = open(out_path, 'w', encoding='utf-8')
    vcf_output.write('##fileformat=VCFv4.3\n')
    vcf_output.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n')  # Header
    
    for variant in variant_list:
        chrom = variant["CHROM"]
        pos = variant["POS"]
        ref = variant["REF"]
        alt = variant["ALT"]
        vcf_output.write(f'{chrom}\t{pos}\t.\t{ref}\t{alt}\t.\t.\t')
        
        for key in variant["INFO"].keys():
            vcf_output.write(f'{key}={variant["INFO"][key]};')
            
        vcf_output.write("\n")

    vcf_output.close()


def sum_of_list(l):
    """
    Calculate the sum of all elements in a list.

    Parameters
    ----------
    l : list
        The list of numbers.

    Returns
    -------
    int
        The sum of all elements in the list.
    """
     
    res = 0
    for elem in l:
        res += elem 
    
    return res 

def read_mim2gene():
    """
    Read mim2gene.txt file downloaded from OMIM into a pandas dataframe 

    Parameters
    ----------

    Returns
    -------
    pd.DataFrame
        Content of the mim2gene.txt file in a pandas dataframe with 5 columns: 
        "mim_number", "mim_entry_type", "ncbi_entrez_gene_id", "hgnc_gene_symbol",
        "ensembl_gene_id"
    """
    with open(config.mim2gene_path,"r") as f:
        lines = [l for l in f if not l.startswith('#')]

    df = pd.read_csv(
            io.StringIO(''.join(lines)),
            names=["mim_number", "mim_entry_type", "ncbi_entrez_gene_id", "hgnc_gene_symbol", "ensembl_gene_id"],
            sep='\t', index_col=False
        )

    return df

def flip_ACGT(acgt):
    nt="";
    if acgt=="A":
        nt="T"
    if acgt=="T":
        nt="A"
    if acgt=="C":
        nt="G"
    if acgt=="G":
        nt="C"
    if acgt=="N":
        nt="N"
    if acgt=="X":
        nt="X"
    return(nt)

def read_BS2_dict():

    BS2_snps_recessive_dict = dict()
    BS2_snps_dominant_dict = dict()

    f = gzip.open(config.hg38_BS2_snps_dict_path, 'rb')

    lines = f.read().decode()

    # Process each line 
    for line2 in lines.split('\n'):
        values = line2.split(' ')
        if len(values[0]) >= 1:

            chr = values[0]
            pos = values[1]
            ref = values[2]
            alt = values[3]
            recessive_flag = values[4]
            dominant_flag = values[5]

            variant_key1 = chr +"_"+ pos +"_"+ pos +"_"+ ref +"_"+ alt

            BS2_snps_recessive_dict[ variant_key1 ] = recessive_flag  # key as snp info 0
            BS2_snps_dominant_dict[ variant_key1 ] = dominant_flag  # key as snp info 1 

            variant_key2 =  chr +"_"+ pos +"_"+ pos + "_" + flip_ACGT(ref)+"_"+ flip_ACGT(alt)

            BS2_snps_recessive_dict[variant_key2] = recessive_flag  # key as snp info
            BS2_snps_dominant_dict[variant_key2] = dominant_flag  # key as snp info

    return BS2_snps_recessive_dict, BS2_snps_dominant_dict

def extract_aa_change(hgvsp):
    """
    Extracts the amino acid change and alternate amino acid from the given HGVSp representation.

    Parameters:
    - hgvsp (str): The HGVSp representation containing the amino acid change.

    Returns:
    - string: A string containing amino acid change. First letter of reference aa, first letter of 
            alternate aa and position. <refA><pos><altA>
             Returns None if no information is found.

    Example:
    >>> hgvsp = "ENSP00000368031.3:p.Arg170Trp"
    >>> parse_hgvsp(hgvsp)
    ('A170T')
    """
    # Define regular expression pattern
    pattern = r"p\.([A-Za-z]+)(\d+)([A-Za-z]+)"

    # Match the pattern
    match = re.search(pattern, hgvsp)

    # Extract amino acid changes
    if match:
        aa_change = match.group(1)[0] + match.group(2) + match.group(3)[0]
        return aa_change
    else:
        return None

def exists(key, dict):
    if key in dict and check_value(dict[key]): return True 
    
    return False