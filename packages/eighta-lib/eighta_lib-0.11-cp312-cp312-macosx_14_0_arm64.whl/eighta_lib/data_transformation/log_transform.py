import h5py
import numpy as np
import psutil
from scipy.sparse import *

from ..file_management import update_h5ad

# TODO: handle csr, csc, np_array format


def log_transform(
    filepath,
    inner_directory,
):
    with h5py.File(filepath, "r") as f:
        attrs = f[inner_directory].attrs

        # Determine the type
        encoding_type = attrs.get("encoding-type")

    match encoding_type:
        case "csr_matrix":
            log_transform_csr_csc(filepath, inner_directory)
        case "csc_matrix":
            log_transform_csr_csc(filepath, inner_directory)
        case "array":
            log_transform_array(filepath, inner_directory)
        case _:
            raise ValueError("Invalid encoding to apply log transform")


def log_transform_csr_csc(filepath, inner_directory):
    with h5py.File(filepath, "r+") as f:
        data = f[inner_directory]["data"]
        indptr = f[inner_directory]["indptr"]

        for i in range(0, len(indptr)):
            if i + 1 < len(indptr):
                data[indptr[i]: indptr[i + 1]] = np.log1p(
                    data[indptr[i]: indptr[i + 1]]
                )
            else:
                data[indptr[i]:] = np.log1p(data[indptr[i]:])


def log_transform_array(filepath, inner_directory):
    with h5py.File(filepath, "r+") as f:
        data = f[inner_directory]
        shape = f[inner_directory].shape
        for i in range(shape[0]):
            data[i] = np.log1p(data[i])
