import tkinter as TK;
from tkinter import ttk;
from tkinter import messagebox;
from tkcalendar import DateEntry;
from datetime import datetime;
import locale;
import sys;
from AlmaxUtils import Time as AUT;

WindowElementsDefaultPaddingWidth = 10;
WindowElementsDefaultPaddingHeight = 10;

class Window:
    def __init__(
        self,
        programName: str
    ):
        self.__Istance = TK.Tk();
        self.__Istance.resizable(False, False);
        self.__Istance.title(programName);

        self.__IsRunning = False;

        self.__Frames = {};
        self.__ButtonsToDisable = [];
        self.__RadioButtons = [];
   
    def AddFrame(self, frameName, position):
        self.__Frames[frameName] = TK.Frame(self.__Istance);
        self.__Frames[frameName].pack(anchor=position);
   
    def AddLabelToFrame(self, labelName: str, frameName: str, position):
        WindowLabelRow = WindowCreateLabel(self.__Istance, labelName);
        WindowLabelRow.pack(in_=self.__Frames[frameName], side=position);
        return WindowLabelRow;
   
    def AddButtonToFrame(self, buttonName: str, commandIndex: int, commandFunction, frameName: str, position, disableAtSubmit: bool = True, defaultDisabled: bool = False) -> TK.Button:
        WindowButtonRow = WindowCreateButton(self.__Istance, buttonName, commandIndex, commandFunction);
        WindowButtonRow.pack(in_=self.__Frames[frameName], side=position);
        if disableAtSubmit:
            self.__ButtonsToDisable.append(WindowButtonRow);
        if defaultDisabled:
            WindowButtonRow['state'] = "disabled";
            WindowButtonRow['width'] = len(WindowButtonRow['text'])-5;
        return WindowButtonRow;

    def AddRadioButtonToFrame(self, WindowRadioButtonOptions, WindowRadioButtonSelected, frameName, position):
        WindowRadioButtonRow = WindowCreateRadioButton(self.__Istance, WindowRadioButtonOptions, WindowRadioButtonSelected);
        for rb in WindowRadioButtonRow:
            rb.pack(in_=self.__Frames[frameName], side=position);
        self.__RadioButtons += WindowRadioButtonRow;
        return WindowRadioButtonRow;
   
    def AddProgressbarToFrame(self, frameName):
        WindowProgressionProgressbarRow = WindowCreateProgressbar(self.__Istance);
        Progression = ProgressbarProgression(
            WindowProgressionProgressbarRow,
            self.AddLabelToFrame("0%", "Progressbar", TK.LEFT)
        );

        WindowProgressionProgressbarRow.pack(in_=self.__Frames[frameName], side=TK.LEFT);
        return Progression;

    def AddCalendarToFrame(
            self, 
            frameName, 
            position, 
            defaultDate: datetime = AUT.now, 
            localeZone = 'it_IT',
            showLabel: bool = False
        ):
        locale.setlocale(locale.LC_TIME, localeZone);
        def update_label(event):
            dateLabel.config(text=date_entry.get_date().strftime('%A %d %B %Y'));
        
        date_entry = DateEntry(
            self.__Istance, 
            locale=localeZone, 
            date_pattern='dd/mm/y',
            selectmode="day",
            year=defaultDate.year, 
            month=defaultDate.month, 
            day=defaultDate.day
        );
        date_entry.pack(in_=self.__Frames[frameName], side=position);

        if showLabel:
            dateLabel = self.AddLabelToFrame("",frameName, TK.RIGHT);
            dateLabel.config(text=date_entry.get_date().strftime('%A %d %B %Y'));
            date_entry.bind("<<DateEntrySelected>>", update_label);

        return date_entry;

    def DisableAllButtons(self):
        for button in self.__ButtonsToDisable:
            button["state"] = "disabled";
        for rbutton in self.__RadioButtons:
            rbutton["state"] = "disabled";

    def Resize(self):
        self.__Istance.update_idletasks();
        self.__Istance.geometry(
            f"{
                self.__Istance.winfo_reqwidth()+WindowElementsDefaultPaddingWidth
            }x{
                self.__Istance.winfo_reqheight()+WindowElementsDefaultPaddingHeight
            }"
        );

    def Mainloop(self):
        self.Resize();
        self.__IsRunning = True;
        self.__Istance.mainloop();
   
    def Refresh(self):
        if self.__IsRunning and self.__Istance.winfo_exists():
            self.__Istance.update();
        else:
            sys.exit();

    def Destroy(self):
        print(f"{self.__Istance.title()} è stato Terminato!");
        messagebox.showinfo(self.__Istance.title(), "Le Operazioni sono state Concluse con successo!");
        self.__Istance.destroy();

    def Quit(self, message: str = ''):
        if message != '':
            messagebox.showerror(self.__Istance.title(), message);
        print(f"{self.__Istance.title()} è stato Terminato!");
        self.__IsRunning = False;
        self.__Istance.quit();
        sys.exit();
   
class ProgressbarProgression:
    def __init__(
        self,
        progressbarRow: ttk.Progressbar,
        progressbarPercRow: TK.Label,
        progressRatio: int = 50
    ):
        self.__Progression = 0;
        self.__ProgressbarRow = progressbarRow;
        self.__ProgressbarPercRow = progressbarPercRow;
        self.__ProgressRatio = progressRatio;
   
    def Update(self):
        self.__Progression += self.__ProgressRatio;
        self.__ProgressbarRow["value"] = self.__Progression;
        self.__ProgressbarRow.update();
        self.__ProgressbarPercRow["text"] = str(round(self.__Progression, 2)) + "%";
        self.__ProgressbarPercRow.update();

    def ChangeProgressionRatio(self, progressionRatio: int):
        self.__ProgressRatio = progressionRatio;

def WindowCreateLabel(
    Window: TK.Tk,
    Text: str
) -> TK.Label:
    WindowLabel = TK.Label(
        Window,
        text=Text,
        padx=WindowElementsDefaultPaddingWidth,
        pady=WindowElementsDefaultPaddingHeight,
        anchor=TK.W
    );
    return WindowLabel;

def WindowCreateButton(
    Window: TK.Tk,
    Text: str,
    CommandIndex: int,
    AssignCommand
) -> TK.Button:
    WindowButton = TK.Button(
        Window,
        text = Text,
        command = lambda: AssignCommand(WindowButton, CommandIndex),
        width=WindowElementsDefaultPaddingWidth,
        padx=WindowElementsDefaultPaddingWidth
    );
    return WindowButton;

def WindowCreateRadioButton(
    Window: TK.Tk,
    Options: list,
    WindowRadioButtonSelected: TK.IntVar
):
    radioButtons = [];
    for (optionLabel, optionValue) in Options:
        radioButtons.append(TK.Radiobutton(
            Window,
            text = optionLabel,
            value = optionValue,
            variable=WindowRadioButtonSelected,
            width=WindowElementsDefaultPaddingWidth
        ));
    return radioButtons;

def WindowCreateProgressbar(
   Window: TK.Tk
):
    progressbar = ttk.Progressbar(
        Window,
        mode="determinate",
        orient="horizontal",
        maximum=100,
        length=286
    );
    return progressbar;