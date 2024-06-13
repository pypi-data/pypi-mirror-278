from functools import lru_cache
from typing import Union, Optional, List, Dict, Tuple
from collections import defaultdict, deque

from .core import Interface, InterfaceStep, Image
from .image_recognition import match_template
from .log import logger


class GameInterfaceController(object):
    def __init__(self, current_inf: Interface) -> None:
        self.current: Optional[Interface] = current_inf
        self.name_to_inf: Dict[str, Interface] = dict()
    
    def add_interface(self, interface: Interface) -> None:
        """ 添加界面 """
        self.name_to_inf[interface.name] = interface
    
    def add_interfaces(self, interfaces: List[Interface]) -> None:
        """ 添加界面 """
        for interface in interfaces:
            self.add_interface(interface)
    
    # 通过缓存加快查找速度
    @lru_cache(maxsize=128)
    def find_steps(self, start: str, target: str) -> List[InterfaceStep]:
        """查找从start到target的路径
        
        从start界面开始,向父界面以及子界面搜索,直到找到target界面或者搜索完所有界面

        Args:
            start (str): 当前界面的名称
            target (str): 目标界面的名称

        Returns:
            List[InterfaceStep]: 从start到target的路径
        """
        result = []
        directions = []
        
        def dfs(cur: Interface, pre=None):
            if cur.name == target:
                return True
            
            for nex in cur.parents:
                if nex == pre:
                    continue
                directions.append((0, nex.name))
                if dfs(nex, cur):
                    return True
                directions.pop()
                
            
            for nex in cur.children:
                if nex == pre:
                    continue
                directions.append((1, nex.name))
                if dfs(nex, cur):
                    return True
                directions.pop()
            return False
        
        dfs(self.name_to_inf[start])
        cur_inf = self.name_to_inf[start]
        for _, name in directions:
            inf = cur_inf.get_interface(name)
            if inf is None:
                raise ValueError(f"<界面{cur_inf.name}>找不到界面<{name}>")
            result.append(cur_inf.get_step(inf))
            cur_inf = inf
        return result
    
    def get_interface(self, inf_name: str) -> Interface:
        return self.name_to_inf[inf_name]
    
    def to_interface(self, interface_name: str) -> List[InterfaceStep]:
        current_inf = self.current
        if current_inf is None:
            logger.error("当前界面为None,请初始化当前界面")
            return []
        if interface_name == current_inf.name:
            logger.debug(f"当前界面为{current_inf.name},无需切换")
            return []
        steps = self.find_steps(current_inf.name, interface_name)
        return steps

    def set_current(self, inf_name: str):
        self.current = self.name_to_inf[inf_name]
    
    def exists(self, name: str) -> bool:
        return name in self.name_to_inf

