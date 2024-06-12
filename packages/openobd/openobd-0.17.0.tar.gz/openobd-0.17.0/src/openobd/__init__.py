# Copyright (c) 2024 Jifeline Networks B.V.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""OpenOBD Python Client implementiation"""

try:
    # pylint: disable=ungrouped-imports
    from openobd._metadata import __version__
except ImportError:
    __version__ = "dev0"

'''Import the message definitions from openobd_protocol '''
from openobd_protocol.BusConfiguration_pb2 import *
from openobd_protocol.CAN.Isotp_pb2 import *
from openobd_protocol.UserInterface.UserInterface_pb2 import *
from openobd_protocol.SessionController.Session_pb2 import *
from openobd_protocol.ConnectionMonitor.ConnectionInformation_pb2 import *
from openobd_protocol.Status_pb2 import *

'''Import the openOBD client class'''
from .openobd import OpenOBD as OpenOBD
from .openobd import OpenOBDSession as OpenOBDSession
from .openobd import OpenOBDSessionController as OpenOBDSessionController

''' Lastly import openobd_utils (needs to be last, since it imports parts of this openobd library) '''
from openobd_utils import *
