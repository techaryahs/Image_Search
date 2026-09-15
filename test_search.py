from pathlib import Path
from PIL import Image

from src.config import (
    GOLD_DIR,
    PROTOTYPE_DIR,
    IMAGE_EXTENSIONS,
)
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


def test_bidirectional_search():

    prototype_images = get_image_files(
        PROTOTYPE_DIR
    )

    gold_images = get_image_files(
        GOLD_DIR
    )

    print(
        "Loading Bidirectional Search Engine..."
    )

    search_engine = BidirectionalJewelrySearch()

    # ====================================================
    # MODE 1: PROTOTYPE → GOLD
    # ====================================================

    print("\n" + "=" * 60)
    print(
        "TESTING MODE 1: PROTOTYPE → GOLD SEARCH"
    )
    print("=" * 60)

    for proto_path in prototype_images:

        print(
            f"\nQUERY: {proto_path.name}"
        )

        image = Image.open(
            proto_path
        ).convert("RGB")

        results = search_engine.search_gold(
            image,
            top_k=3
        )

        for rank, res in enumerate(
            results,
            start=1
        ):

            target_name = Path(
                res["image_path"]
            ).name

            print(
                f"  Rank {rank}: "
                f"Gold Product={target_name} | "
                f"Visual Similarity Score="
                f"{res['similarity']:.4f}"
            )

    # ====================================================
    # MODE 2: GOLD → PROTOTYPE
    # ====================================================

    print("\n" + "=" * 60)
    print(
        "TESTING MODE 2: GOLD → PROTOTYPE SEARCH"
    )
    print("=" * 60)

    for gold_path in gold_images:

        print(
            f"\nQUERY: {gold_path.name}"
        )

        image = Image.open(
            gold_path
        ).convert("RGB")

        results = search_engine.search_prototype(
            image,
            top_k=3
        )

        for rank, res in enumerate(
            results,
            start=1
        ):

            target_name = Path(
                res["image_path"]
            ).name

            print(
                f"  Rank {rank}: "
                f"Prototype Design={target_name} | "
                f"Visual Similarity Score="
                f"{res['similarity']:.4f}"
            )

    # ====================================================
    # MODE 3: VALID / INVALID IMAGE CHECK
    # ====================================================

    print("\n" + "=" * 60)
    print(
        "TESTING MODE 3: VALID / INVALID IMAGE CHECK"
    )
    print("=" * 60)

    # ----------------------------------------------------
    # Test all prototype images as VALID images
    # ----------------------------------------------------

    print("\n" + "-" * 60)
    print("VALID IMAGE TEST")
    print("-" * 60)

    valid_correct = 0
    valid_total = 0

    for proto_path in prototype_images:

        print(
            f"\nTEST IMAGE: {proto_path.name}"
        )

        image = Image.open(
            proto_path
        ).convert("RGB")

        result = search_engine.check_image_validity(
            image
        )

        valid_total += 1

        if result["valid"]:
            valid_correct += 1

        print(
            f"  Result: {result['message']}"
        )

        print(
            f"  Best Match: "
            f"{result['best_match']}"
        )

        print(
            f"  Similarity: "
            f"{result['similarity']:.4f}"
        )

        print(
            f"  Threshold: "
            f"{result['threshold']:.4f}"
        )

    if valid_total > 0:

        valid_accuracy = (
            valid_correct
            / valid_total
        ) * 100

        print(
            "\nValid Image Detection Accuracy: "
            f"{valid_accuracy:.2f}%"
        )

    # ----------------------------------------------------
    # Test Gold images as VALID images
    # ----------------------------------------------------

    print("\n" + "-" * 60)
    print("GOLD IMAGE VALIDITY TEST")
    print("-" * 60)

    gold_valid_correct = 0
    gold_valid_total = 0

    for gold_path in gold_images:

        print(
            f"\nTEST IMAGE: {gold_path.name}"
        )

        image = Image.open(
            gold_path
        ).convert("RGB")

        result = search_engine.check_image_validity(
            image
        )

        gold_valid_total += 1

        if result["valid"]:
            gold_valid_correct += 1

        print(
            f"  Result: {result['message']}"
        )

        print(
            f"  Best Match: "
            f"{result['best_match']}"
        )

        print(
            f"  Similarity: "
            f"{result['similarity']:.4f}"
        )

        print(
            f"  Threshold: "
            f"{result['threshold']:.4f}"
        )

    if gold_valid_total > 0:

        gold_accuracy = (
            gold_valid_correct
            / gold_valid_total
        ) * 100

        print(
            "\nGold Image Detection Accuracy: "
            f"{gold_accuracy:.2f}%"
        )

    # ====================================================
    # MODE 4: UNRELATED / INVALID IMAGE TEST
    # ====================================================

    print("\n" + "=" * 60)
    print(
        "TESTING MODE 4: INVALID / UNRELATED IMAGE"
    )
    print("=" * 60)

    print(
        "\nTo test invalid-image detection, place "
        "unrelated images inside:"
    )

    print(
        "data/invalid/"
    )

    invalid_dir = (
        Path("data") / "invalid"
    )

    if not invalid_dir.exists():

        print(
            "\nInvalid image folder does not exist."
        )

        print(
            "Create it and add unrelated images "
            "(for example car.jpg, flower.jpg, "
            "building.jpg), then run this test again."
        )

        return

    invalid_images = get_image_files(
        invalid_dir
    )

    if len(invalid_images) == 0:

        print(
            "\nNo invalid/unrelated images found."
        )

        print(
            "Add some unrelated images to:"
        )

        print(
            "data/invalid/"
        )

        return

    invalid_correct = 0
    invalid_total = 0

    print(
        f"\nFound {len(invalid_images)} "
        "invalid/unrelated images."
    )

    for invalid_path in invalid_images:

        print(
            f"\nTEST IMAGE: "
            f"{invalid_path.name}"
        )

        image = Image.open(
            invalid_path
        ).convert("RGB")

        result = search_engine.check_image_validity(
            image
        )

        invalid_total += 1

        # For invalid images, correct result is valid=False
        if not result["valid"]:
            invalid_correct += 1

        print(
            f"  Result: {result['message']}"
        )

        print(
            f"  Best Match: "
            f"{result['best_match']}"
        )

        print(
            f"  Similarity: "
            f"{result['similarity']:.4f}"
        )

        print(
            f"  Threshold: "
            f"{result['threshold']:.4f}"
        )

    if invalid_total > 0:

        invalid_accuracy = (
            invalid_correct
            / invalid_total
        ) * 100

        print(
            "\nInvalid Image Detection Accuracy: "
            f"{invalid_accuracy:.2f}%"
        )


if __name__ == "__main__":

    test_bidirectional_search()