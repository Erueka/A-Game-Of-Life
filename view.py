from tkinter import *
import model


cell_size = 5
is_running = False
global root, grid_view, start_button, clear_button, choice


def setup():
    global root, grid_view, cell_size, start_button, clear_button, choice

    root = Tk()
    root.title('The Game of Life')

    grid_view = Canvas(root, width=model.width*cell_size,
                       height=model.height*cell_size,
                       borderwidth=0,
                       highlightthickness=0,
                       bg='white')
    grid_view.bind('<Button-1>', grid_handler)

    start_button = Button(root, text='Start', width=12)
    start_button.bind('<Button-1>', start_handler)
    clear_button = Button(root, text='Clear', width=12)
    clear_button.bind('<Button-1>', clear_handler)

    choice = StringVar(root)
    choice.set('Choose a Pattern')
    option = OptionMenu(root, choice, 'Choose a Pattern', 'glider', 'glider gun', 'random')
    option.config(width=20)
    option.bind('<Button-1>', option_handler)

    grid_view.grid(row=0, columnspan=3, padx=20, pady=20)
    start_button.grid(row=1, column=0, sticky=W, padx=20, pady=20)
    clear_button.grid(row=1, column=2, sticky=E, padx=20, pady=20)
    option.grid(row=1, column=1, padx=20, pady=20)


def start_handler(event):
    global grid_view, is_running

    if is_running:
        is_running = False
        start_button.config(text='Start')
    else:
        is_running = True
        start_button.config(text='Pause')
        update()


def clear_handler(event):
    # 预设的图案还未添加
    global grid_view, is_running

    is_running = False
    # model.grid_model.clear()
    # 如果直接清空列表update会产生index错误，要逐个置零
    for i in range(model.height):
        for j in range(model.width):
            model.grid_model[i][j] = 0

    start_button.config(text='Start')

    update()


def grid_handler(event):
    global grid_view, cell_size

    x = int(event.x / cell_size)
    y = int(event.y / cell_size)

    if model.grid_model[x][y]:
        model.grid_model[x][y] = 0
        draw_cell(x, y, 'white')
    else:
        model.grid_model[x][y] = 1
        draw_cell(x, y, 'black')


def option_handler(event):
    global is_running, start_button, choice

    is_running = False
    start_button.config(text='Start')

    option = choice.get()

    if option == 'random':
        model.randomize(model.grid_model, model.width, model.height)

    update()


def update():
    global grid_view, is_running

    grid_view.delete(ALL)

    model.next_gen()
    for i in range(model.height):
        for j in range(model.width):
            if model.grid_model[i][j] == 1:
                draw_cell(i, j, 'black')

    if is_running:
        root.after(300, update)


def draw_cell(row, col, color):
    global grid_view, cell_size

    if color == 'black':
        outline = 'gray'
    else:
        outline = 'white'

    grid_view.create_rectangle(row*cell_size,
                               col*cell_size,
                               row*cell_size+cell_size,
                               col*cell_size+cell_size,
                               fill=color, outline=outline)


if __name__ == '__main__':
    setup()
    update()
    mainloop()