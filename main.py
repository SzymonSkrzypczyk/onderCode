from pathlib import Path
from src.OnderCodeCompiler import Interpreter

TEST_FILE_PATH = Path(__file__).parent / "test_file.oc"
TEST_SIMPLE_PATH = Path(__file__).parent / "test_2.oc"


if __name__ == "__main__":
    c = Interpreter(TEST_FILE_PATH, x=7, y=2)
    print(c.variables)
    c()
    print(c.variables)
