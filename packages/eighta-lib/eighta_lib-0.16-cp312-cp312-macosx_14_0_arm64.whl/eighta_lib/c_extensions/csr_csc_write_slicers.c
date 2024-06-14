#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <hdf5.h>
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
    } else if (H5Tequal(hdf5_dtype, H5T_NATIVE_LLONG)) {
        return NPY_INT64;
    } else {
        return -1;  // Unknown type
    }
}

void write_process_csr_matrix(const char* src_file_name, const char* dst_file_name, const char* src_group_name,
                              int64_t* row_indices, int n_rows, int64_t* col_indices, int n_cols, int batch_size) {
    // Open the files
    hid_t src_file_id = H5Fopen(src_file_name, H5F_ACC_RDONLY, H5P_DEFAULT);
    if (src_file_id < 0) {
        fprintf(stderr, "Error reopening source file.\n");
        return;
    }

    hid_t dst_file_id = H5Fopen(dst_file_name, H5F_ACC_RDWR, H5P_DEFAULT);
    if (dst_file_id < 0) {
        fprintf(stderr, "Error reopening destination file.\n");
        H5Fclose(src_file_id);
        return;
    }

    // Open the source group
    hid_t src_group_id = H5Gopen2(src_file_id, src_group_name, H5P_DEFAULT);
    if (src_group_id < 0) {
        fprintf(stderr, "Error opening source group.\n");
        H5Fclose(src_file_id);
        H5Fclose(dst_file_id);
        return;
    }

    // Create or open the destination group
    hid_t dst_group_id = H5Gopen2(dst_file_id, src_group_name, H5P_DEFAULT);
    if (dst_group_id < 0) {
        fprintf(stderr, "Error creating destination group.\n");
        H5Gclose(src_group_id);
        H5Fclose(src_file_id);
        H5Fclose(dst_file_id);
        return;
    }

    // Open datasets in the source group
    hid_t data_id = H5Dopen2(src_group_id, "data", H5P_DEFAULT);
    hid_t indices_id = H5Dopen2(src_group_id, "indices", H5P_DEFAULT);
    hid_t indptr_id = H5Dopen2(src_group_id, "indptr", H5P_DEFAULT);
    if (data_id < 0 || indices_id < 0 || indptr_id < 0) {
        fprintf(stderr, "Error opening dataset.\n");
        H5Gclose(src_group_id);
        H5Gclose(dst_group_id);
        H5Fclose(src_file_id);
        H5Fclose(dst_file_id);
        return;
    }

    // Determine data types and sizes
    hid_t data_dtype = H5Dget_type(data_id);
    hid_t index_dtype = H5Dget_type(indices_id);
    hid_t indptr_dtype = H5Dget_type(indptr_id);
    size_t element_size = H5Tget_size(data_dtype);
    size_t index_size = H5Tget_size(index_dtype);
    size_t indptr_size = H5Tget_size(indptr_dtype);
    int npy_data_dtype = hdf5_dtype_to_numpy_dtype(data_dtype);
    int npy_index_dtype = hdf5_dtype_to_numpy_dtype(index_dtype);
    int npy_indptr_dtype = hdf5_dtype_to_numpy_dtype(indptr_dtype);

    // Use the first and last elements to determine the range
    int64_t start_col_index = col_indices[0];
    int64_t end_col_index = col_indices[n_cols - 1];
    int64_t range = end_col_index - start_col_index + 1;

    // Allocate col_map to cover the entire range of possible column indices
    int64_t *col_map = (int64_t*)malloc(range * sizeof(int64_t));
    if (!col_map) {
        fprintf(stderr, "Memory allocation failed for col_map.\n");
        goto cleanup;
    }

    // Initialize col_map with -1 (indicating invalid index)
    for (int64_t i = 0; i < range; i++) {
        col_map[i] = -1;
    }

    // Map column indices
    for (int i = 0; i < n_cols; i++) {
        col_map[col_indices[i] - start_col_index] = i;
    }

    // Open datasets in the dest group
    hid_t data_set = H5Dopen2(dst_group_id, "data", H5P_DEFAULT);
        if (data_set < 0) {
        fprintf(stderr, "Error creating data dataset.\n");
        goto cleanup;
    }
    hid_t indices_set = H5Dopen2(dst_group_id, "indices", H5P_DEFAULT);
    if (indices_set < 0) {
        fprintf(stderr, "Error creating indices dataset.\n");
        goto cleanup_data_set;
    }

    hid_t indptr_set = H5Dopen2(dst_group_id, "indptr", H5P_DEFAULT);
    if (indptr_set < 0) {
        fprintf(stderr, "Error creating indptr dataset.\n");
        goto cleanup_indices_set;
    }

    int current_length = 0;
    void* total_indptr = calloc(n_rows + 1, indptr_size);
    if (!total_indptr) {
        fprintf(stderr, "Memory allocation failed for total_indptr.\n");
        goto cleanup_indptr_set;
    }

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
                continue;
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
                    if (((int*)indices_slice)[j] >= start_col_index && ((int*)indices_slice)[j] <= end_col_index && col_map[((int*)indices_slice)[j] - start_col_index] >= 0) {
                        valid_count++;
                    }
                } else if (npy_index_dtype == NPY_INT64) {
                    if (((int64_t*)indices_slice)[j] >= start_col_index && ((int64_t*)indices_slice)[j] <= end_col_index && col_map[((int64_t*)indices_slice)[j] - start_col_index] >= 0) {
                        valid_count++;
                    }
                }
            }

            if (valid_count > 0) {
                void *filtered_data = malloc(valid_count * element_size);
                void *filtered_indices = malloc(valid_count * index_size);
                if (!filtered_data || !filtered_indices) {
                    fprintf(stderr, "Memory allocation failed for filtered_data or filtered_indices.\n");
                    free(data_slice);
                    free(indices_slice);
                    free(filtered_data);
                    free(filtered_indices);
                    continue;
                }

                valid_count = 0;
                for (hsize_t j = 0; j < row_size; j++) {
                    if (npy_index_dtype == NPY_INT32) {
                        if (((int*)indices_slice)[j] >= start_col_index && ((int*)indices_slice)[j] <= end_col_index && col_map[((int*)indices_slice)[j] - start_col_index] >= 0) {
                            memcpy((char*)filtered_data + valid_count * element_size, (char*)data_slice + j * element_size, element_size);
                            ((int*)filtered_indices)[valid_count] = col_map[((int*)indices_slice)[j] - start_col_index];
                            valid_count++;
                        }
                    } else if (npy_index_dtype == NPY_INT64) {
                        if (((int64_t*)indices_slice)[j] >= start_col_index && ((int64_t*)indices_slice)[j] <= end_col_index && col_map[((int64_t*)indices_slice)[j] - start_col_index] >= 0) {
                            memcpy((char*)filtered_data + valid_count * element_size, (char*)data_slice + j * element_size, element_size);
                            ((int64_t*)filtered_indices)[valid_count] = col_map[((int64_t*)indices_slice)[j] - start_col_index];
                            valid_count++;
                        }
                    }
                }

                hsize_t new_size[1] = {current_length + valid_count};
                H5Dset_extent(data_set, new_size);
                H5Dset_extent(indices_set, new_size);

                hsize_t offset[1] = {current_length};
                hsize_t count[1] = {valid_count};

                hid_t memspace = H5Screate_simple(1, count, NULL);

                hid_t new_data_space = H5Dget_space(data_set);
                H5Sselect_hyperslab(new_data_space, H5S_SELECT_SET, offset, NULL, count, NULL);
                H5Dwrite(data_set, data_dtype, memspace, new_data_space, H5P_DEFAULT, filtered_data);
                H5Sclose(new_data_space);

                hid_t new_indices_space = H5Dget_space(indices_set);
                H5Sselect_hyperslab(new_indices_space, H5S_SELECT_SET, offset, NULL, count, NULL);
                H5Dwrite(indices_set, index_dtype, memspace, new_indices_space, H5P_DEFAULT, filtered_indices);
                H5Sclose(new_indices_space);

                H5Sclose(memspace);

                current_length += valid_count;
                if (npy_indptr_dtype == NPY_INT32) {
                    ((int*)total_indptr)[i + 1] = current_length;
                } else if (npy_indptr_dtype == NPY_INT64) {
                    ((int64_t*)total_indptr)[i + 1] = current_length;
                }

                free(data_slice);
                free(indices_slice);
                free(filtered_data);
                free(filtered_indices);
            } else {
                if (npy_indptr_dtype == NPY_INT32) {
                    ((int*)total_indptr)[i + 1] = current_length;
                } else if (npy_indptr_dtype == NPY_INT64) {
                    ((int64_t*)total_indptr)[i + 1] = current_length;
                }
            }
        } else {
            if (npy_indptr_dtype == NPY_INT32) {
                ((int*)total_indptr)[i + 1] = current_length;
            } else if (npy_indptr_dtype == NPY_INT64) {
                ((int64_t*)total_indptr)[i + 1] = current_length;
            }
        }
    }

    H5Dwrite(indptr_set, indptr_dtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, total_indptr);

    // Cleanup
    free(total_indptr);
cleanup_indptr_set:
    H5Dclose(indptr_set);
cleanup_indices_set:
    H5Dclose(indices_set);
cleanup_data_set:
    H5Dclose(data_set);
cleanup:
    free(col_map);
    H5Dclose(data_id);
    H5Dclose(indices_id);
    H5Dclose(indptr_id);
    H5Gclose(src_group_id);
    H5Gclose(dst_group_id);
    H5Fclose(src_file_id);
    H5Fclose(dst_file_id);
}

// Python wrapper for the C function
static PyObject* py_write_process_csr_matrix(PyObject* self, PyObject* args) {
    const char *src_file_name;
    const char *dest_file_name;
    const char *src_group_name;
    PyObject *py_row_indices;
    PyObject *py_col_indices;
    int batch_size;

    if (!PyArg_ParseTuple(args, "sssO!O!i", &src_file_name, &dest_file_name, &src_group_name,
                          &PyArray_Type, &py_row_indices,
                          &PyArray_Type, &py_col_indices,
                          &batch_size)) {
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

    // Release the GIL while the C function is executing
    Py_BEGIN_ALLOW_THREADS
    write_process_csr_matrix(src_file_name, dest_file_name, src_group_name, row_indices, n_rows, col_indices, n_cols, batch_size);
    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}

void write_process_csc_matrix(const char* src_file_name, const char* dst_file_name, const char* src_group_name,
                              int64_t* row_indices, int n_rows, int64_t* col_indices, int n_cols, int batch_size) {
    // Open the files
    hid_t src_file_id = H5Fopen(src_file_name, H5F_ACC_RDONLY, H5P_DEFAULT);
    if (src_file_id < 0) {
        fprintf(stderr, "Error reopening source file.\n");
        return;
    }

    hid_t dst_file_id = H5Fopen(dst_file_name, H5F_ACC_RDWR, H5P_DEFAULT);
    if (dst_file_id < 0) {
        fprintf(stderr, "Error reopening destination file.\n");
        H5Fclose(src_file_id);
        return;
    }

    // Open the source group
    hid_t src_group_id = H5Gopen2(src_file_id, src_group_name, H5P_DEFAULT);
    if (src_group_id < 0) {
        fprintf(stderr, "Error opening source group.\n");
        H5Fclose(src_file_id);
        H5Fclose(dst_file_id);
        return;
    }

    // Create or open the destination group
    hid_t dst_group_id = H5Gopen2(dst_file_id, src_group_name, H5P_DEFAULT);
    if (dst_group_id < 0) {
        fprintf(stderr, "Error creating destination group.\n");
        H5Gclose(src_group_id);
        H5Fclose(src_file_id);
        H5Fclose(dst_file_id);
        return;
    }

    // Open datasets in the source group
    hid_t data_id = H5Dopen2(src_group_id, "data", H5P_DEFAULT);
    hid_t indices_id = H5Dopen2(src_group_id, "indices", H5P_DEFAULT);
    hid_t indptr_id = H5Dopen2(src_group_id, "indptr", H5P_DEFAULT);
    if (data_id < 0 || indices_id < 0 || indptr_id < 0) {
        fprintf(stderr, "Error opening dataset.\n");
        H5Gclose(src_group_id);
        H5Gclose(dst_group_id);
        H5Fclose(src_file_id);
        H5Fclose(dst_file_id);
        return;
    }

    // Determine data types and sizes
    hid_t data_dtype = H5Dget_type(data_id);
    hid_t index_dtype = H5Dget_type(indices_id);
    hid_t indptr_dtype = H5Dget_type(indptr_id);
    size_t element_size = H5Tget_size(data_dtype);
    size_t index_size = H5Tget_size(index_dtype);
    size_t indptr_size = H5Tget_size(indptr_dtype);
    int npy_data_dtype = hdf5_dtype_to_numpy_dtype(data_dtype);
    int npy_index_dtype = hdf5_dtype_to_numpy_dtype(index_dtype);
    int npy_indptr_dtype = hdf5_dtype_to_numpy_dtype(indptr_dtype);

    // Use the first and last elements to determine the range
    int64_t start_row_index = row_indices[0];
    int64_t end_row_index = row_indices[n_rows - 1];
    int64_t range = end_row_index - start_row_index + 1;

    // Allocate row_map to cover the entire range of possible row indices
    int64_t *row_map = (int64_t*)malloc(range * sizeof(int64_t));
    if (!row_map) {
        fprintf(stderr, "Memory allocation failed for row_map.\n");
        goto cleanup;
    }

    // Initialize row_map with -1 (indicating invalid index)
    for (int64_t i = 0; i < range; i++) {
        row_map[i] = -1;
    }

    // Map row indices
    for (int i = 0; i < n_rows; i++) {
        row_map[row_indices[i] - start_row_index] = i;
    }

    // Open datasets in the dest group
    hid_t data_set = H5Dopen2(dst_group_id, "data", H5P_DEFAULT);
    if (data_set < 0) {
        fprintf(stderr, "Error creating data dataset.\n");
        goto cleanup;
    }
    hid_t indices_set = H5Dopen2(dst_group_id, "indices", H5P_DEFAULT);
    if (indices_set < 0) {
        fprintf(stderr, "Error creating indices dataset.\n");
        goto cleanup_data_set;
    }

    hid_t indptr_set = H5Dopen2(dst_group_id, "indptr", H5P_DEFAULT);
    if (indptr_set < 0) {
        fprintf(stderr, "Error creating indptr dataset.\n");
        goto cleanup_indices_set;
    }

    int current_length = 0;
    void* total_indptr = calloc(n_cols + 1, indptr_size);
    if (!total_indptr) {
        fprintf(stderr, "Memory allocation failed for total_indptr.\n");
        goto cleanup_indptr_set;
    }

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
                continue;
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
                    if (((int*)indices_slice)[j] >= start_row_index && ((int*)indices_slice)[j] <= end_row_index && row_map[((int*)indices_slice)[j] - start_row_index] >= 0) {
                        valid_count++;
                    }
                } else if (npy_index_dtype == NPY_INT64) {
                    if (((int64_t*)indices_slice)[j] >= start_row_index && ((int64_t*)indices_slice)[j] <= end_row_index && row_map[((int64_t*)indices_slice)[j] - start_row_index] >= 0) {
                        valid_count++;
                    }
                }
            }

            if (valid_count > 0) {
                void *filtered_data = malloc(valid_count * element_size);
                void *filtered_indices = malloc(valid_count * index_size);
                if (!filtered_data || !filtered_indices) {
                    fprintf(stderr, "Memory allocation failed for filtered_data or filtered_indices.\n");
                    free(data_slice);
                    free(indices_slice);
                    free(filtered_data);
                    free(filtered_indices);
                    continue;
                }

                valid_count = 0;
                for (hsize_t j = 0; j < col_size; j++) {
                    if (npy_index_dtype == NPY_INT32) {
                        if (((int*)indices_slice)[j] >= start_row_index && ((int*)indices_slice)[j] <= end_row_index && row_map[((int*)indices_slice)[j] - start_row_index] >= 0) {
                            memcpy((char*)filtered_data + valid_count * element_size, (char*)data_slice + j * element_size, element_size);
                            ((int*)filtered_indices)[valid_count] = row_map[((int*)indices_slice)[j] - start_row_index];
                            valid_count++;
                        }
                    } else if (npy_index_dtype == NPY_INT64) {
                        if (((int64_t*)indices_slice)[j] >= start_row_index && ((int64_t*)indices_slice)[j] <= end_row_index && row_map[((int64_t*)indices_slice)[j] - start_row_index] >= 0) {
                            memcpy((char*)filtered_data + valid_count * element_size, (char*)data_slice + j * element_size, element_size);
                            ((int64_t*)filtered_indices)[valid_count] = row_map[((int64_t*)indices_slice)[j] - start_row_index];
                            valid_count++;
                        }
                    }
                }

                hsize_t new_size[1] = {current_length + valid_count};
                H5Dset_extent(data_set, new_size);
                H5Dset_extent(indices_set, new_size);

                hsize_t offset[1] = {current_length};
                hsize_t count[1] = {valid_count};

                hid_t memspace = H5Screate_simple(1, count, NULL);

                hid_t new_data_space = H5Dget_space(data_set);
                H5Sselect_hyperslab(new_data_space, H5S_SELECT_SET, offset, NULL, count, NULL);
                H5Dwrite(data_set, data_dtype, memspace, new_data_space, H5P_DEFAULT, filtered_data);
                H5Sclose(new_data_space);

                hid_t new_indices_space = H5Dget_space(indices_set);
                H5Sselect_hyperslab(new_indices_space, H5S_SELECT_SET, offset, NULL, count, NULL);
                H5Dwrite(indices_set, index_dtype, memspace, new_indices_space, H5P_DEFAULT, filtered_indices);
                H5Sclose(new_indices_space);

                H5Sclose(memspace);

                current_length += valid_count;
                if (npy_indptr_dtype == NPY_INT32) {
                    ((int*)total_indptr)[i + 1] = current_length;
                } else if (npy_indptr_dtype == NPY_INT64) {
                    ((int64_t*)total_indptr)[i + 1] = current_length;
                }

                free(data_slice);
                free(indices_slice);
                free(filtered_data);
                free(filtered_indices);
            } else {
                if (npy_indptr_dtype == NPY_INT32) {
                    ((int*)total_indptr)[i + 1] = current_length;
                } else if (npy_indptr_dtype == NPY_INT64) {
                    ((int64_t*)total_indptr)[i + 1] = current_length;
                }
            }
        } else {
            if (npy_indptr_dtype == NPY_INT32) {
                ((int*)total_indptr)[i + 1] = current_length;
            } else if (npy_indptr_dtype == NPY_INT64) {
                ((int64_t*)total_indptr)[i + 1] = current_length;
            }
        }
    }

    H5Dwrite(indptr_set, indptr_dtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, total_indptr);

    // Cleanup
    free(total_indptr);
cleanup_indptr_set:
    H5Dclose(indptr_set);
cleanup_indices_set:
    H5Dclose(indices_set);
cleanup_data_set:
    H5Dclose(data_set);
cleanup:
    free(row_map);
    H5Dclose(data_id);
    H5Dclose(indices_id);
    H5Dclose(indptr_id);
    H5Gclose(src_group_id);
    H5Gclose(dst_group_id);
    H5Fclose(src_file_id);
    H5Fclose(dst_file_id);
}

// Python wrapper for the C function
static PyObject* py_write_process_csc_matrix(PyObject* self, PyObject* args) {
    const char *src_file_name;
    const char *dest_file_name;
    const char *src_group_name;
    PyObject *py_row_indices;
    PyObject *py_col_indices;
    int batch_size;

    if (!PyArg_ParseTuple(args, "sssO!O!i", &src_file_name, &dest_file_name, &src_group_name,
                          &PyArray_Type, &py_row_indices,
                          &PyArray_Type, &py_col_indices,
                          &batch_size)) {
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

    // Release the GIL while the C function is executing
    Py_BEGIN_ALLOW_THREADS
    write_process_csc_matrix(src_file_name, dest_file_name, src_group_name, row_indices, n_rows, col_indices, n_cols, batch_size);
    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}

// Method definition object for this extension, these methods will be callable from Python
static PyMethodDef slicers_write_methods[] = {
    {"write_process_csr_matrix", (PyCFunction)py_write_process_csr_matrix, METH_VARARGS, "Writes and processes a CSR matrix from an HDF5 group to another HDF5 group"},
    {"write_process_csc_matrix", (PyCFunction)py_write_process_csc_matrix, METH_VARARGS, "Writes and processes a CSC matrix from an HDF5 group to another HDF5 group"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef slicers_write_module = {
    PyModuleDef_HEAD_INIT,
    "slicers_write", // Module name
    NULL,            // Module documentation (can be NULL)
    -1,              // Size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
    slicers_write_methods
};

// Module initialization function
PyMODINIT_FUNC PyInit_slicers_write(void) {
    import_array();  // Initialize NumPy C API
    return PyModule_Create(&slicers_write_module);
}