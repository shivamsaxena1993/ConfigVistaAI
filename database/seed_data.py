"""
====================================================================
File: seed_data.py

Project : ConfigVista AI

Purpose
-------
Populate the SQLite database with sample data for development,
testing and Mid-Sem demonstration.

====================================================================
"""

from database.database import SessionLocal
from database.models import (
    Role,
    User,
    Device,
    Change,
    Recommendation,
    DatabaseVersion,
    ModelMetric,
)


def seed_database():

    session = SessionLocal()

    print("\nSeeding ConfigVista AI Database...\n")

    try:

        # ----------------------------------------------------------
        # Roles
        # ----------------------------------------------------------

        if session.query(Role).count() == 0:

            roles = [

                Role(
                    role_name="Administrator",
                    description="System Administrator"
                ),

                Role(
                    role_name="Network Engineer",
                    description="Performs Network Changes"
                ),

                Role(
                    role_name="Reviewer",
                    description="Reviews Recommendations"
                ),

                Role(
                    role_name="NOC Manager",
                    description="Approves Changes"
                )

            ]

            session.add_all(roles)

            print("✓ Roles inserted.")

        session.commit()

        # ----------------------------------------------------------
        # Users
        # ----------------------------------------------------------

        if session.query(User).count() == 0:

            admin_role = session.query(Role).filter_by(
                role_name="Administrator"
            ).first()

            engineer_role = session.query(Role).filter_by(
                role_name="Network Engineer"
            ).first()

            reviewer_role = session.query(Role).filter_by(
                role_name="Reviewer"
            ).first()

            manager_role = session.query(Role).filter_by(
                role_name="NOC Manager"
            ).first()

            users = [

                User(
                    username="admin",
                    full_name="System Administrator",
                    email="admin@configvista.ai",
                    role_id=admin_role.role_id
                ),

                User(
                    username="engineer1",
                    full_name="John Engineer",
                    email="engineer@configvista.ai",
                    role_id=engineer_role.role_id
                ),

                User(
                    username="reviewer1",
                    full_name="Jane Reviewer",
                    email="reviewer@configvista.ai",
                    role_id=reviewer_role.role_id
                ),

                User(
                    username="manager1",
                    full_name="Mike Manager",
                    email="manager@configvista.ai",
                    role_id=manager_role.role_id
                )

            ]

            session.add_all(users)

            print("✓ Users inserted.")

        session.commit()

        # ----------------------------------------------------------
        # Devices
        # ----------------------------------------------------------

        if session.query(Device).count() == 0:

            devices = [

                Device(
                    hostname="Core-R1",
                    vendor="Cisco",
                    model="ASR1001-X",
                    device_type="Router",
                    management_ip="10.10.1.1",
                    site="DC1",
                    environment="Production",
                    criticality="High"
                ),

                Device(
                    hostname="Core-R2",
                    vendor="Cisco",
                    model="ASR1001-X",
                    device_type="Router",
                    management_ip="10.10.1.2",
                    site="DC1",
                    environment="Production",
                    criticality="High"
                ),

                Device(
                    hostname="Dist-SW1",
                    vendor="Cisco",
                    model="Catalyst 9500",
                    device_type="Switch",
                    management_ip="10.10.2.1",
                    site="DC1",
                    environment="Production",
                    criticality="High"
                ),

                Device(
                    hostname="Branch-R1",
                    vendor="Cisco",
                    model="ISR4331",
                    device_type="Router",
                    management_ip="10.20.1.1",
                    site="Branch",
                    environment="Production",
                    criticality="Medium"
                ),

                Device(
                    hostname="LAB-R1",
                    vendor="Cisco",
                    model="CSR1000v",
                    device_type="Virtual Router",
                    management_ip="192.168.1.10",
                    site="Lab",
                    environment="Development",
                    criticality="Low"
                )

            ]

            session.add_all(devices)

            print("✓ Devices inserted.")

        session.commit()

        # ----------------------------------------------------------
        # Sample Change
        # ----------------------------------------------------------

        if session.query(Change).count() == 0:

            engineer = session.query(User).filter_by(
                username="engineer1"
            ).first()

            device = session.query(Device).filter_by(
                hostname="Core-R1"
            ).first()

            change = Change(

                change_reference="CHG000001",

                device_id=device.device_id,

                submitted_by=engineer.user_id,

                change_type="Routing",

                description="Update BGP Neighbor Configuration",

                risk_label="Medium",

                risk_score=58.4,

                confidence_score=88.7,

                approval_status="Pending",

                change_status="Submitted"

            )

            session.add(change)

            print("✓ Sample Change inserted.")

        session.commit()

        # ----------------------------------------------------------
        # Recommendation
        # ----------------------------------------------------------

        if session.query(Recommendation).count() == 0:

            change = session.query(Change).first()

            recommendation = Recommendation(

                change_id=change.change_id,

                recommendation_text=(
                    "Validate BGP neighbors after deployment."
                ),

                explanation=(
                    "Historical routing changes indicate a "
                    "moderate rollback probability."
                ),

                llm_summary=(
                    "Proceed with change after validating "
                    "routing adjacency."
                )

            )

            session.add(recommendation)

            print("✓ Recommendation inserted.")

        session.commit()

        # ----------------------------------------------------------
        # Model Metrics
        # ----------------------------------------------------------

        if session.query(ModelMetric).count() == 0:

            metrics = [

                ModelMetric(

                    model_name="Random Forest",

                    version="1.0",

                    accuracy=91.8,

                    precision_score=90.5,

                    recall_score=89.7,

                    f1_score=90.1,

                    training_time=1.82,

                    inference_time=0.07

                ),

                ModelMetric(

                    model_name="XGBoost",

                    version="1.0",

                    accuracy=94.2,

                    precision_score=93.8,

                    recall_score=92.9,

                    f1_score=93.3,

                    training_time=2.15,

                    inference_time=0.05

                )

            ]

            session.add_all(metrics)

            print("✓ Model Metrics inserted.")

        session.commit()

        # ----------------------------------------------------------
        # Database Version
        # ----------------------------------------------------------

        if session.query(DatabaseVersion).count() == 0:

            version = DatabaseVersion(

                version="2.0.0",

                description="Initial MVP Database"

            )

            session.add(version)

            print("✓ Database Version inserted.")

        session.commit()

        print("\n========================================")
        print("Database seeded successfully.")
        print("========================================\n")

    except Exception as ex:

        session.rollback()

        print(f"\nError: {ex}")

    finally:

        session.close()


if __name__ == "__main__":

    seed_database()