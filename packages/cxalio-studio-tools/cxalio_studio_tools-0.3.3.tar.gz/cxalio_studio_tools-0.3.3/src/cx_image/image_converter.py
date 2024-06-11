from typing import Callable

from PIL import Image


class ImageProcessor:
    """
    图像处理器基类。
    这个类提供了一个 __call__ 方法接口用于执行图像转换操作。
    所有继承自 ImageProcessor 的子类都应该重写这个方法来实现具体处理逻辑。
    """

    def __call__(self, image: Image):
        """执行图像处理操作的方法，需要在子类中被覆盖实现。"""
        raise NotImplementedError("The __call__ method must be implemented by subclass.")


class ImageConverter:
    """用于转换图片格式的转换器类。使用Pillow库。"""

    ACCEPTABLE_OUTPUT_FORMATS = {
        "BMP": ".bmp",
        "EPS": ".eps",
        "GIF": ".gif",
        "ICO": ".ico",
        "IM": ".im",
        "JPEG": ".jpg",
        "JPEG 2000": ".jp2",
        "MSP": ".msp",
        "PCX": ".pcx",
        "PDF": ".pdf",
        "PNG": ".png",
        "PPM": ".ppm",
        "SGI": ".sgi",
        "SPI": ".spi",
        "TGA": ".tga",
        "TIFF": ".tiff",
        "WEBP": ".webp",
        "XBM": ".xbm"
    }

    def __init__(self, output_format=None, quality=85, *processors):
        self._output_format = output_format
        self._quality = quality
        self._processors = list(processors)

    def install_processor(self, processor):
        if isinstance(processor, ImageProcessor) or isinstance(processor, Callable):
            self._processors.append(processor)
        else:
            raise TypeError('processor must be an instance of ImageProcessor or a Callable')

    def convert(self, input_path, output_path):
        # 打开输入图片文件
        with Image.open(input_path) as img:
            # 链式调用所有安装的处理器
            for processor in self._processors:
                img = processor(img)
            # 将图片保存到目标路径，并设置格式和质量。
            img.save(output_path, format=self._output_format, quality=self._quality)
