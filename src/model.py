import os

# Force CPU on Render
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import torch
import torch.nn as nn
import numpy as np
import streamlit as st

from PIL import Image, ImageOps
from torchvision import models, transforms


@st.cache_resource(show_spinner="Loading AI model...")
def get_encoder():
    """
    Load MobileNetV3 only once and reuse it across all Streamlit reruns.
    ~20MB model, fits comfortably in Render free tier 512MB RAM.
    """
    return ImageEncoder()


class ImageEncoder:
    """
    Lightweight image encoder using MobileNetV3-Large.
    Strips the classifier head and uses the pooled feature vector (~960-D).
    Combined RGB + grayscale view gives 1920-D final embedding.
    """

    def __init__(self):

        self.device = torch.device("cpu")

        print("=" * 50)
        print("Loading MobileNetV3-Large encoder...")
        print("Device:", self.device)
        print("=" * 50)

        # Load pretrained MobileNetV3-Large
        backbone = models.mobilenet_v3_large(
            weights=models.MobileNet_V3_Large_Weights.IMAGENET1K_V2
        )

        # Remove classifier — keep features + adaptive pool only
        self.model = nn.Sequential(
            backbone.features,
            backbone.avgpool,
            nn.Flatten(),
        )

        self.model = self.model.to(self.device)
        self.model.eval()

        # ImageNet normalization
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])

        print("MobileNetV3 loaded successfully.")
        print("=" * 50)

    def _extract_features(self, image: Image.Image) -> np.ndarray:
        """Extract 960-D feature vector from a PIL image."""
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.inference_mode():
            features = self.model(img_tensor)

        vec = features.cpu().numpy()[0]

        # L2 normalize
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm

        return vec.astype(np.float32)

    def encode_image(self, image: Image.Image) -> np.ndarray:
        """
        Dual-view encoding: RGB + grayscale concatenated → 1920-D vector.
        Improves texture/shape robustness without heavy compute.
        """
        rgb_image = image.convert("RGB")

        # View 1 — RGB
        rgb_features = self._extract_features(rgb_image)

        # View 2 — Grayscale (shape/texture focus)
        gray_image = ImageOps.grayscale(rgb_image).convert("RGB")
        gray_features = self._extract_features(gray_image)

        # Fuse
        combined = np.concatenate([rgb_features, gray_features])

        # Final L2 normalize
        norm = np.linalg.norm(combined)
        if norm > 0:
            combined = combined / norm

        return combined.astype(np.float32)
