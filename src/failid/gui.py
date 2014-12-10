from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from failid.data_defs import *
from failid.file_algorithms import *

def runAlgorithm(canvas, patternString):
    try:
        requests = testPatternToArray(patternString)
        requests_copy = requests[:]
    except:
        messagebox.showerror(title="Viga sisendis", message="Vigane kasutaja sisestatud muster!")
        return

    try:
        states = allocateFiles(requests_copy)
        drawDiskStates(requests, states, canvas)
    except NoFreeSpaceError as err:
        states = err.args[1]
        drawDiskStates(requests, states, canvas)
        messagebox.showerror(title="Viga sisendis", message="Fail {} ei mahu failisüsteemi (kogusuurus on {} ühikut)!".format(err.args[0], DISK_SIZE))

    (p_f, p_s) = getFragmentedPercs(states[-1])

    showFragPerc(100 * p_f, 100 * p_s)

def showFragPerc(perc_files_frag, perc_space_frag):
    infoBoxText.delete(1.0, END)
    infoBoxText.insert(INSERT, "{:.1f}% failidest fragmenteerunud.".format(perc_files_frag) + "\n")
    infoBoxText.insert(INSERT, "{:.1f}% ruumist fragmenteerunud.".format(perc_space_frag) + "\n")


def getFillColor(id_char):
    id = letterToId(id_char) - 1
    colors_base = ["mint cream", "light sky blue", "turquoise", "aquamarine", "pale green", "dark khaki", "orange", "firebrick1", "yellow2", "DeepPink2"]
    colors = colors_base * 10
    return colors[id]


def runMemoryAllocationApp():
    testingGui()

def clearCanvas(canvas):
    canvas.delete('all')

def drawDiskStates(requests, states, canvas):
    clearCanvas(canvas)

    lineHeight = 20

    fillEmpty = "snow3"

    y_offset = -30
    for s in range(0,len(states)):

        currentFill = True

        state = states[s]

        rect_allmemory = canvas.create_rectangle(20, 60 + y_offset, 20 + DISK_SIZE * 16,60 + lineHeight + y_offset, fill=fillEmpty, outline=fillEmpty)
        m = canvas.create_text(20, 60 + lineHeight * 1.30 + y_offset, text=str(0))
        m = canvas.create_text(20 + DISK_SIZE * 16, 60 + lineHeight * 1.30 + y_offset, text=str(50))

        for i in range(len(state)):
            b_id = state[i][0]
            b_start_index = state[i][1]
            b_end_index = b_start_index + state[i][2]
            b_size = state[i][2]

            box_left_x = 20 + b_start_index * 16
            box_right_x = box_left_x + b_size * 16

            # swap colors for consecutive blocks
            fillColor = getFillColor(b_id)

            rect_duration = canvas.create_rectangle(box_left_x, 60 + y_offset, box_right_x, 60 + lineHeight + y_offset, fill=fillColor)

            # box label
            rect_duration_center = (box_left_x + box_right_x) / 2
            text_bid = canvas.create_text(rect_duration_center, 60 + lineHeight / 2 + y_offset, text=b_id, font="Arial 13 bold")

            # index labels
            if b_start_index != 0:
                m = canvas.create_text(box_left_x, 60 + lineHeight * 1.30 + y_offset, text=str(b_start_index))
            m = canvas.create_text(box_right_x, 60 + lineHeight * 1.30 + y_offset, text=str(b_end_index))


        y_offset += lineHeight * 1.8




def testingGui():
    window = Tk()
    window.title("Mäluhalduse planeerimise algoritmid")
    window.resizable(False, False)
    window.geometry("1000x650")

    chosenPattern = IntVar()
    chosenPattern.set(0)
    Radiobutton(window, text="Muster 1:", variable=chosenPattern, value=0).place(x=10,y=40)
    Radiobutton(window, text="Muster 2:", variable=chosenPattern, value=1).place(x=10,y=70)
    Radiobutton(window, text="Muster 3:", variable=chosenPattern, value=2).place(x=10,y=100)
    Radiobutton(window, text="Oma muster:", variable=chosenPattern, value=3).place(x=10,y=130)

    silt_vali = ttk.Label(window, text="Vali või sisesta muster kujul \"fail1,suurus1;...\"")
    silt_vali.place(x=10, y=10)

    silt1 = ttk.Label(window, text=preDefPattern(0))
    silt1.place(x=120, y=40)

    silt2 = ttk.Label(window, text=preDefPattern(1))
    silt2.place(x=120, y=70)

    silt3 = ttk.Label(window, text=preDefPattern(2))
    silt3.place(x=120, y=100)

    silt_run = ttk.Label(window, text="Algoritmi käivitamiseks vajuta nupule:")
    silt_run.place(x=10, y=160)

    silt_tahvel = ttk.Label(window, text="Info:")
    silt_tahvel.place(x=450, y=10)

    patternFromUserEntry = ttk.Entry(window)
    patternFromUserEntry.place(x=120, y=130, height=25, width=240)

    tahvel = Canvas(window, width=1000, height=180+250, background="white")
    tahvel.place(x=0, y=220)


    getPattern = lambda n: preDefPattern(n) if n in [0,1,2] else patternFromUserEntry.get()

    button_run = ttk.Button(window, text="Käivita", command = lambda: runAlgorithm(tahvel, getPattern(chosenPattern.get())))
    button_run.place(x=10, y=190,height=25, width=60)

    button_clear = ttk.Button(window, text="Puhasta väljund", command = lambda: clearCanvas(tahvel))
    button_clear.place(x=500, y=190,height=25, width=130)

    global infoBoxText
    try:
        infoBoxText = Text(window, width=35, height=9, font="Courier 11")   # if possible, use Courier font
    except:
        infoBoxText = Text(window, width=35, height=9)                      # if not, use default font
    infoBoxText.place(x=450, y=30)

    window.mainloop()




runMemoryAllocationApp()