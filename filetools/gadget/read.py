import numpy as np
import pygadgetreader as pyg

from . import read_single
from .. import utils


class ReadGADGET:


    def __init__(self):
        """Initialises the class."""
        self.fname = None
        self.info = None
        self.filenum = None
        self.filexmin = None
        self.fileymin = None
        self.filezmin = None
        self.filexmax = None
        self.fileymax = None
        self.filezmax = None


    def _is_file_in_range_1d(self, xmin, xmax, file_xmin, file_xmax):
        """Internal function for checking whether a file is within range along one axis.

        Parameters
        ----------
        xmin : float
            Minimum X.
        xmax : float
            Maximum X.
        file_xmin : float
            File minimum X.
        file_xmax : float
            File maximum X.
        """
        if xmin is not None and xmax is not None:
            # To be out of range both extremes have to be outside the target range.
            if file_xmax <= xmin:
                return False
            elif file_xmin >= xmax:
                return False
            else:
                return True
        elif xmin is not None and xmax is None:
            if file_xmax <= xmin:
                return False
            else:
                return True
        elif xmin is None and xmax is not None:
            if file_xmin > xmax:
                return False
            else:
                return True
        else:
            return True


    def _is_file_in_range(self, xmin, xmax, ymin, ymax, zmin, zmax):
        """Internal function for checking whether a file is within a range.

        Parameters
        ----------
        xmin : float
            Minimum X.
        xmax : float
            Maximum X.
        ymin : float
            Minimum Y.
        ymax : float
            Maximum Y.
        zmin : float
            Minimum Z.
        zmax : float
            Maximum Z.
        """
        files_needed = []
        for i in range(0, len(self.filenum)):
            is_x_in_range = self._is_file_in_range_1d(xmin, xmax, self.filexmin[i], self.filexmax[i])
            is_y_in_range = self._is_file_in_range_1d(ymin, ymax, self.fileymin[i], self.fileymax[i])
            is_z_in_range = self._is_file_in_range_1d(zmin, zmax, self.filezmin[i], self.filezmax[i])
            if is_x_in_range*is_y_in_range*is_z_in_range == 1:
                files_needed.append(self.filenum[i])
        return files_needed


    def file(self, fname, info=None):
        """Sets file name and file info.

        Parameters
        ----------
        fname : str
            File name.
        info : str
            Info file name.
        """
        self.fname = fname
        self.info = info
        if self.info is not None:
            dinfo = np.loadtxt(self.info, unpack=True)
            self.filenum = dinfo[0].astype('int')
            self.filexmin = dinfo[1]
            self.fileymin = dinfo[2]
            self.filezmin = dinfo[3]
            self.filexmax = dinfo[4]
            self.fileymax = dinfo[5]
            self.filezmax = dinfo[6]


    def readsnap(self, fname, return_pos=True, return_vel=True, part='dm', single=0,
                 xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None):
        """Reads snapshot file.

        Parameters
        ----------
        fname : str
            Gadget file name.
        return_pos : bool, optional
            Reads and outputs the positions from a GADGET file.
        return_vel : bool, optional
            Reads and outputs the velocities from a GADGET file.
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
        usepara : bool, optional
            Open files in parallel if more than one.
        """
        return read_single.readsnap(fname, return_pos=return_pos, return_vel=return_vel,
                                    part=part, single=single, xmin=xmin, xmax=xmax,
                                    ymin=ymin, ymax=ymax, zmin=zmin, zmax=zmax)


    def read(self, return_pos=True, return_vel=True, part='dm', xmin=None, xmax=None,
             ymin=None, ymax=None, zmin=None, zmax=None, MPI=None, combine=True):
        """Reads file.

        Parameters
        ----------
        return_pos : bool, optional
            Reads and outputs the positions from a GADGET file.
        return_vel : bool, optional
            Reads and outputs the velocities from a GADGET file.
        part : str, optional
            Particle type, default set to 'dm' (dark matter).
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
        MPI : obj, optional
            mpiutils MPI class object.
        combine : bool, optional
            If MPI is on this sets whether we need to combine the final dataset.
        """
        if self.info is None:
            # then we just read the entire thing.
            out = self.readsnap(self.fname, return_pos=return_pos, return_vel=return_vel,
                                part=part, single=0, xmin=xmin, xmax=xmax, ymin=ymin,
                                ymax=ymax, zmin=zmin, zmax=zmax)
            if return_pos == True and return_vel == True:
                pos, vel = out[0], out[1]
            elif return_pos == True and return_vel == False:
                pos = out
            elif return_pos == False and return_vel == True:
                vel = out
        else:
            files_needed = self._is_file_in_range(xmin, xmax, ymin, ymax, zmin, zmax)
            if MPI is None:
                for i in range(0, len(files_needed)):
                    fname_chunk = self.fname + '.' + str(files_needed[i])
                    _out = self.readsnap(fname_chunk, return_pos=return_pos, return_vel=return_vel,
                                         part=part, single=1, xmin=xmin, xmax=xmax, ymin=ymin,
                                         ymax=ymax, zmin=zmin, zmax=zmax)
                    if return_pos == True and return_vel == True:
                        _pos, _vel = _out[0], _out[1]
                    elif return_pos == True and return_vel == False:
                        _pos = _out
                    elif return_pos == False and return_vel == True:
                        _vel = _out
                    if i == 0:
                        poss = [_pos]
                        if return_vel == True:
                            vels = [_vel]
                    else:
                        poss.append(_pos)
                        if return_vel == True:
                            vels.append(_vel)
                    utils.progress_bar(i, len(files_needed), indexing=True, explanation='Reading from GADGET File')
                pos = np.concatenate(poss)
                if return_vel == True:
                    vel = np.concatenate(vels)
            else:
                if MPI.rank == 0:
                    fnames = []
                    for i in range(0, len(files_needed)):
                        fname_chunk = self.fname + '.' + str(files_needed[i])
                        fnames.append(fname_chunk)
                    MPI.send(fnames, tag=11)
                else:
                    fnames = MPI.recv(0, tag=11)
                MPI.wait()
                MPI_loop_size = MPI.set_loop(len(fnames))
                for mpi_ind in range(0, MPI_loop_size):
                    i = MPI.mpi_ind2ind(mpi_ind)
                    if i is not None:
                        _out = self.readsnap(fnames[i], return_pos, return_vel, part,
                                             1, xmin, xmax, ymin, ymax, zmin, zmax)
                        if return_pos == True and return_vel == True:
                            _pos, _vel = _out[0], _out[1]
                        elif return_pos == True and return_vel == False:
                            _pos = _out
                        elif return_pos == False and return_vel == True:
                            _vel = _out
                        if mpi_ind == 0:
                            poss = [_pos]
                            if return_vel == True:
                                vels = [_vel]
                        else:
                            poss.append(_pos)
                            if return_vel == True:
                                vels.append(_vel)
                    else:
                        if mpi_ind == 0:
                            poss = []
                            vels = []
                if len(poss) != 0:
                    pos = np.concatenate(poss)
                    if return_vel == True:
                        vel = np.concatenate(vels)
                else:
                    pos, vel = None, None
                if combine == True and MPI is not None:
                    if MPI.rank != 0:
                        if return_pos == True:
                            MPI.send(pos, to_rank=0, tag=11)
                        if return_vel == True:
                            MPI.send(vel, to_rank=0, tag=12)
                    else:
                        if return_pos == True:
                            poss = [pos]
                        if return_vel == True:
                            vels = [vel]
                        for i in range(1, MPI.size):
                            if return_pos == True:
                                _pos = MPI.recv(i, tag=11)
                                if _pos is not None:
                                    poss.append(_pos)
                            if return_vel == True:
                                _vel = MPI.recv(i, tag=12)
                                if _vel is not None:
                                    vels.append(_vel)
                        if return_pos == True:
                            pos = np.concatenate(poss)
                        if return_vel == True:
                            vel = np.concatenate(vels)
        # outputs
        if combine == True and MPI is not None:
            if MPI.rank == 0:
                if return_pos == True and return_vel == True:
                    return pos, vel
                elif return_pos == True and return_vel == False:
                    return pos
                elif return_pos == False and return_vel == True:
                    return vel
            else:
                if return_pos == True and return_vel == True:
                    return None, None
                elif return_pos == True and return_vel == False:
                    return None
                elif return_pos == False and return_vel == True:
                    return None
        else:
            if return_pos == True and return_vel == True:
                return pos, vel
            elif return_pos == True and return_vel == False:
                return pos
            elif return_pos == False and return_vel == True:
                return vel


    def clean(self):
        """Reinitialises the class."""
        self.__init__()
