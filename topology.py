from parsgml import GmlManager
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController, OVSSwitch
from mininet.log import info, setLogLevel
from time import sleep
import sys


class TopologyManager:
    def __init__(self):
        tmp = GmlManager()
        tmp.parse()
        self.topologies = tmp.topologies
        with open("unlinks.txt", "r") as unlinks_file:
            unlinks = map(str.strip, unlinks_file.readlines())
            self.unlinks = [list(map(int, t.split(","))) for t in unlinks]

        self.net = None
        self.cnt_name = None

    def addController(self, name, ip, port):
        info(f"*** Adding controller: {name} | {ip = } | {port = }\n")
        self.cnt_name = name
        return self.net.addController(
            name=name, controller=RemoteController, ip=ip, port=int(port)
        )

    def addSwitch(self, name, dpid, proto="OpenFlow13"):
        info(f"*** Adding switch: {name} | {dpid = }\n")
        return self.net.addSwitch(
            name=name, dpid=str(dpid), protocols=proto, cls=OVSSwitch
        )

    def addLink(self, S1, S2):
        info(f"*** Adding link between: {int(S1.dpid)} | {int(S2.dpid)}\n")
        self.net.addLink(S1, S2)

    def delLink(self, S1, S2):
        info(f"*** Delete link between: {int(S1.dpid)} | {int(S2.dpid)}\n")
        self.net.delLinkBetween(S1, S2)

    def run(self, ip, port, n_topo):
        setLogLevel("info")
        info("*** Prepairing topology\n")
        info("\n*** Start emulating ***\n")

        self.net = Mininet(controller=RemoteController)

        topo = self.topologies[n_topo]
        unlinks = self.unlinks[n_topo]

        c0 = self.addController("C", ip, port)

        switches = []
        for i, node in enumerate(topo.nodes):
            switches.append(self.addSwitch(f"S{i + 1}", i + 1))

        for edge in topo.edges:
            self.addLink(
                switches[edge.source],
                switches[edge.target],
            )

        for sw in switches:
            sw.start([c0])

        self.net.start()

        for i in range(1, 20):
            info(f"Sleep for {i}\n")
            sleep(1)

        for i in unlinks:
            edge = topo.edges[i]
            self.delLink(
                switches[edge.source],
                switches[edge.target],
            )
            sleep(1)

        CLI(self.net)

    def __del__(self):
        self.net.stop()


if __name__ == "__main__":
    N_TOPO = int(sys.argv[1])
    manager = TopologyManager()
    manager.run("127.0.0.1", "6653", N_TOPO)
