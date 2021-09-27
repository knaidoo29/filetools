# FileTools

A tool for reading and writing different file types. This pools together a bunch
of python modules used to read all sorts of files to have a centralised toolkit
for handling this.

## Dependencies

* `numpy`
* `h5py`
* [`pygadgetreader`](https://github.com/jveitchmichaelis/pygadgetreader)
* [`fitsio`](https://github.com/esheldon/fitsio)
* `mpi4py`

## Installation

```
python setup.py build
python setup.py install
```

## Tutorial

Reading FITS file in chunks:

```
from filetools.fits import ReadFITS

fname = # fits file name.

reader = ReadFITS()
reader.file(fname) # optional: chunks=100

# To read a chunk:
reader.read()

# specify chunk and columns
chunk = # which chunk we want
columns = # columns we want.
reader.read(chunk=chunk, columns=columns)

# To read chunks iteratively, default number of chunks is 100
while reader.read_all == False:
    reader.read()

# For testing maybe you just want to read the first 4 chunks
reader.current_chunk = 0
while reader.current_chunk < 4:
    data = reader.read()
```

## Functions

* `fits` :
  * `fits.ReadFITS` : Reads fits file in chunks.  
* `folder` :
  * `folder.create_folder`: creates a folder with a specified name in a given path.
* `gadget` :
  * `gadget.get_gadget_info` : Returns information about a simulation snapshot.
  * `gadget.gadget2ascii` : Creates ascii copy of a gadget file.
  * `gadget.rm_gadget_ascii_copy` : Removes gadget ascii copy.
  * `gadget.ReadGADGET` : Reads Gadget file in chunks.
* `hdf5` :
  * `hdf5.get_hdf5_data` : Reads HDF5 files.
  * `print_hdf5_item_structure` : Prints the HDF5 file structure.
  * `get_hdf5_keys` : Gets the HDF5 keys.
