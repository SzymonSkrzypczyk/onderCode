from pathlib import Path
from src.OnderCodeCompiler import Interpreter

TEST_FILE_PATH = Path(__file__).parent / "test_scripts" / "test_file.oc"
TEST_SIMPLE_PATH = Path(__file__).parent / "test_scripts" / "test_2.oc"
TEST_NWW_PATH = Path(__file__).parent / "test_scripts" / "test_nww.oc"
TEMP_NWP_PATH = Path(__file__).parent / "test_scripts" / "test_nwp.oc"

if __name__ == "__main__":
    c = Interpreter(TEMP_NWP_PATH, debug=False, a=6, b=4,
                    c=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    c()
    print(c.variables)
    c.variable_assign("c_5 <- c_a")
    print(c.variables)
