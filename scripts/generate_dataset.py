from comparison.comparison_engine import ComparisonEngine

engine = ComparisonEngine()

result = engine.compare(
    baseline_file="comparison_examples/baseline.txt",
    candidate_file="comparison_examples/candidate2.txt",
    export_csv=True,
)

print(result.summary)
print("\nDataset generated successfully.")

