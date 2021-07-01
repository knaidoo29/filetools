import numpy as np
import pygadgetreader as pyg

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


    def read(self, return_pos=True, return_vel=True, part='dm', xmin=None, xmax=None,
             ymin=None, ymax=None, zmin=None, zmax=None):
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
        """
        if self.info is None:
            # then we just read the entire thing.
            if return_pos == True:
                pos = pyg.readsnap(self.fname, 'pos', part, single=0)
            if return_vel == True:
                vel = pyg.readsnap(self.fname, 'vel', part, single=0)
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
        else:
            files_needed = self._is_file_in_range(xmin, xmax, ymin, ymax, zmin, zmax)
            for i in range(0, len(files_needed)):
                fname_chunk = self.fname + '.' + str(files_needed[i])
                if return_pos == True:
                    _pos = pyg.readsnap(fname_chunk, 'pos', part, single=1)
                if return_vel == True:
                    _vel = pyg.readsnap(fname_chunk, 'vel', part, single=1)
                # Truncate the data if we have position data.
                if return_pos == True:
                    mask = np.ones(len(_pos))
                    if xmin is not None:
                        cond = np.where(_pos[:, 0] < xmin)[0]
                        mask[cond] = 0.
                    if xmax is not None:
                        cond = np.where(_pos[:, 0] > xmax)[0]
                        mask[cond] = 0.
                    if ymin is not None:
                        cond = np.where(_pos[:, 1] < ymin)[0]
                        mask[cond] = 0.
                    if ymax is not None:
                        cond = np.where(_pos[:, 1] > ymax)[0]
                        mask[cond] = 0.
                    if zmin is not None:
                        cond = np.where(_pos[:, 2] < zmin)[0]
                        mask[cond] = 0.
                    if zmax is not None:
                        cond = np.where(_pos[:, 2] > zmax)[0]
                        mask[cond] = 0.
                    cond = np.where(mask == 1.)[0]
                    _pos = _pos[cond]
                    if return_vel == True:
                        _vel = _vel[cond]
                if i == 0:
                    pos = _pos
                    if return_vel == True:
                        vel = _vel
                else:
                    pos = np.concatenate([pos, _pos])
                    if return_vel == True:
                        vel = np.concatenate([vel, _vel])
                utils.progress_bar(i, len(files_needed), indexing=True, explanation='Reading from GADGET File')
        # outputs
        if return_pos == True and return_vel == True:
            return pos, vel
        elif return_pos == True and return_vel == False:
            return pos
        elif return_pos == False and return_vel == True:
            return vel


    def clean(self):
        """Reinitialises the class."""
        self.__init__()
