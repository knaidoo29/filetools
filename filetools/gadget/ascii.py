import numpy as np
import subprocess

from . import ascii_single


def gadget2ascii(gfname, infoname, MPI=None):
    """Creates an ascii copy of the gadget file.

    Parameters
    ----------
    gfname : str
        Gadget filename root.
    infofname : str
        Used for obtaining particle IDs.
    MPI : obj, optional
        MPIutils MPI class object.
    """
    if MPI is None:
        data = np.loadtxt(infoname, unpack=True)
        blocks = data[0]
        nparts = np.zeros(len(blocks))
        nparts[1:] = data[7][:-1]
        nparts = nparts.astype('int')
        nparts = np.cumsum(nparts)
        fnames = []
        for i in range(0, len(blocks)):
            fnames.append(gfname + '.' + str(i))
        for i in range(0, len(blocks)):
            ascii_single.gadget2ascii_single(fnames[i], nparts[i])
    else:
        if MPI.rank == 0:
            data = np.loadtxt(infoname, unpack=True)
            blocks = data[0]
            nparts = np.zeros(len(blocks))
            nparts[1:] = data[7][:-1]
            nparts = nparts.astype('int')
            nparts = np.cumsum(nparts)
            fnames = []
            for i in range(0, len(blocks)):
                fnames.append(gfname + '.' + str(i))
            MPI.send(fnames, tag=11)
            MPI.send(nparts, tag=12)
        else:
            fnames = MPI.recv(0, tag=11)
            nparts = MPI.recv(0, tag=12)
        MPI_loop_size = MPI.set_loop(len(fnames))
        for mpi_ind in range(0, MPI_loop_size):
            i = MPI.mpi_ind2ind(mpi_ind)
            if i is not None:
                ascii_single.gadget2ascii_single(fnames[i], nparts[i])


def rm_gadget_ascii_copy(gfname):
    """Removes all ascii copies of the gadget file.

    Parameters
    ----------
    gfname : str
        Gadget filename root.
    """
    subprocess.call('rm ' + gfname + '*.ascii', shell=True)
