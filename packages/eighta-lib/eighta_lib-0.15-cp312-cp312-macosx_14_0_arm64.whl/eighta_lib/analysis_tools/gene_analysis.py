import h5py
import math
import numpy as np
from multiprocessing import Pool
from eighta_lib import file_management
from tqdm import tqdm

def compute_var_csr_test(file_path):
    with h5py.File(file_path) as file:
        n_col = file['var']['_index'].size
        n_row = file['obs']['_index'].size
        vars = np.zeros(n_col)
        for i in tqdm(range(n_col)):
            col = file['X']['data'][file['X']['indices'][:] == i]
            mean = np.sum(col)/n_row
            sum = np.sum((col - mean)**2)
            sum += (n_row - len(col)) * mean**2
            vars[i] = sum/n_row
        return vars

def compute_var_csc(file_path):
    with h5py.File(file_path) as file:
        n_col = file['var']['_index'].size
        n_row = file['obs']['_index'].size
        vars = np.zeros(n_col)
        for i in tqdm(range(1, n_col+1)):
            col = file['X']['data'][file['X']['indptr'][i-1] : file['X']['indptr'][i]]
            mean = np.sum(col)/n_row
            sum = np.sum((col - mean)**2)
            sum += (n_row - len(col)) * mean**2
            vars[i-1] = sum/n_row
        return vars
    
def compute_var_array(file_path):
    with h5py.File(file_path) as file:
        n_col = file['var']['_index'].size
        n_row = file['obs']['_index'].size
        vars = np.zeros(n_col)
        for i in tqdm(range(n_col)):
            col = file['X'][:,i]
            mean = np.sum(col)/n_row
            sum = np.sum((col - mean)**2)
            vars[i] = sum/n_row
        return vars
    
def gene_variance(file_path: str, destination_key: str = "variance"):
    """
    Compute the variance of all genes in X and store in var.
    
    Parameters:
    - file_path (str): The path to the HDF5 file.
    - n_batch (str): The number of batches to run in parallel for csr matrix. Default is 1 (not using parallel).
    - destination_key (str): The key of the column where the variances will be stored in var. Default is "variance".

    Returns:
    - numpy.ndarray: An array of the computed variances
    """
    with h5py.File(file_path) as f:
        encoding_type = f['X'].attrs.get("encoding-type")
    if encoding_type == "csr_matrix":            
        col_vars = compute_var_csr_test(file_path)
    elif encoding_type == "csc_matrix":
        col_vars = compute_var_csc(file_path)
    elif encoding_type == "array":
        col_vars = compute_var_array(file_path)
    else:
        raise TypeError(f"Encoding type of X {encoding_type} is not supported.")
    file_management.update_h5ad(file_path, f"var/{destination_key}", col_vars)
    return col_vars

def top_n_variance(file_path: str, n: int, variance_key_in_var: str = None):
    """
    Find the indexs of genes with the top n variance.
    
    Parameters:
    - file_path (str): The path to the HDF5 file.
    - n (int): Number of genes to find.
    - variance_key_in_var (str): The key of the column where the variances are stored in var. 
            Default is None, meaning that the variances will be computed and stored in "var/variance".

    Returns:
    - numpy.ndarray: An array of the indexs of genes with the top n variance.
    """
    if variance_key_in_var == None:
        vars = gene_variance(file_path)
    else:
        with h5py.File(file_path) as file:
            vars = file['var'][variance_key_in_var][:]
    return np.argpartition(vars, -n)[-n:]
    

def create_mask_top_n_variance(file_path: str, n: int, variance_key_in_var: str = None, destination_key: str = "var_mask"):
    """
    Create a mask of X where only the columns repersenting the genes with top n variance is marked as true, and store it in layers.
    
    Parameters:
    - file_path (str): The path to the HDF5 file.
    - n (int): Number of genes to find.
    - variance_key_in_var (str): The key of the column where the variances are stored in var. 
            Default is None, meaning that the variances will be computed and stored in "var/variance".
    - destination_key (str): The key where the variances will be stored in layers. Default is "var_mask".
    """
    top_n_index = top_n_variance(file_path, n, variance_key_in_var)
    with h5py.File(file_path) as file:
        n_col = file['var']['_index'].size
        n_row = file['obs']['_index'].size
        mask = np.full(n_col, False)
        mask[top_n_index] = True
        mask = np.vstack((mask, )*n_row)
    file_management.update_h5ad(file_path, f"layers/{destination_key}", mask)



