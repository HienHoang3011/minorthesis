#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
OptionalImageAdapter — searches products by visual similarity.

Algorithm (PIL-based, no external AI model required):
  1. Build a color histogram for each product image stored in the DB.
  2. For the query image, compute its histogram.
  3. Rank products by histogram intersection (colour similarity score).
  4. Return product IDs in descending similarity order.

Limitations: colour-only matching works well for plant/accessory images
where dominant colours (green, brown, terracotta) distinguish categories.
A production system would use a deep visual embedding (CLIP, EfficientNet).
"""
import io
import os
import math

from application.service.ImageSearch import ImageSearch

_HIST_BINS = 8        # 8 bins per channel → 8³ = 512-dimensional histogram
_RESIZE_PX = 64       # resize query + stored images before computing histogram


class OptionalImageAdapter(ImageSearch):

    def __init__(self, productImageRepository=None):
        # Injected repository gives access to stored product images.
        # Can be None — falls back to empty results.
        self._repo = productImageRepository
        self._index: dict = {}   # productId → normalised histogram list

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def buildIndex(self, products: list, image_dir: str = '') -> None:
        """Pre-compute histograms for all product images."""
        self._index = {}
        for product in products:
            imgs = getattr(product, '_images', []) or []
            for img_obj in imgs:
                path = getattr(img_obj, '_url', '') or ''
                if path and os.path.isfile(path):
                    hist = self._histogram_from_file(path)
                    if hist:
                        self._index[product._productId] = hist
                        break   # one representative image per product

    def searchByImage(self, imageBytes: bytes, limit: int = 20) -> list:
        """Return product IDs sorted by colour similarity to the query image."""
        if not imageBytes:
            return []
        query_hist = self._histogram_from_bytes(imageBytes)
        if query_hist is None or not self._index:
            # No index yet — return all product IDs (caller filters by published)
            return list(self._index.keys())[:limit]
        scores = {}
        for pid, stored_hist in self._index.items():
            scores[pid] = self._histogram_intersection(query_hist, stored_hist)
        ranked = sorted(scores.keys(), key=lambda p: scores[p], reverse=True)
        return ranked[:limit]

    # ------------------------------------------------------------------
    # Histogram helpers (pure PIL / stdlib, no external model)
    # ------------------------------------------------------------------

    def _histogram_from_file(self, path: str):
        try:
            from PIL import Image
            with Image.open(path) as img:
                return self._compute_histogram(img)
        except Exception:
            return None

    def _histogram_from_bytes(self, data: bytes):
        try:
            from PIL import Image
            with Image.open(io.BytesIO(data)) as img:
                return self._compute_histogram(img)
        except Exception:
            return None

    def _compute_histogram(self, img) -> list:
        from PIL import Image
        rgb = img.convert('RGB').resize((_RESIZE_PX, _RESIZE_PX), Image.LANCZOS)
        pixels = list(rgb.getdata())
        bins = _HIST_BINS
        hist = [0] * (bins ** 3)
        for r, g, b in pixels:
            ri = min(r * bins // 256, bins - 1)
            gi = min(g * bins // 256, bins - 1)
            bi = min(b * bins // 256, bins - 1)
            hist[ri * bins * bins + gi * bins + bi] += 1
        total = max(1, len(pixels))
        return [v / total for v in hist]   # normalise

    @staticmethod
    def _histogram_intersection(h1: list, h2: list) -> float:
        return sum(min(a, b) for a, b in zip(h1, h2))
