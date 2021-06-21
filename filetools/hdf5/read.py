import numpy as np
import h5py


def get_hdf5_data(hdf5_filename, key_name, overide_extension=False):
    """Outputs a specific data set from the hdf5 data set.

    Parameters
    ----------
    hdf5_filename : str
        Filename of the hdf5 file.
    key_name : str
        the key_name or key_names of items in the hdf5 file that are to be outputted.
    overide_extension : bool
        Checks extension is hdf5 and allow for this to be added if not included in
        the filename.

    Returns
    -------
    data : array
        If key_name is a string then the associated array from the hdf5 file is outputted,
        if a list then a list of arrays is given.
    """
    islist = False
    if isinstance(key_name, list) is True:
        islist = True
    if hdf5_filename.endswith('.hdf5') != True and overide_extension == True:
        hdf5_filename = hdf5_filename + '.hdf5'
    hdf5_file = h5py.File(hdf5_filename, 'r')
    if islist is False:
        data = np.array(hdf5_file[key_name])
    else:
        data = []
        for i in range(0, len(key_name)):
            data.append(np.array(hdf5_file[key_name[i]]))
    return data
