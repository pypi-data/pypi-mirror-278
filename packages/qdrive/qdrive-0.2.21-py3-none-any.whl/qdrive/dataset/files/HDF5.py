from qdrive.dataset.files.file_mgr_single import file_mgr_single

import h5py, xarray, shutil, netCDF4, os, tabulate, tempfile, datetime

# TODO check if HDF5 that keep open due to user operations block additional writes to it.

class HDF5_file(file_mgr_single):
    def __init__(self, file_info, group_selection = "/"):
        super().__init__(file_info)
        self.__group_selection = group_selection
    
    @property           
    def raw(self):
        if self.object_handle == None:
            self.object_handle = h5py.File(self.file_obj.current.path,'r', swmr=True)
        return self.object_handle
    
    @property
    def hdf5(self):
        return self.raw
    
    @property
    def xarray(self):
        return xarray.open_dataset(self.file_obj.current.path,
                                   group  = self.__group_selection, lock=False)
    
    @property
    def netcdf4(self):
        dataset =  netCDF4.Dataset(self.file_obj.current.path, mode='r')
        return dataset
    
    @property
    def pandas(self):
        return self.xarray.to_dataframe()
    
    def __setitem__(self, key, value):
        if key in self.hdf5.keys():
            raise ValueError(f"Cannot add to dataset. There is already an item present under the name '{key}'.")
        self.object_handle.close()
        self.object_handle = None
        
        if isinstance(value, xarray.Dataset):
            with tempfile.TemporaryDirectory() as tmpdirname:
                new_content_file_loc = f'{tmpdirname}/temp_file.hdf5'
                value.to_netcdf(new_content_file_loc)
                
                new_content_file = h5py.File(new_content_file_loc,'r')
                main_file = h5py.File(self.file_obj.current.path,'a', swmr=True)
                
                main_file.create_group(key)
                grp = main_file[key]
                
                for dataset in new_content_file.keys():
                    h5py.h5o.copy(new_content_file.id, dataset.encode('utf-8'), grp.id, dataset.encode('utf-8'))
                
                new_content_file.close()
                main_file.close()
                
                self._save()   
        else: 
            raise ValueError(f"Assignement of type {type(value)} is not supported. Please provide and xarray Dataset, or qdrive lineplot or heatmap objects")
    
    def __getitem__(self, key):
        if key in self.keys():
            return HDF5_file(self.file_obj, group_selection=key)
        raise ValueError(f"Group {key} is not present is this dataset. To inspect the available groups, print the dataset.")
    
    def keys(self):
        keys = ["/"]
        for item in self.hdf5.keys():
            if isinstance(self.hdf5[item], h5py.Group):
                keys.append(item)
        return keys
    
    # TODO add support for the other types
    def update(self, object):
        new_desination = self._create_new_file_path(f'{self.name}.hdf5')
        if isinstance(object, (xarray.Dataset, xarray.DataArray)):
            object.to_netcdf(new_desination)
        elif isinstance(object, h5py.File):
            ori_filename = (object.file.filename)
            object.file.close()
            shutil.copyfile(ori_filename, new_desination)
        else:
            raise ValueError("Please provide a type that can be converted into a HDF5 file.")
        self._update(new_desination)
        
    def __repr__(self):
        if len(self.keys()) == 1:
            out = "This is a HDF5 dataset (netcdf4 compatible)."
        else:
            out = "This data file (HDF5) contains sub-datsets :\n"
            table_items = []
            for key in self.keys():
                if key == "/":
                    table_items.append( [key, f"ds['{self.name}']"])
                else:
                    table_items.append( [key, f"ds['{self.name}']['{key}']"])
            out += tabulate.tabulate(table_items)
        out += "\nFor more info see : [out website]"
        return out