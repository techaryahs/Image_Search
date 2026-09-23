import os

# Force CPU on Render
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import torch
import numpy as np
import streamlit as st

from PIL import Image, ImageOps
from transformers import AutoImageProcessor, AutoModel

from src.config import MODEL_NAME


@st.cache_resource(show_spinner="Loading AI model...")
def get_dinov2_encoder():
    """
    Load DINOv2 only once and reuse it across Streamlit reruns.
    """
    return DINOv2Encoder()


class DINOv2Encoder:

    def __init__(self):

        # Render Free instance uses CPU
        self.device = torch.device("cpu")

        print("========================================")
        print("Using device:", self.device)
        print("Loading DINOv2 model...")
        print("========================================")

        # Image processor
        self.processor = AutoImageProcessor.from_pretrained(
            MODEL_NAME
        )

        # Load model
        self.model = AutoModel.from_pretrained(
            MODEL_NAME
        )

        # CPU
        self.model = self.model.to(self.device)

        # Evaluation mode
        self.model.eval()

        print("========================================")
        print("DINOv2 model loaded successfully.")
        print("========================================")

    def _extract_features(self, image: Image.Image):

        # Process image
        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        # Move tensors to CPU
        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        # Inference only
        with torch.inference_mode():

            outputs = self.model(
                **inputs
            )

        # CLS token
        embedding = outputs.last_hidden_state[:, 0]

        # L2 normalization
        embedding = embedding / embedding.norm(
            dim=-1,
            keepdim=True
        )

        # Convert to NumPy
        return embedding.cpu().numpy()[0]

    def encode_image(self, image: Image.Image):

        # ==================================================
        # VIEW 1 — ORIGINAL RGB
        # ==================================================

        rgb_image = image.convert("RGB")

        rgb_features = self._extract_features(
            rgb_image
        )

        # ==================================================
        # VIEW 2 — GRAYSCALE
        # ==================================================

        gray_image = ImageOps.grayscale(
            rgb_image
        ).convert("RGB")

        gray_features = self._extract_features(
            gray_image
        )

        # ==================================================
        # FEATURE FUSION
        # ==================================================

        combined = np.concatenate(
            [
                rgb_features,
                gray_features
            ]
        )

        # Final normalization
        norm = np.linalg.norm(combined)

        if norm > 0:
            combined = combined / norm

        return combined.astype(
            np.float32
        )