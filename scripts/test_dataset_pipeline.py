from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from enterprise.exporters.dataset_exporter import DatasetExporter
from enterprise.generators.enterprise_generator import EnterpriseGenerationConfig
from enterprise.generators.site_generator import SiteGenerator
from enterprise.generators.device_generator import DeviceGenerator
from enterprise.generators.business_service_generator import BusinessServiceGenerator
from enterprise.generators.change_generator import ChangeGenerator
from enterprise.generators.incident_generator import IncidentGenerator
from enterprise.generators.configuration_backup_generator import ConfigurationBackupGenerator
from enterprise.generators.operational_snapshot_generator import OperationalSnapshotGenerator
from enterprise.generators.feature_generator import FeatureGenerator

config = EnterpriseGenerationConfig()

sites = SiteGenerator().generate(config)

devices = DeviceGenerator().generate(
    config,
    sites,
    [],
)

services = BusinessServiceGenerator().generate(config)

changes = ChangeGenerator().generate(
    config,
    sites,
    devices,
    services,
)

incidents = IncidentGenerator().generate(
    config,
    sites,
    devices,
    services,
    changes,
)

backups = ConfigurationBackupGenerator().generate(
    config,
    devices,
)

snapshots = OperationalSnapshotGenerator().generate(
    config,
    devices,
)

features = FeatureGenerator().generate(
    config,
    sites,
    devices,
    services,
    changes,
    incidents,
    backups,
    snapshots,
)

exporter = DatasetExporter()

exporter.export_dataframe(features)

exporter.export_csv(
    features,
    "datasets/generated/feature_dataset.csv",
)

exporter.export_metadata(
    "datasets/generated/metadata.json",
)

# ============================================================
# Train / Validation / Test Split
# ============================================================

splits = exporter.export_train_validation_test_split(
    "datasets/generated",
)

print(f"Train      : {len(splits['train'])}")
print(f"Validation : {len(splits['validation'])}")
print(f"Test       : {len(splits['test'])}")

# ============================================================
# Manifest
# ============================================================

manifest = exporter.export_manifest(
    "datasets/generated/manifest.json",
)

print("\nManifest")
print("--------------------------------")

for key, value in manifest.items():

    print(f"{key}: {value}")

# ============================================================
# Dataset Statistics
# ============================================================

print("\nStatistics")
print("--------------------------------")

print(exporter.statistics())

print("\nDataset Valid")

print(exporter.validate_dataset())