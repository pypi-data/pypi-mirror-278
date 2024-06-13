"""界面类
通过创建一个个游戏界面类从而达到操控游戏的目的
"""

from enum import Enum
from typing import Dict, Union, List, Tuple, Any

from .image import Image
from .pos import Pos


class InterfaceAction(Enum):
    MOUSE_CLICK = 0  # 鼠标点击
    MOUSE_MOVE = 1  # 鼠标移动
    MOUSE_DRAG = 2  # 鼠标拖拽
    KEYBOARD = 3  # 键盘输入


DownTime = Union[int, float]


class StepContent(object):
    def __init__(
        self,
        action: InterfaceAction,
        content: Union[Image, str, Pos, Tuple[str, DownTime], Tuple[Pos, Pos]],
        kwargs: Union[Dict[str, object], None] = None,
    ) -> None:
        if kwargs is None:
            self.kwargs = dict()
        else:
            self.kwargs = kwargs
        self.action = action
        self.content = content


InterfaceStep = List[StepContent]


class Interface(object):
    def __init__(
        self,
        id_: Union[Image, str],
        only_name: str,
        to_parent_steps,
        to_child_steps,
        root=False,
    ):
        """界面类

        Args:
            id_ (Union[Image, str]): 界面的唯一标识, 可以是图片也可以是字符串
            only_name (str): 唯一名称, 不该出现重复名称
            to_parent_steps (Union[Dict[Interface, InterfaceStep], None]): 前往父界面的步骤
            to_child_steps (Union[Dict[Interface, InterfaceStep], None]): 前往子界面的步骤
            root (bool, optional): 用于标识是否为根界面. Defaults to False.
        """
        self._id: Image | str = id_  # 用来判断当前是不是这个界面
        self._root: bool = root  # 根界面标识
        self._name: str = only_name  # 界面名称
        self._to_parent_steps: Dict[Interface, InterfaceStep] = (
            dict() if to_parent_steps is None else to_parent_steps
        )
        self._to_child_steps: Dict[Interface, InterfaceStep] = (
            dict() if to_child_steps is None else to_child_steps
        )

    def add_interface(
        self, inf: "Interface", step: InterfaceStep, is_parent: bool
    ) -> None:
        """添加一个界面

        Args:
            inf (Interface): 界面
            step (InterfaceStep): 前往该新界面的步骤
            is_parent (bool): 是否为父界面
        """
        if inf in self._to_parent_steps or inf in self._to_child_steps:
            raise ValueError(f"界面{self.name}已经存在前往{inf.name}的步骤")
        if is_parent:
            self._to_parent_steps[inf] = step
        else:
            self._to_child_steps[inf] = step

    @property
    def children(self) -> list["Interface"]:
        return list(self._to_child_steps.keys())

    def get_interface(self, name: str) -> Union["Interface", None]:
        for p in self.parents:
            if p.name == name:
                return p
        for c in self.children:
            if c.name == name:
                return c
        return None

    def get_step(self, inf: "Interface") -> InterfaceStep:
        if inf in self._to_parent_steps:
            return self._to_parent_steps[inf]
        elif inf in self._to_child_steps:
            return self._to_child_steps[inf]
        else:
            raise ValueError(f"在界面{self.name}中找不到前往{inf.name}的步骤")

    @property
    def id(self) -> Union[Image, str]:
        return self._id

    @property
    def is_root(self) -> bool:
        return self._root

    @property
    def name(self) -> str:
        return self._name

    @property
    def parents(self) -> list["Interface"]:
        return list(self._to_parent_steps.keys())
