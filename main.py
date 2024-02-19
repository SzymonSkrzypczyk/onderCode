from pathlib import Path
from src.gui import OnderApp

TEST_FILE_PATH = Path(__file__).parent / "test_scripts" / "test_file.oc"
TEST_SIMPLE_PATH = Path(__file__).parent / "test_scripts" / "test_2.oc"
TEST_NWW_PATH = Path(__file__).parent / "test_scripts" / "test_nww.oc"
TEMP_NWP_PATH = Path(__file__).parent / "test_scripts" / "test_nwp.oc"
TEST_DIV_LIST = Path(__file__).parent / "test_scripts" / "test_div_list.oc"

if __name__ == "__main__":
    app = OnderApp()
    app.mainloop()
