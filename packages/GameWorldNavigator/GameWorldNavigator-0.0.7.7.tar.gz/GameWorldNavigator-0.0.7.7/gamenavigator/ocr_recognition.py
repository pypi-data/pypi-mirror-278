"""OCR模块
"""
from ppocronnx import TextSystem
from numpy import ndarray, array

from . import log
from .core import Pos

system = TextSystem(use_angle_cls=False)


def get_text_position(img: ndarray, texts: tuple[str, ...]) -> ndarray:
    """获取输入的文本坐标

    优先返回与text完全相同的文本的坐标,其次返回相似度最高的文本的坐标,最后返回空坐标

    Args:
        img (ndarray): 图像
        text (str): 文本

    Returns:
        ndarray: 文本坐标
    """
    res = system.detect_and_ocr(img)
    equal = None
    equal_val = 0
    similarity = None
    similarity_val = 0
    for i in range(len(res)):
        box = res[i]
        for text in texts:
            if box.ocr_text == text:
                if box.score > equal_val:
                    equal_val = box.score
                    equal = box.box
            if text in box.ocr_text:
                if box.score > similarity_val:
                    similarity_val = box.score
                    similarity = box.box
    if equal is not None:
        return equal
    elif similarity is not None:
        return similarity
    log.debug("There are no equal or similar texts")
    return array([])

def get_text_direction_position(positions: ndarray, direction: str = "center") -> Pos:
    """获取文本方向坐标

    Args:
        positions (ndarray): 文本坐标
        direction (str, optional): 可以是["left", "center", "right"]. Defaults to "center".

    Returns:
        Pos: 坐标
    """
    index = 0
    if direction == "center":
        index = (positions.size - 1) // 2
        if index < 0:
            index = 0
    elif direction == "right":
        index = -1
    positions = positions[index]
    x, y = positions
    pos = Pos(int(x), int(y))
    return pos

def text_in_img(img: ndarray, texts: tuple[str, ...]) -> bool:
    """ 判断图片中是否包含该文本 """
    res = get_text_position(img, texts)
    return res.size != 0
