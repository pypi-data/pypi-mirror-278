__version__ = '0.2.20'

try:
    from etiket_client.local.dao.app import dao_app_registerer
    from etiket_client.local.types import ProcTypes

    dao_app_registerer.register(__version__, ProcTypes.qDrive, __file__)
except Exception as e:
    print("Failed to update version information about the current session (qdrive). \nError : ", e)


from etiket_client import login, logout
from etiket_client.GUI.sync.app import launch_GUI as l_GUI
from etiket_client.settings.user_settings import user_settings

def launch_GUI():
    l_GUI()

from qdrive.dataset.dataset import dataset
