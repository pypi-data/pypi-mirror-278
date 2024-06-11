"""
azcamserver script for a mock system.

Command line options:
  -system azcam_mock
  -datafolder path_to_datafolder
  -cmdport azcamserver_port
"""

import os
import sys

import azcam
import azcam.server
from azcam.scripts.scripts import loadscripts

from azcam.logger import check_for_remote_logger

from azcam.tools.queue import Queue
from azcam.tools.controller import Controller
from azcam.tools.instrument import Instrument
from azcam.tools.tempcon import TempCon
from azcam.tools.display import Display
from azcam.tools.telescope import Telescope
from azcam.tools.exposure import Exposure
from azcam.cmdserver import CommandServer
from azcam.tools.focus import Focus
import azcam.shortcuts

from azcam.webtools.webserver import WebServer
from azcam.webtools.status.status import Status
from azcam.webtools.exptool.exptool import Exptool

# ****************************************************************
# parse command line arguments
# ****************************************************************
try:
    i = sys.argv.index("-system")
    systemname = sys.argv[i + 1]
except ValueError:
    systemname = "azcam_mock"
try:
    i = sys.argv.index("-datafolder")
    datafolder = sys.argv[i + 1]
except ValueError:
    datafolder = None
try:
    i = sys.argv.index("-cmdport")
    cmdport = int(sys.argv[i + 1])
except ValueError:
    cmdport = 2402


def setup():
    global systemname, datafolder, cmdport
    azcam.db.systemname = systemname
    azcam.db.systemfolder = os.path.dirname(__file__)
    azcam.db.systemfolder = azcam.utils.fix_path(azcam.db.systemfolder)
    azcam.db.datafolder = azcam.utils.get_datafolder(datafolder)
    azcam.db.servermode = azcam.db.systemname

    azcam.db.verbosity = 2

    # ****************************************************************
    # parameter file
    # ****************************************************************
    parfile = os.path.join(
        azcam.db.datafolder, "parameters", "parameters_server_mock.ini"
    )
    azcam.db.parameters.read_parfile(parfile)
    azcam.db.parameters.update_pars()

    # ****************************************************************
    # logging
    # ****************************************************************
    logfile = os.path.join(azcam.db.datafolder, "logs", "server.log")
    if check_for_remote_logger():
        azcam.db.logger.start_logging(logtype="23", logfile=logfile)
    else:
        azcam.db.logger.start_logging(logtype="1", logfile=logfile)

    # message
    azcam.log(f"Configuring {azcam.db.systemname}")

    # define command server
    cmdserver = CommandServer()
    cmdserver.port = cmdport
    cmdserver.logcommands = 0

    # ****************************************************************
    # tools
    # ****************************************************************
    controller = Controller()
    instrument = Instrument()
    instrument.enabled = 0
    telescope = Telescope()
    telescope.enabled = 0
    tempcon = TempCon()
    tempcon.enabled = 0
    display = Display()
    exposure = Exposure()
    focus = Focus()

    # ****************************************************************
    # scripts
    # ****************************************************************
    azcam.log("Loading azcam.scripts")
    loadscripts(["azcam.scripts"])

    # ****************************************************************
    # web server
    # ****************************************************************
    if 1:
        webserver = WebServer()
        webserver.port = cmdport + 1
        webserver.logcommands = 0
        webserver.logstatus = 0
        webserver.index = os.path.join(azcam.db.systemfolder, "index.html")
        webserver.message = f"for host {azcam.db.hostname}"
        webserver.datafolder = azcam.db.datafolder
        webserver.start()

        webstatus = Status(webserver)
        webstatus.message = "for a mock system"
        webstatus.initialize()

        exptool = Exptool(webserver)
        exptool.initialize()

        # queue = Queue()
        # queue.initialize()

        azcam.log("Started web apps")

    # ****************************************************************
    # start command server
    # ****************************************************************
    azcam.log(f"Starting cmdserver - listening on port {cmdserver.port}")
    cmdserver.start()


setup()
from azcam.cli import *
