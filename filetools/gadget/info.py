import pygadgetreader as pyg


def get_gadget_info(gfname):
    """Retrieves information of a simulation snapshot from the gadget file

    Parameters
    ----------
    gfname : str
        Gadget filename root.

    Returns
    -------
    partmass : float
        DM particle mass.
    boxsize : float
        Boxsize of the simulation.
    omegam : float
        Matter density.
    omegal : float
        Lambda density.
    h : float
        Hubble constant.
    npart : int
        Total number of particles.
    """
    partmass = pyg.readheader(gfname, 'massTable')[1]
    boxsize = pyg.readheader(gfname, 'boxsize')
    omegam = pyg.readheader(gfname, 'O0')
    omegal = pyg.readheader(gfname, 'Ol')
    h = pyg.readheader(gfname, 'h')
    npart = pyg.readheader(gfname, 'npartTotal')[1]
    return omegam, omegal, h, boxsize, partmass, npart
