from PIL import Image, ImageDraw


class Hmi:
    def show_on_display(self, image: Image) -> None:
        raise RuntimeError("implement start-method in the respective hmi subclass!")

    @property
    def display(self) -> ImageDraw.Draw:
        raise RuntimeError("implement start-method in the respective hmi subclass!")
