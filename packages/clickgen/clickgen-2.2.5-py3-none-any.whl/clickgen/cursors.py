#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Iterator, List, Tuple

from PIL.Image import Image


class CursorImage:
    image: Image
    hotspot: Tuple[int, int]
    nominal: int
    re_canvas: bool

    def __init__(
        self,
        image: Image,
        hotspot: Tuple[int, int],
        nominal: int,
        re_canvas: bool = False,
    ) -> None:
        self.image = image
        self.hotspot = hotspot
        self.nominal = nominal
        self.re_canvas = re_canvas

    def __repr__(self) -> str:
        return f"CursorImage(image={self.image!r}, hotspot={self.hotspot!r}, nominal={self.nominal!r}, re_canvas={self.re_canvas!r})"


class CursorFrame:
    images: List[CursorImage]
    delay: int

    def __init__(self, images: List[CursorImage], delay: int = 0) -> None:
        self.images = images
        self.delay = delay

    def __getitem__(self, item: int) -> CursorImage:
        return self.images[item]

    def __len__(self) -> int:
        return len(self.images)

    def __iter__(self) -> Iterator[CursorImage]:
        return iter(self.images)

    def __repr__(self) -> str:
        return f"CursorFrame(images={self.images!r}, delay={self.delay!r})"
