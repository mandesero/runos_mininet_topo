from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.log import info, setLogLevel

from parsgml import GmlManager
import argparse
import time


def CmdParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--controller", nargs=2, default="127.0.0.1 6653")
    parser.add_argument("-t", "--topo", type=int, default=0)
    return parser


def get_topology(n_topo=0):
    manager = GmlManager()
    manager.parse()
    return manager.topologies[n_topo]

class T:
    def __init__(self, topo, ip, port, unlinks):
        info("*** Prepairing topology\n")

        info("\n*** Start emulating ***\n")

        net = Mininet(controller=RemoteController)
        self.net = net

        info("*** Adding controller\n")

        net.addController("cr0", controller=RemoteController, ip=ip, port=port)

        switches = []
        
        for node in topo.nodes:
            info(f"*** Adding switch: Sw{node + 1}\n")
            switches.append(net.addSwitch(f"Sw{node + 1}", dpid=f"{(node + 1)}", protocols="OpenFlow13"))

        for link in topo.edges:
            info(f"*** Adding link from: Sw{link.source + 1}, to: Sw{link.target + 1}")
            net.addLink(switches[link.source], switches[link.target])

        net.start()
        info("Waiting (5sec) ...\n")
        time.sleep(5)
        try:
            for i in unlinks:
                edge = topo.edges[i]
                info(f"*** Del link between: Sw{link.source + 1}, to: Sw{link.target + 1}")
                net.delLinkBetween(switches[link.source], switches[link.target])
                time.sleep(1)
        except:
            pass

        CLI(net)

    def __del__(self):
        self.net.stop()


def get_unlinks(n_topo):
    unlinks = open("unlinks.txt", "r")
    tmp = list(map(int, unlinks.readlines()[n_topo].split(',')))
    info(f"{tmp}")
    unlinks.close()
    return tmp



def main():
    setLogLevel("info")
    args = CmdParser().parse_args()
    CONTROLLER_IP, CONTROLLER_PORT, N_TOPO = (
        args.controller[0],
        int(args.controller[1]),
        args.topo,
    )
    unlinks = get_unlinks(N_TOPO)

    T(get_topology(N_TOPO), CONTROLLER_IP, CONTROLLER_PORT, unlinks)


if __name__ == "__main__":
    main()
