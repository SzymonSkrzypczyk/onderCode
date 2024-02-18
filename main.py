from pathlib import Path
from src.OnderCodeCompiler import Interpreter

TEST_FILE_PATH = Path(__file__).parent / "test_scripts" / "test_file.oc"
TEST_SIMPLE_PATH = Path(__file__).parent / "test_scripts" / "test_2.oc"
TEST_NWW_PATH = Path(__file__).parent / "test_scripts" / "test_nww.oc"
TEMP_NWP_PATH = Path(__file__).parent / "test_scripts" / "test_nwp.oc"


if __name__ == "__main__":
    c = Interpreter(TEMP_NWP_PATH, debug=False, a=6, b=4)
    print(c.variables)
    c()
    # print(c.steps)
    print(c.variables)
