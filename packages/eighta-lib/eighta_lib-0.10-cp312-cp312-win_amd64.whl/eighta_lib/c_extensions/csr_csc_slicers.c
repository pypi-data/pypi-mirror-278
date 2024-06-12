#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include "hdf5.h"
#include <numpy/arrayobject.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

int hdf5_dtype_to_numpy_dtype(hid_t hdf5_dtype) {
    if (H5Tequal(hdf5_dtype, H5T_NATIVE_FLOAT)) {
        return NPY_FLOAT32;
    } else if (H5Tequal(hdf5_dtype, H5T_NATIVE_DOUBLE)) {
        return NPY_FLOAT64;
    } else if (H5Tequal(hdf5_dtype, H5T_NATIVE_INT)) {
        return NPY_INT32;
    } else if (H5Tequal(hdf5_dtype, H5T_NATIVE_UINT)) {
        return NPY_UINT32;
    } else if (H5Tequal(hdf5_dtype, H5T_NATIVE_LLONG)) { // Added for int64
        return NPY_INT64;
    } else {
        return -1;  // Unknown type
    }
}

typedef struct {
    void *data;
    void *indices;
    void *indptr;
    int n_rows;
    int n_cols;
    int data_type;
    int index_type;
    int indptr_type;
} CSRMatrix;

CSRMatrix* read_process_csr_matrix(const char* file_path, const char* group_name, int64_t* row_indices, int n_rows, int64_t* col_indices, int n_cols) {
    // Open HDF5 file and group
    hid_t file_id = H5Fopen(file_path, H5F_ACC_RDONLY, H5P_DEFAULT);
    if (file_id < 0) {
        fprintf(stderr, "Error opening file.\n");
        return NULL;
    }

    hid_t group_id = H5Gopen(file_id, group_name, H5P_DEFAULT);
    if (group_id < 0) {
        fprintf(stderr, "Error opening group.\n");
        H5Fclose(file_id);
        return NULL;
    }

    // Open datasets
    hid_t data_id = H5Dopen2(group_id, "data", H5P_DEFAULT);
    hid_t indices_id = H5Dopen2(group_id, "indices", H5P_DEFAULT);
    hid_t indptr_id = H5Dopen2(group_id, "indptr", H5P_DEFAULT);
    if (data_id < 0 || indices_id < 0 || indptr_id < 0) {
        fprintf(stderr, "Error opening dataset.\n");
        H5Gclose(group_id);
        H5Fclose(file_id);
        return NULL;
    }

    // Determine data types
    hid_t data_dtype = H5Dget_type(data_id);
    hid_t index_dtype = H5Dget_type(indices_id);
    hid_t indptr_dtype = H5Dget_type(indptr_id);

    int npy_data_dtype = hdf5_dtype_to_numpy_dtype(data_dtype);
    size_t element_size = H5Tget_size(data_dtype);

    int npy_index_dtype = hdf5_dtype_to_numpy_dtype(index_dtype);
    size_t index_size = H5Tget_size(index_dtype);

    int npy_indptr_dtype = hdf5_dtype_to_numpy_dtype(indptr_dtype);
    size_t indptr_size = H5Tget_size(indptr_dtype);

    // Determine the maximum value in col_indices to allocate col_map correctly
    int64_t max_col_index = col_indices[0];
    for (int i = 1; i < n_cols; i++) {
        if (col_indices[i] > max_col_index) {
            max_col_index = col_indices[i];
        }
    }

    // Allocate col_map to cover the entire range of possible column indices
    int *col_map = (int*)malloc((max_col_index + 1) * sizeof(int));
    if (!col_map) {
        fprintf(stderr, "Memory allocation failed for col_map.\n");
        H5Tclose(data_dtype);
        H5Dclose(data_id);
        H5Dclose(indices_id);
        H5Dclose(indptr_id);
        H5Gclose(group_id);
        H5Fclose(file_id);
        return NULL;
    }

    // Initialize col_map with -1 (indicating invalid index)
    for (int64_t i = 0; i <= max_col_index; i++) {
        col_map[i] = -1;
    }

    // Map column indices
    for (int i = 0; i < n_cols; i++) {
        col_map[col_indices[i]] = i;
    }

    // Prepare lists to collect sliced data
    void *data_list = malloc(0);
    void *indices_list = malloc(0);
    void *indptr_list = malloc((n_rows + 1) * indptr_size);
    if (!indptr_list) {
        fprintf(stderr, "Memory allocation failed for indptr_list.\n");
        free(col_map);
        H5Tclose(data_dtype);
        H5Dclose(data_id);
        H5Dclose(indices_id);
        H5Dclose(indptr_id);
        H5Gclose(group_id);
        H5Fclose(file_id);
        return NULL;
    }
    memset(indptr_list, 0, (n_rows + 1) * indptr_size);
    int current_length = 0;

    // Iterate through the specified row indices to slice the CSR matrix
    for (int i = 0; i < n_rows; i++) {
        int64_t row_idx = row_indices[i];
        int64_t data_start_idx_int = 0, data_end_idx_int = 0;

        // Read the start and end indices for the row from 'indptr'
        hsize_t indptr_offset[1] = {row_idx};
        hsize_t indptr_count[1] = {1};
        hid_t indptr_space = H5Dget_space(indptr_id);
        H5Sselect_hyperslab(indptr_space, H5S_SELECT_SET, indptr_offset, NULL, indptr_count, NULL);
        hid_t indptr_mem_space = H5Screate_simple(1, indptr_count, NULL);
        if (npy_indptr_dtype == NPY_INT32) {
            int data_start_idx_tmp;
            H5Dread(indptr_id, H5T_NATIVE_INT, indptr_mem_space, indptr_space, H5P_DEFAULT, &data_start_idx_tmp);
            data_start_idx_int = data_start_idx_tmp;
        } else if (npy_indptr_dtype == NPY_INT64) {
            H5Dread(indptr_id, H5T_NATIVE_LLONG, indptr_mem_space, indptr_space, H5P_DEFAULT, &data_start_idx_int);
        }
        H5Sclose(indptr_mem_space);
        H5Sclose(indptr_space);

        indptr_offset[0] = row_idx + 1;
        indptr_space = H5Dget_space(indptr_id);
        H5Sselect_hyperslab(indptr_space, H5S_SELECT_SET, indptr_offset, NULL, indptr_count, NULL);
        indptr_mem_space = H5Screate_simple(1, indptr_count, NULL);
        if (npy_indptr_dtype == NPY_INT32) {
            int data_end_idx_tmp;
            H5Dread(indptr_id, H5T_NATIVE_INT, indptr_mem_space, indptr_space, H5P_DEFAULT, &data_end_idx_tmp);
            data_end_idx_int = data_end_idx_tmp;
        } else if (npy_indptr_dtype == NPY_INT64) {
            H5Dread(indptr_id, H5T_NATIVE_LLONG, indptr_mem_space, indptr_space, H5P_DEFAULT, &data_end_idx_int);
        }
        H5Sclose(indptr_mem_space);
        H5Sclose(indptr_space);

        hsize_t data_start_idx = (hsize_t)data_start_idx_int;
        hsize_t data_end_idx = (hsize_t)data_end_idx_int;

        if (data_start_idx < data_end_idx) {
            hsize_t row_size = data_end_idx - data_start_idx;

            // Allocate temporary buffers
            void *data_slice = malloc(row_size * element_size);
            void *indices_slice = malloc(row_size * index_size);
            if (!data_slice || !indices_slice) {
                fprintf(stderr, "Memory allocation failed for data_slice or indices_slice.\n");
                free(data_slice);
                free(indices_slice);
                free(data_list);
                free(indices_list);
                free(indptr_list);
                free(col_map);
                H5Tclose(data_dtype);
                H5Dclose(data_id);
                H5Dclose(indices_id);
                H5Dclose(indptr_id);
                H5Gclose(group_id);
                H5Fclose(file_id);
                return NULL;
            }

            // Define the hyperslab in the dataset to read the current row
            hsize_t data_offset[1] = {data_start_idx};
            hsize_t data_count[1] = {row_size};
            hid_t data_space = H5Dget_space(data_id);
            H5Sselect_hyperslab(data_space, H5S_SELECT_SET, data_offset, NULL, data_count, NULL);
            hid_t data_mem_space = H5Screate_simple(1, data_count, NULL);
            H5Dread(data_id, data_dtype, data_mem_space, data_space, H5P_DEFAULT, data_slice);
            H5Sclose(data_mem_space);
            H5Sclose(data_space);

            // Define the hyperslab in the dataset to read the current row's indices
            hsize_t indices_offset[1] = {data_start_idx};
            hsize_t indices_count[1] = {row_size};
            hid_t indices_space = H5Dget_space(indices_id);
            H5Sselect_hyperslab(indices_space, H5S_SELECT_SET, indices_offset, NULL, indices_count, NULL);
            hid_t indices_mem_space = H5Screate_simple(1, indices_count, NULL);
            H5Dread(indices_id, index_dtype, indices_mem_space, indices_space, H5P_DEFAULT, indices_slice);
            H5Sclose(indices_mem_space);
            H5Sclose(indices_space);

            // Mask to select columns of interest
            int valid_count = 0;
            for (hsize_t j = 0; j < row_size; j++) {
                if (npy_index_dtype == NPY_INT32) {
                    if (((int*)indices_slice)[j] <= max_col_index && col_map[((int*)indices_slice)[j]] >= 0) {
                        valid_count++;
                    }
                } else if (npy_index_dtype == NPY_INT64) {
                    if (((int64_t*)indices_slice)[j] <= max_col_index && col_map[((int64_t*)indices_slice)[j]] >= 0) {
                        valid_count++;
                    }
                }
            }

            if (valid_count > 0) {
                void *new_data_list = realloc(data_list, (current_length + valid_count) * element_size);
                if (!new_data_list) {
                    fprintf(stderr, "Memory allocation failed for data_list.\n");
                    free(data_slice);
                    free(indices_slice);
                    free(data_list);
                    free(indices_list);
                    free(indptr_list);
                    free(col_map);
                    H5Tclose(data_dtype);
                    H5Dclose(data_id);
                    H5Dclose(indices_id);
                    H5Dclose(indptr_id);
                    H5Gclose(group_id);
                    H5Fclose(file_id);
                    return NULL;
                }
                data_list = new_data_list;

                void *new_indices_list = realloc(indices_list, (current_length + valid_count) * index_size);
                if (!new_indices_list) {
                    fprintf(stderr, "Memory allocation failed for indices_list.\n");
                    free(data_slice);
                    free(indices_slice);
                    free(data_list);
                    free(indices_list);
                    free(indptr_list);
                    free(col_map);
                    H5Tclose(data_dtype);
                    H5Dclose(data_id);
                    H5Dclose(indices_id);
                    H5Dclose(indptr_id);
                    H5Gclose(group_id);
                    H5Fclose(file_id);
                    return NULL;
                }
                indices_list = new_indices_list;

                // Append valid data and indices to the lists
                for (hsize_t j = 0; j < row_size; j++) {
                    if (npy_index_dtype == NPY_INT32) {
                        if (((int*)indices_slice)[j] <= max_col_index && col_map[((int*)indices_slice)[j]] >= 0) {
                            memcpy((char*)data_list + current_length * element_size, (char*)data_slice + j * element_size, element_size);
                            ((int*)indices_list)[current_length] = col_map[((int*)indices_slice)[j]];
                            current_length++;
                        }
                    } else if (npy_index_dtype == NPY_INT64) {
                        if (((int64_t*)indices_slice)[j] <= max_col_index && col_map[((int64_t*)indices_slice)[j]] >= 0) {
                            memcpy((char*)data_list + current_length * element_size, (char*)data_slice + j * element_size, element_size);
                            ((int64_t*)indices_list)[current_length] = col_map[((int64_t*)indices_slice)[j]];
                            current_length++;
                        }
                    }
                }
                if (npy_indptr_dtype == NPY_INT32) {
                    ((int*)indptr_list)[i + 1] = current_length;
                } else if (npy_indptr_dtype == NPY_INT64) {
                    ((int64_t*)indptr_list)[i + 1] = current_length;
                }
            } else {
                if (npy_indptr_dtype == NPY_INT32) {
                    ((int*)indptr_list)[i + 1] = current_length;
                } else if (npy_indptr_dtype == NPY_INT64) {
                    ((int64_t*)indptr_list)[i + 1] = current_length;
                }
            }

            // Free temporary buffers
            free(data_slice);
            free(indices_slice);
        } else {
            if (npy_indptr_dtype == NPY_INT32) {
                ((int*)indptr_list)[i + 1] = current_length;
            } else if (npy_indptr_dtype == NPY_INT64) {
                ((int64_t*)indptr_list)[i + 1] = current_length;
            }
        }
    }

    // Create CSRMatrix struct
    CSRMatrix *csr_matrix = (CSRMatrix*)malloc(sizeof(CSRMatrix));
    if (!csr_matrix) {
        fprintf(stderr, "Memory allocation failed for csr_matrix.\n");
        free(data_list);
        free(indices_list);
        free(indptr_list);
        free(col_map);
        H5Tclose(data_dtype);
        H5Dclose(data_id);
        H5Dclose(indices_id);
        H5Dclose(indptr_id);
        H5Gclose(group_id);
        H5Fclose(file_id);
        return NULL;
    }
    csr_matrix->data = realloc(data_list, current_length * element_size);
    csr_matrix->indices = realloc(indices_list, current_length * index_size);
    csr_matrix->indptr = indptr_list;
    csr_matrix->n_rows = n_rows;
    csr_matrix->n_cols = n_cols;
    csr_matrix->data_type = npy_data_dtype;
    csr_matrix->index_type = npy_index_dtype;
    csr_matrix->indptr_type = npy_indptr_dtype;

    // Close datasets and free resources
    H5Tclose(data_dtype);
    H5Dclose(data_id);
    H5Dclose(indices_id);
    H5Dclose(indptr_id);
    H5Gclose(group_id);
    H5Fclose(file_id);

    free(col_map);

    return csr_matrix;
}

static PyObject* py_read_process_csr_matrix(PyObject* self, PyObject* args) {
    const char *file_path;
    const char *group_name;
    PyObject *py_row_indices;
    PyObject *py_col_indices;

    if (!PyArg_ParseTuple(args, "ssOO", &file_path, &group_name, &py_row_indices, &py_col_indices)) {
        return NULL;
    }

    if (!PyArray_Check(py_row_indices) || !PyArray_Check(py_col_indices)) {
        PyErr_SetString(PyExc_TypeError, "row_indices and col_indices must be NumPy arrays");
        return NULL;
    }

    int n_rows = (int)PyArray_SIZE((PyArrayObject*)py_row_indices);
    int n_cols = (int)PyArray_SIZE((PyArrayObject*)py_col_indices);

    int64_t *row_indices = (int64_t*)PyArray_DATA((PyArrayObject*)py_row_indices);
    int64_t *col_indices = (int64_t*)PyArray_DATA((PyArrayObject*)py_col_indices);

    CSRMatrix* csr_matrix;
    // Release the GIL while the C function is executing
    Py_BEGIN_ALLOW_THREADS
    csr_matrix = read_process_csr_matrix(file_path, group_name, row_indices, n_rows, col_indices, n_cols);
    Py_END_ALLOW_THREADS

    if (!csr_matrix) {
        return NULL;
    }

    npy_intp data_dims[1] = {csr_matrix->indptr_type == NPY_INT32 ? ((int*)csr_matrix->indptr)[csr_matrix->n_rows] : ((int64_t*)csr_matrix->indptr)[csr_matrix->n_rows]};
    npy_intp indptr_dims[1] = {csr_matrix->n_rows + 1};
    npy_intp indices_dims[1] = {csr_matrix->indptr_type == NPY_INT32 ? ((int*)csr_matrix->indptr)[csr_matrix->n_rows] : ((int64_t*)csr_matrix->indptr)[csr_matrix->n_rows]};

    PyObject* data_array = PyArray_SimpleNewFromData(1, data_dims, csr_matrix->data_type, csr_matrix->data);
    PyObject* indices_array = PyArray_SimpleNewFromData(1, indices_dims, csr_matrix->index_type, csr_matrix->indices);
    PyObject* indptr_array = PyArray_SimpleNewFromData(1, indptr_dims, csr_matrix->indptr_type, csr_matrix->indptr);

    // Ensure NumPy owns the data and will manage its lifetime
    PyArray_ENABLEFLAGS((PyArrayObject*)data_array, NPY_ARRAY_OWNDATA);
    PyArray_ENABLEFLAGS((PyArrayObject*)indices_array, NPY_ARRAY_OWNDATA);
    PyArray_ENABLEFLAGS((PyArrayObject*)indptr_array, NPY_ARRAY_OWNDATA);

    PyObject* result = PyTuple_Pack(3, data_array, indices_array, indptr_array);

    // Do not free the csr_matrix data arrays here as they are now owned by the NumPy arrays
    free(csr_matrix);

    return result;
}

typedef struct {
    void *data;
    void *indices;
    void *indptr;
    int n_rows;
    int n_cols;
    int data_type;
    int index_type;
    int indptr_type;
} CSCMatrix;

CSCMatrix* read_process_csc_matrix(const char* file_path, const char* group_name, int64_t* row_indices, int n_rows, int64_t* col_indices, int n_cols) {
    // Open HDF5 file and group
    hid_t file_id = H5Fopen(file_path, H5F_ACC_RDONLY, H5P_DEFAULT);
    if (file_id < 0) {
        fprintf(stderr, "Error opening file.\n");
        return NULL;
    }

    hid_t group_id = H5Gopen(file_id, group_name, H5P_DEFAULT);
    if (group_id < 0) {
        fprintf(stderr, "Error opening group.\n");
        H5Fclose(file_id);
        return NULL;
    }

    // Open datasets
    hid_t data_id = H5Dopen2(group_id, "data", H5P_DEFAULT);
    hid_t indices_id = H5Dopen2(group_id, "indices", H5P_DEFAULT);
    hid_t indptr_id = H5Dopen2(group_id, "indptr", H5P_DEFAULT);
    if (data_id < 0 || indices_id < 0 || indptr_id < 0) {
        fprintf(stderr, "Error opening dataset.\n");
        H5Gclose(group_id);
        H5Fclose(file_id);
        return NULL;
    }

    // Determine data types
    hid_t data_dtype = H5Dget_type(data_id);
    hid_t index_dtype = H5Dget_type(indices_id);
    hid_t indptr_dtype = H5Dget_type(indptr_id);

    int npy_data_dtype = hdf5_dtype_to_numpy_dtype(data_dtype);
    size_t element_size = H5Tget_size(data_dtype);

    int npy_index_dtype = hdf5_dtype_to_numpy_dtype(index_dtype);
    size_t index_size = H5Tget_size(index_dtype);

    int npy_indptr_dtype = hdf5_dtype_to_numpy_dtype(indptr_dtype);
    size_t indptr_size = H5Tget_size(indptr_dtype);

    // Determine the maximum value in row_indices to allocate row_map correctly
    int64_t max_row_index = row_indices[0];
    for (int64_t i = 1; i < n_rows; i++) {
        if (row_indices[i] > max_row_index) {
            max_row_index = row_indices[i];
        }
    }

    // Allocate row_map to cover the entire range of possible row indices
    int *row_map = (int*)malloc((max_row_index + 1) * sizeof(int));
    if (!row_map) {
        fprintf(stderr, "Memory allocation failed for row_map.\n");
        H5Tclose(data_dtype);
        H5Dclose(data_id);
        H5Dclose(indices_id);
        H5Dclose(indptr_id);
        H5Gclose(group_id);
        H5Fclose(file_id);
        return NULL;
    }

    // Initialize row_map with -1 (indicating invalid index)
    for (int64_t i = 0; i <= max_row_index; i++) {
        row_map[i] = -1;
    }

    // Map row indices
    for (int64_t i = 0; i < n_rows; i++) {
        row_map[row_indices[i]] = i;
    }

    // Prepare lists to collect sliced data
    void *data_list = malloc(0);
    void *indices_list = malloc(0);
    void *indptr_list = malloc((n_cols + 1) * indptr_size);
    if (!indptr_list) {
        fprintf(stderr, "Memory allocation failed for indptr_list.\n");
        free(row_map);
        H5Tclose(data_dtype);
        H5Dclose(data_id);
        H5Dclose(indices_id);
        H5Dclose(indptr_id);
        H5Gclose(group_id);
        H5Fclose(file_id);
        return NULL;
    }
    memset(indptr_list, 0, (n_cols + 1) * indptr_size);
    int current_length = 0;

    // Iterate through the specified column indices to slice the CSC matrix
    for (int i = 0; i < n_cols; i++) {
        int64_t col_idx = col_indices[i];
        int64_t data_start_idx_int = 0, data_end_idx_int = 0;

        // Read the start and end indices for the column from 'indptr'
        hsize_t indptr_offset[1] = {col_idx};
        hsize_t indptr_count[1] = {1};
        hid_t indptr_space = H5Dget_space(indptr_id);
        H5Sselect_hyperslab(indptr_space, H5S_SELECT_SET, indptr_offset, NULL, indptr_count, NULL);
        hid_t indptr_mem_space = H5Screate_simple(1, indptr_count, NULL);
        if (npy_indptr_dtype == NPY_INT32) {
            int data_start_idx_tmp;
            H5Dread(indptr_id, H5T_NATIVE_INT, indptr_mem_space, indptr_space, H5P_DEFAULT, &data_start_idx_tmp);
            data_start_idx_int = data_start_idx_tmp;
        } else if (npy_indptr_dtype == NPY_INT64) {
            H5Dread(indptr_id, H5T_NATIVE_LLONG, indptr_mem_space, indptr_space, H5P_DEFAULT, &data_start_idx_int);
        }
        H5Sclose(indptr_mem_space);
        H5Sclose(indptr_space);

        indptr_offset[0] = col_idx + 1;
        indptr_space = H5Dget_space(indptr_id);
        H5Sselect_hyperslab(indptr_space, H5S_SELECT_SET, indptr_offset, NULL, indptr_count, NULL);
        indptr_mem_space = H5Screate_simple(1, indptr_count, NULL);
        if (npy_indptr_dtype == NPY_INT32) {
            int data_end_idx_tmp;
            H5Dread(indptr_id, H5T_NATIVE_INT, indptr_mem_space, indptr_space, H5P_DEFAULT, &data_end_idx_tmp);
            data_end_idx_int = data_end_idx_tmp;
        } else if (npy_indptr_dtype == NPY_INT64) {
            H5Dread(indptr_id, H5T_NATIVE_LLONG, indptr_mem_space, indptr_space, H5P_DEFAULT, &data_end_idx_int);
        }
        H5Sclose(indptr_mem_space);
        H5Sclose(indptr_space);

        hsize_t data_start_idx = (hsize_t)data_start_idx_int;
        hsize_t data_end_idx = (hsize_t)data_end_idx_int;

        if (data_start_idx < data_end_idx) {
            hsize_t col_size = data_end_idx - data_start_idx;

            // Allocate temporary buffers
            void *data_slice = malloc(col_size * element_size);
            void *indices_slice = malloc(col_size * index_size);
            if (!data_slice || !indices_slice) {
                fprintf(stderr, "Memory allocation failed for data_slice or indices_slice.\n");
                free(data_slice);
                free(indices_slice);
                free(data_list);
                free(indices_list);
                free(indptr_list);
                free(row_map);
                H5Tclose(data_dtype);
                H5Dclose(data_id);
                H5Dclose(indices_id);
                H5Dclose(indptr_id);
                H5Gclose(group_id);
                H5Fclose(file_id);
                return NULL;
            }

            // Define the hyperslab in the dataset to read the current column
            hsize_t data_offset[1] = {data_start_idx};
            hsize_t data_count[1] = {col_size};
            hid_t data_space = H5Dget_space(data_id);
            H5Sselect_hyperslab(data_space, H5S_SELECT_SET, data_offset, NULL, data_count, NULL);
            hid_t data_mem_space = H5Screate_simple(1, data_count, NULL);
            H5Dread(data_id, data_dtype, data_mem_space, data_space, H5P_DEFAULT, data_slice);
            H5Sclose(data_mem_space);
            H5Sclose(data_space);

            // Define the hyperslab in the dataset to read the current column's indices
            hsize_t indices_offset[1] = {data_start_idx};
            hsize_t indices_count[1] = {col_size};
            hid_t indices_space = H5Dget_space(indices_id);
            H5Sselect_hyperslab(indices_space, H5S_SELECT_SET, indices_offset, NULL, indices_count, NULL);
            hid_t indices_mem_space = H5Screate_simple(1, indices_count, NULL);
            H5Dread(indices_id, index_dtype, indices_mem_space, indices_space, H5P_DEFAULT, indices_slice);
            H5Sclose(indices_mem_space);
            H5Sclose(indices_space);

            // Mask to select rows of interest
            int valid_count = 0;
            for (hsize_t j = 0; j < col_size; j++) {
                if (npy_index_dtype == NPY_INT32) {
                    if (((int*)indices_slice)[j] <= max_row_index && row_map[((int*)indices_slice)[j]] >= 0) {
                        valid_count++;
                    }
                } else if (npy_index_dtype == NPY_INT64) {
                    if (((int64_t*)indices_slice)[j] <= max_row_index && row_map[((int64_t*)indices_slice)[j]] >= 0) {
                        valid_count++;
                    }
                }
            }

            if (valid_count > 0) {
                void *new_data_list = realloc(data_list, (current_length + valid_count) * element_size);
                if (!new_data_list) {
                    fprintf(stderr, "Memory allocation failed for data_list.\n");
                    free(data_slice);
                    free(indices_slice);
                    free(data_list);
                    free(indices_list);
                    free(indptr_list);
                    free(row_map);
                    H5Tclose(data_dtype);
                    H5Dclose(data_id);
                    H5Dclose(indices_id);
                    H5Dclose(indptr_id);
                    H5Gclose(group_id);
                    H5Fclose(file_id);
                    return NULL;
                }
                data_list = new_data_list;

                void *new_indices_list = realloc(indices_list, (current_length + valid_count) * index_size);
                if (!new_indices_list) {
                    fprintf(stderr, "Memory allocation failed for indices_list.\n");
                    free(data_slice);
                    free(indices_slice);
                    free(data_list);
                    free(indices_list);
                    free(indptr_list);
                    free(row_map);
                    H5Tclose(data_dtype);
                    H5Dclose(data_id);
                    H5Dclose(indices_id);
                    H5Dclose(indptr_id);
                    H5Gclose(group_id);
                    H5Fclose(file_id);
                    return NULL;
                }
                indices_list = new_indices_list;

                // Append valid data and indices to the lists
                for (hsize_t j = 0; j < col_size; j++) {
                    if (npy_index_dtype == NPY_INT32) {
                        if (((int*)indices_slice)[j] <= max_row_index && row_map[((int*)indices_slice)[j]] >= 0) {
                            memcpy((char*)data_list + current_length * element_size, (char*)data_slice + j * element_size, element_size);
                            ((int*)indices_list)[current_length] = row_map[((int*)indices_slice)[j]];
                            current_length++;
                        }
                    } else if (npy_index_dtype == NPY_INT64) {
                        if (((int64_t*)indices_slice)[j] <= max_row_index && row_map[((int64_t*)indices_slice)[j]] >= 0) {
                            memcpy((char*)data_list + current_length * element_size, (char*)data_slice + j * element_size, element_size);
                            ((int64_t*)indices_list)[current_length] = row_map[((int64_t*)indices_slice)[j]];
                            current_length++;
                        }
                    }
                }
                if (npy_indptr_dtype == NPY_INT32) {
                    ((int*)indptr_list)[i + 1] = current_length;
                } else if (npy_indptr_dtype == NPY_INT64) {
                    ((int64_t*)indptr_list)[i + 1] = current_length;
                }
            } else {
                if (npy_indptr_dtype == NPY_INT32) {
                    ((int*)indptr_list)[i + 1] = current_length;
                } else if (npy_indptr_dtype == NPY_INT64) {
                    ((int64_t*)indptr_list)[i + 1] = current_length;
                }
            }

            // Free temporary buffers
            free(data_slice);
            free(indices_slice);
        } else {
            if (npy_indptr_dtype == NPY_INT32) {
                ((int*)indptr_list)[i + 1] = current_length;
            } else if (npy_indptr_dtype == NPY_INT64) {
                ((int64_t*)indptr_list)[i + 1] = current_length;
            }
        }
    }

    // Create CSCMatrix struct
    CSCMatrix *csc_matrix = (CSCMatrix*)malloc(sizeof(CSCMatrix));
    if (!csc_matrix) {
        fprintf(stderr, "Memory allocation failed for csc_matrix.\n");
        free(data_list);
        free(indices_list);
        free(indptr_list);
        free(row_map);
        H5Tclose(data_dtype);
        H5Dclose(data_id);
        H5Dclose(indices_id);
        H5Dclose(indptr_id);
        H5Gclose(group_id);
        H5Fclose(file_id);
        return NULL;
    }
    csc_matrix->data = realloc(data_list, current_length * element_size);
    csc_matrix->indices = realloc(indices_list, current_length * index_size);
    csc_matrix->indptr = indptr_list;
    csc_matrix->n_rows = n_rows;
    csc_matrix->n_cols = n_cols;
    csc_matrix->data_type = npy_data_dtype;
    csc_matrix->index_type = npy_index_dtype;
    csc_matrix->indptr_type = npy_indptr_dtype;

    // Close datasets and free resources
    H5Tclose(data_dtype);
    H5Dclose(data_id);
    H5Dclose(indices_id);
    H5Dclose(indptr_id);
    H5Gclose(group_id);
    H5Fclose(file_id);

    free(row_map);

    return csc_matrix;
}

static PyObject* py_read_process_csc_matrix(PyObject* self, PyObject* args) {
    const char *file_path;
    const char *group_name;
    PyObject *py_row_indices;
    PyObject *py_col_indices;

    if (!PyArg_ParseTuple(args, "ssOO", &file_path, &group_name, &py_row_indices, &py_col_indices)) {
        return NULL;
    }

    if (!PyArray_Check(py_row_indices) || !PyArray_Check(py_col_indices)) {
        PyErr_SetString(PyExc_TypeError, "row_indices and col_indices must be NumPy arrays");
        return NULL;
    }

    int n_rows = (int)PyArray_SIZE((PyArrayObject*)py_row_indices);
    int n_cols = (int)PyArray_SIZE((PyArrayObject*)py_col_indices);

    int64_t *row_indices = (int64_t*)PyArray_DATA((PyArrayObject*)py_row_indices);
    int64_t *col_indices = (int64_t*)PyArray_DATA((PyArrayObject*)py_col_indices);

    CSCMatrix* csc_matrix;
    // Release the GIL while the C function is executing
    Py_BEGIN_ALLOW_THREADS
    csc_matrix = read_process_csc_matrix(file_path, group_name, row_indices, n_rows, col_indices, n_cols);
    Py_END_ALLOW_THREADS

    if (!csc_matrix) {
        return NULL;
    }

    npy_intp data_dims[1] = {csc_matrix->indptr_type == NPY_INT32 ? ((int*)csc_matrix->indptr)[csc_matrix->n_cols] : ((int64_t*)csc_matrix->indptr)[csc_matrix->n_cols]};
    npy_intp indptr_dims[1] = {csc_matrix->n_cols + 1};
    npy_intp indices_dims[1] = {csc_matrix->indptr_type == NPY_INT32 ? ((int*)csc_matrix->indptr)[csc_matrix->n_cols] : ((int64_t*)csc_matrix->indptr)[csc_matrix->n_cols]};

    PyObject* data_array = PyArray_SimpleNewFromData(1, data_dims, csc_matrix->data_type, csc_matrix->data);
    PyObject* indices_array = PyArray_SimpleNewFromData(1, indices_dims, csc_matrix->index_type, csc_matrix->indices);
    PyObject* indptr_array = PyArray_SimpleNewFromData(1, indptr_dims, csc_matrix->indptr_type, csc_matrix->indptr);

    // Ensure NumPy owns the data and will manage its lifetime
    PyArray_ENABLEFLAGS((PyArrayObject*)data_array, NPY_ARRAY_OWNDATA);
    PyArray_ENABLEFLAGS((PyArrayObject*)indices_array, NPY_ARRAY_OWNDATA);
    PyArray_ENABLEFLAGS((PyArrayObject*)indptr_array, NPY_ARRAY_OWNDATA);

    PyObject* result = PyTuple_Pack(3, data_array, indices_array, indptr_array);

    // Do not free the csc_matrix data arrays here as they are now owned by the NumPy arrays
    free(csc_matrix);

    return result;
}

// Method definition object for this extension, these methods will be callable from Python
static PyMethodDef slicers_methods[] = {
    {"read_process_csr_matrix", (PyCFunction)py_read_process_csr_matrix, METH_VARARGS, "Reads and processes a CSR matrix from an HDF5 group"},
    {"read_process_csc_matrix", (PyCFunction)py_read_process_csc_matrix, METH_VARARGS, "Reads and processes a CSC matrix from an HDF5 group"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef slicersmodule = {
    PyModuleDef_HEAD_INIT,
    "slicers", // Module name
    NULL,      // Module documentation (can be NULL)
    -1,        // Size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
    slicers_methods
};

// Module initialization function
PyMODINIT_FUNC PyInit_slicers(void) {
    import_array();  // Initialize NumPy C API
    return PyModule_Create(&slicersmodule);
}