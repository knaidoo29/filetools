import numpy as np
import pygadgetreader as pyg


def readsnap(fname, return_pos=True, return_vel=True, return_pid=False, part='dm', single=0,
             xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None, suppress=1):
    """Reads snapshot file.

    Parameters
    ----------
    fname : str
        Gadget file name.
    return_pos : bool, optional
        Reads and outputs the positions from a GADGET file.
    return_vel : bool, optional
        Reads and outputs the velocities from a GADGET file.
    return_pid : bool, optional
        Reads and outputs the particle IDs from a GADGET file.
    part : str, optional
        Particle type, default set to 'dm' (dark matter).
    single : int, optional
        If 1 opens a single snapshot part, otherwise opens them all.
    xmin : float, optional
        Minimum x-value.
    xmax : float, optional
        Maximum x-value.
    ymin : float, optional
        Minimum y-value.
    ymax : float, optional
        Maximum y-value.
    zmin : float, optional
        Minimum z-value.
    zmax : float, optional
        Maximum z-value.
    suppress : int, optional
        Suppresses print statements from pygadgetreader.
    """
    if return_pos == True:
        pos = pyg.readsnap(fname, 'pos', part, single=single, suppress=suppress)
    if return_vel == True:
        vel = pyg.readsnap(fname, 'vel', part, single=single, suppress=suppress)
    if return_pid == True:
        pid = pyg.readsnap(fname, 'pid', part, single=single, suppress=suppress)
    if return_pos == True:
        mask = np.ones(len(pos))
        if xmin is not None:
            cond = np.where(pos[:, 0] < xmin)[0]
            mask[cond] = 0.
        if xmax is not None:
            cond = np.where(pos[:, 0] > xmax)[0]
            mask[cond] = 0.
        if ymin is not None:
            cond = np.where(pos[:, 1] < ymin)[0]
            mask[cond] = 0.
        if ymax is not None:
            cond = np.where(pos[:, 1] > ymax)[0]
            mask[cond] = 0.
        if zmin is not None:
            cond = np.where(pos[:, 2] < zmin)[0]
            mask[cond] = 0.
        if zmax is not None:
            cond = np.where(pos[:, 2] > zmax)[0]
            mask[cond] = 0.
        cond = np.where(mask == 1.)[0]
        pos = pos[cond]
        if return_vel == True:
            vel = vel[cond]
        if return_pid == True:
            pid = pid[cond]
    if return_pid == True:
        if return_pos == True and return_vel == True:
            return [pos, vel, pid]
        elif return_pos == True and return_vel == False:
            return [pos, pid]
        elif return_pos == False and return_vel == True:
            return [vel, pid]
    else:
        if return_pos == True and return_vel == True:
            return [pos, vel]
        elif return_pos == True and return_vel == False:
            return pos
        elif return_pos == False and return_vel == True:
            return vel
