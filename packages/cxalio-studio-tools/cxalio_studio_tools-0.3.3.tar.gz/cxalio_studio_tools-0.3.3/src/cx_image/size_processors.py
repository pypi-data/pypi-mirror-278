from functools import cached_property

from PIL import Image

from .image_converter import ImageProcessor


class MaxEdgeResizeProcessor(ImageProcessor):
    """
    图片长边尺寸检查器。
    当图片最长边超过指定长度时，将其等比例缩放至最大长度范围内。
    如果图片在安全尺寸范围内，则保持原始大小不变。
    Attributes:
        max_edge_length (int): 图片允许的最大边长。
    构造函数初始化图片长边尺寸检查器实例。
     Parameters:
        max_edge_length (int): 允许的图片最大边长。
   """

    def __init__(self, max_edge_length):
        self._max_edge_length = max_edge_length

    @cached_property
    def max_edge_length(self):
        if self._max_edge_length > 0:
            return self._max_edge_length
        return 0

    def __call__(self, image: Image):
        """
        处理图像，按比例缩放图像确保最长边不超过设定值。
        Parameters:
            image (Image): 需要处理的 PIL Image 对象。
        Returns:
            Image: 处理后（可能被缩放）的 PIL Image 对象。
        """
        original_width, original_height = image.size
        longer_edge = max(original_width, original_height)
        # 如果图片大小超过限制，则调整大小
        if 0 < self.max_edge_length < longer_edge:
            scale_ratio = self.max_edge_length / float(longer_edge)
            new_width = int(original_width * scale_ratio)
            new_height = int(original_height * scale_ratio)
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return image


class MaxAreaResizeProcessor(ImageProcessor):
    def __init__(self, width, height=1):
        """
        构造函数初始化图像根据最大面积进行缩放的处理器。
        参数：
            width (int): 图片允许的最大宽度。
            height (int): 图片允许的最大高度。
        """
        self.width = width
        self.height = height

    @cached_property
    def max_area(self):
        """
        计算并返回合法的图片最大面积。如果计算结果小于等于0，则只会返回0。
        返回：
            int: 合法的图片最大面积或者0。
        """
        area = self.width * self.height
        return area if area > 0 else 0

    def __call__(self, image):
        # 获取当前图片尺寸和面积
        original_width, original_height = image.size
        current_area = original_width * original_height
        # 如果当前图片大小超过允许最大值且max_area属性值有效，则调整大小
        if current_area > self.max_area > 0:
            scale_factor = (self.max_area / float(current_area)) ** 0.5  # 开平方以得到边长比率
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # 如果max_area为非正数或图片未超出限定大小则不做改变直接返回原图像对象
        return image


class ForceSizeProcessor(ImageProcessor):
    def __init__(self, width, height, fill=True, keep_aspect=True, background_color=(255, 255, 255)):
        """
        初始化强制调整图片尺寸和填充方式的处理器。
        参数:
            width (int): 目标宽度。
            height (int): 目标高度。
            fill (bool): 是否填满画面。
            keep_aspect (bool): 是否保持原图比例。
            background_color (tuple): 背景颜色，默认为白色背景。(R,G,B)
        """
        self._width = width
        self._height = height
        self._fill = fill
        self._keep_aspect = keep_aspect
        self._background_color = background_color

    @property
    def target_size(self):
        return self._width, self._height

    def __call__(self, image: Image.Image) -> Image.Image:
        if not isinstance(image, Image.Image):
            raise ValueError("The input must be a PIL Image object.")
        # Step 1: Calculate scale ratio
        if self._keep_aspect:
            if self._fill:
                scale_ratio = max(self._width / image.width, self._height / image.height)
            else:
                scale_ratio = min(self._width / image.width, self._height / image.height)
            new_width = int(image.width * scale_ratio)
            new_height = int(image.height * scale_ratio)
        else:
            new_width = self._width
            new_height = self._height
        # Step 2: Resize the original image
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # Step 3: Create the background image
        background_image = Image.new('RGB', (self._width, self._height), color=self._background_color)
        # Step 4: Calculate paste coordinates
        paste_x = (self._width - new_width) // 2
        paste_y = (self._height - new_height) // 2
        # Step 5: Paste the resized image onto the background
        background_image.paste(resized_image, (paste_x, paste_y))
        return background_image
