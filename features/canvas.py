from __future__ import annotations

from typing import List

from features.tuple import Color

class Canvas:
    def __init__(self, w=0, h=0, c=Color(0,0,0)):
        self.width = w
        self.height = h
        self.grid: List[List[float]] = [[c] * self.width for _ in range(self.height)]

    def write_pixel(self, w, h, c) -> None:
        try:
            self.grid[h][w] = c
        except IndexError as e:
            print(f"out of range for grid[{self.width}][{self.height}]")

    def pixel_at(self, w, h) -> float:
        try:
            return self.grid[h][w]
        except IndexError as e:
            print(f"out of range for grid[{self.width}][{self.height}]")

    def header(self) -> str:
        return f"P3\n{self.width} {self.height}\n255\n"

    def to_ppm(self) -> str:
        header = self.header()
        ppm_data = ""
        for row in self.grid:
            ppm_row = []
            for pixel in row:
                (r, g, b) = pixel.to_rgb()
                ppm_row.extend([r, g, b])
            # ppm_data += " ".join(str(i) for i in ppm_row)
            # but break into at most 17 elements per line to stay < 70 chars
            for line in [ppm_row[i: i + 17] for i in range(0, len(ppm_row), 17)]:
                ppm_data += " ".join(str(c) for c in line) + "\n"
        return header + ppm_data

