import atexit
import os.path
import tkinter

from tkinter import *
from tkinter import filedialog

version_num = "1.0"
# Description:
# - Get Data: get data from excel file
# - Manual read: manually read from Arduino
# - Open Port: enter port# into entry box, then press open port to establish serial connection
# - Browse for .xls: browse computer for .xls file to load, use Get Data afterwards to update data tables
# - Write First 32 Bytes: send the first 32 bytes to the Arduino
# - Write Second 32 Bytes: send the second 32 bytes to the Arduino
# - Ignore Control: sets control byte to 0 after every read (temporary)

stored_data_array = [None] * 33  # for storing data from excel/read temporarily
A = 1
B = 0
file_input = "test"


def send_data(bytes):  # Define send data function
    i = 0  # array index variable
    print("Sending data, CS =", end=" ")
    print(bytes[33])

    while i < len(bytes):  # While loop that sends the data
        i = i + 1
    print("Complete")


def manual_read():  # Read data function for Arduino
    for i in range(33):  # clear internal data storage array
        stored_data_array[i] = 0
    print("Stored array cleared, preparing for read...")

    for i in range(33):
        try:
            data = ser.readline().decode().strip()
            # print(data, end=", ")
            stored_data_array[i] = int(data, base=10)

            ################################################ DEBUG
            # print(stored_data_array[i], end=", ")
            # print("num:" + str(i), end=", ")
            print(data)

        except:
            print("Num: " + str(i) + " failed")

    print("Reading Finished")


# Functions for saving configurations automatically on termination
def save_variables_config():  # save variables into config
    global A, B
    try:
        with open("config.txt", "w") as t:
            t.write(A)  # write variable A onto config
            t.write("\n")
            t.write(B)  # write variable B onto config
            t.write("\n")
    except ValueError:
        return


def read_variables_config():  # read saved config and load variables
    global A, B
    try:
        with open("config.txt", "r") as t:
            A = t.readline().rstrip('\n')  # read through the config to get variable A, then strip
            B = t.read().rstrip('\n')  # read through config for variable B, then strip
    except ValueError:
        return


read_variables_config()  # read config on startup
atexit.register(save_variables_config)  # save config when program terminates


def combined_send1(BYTES):  # SEND FIRST 32
    print("[", end="")  # Print data in hex
    for i in range(len(BYTES)):
        if i != len(BYTES) - 1:
            print(hex(int(BYTES[i])), end=", ")
        else:
            print(hex(int(BYTES[i])), end="")
    print("]")
    send_data(BYTES)
    root.update()


def combined_send2(BYTES2):  # SEND SECOND 32
    print("[", end="")  # Print data in hex
    for i in range(len(BYTES2)):
        if i != len(BYTES2) - 1:
            print(hex(int(BYTES2[i])), end=", ")
        else:
            print(hex(int(BYTES2[i])), end="")
    print("]")
    send_data(BYTES2)
    root.update()


def single_send1(register, value,
                 cs):  # Function to send a single Byte to Arduino, single_byte = [index, int_byte, chip_select]
    # print("Sending one byte of value " + str(value) + " to " + str(register))
    print("Sending one byte to register" + str(register) + " with a value of " + str(value) + " in set " + str(cs))
    location_byte = int(register)
    print("Complete")


single_read_data = [0, 0]


def single_read(register,
                cs):  # Function to send a single Byte to Arduino, single_byte = [index, int_byte, chip_select]
    print("Reading one byte from register " + str(register))
    location_byte = int(register)

    # for i in range(33): # clear internal data storage array
    #     stored_data_array[i] = 2
    # print("Stored array cleared, preparing for read...")

    global single_read_data
    for i in range(2):
        try:
            data = ser.readline().decode().strip()
            single_read_data[i] = int(data)
            print(data)

        except:
            print("Num: " + str(i) + " failed")

    print("Complete")


# GUI CODE
root = Tk()
root.title("Arduino SPI Data Controller V" + str(version_num))


def gui():
    reg_label = []  # Labels for registers
    top_labels = []  # Labels for the top of each column
    bit_label = []
    bits = [0, 0, 0, 0, 0, 0, 0, 0]  # temporary storage for bits, only for label creation
    bytes = []  # stores all the bytes to be sent

    k = 0

    file_label = Label(root, text=os.path.basename("INSERT TITLE1"))  # temp
    file_label.grid(row=1, column=0, sticky=EW, padx=5, columnspan=1)
    file_label = Label(root, text=os.path.basename("INSERT TITLE2"))
    file_label.grid(row=1, column=1, sticky=EW, padx=5, columnspan=1)

    # Buttons and Entry Boxes

    main_button_frame = Frame(root)
    main_button_frame.grid(row=2, column=0, sticky=NSEW, columnspan=2)
    # button 1
    button1 = Button(main_button_frame, text="Button 1", command=lambda: test_config(0), state=ACTIVE)
    button1.grid(row=1, column=0, columnspan=1, sticky=EW, padx=5)  # set location on GUI

    # button 2
    button2 = Button(main_button_frame, text="Button 2", command=lambda: test_config(0), state=ACTIVE)
    button2.grid(row=2, column=0, columnspan=1, sticky=EW, padx=5)

    button3 = Button(main_button_frame, text="Button 3", command=lambda: test_config(0))
    button3.grid(row=3, column=0, sticky=EW, padx=5)

    # frame + buttons
    small_frame = Frame(main_button_frame)
    small_frame.grid(row=4, column=0, sticky=NSEW, columnspan=1)
    read_data_debug_button1 = Button(small_frame, text="frame b1", command=lambda: test_config(0),
                                     state=DISABLED, justify='center')  # read_data_debug())
    read_data_debug_button1.grid(row=0, column=0, sticky=NSEW, padx=5)
    read_data_debug_button2 = Button(small_frame, text="frame b2", command=lambda: test_config(0),
                                     state=DISABLED, justify='center')  # read_data_debug())
    read_data_debug_button2.grid(row=0, column=1, sticky=NSEW, padx=5)
    # Modify Columns and Rows property
    for col in range(2):
        small_frame.columnconfigure(col, weight=1)
    for row in range(1):
        small_frame.rowconfigure(row, weight=1)

    # entry box
    entry_text = tkinter.StringVar()
    entry_text.set("Enter Text Here")
    entry_port_box = Entry(main_button_frame, text="Enter Port Number", justify='center', textvariable=entry_text)
    entry_port_box.config(width=10)
    entry_port_box.grid(row=5, column=0, sticky=EW, padx=5, columnspan=1)

    # file input
    file_select_button = Button(main_button_frame, text="Browse for file", command=lambda: select_file(), justify='center')
    file_select_button.grid(row=1, column=1, sticky=EW, padx=5)
    file_label = Label(main_button_frame, text=os.path.basename("File Name"), justify='center', anchor=W)
    file_label.grid(row=2, column=1, sticky=EW, padx=5, columnspan=1)

    # check button
    ignore_con_var = IntVar()  # Var used to set whether the program should read right after sending data
    ignore_con_chk = Checkbutton(main_button_frame, text="Ignore Control", variable=ignore_con_var, onvalue=1, offvalue=0)
    ignore_con_chk.grid(row=3, column=1, columnspan=1, sticky=EW)

    # validating input
    validate_button = Button(main_button_frame, text="Validate Test", command=lambda: validate(0), state=DISABLED)
    validate_button.grid(column=1, row=4, sticky=EW, padx=5, columnspan=1)

    # Validate
    def validate(control):
        if control == 0:  # set single byte
            if 0 <= int(entry_port_box.get()) < 32:
                single_send1(1)
            else:
                print("Invalid arguments, register must be < 32, value must be < 256, and CS must be either 0 or 1")

    # Create labels on the top of the GUI
    top_labels.append(Label(root, text="C0"))
    top_labels.append(Label(root, text="C1"))
    top_labels.append(Label(root, text="C2"))
    top_labels.append(Label(root, text="C3"))
    top_labels.append(Label(root, text="C4"))
    top_labels.append(Label(root, text="C5"))
    for i in range(len(top_labels)):  # Generate category labels
        top_labels[i].grid(row=0, column=i)

    # Row/Column properties

    # Set column and row padding
    for i in range(8):
        root.grid_columnconfigure(i, pad=2)
    for i in range(33):
        root.grid_rowconfigure(i, pad=0.5)

    # Modify Columns and Rows
    for col in range(6):
        root.columnconfigure(col, weight=1)  # set weight
        # root.grid_columnconfigure(0, minsize=200)  # set column size
    for row in range(36):
        root.rowconfigure(row, weight=1)

    # FUNCTIONS

    def test_config(input):  # Open the com port from the entry box
        global A
        global B
        save_variables_config()

    def select_file():  # Function for loading file
        global file_input
        previous_file_input = ""
        try:
            previous_file_input = file_input
            file_input = tkinter.filedialog.askopenfilename(initialdir="C:/", title="Select a file", filetypes=[("text", ".txt")])
            if len(file_input) == 0:  # No file selected
                file_input = previous_file_input
            else:  # File selected
                print("File " + file_input + " selected")
            file_label.config(text=os.path.basename(file_input))  # update text
        except FileExistsError:
            print("Failed to open file")

# END OF GUI

################################### END OF CODE
gui()
root.mainloop()
