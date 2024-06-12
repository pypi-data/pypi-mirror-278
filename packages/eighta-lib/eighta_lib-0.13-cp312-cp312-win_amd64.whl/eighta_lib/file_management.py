"""
This module provides functions to update, pop, and partially load data from an HDF5 file.
This is useful for interacting with .h5ad files without loading the entire file as 
an AnnData object in memory. 
"""
import subprocess
import os
from collections import OrderedDict
import h5py
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix
from scipy.sparse import issparse
import anndata as ad

def update_h5ad(
    file_path: str, key: str, data, compression: str = None, repack: bool = True
):
    """
    Update the data at the specified key in the HDF5 file. If the key does not exist, 
    it will be created. Otherwise, the data will be overwritten.

    Parameters:
    - file_path (str): Path to the HDF5 file.
    - key (str): The key specifying the location of the data to update.
    - data: The data to be updated.
    - compression (str): The compression algorithm to use. Default is None.
    - repack (bool): Whether to repack the file after updating. This can retrieve unused space in 
    the file. Default is True.
    """

    def validate_compatibility(
        file: h5py.File, key: str, data, is_in_df: bool, df_group: str
    ):
        """
        Validate that the data is compatible with the key.

        Parameters:
        - file (h5py.File): The HDF5 file object.
        - keys (list[str]): The components of the key.
        - data: The data to be updated.
        - is_in_df (bool): Whether the data is being appended to a DataFrame.
        - df_group (str): The group in which the DataFrame is stored.
        """
        # Check if the key is a column in a DataFrame
        keys = key.split("/")
        # Overwrite the root-level group
        if len(keys) == 1:
            if key not in file and key != "raw":
                raise KeyError(f"Key {key} not found in the .h5ad file.")
            if key == "X":
                validate_shape(data, (num_obs, num_var))
            # If the key is a DataFrame, validate the shape of the DataFrame
            elif key in ["obs", "var"] and isinstance(data, pd.DataFrame):
                validate_shape(data, (num_obs if key == "obs" else num_var,))
            # If the key is a dictionary, validate the shape of the dictionary
            elif key in [
                "obsm",
                "varm",
                "obsp",
                "varp",
                "layers",
                "uns",
            ] and isinstance(data, dict):
                # Different keys have different shapes
                if key in ["obsp", "varp", "layers"]:
                    row_shape = num_var if key == "varp" else num_obs
                    col_shape = num_obs if key == "obsp" else num_var
                    validate_dict_shape(data, (row_shape, col_shape))
                elif key in ["obsm", "varm"]:
                    row_shape = num_obs if key == "obsm" else num_var
                    validate_dict_shape(data, (row_shape,))
                # No shape validation needed for uns
                else:
                    pass
            # Update the raw data, no shape validation needed, but requires AnnData object or
            # .h5ad file
            elif key == "raw" and (
                isinstance(data, ad.AnnData)
                or (isinstance(data, str) and data.endswith(".h5ad"))
            ):
                pass
            else:
                raise KeyError(
                    "Cannot append to this location with the given data type."
                )
        # Overwrite a nested group or dataset
        else:
            # Only one level of nesting is allowed for these keys, otherwise it cannot be read
            # as an AnnData object
            if keys[0] in ["obsm", "varm", "obsp", "varp", "layers"] and len(keys) > 2:
                raise KeyError(
                    "Cannot append to this location. Only one level of nesting is allowed "
                    "for this key."
                )

            if keys[0] in ["obs", "var"]:
                validate_shape(data, (num_obs, 1) if keys[0] == "obs" else (num_var,))
            elif keys[0] == "obsm":
                validate_shape(data, (num_obs,))
                # If the data is being appended to a DataFrame, need to validate the row names
                if isinstance(data, pd.DataFrame):
                    obs_names = file["obs"][file["obs"].attrs["_index"]][:]
                    # Decode the byte strings to utf-8
                    expected_row_names = (
                        [str(name, "utf-8") for name in obs_names]
                        if np.issubdtype(obs_names.dtype, np.object_)
                        else obs_names
                    )
                    # Validate the row names of the DataFrame, should match the index names of
                    # the obs group
                    validate_dataframe_row_names(data, expected_row_names)
            elif keys[0] == "varm":
                validate_shape(data, (num_var,))
                # If the data is being appended to a DataFrame, need to validate the row names
                if isinstance(data, pd.DataFrame):
                    var_names = file["var"][file["var"].attrs["_index"]][:]
                    # Decode the byte strings to utf-8
                    expected_row_names = (
                        [str(name, "utf-8") for name in var_names]
                        if np.issubdtype(var_names.dtype, np.object_)
                        else var_names
                    )
                    # Validate the row names of the DataFrame, should match the index names of
                    # the var group
                    validate_dataframe_row_names(data, expected_row_names)
            elif keys[0] == "obsp":
                validate_shape(data, (num_obs, num_obs))
            elif keys[0] == "varp":
                validate_shape(data, (num_var, num_var))
            elif keys[0] == "layers":
                validate_shape(data, (num_obs, num_var))
            elif keys[0] == "uns":
                # If the data is being appended to a DataFrame, check if the shape matches
                # the dataframe shape
                if is_in_df:
                    validate_shape(
                        data, (file[df_group][file[df_group].attrs["_index"]].shape[0],)
                    )
            elif keys[0] == "raw" and len(keys) != 2:
                if "raw/X" not in file:
                    raise KeyError("Key 'raw' not found in the .h5ad file.")
                # Infer the shape of the data from the X matrix
                _, num_raw_var = file["raw/X"].attrs["shape"]
                if keys[1] == "var":
                    if isinstance(data, pd.DataFrame):
                        raise ValueError("Cannot append a DataFrame to this location.")
                    validate_shape(data, (num_raw_var, 1))
                elif keys[1] == "varm":
                    validate_shape(data, (num_raw_var,))
                    # If the data is being appended to a DataFrame, need to validate the row names
                    if isinstance(data, pd.DataFrame):
                        raw_var_names = file["raw/var"][
                            file["raw/var"].attrs["_index"]
                        ][:]
                        # Decode the byte strings to utf-8
                        expected_row_names = (
                            [str(name, "utf-8") for name in raw_var_names]
                            if np.issubdtype(raw_var_names.dtype, np.object_)
                            else raw_var_names
                        )
                        # Validate the row names of the DataFrame, should match the index names of
                        # the raw/var group
                        validate_dataframe_row_names(data, expected_row_names)
                else:
                    raise KeyError("Cannot append to this location.")
            else:
                raise KeyError("Cannot append to this location.")

    def validate_shape(data, expected_shape: tuple):
        """
        Validate the shape of the data against the expected shape.

        Parameters:
        - data: The data to validate.
        - expected_shape (tuple): The expected shape of the data.
        """
        if isinstance(data, list):
            # expected_shape should be (len(data), 1) or (len(data),)
            if len(data) != expected_shape[0] or (
                len(expected_shape) > 1 and expected_shape[1] != 1
            ):
                raise ValueError(
                    f"List length {len(data)} does not match expected shape {expected_shape}."
                )
        else:
            if data.shape[0] != expected_shape[0]:
                raise ValueError(
                    f"Data shape {data.shape} does not match expected shape {expected_shape}."
                )
            if len(expected_shape) > 1:
                if (len(data.shape) == 1 and expected_shape[1] != 1) or (
                    len(data.shape) > 1 and data.shape[1] != expected_shape[1]
                ):
                    raise ValueError(
                        f"Data shape {data.shape} does not match expected shape {expected_shape}."
                    )

    def validate_dict_shape(data_dict: dict, expected_shape: tuple):
        """
        Validate the shape of the dictionary against the expected shape.

        Parameters:
        - data_dict (dict): The dictionary to validate.
        - expected_shape (tuple): The expected shape of the dictionary.
        """
        for _, value in data_dict.items():
            validate_shape(value, expected_shape)

    def validate_dataframe_row_names(df: pd.DataFrame, expected_names: list):
        """
        Validate the row names of the DataFrame against the expected names.

        Parameters:
        - df (pd.DataFrame): The DataFrame to validate.
        - expected_names (list): The expected row names.
        """
        if not df.index.equals(pd.Index(expected_names)):
            raise ValueError(
                f"DataFrame row names {df.index.to_list()} do not match expected names "
                f"{expected_names}."
            )

    # Split the key into its components
    keys = key.split("/")
    with h5py.File(file_path, "a") as f:
        # Infer the shape of the data from the X matrix
        if isinstance(f["X"], h5py.Dataset):
            num_obs, num_var = f["X"].shape
        else:
            num_obs, num_var = f["X"].attrs["shape"]
        # If data is a pandas Series, convert it to a numpy array
        if isinstance(data, pd.Series):
            data = data.values
        # If data is a pandas DataFrame and we are updating to a key in 'obsp', 'varp', or
        # 'layers', convert it to a numpy array
        if isinstance(data, pd.DataFrame):
            if key == "X":
                data = data.to_numpy()
            elif len(keys) > 1:
                if keys[0] in ["obsp", "varp", "layers"]:
                    data = data.to_numpy()
                elif keys[0] in ["obs", "var"] and data.shape[1] == 1:
                    data = data.to_numpy().flatten()

        if isinstance(data, dict) and key in ["obsp", "varp", "layers"]:
            for key_dict, value in data.items():
                if isinstance(value, pd.DataFrame):
                    data[key_dict] = value.to_numpy()
        # Check if the key is a column in a DataFrame
        is_in_df, df_group, df_col = in_dataframe(f, key)

        # If the data is a scalar and we append it to a DataFrame, repeat it to match the shape of
        # the DataFrame
        if isinstance(data, (bool, str, int, float, complex)):
            if is_in_df:
                data = np.repeat(
                    data, f[df_group][f[df_group].attrs["_index"]].shape[0]
                )

        # Validate the compatibility of the data with the key
        validate_compatibility(f, key, data, is_in_df, df_group)

        is_deleted = False
        if key in f:
            del f[key]
            is_deleted = True

    # Cannot repack during append mode
    if is_deleted and repack:
        repack_file(file_path)

    with h5py.File(file_path, "a") as f:
        # Perform the update
        deep_update(f, keys, data, compression=compression)

        # Update column-order after a successful deep_update
        if is_in_df:
            if is_deleted:
                # Delete all the columns starting with the same prefix
                column_order = [col if isinstance(col, str) else str(col, "utf-8") 
                                for col in f[df_group].attrs["column-order"]]
                f[df_group].attrs["column-order"] = np.array(
                    [col for col in column_order if not col.startswith(df_col)], dtype="S")
            f[df_group].attrs["column-order"] = np.array(
                np.append(f[df_group].attrs["column-order"], df_col), dtype=h5py.special_dtype(vlen=str)
            )


def in_dataframe(file: h5py.Group, key: str):
    """
    Check if the key is a column in a DataFrame in the HDF5 file.

    Parameters:
    - file (h5py.Group): The HDF5 file to check.
    - key (str): The key to check.

    Returns:
    - bool: A boolean indicating whether the key is a column in a DataFrame.
    - str: The name of the DataFrame group if the key is a column in a DataFrame.
    - str: The name of the column if the key is a column in a DataFrame.
    """
    keys = key.split("/")
    # The last key is the column name
    column_name = keys.pop()
    # One level up is the group name
    current_group = "/".join(keys)
    # Check if the key is or is going to be a column in a DataFrame
    while current_group and (
        current_group not in file or "encoding-type" not in file[current_group].attrs
    ):
        # One level up is the new column name
        column_name = f"{keys.pop()}/{column_name}"
        current_group = "/".join(keys)
    if current_group and file[current_group].attrs["encoding-type"] == "dataframe":
        return True, current_group, column_name
    return False, None, None


def deep_update(file: h5py.Group, keys: list[str], data, compression: str = None):
    """
    Recursively updates the data at the specified key in the HDF5 file.

    Parameters:
    - file (h5py.Group): The HDF5 group to update.
    - keys (list): A list of keys specifying the location of the data to update.
    - data: The data to be updated.
    - compression (str): The compression algorithm to use. Default is None.
    - repack (bool): Whether to repack the file after updating. This can retrieve unused space 
    in the file. Default is True.
    """

    def create_anndata_group(
        file: h5py.Group, name: str, data: ad.AnnData, compression: str = None
    ):
        """
        Create a new group in the HDF5 file to store an AnnData object.

        Parameters:
        - file (h5py.Group): The parent group in the HDF5 file.
        - name (str): The name of the new group.
        - data (ad.AnnData): The AnnData object to be stored in the new group.
        - compression (str): The compression algorithm to use.
        """
        anndata_group = file.create_group(name)
        anndata_group.attrs.update(
            {"encoding-type": "anndata", "encoding-version": "0.1.0"}
        )
        # Extract all the root-level components of the AnnData object
        if issparse(data.X):
            create_sparse_matrix_group(
                anndata_group, "X", data.X, compression=compression
            )
        else:
            create_dataset(anndata_group, "X", data.X, "array", compression=compression)
        create_dataframe_group(anndata_group, "obs", data.obs, compression=compression)
        create_dataframe_group(anndata_group, "var", data.var, compression=compression)
        create_dict_group(anndata_group, "obsm", data.obsm, compression=compression)
        create_dict_group(anndata_group, "varm", data.varm, compression=compression)
        create_dict_group(anndata_group, "obsp", data.obsp, compression=compression)
        create_dict_group(anndata_group, "varp", data.varp, compression=compression)
        create_dict_group(anndata_group, "layers", data.layers, compression=compression)
        create_dict_group(anndata_group, "uns", data.uns, compression=compression)
        if data.raw is not None:
            create_raw_group(anndata_group, "raw", data.raw, compression=compression)

    def create_raw_group(
        file: h5py.Group, name: str, data: ad.AnnData | ad.Raw, compression: str = None
    ):
        """
        Create a new raw group in the HDF5 file.

        Parameters:
        - file (h5py.Group): The parent group in the HDF5 file.
        - keys (list[str]): The components of the key.
        - data: The data to be stored in the raw group.
        - compression (str): The compression algorithm to use.
        """
        # raw group is a special case, it is a group with X, var, and varm datasets of
        # the AnnData object
        raw_group = file.create_group(name)
        raw_group.attrs.update({"encoding-type": "raw", "encoding-version": "0.1.0"})
        # Extract the X, var, and varm datasets from the AnnData object
        if issparse(data.X):
            create_sparse_matrix_group(raw_group, "X", data.X, compression=compression)
        else:
            create_dataset(raw_group, "X", data.X, "array", compression=compression)
        create_dataframe_group(raw_group, "var", data.var, compression=compression)
        create_dict_group(raw_group, "varm", data.varm, compression=compression)

    def create_dataset(
        group: h5py.Group,
        name: str,
        data,
        encoding_type: str,
        encoding_version: str = "0.2.0",
        dtype: np.dtypes = None,
        compression: str = None,
    ):
        """
        Helper function to create a dataset in the HDF5 file.

        Parameters:
        - group (h5py.Group): The HDF5 group to create the dataset in.
        - name (str): The name of the dataset.
        - data: The data to be stored in the dataset.
        - encoding_type (str): The encoding type of the dataset.
        - encoding_version (str): The encoding version of the dataset.
        - dtype: The data type of the dataset.
        - compression (str): The compression algorithm to use.
        """
        # If the string array has duplicates, convert it to a categorical
        if (
            isinstance(data, np.ndarray)
            and len(data.shape) == 1
            and np.issubdtype(data.dtype, np.str_)
            and len(data) != len(np.unique(data))
        ):
            # ordered=False to match the behavior of the AnnData object
            data = pd.Categorical(data, ordered=False)
        # Create categorical group
        if isinstance(data, pd.Categorical):
            new_group = group.create_group(name)
            new_group.attrs.update(
                {
                    "encoding-type": "categorical",
                    "encoding-version": encoding_version,
                    "ordered": data.ordered,
                }
            )
            data_type = (
                np.object_
                if data.categories.dtype == h5py.special_dtype(vlen=str)
                else None
            )
            encoding_type = "string-array" if data_type == np.object_ else "array"
            create_dataset(
                new_group,
                "categories",
                data.categories,
                encoding_type,
                dtype=data_type,
                compression=compression,
            )
            create_dataset(
                new_group, "codes", data.codes, "array", compression=compression
            )
        # Create regular dataset
        else:
            if np.issubdtype(dtype, np.object_):
                dtype = h5py.special_dtype(vlen=str)
                data = np.array(data, dtype="S")
            group.create_dataset(name, data=data, dtype=dtype, compression=compression)
            group[name].attrs.update(
                {"encoding-type": encoding_type, "encoding-version": encoding_version}
            )

    def create_dataframe_group(
        group: h5py.Group, name: str, data: pd.DataFrame, compression: str = None
    ):
        """
        Create a new group in the HDF5 file to store a DataFrame.

        Parameters:
        - group (h5py.Group): The parent group in the HDF5 file.
        - name (str): The name of the new group.
        - data (pd.DataFrame): The DataFrame to be stored in the new group.
        - compression (str): The compression algorithm to use.
        """
        index_name = data.index.name if data.index.name is not None else "_index"
        new_group = group.create_group(name)
        # Convert all the column names to strings
        data.columns = data.columns.astype(str)
        # Add metadata
        new_group.attrs.update(
            {
                "_index": index_name,
                "column-order": np.array(
                    data.columns, dtype=h5py.special_dtype(vlen=str)
                ),
                "encoding-type": "dataframe",
                "encoding-version": "0.2.0",
            }
        )
        # If the index is a string, use a variable-length string type which can be accepted by
        # h5py create_dataset function, they are equivalent.
        index_dtype = (
            h5py.special_dtype(vlen=str)
            if np.issubdtype(data.index.dtype, np.object_)
            else None
        )
        new_group.create_dataset(
            index_name,
            data=data.index.values,
            dtype=index_dtype,
            compression=compression,
        )
        new_group[index_name].attrs.update(
            {
                "encoding-type": "string-array"
                if index_dtype == h5py.special_dtype(vlen=str)
                else "array",
                "encoding-version": "0.2.0",
            }
        )
        for col in data.columns:
            col_data = data[col].values
            col_dtype = (
                np.object_
                if isinstance(col_data, pd.Categorical)
                and col_data.categories.dtype == h5py.special_dtype(vlen=str)
                or col_data.dtype == np.object_
                else None
            )
            create_dataset(
                new_group,
                col,
                col_data,
                "string-array" if col_dtype == np.object_ else "array",
                dtype=col_dtype,
                compression=compression,
            )

    def create_dict_group(
        group: h5py.Group, name: str, data: dict, compression: str = None
    ):
        """
        Create a new group in the HDF5 file to store a dictionary.

        Parameters:
        - group (h5py.Group): The parent group in the HDF5 file.
        - name (str): The name of the new group.
        - data (dict): The dictionary to be stored in the new group.
        - compression (str): The compression algorithm to use.
        """
        new_group = group.create_group(name)
        new_group.attrs.update({"encoding-type": "dict", "encoding-version": "0.1.0"})
        for key, value in data.items():
            # Handle different data types
            if isinstance(value, (bool, int, float, complex)):
                create_dataset(
                    new_group,
                    key,
                    np.array(value),
                    "numeric-scalar",
                    compression=compression,
                )
            elif isinstance(value, str):
                create_dataset(new_group, key, value, "string", compression=compression)
            elif isinstance(value, pd.DataFrame):
                create_dataframe_group(new_group, key, value, compression=compression)
            elif isinstance(value, dict):
                create_dict_group(new_group, key, value, compression=compression)
            elif isinstance(value, list):
                # Handle list of strings
                if any(isinstance(i, str) for i in value):
                    # Convert all elements to strings
                    str_value = np.array(value, dtype="S")
                    create_dataset(
                        new_group,
                        key,
                        str_value,
                        "string-array",
                        dtype=np.object_,
                        compression=compression,
                    )
                # Handle list of numbers
                elif all(isinstance(i, (bool, int, float, complex)) for i in value):
                    create_dataset(
                        new_group,
                        key,
                        np.array(value),
                        "array",
                        compression=compression,
                    )
                else:
                    raise TypeError(f"Unsupported list type in key {key}.")
            elif isinstance(value, np.ndarray):
                # Handle array of strings
                if np.issubdtype(value.dtype, np.object_) or np.issubdtype(
                    value.dtype, np.str_
                ):
                    create_dataset(
                        new_group,
                        key,
                        value,
                        "string-array",
                        dtype=np.object_,
                        compression=compression,
                    )
                else:
                    create_dataset(
                        new_group, key, value, "array", compression=compression
                    )
            elif isinstance(value, pd.Categorical):
                if np.issubdtype(value.categories.dtype, np.object_) or np.issubdtype(
                    value.categories.dtype, np.str_
                ):
                    create_dataset(
                        new_group, key, value, "string-array", compression=compression
                    )
                else:
                    create_dataset(
                        new_group, key, value, "array", compression=compression
                    )
            elif isinstance(value, ad.AnnData):
                create_anndata_group(new_group, key, value, compression=compression)
            elif isinstance(value, ad.Raw):
                create_raw_group(new_group, key, value, compression=compression)
            else:
                raise TypeError(f"Unsupported data type {type(value)} for key {key}.")

    def create_sparse_matrix_group(
        group: h5py.Group, name: str, data, compression: str = None
    ):
        """
        Create a new group in the HDF5 file to store a sparse matrix.

        Parameters:
        - group (h5py.Group): The parent group in the HDF5 file.
        - name (str): The name of the new group.
        - data: The sparse matrix to be stored in the new group.
        """
        if isinstance(data, (csr_matrix, csc_matrix)):
            sparse_group = group.create_group(name)
            sparse_group.create_dataset("data", data=data.data, compression=compression)
            sparse_group.create_dataset(
                "indices", data=data.indices, compression=compression
            )
            sparse_group.create_dataset(
                "indptr", data=data.indptr, compression=compression
            )
            sparse_group.attrs.update(
                {
                    "shape": data.shape,
                    "encoding-type": "csr_matrix"
                    if isinstance(data, csr_matrix)
                    else "csc_matrix",
                    "encoding-version": "0.1.0",
                }
            )
        else:
            raise TypeError(f"Unsupported sparse matrix format {type(data)}.")

    # Base case
    if len(keys) == 1:
        if issparse(data):
            # Handle csr_matrix or csc_matrix
            create_sparse_matrix_group(file, keys[0], data, compression=compression)
        elif isinstance(data, ad.AnnData):
            # If we are updating to 'raw' with an AnnData object, we need to create a raw group
            if len(keys) == 1 and keys[0] == "raw":
                create_raw_group(file, keys[0], data, compression=compression)
            else:
                create_anndata_group(file, keys[0], data, compression=compression)
        elif isinstance(data, ad.Raw):
            create_raw_group(file, keys[0], data, compression=compression)
        # Copying raw data from another file
        # Since it already has the correct postfix '.h5ad'(We checked in update_h5ad),
        # we can just copy the X, var, and varm datasets directly
        elif keys[0] == "raw" and isinstance(data, str):
            raw_group = file.create_group("raw")
            raw_group.attrs.update(
                {"encoding-type": "raw", "encoding-version": "0.1.0"}
            )
            with h5py.File(data, "r") as f:
                f.copy("X", raw_group)
                f.copy("var", raw_group)
                f.copy("varm", raw_group)
        elif isinstance(data, list):
            # Handle list of strings
            if any(isinstance(i, str) for i in data):
                str_data = np.array(data, dtype="S")
                create_dataset(
                    file,
                    keys[0],
                    str_data,
                    "string-array",
                    dtype=np.object_,
                    compression=compression,
                )
            # Handle list of numbers
            elif all(isinstance(i, (bool, int, float, complex)) for i in data):
                create_dataset(
                    file, keys[0], np.array(data), "array", compression=compression
                )
            else:
                raise TypeError(f"Unsupported list type in key {keys[0]}.")
        elif isinstance(data, (bool, int, float, np.bool_)):
            create_dataset(
                file, keys[0], data, "numeric-scalar", compression=compression
            )
        elif isinstance(data, str):
            create_dataset(file, keys[0], data, "string", compression=compression)
        elif isinstance(data, pd.Categorical):
            # Handle categorical data
            # If the categories are strings, annotate the categories as string-array
            if np.issubdtype(data.categories.dtype, np.object_) or np.issubdtype(
                data.categories.dtype, np.str_
            ):
                create_dataset(
                    file, keys[0], data, "string-array", compression=compression
                )
            else:
                create_dataset(file, keys[0], data, "array", compression=compression)
        elif isinstance(data, np.ndarray):
            # if data is an array of strings
            if np.issubdtype(data.dtype, np.str_):
                create_dataset(
                    file,
                    keys[0],
                    data,
                    "string-array",
                    dtype=np.object_,
                    compression=compression,
                )
            else:
                create_dataset(file, keys[0], data, "array", compression=compression)
        elif isinstance(data, pd.DataFrame):
            create_dataframe_group(file, keys[0], data, compression=compression)
        elif isinstance(data, dict):
            # Handle dictionary
            create_dict_group(file, keys[0], data, compression=compression)
        else:
            raise TypeError(
                f"Unsupported data type {type(data)} for key {keys[0]}. We need to implement this "
                "if needed."
            )
    else:
        if keys[0] not in file:
            file.create_group(keys[0])
        # Recursively update the next level
        deep_update(file[keys[0]], keys[1:], data, compression=compression)


def pop_h5ad(file_path: str, key: str, repack: bool = True):
    """
    Remove the data at the specified key in the HDF5 file and return it.

    Parameters:
    - file_path (str): Path to the HDF5 file.
    - target (str): The key specifying the location of the data to remove.
    - repack (bool): Whether to repack the file after removing the data. Defaults to True.

    Returns:
    - The data that was removed.
    """
    keys = key.split("/")
    # We do not allow removing the whole X/obs/var group
    if len(keys) < 2 and key not in [
        "obsm",
        "varm",
        "obsp",
        "varp",
        "uns",
        "layers",
        "raw",
    ]:
        raise KeyError(f"Invalid target key {key}. Cannot remove from this location.")

    with h5py.File(file_path, "a") as f:
        # Check if the target exists in the file
        if key not in f:
            raise KeyError(f"{key} not found in the .h5ad file.")

        # We do not allow removing the whole raw/var group
        if key in ["raw/var", "raw/X"]:
            raise KeyError(
                f"Cannot remove the whole {key} group. Please specify a column to remove."
            )

        if "encoding-type" in f[key].parent.attrs and f[key].parent.attrs[
            "encoding-type"
        ] in ["categorical", "csr_matrix", "csc_matrix"]:
            raise KeyError(
                f"Cannot remove {key}. Please remove the whole parent group instead."
            )

        # Check if the target is a column in a DataFrame
        is_in_df, df_group, df_col = in_dataframe(f, key)
        # Load the data before deleting it
        ret = load_h5ad(f[key])

        # If the target is a column in a DataFrame
        if is_in_df:
            # Return a pd.Series with the corresponding indices
            # Indices needs to be converted to a list of strings
            indices = [
                x.decode("utf-8") for x in f[df_group][f[df_group].attrs["_index"]][:]
            ]
            # Return the data as a pd.Series with the corresponding indices
            ret = pd.Series(
                ret,
                index=pd.Index(
                    indices,
                    name=f[df_group].attrs["_index"]
                    if f[df_group].attrs["_index"] != "_index"
                    else None,
                ),
                name=df_col,
            )

            if df_col not in f[df_group].attrs["column-order"]:
                raise KeyError(f"{df_col} not found in the {df_group} group.")
            # Remove the column from the column-order
            f[df_group].attrs["column-order"] = [
                col for col in f[df_group].attrs["column-order"] if col != df_col
            ]

        # Delete the target dataset or group
        del f[key]

        # Check if we need to delete any upper-level empty groups
        group_components = keys[:-1]
        group_path = "/".join(group_components)
        while (
            group_components
            and isinstance(f[group_path], h5py.Group)
            and "encoding-type" not in f[group_path].attrs
            and len(f[group_path]) == 0
        ):
            # Delete the empty group
            del f[group_path]
            # Move up one level
            group_components.pop()
            group_path = "/".join(group_components)

        # If we deleted a root-level group, we need to make a new empty group
        if key in ["obsm", "varm", "obsp", "varp", "uns", "layers", "raw/varm"]:
            group = (
                f["raw"].create_group("varm")
                if key == "raw/varm"
                else f.create_group(key)
            )
            group.attrs.update({"encoding-type": "dict", "encoding-version": "0.1.0"})
    # Repack the file to reclaim space
    if repack:
        repack_file(file_path)

    return ret


def load_h5ad(target: h5py.Group | h5py.Dataset, exclude: list[str] = None):
    """
    Load the data from the HDF5 file at the specified target location.

    Parameters:
    - target (h5py.Group | h5py.Dataset): The target location in the HDF5 file.

    Returns:
    - The data loaded from the HDF5 file.
    """
    # If the target is in the exclude list, return None
    ret = None

    if exclude is None or target.name not in exclude:
        if isinstance(target, h5py.Dataset):
            # We need to explicitly convert to string if the encoding-type is string/string-array
            if target.shape == ():  # scalar
                ret = (
                    str(target[()], "utf-8")
                    if target.attrs["encoding-type"] == "string"
                    else target[()]
                )
            else:  # array
                ret = (
                    np.array([str(val, "utf-8") for val in target[:]], dtype=object)
                    if target.attrs["encoding-type"] == "string-array"
                    else target[:]
                )
        else:
            # Load encoded group
            if "encoding-type" in target.attrs:
                # CSR matrix
                if target.attrs["encoding-type"] == "csr_matrix":
                    ret = csr_matrix(
                        (target["data"][:], target["indices"][:], target["indptr"][:]),
                        shape=target.attrs["shape"],
                    )
                # CSC matrix
                elif target.attrs["encoding-type"] == "csc_matrix":
                    ret = csc_matrix(
                        (target["data"][:], target["indices"][:], target["indptr"][:]),
                        shape=target.attrs["shape"],
                    )
                # Categorical data
                elif target.attrs["encoding-type"] == "categorical":
                    if target["categories"].attrs["encoding-type"] == "string-array":
                        categories = [
                            str(cat, "utf-8") for cat in target["categories"][:]
                        ]
                    else:
                        categories = target["categories"][:]
                    ret = pd.Categorical.from_codes(target["codes"][:], categories)
                # DataFrame
                elif target.attrs["encoding-type"] == "dataframe":
                    ret = load_dataframe_group(target, exclude=exclude)
                # Dictionary
                elif target.attrs["encoding-type"] == "dict":
                    ret = load_dict_group(target, exclude=exclude)
                elif target.attrs["encoding-type"] in ["raw", "anndata"]:
                    loaded_X = load_h5ad(target["X"], exclude=exclude)
                    # If X is None, create a dummy csc_matrix
                    if loaded_X is None:
                        shape = (
                            target["X"].attrs["shape"]
                            if isinstance(target, h5py.Group)
                            else target.shape
                        )
                        loaded_X = csc_matrix(([], [], np.zeros(shape[1] + 1)), shape=shape)
                    if target.attrs["encoding-type"] == "raw":
                        adata = ad.AnnData(
                            X=loaded_X,
                            var=load_dataframe_group(target["var"], exclude=exclude),
                            varm=load_dict_group(target["varm"], exclude=exclude),
                        )
                        ret = ad.Raw(adata)
                    else:
                        ret = ad.AnnData(
                            X=loaded_X,
                            obs=load_dataframe_group(target["obs"], exclude=exclude),
                            var=load_dataframe_group(target["var"], exclude=exclude),
                            obsm=load_dict_group(target["obsm"], exclude=exclude),
                            varm=load_dict_group(target["varm"], exclude=exclude),
                            obsp=load_dict_group(target["obsp"], exclude=exclude),
                            varp=load_dict_group(target["varp"], exclude=exclude),
                            layers=load_dict_group(target["layers"], exclude=exclude),
                            uns=load_dict_group(target["uns"], exclude=exclude),
                        )
                else:
                    raise NotImplementedError(
                        f"Unknown group type in {target.name}, please contact the developers."
                    )
            # If the group does not have an encoding-type, it is a regular group
            # We do not allow loading regular groups directly
            else:
                raise ValueError("Cannot load a group.")
    return ret


def load_dataframe_group(group: h5py.Group, exclude: list[str] = None):
    """
    Load a DataFrame group from the HDF5 file.

    Parameters:
    - group (h5py.Group): The group containing the DataFrame data.

    Returns:
    - pd.DataFrame: The DataFrame loaded from the HDF5 file.
    """
    index_name = group.attrs["_index"]
    index_data = group[index_name][:]
    if group[index_name].attrs["encoding-type"] == "string-array":
        index_data = [str(val, "utf-8") for val in index_data]
    columns = group.attrs["column-order"]
    # OrderedDict to preserve column order
    data = OrderedDict()
    for col in columns:
        # Only include the specified columns if exclude is None or the column is not in
        # the exclude list
        if exclude is None or f"{group.name}/{col}" not in exclude:
            if isinstance(group[col], h5py.Dataset):
                col_data = group[col][:]
                if group[col].attrs["encoding-type"] == "string-array":
                    col_data = [str(val, "utf-8") for val in col_data]
            else:
                if group[col].attrs["encoding-type"] == "categorical":
                    categories = group[col]["categories"][:]
                    if (
                        group[col]["categories"].attrs["encoding-type"]
                        == "string-array"
                    ):
                        categories = [str(cat, "utf-8") for cat in categories]
                    col_data = pd.Categorical.from_codes(
                        group[col]["codes"][:], categories
                    )
                elif group[col].attrs["encoding-type"] == "csr_matrix" and (
                    group[col].attrs["shape"][0] == 1
                    or group[col].attrs["shape"][1] == 1
                ):
                    col_data = (
                        csr_matrix(
                            (
                                group[col]["data"][:],
                                group[col]["indices"][:],
                                group[col]["indptr"][:],
                            ),
                            shape=group[col].attrs["shape"],
                        )
                        .toarray()
                        .flatten()
                    )
                elif group[col].attrs["encoding-type"] == "csc_matrix" and (
                    group[col].attrs["shape"][0] == 1
                    or group[col].attrs["shape"][1] == 1
                ):
                    col_data = (
                        csc_matrix(
                            (
                                group[col]["data"][:],
                                group[col]["indices"][:],
                                group[col]["indptr"][:],
                            ),
                            shape=group[col].attrs["shape"],
                        )
                        .toarray()
                        .flatten()
                    )
                else:
                    raise NotImplementedError(
                        f"Unsupported format {group[col].attrs['encoding-type']}."
                    )
            # Add the value to the data dictionary with the column name as the key
            data[col] = col_data

    # If we did not include any data, it is not a root-level and not empty originally group,
    # return None
    if not data and group.name not in ["/obs", "/var"] and len(columns) > 0:
        return None
    # Create the DataFrame from the data dictionary
    # Set the index name if it is not the default '_index'
    df = pd.DataFrame(
        data,
        index=pd.Index(index_data, name=index_name if index_name != "_index" else None),
    )
    return df


def load_dict_group(group: h5py.Group, exclude: list[str] = None):
    """
    Load a dictionary group from the HDF5 file.

    Parameters:
    - group (h5py.Group): The group containing the dictionary data.

    Returns:
    - dict: The dictionary loaded from the HDF5 file.
    """
    data = {}
    for key, value in group.items():
        # Load the data only if it is not in the exclude list
        if exclude is None or f"{group.name}/{key}" not in exclude:
            # Dataset
            if isinstance(value, h5py.Dataset):
                if value.attrs["encoding-type"] == "numeric-scalar":
                    data[key] = value[()]
                elif value.attrs["encoding-type"] == "string":
                    data[key] = str(value[()], "utf-8")
                elif value.attrs["encoding-type"] == "array":
                    data[key] = value[:]
                elif value.attrs["encoding-type"] == "string-array":
                    data[key] = np.array(
                        [str(val, "utf-8") for val in value[:]], dtype=object
                    )
                else:
                    raise NotImplementedError(
                        f"Unsupported format {value.attrs['encoding-type']}."
                    )
            # Group
            else:
                if value.attrs["encoding-type"] == "dataframe":
                    val = load_dataframe_group(value, exclude=exclude)
                    # If the DataFrame is empty, do not include it
                    if val is not None:
                        data[key] = val
                elif value.attrs["encoding-type"] == "dict":
                    # Recursively load the dictionary
                    val = load_dict_group(value, exclude=exclude)
                    # If the dictionary is empty, do not include it
                    if val is not None:
                        data[key] = val
                elif value.attrs["encoding-type"] == "categorical":
                    if value["categories"].attrs["encoding-type"] == "string-array":
                        categories = [
                            str(cat, "utf-8") for cat in value["categories"][:]
                        ]
                    else:
                        categories = value["categories"][:]
                    data[key] = pd.Categorical.from_codes(value["codes"][:], categories)
                elif value.attrs["encoding-type"] == "csr_matrix":
                    data[key] = csr_matrix(
                        (value["data"][:], value["indices"][:], value["indptr"][:]),
                        shape=value.attrs["shape"],
                    )
                elif value.attrs["encoding-type"] == "csc_matrix":
                    data[key] = csc_matrix(
                        (value["data"][:], value["indices"][:], value["indptr"][:]),
                        shape=value.attrs["shape"],
                    )
                elif value.attrs["encoding-type"] in ["raw", "anndata"]:
                    # Find all paths of this group that can be deserialized
                    all_paths = find_all_deserializable_paths(value)
                    # Include the paths that are in the exclude list
                    group_exclude = (
                        [item for item in all_paths if item in exclude]
                        if exclude is not None
                        else []
                    )
                    if len(group_exclude) < len(all_paths):
                        loaded_X = load_h5ad(value["X"], exclude=group_exclude)
                        # If X is not in the include list, we need to create an empty dummy matrix
                        # with the correct shape
                        if loaded_X is None:
                            shape = (
                                value["X"].attrs["shape"]
                                if isinstance(value, h5py.Group)
                                else value.shape
                            )
                            loaded_X = csc_matrix(
                                ([], [], np.zeros(shape[1] + 1)), shape=shape
                            )
                        if value.attrs["encoding-type"] == "raw":
                            adata = ad.AnnData(
                                X=loaded_X,
                                var=load_dataframe_group(
                                    value["var"], exclude=group_exclude
                                ),
                                varm=load_dict_group(
                                    value["varm"], exclude=group_exclude
                                ),
                            )
                            data[key] = ad.Raw(adata)
                        else:
                            adata = ad.AnnData(
                                X=loaded_X,
                                obs=load_dataframe_group(
                                    value["obs"], exclude=group_exclude
                                ),
                                var=load_dataframe_group(
                                    value["var"], exclude=group_exclude
                                ),
                                obsm=load_dict_group(
                                    value["obsm"], exclude=group_exclude
                                ),
                                varm=load_dict_group(
                                    value["varm"], exclude=group_exclude
                                ),
                                obsp=load_dict_group(
                                    value["obsp"], exclude=group_exclude
                                ),
                                varp=load_dict_group(
                                    value["varp"], exclude=group_exclude
                                ),
                                layers=load_dict_group(
                                    value["layers"], exclude=group_exclude
                                ),
                                uns=load_dict_group(
                                    value["uns"], exclude=group_exclude
                                ),
                            )
                            data[key] = adata
                else:
                    raise NotImplementedError(
                        f"Unsupported format {value.attrs['encoding-type']}."
                    )

    # If we did not include any data, it is not a root-level group and not empty originally,
    # return None
    if (
        not data
        and group.name not in ["/obsm", "/varm", "/obsp", "/varp", "/uns", "/layers"]
        and len(group.items()) > 0
    ):
        return None
    return data


def repack_file(file_path: str):
    """
    Repack the HDF5 file to reclaim space.

    Parameters:
    - file_path (str): Path to the HDF5 file.
    """
    temp_file = file_path + ".temp"
    subprocess.run(["h5repack", file_path, temp_file], check=True)
    os.replace(temp_file, file_path)


def filter_anndata_h5ad(
    file_path: str, include: list[str] = None, exclude: list[str] = None
):
    """
    Filter the data in an HDF5-stored AnnData object and partially load it based on 
    the specified keys. Only able to filter deserializable paths.
    
    Parameters:
    - file_path (str): Path to the HDF5 file.
    - include (list): A list of keys to include in the filtered data.
    - exclude (list): A list of keys to exclude from the filtered data.

    Returns:
    - An AnnData object containing the filtered data.
    """

    if include and exclude:
        raise ValueError("Only one of 'include' or 'exclude' can be used at a time.")

    with h5py.File(file_path, "r") as f:
        # Load the entire dataset if no include/exclude is specified
        if include is None and exclude is None:
            return ad.read_h5ad(file_path)

        path_list = find_all_deserializable_paths(f)

        # Exhaustively exclude all children of the specified keys
        if exclude:
            exclude_list = set()
            for key in exclude:
                if key not in f:
                    raise KeyError(f"Key {key} not found in the .h5ad file.")
                exclude_list.update(get_group_and_children(key, path_list))
            exclude = [item for item in path_list if item in exclude_list]
        # Complement the include list with all children of the specified keys to get
        # the exclude list
        else:
            include_list = set()
            for key in include:
                if key not in f:
                    raise KeyError(f"Key {key} not found in the .h5ad file.")
                include_list.update(get_group_and_children(key, path_list))
            exclude = [item for item in path_list if item not in include_list]

        # Load the whole anndata object if the exclude list is empty
        if not exclude:
            return ad.read_h5ad(file_path)

        # Determine the X matrix
        filtered_X = load_h5ad(f["X"], exclude=exclude)
        # If X is not in the include list, we need to create an empty dummy matrix with
        # the correct shape
        if filtered_X is None:
            shape = (
                f["X"].attrs["shape"]
                if isinstance(f["X"], h5py.Group)
                else f["X"].shape
            )
            filtered_X = csc_matrix(([], [], np.zeros(shape[1] + 1)), shape=shape)

        adata = ad.AnnData(
            X=filtered_X,
            layers=load_dict_group(f["layers"], exclude=exclude),
            obs=load_dataframe_group(f["obs"], exclude=exclude),
            var=load_dataframe_group(f["var"], exclude=exclude),
            obsm=load_dict_group(f["obsm"], exclude=exclude),
            varm=load_dict_group(f["varm"], exclude=exclude),
            obsp=load_dict_group(f["obsp"], exclude=exclude),
            varp=load_dict_group(f["varp"], exclude=exclude),
            uns=load_dict_group(f["uns"], exclude=exclude),
        )

        # Load the raw data if it is in the file and not excluded
        if "raw" in f:
            # Find all the deserializable paths in the raw group
            raw_path_list = find_all_deserializable_paths(f["raw"])
            # The deserializable paths in the raw group that are in the exclude list
            raw_exclude = [item for item in raw_path_list if item in exclude]
            # Load the raw data with the exclude list if any of the raw data is not excluded
            if len(raw_exclude) < len(raw_path_list):
                raw = load_h5ad(f["raw"], exclude=raw_exclude)
                adata.raw = ad.AnnData(X=raw.X, var=raw.var, varm=raw.varm)
        return adata


def get_group_and_children(group: str, group_list: list[str]):
    """
    Get the specified group and all its children from the group list.

    Parameters:
    - group (str): The group to get.
    - group_list (list[str]): A list of groups to search.

    Returns:
    - list[str]: A list of groups and their children, depending on the inclusion or 
    exclusion criteria.
    """
    # Ensure the group name starts with a '/' for uniform and consistent handling across
    # different representations.
    # Example transformation: 'uns/a/b' becomes '/uns/a/b'.
    if not group.startswith("/"):
        group = "/" + group
    return [
        item for item in group_list if item == group or item.startswith(group + "/")
    ]


def find_all_deserializable_paths(h5file: h5py.Group) -> list[str]:
    """
    Recursively find all paths in an HDF5 file that can be deserialized, filtering out
    paths based on certain encoding types and excluding specific datasets.

    Parameters:
    - hdf5_group (h5py.Group): The current HDF5 group to search within.

    Returns:
    - list[str]: A list of all unique paths to deserializable data within the HDF5 file,
           excluding datasets representing indices and children of any non-dictionary or 
           non-dataframe encoded groups, such as children of sparse matrix representation groups 
           and children of categorical groups.
    """
    dataset_paths = []
    for key in h5file.keys():
        full_key = f"{h5file.name}/{key}" if h5file.name != "/" else f"/{key}"
        if isinstance(h5file[key], h5py.Group):
            if "encoding-type" in h5file[key].attrs and h5file[key].attrs[
                "encoding-type"
            ] not in ["dict", "raw", "anndata"]:
                # dataframes we return the columns in the column-order
                if h5file[key].attrs["encoding-type"] == "dataframe":
                    dataset_paths.extend(
                        [
                            f"{full_key}/{col}"
                            for col in h5file[key].attrs["column-order"]
                        ]
                    )
                # for sparse matrices and categorical data, we skip the children
                else:
                    dataset_paths.append(full_key)
            # If the group is a dictionary/raw/anndata/regular group, we recursively search for
            # data paths
            else:
                dataset_paths.extend(find_all_deserializable_paths(h5file[key]))
        # If the key is a dataset, we add it to the list
        else:
            dataset_paths.append(full_key)
    return dataset_paths
