from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.log import info, setLogLevel

from parsgml import GmlManager
import argparse


def CmdParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--controller", nargs=2, default="172.17.0.2 6653")
    parser.add_argument("-t", "--topo", type=int, default=0)
    return parser


def get_topology(n_topo=0):
    manager = GmlManager()
    manager.parse()
    return manager.topologies[n_topo]


def run(topo, ip, port):
    info("*** Prepairing topology\n")
    topo.random_edges_weights()

    info("\n*** Start emulating ***\n")

    net = Mininet(controller=RemoteController)

    info("*** Adding controller\n")

    net.addController("c0", controller=RemoteController, ip=ip, port=port)

    switches = []
    
    for node in topo.nodes:
        info(f"*** Adding switch: S{node}\n")
        switches.append(net.addSwitch(f"S{node}", protocols="OpenFlow13", role="AR" if node < 5 else "DR"))

    for link in topo.edges:
        info(f"*** Adding link from: S{link.source}, to: S{link.target} | bw = {topo.matrix[link.source][link.target]}\n")
        net.addLink(switches[link.source], switches[link.target], bw=topo.matrix[link.source][link.target])

    net.start()
    CLI(net)

    net.stop()


def main():
    setLogLevel("info")
    args = CmdParser().parse_args()
    CONTROLLER_IP, CONTROLLER_PORT, N_TOPO = (
        args.controller[0],
        int(args.controller[1]),
        args.topo,
    )

    run(get_topology(N_TOPO), CONTROLLER_IP, CONTROLLER_PORT)


if __name__ == "__main__":
    main()
