from functools import cached_property

from .image_converter import ImageProcessor


class ColorSpaceProcessor(ImageProcessor):
    COLOR_SPACES = {
        "binary": "1",  # 1-bit 像素，黑和白，存储每个像素 8 个像素
        "grayscale": "L",  # 8-bit 像素，黑和白
        "greyscale": "L",
        "palette": "P",  # 8-bit 像素，使用调色板映射到任何其他模式
        "rgb": "RGB",  # 3x8-bit 像素，真彩
        "rgba": "RGBA",  # 4x8-bit 像素，真彩，带透明度掩模
        "cmyk": "CMYK",  # 4x8-bit 像素
        "yuv": "YCbCr",  # 3x8-bit 像素，颜色视频格式
        "lab": "LAB",  # 3x8-bit 像素
        "hsv": "HSV",  # 3x8-bit 像素
        "int32": "I",  # 32-bit 整型像素
        "float32": "F",  # 32-bit 浮点型像素
        "auto": None
    }

    def __init__(self, color_space='auto'):
        self._color_space = color_space

    @cached_property
    def _convert_arg(self):
        return ColorSpaceProcessor.COLOR_SPACES.get(self._color_space.strip().lower(), None)

    def __call__(self, image):
        if self._convert_arg:
            return image.convert(self._convert_arg)
        return image
