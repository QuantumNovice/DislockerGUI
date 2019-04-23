#test.py
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu


class Application:
    def __init__(self, master):
        disks = 'sd'
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('dislocker.ui')
        builder.connect_callbacks(self)
        callbacks = {
            'on_click': self.on_click
            }

        builder.connect_callbacks(callbacks)
        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainFrame', master)

        def on_click(self):
            print('click')


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
