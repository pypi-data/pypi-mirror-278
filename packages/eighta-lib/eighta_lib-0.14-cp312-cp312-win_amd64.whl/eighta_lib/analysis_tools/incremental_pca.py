"""
This module provides analytical tools for processing genomic data.

Features include:
- Incremental Principal Component Analysis (IPCA) to handle large datasets efficiently.
- Operations on elements, columns, and rows to facilitate data manipulation and transformations.
- Gene variance analysis tools to measure and interpret variations within gene expression data.

These tools are designed to support bioinformatics analyses and data processing workflows.
"""

import h5py
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import IncrementalPCA
from eighta_lib.slicing import read_process_csc_matrix

# pylint: disable=too-many-arguments
def incremental_pca_h5ad(file_path: str, path_to_item: str, n_components: int, \
                         batch_size: int, store_key: str = None, overwrite: bool = False):
    """
    Perform Incremental Principal Component Analysis (IPCA) on a dataset, represented as a 
    h5py.Group or a h5py.Dataset, stored in an HDF5 file.
    
    - The dataset on which IPCA will be performed on should be present in the X, layers, 
    obsm or varm components of the object.
    - The dataset on which IPCA will be performed on should be represented in csr-format, 
    csc-format, or as an array.

    This function incrementally fits the PCA model and transforms the data in batches, 
    which is especially useful for large datasets that do not fit into memory. 
    The results, including the transformed data, eigenvectors, explained variances, 
    and explained variance ratios, are saved back into the same HDF5 file 
    under specified groups simulating the .h5ad format.

    Args:
        file_path (str): Path to the HDF5 file containing the dataset.
        path_to_item (str): Path to the item in the file on which Incremental 
                            PCA should be performed.
                            For example, to perform IPCA on the X component, 
                            one might specify path_to_item as "/X".
        n_components (int): Number of principal components to retain.
        batch_size (int): Size of each batch used during the IPCA 
                            fitting and transformation steps.
        store_key (str, optional): A custom key under which the PCA results should be stored 
                            within the HDF5 file. If not provided, the function defaults to 
                            using a key derived from the provided path_to_item. 
                            Providing a store_key helps prevent overwriting existing data by 
                            allowing the definition of unique identifiers for the PCA datasets.
        overwrite (bool, optional): Flag to determine if existing PCA data under the same 
                            store_key should be overwritten. If False, the function will 
                            raise a ValueError when attempting to overwrite existing data. 
                            Default is False.

    Returns:
        None: The function modifies the dataset directly within the file, storing PCA components, 
        the explained variances, the explained variance ratios, and transformed data.

    Raises:
        ValueError: If any part of the PCA results to be stored already exists under the same key, 
        to prevent unintentional data overwriting without explicit user action.

    Notes:
        The PCA results are stored in the following components within the HDF5 file:
        - 'obsm': For storing the transformed data.
        - 'varm': For storing the PCA components (eigenvectors).
        - 'uns': For storing the explained variances and explained variance ratios.
    """
    with h5py.File(file_path, 'r+') as f:
        # Use the helper function to validate and retrieve the item
        item, encoding_type, shape = verify_and_get_item(f, path_to_item)

        if batch_size <= 0:
            raise ValueError("Batch size must be larger than 0.")
        if n_components <= 0:
            raise ValueError("Number of components must be larger than 0.")

        if batch_size < n_components:
            raise ValueError(
                "Batch size must be greater than or equal to the "
                "number of components."
            )

        # Check if the number of samples in the last batch is less than the number of components
        if (shape[0] % batch_size) < n_components and (shape[0] % batch_size) != 0:
            raise ValueError(
                "The number of samples in the last batch must be greater than "
                "or equal to the number of components."
                "This condition is violated when the remainder of the "
                "total number of rows divided by the batch size "
                "(number of rows % batch size) is less than the number of components and not zero."
            )

        # Initialize the name_suffix identifier, that will be used to store the PCA data
        if store_key is None:
            # Naming convention correction for consistency
            name_suffix = path_to_item.strip('/')
        else:
            name_suffix = store_key

        if encoding_type == "array":
            perform_incremental_pca_array(f, item, shape, batch_size,
                                          n_components, name_suffix, overwrite)
        elif encoding_type == "csr_matrix":
            perform_incremental_pca_csr_matrix(f, item, shape, batch_size,
                                               n_components, name_suffix, overwrite)
        elif encoding_type == "csc_matrix":
            perform_incremental_pca_csc_matrix(f, item, shape, batch_size,
                                               n_components, name_suffix, overwrite)

# pylint: disable=too-many-arguments
def perform_incremental_pca_csc_matrix(f, item_group, shape, batch_size, \
                                       n_components, name_suffix, overwrite):
    """
    Helper method that performs Incremental Principal Component Analysis (IPCA) on 
    a dataset stored as a CSC matrix in an HDF5 file.

    This function fits an IncrementalPCA model to the data in batches. The results, 
    including the transformed data, eigenvectors, explained variances, 
    and explained variance ratios, are saved back into the HDF5 file.

    Args:
        f (h5py.File): An open HDF5 file with write access.
        item_group (h5py.Group): The HDF5 group containing the CSC matrix components.
        shape (tuple): The shape of the dataset, used to determine batch processing.
        batch_size (int): The size of each batch for fitting and transforming the IPCA.
        n_components (int): The number of principal components to retain.
        name_suffix (str): A suffix appended to the names of PCA datasets to uniquely 
                        identify them within the file.
        overwrite (bool): Flag to control the behavior when datasets with the same name_suffix 
                        already exist. If False, an error is raised to prevent data loss. 
                        If True, existing datasets are overwritten.

    Returns:
        None: The function modifies the dataset directly within the file, 
            storing PCA components, the explained variances, 
            the explained variance ratios, and transformed data.
    """

    # Create an instance of IncrementalPCA
    ipca = IncrementalPCA(n_components=n_components, batch_size=batch_size)

    # Process the dataset in batches for fitting
    for i in range(0, shape[0], batch_size):
        start_row = i
        end_row = min(i + batch_size, shape[0])  # Avoid going out of bounds

        row_indices = np.arange(start_row, end_row)
        col_indices = np.arange(item_group.attrs["shape"][1])

        # Fetch the matrix slice for current batch of rows
        batch_data = read_process_csc_matrix(item_group, row_indices, col_indices)
        ipca.fit(batch_data)

    prepare_and_create_datasets(f, shape, ipca, n_components, name_suffix, overwrite)

    obsm_group = f.require_group('obsm')

    # Process the dataset in batches for transformation
    for i in range(0, shape[0], batch_size):
        start_row = i
        end_row = min(i + batch_size, shape[0])  # Avoid going out of bounds

        row_indices = np.arange(start_row, end_row)
        col_indices = np.arange(item_group.attrs["shape"][1])

        # Fetch the entire matrix slice for current batch of rows for transformation
        batch_data = read_process_csc_matrix(item_group, row_indices,col_indices)
        obsm_group[f'ipca_{name_suffix}'][i:i + end_row - start_row] = ipca.transform(batch_data)


# pylint: disable=too-many-arguments, too-many-locals
def perform_incremental_pca_csr_matrix(f, item_group, shape, batch_size, \
                                       n_components, name_suffix, overwrite):
    """
    Helper method that performs Incremental Principal Component Analysis (IPCA) on 
    a dataset stored as a CSR matrix in an HDF5 file.

    This function fits an IncrementalPCA model to the data in batches. 
    The results, including the transformed data, eigenvectors, 
    explained variances, and explained variance ratios, are saved back into the HDF5 file.

    Args:
        f (h5py.File): An open HDF5 file with write access.
        item_group (h5py.Group): The HDF5 group containing the CSR matrix components.
        shape (tuple): The shape of the dataset, used to determine batch processing.
        batch_size (int): The size of each batch for fitting and transforming the IPCA.
        n_components (int): The number of principal components to retain.
        name_suffix (str): A suffix appended to the names of PCA datasets to uniquely 
                        identify them within the file.
        overwrite (bool): Flag to control the behavior when datasets with the same 
                        name_suffix already exist. If False, an error is raised 
                        to prevent data loss. If True, existing datasets are overwritten.

    Returns:
        None: The function modifies the dataset directly within the file, 
            storing PCA components, the explained variances, 
            the explained variance ratios, and transformed data.
    """
    # item_group corresponds to the HDF5 group containing the csr_matrix components
    data = item_group['data']
    indices = item_group['indices']
    indptr = item_group['indptr']

    # Create an instance of IncrementalPCA
    ipca = IncrementalPCA(n_components=n_components, batch_size=batch_size)

    # Process the dataset in batches for fitting
    for i in range(0, shape[0], batch_size):
        start_row = i
        end_row = min(i + batch_size, shape[0])  # Avoid going out of bounds

        # Extract the relevant slice of the csr_matrix
        batch_data = csr_matrix((data[indptr[start_row]:indptr[end_row]],
                                 indices[indptr[start_row]:indptr[end_row]],
                                 indptr[start_row:end_row + 1] - indptr[start_row]),
                                shape=(end_row - start_row, shape[1]))
        ipca.fit(batch_data)

    prepare_and_create_datasets(f, shape, ipca, n_components, name_suffix, overwrite)

    obsm_group = f.require_group('obsm')

    #  Process the dataset in batches for transformation
    for i in range(0, shape[0], batch_size):
        start_row = i
        end_row = min(i + batch_size, shape[0])  # Avoid going out of bounds

        # Extract the relevant slice of the csr_matrix
        batch_data = csr_matrix((data[indptr[start_row]:indptr[end_row]],
                                 indices[indptr[start_row]:indptr[end_row]],
                                 indptr[start_row:end_row + 1] - indptr[start_row]),
                                shape=(end_row - start_row, shape[1]))

        obsm_group[f'ipca_{name_suffix}'][i:i + end_row - start_row] = ipca.transform(batch_data)


def perform_incremental_pca_array(f, item, shape, batch_size, n_components, name_suffix, overwrite):
    """
    Helper method that performs Incremental Principal Component Analysis (IPCA) 
    on a dataset stored as an array in an HDF5 file.

    This function fits an IncrementalPCA model to the data in batches. 
    The results, including the transformed data, eigenvectors, explained variances, 
    and explained variance ratios, are saved back into the HDF5 file.

    Args:
        f (h5py.File): An open HDF5 file with write access.
        item (h5py.Dataset): The dataset to be processed, retrieved from the HDF5 file.
        shape (tuple): The shape of the dataset, used to determine batch processing.
        batch_size (int): The size of each batch for fitting and transforming the IPCA.
        n_components (int): The number of principal components to retain.
        name_suffix (str): A suffix appended to the names of PCA datasets to 
                        uniquely identify them within the file.
        overwrite (bool): Flag to control the behavior when datasets with the 
                        same name_suffix already exist.
                        If False, an error is raised to prevent data loss. 
                        If True, existing datasets are overwritten.

    Returns:
        None: The function modifies the dataset directly within the file, 
            storing PCA components, the explained variances,
            the explained variance ratios, and transformed data.
    """

    # Create an instance of IncrementalPCA
    ipca = IncrementalPCA(n_components=n_components, batch_size=batch_size)

    # Process the dataset in batches
    for i in range(0, shape[0], batch_size):
        batch_data = item[i:i + batch_size]
        ipca.fit(batch_data) # Update IPCA with this batch

    prepare_and_create_datasets(f, shape, ipca, n_components, name_suffix, overwrite)

    obsm_group = f.require_group('obsm')

    # Process the dataset in batches for transformation
    for i in range(0, shape[0], batch_size):
        batch_data = item[i:i + batch_size]
        transformed_data = ipca.transform(batch_data)  # Transform the current batch
        # Store the transformed data
        obsm_group[f'ipca_{name_suffix}'][i:i + batch_size] = transformed_data


def prepare_and_create_datasets(f, shape, ipca, n_components, name_suffix, overwrite):
    """
    Helper method that prepares and manages datasets within an HDF5 file for 
    storing the results of Incremental PCA.

    This function handles the creation of necessary groups and datasets 
    within the HDF5 file structure, managing overwrite behaviors, and organizing 
    the PCA results under specified keys derived from `name_suffix`.

    Args:
        f (h5py.File): An open HDF5 file with write access.
        shape (ndarray): The shape of the item from the HDF5 file on which IPCA 
                    was performed, used for determiningthe shape of the output datasets.
        ipca (IncrementalPCA): The fitted IncrementalPCA object, from which PCA results 
                        are retrieved such as explained variance, components, and ratio.
        n_components (int): The number of principal components retained in the IPCA.
        name_suffix (str): A suffix appended to the names of PCA datasets to uniquely 
                        identify them within the file.
                        This is critical for avoiding unintentional data overwrites.
        overwrite (bool): Flag to control the behavior when datasets with the 
                        same `name_suffix` already exist.
                        If False, an error is raised to prevent data loss. 
                        If True, existing datasets are overwritten.

    Raises:
        ValueError: If `overwrite` is False and datasets with the 
                    specified `name_suffix` already exist in the file, 
                    indicating a risk of unintentional data overwriting.

    Notes:
        The method organizes the PCA results into different groups within the HDF5 file:
        - 'obsm' for transformed data,
        - 'varm' for PCA components,
        - 'uns' for explained variance and variance ratios.
        
        The method assumes that the necessary groups (`obsm`, `varm`, `uns`) may not exist and uses 
        `require_group` to ensure they are created if absent. It also checks for existing datasets 
        corresponding to the `name_suffix`before proceeding with dataset creation or overwriting, 
        based on the `overwrite` parameter.
    """

    # Prepare groups within the HDF5 file
    # 'require_group' checks if the specified group exists; if not, it creates it.
    obsm_group = f.require_group('obsm')
    varm_group = f.require_group('varm')
    uns_group = f.require_group('uns')

    # If `overwrite` is set to False, check if datasets exist and raise an error if they do.
    if not overwrite:
        if f'ipca_{name_suffix}' in obsm_group or \
        f'ipca_explained_variance_{name_suffix}' in uns_group or \
        f'ipca_explained_variance_ratio_{name_suffix}' in uns_group or \
        f'ipca_components_{name_suffix}' in varm_group:
            raise ValueError(
                f"Data under the key '{name_suffix}' already exists and "
                "cannot be overwritten."
            )

    # If `overwrite` is set to True, delete existing datasets under the `name_suffix` identifier.
    else:
        if f'ipca_{name_suffix}' in obsm_group:
            del obsm_group[f'ipca_{name_suffix}']
        if f'ipca_explained_variance_{name_suffix}' in uns_group:
            del uns_group[f'ipca_explained_variance_{name_suffix}']
        if f'ipca_explained_variance_ratio_{name_suffix}' in uns_group:
            del uns_group[f'ipca_explained_variance_ratio_{name_suffix}']
        if f'ipca_components_{name_suffix}' in varm_group:
            del varm_group[f'ipca_components_{name_suffix}']

    # Create datasets to store incremental transformations
    obsm_group.create_dataset(
        f'ipca_{name_suffix}', shape=(shape[0], n_components), dtype='float32'
    )
    uns_group.create_dataset(
        f'ipca_explained_variance_{name_suffix}', data=ipca.explained_variance_
    )
    uns_group.create_dataset(
        f'ipca_explained_variance_ratio_{name_suffix}', 
        data=ipca.explained_variance_ratio_
    )
    varm_group.create_dataset(
        f'ipca_components_{name_suffix}', data=ipca.components_
    )


def verify_and_get_item(f, path_to_item: str):
    """
    Helper method to verify the existence and type of an item within an HDF5 file, 
    and to return the item along with its encoding type and shape.

    This function checks if the specified path exists in the HDF5 file, 
    validates that the item belongs to an allowed group,
    and ensures it is a recognized dataset or matrix format suitable for IPCA. 
    It also confirms that the data type is numeric.

    Args:
        f (h5py.File): An open HDF5 file with read access.
        path_to_item (str): The path to the item within the HDF5 file.

    Returns:
        item (h5py.Dataset or h5py.Group): The HDF5 item found at the specified path.
        encoding_type (str): The encoding type of the item 
                            ('array', 'csr_matrix', or 'csc_matrix').
        shape (tuple): The shape of the item.

    Raises:
        ValueError: If the specified path does not exist, if the item is not 
                    within an allowed group, if the item is not a suitable 
                    dataset or recognized sparse matrix format,
                    or if the item's data type is not numeric.
                    
    Notes:
        The method only allows items within the groups 'X', 'layers', 'obsm', and 'varm'.
        It supports datasets encoded as arrays and groups encoded as CSR or CSC matrices.
    """

    # Check if the item exists in the file
    if path_to_item not in f:
        raise ValueError(f"The specified path '{path_to_item}' does not exist in the HDF5 file.")

    valid_groups = ['X', 'layers', 'obsm', 'varm']
    # Extract the base group from path_to_item to validate it
    if path_to_item.split('/')[0] == "":
        base_group = path_to_item.split('/')[1]
    else:
        base_group = path_to_item.split('/')[0]

    # Check if the base group is one of the allowed groups
    if base_group not in valid_groups:
        raise ValueError(
            f"Path '{path_to_item}' must be within one of the following groups: "
            f"{', '.join(valid_groups)}."
        )

    item = f[path_to_item]

    # Check if the item is a dataset or a group that can represent a matrix
    # First, Checking for array matrix format
    if isinstance(item, h5py.Dataset) and item.attrs["encoding-type"] == "array":
        encoding_type = item.attrs["encoding-type"]
        data_type = item.dtype
        shape = item.shape

    # Checking for CSR or CSC matrix format
    elif (isinstance(item, h5py.Group) and
        item.attrs["encoding-type"] in ("csr_matrix", "csc_matrix") and
        "data" in item):
        encoding_type = item.attrs["encoding-type"]
        data_type = item['data'].dtype
        shape = item.attrs["shape"]

    else:
        raise ValueError(
            f"The item specified at '{path_to_item}' is neither a suitable dataset "
            f"nor a recognized sparse matrix format."
        )

    # Ensure the data type is numeric
    if not np.issubdtype(data_type, np.number):
        raise ValueError(
            f"The data at '{path_to_item}' is not numeric. "
            f"PCA requires numeric data types."
        )

    return item, encoding_type, shape
