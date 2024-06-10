from libcde import libcde

def test_create_dt_struct():
    CURLY_OPEN = '{'
    CURLY_CLOSE = '}'
    assert libcde.create_dt_struct(
            "LibCDE_Test", "LibCDE_Test_Label", "libcde-test"
            ) == (f"ACTION LibCDE_Test\n"
                  f"{CURLY_OPEN}\n"
                  f"    LABEL        LibCDE_Test_Label\n"
                  f"    TYPE         COMMAND\n"
                  f"    EXEC_STRING  libcde-test\n"
                  f"    ICON         Dtactn\n"
                  f"    WINDOW_TYPE  NO_STDIO\n"
                  f"{CURLY_CLOSE}\n")
