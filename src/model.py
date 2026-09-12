import torch
import numpy as np

from PIL import Image, ImageOps
from transformers import AutoImageProcessor, AutoModel

from src.config import MODEL_NAME


class DINOv2Encoder:

    def __init__(self):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        print(f"Using device: {self.device}")
        print("Loading DINOv2 model...")

        self.processor = AutoImageProcessor.from_pretrained(
            MODEL_NAME
        )

        self.model = AutoModel.from_pretrained(
            MODEL_NAME
        )

        self.model = self.model.to(self.device)
        self.model.eval()

        print("DINOv2 model loaded successfully.")

    def _extract_features(self, image):

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():

            outputs = self.model(
                **inputs
            )

        # CLS token
        embedding = outputs.last_hidden_state[:, 0]

        # Normalize individual feature
        embedding = embedding / embedding.norm(
            dim=-1,
            keepdim=True
        )

        return embedding.cpu().numpy()[0]

    def encode_image(self, image: Image.Image):

        # ------------------------------------------------
        # VIEW 1: Original RGB
        # ------------------------------------------------

        rgb_image = image.convert("RGB")

        rgb_features = self._extract_features(
            rgb_image
        )


        # ------------------------------------------------
        # VIEW 2: Grayscale
        # ------------------------------------------------

        gray_image = ImageOps.grayscale(
            rgb_image
        ).convert("RGB")

        gray_features = self._extract_features(
            gray_image
        )


        # ------------------------------------------------
        # Feature Fusion
        # ------------------------------------------------

        combined = np.concatenate(
            [
                rgb_features,
                gray_features
            ]
        )


        # Final L2 normalization
        combined = combined / np.linalg.norm(
            combined
        )

        return combined.astype(
            np.float32
        )