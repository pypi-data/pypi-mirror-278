import pytest;
from AlmaxUtils.Generic import PrintBytes,CheckStringInFile;

def test_PrintBytes():
    assert PrintBytes(500) == "500 B"
    assert PrintBytes(2048) == "2.0 KB"
    assert PrintBytes(2_097_152) == "2.0 MB"
    assert PrintBytes(2_147_483_648) == "2.0 GB"
    assert PrintBytes(2_199_023_255_552) == "2.0 TB"

@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "temp_file.txt";
    with open(file_path, 'w') as f:
        f.write("Hello, this is a test file.\n")
        f.write("It contains multiple lines.\n")
        f.write("This is the target line.\n")
    return file_path;

def test_CheckStringInFile(temp_file):
    assert CheckStringInFile(temp_file, "target line") == True
    assert CheckStringInFile(temp_file, "not in file") == False
    assert CheckStringInFile("nonexistent_file.txt", "target line") == False