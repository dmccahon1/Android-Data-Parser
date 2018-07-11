import tkinter
from acquisition import adbExtract
from tkinter import ttk


def ChangeLabelText(m):
    m.config(text='You pressed the button!')

    m.config(text='You pressed the button twice!')

def main():
    'GUI for Application'
    root = tkinter.Tk()
    root.geometry("400x300")

    MyLabel = ttk.Label(root, text = 'The button has not been pressed.')
    MyLabel.pack()
    MyButton = ttk.Button(root, text = 'Press Me', command = lambda: ChangeLabelText(MyLabel))
    MyButton.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
