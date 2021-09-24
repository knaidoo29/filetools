import numpy as np
import subprocess
import multiprocessing as mp

from . import ascii_single


def gadget2ascii(gfname, infoname, ncpu=4):
    """Creates an ascii copy of the gadget file.

    Parameters
    ----------
    gfname : str
        Gadget filename root.
    infofname : str
        Used for obtaining particle IDs.
    ncpu : int, optional
        Number of CPUs for running multiprocessed gadget ascii copying.
    """
    data = np.loadtxt(infoname, unpack=True)
    blocks = data[0]
    nparts = np.zeros(len(blocks))
    nparts[1:] = data[7][:-1]
    nparts = nparts.astype('int')
    nparts = np.cumsum(nparts)
    fnames = []
    for i in range(0, len(blocks)):
        fnames.append(gfname + '.' + str(i))
    # Step 1: Init multiprocessing.Pool()
    args_list = [(fnames[i], nparts[i]) for i in range(0, len(blocks))]
    pool = mp.Pool(ncpu)
    # Step 2: `pool.starmap` for multiple arguments
    output = pool.starmap(ascii_single.gadget2ascii_single, args_list)
    # Step 3: Don't forget to close
    pool.close()


def rm_gadget_ascii_copy(gfname):
    """Removes all ascii copies of the gadget file.

    Parameters
    ----------
    gfname : str
        Gadget filename root.
    """
    subprocess.call('rm ' + gfname + '*.ascii', shell=True)
