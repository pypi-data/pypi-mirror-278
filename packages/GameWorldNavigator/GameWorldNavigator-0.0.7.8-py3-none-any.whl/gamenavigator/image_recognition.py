from ast import Tuple
import cv2
import numpy as np
from typing import Union
from cv2.typing import MatLike, Point


def __to_ndarray(img: Union[str, np.ndarray, MatLike]) -> Union[np.ndarray, MatLike]:
    """若img是图像路径则读取后返回，否则直接返回"""
    if isinstance(img, str):
        img = cv2.imread(img)
    return img


def match_template(
    img: Union[str, np.ndarray], template: Union[str, np.ndarray], **kwargs
) -> tuple[float, float, Point, Point]:
    """图像匹配
    使用的是cv2的模板匹配，必须要保证 img 和 template 是属于同一种类型图像，即都是灰度图或彩色图，且大小一致。
    使用的是cv2.TM_CCOEFF_NORMED进行模板匹配，可以通过修改method来自定义模板匹配。图像必须是BGR格式

    Keyword Arguments:
        method (str): 模板匹配方法，默认是TM_CCOEFF_NORMED  str类型
        mode (str): 匹配模式 color binary gray (default color)
        thresh (int): 只有在二值图模式下才有用  int类型
        max_val (int): 只有在二值图模式下才有用  int类型

    Returns:
        min_val, max_val, min_loc, max_loc
    """
    if not isinstance(img, (str, np.ndarray)):
        raise TypeError("only accept str or np.ndarray or MatLike")
    elif not isinstance(template, (str, np.ndarray)):
        raise TypeError("only accept str or np.ndarray or MatLike")

    img = __to_ndarray(img)
    template = __to_ndarray(template)

    method = kwargs.get("method", "TM_CCOEFF_NORMED")
    method_check = (
        "TM_SQDIFF",
        "TM_SQDIFF_NORMED",
        "TM_CCOEFF_NORMED",
        "TM_CCORR_NORMED",
        "TM_CCORR",
        "TM_CCOEFF",
    )
    mode = kwargs.get("mode", "color")
    mode_check = ("color", "gray", "binary")

    # 判断传入的关键词是否支持
    if method not in method_check:
        raise ValueError(f"method must in {method_check}")
    elif mode not in mode_check:
        raise ValueError(f"mode must in {mode_check}")

    method = eval(f"cv2.{method}")
    i_channel = img.ndim
    t_channel = template.ndim
    
    match mode:
        case "color":
            if i_channel != 3 or t_channel != 3:
                raise ValueError("Image or template channels not equal to 3")
            res = cv2.matchTemplate(img, template, method)
            return cv2.minMaxLoc(res)
        case "gray":
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if i_channel == 3 else img
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) if t_channel == 3 else template
            res = cv2.matchTemplate(img_gray, template_gray, method)
            return cv2.minMaxLoc(res)
        case "binary":
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if i_channel == 3 else img
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) if t_channel == 3 else template
            thresh = kwargs.get("thresh", 127)
            max_val = kwargs.get("max_val", 255)
            _, img_binary = cv2.threshold(img_gray, thresh, max_val, cv2.THRESH_BINARY)
            _, template_binary = cv2.threshold(
                template_gray, thresh, max_val, cv2.THRESH_BINARY
            )
            res = cv2.matchTemplate(img_binary, template_binary, method)
            return cv2.minMaxLoc(res)
        case _:
            raise ValueError("mode must in ('color', 'gray', 'binary')")


def where_img(
    img: Union[str, np.ndarray],
    template: Union[str, np.ndarray],
    threshold=0.8,
) -> tuple:
    """查找所有匹配的图片

    Args:
        img (Union[str, np.ndarray]): 要检测的图片
        template (Union[str, np.ndarray]): 模板图片
        threshold (float, optional): 阈值,大于等于该阈值的对象被视为是类似图片. Defaults to 0.8.

    Returns:
        tuple: 一个元组,包含所有匹配的图片坐标
    """
    img = __to_ndarray(img)
    template = __to_ndarray(template)
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    positions = np.where(res >= threshold)
    return tuple(zip(*positions[::-1]))
