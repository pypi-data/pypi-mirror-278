from eighta_lib import file_management, slicing
import h5py
import os
import numpy as np
import pandas as pd
import psutil

class BackedAnnData:

    def __init__(self, file_path: str) -> None:
        try:
            with h5py.File(file_path) as f:
                self.file_path = file_path
                self.obs = Group("obs", file_path)
                self.var = Group("var", file_path)
                self.uns = Group("uns", file_path)
                self.obsm = Group("obsm", file_path)
                self.varm = Group("varm", file_path)
                self.layers = Group("layers", file_path)
                self.obsp = Group("obsp", file_path)
                self.varp = Group("varp", file_path)
                self.raw = Group("raw", file_path)
        except:
            raise FileNotFoundError("The given path cannot be opened as hdf5 file.")
        
    def __repr__(self) -> str:
        with h5py.File(self.file_path) as file:
            n_obs = file['obs']['_index'].size
            n_var = file['var']['_index'].size
            res = f"BackedAnnData object with (n_obs x n_var) = ({n_obs} x {n_var})\n"
            for field in ["obs", "var", "uns", "obsm", "varm", "layers", "obsp", "varp"]:
                res = res + f"    {field}: "
                for key in file[field].keys():
                    if key != "_index":                
                        res = res + f"'{key}', "
                res = res[:-2] + "\n"
            res += f"\n  backing file: '{self.file_path}'\n"
            res += f"  size on dish: {os.path.getsize(self.file_path)/(1024**3):.4f} GB"
        return res
    
    def __str__(self) -> str:
        return f"<BackAnnData object with file path '{self.file_path}'>"
    
    def detailed_info(self) -> str:

        def convert_size(size):
            if size / (1024 ** 3) > 0.01:
                return f"{(size / (1024 ** 3)):.4f} GB"
            elif size / (1024 ** 2) > 0.01:
                return f"{(size / (1024 ** 2)):.4f} MB"
            elif size / 1024 > 0.01:
                return f"{(size / 1024):.4f} KB"
            else:
                return f"{size:.4f} Bytes"

        def dataset_to_string(dataset, key, indent):
            indent_str = '  ' * indent
            if isinstance(dataset, h5py.Dataset):
                dataset_size = (np.prod(dataset.shape) * dataset.dtype.itemsize)
                if dataset.attrs.get('encoding-type') in ['string', 'string-array']:
                    return f"{indent_str}{key}: string {dataset.shape}, {convert_size(dataset_size)}\n"
                else:
                    return f"{indent_str}{key}: {dataset.dtype} {dataset.shape}, {convert_size(dataset_size)}\n"
        
            if isinstance(dataset, h5py.Group):
                if dataset.attrs.get('encoding-type') == 'csr_matrix':
                    dataset_size = 0
                    for i in ['data', 'indptr', 'indices']:
                        dataset_size += (dataset[i].size * dataset[i].dtype.itemsize)
                    return f"{indent_str}{key}: sparse csr_matrix, {dataset['data'].size} elements, {convert_size(dataset_size)}\n"
                elif dataset.attrs.get('encoding-type') == 'csc_matrix':
                    dataset_size = 0
                    for i in ['data', 'indptr', 'indices']:
                        dataset_size += (dataset[i].size * dataset[i].dtype.itemsize)
                    return f"{indent_str}{key}: sparse csc_matrix, {dataset['data'].size} elements, {convert_size(dataset_size)}\n"
                elif dataset.attrs.get('encoding-type') == 'categorical':
                    dataset_size = 0
                    for i in ['categories', 'codes']:
                        dataset_size += (dataset[i].size * dataset[i].dtype.itemsize)
                    return f"{indent_str}{key}: Categorical ({dataset['categories'].size} categories), {convert_size(dataset_size)}\n"
                else:
                    str = f"{indent_str}{key}:\n"
                    for child in dataset.keys():
                        if child != "_index":
                            str += dataset_to_string(dataset[child], child, indent+1, )
                    return str


        with h5py.File(self.file_path) as file:
            n_obs = file['obs']['_index'].size
            n_var = file['var']['_index'].size
            res = f"BackedAnnData object with (n_obs x n_var) = ({n_obs} x {n_var})\n"
            for key in file.keys():
                res += dataset_to_string(file[key], key, 1)
            res += f"\n  backing file: '{self.file_path}'\n"
            res += f"  size on dish: {convert_size(os.path.getsize(self.file_path))}"
            return res
        
    @property
    def X(self):
        def convert_size(size):
            if size / (1024 ** 3) > 0.01:
                return f"{(size / (1024 ** 3)):.4f} GB"
            elif size / (1024 ** 2) > 0.01:
                return f"{(size / (1024 ** 2)):.4f} MB"
            elif size / 1024 > 0.01:
                return f"{(size / 1024):.4f} KB"
            else:
                return f"{size:.4f} Bytes"
            
        with h5py.File(self.file_path) as file:
            X_size = 0
            if file['X'].attrs.get('encoding-type') in ['csc_matrix', 'csr_matrix']:
                for key in file['X'].keys():
                    X_size += file['X'][key].dtype.itemsize * file['X'][key].size
            else:
                X_size = np.prod(file['X'].shape) * file['X'].dtype.itemsize
            avaliable_memory = psutil.virtual_memory().available
            print(f"The size of X is {convert_size(X_size)}.")
            print(f"Avaliable memory is {convert_size(avaliable_memory)}.")
            if X_size > avaliable_memory*0.7:
                raise MemoryError(f"The size of X is more than 70% of avaliable memory. Have {convert_size(avaliable_memory)}, need {convert_size(X_size)}. If you want to continue anyway, call '.force_X().'")
            return file_management.load_h5ad(file['X'])
        
    def force_X(self):
        with h5py.File(self.file_path) as file:
            return file_management.load_h5ad(file['X'])
        
    def __getitem__(self, key):
        if isinstance(key, str):
            with h5py.File(self.file_path) as file:
                data = file_management.load_h5ad(file[key])
                keys = key.split("/")
                if keys[0] in ['obs', 'var'] and len(keys) > 1:
                    return pd.Series(data, file[keys[0]]['_index'][:].astype('str'))
                else:  
                    return data
        elif isinstance(key, slice):
            with h5py.File(self.file_path) as file:
                n_var = file['var']['_index'].size
            return slicing.read_slice_h5ad(self.file_path, key, slice(n_var))
        elif isinstance(key, tuple):
            return slicing.read_slice_h5ad(self.file_path, key[0], key[1])
        else:
            raise KeyError("Invalid key.")
    
    def __setitem__(self, name: str, new_value):
        file_management.update_h5ad(self.file_path, name, new_value)


    def __delitem__(self, name: str):
        file_management.pop_h5ad(self.file_path, name)

    def remove(self, key, repack):
        file_management.pop_h5ad(self.file_path, key, repack=repack)

    def pop(self, key):
        return file_management.pop_h5ad(self.file_path, key)
    
    def slice_to_file(self, new_file_path: str, row: slice, col: slice):
        slicing.write_slice_h5ad(self.file_path, new_file_path, row, col)
    
    def filter(self, include = None, exclude = None):
        return file_management.filter_anndata_h5ad(self.file_path, include, exclude)
        
class Group:
    
    def __init__(self, key, file_path) -> None:
        self.key = key
        self.file_path = file_path

    def __getitem__(self, name: str):
        with h5py.File(self.file_path) as file:
            data = file_management.load_h5ad(file[f"{self.key}/{name}"])
            if self.key in ['obs', 'var'] and name != "":
                return pd.Series(data, file[self.key]['_index'][:].astype('str'))
            else:  
                return data
            
    def __setitem__(self, name: str, new_value):
        file_management.update_h5ad(self.file_path, f"{self.key}/{name}", new_value)

    def __delitem__(self, name: str):
        file_management.pop_h5ad(self.file_path, f"{self.key}/{name}")
