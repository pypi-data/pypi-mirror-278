import codicefiscale as CFLib;

def PrintBytes(size: int) -> str:
    if size > 1024:
        size = round(size / 1024, 2);
        if(size > 1024):
            size = round(size / 1024, 4);
            if(size > 1024):
                size = round(size / 1024, 8);
                if(size > 1024):
                    size = round(size / 1024, 16);
                    return f"{size} TB";
                else:
                    return f"{size} GB";
            else:
                return f"{size} MB";
        else:
            return f"{size} KB";
   
    return f"{size} B";

def CheckStringInFile(file_path, target_string):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if target_string in line:
                    return True;
        return False;
    except FileNotFoundError:
        return False;

def CleanArrayFromEmptyString(array: list) -> list:
    return [string for string in array if string != ""];

def ReadFile(file_path: str) -> list:
    with open(file_path, 'r') as file:
        lines = file.readlines();
    return lines;

def isCodiceFiscale(parola):
    """ - DA RIVEDERE - Data in input una stringa, viene analizzata la composizione della stringa per determinare se è un codice fiscale o meno.
    Ritorna True in caso sia un codice fiscale, False altrimenti. """
    trovato = False,parola
    if len(parola) > 16:

        trovato = isCodiceFiscale(parola[0:16])
        if trovato[0]:
            return True,parola[0:16]

        trovato = isCodiceFiscale(parola[-16:])
        if trovato[0]:
            return True,parola[-16:]
        return False,parola

    if len(parola) == 16:
        if ( (not parola[0:6].isnumeric()) and (parola[6:8].isnumeric()) and (not parola[8].isnumeric()) and (parola[9:11].isnumeric()) and (not parola[15].isnumeric()) ):
            return CFLib.isvalid(parola),parola
        return False,parola
    return trovato;

def AllElementsHaveSameClass(array: list, cls) -> bool:
    return all(isinstance(element, cls) for element in array);