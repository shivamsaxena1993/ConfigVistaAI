"""
=============================================================
ConfigVista AI

Enterprise Models Tests

Artifact-2
Gate 2.2.2 (Part-1)

=============================================================
"""

import re
from datetime import UTC

import pytest

from enterprise.constants import (
    InterfaceLayer,
    InterfaceStatus,
    InterfaceType,
)

from enterprise.models import (
    BaseModel,
    EnterpriseMetadata,
    EnterpriseStatistics,
    Interface,
    ConfigurationSnapshot,
    OperationalSnapshot,
)


# ============================================================
# BaseModel
# ============================================================

def test_base_model_creation():

    model = BaseModel()

    assert model.created_at is not None
    assert model.updated_at is not None


def test_base_model_to_dict():

    model = BaseModel()

    data = model.to_dict()

    assert isinstance(data, dict)

    assert "created_at" in data
    assert "updated_at" in data


def test_base_model_touch():

    model = BaseModel()

    original = model.updated_at

    model.touch()

    assert model.updated_at >= original


# ============================================================
# Enterprise Metadata
# ============================================================

def test_enterprise_metadata_defaults():

    metadata = EnterpriseMetadata()

    assert metadata.enterprise_name == "ConfigVista Enterprise Lab"
    assert metadata.country == "India"
    assert metadata.industry == "Manufacturing"
    assert metadata.dataset_version == "1.0"


# ============================================================
# Enterprise Statistics
# ============================================================

def test_enterprise_statistics_defaults():

    stats = EnterpriseStatistics()

    assert stats.total_sites == 0
    assert stats.total_devices == 0
    assert stats.total_interfaces == 0
    assert stats.total_changes == 0


# ============================================================
# Interface
# ============================================================

def test_interface_defaults():

    interface = Interface(
        name="GigabitEthernet0/0"
    )

    assert interface.interface_id.startswith("IF-")

    assert interface.name == "GigabitEthernet0/0"

    assert interface.interface_type == InterfaceType.PHYSICAL

    assert interface.layer == InterfaceLayer.LAYER3

    assert interface.admin_status == InterfaceStatus.UP

    assert interface.operational_status == InterfaceStatus.UP

    assert interface.mtu == 1500


def test_interface_unique_ids():

    int1 = Interface(name="Gi0/0")

    int2 = Interface(name="Gi0/1")

    assert int1.interface_id != int2.interface_id


def test_interface_vlan():

    interface = Interface(

        name="Gi0/10",

        vlan=100
    )

    assert interface.vlan == 100


def test_invalid_vlan():

    with pytest.raises(ValueError):

        Interface(

            name="Gi0/1",

            vlan=5000
        )


def test_invalid_mtu():

    with pytest.raises(ValueError):

        Interface(

            name="Gi0/1",

            mtu=0
        )


# ============================================================
# Configuration Snapshot
# ============================================================

def test_configuration_snapshot_defaults():

    snapshot = ConfigurationSnapshot()

    assert snapshot.snapshot_id.startswith("CFG-")

    assert snapshot.configuration_version == 1


def test_configuration_snapshot_validation():

    with pytest.raises(ValueError):

        ConfigurationSnapshot(

            configuration_version=0
        )

# ============================================================
# ID Format Validation
# ============================================================

def test_interface_id_format():

    interface = Interface(name="Gi0/0")

    assert re.fullmatch(
        r"IF-\d{6}",
        interface.interface_id
    )


def test_configuration_snapshot_id_format():

    snapshot = ConfigurationSnapshot()

    assert re.fullmatch(
        r"CFG-\d{6}",
        snapshot.snapshot_id
    )


def test_operational_snapshot_id_format():

    snapshot = OperationalSnapshot()

    assert re.fullmatch(
        r"OPS-\d{6}",
        snapshot.snapshot_id
    )

# ============================================================
# ID Uniqueness
# ============================================================

def test_multiple_interface_ids_unique():

    ids = {

        Interface(name=f"Gi0/{i}").interface_id

        for i in range(20)

    }

    assert len(ids) == 20


def test_multiple_configuration_snapshot_ids_unique():

    ids = {

        ConfigurationSnapshot().snapshot_id

        for _ in range(20)

    }

    assert len(ids) == 20


def test_multiple_operational_snapshot_ids_unique():

    ids = {

        OperationalSnapshot().snapshot_id

        for _ in range(20)

    }

    assert len(ids) == 20


# ============================================================
# Timestamp Validation
# ============================================================

def test_created_updated_timestamp_on_creation():

    interface = Interface(name="Gi0/0")

    assert interface.updated_at >= interface.created_at


def test_touch_updates_timestamp():

    interface = Interface(name="Gi0/0")

    original = interface.updated_at

    interface.touch()

    assert interface.updated_at >= original

# ============================================================
# Serialization Integrity
# ============================================================

def test_interface_to_dict_contains_expected_fields():

    interface = Interface(

        name="GigabitEthernet0/0",

        vlan=100,

        mtu=1500
    )

    data = interface.to_dict()

    expected = {

        "interface_id",

        "name",

        "interface_type",

        "layer",

        "description",

        "admin_status",

        "operational_status",

        "mtu",

        "speed",

        "vrf",

        "vlan",

        "ip_address",

        "subnet_mask",

        "mac_address",

        "neighbor_device",

        "neighbor_interface",

        "created_at",

        "updated_at"

    }

    assert expected.issubset(set(data.keys()))

# ============================================================
# BaseModel Consistency
# ============================================================

def test_all_models_inherit_base_model():

    assert isinstance(
        EnterpriseMetadata(),
        BaseModel
    )

    assert isinstance(
        EnterpriseStatistics(),
        BaseModel
    )

    assert isinstance(
        Interface(name="Gi0/0"),
        BaseModel
    )

    assert isinstance(
        ConfigurationSnapshot(),
        BaseModel
    )

    assert isinstance(
        OperationalSnapshot(),
        BaseModel
    )

# ============================================================
# Enterprise Default Values
# ============================================================

def test_enterprise_metadata_not_empty():

    metadata = EnterpriseMetadata()

    assert metadata.enterprise_name

    assert metadata.country

    assert metadata.industry

    assert metadata.timezone


# ============================================================
# Operational Snapshot
# ============================================================

def test_operational_snapshot_defaults():

    snapshot = OperationalSnapshot()

    assert snapshot.snapshot_id.startswith("OPS-")

    assert snapshot.cpu_utilization == 0

    assert snapshot.memory_utilization == 0

    assert snapshot.health_score == 100


def test_operational_snapshot_cpu_validation():

    with pytest.raises(ValueError):

        OperationalSnapshot(

            cpu_utilization=150
        )


def test_operational_snapshot_memory_validation():

    with pytest.raises(ValueError):

        OperationalSnapshot(

            memory_utilization=-5
        )


def test_operational_snapshot_health_validation():

    with pytest.raises(ValueError):

        OperationalSnapshot(

            health_score=101
        )


def test_operational_snapshot_interface_errors_validation():

    with pytest.raises(ValueError):

        OperationalSnapshot(

            input_errors=-1,

            output_errors=0,

            crc_errors=0,

        )

    with pytest.raises(ValueError):

        OperationalSnapshot(

            input_errors=0,

            output_errors=-1,

            crc_errors=0,

        )

    with pytest.raises(ValueError):

        OperationalSnapshot(

            input_errors=0,

            output_errors=0,

            crc_errors=-1,

        )

def test_operational_snapshot_packet_drop_validation():

    with pytest.raises(ValueError):

        OperationalSnapshot(

            packet_drops=-5
        )


def test_operational_snapshot_neighbors_validation():

    with pytest.raises(ValueError):

        OperationalSnapshot(

            ospf_neighbors=-1,

        )

    with pytest.raises(ValueError):

        OperationalSnapshot(

            bgp_neighbors=-1,

        )

    with pytest.raises(ValueError):

        OperationalSnapshot(

            eigrp_neighbors=-1,

        )

def test_operational_snapshot_packet_loss_validation():

    with pytest.raises(ValueError):

        OperationalSnapshot(

            packet_loss_percent=101

        )




# ============================================================
# Serialization
# ============================================================

def test_interface_serialization():

    interface = Interface(

        name="GigabitEthernet0/0"
    )

    data = interface.to_dict()

    assert isinstance(data, dict)

    assert data["name"] == "GigabitEthernet0/0"

    assert data["interface_id"].startswith("IF-")


def test_snapshot_serialization():

    snapshot = ConfigurationSnapshot()

    data = snapshot.to_dict()

    assert isinstance(data, dict)

    assert data["snapshot_id"].startswith("CFG-")


# ============================================================
# Timestamp Validation
# ============================================================

def test_timestamp_timezone():

    interface = Interface(

        name="GigabitEthernet0/0"
    )

    assert interface.created_at.tzinfo == UTC

    assert interface.updated_at.tzinfo == UTC


# ============================================================
# String Representation
# ============================================================

def test_string_representation():

    interface = Interface(

        name="GigabitEthernet0/0"
    )

    text = str(interface)

    assert "Interface" in text

    assert "GigabitEthernet0/0" in text


# ============================================================
# Overall Sanity
# ============================================================

def test_all_models_can_be_created():

    EnterpriseMetadata()

    EnterpriseStatistics()

    Interface(name="Gi0/0")

    ConfigurationSnapshot()

    OperationalSnapshot()