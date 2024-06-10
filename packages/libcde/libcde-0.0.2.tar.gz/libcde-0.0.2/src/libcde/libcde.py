import os
import errno

# /------------------------------------/
# / create_dt_struct(action,label,cmd) /
# /                                    /
# /  Creates a DT application struct   /
# /                                    /
# /  Arguments:                        /
# /                                    /
# /  action -> Action name, should be  /
# /  the same as label                 /
# /                                    /
# /  label -> The name that appears in /
# /  the application toolbox.          /
# /                                    /
# /  cmd -> The command to execute     /
# /------------------------------------/
def create_dt_struct(action, label, cmd):
    # Wtf.
    
    CURLY_OPEN = '{'
    CURLY_CLOSE = '}' 
    
    dt_struct = (f"ACTION {action}\n"
                 f"{CURLY_OPEN}\n"
                 f"    LABEL        {label}\n"
                 f"    TYPE         COMMAND\n"
                 f"    EXEC_STRING  {cmd}\n"
                 f"    ICON         Dtactn\n"
                 f"    WINDOW_TYPE  NO_STDIO\n"
                 f"{CURLY_CLOSE}\n")
    return dt_struct

# /----------------------------------------/
# / make_dt_local(out, action, label, cmd) /
# / Creates an application dt entry, and   /
# / saves it to a file. Should be wrapped  /
# / recursively.                           /
# /                                        /
# / Arguments:                             /
# /                                        /
# / dt_out: Output file directory          /
# /                                        /
# / The rest: Refer to create_dt_struct    /
# /                                        /
# /----------------------------------------/
def make_dt_local(dt_out, action, label, cmd):
    # Open file handle using os.open for performance.

    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY    # Create file only if it doesn't exist.

    try:
        dt_handle = os.open(dt_out, flags)
    except OSError as err:
        if err.errno == errno.EEXIST:   # Pass - file already exists.
            pass
        else:
            pass    # Log to file, probably?
    else:
        with os.fdopen(dt_handle, 'w') as dt_object:    # Convert to py file object
            dt_object.write(create_dt_struct(action, label, cmd))
