from pathlib import Path
from PIL import Image

from src.config import PROTOTYPE_DIR, GOLD_DIR, IMAGE_EXTENSIONS
from src.search import BidirectionalJewelrySearch


def get_image_files(directory: Path):
    return sorted(
        [
            p
            for p in directory.iterdir()
            if p.is_file()
            and p.suffix.lower() in IMAGE_EXTENSIONS
        ]
    )


def get_best_similarity(search_engine, image_path):
    image = Image.open(image_path).convert("RGB")

    result = search_engine.check_image_validity(
        image
    )

    return float(result["similarity"])

    if not result:
        return None

    return float(result[0]["similarity"])


def main():

    print("=" * 70)
    print("AUTOMATIC VALID / INVALID THRESHOLD TEST")
    print("=" * 70)

    search_engine = BidirectionalJewelrySearch()

    prototype_images = get_image_files(PROTOTYPE_DIR)
    gold_images = get_image_files(GOLD_DIR)

    invalid_dir = Path("data") / "invalid"

    if not invalid_dir.exists():
        print("\nERROR: data/invalid folder not found.")
        return

    invalid_images = get_image_files(invalid_dir)

    print(
        f"\nValid Gold Images : {len(gold_images)}"
    )

    print(
        f"Invalid Images    : {len(invalid_images)}"
    )

    # ======================================================
    # IMPORTANT:
    # Do NOT use prototype images themselves for threshold
    # because they give self-match = 1.0.
    # ======================================================

    valid_scores = []

    print("\n" + "-" * 70)
    print("VALID GOLD IMAGE SCORES")
    print("-" * 70)

    for image_path in gold_images:

        score = get_best_similarity(
            search_engine,
            image_path
        )

        if score is not None:

            valid_scores.append(score)

            print(
                f"{image_path.name:<20} "
                f"{score:.4f}"
            )

    invalid_scores = []

    print("\n" + "-" * 70)
    print("INVALID IMAGE SCORES")
    print("-" * 70)

    for image_path in invalid_images:

        score = get_best_similarity(
            search_engine,
            image_path
        )

        if score is not None:

            invalid_scores.append(score)

            print(
                f"{image_path.name:<20} "
                f"{score:.4f}"
            )

    if not valid_scores or not invalid_scores:

        print(
            "\nNot enough data to calculate threshold."
        )

        return

    # ======================================================
    # TEST DIFFERENT THRESHOLDS
    # ======================================================

    print("\n" + "=" * 70)
    print("THRESHOLD EVALUATION")
    print("=" * 70)

    best_threshold = None
    best_accuracy = -1

    for threshold_int in range(0, 31):

        threshold = threshold_int / 100

        valid_correct = sum(
            score >= threshold
            for score in valid_scores
        )

        invalid_correct = sum(
            score < threshold
            for score in invalid_scores
        )

        total_correct = (
            valid_correct
            + invalid_correct
        )

        total_images = (
            len(valid_scores)
            + len(invalid_scores)
        )

        accuracy = (
            total_correct
            / total_images
        ) * 100

        print(
            f"Threshold={threshold:.2f} | "
            f"Valid={valid_correct}/{len(valid_scores)} | "
            f"Invalid={invalid_correct}/{len(invalid_scores)} | "
            f"Accuracy={accuracy:.2f}%"
        )

        if accuracy > best_accuracy:

            best_accuracy = accuracy
            best_threshold = threshold

    # ======================================================
    # FINAL RESULT
    # ======================================================

    print("\n" + "=" * 70)
    print("BEST THRESHOLD")
    print("=" * 70)

    print(
        f"Best Threshold : {best_threshold:.2f}"
    )

    print(
        f"Best Accuracy  : {best_accuracy:.2f}%"
    )

    print("\nRecommended change in src/search.py:")

    print(
        f"MATCH_THRESHOLD = {best_threshold:.2f}"
    )


if __name__ == "__main__":
    main()