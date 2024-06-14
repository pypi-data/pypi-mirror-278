import h5py
import numpy as np
import pandas as pd


def normalize(filepath, inner_directory):
    with h5py.File(filepath, "r") as f:
        attrs = f[inner_directory].attrs

        # Determine the type
        encoding_type = attrs.get("encoding-type")

    match encoding_type:
        case "csr_matrix":
            normalize_csr(filepath, inner_directory)
        case "csc_matrix":
            normalize_csc(filepath, inner_directory)
        case "array":
            normalize_array(filepath, inner_directory)
        case _:
            raise ValueError("Unsupported Encoding Type for normalization")


def normalize_csr(filepath, inner_directory):
    with h5py.File(filepath, "r+") as f:
        data = f[inner_directory]["data"]
        indptr = f[inner_directory]["indptr"]
        shape = f[inner_directory].attrs.get("shape")

        for i in range(shape[0]):
            row = data[indptr[i]: indptr[i + 1]]
            norm = np.linalg.norm(row)
            if norm != 0:
                data[indptr[i]: indptr[i + 1]] = row / norm


def normalize_csc(filepath, inner_directory):
    with h5py.File(filepath, "r+") as f:
        data = f[inner_directory]["data"]
        indices = f[inner_directory]["indices"]
        shape = f[inner_directory].attrs.get("shape")

        # for each row, calculate its sum and divide
        for i in range(shape[0]):
            mask = indices[:] == i
            row = data[mask]
            norm = np.linalg.norm(row)
            if norm != 0:
                data[mask] = row / norm

def normalize_array(filepath, inner_directory):
    with h5py.File(filepath, "r+") as f:
        data = f[inner_directory]
        shape = f[inner_directory].shape

        if data.ndim < 2:
            norm = np.linalg.norm(data)
            if norm != 0:
                data[:] = data / norm
        else:
            for i in range(shape[0]):
                row = data[i]
                norm = np.linalg.norm(row)
                if norm != 0:
                    data[i] = row / norm
