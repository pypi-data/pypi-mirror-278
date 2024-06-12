import h5py
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix
import psutil
import anndata as ad
import slicers


def explore_hdf5_file(file_path):
    """
    Recursively explores and prints the structure of an HDF5 file.

    Parameters:
        file_path (str): The path to the HDF5 file to explore.

    Outputs:
        This function prints the structure of the HDF5 file, including paths, dataset shapes, data
        types, compression (if applied) as well as the size of each dataset in gigabytes.
    """
    def explore_hdf5(item, path='/', indent=0):
        total_size_gb = 0
        indent_str = '    ' * indent

        if isinstance(item, h5py.Dataset):
            if '_index' in item.attrs:
                index_name = item.attrs['_index']
                print(f"{indent_str}{path} is a Dataset with index: {index_name}")
            else:
                dataset_size_gb = (np.prod(item.shape) * item.dtype.itemsize) / (1024 ** 3)
                total_size_gb += dataset_size_gb
                print(f"{indent_str}{path} is a Dataset with shape {item.shape}, "
                      f"dtype {item.dtype}, and size {dataset_size_gb:.4f} GB")

            # Add the compression information if available
            compression = item.compression if item.compression else "None"
            print(f"{indent_str}Compression: {compression}")

        elif isinstance(item, h5py.Group):
            index_info = ""
            if '_index' in item.attrs:
                index_name = item.attrs['_index']
                index_info = f" with index: {index_name}"
            print(f"{indent_str}{path} is a Group{index_info}")
            for key in item.keys():
                total_size_gb += explore_hdf5(item[key], path=f"{path}{key}/", indent=indent + 1)

        return total_size_gb

    with h5py.File(file_path, 'r') as f:
        print(f"AnnData object with n_obs × n_vars = {f['X'].attrs['shape'][0]} x {f['X'].attrs['shape'][1]}")
        total_size_gb = explore_hdf5(f)
        print(f"\nTotal size of the HDF5 file: {total_size_gb:.4f} GB")


def get_csr_matrix_size(source_group, row_indices, col_indices, batch_size):
    """
    Calculates the size of a CSR (Compressed Sparse Row) matrix slice.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the CSR matrix.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        batch_size (int): The size of the batches for processing rows.

    Returns:
        int: The total size of the sliced CSR matrix in bytes.
    """
    data_dtype = source_group['data'].dtype
    indices_dtype = source_group['indices'].dtype
    indptr_dtype = source_group['indptr'].dtype

    total_data_size = 0
    total_indices_size = 0
    total_indptr_size = (len(row_indices) + 1) * indptr_dtype.itemsize

    for start in range(0, len(row_indices), batch_size):
        end = min(start + 1000, len(row_indices))
        batch_row_indices = row_indices[start:end]

        for row_idx in batch_row_indices:
            data_start_idx = source_group['indptr'][row_idx]
            data_end_idx = source_group['indptr'][row_idx + 1]

            if data_start_idx < data_end_idx:
                data = source_group['data'][data_start_idx:data_end_idx]
                indices = source_group['indices'][data_start_idx:data_end_idx]

                mask = np.isin(indices, col_indices)
                data = data[mask]
                indices = indices[mask]

                total_data_size += data.shape[0] * data_dtype.itemsize
                total_indices_size += indices.shape[0] * indices_dtype.itemsize

    total_size = total_data_size + total_indices_size + total_indptr_size
    return total_size


def get_csc_matrix_size(source_group, row_indices, col_indices, batch_size):
    """
    Calculates the size of a CSC (Compressed Sparse Column) matrix slice.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the CSC matrix.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        batch_size (int): The size of the batches for processing columns.

    Returns:
        int: The total size of the sliced CSC matrix in bytes.
    """
    data_dtype = source_group['data'].dtype
    indices_dtype = source_group['indices'].dtype
    indptr_dtype = source_group['indptr'].dtype

    total_data_size = 0
    total_indices_size = 0
    total_indptr_size = (len(col_indices) + 1) * indptr_dtype.itemsize

    for start in range(0, len(col_indices), batch_size):
        end = min(start + batch_size, len(col_indices))
        batch_col_indices = col_indices[start:end]

        for col_idx in batch_col_indices:
            data_start_idx = source_group['indptr'][col_idx]
            data_end_idx = source_group['indptr'][col_idx + 1]

            if data_start_idx < data_end_idx:
                data = source_group['data'][data_start_idx:data_end_idx]
                indices = source_group['indices'][data_start_idx:data_end_idx]

                mask = np.isin(indices, row_indices)
                data = data[mask]
                indices = indices[mask]

                total_data_size += data.shape[0] * data_dtype.itemsize
                total_indices_size += indices.shape[0] * indices_dtype.itemsize

    total_size = total_data_size + total_indices_size + total_indptr_size
    return total_size


def get_categorical_group_size(source_group, row_indices, col_indices):
    """
    Calculates the size of a categorical group slice.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the categorical data.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.

    Returns:
        int: The total size of the sliced categorical group in bytes.
    """
    size_in_bytes = 0

    categories = source_group['categories']
    categories_size = categories.size * categories.dtype.itemsize
    size_in_bytes += categories_size

    if 'var' in source_group.name:
        codes = source_group['codes'][col_indices]
    elif 'obs' in source_group.name:
        codes = source_group['codes'][row_indices]
    else:
        raise ValueError("source_group.name must contain either 'var' or 'obs'")

    unique_codes = np.unique(codes)
    new_categories_size = unique_codes.size * categories.dtype.itemsize
    codes_size = codes.size * codes.dtype.itemsize
    size_in_bytes += new_categories_size + codes_size

    return size_in_bytes


def get_obsp_group_size(source_group, row_indices, batch_size):
    """
    Calculates the size of an 'obsp' group slice.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the 'obsp' data.
        row_indices (array-like): The indices of the rows to slice.
        batch_size (int): The size of the batches for processing rows.

    Returns:
        int: The total size of the sliced 'obsp' group in bytes.
    """
    total_size = 0
    for key in source_group.keys():
        item = source_group[key]
        if isinstance(item, h5py.Group):
            parent_encoding_type = item.attrs.get('encoding-type', None)
            is_csr = True
            if parent_encoding_type == "csc_matrix":
                is_csr = False
            total_size += get_matrix_group_size(item, row_indices, row_indices, batch_size, is_csr)
        elif isinstance(item, h5py.Dataset):
            data_dtype = item.dtype
            data_shape = (len(row_indices), len(row_indices))
            data_size = np.prod(data_shape) * data_dtype.itemsize
            total_size += data_size

    return total_size


def get_varp_group_size(source_group, col_indices, batch_size):
    """
    Calculates the size of a 'varp' group slice.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the 'varp' data.
        col_indices (array-like): The indices of the columns to slice.
        batch_size (int): The size of the batches for processing columns.

    Returns:
        int: The total size of the sliced 'varp' group in bytes.
    """
    total_size = 0
    for key in source_group.keys():
        item = source_group[key]
        if isinstance(item, h5py.Group):
            parent_encoding_type = item.attrs.get('encoding-type', None)
            is_csr = True
            if parent_encoding_type == "csc_matrix":
                is_csr = False
            total_size += get_matrix_group_size(item, col_indices, col_indices, batch_size, is_csr)
        elif isinstance(item, h5py.Dataset):
            data_dtype = item.dtype
            data_shape = (len(col_indices), len(col_indices))
            data_size = np.prod(data_shape) * data_dtype.itemsize
            total_size += data_size

    return total_size


def get_raw_group_size(source_group, row_indices, col_indices, batch_size):
    """
    Calculates the size of a 'raw' group slice.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the 'raw' data.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        batch_size (int): The size of the batches for processing rows and columns.

    Returns:
        int: The total size of the sliced 'raw' group in bytes.
    """
    total_size = 0

    if 'X' in source_group.name:
        num_cols = source_group.attrs['shape'][1]
        col_indices = np.arange(num_cols)
        total_size += get_matrix_group_size(
            source_group,
            row_indices,
            col_indices,
            batch_size,
            is_csr=True
        )

    if 'var' in source_group.name:
        for var_key in source_group.keys():
            item = source_group[var_key]
            if isinstance(item, h5py.Dataset):
                total_size += item.size * item.dtype.itemsize
            elif isinstance(item, h5py.Group):
                total_size += get_group_size(item, row_indices, col_indices, batch_size)

    if 'varm' in source_group.name:
        for varm_key in source_group.keys():
            item = source_group[varm_key]
            if isinstance(item, h5py.Dataset):
                total_size += item.size * item.dtype.itemsize
            elif isinstance(item, h5py.Group):
                total_size += get_group_size(item, row_indices, col_indices, batch_size)

    return total_size


def get_dataset_size(
    dataset,
    row_indices,
    col_indices,
    parent_encoding_type=None,
    parent_group_name=None
):
    """
    Calculates the size of a dataset slice.

    Args:
        dataset (h5py.Dataset): The HDF5 dataset to process.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        parent_encoding_type (str, optional): The encoding type of the parent group.
            Default is None.
        parent_group_name (str, optional): The name of the parent group. Default is None.

    Returns:
        int: The size of the dataset slice in bytes.
    """
    if (parent_encoding_type in ['csr_matrix', 'csc_matrix'] or
            dataset.attrs.get('encoding-type') == 'categorical'):
        return 0

    size_in_bytes = 0
    if dataset.ndim == 1:
        if 'obs' in parent_group_name:
            valid_row_indices = row_indices[row_indices < dataset.shape[0]]
            size_in_bytes = len(valid_row_indices) * dataset.dtype.itemsize
        elif 'var' in parent_group_name:
            valid_col_indices = col_indices[col_indices < dataset.shape[0]]
            size_in_bytes = len(valid_col_indices) * dataset.dtype.itemsize
        else:
            size_in_bytes = dataset.size * dataset.dtype.itemsize
    elif dataset.ndim == 2:
        if 'layers' in parent_group_name:
            # Calculate size across both dimensions
            size_in_bytes = len(row_indices) * len(col_indices) * dataset.dtype.itemsize
        elif 'obsm' in parent_group_name:
            # Calculate size across rows using row_indices
            size_in_bytes = len(row_indices) * dataset.shape[1] * dataset.dtype.itemsize
        elif 'varm' in parent_group_name:
            # Calculate size across rows using col_indices
            size_in_bytes = len(col_indices) * dataset.shape[1] * dataset.dtype.itemsize
    else:
        size_in_bytes = dataset.size * dataset.dtype.itemsize

    return size_in_bytes


def get_matrix_group_size(source_group, row_indices, col_indices, batch_size, is_csr=True):
    """
    Passed the size of a matrix group slice, either CSR or CSC.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the matrix.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        batch_size (int): The size of the batches for processing.
        is_csr (bool): True if the matrix is CSR, False if CSC.

    Returns:
        int: The size of the matrix slice in bytes.
    """
    if is_csr:
        return get_csr_matrix_size(source_group, row_indices, col_indices, batch_size)
    return get_csc_matrix_size(source_group, row_indices, col_indices, batch_size)


def get_group_size(source_group, row_indices, col_indices, batch_size):
    """
    Calculates the size of an HDF5 group slice.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        batch_size (int): The size of the batches for processing.

    Returns:
        int: The size of the group slice in bytes.
    """
    total_size = 0
    parent_encoding_type = source_group.attrs.get('encoding-type', None)
    if parent_encoding_type == 'csr_matrix':
        total_size += get_matrix_group_size(
            source_group,
            row_indices,
            col_indices,
            batch_size,
            is_csr=True
        )
    elif parent_encoding_type == 'csc_matrix':
        total_size += get_matrix_group_size(
            source_group,
            row_indices,
            col_indices,
            batch_size,
            is_csr=False
        )
    elif parent_encoding_type == 'categorical':
        total_size += get_categorical_group_size(
            source_group,
            row_indices,
            col_indices
        )
    elif 'obsp' in source_group.name:
        total_size += get_obsp_group_size(source_group, row_indices, batch_size)
    elif 'varp' in source_group.name:
        total_size += get_varp_group_size(source_group, col_indices, batch_size)
    else:
        for key in source_group.keys():
            item = source_group[key]

            if isinstance(item, h5py.Dataset):
                total_size += get_dataset_size(
                    item,
                    row_indices,
                    col_indices,
                    parent_encoding_type,
                    source_group.name
                )
            elif isinstance(item, h5py.Group):
                if source_group.name == '/raw':
                    total_size += get_raw_group_size(item, row_indices, col_indices, batch_size)
                else:
                    total_size += get_group_size(item, row_indices, col_indices, batch_size)

    return total_size


def get_slice_size(source_file_path, rows: slice, cols: slice, batch_size=1000):
    """
    Calculates the total size of a slice of an HDF5 file.

    Args:
        source_file_path (str): The file path to the source HDF5 file.
        rows (slice): The slice object specifying the row indices to extract.
        cols (slice): The slice object specifying the column indices to extract.
        batch_size (int): The size of the batches for processing.

    Returns:
        int: The total size of the slice in bytes.
    """
    total_size = 0
    with h5py.File(source_file_path, 'r') as f:
        num_rows = f['obs'][f['obs'].attrs['_index']].shape[0]
        num_cols = f['var'][f['var'].attrs['_index']].shape[0]

        row_indices = np.arange(
            rows.start or 0,
            rows.stop if rows.stop is not None else num_rows,
            rows.step or 1
        )
        col_indices = np.arange(
            cols.start or 0,
            cols.stop if cols.stop is not None else num_cols,
            cols.step or 1
        )

        row_indices = row_indices[row_indices < num_rows]
        col_indices = col_indices[col_indices < num_cols]

        for key in f.keys():
            item = f[key]
            total_size += get_group_size(item, row_indices, col_indices, batch_size)

    return total_size


def read_process_csr_matrix(source_group, row_indices, col_indices):
    """
    Processes and slices a CSR (Compressed Sparse Row) matrix into memory.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the CSR matrix.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.

    Returns:
        csr_matrix: A sliced CSR matrix.
    """
    data_list = []
    indices_list = []
    total_indptr = np.zeros(len(row_indices) + 1, dtype=source_group['indptr'].dtype)
    current_length = 0

    # Iterate through the specified row indices to slice the CSR matrix
    for i, row_idx in enumerate(row_indices):
        data_start_idx = source_group['indptr'][row_idx]
        data_end_idx = source_group['indptr'][row_idx + 1]

        if data_start_idx < data_end_idx:
            # Extract data and indices for the current row
            data = source_group['data'][data_start_idx:data_end_idx]
            indices = source_group['indices'][data_start_idx:data_end_idx]

            # Mask to select columns of interest
            mask = np.isin(indices, col_indices)
            if np.any(mask):
                data = data[mask]
                indices = indices[mask]

                # Map indices to new indices based on the selected columns
                index_map = {col: idx for idx, col in enumerate(col_indices)}
                indices = np.array([index_map[i] for i in indices])

                data_list.append(data)
                indices_list.append(indices)

                current_length += data.shape[0]
                total_indptr[i + 1] = current_length
            else:
                total_indptr[i + 1] = current_length
        else:
            total_indptr[i + 1] = current_length

    data_array = (
        np.concatenate(data_list)
        if data_list
        else np.array([], dtype=source_group['data'].dtype)
    )
    indices_array = (
        np.concatenate(indices_list)
        if indices_list
        else np.array([], dtype=source_group['indices'].dtype)
    )
    indptr_array = total_indptr

    return csr_matrix((
        data_array,
        indices_array,
        indptr_array),
        shape=(len(row_indices), len(col_indices))
    )


def read_process_csc_matrix(source_group, row_indices, col_indices):
    """
    Processes and slices a CSC (Compressed Sparse Column) matrix into memory.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the CSC matrix.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.

    Returns:
        csc_matrix: A sliced CSC matrix.
    """
    data_list = []
    indices_list = []
    total_indptr = np.zeros(len(col_indices) + 1, dtype=source_group['indptr'].dtype)
    current_length = 0

    # Iterate through the specified column indices to slice the CSC matrix
    for i, col_idx in enumerate(col_indices):
        data_start_idx = source_group['indptr'][col_idx]
        data_end_idx = source_group['indptr'][col_idx + 1]

        if data_start_idx < data_end_idx:
            # Extract data and indices for the current column
            data = source_group['data'][data_start_idx:data_end_idx]
            indices = source_group['indices'][data_start_idx:data_end_idx]

            # Mask to select rows of interest
            mask = np.isin(indices, row_indices)
            if np.any(mask):
                data = data[mask]
                indices = indices[mask]

                # Map indices to new indices based on the selected rows
                index_map = {row: idx for idx, row in enumerate(row_indices)}
                indices = np.array([index_map[i] for i in indices])

                data_list.append(data)
                indices_list.append(indices)

                current_length += data.shape[0]
                total_indptr[i + 1] = current_length
            else:
                total_indptr[i + 1] = current_length
        else:
            total_indptr[i + 1] = current_length

    data_array = np.concatenate(data_list) \
        if data_list \
        else np.array([], dtype=source_group['data'].dtype)
    indices_array = np.concatenate(indices_list) \
        if indices_list \
        else np.array([], dtype=source_group['indices'].dtype)
    indptr_array = total_indptr

    return csc_matrix((
        data_array,
        indices_array,
        indptr_array),
        shape=(len(row_indices), len(col_indices))
    )


def read_process_matrix(source_group, row_indices, col_indices, is_csr):
    """
    Process and slice a matrix (CSR or CSC) into memory.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the matrix.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        is_csr (bool): True if the matrix is CSR, False if CSC.

    Returns:
        csr_matrix or csc_matrix: The sliced matrix.
    """
    if is_csr:
        result = slicers.read_process_csr_matrix(source_group.file.filename, source_group.name, row_indices, col_indices)
        return csr_matrix((result[0], result[1], result[2]), shape=(len(row_indices), len(col_indices)))
    result = slicers.read_process_csc_matrix(source_group.file.filename, source_group.name, row_indices, col_indices)
    return csc_matrix((result[0], result[1], result[2]), shape=(len(row_indices), len(col_indices)))


def read_process_categorical_group(source_group, row_indices, col_indices):
    """
    Process an HDF5 group representing a categorical variable, slicing based on
    the specified row or column indices.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.

    Returns:
        pandas.Categorical: A categorical representation of the sliced data.
    """
    # Retrieve the 'categories' dataset from the source group
    categories = source_group['categories'][:]

    # Decode byte strings to UTF-8 if necessary
    if isinstance(categories[0], bytes):
        categories = [cat.decode('utf-8') for cat in categories]

    # Determine whether to slice based on row or column indices
    if 'var' in source_group.name:
        codes = source_group['codes'][col_indices]
    elif 'obs' in source_group.name:
        codes = source_group['codes'][row_indices]
    else:
        raise ValueError("Source group name must contain 'var' or 'obs'")

    # Ensure unique codes are integers
    unique_codes = np.unique(codes).astype(int)
    # Generate new categories based on the unique codes
    new_categories = [categories[i] for i in unique_codes]
    # Create a mapping from old codes to new codes
    code_map = {old_code: new_code for new_code, old_code in enumerate(unique_codes)}
    # Map the old codes to the new codes
    new_codes = np.array([code_map[code] for code in codes], dtype=codes.dtype)

    # Return a pandas Categorical from the new codes and categories
    return pd.Categorical.from_codes(new_codes, new_categories)


def read_process_dataframe_group(source_group, indices, is_obs):
    """
    Processes and slices a dataframe group from an HDF5 file.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the dataframe.
        indices (array-like): The indices to slice.
        is_obs (bool): True if the dataframe belongs to 'obs', False if it belongs to 'var'.

    Returns:
        pd.DataFrame: The sliced dataframe with the specified indices.
    """
    sliced_data = {}

    # Iterate over all keys in the source group
    for key in source_group.keys():
        if key == "_index":
            continue # Skip the index key
        item = source_group[key]
        if isinstance(item, h5py.Dataset):
            # Process datasets by slicing based on indices
            sliced_data[key] = item[indices]
        elif isinstance(item, h5py.Group):
            # Recursively process sub-groups
            sliced_data[key] = read_process_group(item, indices, indices)

    index_key = "_index"

    # Get the original indices from the parent 'obs' or 'var' group
    if is_obs:
        original_indices = (
            source_group.parent['obs'][source_group.parent['obs'].attrs[index_key]][indices]
        )
    else:
        original_indices = (
            source_group.parent['var'][source_group.parent['var'].attrs[index_key]][indices]
        )

    # Return the sliced dataframe with the appropriate indices
    return pd.DataFrame(sliced_data, index=original_indices.astype(str))


def read_process_raw_group(source_group, row_indices):
    """
    Process an HDF5 group representing a 'raw' group, slicing based on the specified row indices.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        row_indices (array-like): The indices of the rows to slice.

    Returns:
        dict: A dictionary containing the sliced data from the 'raw' group.
    """
    sliced_data = {}

    def copy_group(group):
        """
        Recursively copy an HDF5 group into a dictionary.

        Args:
            group (h5py.Group): The HDF5 group to copy.

        Returns:
            dict: A dictionary representation of the HDF5 group.
        """
        data = {}
        for key in group.keys():
            item = group[key]
            if isinstance(item, h5py.Group):
                # Recursively copy sub-groups
                data[key] = copy_group(item)
            elif isinstance(item, h5py.Dataset):
                # Copy datasets
                data[key] = item[()]
        return data

    # Process the 'X' dataset within the 'raw' group
    if 'X' in source_group:
        parent_encoding_type = source_group['X'].attrs.get('encoding-type', None)
        is_csr = parent_encoding_type != "csc_matrix"
        # Get all column indices for slicing
        col_indices = np.arange(source_group['X'].attrs['shape'][1])
        sliced_data['X'] = read_process_matrix(source_group['X'], row_indices, col_indices, is_csr)

    # Process the 'var' dataframe within the 'raw' group
    if 'var' in source_group:
        # Slice the 'var' dataframe (use all rows with slice(None) since we want to keep
        # the unsliced version)
        sliced_data['var'] = read_process_dataframe_group(
            source_group['var'],
            slice(None),
            is_obs=False
        )

    # Process the 'varm' group within the 'raw' group
    if 'varm' in source_group:
        # Recursively copy the 'varm' group
        sliced_data['varm'] = copy_group(source_group['varm'])

    return sliced_data


def read_process_obsp_group(source_group, row_indices):
    """
    Process an HDF5 group representing an 'obsp' group, slicing based on the specified row indices.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        row_indices (array-like): The indices of the rows to slice.

    Returns:
        dict: A dictionary containing the sliced data from the 'obsp' group.
    """
    sliced_data = {}
    for key in source_group.keys():
        item = source_group[key]
        if isinstance(item, h5py.Group):
            # Determine if the matrix is CSR or CSC
            parent_encoding_type = item.attrs.get('encoding-type', None)
            is_csr = parent_encoding_type != "csc_matrix"
            sliced_data[key] = read_process_matrix(item, row_indices, row_indices, is_csr)
        elif isinstance(item, h5py.Dataset):
            # Slice the dataset across both dimensions using row indices
            data = item[row_indices, :][:, row_indices]
            sliced_data[key] = data

    return sliced_data


def read_process_varp_group(source_group, col_indices):
    """
    Process an HDF5 group representing a 'varp' group, slicing based on the
    specified column indices.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        col_indices (array-like): The indices of the columns to slice.

    Returns:
        dict: A dictionary containing the sliced data from the 'varp' group.
    """
    sliced_data = {}
    for key in source_group.keys():
        item = source_group[key]
        if isinstance(item, h5py.Group):
            # Determine if the matrix is CSR or CSC
            parent_encoding_type = item.attrs.get('encoding-type', None)
            is_csr = parent_encoding_type != "csc_matrix"
            sliced_data[key] = read_process_matrix(item, col_indices, col_indices, is_csr)
        elif isinstance(item, h5py.Dataset):
            # Slice the dataset across both dimensions using column indices
            data = item[col_indices, :][:, col_indices]
            sliced_data[key] = data

    return sliced_data


def read_process_dataset(
        dataset,
        row_indices,
        col_indices,
        parent_encoding_type=None,
        parent_group_name=None
):
    """
    Process an HDF5 dataset based on the specified row and column indices.

    Args:
        dataset (h5py.Dataset): The HDF5 dataset to process.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        parent_encoding_type (str, optional): The encoding type of the parent group.
            Default is None.
        parent_group_name (str, optional): The name of the parent group. Default is None.

    Returns:
        numpy.ndarray or None: The sliced data from the dataset or None if no processing is done.
    """
    data = None

    # Skip processing here as it will be handled by read_h5ad_process_matrix
    if parent_encoding_type in ['csr_matrix', 'csc_matrix']:
        return None

    # Scalar datasets
    if dataset.shape == ():
        data = (
            str(dataset[()], 'utf-8')
            if dataset.attrs['encoding-type'] == 'string'
            else dataset[()]
        )
    # 1-D datasets
    elif dataset.ndim == 1:
        data = (
            np.array([str(val, 'utf-8') for val in dataset[:]], dtype=object)
            if dataset.attrs['encoding-type'] == 'string-array'
            else dataset[:]
        )
    # 2-D datasets
    elif dataset.ndim == 2:
        if 'layers' in parent_group_name:
            # Slice across both dimensions
            data = np.empty((len(row_indices), len(col_indices)), dtype=dataset.dtype)
            for i, row in enumerate(row_indices):
                data[i, :] = dataset[row, col_indices]
        elif 'obsm' in parent_group_name:
            # Slice across rows using row_indices
            data = np.empty((len(row_indices), dataset.shape[1]), dtype=dataset.dtype)
            for i, row in enumerate(row_indices):
                data[i, :] = dataset[row, :]
        elif 'varm' in parent_group_name:
            # Slice across rows using col_indices
            data = np.empty((len(col_indices), dataset.shape[1]), dtype=dataset.dtype)
            for i, col in enumerate(col_indices):
                data[i, :] = dataset[col, :]

    return data


def read_process_group(source_group, row_indices, col_indices):
    """
    Process an HDF5 group based on the specified row and column indices.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.

    Returns:
        dict: A dictionary containing the sliced data.
    """
    # Get the encoding type of the parent group
    parent_encoding_type = source_group.attrs.get('encoding-type', None)
    sliced_data = {}

    # Process based on the encoding type
    if parent_encoding_type == 'csr_matrix':
        # CSR group - X and Layers
        sliced_data = read_process_matrix(source_group, row_indices, col_indices, is_csr=True)
    elif parent_encoding_type == 'csc_matrix':
        # CSC group - X and Layers
        sliced_data = read_process_matrix(source_group, row_indices, col_indices, is_csr=False)
    elif parent_encoding_type == 'categorical':
        # Categorical group inside Obs, Var, and Raw/Var
        sliced_data = read_process_categorical_group(source_group, row_indices, col_indices)
    elif 'obsp' in source_group.name:
        sliced_data = read_process_obsp_group(source_group, row_indices)
    elif 'varp' in source_group.name:
        sliced_data = read_process_varp_group(source_group, col_indices)
    elif 'obs' in source_group.name and parent_encoding_type == 'dataframe':
        sliced_data = read_process_dataframe_group(source_group, row_indices, is_obs=True)
    elif 'var' in source_group.name and parent_encoding_type == 'dataframe':
        sliced_data = read_process_dataframe_group(source_group, col_indices, is_obs=False)
    elif parent_encoding_type == 'raw':
        sliced_data = read_process_raw_group(source_group, row_indices)
    else:
        # Process nested groups and datasets usually when dictionary is encountered
        for key in source_group.keys():
            item = source_group[key]

            if isinstance(item, h5py.Dataset):
                # Process dataset
                sliced_data[key] = read_process_dataset(
                    item,
                    row_indices,
                    col_indices,
                    parent_encoding_type,
                    source_group.name
                )
            elif isinstance(item, h5py.Group):
                # Recursively process sub-group
                sliced_data[key] = read_process_group(item, row_indices, col_indices)

    return sliced_data


def read_slice_h5ad(file_path, rows: slice, cols: slice, check_size=False, include_raw=False):
    """
    Slice a .h5ad file based on specified rows and columns and return an AnnData object.

    Args:
        file_path (str): The path to the .h5ad file to be sliced.
        rows (slice): A slice object specifying the range of rows to include.
        cols (slice): A slice object specifying the range of columns to include.
        check_size (bool, optional): If True, check if the slice size fits in memory before slicing.
            Default is False.
        include_raw (bool, optional): If True, include the 'raw' group in the sliced data.
            Default is False.

    Returns:
        AnnData: An AnnData object containing the sliced data.

    Raises:
        MemoryError: If the slice size exceeds available memory when check_size is True.
        ValueError: If no rows or columns are available to slice.
    """
    if check_size:
        # Check if the sliced data will fit in available memory
        _, available_memory_gb = get_memory_info()
        total_size_b = get_slice_size(file_path, rows, cols)
        total_size_gb = total_size_b / (1024 ** 3)

        if total_size_gb > available_memory_gb:
            raise MemoryError(
                f"The slice size ({total_size_gb:.2f} GB) exceeds the available "
                f"physical + swap memory ({available_memory_gb:.2f} GB)."
            )

        print("File fits in memory and will be sliced.")

    with h5py.File(file_path, 'r') as f:
        # Get the total number of rows and columns
        num_rows = f['X'].attrs['shape'][0]
        num_cols = f['X'].attrs['shape'][1]

        # Generate row and column indices based on the slice objects
        row_indices = np.arange(
            rows.start or 0,
            rows.stop if rows.stop is not None else num_rows,
            rows.step or 1
        )
        col_indices = np.arange(
            cols.start or 0,
            cols.stop if cols.stop is not None else num_cols,
            cols.step or 1
        )

        # Ensure indices are within bounds
        row_indices = row_indices[row_indices < num_rows]
        col_indices = col_indices[col_indices < num_cols]

        if len(row_indices) == 0 or len(col_indices) == 0:
            raise ValueError("No rows or columns to slice")

        sliced_data = {}
        for key in f.keys():
            item = f[key]
            if item == 'raw' and include_raw:
                continue
            if isinstance(item, h5py.Group):
                # Process h5py.Group items (X, layers, obs, ...)
                sliced_data[key] = read_process_group(item, row_indices, col_indices)
            elif isinstance(item, h5py.Dataset):
                # Process h5py.Dataset items (usually not the case, mostly for completeness)
                sliced_data[key] = read_process_dataset(item, row_indices, col_indices)

        # Extract data components from the sliced data
        x = sliced_data.pop('X')
        layers = sliced_data.pop('layers', {})
        obs = sliced_data.pop('obs')
        obsm = sliced_data.pop('obsm', {})
        obsp = sliced_data.pop('obsp', {})
        raw = sliced_data.pop('raw', {}) if include_raw else None
        uns = sliced_data.pop('uns', {})
        var = sliced_data.pop('var')
        varm = sliced_data.pop('varm', {})
        varp = sliced_data.pop('varp', {})

        # Create and return the AnnData object
        adata = ad.AnnData(
            X=x,
            layers=layers,
            obs=obs,
            obsm=obsm,
            obsp=obsp,
            raw=raw,
            uns=uns,
            var=var,
            varm=varm,
            varp=varp
        )

        return adata


def calculate_batch_size(memory_fraction, num_cols, dtype_size):
    """
    Calculate the batch size based on available memory, number of columns, and data type size.

    Args:
        memory_fraction (float): Fraction of total memory to use for the calculation.
        num_cols (int): Number of columns in the dataset.
        dtype_size (int): Size of the data type in bytes.

    Returns:
        int: The calculated batch size, ensuring at least 1 row is included.
    """
    available_memory_b, _ = get_memory_info()
    memory_to_use = available_memory_b * memory_fraction
    row_size = num_cols * dtype_size
    return max(1, int(memory_to_use // row_size))


def get_memory_info():
    """
    Retrieve and return the system's available physical + swap memory capacity.

    Returns:
        tuple: A tuple containing:
            - available_memory_b (int): Available memory in bytes.
            - available_memory_gb (float): Available memory in gigabytes.
    """
    available_memory_b = psutil.virtual_memory().available
    available_memory_gb = available_memory_b / (1024 ** 3)
    return available_memory_b, available_memory_gb


def copy_attrs(source, dest, shape=None):
    """
    Copies attributes from the source to the destination HDF5 object.

    Args:
        source (h5py.AttributeManager): The source HDF5 object containing attributes.
        dest (h5py.AttributeManager): The destination HDF5 object to copy the attributes to.
        shape (tuple, optional): The shape to set as an attribute in the destination.
            Default is None.
    """
    # Copy each attribute from the source to the destination
    for key, value in source.attrs.items():
        dest.attrs[key] = value

    # If a shape is provided, set it as an attribute in the destination
    if shape is not None:
        dest.attrs['shape'] = shape


def write_process_csr_matrix(source_group, dest_group, row_indices, col_indices, batch_size):
    """
    Processes and slices a CSR (Compressed Sparse Row) matrix.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the CSR matrix.
        dest_group (h5py.Group): The destination HDF5 group to write the processed data.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        batch_size (int): The size of the batches for processing.
    """
    # Create datasets for the data, indices, and indptr in the destination group
    data_group = dest_group.create_dataset(
        'data', shape=(0,), maxshape=(None,), dtype=source_group['data'].dtype,
        compression=source_group['data'].compression
    )
    indices_group = dest_group.create_dataset(
        'indices', shape=(0,), maxshape=(None,), dtype=source_group['indices'].dtype,
        compression=source_group['indices'].compression
    )
    indptr_group = dest_group.create_dataset(
        'indptr', shape=(len(row_indices) + 1,), dtype=source_group['indptr'].dtype,
        compression=source_group['indptr'].compression
    )
    # Initialize the first element of indptr
    indptr_group[0] = 0

    total_indptr = np.zeros(len(row_indices) + 1, dtype=source_group['indptr'].dtype)
    current_length = 0

    # Process rows in batches
    for start in range(0, len(row_indices), batch_size):
        end = min(start + batch_size, len(row_indices))
        batch_row_indices = row_indices[start:end]

        for i, row_idx in enumerate(batch_row_indices, start=start):
            data_start_idx = source_group['indptr'][row_idx]
            data_end_idx = source_group['indptr'][row_idx + 1]

            if data_start_idx < data_end_idx:
                data = source_group['data'][data_start_idx:data_end_idx]
                indices = source_group['indices'][data_start_idx:data_end_idx]

                # Mask to select columns of interest
                mask = np.isin(indices, col_indices)
                data = data[mask]
                indices = indices[mask]

                # Map indices to new indices based on the selected columns
                index_map = {col: i for i, col in enumerate(col_indices)}
                indices = np.array([index_map[i] for i in indices])

                # Resize and update the data and indices groups
                data_group.resize((current_length + data.shape[0],))
                indices_group.resize((current_length + indices.shape[0],))

                data_group[current_length:current_length + data.shape[0]] = data
                indices_group[current_length:current_length + indices.shape[0]] = indices

                current_length += data.shape[0]
                total_indptr[i + 1] = current_length

    # Update the indptr group
    indptr_group[:] = total_indptr
    # Copy attributes
    copy_attrs(source_group, dest_group, shape=(len(row_indices), len(col_indices)))


def write_process_csc_matrix(source_group, dest_group, row_indices, col_indices, batch_size):
    """
    Processes and slices a CSC (Compressed Sparse Column) matrix.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the CSC matrix.
        dest_group (h5py.Group): The destination HDF5 group to write the processed data.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        batch_size (int): The size of the batches for processing.
    """
    # Create datasets for the data, indices, and indptr in the destination group
    data_group = dest_group.create_dataset(
        'data', shape=(0,), maxshape=(None,), dtype=source_group['data'].dtype,
        compression=source_group['data'].compression
    )
    indices_group = dest_group.create_dataset(
        'indices', shape=(0,), maxshape=(None,), dtype=source_group['indices'].dtype,
        compression=source_group['indices'].compression
    )
    indptr_group = dest_group.create_dataset(
        'indptr', shape=(len(col_indices) + 1,), dtype=source_group['indptr'].dtype,
        compression=source_group['indptr'].compression
    )
    indptr_group[0] = 0 # Initialize the first element of indptr

    total_indptr = np.zeros(len(col_indices) + 1, dtype=source_group['indptr'].dtype)
    current_length = 0

    # Process columns in batches
    for start in range(0, len(col_indices), batch_size):
        end = min(start + batch_size, len(col_indices))
        batch_col_indices = col_indices[start:end]

        for i, col_idx in enumerate(batch_col_indices, start=start):
            data_start_idx = source_group['indptr'][col_idx]
            data_end_idx = source_group['indptr'][col_idx + 1]

            if data_start_idx < data_end_idx:
                data = source_group['data'][data_start_idx:data_end_idx]
                indices = source_group['indices'][data_start_idx:data_end_idx]

                # Mask to select rows of interest
                mask = np.isin(indices, row_indices)
                data = data[mask]
                indices = indices[mask]

                # Map indices to new indices based on the selected rows
                index_map = {row: i for i, row in enumerate(row_indices)}
                indices = np.array([index_map[i] for i in indices])

                # Resize and update the data and indices groups
                data_group.resize((current_length + data.shape[0],))
                indices_group.resize((current_length + indices.shape[0],))

                data_group[current_length:current_length + data.shape[0]] = data
                indices_group[current_length:current_length + indices.shape[0]] = indices

                current_length += data.shape[0]
                total_indptr[i + 1] = current_length

    # Update the indptr group
    indptr_group[:] = total_indptr
    # Copy attributes
    copy_attrs(source_group, dest_group, shape=(len(row_indices), len(col_indices)))


def write_process_matrix(source_group, dest_group, row_indices, col_indices, batch_size, is_csr):
    """
    Passes a sliced matrix, either CSR or CSC, based on the specified indices and batch size.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the matrix.
        dest_group (h5py.Group): The destination HDF5 group to write the processed data.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        batch_size (int): The size of the batches for processing.
        is_csr (bool): True if the matrix is CSR, False if CSC.
    """
    if is_csr:
        write_process_csr_matrix(source_group, dest_group, row_indices, col_indices, batch_size)
    else:
        write_process_csc_matrix(source_group, dest_group, row_indices, col_indices, batch_size)


def write_process_categorical_group(source_group, dest_group, row_indices, col_indices):
    """
    Processes and copies a categorical group from the source HDF5 file to the destination HDF5 file,
    slicing based on the specified row or column indices.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the categorical data.
        dest_group (h5py.Group): The destination HDF5 group to write the processed data.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
    """
    # Read the categories dataset
    categories = source_group['categories'][:]

    # Determine the correct slice of codes based on the group name
    if 'var' in source_group.name:
        codes = source_group['codes'][col_indices]
    elif 'obs' in source_group.name:
        codes = source_group['codes'][row_indices]
    else:
        raise ValueError("Source group name must contain 'var' or 'obs'")

    # Find unique codes and create new categories based on them
    unique_codes = np.unique(codes)
    new_categories = categories[unique_codes]

    # Create a mapping from old codes to new codes
    code_map = {old_code: new_code for new_code, old_code in enumerate(unique_codes)}

    # Map the old codes to the new codes
    new_codes = np.array([code_map[code] for code in codes], dtype=codes.dtype)

    # Create datasets for the new categories and codes in the destination group
    dest_group.create_dataset(
        'categories',
        data=new_categories,
        dtype=new_categories.dtype,
        compression=source_group['categories'].compression
    )
    dest_group.create_dataset(
        'codes',
        data=new_codes,
        dtype=new_codes.dtype,
        compression=source_group['codes'].compression
    )

    # Copy attributes from the source group to the destination group
    copy_attrs(source_group, dest_group)


def write_process_raw_group(source_group, dest_group, row_indices, batch_size):
    """
    Processes and copies a 'raw' group from the source HDF5 file to the destination HDF5 file,
    slicing based on the specified row indices.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the 'raw' data.
        dest_group (h5py.Group): The destination HDF5 group to write the processed data.
        row_indices (array-like): The indices of the rows to slice.
        batch_size (int): The size of the batches for processing.
    """
    # Process the 'X' dataset within the 'raw' group
    if 'X' in source_group.name:
        parent_encoding_type = source_group.attrs.get('encoding-type', None)
        is_csr = parent_encoding_type != "csc_matrix"
        write_process_matrix(
            source_group,
            dest_group,
            row_indices,
            np.arange(source_group.attrs['shape'][1]),
            batch_size,
            is_csr
        )

    # Process the 'var' dataframe within the 'raw' group
    if 'var' in source_group.name:
        # Copy the 'var' dataframe since we want to keep the unsliced version
        for var_key in source_group.keys():
            if var_key not in dest_group:
                source_group.copy(var_key, dest_group)

    # Process the 'varm' group within the 'raw' group
    if 'varm' in source_group.name:
        # Recursively copy the 'varm' group
        for varm_key in source_group.keys():
            if varm_key not in dest_group:
                source_group.copy(varm_key, dest_group)


def write_process_obsp_group(source_group, dest_group, row_indices, batch_size):
    """
    Processes and copies data from an 'obsp' group in the source HDF5 file to the
        destination HDF5 file,
    slicing based on the specified row indices.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the 'obsp' data.
        dest_group (h5py.Group): The destination HDF5 group to write the processed data.
        row_indices (array-like): The indices of the rows to slice.
        batch_size (int): The size of the batches for processing.
    """
    for key in source_group.keys():
        item = source_group[key]
        if isinstance(item, h5py.Group):
            new_group = dest_group.create_group(key)
            copy_attrs(item, new_group)
            # Determine if CSR or CSC
            parent_encoding_type = item.attrs.get('encoding-type', None)
            is_csr = parent_encoding_type != "csc_matrix"
            write_process_matrix(item, new_group, row_indices, row_indices, batch_size, is_csr)
        elif isinstance(item, h5py.Dataset):
            # Slice the dataset across both dimensions using row indices
            data = item[row_indices, :][:, row_indices]
            dset = dest_group.create_dataset(key, data=data, compression=item.compression)
            copy_attrs(item, dset, shape=data.shape)


def write_process_varp_group(source_group, dest_group, col_indices, batch_size):
    """
    Processes and copies data from a 'varp' group in the source HDF5 file to the
        destination HDF5 file,
    slicing based on the specified column indices.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the 'varp' data.
        dest_group (h5py.Group): The destination HDF5 group to write the processed data.
        col_indices (array-like): The indices of the columns to slice.
        batch_size (int): The size of the batches for processing.
    """
    for key in source_group.keys():
        item = source_group[key]
        if isinstance(item, h5py.Group):
            new_group = dest_group.create_group(key)
            copy_attrs(item, new_group)
            # Determine if CSR or CSC
            parent_encoding_type = item.attrs.get('encoding-type', None)
            is_csr = parent_encoding_type != "csc_matrix"
            write_process_matrix(item, new_group, col_indices, col_indices, batch_size, is_csr)
        elif isinstance(item, h5py.Dataset):
            # Slice the dataset across both dimensions using column indices
            data = item[col_indices, :][:, col_indices]
            dset = dest_group.create_dataset(key, data=data, compression=item.compression)
            copy_attrs(item, dset, shape=data.shape)


def write_process_dataset(
        dataset,
        dest_group,
        row_indices,
        col_indices,
        parent_encoding_type=None,
        parent_group_name=None
):
    """
    Processes and copies a dataset from a source HDF5 group to a destination HDF5 group,
        handling different encoding types and structures.

    Args:
        dataset (h5py.Dataset): The source HDF5 dataset to process.
        dest_group (h5py.Group): The destination HDF5 group to write the processed data.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        parent_encoding_type (str, optional): The encoding type of the parent group.
            Default is None.
        parent_group_name (str, optional): The name of the parent group. Default is None.
    """
    compression = dataset.compression if dataset.compression else None
    data = None

    # Skip processing for CSR or CSC matrix as it will be handled by process_matrix
    if parent_encoding_type in ['csr_matrix', 'csc_matrix']:
        return

    # 1-D datasets
    if dataset.ndim == 1:
        if 'obs' in parent_group_name:
            valid_row_indices = row_indices[row_indices < dataset.shape[0]]
            data = dataset[valid_row_indices]
        elif 'var' in parent_group_name:
            valid_col_indices = col_indices[col_indices < dataset.shape[0]]
            data = dataset[valid_col_indices]
        else:
            data = dataset[:]
    # 2-D datasets
    elif dataset.ndim == 2:
        if 'layers' in parent_group_name:
            # Slice across both dimensions
            data = np.empty((len(row_indices), len(col_indices)), dtype=dataset.dtype)
            for i, row in enumerate(row_indices):
                data[i, :] = dataset[row, col_indices]
        elif 'obsm' in parent_group_name:
            # Slice across rows using row_indices
            data = np.empty((len(row_indices), dataset.shape[1]), dtype=dataset.dtype)
            for i, row in enumerate(row_indices):
                data[i, :] = dataset[row, :]
        elif 'varm' in parent_group_name:
            # Slice across rows using col_indices
            data = np.empty((len(col_indices), dataset.shape[1]), dtype=dataset.dtype)
            for i, col in enumerate(col_indices):
                data[i, :] = dataset[col, :]

    # Create the new dataset in the destination group and copy attributes
    if data is not None:
        dset = dest_group.create_dataset(
            dataset.name.split('/')[-1],
            data=data,
            compression=compression
        )
        copy_attrs(dataset, dset)


def write_process_group(source_group, dest_group, row_indices, col_indices, batch_size = 1000):
    """
    Processes and copies data from a source HDF5 group to a destination HDF5 group,
    handling different encoding types and structures.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        dest_group (h5py.Group): The destination HDF5 group to write the processed data.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        batch_size (int, optional): The size of the batches for processing. Defaults to 1000.
    """
    parent_encoding_type = source_group.attrs.get('encoding-type', None)
    if parent_encoding_type == 'csr_matrix':
        write_process_matrix(
            source_group,
            dest_group,
            row_indices,
            col_indices,
            batch_size,
            is_csr=True
        )
    elif parent_encoding_type == 'csc_matrix':
        write_process_matrix(
            source_group,
            dest_group,
            row_indices,
            col_indices,
            batch_size,
            is_csr=False
        )
    elif parent_encoding_type == 'categorical':
        write_process_categorical_group(source_group, dest_group, row_indices, col_indices)
    elif 'obsp' in source_group.name:
        write_process_obsp_group(source_group, dest_group, row_indices, batch_size)
    elif 'varp' in source_group.name:
        write_process_varp_group(source_group, dest_group, col_indices, batch_size)
    else:
        for key in source_group.keys():
            item = source_group[key]

            if isinstance(item, h5py.Dataset):
                write_process_dataset(
                    item,
                    dest_group,
                    row_indices,
                    col_indices,
                    parent_encoding_type,
                    source_group.name
                )
            elif isinstance(item, h5py.Group):
                if key not in dest_group:
                    new_group = dest_group.create_group(key)
                else:
                    new_group = dest_group[key]
                copy_attrs(item, new_group)
                if source_group.name == '/raw':
                    write_process_raw_group(item, new_group, row_indices, batch_size)
                else:
                    write_process_group(item, new_group, row_indices, col_indices, batch_size)


def write_slice_h5ad(
        source_file_path,
        dest_file_path,
        rows: slice,
        cols: slice,
        memory_fraction: float = 0.1
):
    """
    Slices specified rows and columns from an HDF5-stored AnnData object and writes them
    to a new HDF5 file.

    Args:
        source_file_path (str): The file path to the source HDF5 file.
        dest_file_path (str): The file path to the destination HDF5 file.
        rows (slice): The slice object specifying the row indices to extract.
        cols (slice): The slice object specifying the column indices to extract.
        memory_fraction (float, optional): The fraction of available memory to use for the
            batch size. Defaults to 0.1.

    Raises:
        ValueError: If no rows or columns are available to slice.
    """
    with h5py.File(source_file_path, 'r') as f_src, h5py.File(dest_file_path, 'w') as f_dest:
        # Get the total number of rows and columns
        num_rows = f_src['X'].attrs['shape'][0]
        num_cols = f_src['X'].attrs['shape'][1]

        # Generate row and column indices based on the slice objects
        row_indices = np.arange(
            rows.start or 0,
            rows.stop if rows.stop is not None else num_rows,
            rows.step or 1
        )
        col_indices = np.arange(
            cols.start or 0,
            cols.stop if cols.stop is not None else num_cols,
            cols.step or 1
        )

        # Ensure indices are within bounds
        row_indices = row_indices[row_indices < num_rows]
        col_indices = col_indices[col_indices < num_cols]

        if len(row_indices) == 0 or len(col_indices) == 0:
            raise ValueError("No rows or columns to slice")

        # Calculate batch size based on available memory and data type size
        dtype_size = f_src['X/data'].dtype.itemsize
        batch_size = calculate_batch_size(memory_fraction, len(col_indices), dtype_size)

        # Iterate through all items in the source file
        for key in f_src.keys():
            item = f_src[key]

            if isinstance(item, h5py.Group):
                if key == 'uns':
                    # Copy 'uns' group directly
                    f_src.copy(key, f_dest)
                else:
                    # Create or get the destination group
                    if key not in f_dest:
                        new_group = f_dest.create_group(key)
                    else:
                        new_group = f_dest[key]
                    copy_attrs(item, new_group)
                    write_process_group(item, new_group, row_indices, col_indices, batch_size)
            elif isinstance(item, h5py.Dataset):
                write_process_dataset(item, f_dest, row_indices, col_indices)
