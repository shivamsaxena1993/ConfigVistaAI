"""
End-to-End Assessment Pipeline Test

Runs every configuration through the complete pipeline.

Author: ConfigVista AI
"""

from pathlib import Path

from services.assessment_service import AssessmentService


CONFIG_DIR = Path(__file__).parent / "configs"


def run_pipeline():

    service = AssessmentService()

    print("=" * 80)
    print("ConfigVista AI - End-to-End Pipeline Test")
    print("=" * 80)

    total = 0
    passed = 0

    for config in sorted(CONFIG_DIR.glob("*.txt")):

        total += 1

        print(f"\nTesting : {config.name}")

        try:

            result = service.run(str(config))

            print("PASS")
            print(f"Hostname : {result['features']['hostname']}")
            print(f"Risk     : {result['risk']['risk_label']}")
            print(f"Score    : {result['risk']['risk_score']}")
            print(f"Priority : {result['recommendation']['priority']}")
            print(
                f"Recommendations : "
                f"{result['recommendation']['recommendation_count']}"
            )

            passed += 1

        except Exception as e:

            print("FAIL")
            print(e)

    print("\n" + "=" * 80)
    print(f"Passed : {passed}/{total}")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()