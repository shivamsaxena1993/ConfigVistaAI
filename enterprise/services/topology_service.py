"""
=============================================================

ConfigVista AI

Enterprise Topology Service

Artifact-2

Enterprise Topology Engine

=============================================================
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict
from typing import Set
from typing import List
from collections import deque

from enterprise.models import (
    DeviceId,
    TopologyLinkId,
)

from enterprise.services.inventory_service import (
    InventoryService,
)


# ============================================================
# INTERNAL GRAPH EDGE
# ============================================================


@dataclass(slots=True)
class GraphEdge:
    """
    Lightweight graph edge used internally.

    The graph engine intentionally does not work directly
    with Enterprise TopologyLink objects.

    This keeps graph algorithms independent from future
    changes to enterprise models.
    """

    source: DeviceId

    destination: DeviceId

    topology_link_id: TopologyLinkId

    weight: float = 1.0

    operational: bool = True


# ============================================================
# TOPOLOGY SERVICE
# ============================================================


class TopologyService:
    """
    Enterprise Topology Graph Engine.

    Responsibilities
    ----------------

    • Build graph from InventoryService

    • Maintain adjacency map

    • Graph validation

    • Neighbor lookup

    • Path traversal (future)

    • Blast Radius (future)

    • Graph statistics (future)
    """

    # --------------------------------------------------------
    # Constructor
    # --------------------------------------------------------

    def __init__(
        self,
        inventory: InventoryService,
    ):

        self.inventory = inventory

        #
        # Device lookup
        #

        self.device_lookup: Dict[
            DeviceId,
            object,
        ] = {}

        #
        # Graph edges
        #

        self.edges: List[GraphEdge] = []

        #
        # Adjacency
        #

        self.adjacency: Dict[
            DeviceId,
            Set[DeviceId],
        ] = defaultdict(set)

        #
        # Reverse adjacency
        #

        self.reverse_adjacency: Dict[
            DeviceId,
            Set[DeviceId],
        ] = defaultdict(set)

        #
        # Validation
        #

        self.invalid_links = []

        self.graph_built = False

        #
        # Build graph immediately
        #

        self.build_graph()

    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def rebuild(self) -> None:
        """
        Rebuild graph from inventory.

        Useful after topology discovery or
        inventory synchronization.
        """

        self.edges.clear()

        self.adjacency.clear()

        self.reverse_adjacency.clear()

        self.invalid_links.clear()

        self.graph_built = False

        self.build_graph()

    # --------------------------------------------------------

    def build_graph(self) -> None:
        """
        Convert Enterprise Inventory into
        an in-memory graph.
        """

        #
        # Device lookup
        #

        self.device_lookup = dict(
            self.inventory.devices
        )

        #
        # Build graph edges
        #

        for topology in self.inventory.topology_links.values():

            source = topology.source_device_id

            destination = topology.destination_device_id

            #
            # Ignore incomplete links
            #

            if source is None or destination is None:

                self.invalid_links.append(
                    topology.link_id
                )

                continue

            #
            # Ignore unknown devices
            #

            if source not in self.device_lookup:

                self.invalid_links.append(
                    topology.link_id
                )

                continue

            if destination not in self.device_lookup:

                self.invalid_links.append(
                    topology.link_id
                )

                continue

            edge = GraphEdge(
                source=source,
                destination=destination,
                topology_link_id=topology.link_id,
                operational=(
                    topology.operational_status.upper()
                    == "UP"
                ),
            )

            self.edges.append(edge)

            #
            # Populate adjacency
            #

            self.adjacency[source].add(
                destination
            )

            self.reverse_adjacency[
                destination
            ].add(
                source
            )

            #
            # Bidirectional links
            #

            if topology.bidirectional:

                self.adjacency[
                    destination
                ].add(
                    source
                )

                self.reverse_adjacency[
                    source
                ].add(
                    destination
                )

        self.graph_built = True

    # --------------------------------------------------------

    def validate(self) -> bool:
        """
        Basic graph validation.

        Returns
        -------
        True

            Graph is valid

        False

            Invalid references discovered
        """

        return len(self.invalid_links) == 0

    # --------------------------------------------------------
    # Device Queries
    # --------------------------------------------------------

    def has_device(
        self,
        device_id: DeviceId,
    ) -> bool:
        """
        Returns True when a device exists in
        the topology graph.
        """

        return device_id in self.device_lookup

    # --------------------------------------------------------

    def get_neighbors(
        self,
        device_id: DeviceId,
    ) -> list:
        """
        Return neighboring device objects.

        Unknown devices return an empty list.
        """

        if device_id not in self.adjacency:
            return []

        neighbors = []

        for neighbor_id in sorted(self.adjacency[device_id]):

            device = self.device_lookup.get(
                neighbor_id
            )

            if device is not None:
                neighbors.append(device)

        return neighbors

    # --------------------------------------------------------

    def get_neighbor_ids(
        self,
        device_id: DeviceId,
    ) -> list[DeviceId]:
        """
        Returns only neighbor IDs.
        """

        return list(
            sorted(
                self.adjacency.get(
                    device_id,
                    set(),
                )
            )
        )

    # --------------------------------------------------------

    def get_degree(
        self,
        device_id: DeviceId,
    ) -> int:
        """
        Graph degree of a node.
        """

        return len(
            self.adjacency.get(
                device_id,
                set(),
            )
        )

    # --------------------------------------------------------
    # DFS Helpers
    # --------------------------------------------------------

    def _dfs(
        self,
        device_id: DeviceId,
        visited: set,
        component: list,
    ) -> None:

        visited.add(device_id)

        component.append(device_id)

        for neighbor in self.adjacency.get(
            device_id,
            set(),
        ):

            if neighbor not in visited:

                self._dfs(
                    neighbor,
                    visited,
                    component,
                )

    # --------------------------------------------------------
    # Connected Components
    # --------------------------------------------------------

    def connected_components(
        self,
    ) -> list[list[DeviceId]]:
        """
        Return all connected components
        within the enterprise graph.
        """

        visited = set()

        components = []

        for device_id in self.device_lookup:

            if device_id in visited:
                continue

            component = []

            self._dfs(
                device_id,
                visited,
                component,
            )

            components.append(component)

        return components

    # --------------------------------------------------------
    # Isolated Devices
    # --------------------------------------------------------

    def isolated_devices(
        self,
    ) -> list:
        """
        Devices without any topology
        relationships.
        """

        isolated = []

        for device_id, device in self.device_lookup.items():

            if self.get_degree(device_id) == 0:

                isolated.append(device)

        return isolated

    # --------------------------------------------------------
    # Graph Properties
    # --------------------------------------------------------

    @property
    def node_count(
        self,
    ) -> int:

        return len(
            self.device_lookup
        )

    # --------------------------------------------------------

    @property
    def edge_count(
        self,
    ) -> int:

        return len(
            self.edges
        )

    # --------------------------------------------------------

    @property
    def connected_component_count(
        self,
    ) -> int:

        return len(
            self.connected_components()
        )

    # --------------------------------------------------------

    @property
    def isolated_device_count(
        self,
    ) -> int:

        return len(
            self.isolated_devices()
        )
    
    # --------------------------------------------------------
    # Path Discovery (Breadth First Search)
    # --------------------------------------------------------

    def has_path(
        self,
        source: DeviceId,
        destination: DeviceId,
    ) -> bool:
        """
        Returns True if a path exists between
        two devices.
        """

        return len(
            self.shortest_path(
                source,
                destination,
            )
        ) > 0

    # --------------------------------------------------------

    def shortest_path(
        self,
        source: DeviceId,
        destination: DeviceId,
    ) -> list[DeviceId]:
        """
        Compute the shortest path using BFS.

        Returns an empty list when no path exists.
        """

        if source not in self.device_lookup:
            return []

        if destination not in self.device_lookup:
            return []

        if source == destination:
            return [source]

        visited = {source}

        queue = deque([(source, [source])])

        while queue:

            current, path = queue.popleft()

            for neighbor in self.adjacency.get(
                current,
                set(),
            ):

                if neighbor in visited:
                    continue

                new_path = path + [neighbor]

                if neighbor == destination:
                    return new_path

                visited.add(neighbor)

                queue.append(
                    (
                        neighbor,
                        new_path,
                    )
                )

        return []

    # --------------------------------------------------------
    # Critical Device Discovery
    # --------------------------------------------------------

    def critical_devices(
        self,
        minimum_degree: int = 3,
    ) -> list:
        """
        Returns devices having a graph degree
        greater than or equal to minimum_degree.
        """

        critical = []

        for device_id, device in self.device_lookup.items():

            if (
                self.get_degree(device_id)
                >= minimum_degree
            ):

                critical.append(device)

        return sorted(
            critical,
            key=lambda d: self.get_degree(
                d.device_id
            ),
            reverse=True,
        )

    # --------------------------------------------------------
    # Graph Statistics
    # --------------------------------------------------------

    def graph_statistics(self) -> dict:
        """
        Enterprise topology statistics.
        """

        degrees = [
            self.get_degree(device_id)
            for device_id in self.device_lookup
        ]

        average_degree = (
            sum(degrees) / len(degrees)
            if degrees
            else 0.0
        )

        return {

            "nodes": self.node_count,

            "edges": self.edge_count,

            "connected_components":
                self.connected_component_count,

            "isolated_devices":
                self.isolated_device_count,

            "average_degree":
                round(
                    average_degree,
                    2,
                ),

            "invalid_links":
                len(self.invalid_links),

            "graph_valid":
                self.validate(),

        }

    # --------------------------------------------------------
    # Enterprise Summary
    # --------------------------------------------------------

    def summary(self) -> dict:
        """
        Returns a complete enterprise
        topology summary.
        """

        return {

            "inventory":

                self.inventory.inventory_statistics(),

            "graph":

                self.graph_statistics(),

            "critical_devices":

                len(
                    self.critical_devices()
                ),

            "graph_built":

                self.graph_built,

        }

    # --------------------------------------------------------
    # String Representation
    # --------------------------------------------------------

    def __len__(self) -> int:

        return self.node_count

    # --------------------------------------------------------

    def __repr__(self) -> str:

        stats = self.graph_statistics()

        return (
            "TopologyService("
            f"nodes={stats['nodes']}, "
            f"edges={stats['edges']}, "
            f"components={stats['connected_components']})"
        )