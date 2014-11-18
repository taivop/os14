from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from ketas.data_defs import *
from ketas.disk_algorithms import *


def runAlgorithm(algorithm, canvas, patternString):
    try:
        requests = testPatternToArray(patternString)
    except:
        messagebox.showerror(title="Viga sisendis", message="Vigane kasutaja sisestatud muster! Kontrolli, et mustris pole ükski indeks suurem kui {0}.".format(MAX_INDEX))
        return
    states = None

    if algorithm == "FCFS":
        states = run_FCFS(requests)
    drawDiskStates(requests, states, canvas)

def runMemoryAllocationApp():
    testingGui()

def clearCanvas(canvas):
    canvas.delete('all')

def drawDiskStates(requests, states, canvas):
    clearCanvas(canvas)

    diskBoxLabels = [0, 1, 10, 20, 30, 40]

    # Draw disk boxes
    x_offset = 20
    y_offset = 20

    disk_width = 800
    box_size = disk_width / MAX_INDEX

    for i in range(0, MAX_INDEX):
        boxFill = "white"
        if i in requests:
            boxFill = "red"

        # draw box
        x_left = x_offset + i * box_size
        x_right = x_offset + (i+1) * box_size
        canvas.create_rectangle(x_left, y_offset, x_right, y_offset + box_size, fill=boxFill, outline="black")

        if i in diskBoxLabels:
            # draw label
            canvas.create_text(x_left, y_offset + box_size * 1.5, text=str(i))

    #draw max label
    canvas.create_text(x_offset + MAX_INDEX * box_size, y_offset + box_size * 1.5, text=str(MAX_INDEX))






# joonistab tahvlile protsesse kujutavad ristkülikud numbrite ja protsesside nimedega
def drawMemoryStates(states, canvas):
    clearCanvas(canvas)

    lineHeight = 20

    fill1 = "orange red"
    fill2 = "orange"
    fillEmpty = "snow3"

    y_offset = -30
    for s in range(0,len(states)):

        currentFill = True

        state = states[s]

        rect_allmemory = canvas.create_rectangle(20, 60 + y_offset, 20 + MEMORY_SIZE * 16,60 + lineHeight + y_offset, fill=fillEmpty, outline=fillEmpty)
        m = canvas.create_text(20, 60 + lineHeight * 1.30 + y_offset, text=str(0))
        m = canvas.create_text(20 + MEMORY_SIZE * 16, 60 + lineHeight * 1.30 + y_offset, text=str(50))

        for i in range(len(state)):
            b_id = state[i][0]
            b_start_index = state[i][2]
            b_end_index = b_start_index + state[i][3]
            b_size = state[i][3]

            box_left_x = 20 + b_start_index * 16
            box_right_x = box_left_x + b_size * 16

            # swap colors for consecutive blocks
            if currentFill:
                fillColor = fill1
            else:
                fillColor = fill2
            currentFill = not currentFill

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

    silt_vali = ttk.Label(window, text="Vali või sisesta muster kujul \"maht1,eluiga1;...\"")
    silt_vali.place(x=10, y=10)

    silt1 = ttk.Label(window, text=preDefPattern(0))
    silt1.place(x=120, y=40)

    silt2 = ttk.Label(window, text=preDefPattern(1))
    silt2.place(x=120, y=70)

    silt3 = ttk.Label(window, text=preDefPattern(2))
    silt3.place(x=120, y=100)

    silt_run = ttk.Label(window, text="Algoritmi käivitamiseks vajuta vastavale nupule")
    silt_run.place(x=10, y=160)

    silt_tahvel = ttk.Label(window, text="Info:")
    silt_tahvel.place(x=450, y=10)

    patternFromUserEntry = ttk.Entry(window)
    patternFromUserEntry.place(x=120, y=130, height=25, width=240)

    tahvel = Canvas(window, width=1000, height=180+250, background="white")
    tahvel.place(x=0, y=220)

    getPattern = lambda n: preDefPattern(n) if n in [0,1,2] else patternFromUserEntry.get()

    button_FCFS = ttk.Button(window, text="FCFS", command = lambda: runAlgorithm("FCFS", tahvel, getPattern(chosenPattern.get())))
    button_FCFS.place(x=10, y=190,height=25, width=80)

    button_SJF = ttk.Button(window, text="BF", command = lambda: runAlgorithm("BF", tahvel, getPattern(chosenPattern.get())))
    button_SJF.place(x=100, y=190,height=25, width=80)

    button_SRTF = ttk.Button(window, text="WF", command = lambda: runAlgorithm("WF", tahvel, getPattern(chosenPattern.get())))
    button_SRTF.place(x=190, y=190,height=25, width=80)

    button_RR = ttk.Button(window, text="RF", command = lambda: runAlgorithm("RF", tahvel, getPattern(chosenPattern.get())))
    button_RR.place(x=280, y=190,height=25, width=80)

    button_clear = ttk.Button(window, text="Puhasta väljund", command = lambda: clearCanvas(tahvel))
    button_clear.place(x=500, y=190,height=25, width=130)

    global processesText
    try:
        processesText = Text(window, width=35, height=9, font="Courier 11")   # if possible, use Courier font
    except:
        processesText = Text(window, width=35, height=9)                      # if not, use default font
    processesText.place(x=450, y=30)

    window.mainloop()




runMemoryAllocationApp()