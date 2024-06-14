import re

import h5py
import numpy as np
import sklearn.preprocessing


def scale(filepath, inner_directory, with_mean: bool = True, with_std: bool = True):
    with h5py.File(filepath, "r") as f:
        attrs = f[inner_directory].attrs

        # Determine the type
        encoding_type = attrs.get("encoding-type")

    match encoding_type:
        case "csr_matrix":
            if with_mean:
                raise ValueError("This breaks the sparsity of the matrix. Use with_mean=False instead")
            scale_csr(filepath, inner_directory, with_std)
        case "csc_matrix":
            if with_mean:
                raise ValueError("This breaks the sparsity of the matrix. Use with_mean=False instead")
            scale_csc(filepath, inner_directory, with_std)
        case "array":
            scale_array(filepath, inner_directory, with_mean, with_std)
        case _:
            raise ValueError("This encoding is not supported")


def scale_array(filepath, inner_directory, with_mean: bool, with_std: bool):
    with h5py.File(filepath, "r+") as f:
        data = f[inner_directory]
        shape = f[inner_directory].shape

        if data.ndim < 2:  # 1D cases (Ex: var or obs)
            print("dim smaller than 2")
            # Center around the mean
            numerator = data - np.nanmean(data) if with_mean else data

            # Get the standard deviation
            denominator = np.nanstd(data) if with_std else 1
            # Prevent divide-by-zero problems
            if np.allclose(denominator, 0):
                print("Oh no, divide by zero!")
                denominator = 1
            data[:] = numerator / denominator
        else:
            for i in range(shape[1]):
                col = data[:, i]

                # Center around the mean
                numerator = col - np.nanmean(col) if with_mean else col

                # Get the standard deviation
                denominator = np.nanstd(col) if with_std else 1
                # Prevent divide-by-zero problems
                if np.allclose(denominator, 0):
                    denominator = 1

                data[:, i] = numerator / denominator


def scale_csc(filepath, inner_directory, with_std: bool):
    with h5py.File(filepath, "r+") as f:
        data = f[inner_directory]["data"]
        indptr = f[inner_directory]["indptr"]
        shape = f[inner_directory].attrs.get("shape")

        if with_std:
            for i in range(0, shape[1]):
                col = data[indptr[i]: indptr[i + 1]]
                std = np.std(np.append(col, np.zeros(shape[0] - col.shape[0])))
                if std != 0:
                    data[indptr[i]: indptr[i + 1]] = col / std


def scale_csr(filepath, inner_directory, with_std: bool):
    with h5py.File(filepath, "r+") as f:
        data = f[inner_directory]["data"]
        indices = f[inner_directory]["indices"]
        shape = f[inner_directory].attrs.get("shape")

        if with_std:
            # for each column, calculate its standard deviation and divide
            for i in range(0, shape[1]):
                mask = indices[:] == i
                arr = data[mask]

                variance = calc_var(arr, shape[0] - np.shape(arr)[0])
                std_dev = np.sqrt(variance)
                if std_dev != 0:
                    data[mask] = arr / std_dev


# A one-pass to calculate std dev taken from https://www.johndcook.com/blog/standard_deviation/
def calc_var(arr, n_zeros=0):
    if np.ndim(arr) > 1:
        raise ValueError("Only 1d arrays are supported")

    m, s, k = 0, 0, n_zeros

    for elem in arr:
        if k == 0:
            m = elem
            s = 0
            k += 1
        else:
            m, s, k = var_helper(elem, m, s, k)

    return 0 if s == 0 else s / (k)


def var_helper(x, m, s, k):
    new_m = m + (x - m) / (k + 1)
    new_s = s + (x - m) * (x - new_m)
    return new_m, new_s, k + 1
