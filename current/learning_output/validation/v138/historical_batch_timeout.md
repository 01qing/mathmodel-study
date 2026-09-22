# Historical regression batch timeout

The first sequential wrapper for the 22 historical Core regression scripts exceeded the outer command time limit before it could write a complete summary. This timeout is recorded as **neither PASS nor FAIL**. The same 22 scripts are rerun below as individually bounded parallel processes; only explicit return code 0 counts as PASS.
