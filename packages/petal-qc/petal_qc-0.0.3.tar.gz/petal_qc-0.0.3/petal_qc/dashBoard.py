"""Test dashboard."""
import sys

try:
    import petal_qc
    
except ImportError:
    from pathlib import Path
    cwd = Path(__file__).parent.parent
    sys.path.append(cwd.as_posix())
    
from itkdb_gtk import dbGtkUtils
from itkdb_gtk import GetShipments
from itkdb_gtk import PetalReceptionTests
from itkdb_gtk import ITkDBlogin
from itkdb_gtk import CreateShipments
from itkdb_gtk import UploadTest
from itkdb_gtk import UploadMultipleTests
from itkdb_gtk import GlueWeight
from itkdb_gtk import UploadModuleIV
from itkdb_gtk import WireBondGui
