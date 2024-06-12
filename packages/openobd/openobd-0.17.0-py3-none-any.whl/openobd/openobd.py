#!/usr/bin/env python3
import grpc
import os

from openobd_protocol import RemoteDiagnosticServices_pb2_grpc as grpcService
from openobd_protocol import BusConfiguration_pb2 as grpcBusConfiguration
from openobd_protocol import Status_pb2 as grpcStatus
from openobd_protocol import BasicResponse_pb2 as grpcBasicResponse
from openobd_protocol.SessionController import Session_pb2 as grpcSession
from openobd_protocol.SessionController import SessionServices_pb2_grpc as grpcSessionControllerService
from openobd_protocol.CAN import Isotp_pb2 as grpcIsotp
from openobd_protocol.CAN import CanServices_pb2_grpc as grpcCanService
from openobd_protocol.UserInterface import UserInterface_pb2 as grpcUserInterface
from openobd_protocol.UserInterface import UserInterfaceServices_pb2_grpc as grpcUserInterfaceService
from openobd_protocol.ConnectionMonitor import ConnectionInformation_pb2 as grpcConnectionInformation
from openobd_protocol.ConnectionMonitor import ConnectionMonitorServices_pb2_grpc as grpcConnectionMonitorService


from typing import Iterator


def _is_valid_response(response, response_object):
    try:
        if response is not None:
            assert isinstance(response, response_object), f"Expected {type(response).__name__} object, received: {type(response_object).__name__}"
            return True
    except AssertionError:
        pass
    return False


class GrpcChannel(object):

    grpc_host = None
    grpc_port = 443
    connected = False
    channel = None

    def _connect(self):
        if not self.connected:
            ''' Check if local grpc-proxy is running '''
            if self.grpc_port == 443:
                self.channel = grpc.secure_channel(self.grpc_host, grpc.ssl_channel_credentials())
            else:
                ''' NOTE: Only use this for development purposes '''
                self.channel = grpc.insecure_channel('{}:{}'.format(self.grpc_host, self.grpc_port))

            ''' TODO: Exceptions and stuff '''
            self.connected = True


class OpenOBDSession(GrpcChannel):

    session_info = None

    """
    Client for gRPC functionality
    """
    def __init__(self, session_info: grpcSession.SessionInfo, grpc_port=443):
        self.session_info = session_info

        self.grpc_host = self.session_info.grpc_endpoint
        self.grpc_port = grpc_port
        self._connect()

        self.rds = grpcService.RemoteDiagnosticServicesStub(self.channel)
        self.can = grpcCanService.CanServicesStub(self.channel)
        self.ui = grpcUserInterfaceService.UserInterfaceServicesStub(self.channel)
        self.connector_monitor = grpcConnectionMonitorService.ConnectionMonitorServicesStub(self.channel)

    def id(self):
        return self.session_info.id

    def _metadata(self):
        metadata = []
        metadata.append(("authorization", "Bearer {}".format(self.session_info.authentication_token)))
        metadata = tuple(metadata)
        return metadata

    def configure_bus(self, bus_configuration: grpcBusConfiguration.BusConfiguration) -> grpcStatus.Status:
        """
        Client function to call the rpc
        :param bus_configuration:
        :return: Status of the bus configuration request
        """
        return self.rds.configureBus(request=bus_configuration, metadata=self._metadata())

    def configure_buses(self, bus_configurations: Iterator[grpcBusConfiguration.BusConfiguration]) -> grpcStatus.Status:
        """
        client function to set up multiple buses
        :param bus_configurations: An iterator containing the buses that are requested to be set
        :return: Status of the bus configuration request
        """
        return self.rds.configureBuses(bus_configurations, metadata=self._metadata())

    def open_channel(self, isotp_messages: Iterator[grpcIsotp.IsotpMessage]) -> Iterator[grpcIsotp.IsotpMessage]:
        """
        Client function to send and receive a stream of ISOTP format messages
        :param isotp_messages: An iterator containing the ISOTP messages that are requested to be sent
        :return: A list of ISOTP response messages
        """
        return self.can.openChannel(isotp_messages, metadata=self._metadata())

    def control(self, user_interface_messages: Iterator[grpcUserInterface.UserInterface]) -> grpcUserInterface.UserInterface:
        """
        Client function to control various components of the user interface
        :param user_interface_messages: An iterator containing the user interface message to be controlled
        :return: User interface component with output or answers depending upon the control fields sent
        """
        return self.ui.control(user_interface_messages, metadata=self._metadata())

    def get_connector_information(self) -> grpcConnectionInformation.ConnectorInformation:
        """
        Client function to retrieve connector information at the give instant
        :return: gRPC Connector Information object
        """
        return self.connector_monitor.getConnectorInformation(request=grpcBasicResponse.EmptyMessage(), metadata=self._metadata())

    def stream_connector_information(self) -> Iterator[grpcConnectionInformation.ConnectorInformation]:
        """
        Client function to stream connector information every second until server is shutdown
        :return: An iterator consisting of gRPC Connector Information object
        """
        return self.connector_monitor.streamConnectorInformation(request=grpcBasicResponse.EmptyMessage(), metadata=self._metadata())

    def finish(self, service_result: grpcBasicResponse.ServiceResult) -> grpcStatus.Status:
        """
        Client function to finish the procedure and close the session from client side
        :param service_result: The result to be set indicating if the desired diagnostic procedure was successfully carried out
        :return: Status of the service request
        """
        return self.rds.finish(service_result, metadata=self._metadata())


class OpenOBD(object):
    """
    Client for gRPC functionality
    """
    session_controller = None

    def __init__(self, **kwargs):
        """
        Initialize openOBD with provided partner credentials

        Keyword Args:
            client_id(str):
            client_secret(str):
            partner_api_key(str):
            cluster_id(str):
            grpc_host(str):
            grpc_port(int):
        """
        self.session_controller = OpenOBDSessionController(**kwargs)

    def start_session_on_connection(self, connection_uuid: str) -> OpenOBDSession:
        response = self.session_controller.start_session_on_connection(grpcSession.ConnectionId(id=connection_uuid))
        return OpenOBDSession(response)

    # TODO: To be implemented
    def start_session_on_connector(self, connector_uuid: str) -> OpenOBDSession:
        pass

    # TODO: To be implemented
    def start_session_on_ticket(self, ticket_id: str) -> OpenOBDSession:
        pass

    def get_session(self, session_id: grpcSession.SessionId) -> grpcSession.SessionInfo:
        return self.session_controller.get_session(session_id)

    def delete_session(self, session_id: grpcSession.SessionId) -> grpcSession.SessionInfo:
        return self.session_controller.delete_session(session_id)

    def get_session_list(self) -> grpcSession.SessionInfoList:
        return self.session_controller.get_session_list()


class OpenOBDSessionController(GrpcChannel):

    client_id = None
    client_secret = None
    partner_api_key = None
    cluster_id = None

    session_controller_token = None

    """
    gRPC Client for SessionController
    """
    def __init__(self, **kwargs):
        """Initialize openobd session controller

        Keyword Args:
            client_id(str):
            client_secret(str):
            partner_api_key(str):
            cluster_id(str):
            grpc_host(str):
            grpc_port(int):
        """
        self.client_id = kwargs.get('client_id') if 'client_id' in kwargs else os.environ.get("OPENOBD_PARTNER_CLIENT_ID")
        self.client_secret = kwargs.get('client_secret') if 'client_secret' in kwargs else os.environ.get("OPENOBD_PARTNER_CLIENT_SECRET")
        self.partner_api_key = kwargs.get('partner_api_key') if 'partner_api_key' in kwargs else os.environ.get("OPENOBD_PARTNER_API_KEY")
        self.cluster_id = kwargs.get('cluster_id') if 'cluster_id' in kwargs else os.environ.get("OPENOBD_CLUSTER_ID")

        self.grpc_host = kwargs.get('grpc_host') if 'grpc_host' in kwargs else os.environ.get("OPENOBD_GRPC_HOST")
        self.grpc_port = kwargs.get('grpc_port') if 'grpc_port' in kwargs else 443
        self._connect()

        self.session_controller = grpcSessionControllerService.SessionServicesStub(self.channel)
        self._get_session_controller_token()

    def _metadata(self):
        metadata = []
        if self.session_controller_token:
            metadata.append(("session", "{}".format(self.session_controller_token)))
        metadata = tuple(metadata)
        return metadata

    def _get_session_controller_token(self) -> grpcSession.SessionToken:
        # retrieve the session token and add it to the metadata
        response = self.session_controller.getSessionToken(
            grpcSession.Authenticate(
                client_id=self.client_id,
                client_secret=self.client_secret,
                api_key=self.partner_api_key,
                cluster_id=self.cluster_id
            ))  # type: grpcSession.SessionToken

        # before setting the session token in the metadata ensure session token exists in the response
        if _is_valid_response(response, grpcSession.SessionToken):
            self.session_controller_token = response.token
        return response

    def start_session_on_connection(self, connection_id: grpcSession.ConnectionId) -> grpcSession.SessionInfo:

        return self.session_controller.startSessionOnConnection(connection_id, metadata=self._metadata())

    # TODO: Add start_session_on_connector / start_session_on_ticket

    def get_session(self, session_id: grpcSession.SessionId) -> grpcSession.SessionInfo:

        return self.session_controller.getSession(session_id, metadata=self._metadata())

    def delete_session(self, session_id: grpcSession.SessionId) -> grpcSession.SessionInfo:
        """
        Manager function to interrupt active session
        :param session_id:
        :return: interrupted Session object
        """
        return self.session_controller.deleteSession(session_id, metadata=self._metadata())

    def get_session_list(self) -> grpcSession.SessionInfoList:
        """
        Manager function to request a list of active sessions
        :return: List of sessions
        """

        return self.session_controller.getSessionList(request=grpcBasicResponse.EmptyMessage(), metadata=self._metadata())


