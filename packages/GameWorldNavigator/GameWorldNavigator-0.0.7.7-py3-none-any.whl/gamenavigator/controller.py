from ast import In, Tuple
from re import I
from typing import Any, Type, Union

from numpy import isin

from .core import Interface, InterfaceAction as Action, InterfaceStep, Pos, Image, StepContent
from .game_controller import GameController
from .game_interface_controller import GameInterfaceController
from .image_recognition import match_template

class Controller:
    def __init__(self, game_class: Union[str, None], game_name: str, root_inf: Interface) -> None:
        self.game_controller = GameController(game_class, game_name)
        self.inf_controller = GameInterfaceController(root_inf)
    
    def find_current_interface(self) -> Union[Interface, None]:
        """遍历查找当前是什么界面

        Returns:
            Interface: 当前界面,没找到返回None
        """
        interfaces = self.inf_controller.name_to_inf.values()
        game_img = self.game_controller.get_screenshot()
        
        res = None
        temp_val = 0.0
        for inf in interfaces:
            if isinstance(inf.id, Image):
                template = inf.id.cv2_image
            else:
                template = inf.id
            _, max_val, _, _ = match_template(game_img, template)
            if max_val > temp_val:
                temp_val = max_val
                res = inf
        return res
    
    def to_interface(self, inf_name: str) -> None:
        """切换界面

        Args:
            inf_name (str): 想要前往的界面
        """
        target_inf = self.inf_controller.get_interface(inf_name)
        steps = self.inf_controller.to_interface(inf_name)
        
        for step in steps:
            self.__run_inf_step(step)
        
        self.inf_controller.set_current(inf_name)
    
    def __run_inf_step(self, step: InterfaceStep) -> None:
        """运行界面步骤
        
        Args:
            step (InterfaceStep): 界面步骤
        
        """
        for step_content in step:
            action = step_content.action
            kwargs = step_content.kwargs
            content = step_content.content
            match action:
                case Action.MOUSE_CLICK:
                    if isinstance(content, tuple):
                        raise TypeError("Invalid mouse click argument")
                    self.__mouse_click(content, **kwargs)
                case Action.MOUSE_MOVE:
                    if isinstance(content, tuple):
                        raise TypeError("Invalid mouse move argument")
                    self.__mouse_move(content, **kwargs)
                case Action.MOUSE_DRAG:
                    if not isinstance(content, tuple):
                        raise TypeError("Invalid mouse drag argument")
                    elif len(content) != 2:
                        raise TypeError("Invalid mouse drag argument")
                    # 这里是为了让IDE识别content类型多此一举
                    p1, p2 = content
                    if not isinstance(p1, Pos) or not isinstance(p2, Pos):
                        raise TypeError("Invalid mouse drag argument")
                    self.__mouse_drag((p1, p2), **kwargs)
                case Action.KEYBOARD:
                    if not isinstance(content, (str, tuple)):
                        raise TypeError("Invalid keyboard argument")
                    self.__keyboard(content, **kwargs)

    def __mouse_click(self, arg: Union[str, Image, Pos], **kwargs) -> None:
        """鼠标点击

        Args:
            arg (Union[str, Image, Pos]): 要点击的元素,可以是文字,图像,位置

        Raises:
            TypeError: Invalid mouse click argument
        """
        if isinstance(arg, str):
            self.game_controller.click_text(arg, **kwargs)
        elif isinstance(arg, Image):
            self.game_controller.click_image(arg.cv2_image, **kwargs)
        elif isinstance(arg, Pos):
            self.game_controller.click_pos(arg)
        else:
            raise TypeError("Invalid mouse click argument")
    
    def __mouse_move(self, arg: Union[str, Image, Pos], **kwargs) -> None:
        """移动鼠标

        Args:
            arg (Union[str, Image, Pos]): 鼠标可以移动到文字,图像,位置
        """
        duration = kwargs.get("duration", 0.0)
        if isinstance(arg, Image):
            self.game_controller.mouse_move_to(arg.cv2_image, duration)
        else:
            self.game_controller.mouse_move_to(arg, duration)
    
    def __mouse_drag(self, arg: tuple[Pos, Pos], **kwargs):
        self.game_controller.mouse_drag(arg[0], arg[1], **kwargs)
    
    def __keyboard(self, arg: Union[str, tuple], **kwargs) -> None:
        if isinstance(arg, str):
            self.game_controller.down_keyboard_time(arg, 0.0, **kwargs)
        elif isinstance(arg, tuple):
            self.game_controller.down_keyboard_time(*arg, **kwargs)
