import warnings
from pylxd import Client as lxdclient, exceptions
warnings.filterwarnings("ignore")
class Cloud:
    def __init__(self, endpoint: str, crt, key, project="default") -> None:
        """Init the base client connection to LXD cloud"""
        self.endpoint = endpoint
        self.certificate = (crt, key)
        self.project = project
        self.base_client = lxdclient(self.endpoint, cert=self.certificate, project=self.project, verify=False)

    def networks(self):
        """Returns all existing networks on the cloud"""
        return self.base_client.networks.all()
    def instances(self):
        """Returns all existing instances on the cloud"""
        return self.base_client.instances.all()