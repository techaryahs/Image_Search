from typing import Dict, List, Any
from pathlib import Path

import faiss
import numpy as np
from PIL import Image

from src.config import (
    GOLD_INDEX_FILE,
    GOLD_PATHS_FILE,
    PROTOTYPE_INDEX_FILE,
    PROTOTYPE_PATHS_FILE,
    TOP_K,
    GOLD_DIR,
    PROTOTYPE_DIR,
    BASE_DIR,
)

from src.model import ImageEncoder, get_encoder


class BidirectionalJewelrySearch:

    def __init__(self, encoder: ImageEncoder = None):
        print("Loading Bidirectional Jewelry Search Engine...")

        self.encoder = (
            encoder
            if encoder is not None
            else get_encoder()
        )

        self.load_indexes()

    # ============================================================
    # LOAD INDEXES
    # ============================================================

    def load_indexes(self):
        """
        Load or reload FAISS indexes and image path arrays.
        """

        # --------------------------------------------------------
        # GOLD
        # --------------------------------------------------------

        if (
            GOLD_INDEX_FILE.exists()
            and GOLD_PATHS_FILE.exists()
        ):

            self.gold_index = faiss.read_index(
                str(GOLD_INDEX_FILE)
            )

            self.gold_paths = np.load(
                GOLD_PATHS_FILE,
                allow_pickle=True,
            )

            print(
                f"Loaded Gold index with "
                f"{self.gold_index.ntotal} products."
            )

        else:

            self.gold_index = None
            self.gold_paths = np.array([])

            print(
                "Gold index file not found."
            )


        # --------------------------------------------------------
        # PROTOTYPE
        # --------------------------------------------------------

        if (
            PROTOTYPE_INDEX_FILE.exists()
            and PROTOTYPE_PATHS_FILE.exists()
        ):

            self.prototype_index = faiss.read_index(
                str(PROTOTYPE_INDEX_FILE)
            )

            self.prototype_paths = np.load(
                PROTOTYPE_PATHS_FILE,
                allow_pickle=True,
            )

            print(
                f"Loaded Prototype index with "
                f"{self.prototype_index.ntotal} prototypes."
            )

        else:

            self.prototype_index = None
            self.prototype_paths = np.array([])

            print(
                "Prototype index file not found."
            )


    # ============================================================
    # RESOLVE IMAGE PATH
    # ============================================================

    def _resolve_image_path(
        self,
        image_path,
        collection=None,
    ):
        """
        Convert an old/local/relative image path into
        the correct path on the current machine/server.

        This is important because the FAISS path files may
        contain paths from the machine where the index was built.
        """

        if image_path is None:
            return None

        try:

            raw_path = str(image_path).strip()

            if not raw_path:
                return None


            # Normalize Windows separators
            normalized_path = raw_path.replace(
                "\\",
                "/"
            )

            path = Path(normalized_path)


            # ----------------------------------------------------
            # 1. If stored path already works
            # ----------------------------------------------------

            if path.exists():

                return path


            # ----------------------------------------------------
            # 2. Project-relative path
            # ----------------------------------------------------

            relative_path = BASE_DIR / normalized_path

            if relative_path.exists():

                return relative_path


            # ----------------------------------------------------
            # 3. Use filename and collection folder
            # ----------------------------------------------------

            filename = Path(
                normalized_path
            ).name


            if collection == "gold":

                candidate = GOLD_DIR / filename

                if candidate.exists():

                    return candidate


            elif collection == "prototype":

                candidate = (
                    PROTOTYPE_DIR / filename
                )

                if candidate.exists():

                    return candidate


            # ----------------------------------------------------
            # 4. Search both folders
            # ----------------------------------------------------

            folders = [
                GOLD_DIR,
                PROTOTYPE_DIR,
            ]

            for folder in folders:

                if not folder.exists():
                    continue

                matches = list(
                    folder.rglob(filename)
                )

                if matches:

                    return matches[0]


        except Exception as error:

            print(
                f"Error resolving image path "
                f"{image_path}: {error}"
            )

        return None


    # ============================================================
    # GENERIC SEARCH
    # ============================================================

    def _search(
        self,
        query_image: Image.Image,
        index: faiss.Index,
        image_paths: np.ndarray,
        top_k: int = TOP_K,
        collection: str = None,
    ) -> List[Dict[str, Any]]:
        """
        Generic FAISS search.
        """

        if (
            index is None
            or len(image_paths) == 0
        ):
            return []


        # --------------------------------------------------------
        # CREATE QUERY EMBEDDING
        # --------------------------------------------------------

        query_embedding = (
            self.encoder.encode_image(
                query_image
            )
        )


        # --------------------------------------------------------
        # FLOAT32
        # --------------------------------------------------------

        query_embedding = np.array(
            [query_embedding],
            dtype=np.float32,
        )


        # --------------------------------------------------------
        # NORMALIZE
        # --------------------------------------------------------

        faiss.normalize_L2(
            query_embedding
        )


        # --------------------------------------------------------
        # SEARCH
        # --------------------------------------------------------

        actual_k = min(
            top_k,
            index.ntotal
        )

        if actual_k <= 0:
            return []


        scores, indices = index.search(
            query_embedding,
            actual_k,
        )


        # --------------------------------------------------------
        # BUILD RESULTS
        # --------------------------------------------------------

        results = []


        for score, idx in zip(
            scores[0],
            indices[0],
        ):

            if idx == -1:
                continue


            # Original path from NPY
            original_path = str(
                image_paths[idx]
            )


            # Resolve actual server path
            resolved_path = (
                self._resolve_image_path(
                    original_path,
                    collection=collection,
                )
            )


            # ----------------------------------------------------
            # IMPORTANT
            # ----------------------------------------------------
            # If image exists on Render, return its actual path.
            # Otherwise keep original path so debugging is possible.
            # ----------------------------------------------------

            if resolved_path is not None:

                final_path = str(
                    resolved_path
                )

            else:

                final_path = original_path


            results.append(
                {
                    "image_path": final_path,
                    "original_image_path": original_path,
                    "similarity": float(score),
                }
            )


        return results


    # ============================================================
    # GOLD SEARCH
    # ============================================================

    def search_gold(
        self,
        query_image: Image.Image,
        top_k: int = TOP_K,
    ) -> List[Dict[str, Any]]:
        """
        Search Gold collection.
        """

        return self._search(
            query_image=query_image,
            index=self.gold_index,
            image_paths=self.gold_paths,
            top_k=top_k,
            collection="gold",
        )


    # ============================================================
    # PROTOTYPE SEARCH
    # ============================================================

    def search_prototype(
        self,
        query_image: Image.Image,
        top_k: int = TOP_K,
    ) -> List[Dict[str, Any]]:
        """
        Search Prototype collection.
        """

        return self._search(
            query_image=query_image,
            index=self.prototype_index,
            image_paths=self.prototype_paths,
            top_k=top_k,
            collection="prototype",
        )


# ================================================================
# BACKWARD COMPATIBILITY
# ================================================================

class GoldProductSearch(
    BidirectionalJewelrySearch
):
    """
    Backward-compatible search class.
    """

    def search(
        self,
        query_image: Image.Image,
        top_k: int = TOP_K,
    ) -> List[Dict[str, Any]]:

        return self.search_gold(
            query_image,
            top_k=top_k,
        )