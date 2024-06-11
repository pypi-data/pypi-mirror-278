import subprocess;

class CustomSubprocess:
    def __init__(self):
        self.__Command = [];
        self.__Istance = None;
   
    def Run(self, command: list):
        self.ChangeCommand(command);
        self.Start();
   
    def ChangeCommand(self, command):
        self.__Command = command;

    def Start(self):
        if self.__Istance is None or self.__Istance.poll() is not None:
            self.__Istance = subprocess.Popen(
                self.__Command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            );
   
    def HasFinished(self):
        return (self.__Istance is not None and self.__Istance.poll() is not None);

    def Stop(self):
        if self.__Istance:
            self.__Istance.terminate();
            self.__Istance = None;
