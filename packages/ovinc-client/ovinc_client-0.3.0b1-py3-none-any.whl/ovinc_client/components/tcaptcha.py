from ovinc_client.components.base import Component, Endpoint
from ovinc_client.constants import RequestMethodEnum


class TCaptcha(Component):
    """
    TCaptcha
    """

    def __init__(self, client, base_url: str):
        self.verify_ticket = VerifyTicketEndpoint(client, base_url)


class VerifyTicketEndpoint(Endpoint):
    """
    Verify Ticket
    """

    method = RequestMethodEnum.POST.value
    path = "/tcaptcha/check/"
