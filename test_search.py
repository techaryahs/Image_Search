from pathlib import Path
from PIL import Image

from src.config import GOLD_DIR, PROTOTYPE_DIR, IMAGE_EXTENSIONS
from src.search import BidirectionalJewelrySearch


def get_image_files(directory: Path):
    return sorted(
        [
            p for p in directory.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
        ]
    )


def test_bidirectional_search():
    prototype_images = get_image_files(PROTOTYPE_DIR)
    gold_images = get_image_files(GOLD_DIR)

    print("Loading Bidirectional Search Engine...")
    search_engine = BidirectionalJewelrySearch()

    # ----------------------------------------------------
    # MODE 1: Prototype → Gold
    # ----------------------------------------------------
    print("\n" + "=" * 60)
    print("TESTING MODE 1: PROTOTYPE → GOLD SEARCH")
    print("=" * 60)

    for proto_path in prototype_images:
        print(f"\nQUERY: {proto_path.name}")
        image = Image.open(proto_path).convert("RGB")
        results = search_engine.search_gold(image, top_k=3)

        for rank, res in enumerate(results, start=1):
            target_name = Path(res["image_path"]).name
            print(f"  Rank {rank}: Gold Product={target_name} | Visual Similarity Score={res['similarity']:.4f}")

    # ----------------------------------------------------
    # MODE 2: Gold → Prototype
    # ----------------------------------------------------
    print("\n" + "=" * 60)
    print("TESTING MODE 2: GOLD → PROTOTYPE SEARCH")
    print("=" * 60)

    for gold_path in gold_images:
        print(f"\nQUERY: {gold_path.name}")
        image = Image.open(gold_path).convert("RGB")
        results = search_engine.search_prototype(image, top_k=3)

        for rank, res in enumerate(results, start=1):
            target_name = Path(res["image_path"]).name
            print(f"  Rank {rank}: Prototype Design={target_name} | Visual Similarity Score={res['similarity']:.4f}")


if __name__ == "__main__":
    test_bidirectional_search()