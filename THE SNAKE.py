import tkinter as tk # python has it; Used to build front end windows
import random # To generate random numbers points to the position of apple
import time 



'''
Note:
The project used audio render package and may require to run on the environment outside ED.
All the package used is python built-in function.

'''

# Each single grid = 20 pixels
grid = 20 

# Map width and height = 30 grids. It's a 30 x 30 map
map_width = 30*grid
map_height = 30*grid 

# Set the margin between grids
margin = 5

# Initialise a snake which contains a set of vectors to display its length
snake = []

# Initialise a list to store the position vector of apple
apple = []

# Initially we defined snake move towards right
move = [1,0] 

# Initialise score 
score = 0

# Initialise time used
t = []







# Initialise the snake and the map
def init():
    # The starting position of the snake
    init_x = 5
    init_y = 5
    apple_x,apple_y = setapple()
    apple.append([apple_x,apple_y])
    for i in range(30):
        for j in range(30):
            canvas.create_rectangle(i*grid,j*grid,(i+1)*grid-margin,(j+1)*grid-margin, fill = 'grey')
            if (i == 0 or i == 29 or j == 0 or j == 29):
                canvas.create_rectangle(i*grid,j*grid,(i+1)*grid-margin,(j+1)*grid-margin, fill = 'black')
            if (i == init_x and j == init_y) or (i == init_x + 1 and j == init_y + 1):
                canvas.create_rectangle(i*grid,j*grid,(i+1)*grid-margin,(j+1)*grid-margin, fill = 'white')
                snake.append([i,j])
            if (i == apple_x and j == apple_y):
                canvas.create_rectangle(i*grid,j*grid,(i+1)*grid-margin,(j+1)*grid-margin, fill = 'red')
    t.append(time.time())
    update()





def setapple():
    # randomly form an apple, starting with 1 and 28 to make sure apple is not placed in the wall
    apple_x = random.randint(1,28)
    apple_y = random.randint(1,28)
    # if apple's position vector is in the snake, then a new position must be formed
    while [apple_x,apple_y] in snake:
        apple_x = random.randint(1,28)
        apple_y = random.randint(1,28)
    return [apple_x,apple_y]



def movement():
    # The movement of snake can be thought as removing the 'tail' of the snake and add a position vector with the 'head' of snake
    del(snake[0]) 
    # assume head = [x,y], the following applies to [x+move_x,y+move_y]
    snake.append([snake[-1][0] + move[0], snake[-1][1] + move[1]])


# This function is used to refresh the window so that the operation could be seen correctly
def update():
    window.update()
    if reached():
        eat()
    # To update the snake after movement, repaint the original tail position to grey, update the positon and fill the head position as white
    canvas.create_rectangle(snake[0][0]*grid,snake[0][1]*grid,(snake[0][0]+1)*grid - margin,(snake[0][1]+1)*grid - margin, fill = 'grey')
    movement()
    canvas.create_rectangle((snake[-1][0])*grid,(snake[-1][1])*grid,(snake[-1][0]+1)*grid - margin,(snake[-1][1]+1)*grid - margin, fill = 'white')
    if lose():
        t.append(time.time())
        result = f'Your final score is {score} in total of {t} seconds.'
        # leave 10 seconds to review the game over window
        window.after(20, window.destroy)
        return
    window.after(500,update)

# Define the function to control the movement of the snake. Bind wasd to the function.
def direction(event):
    global move
    # You cant go left while moving right, you can only move upside down while moving to the right.
    if event.keysym == 'Up' and move != [0,1]:
        move = [0, -1]
    elif event.keysym == 'Left' and move != [0,-1]:
        move = [-1, 0]
    elif event.keysym == 'Down' and move != [1,0]:
        move = [0, 1]
    elif event.keysym == 'Right' and move != [-1,0]:
        move = [1, 0]

# Define a function to check whether the snake eat apple or not
def reached():
    if snake[-1] == apple[0]:
        return True
    return False

# Define eat function, set a new apple and increase the tail by 1
def eat():
    global score
     # Update score
    score += 1

    apple[0][0], apple[0][1] = setapple()

    canvas.create_rectangle(apple[0][0]*grid,apple[0][1]*grid,(apple[0][0]+1)*grid-margin,(apple[0][1]+1)*grid-margin, fill = 'red')

    # Update the snake list
    snake.insert(0,[snake[0][0]- move[0], snake[0][1] - move[1]])


# Define function to check the game over condition
def lose():
    # The position of the snake head is:
    head_x, head_y = snake[-1][0], snake[-1][1]
    # If the head hits the body, or hits the wall, then the game is over

    # snake body can be defined as:
    snake_body = []
    for i in range(len(snake)):
        snake_body.append([snake[i][0],snake[i][1]])
    del(snake_body[-1])

    # determine whether the head hits the body:
    if [head_x,head_y] in snake_body:
        return True
    elif head_x <= 0 or head_x >= 29 or head_y <= 0 or head_y >= 29:
        return True
    else:
        return False
    
window = tk.Tk()

window.title('The Snake')

mapsize = str(map_height) + 'x' + str(map_width)

# Now use geometry function to create the map in the front end window
window.geometry(mapsize)


# Display the windows
canvas = tk.Canvas(window, height = map_height, width = map_width) # display the background
canvas.pack()
canvas.focus_set()
canvas.bind('<KeyPress-Up>',direction)
canvas.bind('<KeyPress-Left>',direction)
canvas.bind('<KeyPress-Down>',direction)
canvas.bind('<KeyPress-Right>',direction)

#
init()
#To activate the game, until quit the game function is triggered.
window.mainloop() 




