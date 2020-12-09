import display
import button

def button_callback1():
    display.text('1 pressed', 0)
    display.show()

def button_callback2():
    display.text('2 pressed', 0)
    display.show()

def button_callback3():
    display.text('3 pressed', 0)
    display.show()

button.create(17, button_callback1)
button.create(18, button_callback2)
button.create(27, button_callback3)

input("Press enter to quit\n\n")
display.clear()
