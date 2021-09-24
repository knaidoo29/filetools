import numpy as np
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
