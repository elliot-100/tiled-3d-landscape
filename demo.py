"""Run a simple demo."""

from app import App

WINDOW_SIZE = 700, 480
LANDSCAPE_SIZE_TILES = 16, 16

if __name__ == "__main__":
    demo = App(
        window_size=WINDOW_SIZE,
        landscape_size_tiles=LANDSCAPE_SIZE_TILES,
    )
    demo.run()
