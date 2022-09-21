from pyvis.network import Network as net

class Graph:
    def __init__(self, lxd, height, width, bgcolor) -> None:
        self.lxd = lxd
        self.g = net(height=height, width=width, bgcolor=bgcolor)
        self.instances_networks = {}

    def _draw_instance(self, instance):
        conf = instance.config
        state = instance.state()
        devices = instance.expanded_devices
        self.instances_networks[conf["volatile.uuid"]] = []
        title = {
            "Location": instance.location,
            "Status": conf["volatile.last_state.power"],
            "IPs": [],
            "Image": f"{conf['image.os']}({conf['image.release']})",
            }

        for interface in state.network:
            if interface != "lo":
                title["IPs"].append(f"{interface}: {[address['address'] for address in state.network[interface]['addresses']]}")        

        for device in devices:
            if devices[device]["type"] == "nic":
                try:
                    self.instances_networks[conf["volatile.uuid"]].append(devices[device]["network"])
                except KeyError:
                    self.instances_networks[conf["volatile.uuid"]].append(devices[device]["parent"])
                else:
                    pass
        self.g.add_node(conf["volatile.uuid"], instance.name, title=str(title).replace(", ", "\n").replace("{", "").replace("}", "").replace("'", ""))
    
    def _draw_network(self, network):
        used_networks = []
        conf = network.config
        for networks in self.instances_networks:
            used_networks += self.instances_networks[networks]

        if network.name in used_networks:
            color = "green"
        else:
            color = "grey"
        
        if conf:
            title = str(conf).replace(", ", "\n").replace("{", "").replace("}", "").replace("'", "")
            self.g.add_node(network.name, network.name,
                            shape="hexagone", color=color, title=title)
        else:
            self.g.add_node(network.name, network.name,
                            shape="hexagone", color=color)

    def _draw_links(self, instance):
        for network in self.instances_networks[instance]:
            self.g.add_edge(instance, network)

        for network in self.lxd.networks():
            try:
                # self.g.add_node(network.config["network"],network.config["network"])
                title = str(network.config).replace(", ", "\n").replace("{", "").replace("}", "").replace("'", "")
                self.g.add_node(network.config["network"], network.config["network"],
                            shape="hexagone", color="green", title=title)
                self.g.add_edge(network.name, network.config["network"])
            except KeyError:
                pass

    def draw(self):
        for instance in self.lxd.instances():
            self._draw_instance(instance)
        for network in self.lxd.networks():
            self._draw_network(network)
        for instance in self.instances_networks:
            self._draw_links(instance)
        self.graph = self.g.generate_html()
        return self.graph
