class Result:
    def __init__(self, status: bool, message: str = "", payload: list = []):
        self.__Status = status;
        self.__Message = message;
        self.__Payload = payload;

    def IsSuccess(self) -> bool:
        return self.__Status;

    def GetMessage(self) -> str:
        return self.__Message;