from pathlib import Path
from PIL import Image

from src.config import GOLD_DIR, PROTOTYPE_DIR
from src.search import BidirectionalJewelrySearch


# Ground truth mapping: Prototype filename -> Gold filename
GROUND_TRUTH = {
    "prototype1.jpeg": "gold1.jpeg",
    "prototype2.jpeg": "gold2.jpeg",
    "prototype3.jpeg": "gold3.jpeg",
    "prototype6.png": "gold4.png",
}


# Reverse ground truth mapping: Gold filename -> Prototype filename
REVERSE_GROUND_TRUTH = {v: k for k, v in GROUND_TRUTH.items()}


def evaluate_direction(search_fn, query_dir: Path, ground_truth_dict: dict, direction_name: str):
    print("=" * 70)
    print(f"EVALUATION: {direction_name}")
    print("=" * 70)

    total = 0
    top1_correct = 0
    top3_correct = 0
    reciprocal_ranks = []

    for query_name, expected_target in ground_truth_dict.items():
        query_path = query_dir / query_name

        if not query_path.exists():
            print(f"\nMissing query image: {query_path}")
            continue

        image = Image.open(query_path).convert("RGB")
        results = search_fn(image, top_k=3)

        predicted_names = [Path(result["image_path"]).name for result in results]
        total += 1

        # Top-1 Accuracy
        if predicted_names and predicted_names[0] == expected_target:
            top1_correct += 1

        # Top-3 Accuracy
        if expected_target in predicted_names:
            top3_correct += 1
            rank = predicted_names.index(expected_target) + 1
            reciprocal_ranks.append(1.0 / rank)
        else:
            reciprocal_ranks.append(0.0)

        print("\n" + "-" * 70)
        print(f"Query Image:    {query_name}")
        print(f"Expected Target:{expected_target}")
        print(f"Top Prediction: {predicted_names[0] if predicted_names else 'None'}")

        for rank, result in enumerate(results, start=1):
            target_name = Path(result["image_path"]).name
            print(f"  Rank {rank}: {target_name} ({result['similarity']:.4f})")

    if total == 0:
        print(f"\nNo images were evaluated for {direction_name}.")
        return None

    top1_accuracy = top1_correct / total
    top3_accuracy = top3_correct / total
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)

    print("\n" + "=" * 70)
    print(f"{direction_name} RESULTS")
    print("=" * 70)
    print(f"Total Queries:     {total}")
    print(f"Top-1 Accuracy:    {top1_accuracy * 100:.2f}%")
    print(f"Top-3 Accuracy:    {top3_accuracy * 100:.2f}%")
    print(f"MRR:               {mrr:.4f}")
    print("=" * 70 + "\n")

    return {
        "top1_accuracy": top1_accuracy,
        "top3_accuracy": top3_accuracy,
        "mrr": mrr,
    }


def evaluate_all():
    print("Loading Search Engine for Evaluation...")
    search_engine = BidirectionalJewelrySearch()

    # 1. Prototype -> Gold
    evaluate_direction(
        search_fn=search_engine.search_gold,
        query_dir=PROTOTYPE_DIR,
        ground_truth_dict=GROUND_TRUTH,
        direction_name="PROTOTYPE → GOLD",
    )

    # 2. Gold -> Prototype
    evaluate_direction(
        search_fn=search_engine.search_prototype,
        query_dir=GOLD_DIR,
        ground_truth_dict=REVERSE_GROUND_TRUTH,
        direction_name="GOLD → PROTOTYPE",
    )


if __name__ == "__main__":
    evaluate_all()