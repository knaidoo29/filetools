import numpy as np
import fitsio


class ReadFITS:


    def __init__(self):
        self.fname = None
        self.FITS = None
        self.nrows = None
        self.chunks = None
        self.fraction = None
        self.fraction_rows = None
        self.column_names = None
        self.current_chunk = 0
        self.read_all = False


    def file(self, fname, chunks=100):
        """Input the fits filename so fitsio can find the number of rows and determine
        the size of chunks.

        Parameters
        ----------
        fname : str
            FITS filename.
        chunks : int
            Number of chunks to be read at one time.
        """
        self.clean()
        self.fname = fname
        self.FITS = fitsio.FITS(fname)
        self.nrows = self.FITS[1].get_nrows()
        self.chunks = chunks
        self.fraction = 1./self.chunks
        self.fraction_rows = int(self.nrows*self.fraction)
        self.column_names = self.FITS[1].get_colnames()
        print('FITS file:', self.fname)
        print('Rows total:', self.nrows)
        print("Chunks:", self.chunks)
        print('Rows per chunk:', self.fraction_rows)
        print('Column names:', self.column_names)


    def read(self, columns=None, chunk=None):
        """Reads iteratively unless the which_chunk is set.

        Parameters
        ----------
        columns : str, optional
            Defines which columns to read, default will output all.
        chunk : int, optional
            Define which chunk of data to read.

        Returns
        -------
        data : dict
            Data contained in a dictionary.
        """
        if columns is None:
            columns = self.column_names
        if chunk is not None:
            assert chunk < self.chunks, "Chunk is too large for number of chunks defined."
            self.current_chunk = chunk
        if self.current_chunk+1 != self.chunks:
            minrows = self.current_chunk*self.fraction_rows
            maxrows = (self.current_chunk+1)*self.fraction_rows
        else:
            minrows = self.current_chunk*self.fraction_rows
            maxrows = self.nrows
        rows = np.arange(minrows, maxrows, 1)
        print(minrows,maxrows)
        data = fitsio.read(self.fname, rows=rows, columns=columns)
        if self.current_chunk + 1 < self.chunks:
            self.current_chunk += 1
        else:
            self.read_all = True
        return data
    

    def clean(self):
        self.__init__()
