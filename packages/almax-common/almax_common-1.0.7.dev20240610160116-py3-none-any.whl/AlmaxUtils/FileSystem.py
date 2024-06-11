import os, shutil;

def CleanPath(path: str, cleanString: str) -> str:
    return path.replace("\\", cleanString).replace('/', cleanString);

def GetSubFolders(folder: str) -> list:
    return [ f.path for f in os.scandir(folder) if f.is_dir() ];

def GetSubFolders(folder: str, level: int) -> list:
    subfolders = [];
    level -= 1;
    if level == 0:
        content = [ f.path for f in os.scandir(folder) if f.is_dir() ];
        if len(content) > 0:
            return content;
        else:
            return [folder];
   
    content = [ f for f in os.scandir(folder) if f.is_dir() ];
    if len(content) > 0:
        for element in content:
            subfolders += GetSubFolders(element.path, level);
    else:
        return [folder];

    return subfolders;

def GetSubFoldersWithFiles_Robocopy(folder: str, level: int) -> list:
    folderForFiles = [];
    level -= 1;
    fileCheckedOnce = False;
    if level == 0:
        for content in os.scandir(folder):
            if content.is_file():
                return [folder];
        return [];
   
    for content in os.scandir(folder):
        if (not fileCheckedOnce) and content.is_file():
            folderForFiles += [folder];
            fileCheckedOnce = True;
        elif content.is_dir():
            folderForFiles += GetSubFoldersWithFiles_Robocopy(content.path, level);

    return folderForFiles;

def GetFolderFiles(folder: str) -> list:
    return [ f.path for f in os.scandir(folder) if f.is_file() ];

def HasFiles(folder: str) -> bool:
    files = os.listdir(folder);
    return len(files) > 0;
   
def GetRobocopyCommand(source: str, elaboration: int = 8, operation:int = 0, onlyFiles=False, customFolder: str = '', checkIfExists: list = [], CalculateDestinationFolder: callable = None) -> list:
    if CalculateDestinationFolder == None:
        return None;
    destination = lambda:CalculateDestinationFolder(source);
    destinationLog = destination.split("/");
    destinationLog = destinationLog[-1];

    logPath = f"{customFolder}{destinationLog.replace(":", "").replace("/", "_") + ("_Files" if onlyFiles else "") + ".log"}";
    i = 0;
    while logPath in checkIfExists:
        i+=1;
        logPath = f"{customFolder}{destinationLog.replace(":", "").replace("/", "_").replace(" ", "_") + ("_Files" if onlyFiles else "") + "_" + str(i) + ".log"}";
    checkIfExists.append(logPath);

    if os.path.isfile(source):
        source = source.split("/");
        if source[-1] == '':
            source = source[:-1];
        fileName = source[-1];
        source = source[:-1];
        source = "/".join(source);

        destination = destination.split("/");
        if destination[-1] == '':
            destination = destination[:-1];
        destination = destination[:-1];
        destination = "/".join(destination);

        command = [
            "Robocopy",
            source,
            destination,
            fileName,
            f"/LOG:{logPath}"
        ];
    else:
        command = [
            "Robocopy",
            source,
            destination,
            f"/LOG:{logPath}"
        ];

        if elaboration in [32, 64, 128]:
            command.append(f"/MT:{elaboration}");
        if not onlyFiles:
            command.append("/E");
        if operation == 1:
            command.append("/MOVE");

    return [command, checkIfExists];

def GetHighestPaths(paths: list) -> list:
    paths.sort();
    highest_paths = [paths[0]];

    for path in paths[1:]:
        if not path.startswith(highest_paths[-1]):
            highest_paths.append(path);

    return highest_paths;

def CreateFolder(folderPath: str):
    pathSplitted = CleanPath(folderPath, "/").split("/");
    if "." in pathSplitted[-1]:
        folderPath = "/".join(pathSplitted[:-1]);
    if not (os.path.exists(folderPath)):
        os.makedirs(folderPath);

def FolderHasContent(folder: str) -> bool:
    if os.path.exists(folder) and os.listdir(folder):
        return True;
    else:
        return False;

def FolderDeleteContents(folder: str) -> list:
    bytes(folder, "utf-8").decode("unicode_escape");
    deleted = [];
    fails = False;
    for filename in os.listdir(folder):
        try:
            file_path = os.path.join(folder, filename);
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path);
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path);
            deleted.append(f"Success: {file_path}");
        except Exception as e:
            deleted.append(f"Fail: {e}; Path: {file_path}");
            fails = True;
    return [fails, deleted];