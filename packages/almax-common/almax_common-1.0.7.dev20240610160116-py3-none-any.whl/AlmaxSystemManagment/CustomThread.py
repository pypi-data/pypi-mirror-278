import threading;
from typing import Callable;
from queue import Queue;

class CustomThread:
    def __init__(self):
        self.__Istance = None;
        self.__Result = Queue();
   
    def Run(self, function: Callable[[str, int], int], par1: str, par2: int):
        self.__Istance = threading.Thread(target=function, args=(par1, par2));
        self.__Istance.start();
   
    def GetResults(self):
        return self.__Result.get();
   
    def HasFinished(self):
        if self.__Istance.is_alive():
            return False;
        else:
            self.__Result.put("ok");
            return True;

    def Stop(self):
        self.__Istance.join(timeout=0);