import ctypes
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Union, Optional

import cv2
import win32api
import win32con
import win32gui
import win32print
from PIL import ImageGrab
from cv2.typing import MatLike
from numpy import ndarray, array

from . import log
from .core import Pos, Rect
from .exception import (
    TemplateMathingFailure,
    WindowOutOfBoundsError,
    TextMatchingFailure,
)
from .image_recognition import match_template
from .keyboard_mouse_simulation import (
    mouse_click_position,
    mouse_move_to,
    mouse_scroll,
    keyboard_press,
    keyboard_down,
    keyboard_up,
    mouse_drag,
)
from .ocr_recognition import get_text_position, get_text_direction_position


def _get_screen_size():
    """电脑缩放后的分辨率"""
    w = win32api.GetSystemMetrics(0)
    h = win32api.GetSystemMetrics(1)
    return w, h


def _get_read_size():
    """获取电脑真实分辨率"""
    hdc = win32gui.GetDC(0)
    w = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES)
    h = win32print.GetDeviceCaps(hdc, win32con.DESKTOPVERTRES)
    return w, h


def _get_scaling() -> float:
    """获取电脑缩放率"""
    return round(_get_read_size()[0] / _get_screen_size()[0], 2)


THREAD_POOL = ThreadPoolExecutor(max_workers=100)


class Game:
    def __init__(self, game_class: Union[str, None], game_name: str):
        """
        :param game_class: 游戏类名
        :param game_name: 游戏名称
        """
        self.screenshot: Optional[ndarray] = None
        self._game_class = game_class
        self._game_name = game_name
        self._hwnd = win32gui.FindWindow(game_class, game_name)

        log.debug(f"class : {game_class}, name : {game_name}, hwnd : {self._hwnd}")

    @property
    def cls(self) -> Union[str, None]:
        return self._game_class

    @property
    def hwnd(self) -> int:
        return self._hwnd

    @property
    def width(self) -> int:
        rect = self.get_view_rect()
        return rect.right - rect.left

    @property
    def height(self) -> int:
        rect = self.get_view_rect()
        return rect.bottom - rect.top

    @property
    def top_left(self) -> Pos:
        rect = self.get_rect()
        pos = Pos(rect.left, rect.top)
        return pos

    @property
    def scaling(self) -> float:
        return ctypes.windll.user32.GetDpiForWindow(self._hwnd) / 96.0

    @property
    def name(self) -> str:
        return self._game_name

    def set_foreground(self) -> None:
        """设置游戏到前台API"""
        win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self._hwnd)

    def get_screenshot(self) -> ndarray:
        """游戏截图API"""
        grab = ImageGrab.grab(bbox=(self.get_rect().rect()))
        img = array(grab)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.screenshot = img
        return img

    def get_rect(self) -> Rect:
        """获取游戏的矩形"""
        x1, y1, x2, y2 = win32gui.GetWindowRect(self._hwnd)
        s = _get_scaling()  # 电脑缩放率
        x1, y1 = int(x1 * s), int(y1 * s)
        x2, y2 = int(x2 * s), int(y2 * s)
        return Rect(x1, y1, x2, y2)
    
    def get_view_rect(self) -> Rect:
        """获取游戏显示区域矩形(不包括标题栏以及边框)"""
        x1, y1, x2, y2 = win32gui.GetClientRect(self._hwnd)
        s = _get_scaling()  # 电脑缩放率
        x1, y1 = int(x1 * s), int(y1 * s)
        x2, y2 = int(x2 * s), int(y2 * s)
        return Rect(x1, y1, x2, y2)

    def get_image_pos(self, image: Union[str, ndarray]) -> Pos:
        """获取游戏内图片位置API

        Args:
            image (Union[str, ndarray]): 模板图
        """
        _, _, _, max_loc = match_template(self.get_screenshot(), image)
        pos = Pos(max_loc[0], max_loc[1])
        return pos

    def get_text_pos(self, texts: tuple[str, ...], direction: str = "center") -> Pos:
        """获取游戏内文字位置API

        Args:
            text (str): 文字
            direction (str, optional): 文字的位置方向 [left, center, right]. Defaults to "center".
        """
        positions = get_text_position(self.get_screenshot(), texts)
        pos = get_text_direction_position(positions, direction)
        return pos


class GameController:
    def __init__(self, game_class: Union[str, None], game_name: str):
        """
        将debug设置为True后需要设置filename才会将调试信息保存

        Args:
            game_class (str, None): 游戏类型
            game_name (str): 游戏名称
        """
        self.game = Game(game_class, game_name)

    def click_pos(self, pos: Pos) -> None:
        """模拟鼠标点击游戏内坐标API

        Args:
            pos (Pos): 坐标
        """
        self.set_foreground()
        try:
            self._click_pos(pos)
        except WindowOutOfBoundsError:
            raise

    def click_image(self, *images: Union[str, ndarray, MatLike], **kwargs):
        """模拟鼠标点击游戏内图片API

        鼠标点击图片中心位置，若传入多个图像则只会点击一个

        Args:
            images (str, ndarray, MatLike): 图像

        Keyword Arguments:
            threshold (int, float): 匹配阈值(default 0.8)
            mode (str): 匹配模式(default)
            x (int): x偏移 (default 0)
            y (int): y偏移 (default 0)
        """
        self.set_foreground()
        try:
            self._click_image(*images, **kwargs)
        except TemplateMathingFailure:
            raise

    def click_text(self, text: str, position: str = "center", **kwargs) -> None:
        """模拟鼠标点击游戏内文字API

        Args:
            text (str): 文字
            position (str): 文字位置(default "center") left, center, right

        Keyword Arguments:
            x (int): x偏移 (default 0)
            y (int): y偏移 (default 0)
        """
        if not isinstance(text, str):
            raise TypeError("text must is str type")
        if not isinstance(position, str):
            raise TypeError("position must is str type")
        try:
            self._click_text(text, position, **kwargs)
        except TextMatchingFailure:
            raise

    def down_keyboard_time(
        self, key: str, stop_time: float, thread=True
    ) -> Union[None, Future]:
        """模拟键盘按压

        Args:
            key (str): 按键
            stop_time (float): 按压时长
            thread (bool, optional): 是否开启线程. Defaults to True.

        Raises:
            TypeError: 类型错误

        Returns:
            Union[None, Future]: 若开启线程则会返回Future对象,否则返回None
        """
        if not isinstance(stop_time, float):
            raise TypeError("param stop_time must is float type")
        if not isinstance(thread, bool):
            raise TypeError("param thread must is bool type")
        self.set_foreground()

        def func():
            keyboard_down(key)
            time.sleep(stop_time)
            keyboard_up(key)

        if thread:
            res = THREAD_POOL.submit(func)
            return res
            # 运行子线程并且返回子线程
        func()
        # 阻塞当前线程直到达到按压时长
        return None

    def get_screenshot(self) -> ndarray:
        """获取游戏截图"""
        return self.game.get_screenshot()

    def image_in_game(self, image: Union[str, ndarray, MatLike], **kwargs) -> bool:
        """判断游戏内是否存在该图片

        Args:
            image (Union[str, ndarray, MatLike]): 模板图
            threshold (float, optional): 匹配阈值(default 0.8)
            mode (str, optional): 匹配模式(default color)

        Returns:
            bool: 是否存在
        """
        threshold = kwargs.get("threshold", 0.8)
        mode = kwargs.get("mode", "color")
        screenshot = self.get_screenshot()
        _, val, _, _ = match_template(screenshot, image, mode=mode)
        return val >= threshold
    
    def press(self, key: str) -> None:
        """模拟键盘按键按压API"""
        self.set_foreground()
        keyboard_press(key)

    def set_foreground(self) -> None:
        """设置游戏到前台"""
        hwnd = win32gui.GetForegroundWindow()
        text = win32gui.GetWindowText(hwnd)
        if text != self.game.name:
            self.game.set_foreground()
            time.sleep(1)

    @property
    def screenshot(self) -> Union[ndarray, None]:
        return self.game.screenshot

    def mouse_move_to(self, target: Union[str, ndarray, Pos], duration: float) -> None:
        """模拟鼠标移动API

        鼠标从当前位置移动到pos持续duration

        Args:
            target (Union[str, ndarray, Pos]): 坐标
            duration (float): 持续时间
        """
        self.set_foreground()
        try:
            self._mouse_move_to(target, duration)
        except WindowOutOfBoundsError:
            raise

    def mouse_drag(self, start: Pos, end: Pos, button="left") -> None:
        """按压鼠标并移动到end松开API"""
        self.set_foreground()
        try:
            start = self._to_global_pos(start)
            end = self._to_global_pos(end)
        except WindowOutOfBoundsError:
            raise
        mouse_drag(start, end, button)

    def mouse_scroll(self, pos: Pos, scale: int, count: int, duration=0.0):
        """鼠标移动至pos滚动scale刻度count次
        Args:
            pos (Pos): 坐标
            scale (int): 刻度
            count (int): 次数
            duration (float): 移动到坐标点的时间
        """
        self.set_foreground()
        self.mouse_move_to(pos, duration)
        mouse_scroll(scale, count)

    def wait_image(self, *images: Union[str, ndarray, MatLike], **kwargs) -> None:
        """等待游戏内图片API

        Args:
            images: (str, ndarray, MatLike)可以多张图片，也可以单张图片

        Keyword Arguments:
            all (bool): True等待所有图片，False其中一个图片(default False)
            timeout (int, float): 等待时间(default 60)
            spacing (int, float): 每次匹配时间间隔(default 1)
            threshold (int, float): 达到该阈值算匹配成功(default 0.8)
            mode (str): 匹配模式

        Raises:
            TimeoutError: 超时
        """
        self.set_foreground()
        try:
            self._wait_image(*images, **kwargs)
        except TimeoutError:
            raise

    def _click_pos(self, pos: Pos) -> None:
        """点击游戏内某个坐标"""
        game_pos = self._to_global_pos(pos)
        mouse_click_position(game_pos)

    def _click_image(self, *images: Union[str, ndarray, MatLike], **kwargs) -> None:
        """点击游戏内图片"""
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        threshold = kwargs.get("threshold", 0.8)
        mode = kwargs.get("mode", "color")
        if not isinstance(x, int):
            raise TypeError("param x must is int type")
        if not isinstance(y, int):
            raise TypeError("param y must is int type")
        if not isinstance(threshold, (int, float)):
            raise TypeError("param threshold must is int or float type")
        if not isinstance(mode, str):
            raise TypeError("param mode must is str type")
        screenshot = self.game.get_screenshot()
        v, p = 0.0, Pos(0, 0)
        log.debug(f"click image: threshold={threshold}, mode={mode}")
        for image in images:
            if not isinstance(image, (str, ndarray)):
                raise TypeError("param image must is str or ndarray type")
            if isinstance(image, str):
                image = cv2.imread(image)
            _, max_val, _, max_loc = match_template(screenshot, image, mode=mode)
            if max_val < threshold:
                if max_val > v:
                    v = max_val
                    p = Pos(max_loc[0], max_loc[1])
                continue
                # 低于阈值的跳过
            else:
                log.debug(f"max_val={max_val}, threshold={threshold}")
                h, w = image.shape[:2]
                center = Pos(max_loc[0] + w // 2, max_loc[1] + h // 2)
                center += Pos(x, y)
                self.click_pos(center)
                return
        log.error(f"template matching failure, max value is {v}")
        raise TemplateMathingFailure(f"Threshold: {v} < {threshold}, GamePos: {p}")

    def _click_text(self, text: str, position: str = "center", **kwargs) -> None:
        """点击游戏内文字"""
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        add_pos = Pos(x, y)
        positions = get_text_position(self.game.get_screenshot(), text)
        if positions.size == 0:
            raise TextMatchingFailure(f"The text does not exist in the game")
            # 没有匹配到相关的文字
        index = 0
        if position == "center":
            index = (positions.size - 1) // 2
            if index < 0:
                index = 0
        elif position == "right":
            index = -1
        position = positions[index]
        x, y = position
        pos = Pos(int(x), int(y)) + add_pos
        self.click_pos(pos)

    def _mouse_move_to(self, target: Union[str, ndarray, Pos], duration: float) -> None:
        """鼠标移动到目标位置

        Args:
            target (Union[str, ndarray, Pos]): 目标位置,文本,图片,坐标
            duration (float): 从当前鼠标位置移动到目标位置的时间
        """
        if isinstance(target, str):
            positions = get_text_position(self.game.get_screenshot(), target)
            pos = get_text_direction_position(positions, "center")
        elif isinstance(target, ndarray):
            _, _, _, max_loc = match_template(self.game.get_screenshot(), target)
            pos = Pos(max_loc[0], max_loc[1])
        elif isinstance(target, Pos):
            pos = target
        else:
            raise TypeError("param target must is str, ndarray or Pos type")
        global_pos = self._to_global_pos(pos)
        mouse_move_to(global_pos, duration)

    def _to_global_pos(self, pos: Pos) -> Pos:
        """将游戏相对坐标转化成全局坐标

        Args:
            pos (Pos): 游戏内坐标

        Raises:
            WindowOutOfBoundsError: 给出的坐标超出游戏窗口范围

        Returns:
            Pos: 全局坐标
        """
        if pos.is_global:
            return pos
        rect = self.game.get_rect()
        x1, y1 = pos.x, pos.y
        x2, y2 = x1 + rect.left, y1 + rect.top
        # 坐标转换成游戏内坐标
        if x2 < rect.left or x2 > rect.right or y2 < rect.top or y2 > rect.bottom:
            log.error(f"The given coordinate ({x2}, {y2}) is outside")
            raise WindowOutOfBoundsError(
                f"The given coordinate ({x2}, {y2}) is outside "
                f"the game window bounds "
                f"({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})"
            )
            # 给出的坐标超出游戏窗口范围
        global_pos = Pos(x2, y2)
        return global_pos

    def _wait_image(self, *images: Union[str, ndarray], **kwargs) -> None:
        """等待图片
        阻塞线程等待图片出现或者超市

        Args:
            *images (Union[str, ndarray]): 图片路径,图片,图片模板
            all (bool, optional): 是否需要所有图片同时出现. Defaults to False.
            threshold (float, optional): 匹配阈值. Defaults to 0.8.
            mode (str, optional): 匹配模式. Defaults to "color".
            timeout (int, optional): 超时时间. Defaults to 60.
            spacing (int, optional): 图片间隔时间. Defaults to 1.

        Raises:
            TypeError: 参数类型错误
            TimeoutError: 超时
        """
        all_ = kwargs.get("all", False)
        threshold = kwargs.get("threshold", 0.8)
        mode = kwargs.get("mode", "color")
        timeout = kwargs.get("timeout", 60)  # second
        spacing = kwargs.get("spacing", 1)  # second
        start_time = time.time()
        length = len(images)
        if not isinstance(all_, bool):
            raise TypeError("param all must is bool type")
        if not isinstance(threshold, (int, float)):
            raise TypeError("param threshold must is int or float type")
        if not isinstance(mode, str):
            raise TypeError("param mode must is str type")
        if not isinstance(timeout, int):
            raise TypeError("param timeout must is int type")
        if not isinstance(spacing, int):
            raise TypeError("param spacing must is int type")

        while time.time() - start_time <= timeout:
            count = 0
            for image in images:
                screenshot = self.game.get_screenshot()
                _, max_val, _, max_loc = match_template(screenshot, image, mode=mode)
                if max_val >= threshold:
                    count += 1
                    if not all_:
                        # 不需要全部匹配成功
                        return
                if count == length:
                    # 全部匹配成功
                    return
            time.sleep(spacing)
        log.error(f"Wait timeout: timeout={timeout}, spacing={spacing}")
        raise TimeoutError(f"Wait timeout")
