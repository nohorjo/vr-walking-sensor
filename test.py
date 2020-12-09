import subprocess

import display

date = subprocess.check_output('date', shell=True).decode("utf-8")

display.text(date, 0)
display.text('1234567890', 1)
display.text('1234567890       ', 2)
display.text('       1234567890', 2)
display.show()
