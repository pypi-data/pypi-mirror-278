"""petal_qc python module."""
__version__ = "0.0.3"


def coreMetrology():
    """Launches the Core metrology analysis ahd PDB script."""
    from .metrology.coreMetrology import main
    main()

def coreThermal():
    """Launches the Core thermal analysis ahd PDB script."""
    from .thermal.coreThermal import main
    main()


def bustapeReport():
    """Launches the Core metrology analysis ahd PDB script."""
    from .BTreport.bustapeReport import main
    main()

