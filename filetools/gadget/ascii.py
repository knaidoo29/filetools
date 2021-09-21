import numpy as np
import subprocess
import multiprocessing as mp

from . import read


def gadget2ascii_single(gfname_single, IDstart=0):
    """Converts single Gadget file into ascii format.

    Parameters
    ----------
    gfname_single : str
        Single gadget filename.
    IDstart : int
        Particle ID starter.
    """
    reader = read.ReadGADGET()
    posvel = reader.readsnap(gfname_single, return_pos=True, return_vel=True, part='dm', single=1)
    pos, vel = posvel[0], posvel[1]
    x, y, z = pos[:, 0], pos[:, 1], pos[:, 2]
    vx, vy, vz = vel[:, 0], vel[:, 1], vel[:, 2]
    partid = np.arange(len(x), dtype='int')
    if IDstart != 0:
        partid += IDstart
    np.savetxt(gfname_single + '.ascii', np.column_stack([x, y, z, vx, vy, vz, partid]))


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
    fnames = []
    for i in range(0, len(blocks)):
        fnames.append(gfname + '.' + str(i))
    # Step 1: Init multiprocessing.Pool()
    pool = mp.Pool(ncpu)
    # Step 2: `pool.apply`
    outs = [pool.apply(gadget2ascii_single, args=(fnames[i], nparts[i])) for i in range(0, len(blocks))]
    # Step 3: Don't forget to close
    pool.close()

    # Old function
    # reader = read.ReadGADGET()
    # startid = 0
    # for i in range(0, blocks):
    #     posvel = reader.readsnap(gfname + '.'+str(i), return_pos=True, return_vel=True, part='dm', single=1)
    #     pos = posvel[0]
    #     vel = posvel[1]
    #     x, y, z = pos[:, 0], pos[:, 1], pos[:, 2]
    #     vx, vy, vz = vel[:, 0], vel[:, 1], vel[:, 2]
    #     #partid = np.arange(len(x)) + startid
    #     #startid += len(x)
    #     partid = np.arange(len(x))
    #     if i > 0:
    #         partid += nparts[i-1]
    #     np.savetxt(gfname + '_' + str(i) + '.ascii', np.column_stack([x, y, z, vx, vy, vz, partid]))


def rm_gadget_ascii_copy(gfname):
    """Removes all ascii copies of the gadget file.

    Parameters
    ----------
    gfname : str
        Gadget filename root.
    """
    subprocess.call('rm ' + gfname + '_*.ascii', shell=True)
