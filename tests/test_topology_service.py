"""
=============================================================

ConfigVista AI

Topology Service Tests

=============================================================
"""

from enterprise.models import (
    Device,
    TopologyLink,
)

from enterprise.services.inventory_service import (
    InventoryService,
)

from enterprise.services.topology_service import (
    TopologyService,
)


# ==========================================================
# Fixtures
# ==========================================================

def build_inventory():

    inventory = InventoryService()

    d1 = Device(hostname="CORE01")
    d2 = Device(hostname="DIST01")
    d3 = Device(hostname="ACCESS01")

    inventory.register_device(d1)
    inventory.register_device(d2)
    inventory.register_device(d3)

    link1 = TopologyLink(
        source_device_id=d1.device_id,
        destination_device_id=d2.device_id,
        source_hostname=d1.hostname,
        destination_hostname=d2.hostname,
    )

    link2 = TopologyLink(
        source_device_id=d2.device_id,
        destination_device_id=d3.device_id,
        source_hostname=d2.hostname,
        destination_hostname=d3.hostname,
    )

    inventory.register_topology_link(link1)
    inventory.register_topology_link(link2)

    return (
        inventory,
        d1,
        d2,
        d3,
    )


# ==========================================================
# Constructor
# ==========================================================

def test_constructor():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert topology.graph_built

    assert topology.node_count == 3

    assert topology.edge_count == 2


def test_validate():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert topology.validate()


def test_rebuild():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    topology.rebuild()

    assert topology.graph_built

    assert topology.validate()


# ==========================================================
# Device Queries
# ==========================================================

def test_has_device():

    inventory, d1, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert topology.has_device(
        d1.device_id
    )


def test_unknown_device():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert not topology.has_device(
        "UNKNOWN"
    )


def test_neighbor_count():

    inventory, _, d2, _ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert topology.get_degree(
        d2.device_id
    ) == 2


def test_neighbor_ids():

    inventory, d1, d2, _ = build_inventory()

    topology = TopologyService(
        inventory
    )

    neighbors = topology.get_neighbor_ids(
        d1.device_id
    )

    assert d2.device_id in neighbors


def test_neighbors():

    inventory, d1, d2, _ = build_inventory()

    topology = TopologyService(
        inventory
    )

    neighbors = topology.get_neighbors(
        d1.device_id
    )

    assert len(neighbors) == 1

    assert neighbors[0].hostname == d2.hostname

# ==========================================================
# Connected Components
# ==========================================================

def test_connected_components():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    components = topology.connected_components()

    assert len(components) == 1

    assert len(components[0]) == 3


def test_connected_component_count():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert topology.connected_component_count == 1


# ==========================================================
# Isolated Devices
# ==========================================================

def test_isolated_devices_empty():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    isolated = topology.isolated_devices()

    assert len(isolated) == 0


def test_isolated_device_detection():

    inventory, *_ = build_inventory()

    isolated = Device(
        hostname="EDGE99"
    )

    inventory.register_device(
        isolated
    )

    topology = TopologyService(
        inventory
    )

    isolated_devices = topology.isolated_devices()

    assert len(isolated_devices) == 1

    assert isolated_devices[0].hostname == "EDGE99"


def test_isolated_device_count():

    inventory, *_ = build_inventory()

    isolated = Device(
        hostname="EDGE100"
    )

    inventory.register_device(
        isolated
    )

    topology = TopologyService(
        inventory
    )

    assert topology.isolated_device_count == 1


# ==========================================================
# Shortest Path
# ==========================================================

def test_has_path():

    inventory, d1, _, d3 = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert topology.has_path(
        d1.device_id,
        d3.device_id,
    )


def test_shortest_path():

    inventory, d1, d2, d3 = build_inventory()

    topology = TopologyService(
        inventory
    )

    path = topology.shortest_path(
        d1.device_id,
        d3.device_id,
    )

    assert len(path) == 3

    assert path[0] == d1.device_id

    assert path[1] == d2.device_id

    assert path[2] == d3.device_id


def test_same_source_destination():

    inventory, d1, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    path = topology.shortest_path(
        d1.device_id,
        d1.device_id,
    )

    assert len(path) == 1

    assert path[0] == d1.device_id


def test_unknown_source():

    inventory, _, _, d3 = build_inventory()

    topology = TopologyService(
        inventory
    )

    path = topology.shortest_path(
        "UNKNOWN",
        d3.device_id,
    )

    assert path == []


def test_unknown_destination():

    inventory, d1, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    path = topology.shortest_path(
        d1.device_id,
        "UNKNOWN",
    )

    assert path == []


def test_no_path():

    inventory, d1, *_ = build_inventory()

    isolated = Device(
        hostname="ACCESS99"
    )

    inventory.register_device(
        isolated
    )

    topology = TopologyService(
        inventory
    )

    assert topology.shortest_path(
        d1.device_id,
        isolated.device_id,
    ) == []

    assert not topology.has_path(
        d1.device_id,
        isolated.device_id,
    )

# ==========================================================
# Critical Devices
# ==========================================================

def test_critical_devices():

    inventory, _, d2, _ = build_inventory()

    topology = TopologyService(
        inventory
    )

    critical = topology.critical_devices(
        minimum_degree=2
    )

    assert len(critical) == 1

    assert critical[0].device_id == d2.device_id


def test_no_critical_devices():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    critical = topology.critical_devices(
        minimum_degree=5
    )

    assert critical == []


# ==========================================================
# Graph Statistics
# ==========================================================

def test_graph_statistics():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    stats = topology.graph_statistics()

    assert stats["nodes"] == 3

    assert stats["edges"] == 2

    assert stats["connected_components"] == 1

    assert stats["isolated_devices"] == 0

    assert stats["graph_valid"]


def test_summary():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    summary = topology.summary()

    assert "inventory" in summary

    assert "graph" in summary

    assert "critical_devices" in summary

    assert summary["graph_built"]


# ==========================================================
# Properties
# ==========================================================

def test_node_count():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert len(topology) == 3


def test_edge_count():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert topology.edge_count == 2


def test_repr():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    representation = repr(
        topology
    )

    assert "TopologyService" in representation

    assert "nodes=3" in representation


# ==========================================================
# Bidirectional Links
# ==========================================================

def test_bidirectional_neighbors():

    inventory, d1, d2, _ = build_inventory()

    topology = TopologyService(
        inventory
    )

    neighbors = topology.get_neighbor_ids(
        d2.device_id
    )

    assert d1.device_id in neighbors


# ==========================================================
# Rebuild Consistency
# ==========================================================

def test_multiple_rebuilds():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    topology.rebuild()

    topology.rebuild()

    topology.rebuild()

    assert topology.node_count == 3

    assert topology.edge_count == 2

    assert topology.validate()


# ==========================================================
# Empty Inventory
# ==========================================================

def test_empty_inventory():

    inventory = InventoryService()

    topology = TopologyService(
        inventory
    )

    assert topology.node_count == 0

    assert topology.edge_count == 0

    assert topology.validate()

    assert topology.connected_components() == []

    assert topology.isolated_devices() == []

    assert topology.graph_statistics()["nodes"] == 0


# ==========================================================
# Invalid Links
# ==========================================================

def test_invalid_topology_link():

    inventory = InventoryService()

    device = Device(
        hostname="CORE01"
    )

    inventory.register_device(
        device
    )

    bad_link = TopologyLink(
        source_device_id=device.device_id,
        destination_device_id="UNKNOWN",
    )

    inventory.register_topology_link(
        bad_link
    )

    topology = TopologyService(
        inventory
    )

    assert not topology.validate()

    assert len(topology.invalid_links) == 1


# ==========================================================
# Graph Stability
# ==========================================================

def test_graph_build_flag():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert topology.graph_built


def test_rebuild_preserves_graph():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    before = topology.graph_statistics()

    topology.rebuild()

    after = topology.graph_statistics()

    assert before == after


def test_neighbor_lookup_unknown():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert topology.get_neighbors(
        "UNKNOWN"
    ) == []


def test_neighbor_ids_unknown():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert topology.get_neighbor_ids(
        "UNKNOWN"
    ) == []


def test_degree_unknown():

    inventory, *_ = build_inventory()

    topology = TopologyService(
        inventory
    )

    assert topology.get_degree(
        "UNKNOWN"
    ) == 0