import display

total_points = 67
current_points = 0
last_percentage = None
done = False

def update():
    global last_percentage, current_points
    current_points += 1
    if not done:
        print('Loading %d/%d' % (current_points, total_points))
        current_percentage = round((current_points * 100) / total_points)
        if last_percentage is not current_percentage:
            display.text('Loading... %d%%' % current_percentage, 0)
            display.show()
            last_percentage = current_percentage

update()

