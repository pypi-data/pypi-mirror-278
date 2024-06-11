"""
Contains the azcam database class for azcamserver.

There is only one instance of this class which is referenced as `azcam.db` and contains
temporary data for this current process.
"""

from azcam.database import AzcamDatabase
from azcam.parameters_server import ParametersServer
from azcam.cmdserver import CommandServer
from azcam.webtools.webserver import WebServer
from azcam.monitor.monitorinterface import AzCamMonitorInterface
from azcam.header import System


class AzcamDatabaseServer(AzcamDatabase):
    """
    The azcam database class.
    """

    parameters: ParametersServer
    """parameters object"""

    cmdserver: CommandServer
    """command server object"""

    webserver: WebServer
    """webserver object"""

    servermode: str
    """server mode"""

    monitor = AzCamMonitorInterface
    """azcammonitor object"""

    process_name = ""
    """process name for azcammonitor"""

    default_tool: str = "api"
    """default tool for remote commands"""

    system: System
    """system header object"""
