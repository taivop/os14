from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from malu.data_defs import *
from malu.memory_algorithms import *

def runAlgorithm(algorithm, canvas, patternString):
    try:
        requests = testPatternToArray(patternString)
    except:
        messagebox.showerror(title="Viga sisendis", message="Vigane kasutaja sisestatud muster!")

    states = None
    if algorithm == "FF":
        states = allocate_FF(requests)
    elif algorithm == "BF":
        states = allocate_BF(requests)
    elif algorithm == "WF":
        states = allocate_WF(requests)
    elif algorithm == "RF":
        states = allocate_RF(requests)
    else:
        raise Exception("Trying to run an algorithm that doesn't exist: " + str(algorithm))

    #waitTime = avgWaitTime(requests, occupations)
    #print("average wait time: {:2f}".format(waitTime))
    #showProcessesAndAvgWaitTime(requests, waitTime)
    drawMemoryStates(states, canvas)

def runMemoryAllocationApp():
    testingGui()

def clearCanvas(canvas):
    canvas.delete('all')

# show parsed processes input
def showProcessesAndAvgWaitTime(processes, waitTime):
    processesText.delete(1.0, END)
    processesText.insert(INSERT, "Protsessid:" + "\n")
    for p in processes:
        s = "id {:2}, saabub t={:2}, kestus {:2}".format(p[0], p[1], p[2])
        processesText.insert(INSERT, s + "\n")
    processesText.insert(INSERT, "Keskmine ooteaeg: {:.2f}".format(waitTime) + "\n")

# joonistab tahvlile protsesse kujutavad ristkülikud numbrite ja protsesside nimedega
def drawMemoryStates(states, canvas):
    clearCanvas(canvas)

    kaugus = 0

    fill1 = "orange red"
    fill2 = "orange"
    fillEmpty = "snow3"

    y_offset = -30
    for s in range(0,len(states)):

        currentFill = True

        state = states[s]
        print(state)

        rect_allmemory = canvas.create_rectangle(20, 60 + y_offset, 20 + MEMORY_SIZE * 16,100 + y_offset, fill=fillEmpty, outline=fillEmpty)
        m = canvas.create_text(20, 110 + y_offset, text=str(0))
        m = canvas.create_text(20 + MEMORY_SIZE * 16, 110 + y_offset, text=str(50))

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

            rect_duration = canvas.create_rectangle(box_left_x, 60 + y_offset, box_right_x, 100 + y_offset, fill=fillColor)

            # box label
            rect_duration_center = (box_left_x + box_right_x) / 2
            text_bid = canvas.create_text(rect_duration_center, 80 + y_offset, text=b_id, font="Arial 13 bold")

            # index labels
            if b_start_index != 0:
                m = canvas.create_text(box_left_x, 110 + y_offset, text=str(b_start_index))
            m = canvas.create_text(box_right_x, 110 + y_offset, text=str(b_end_index))


        y_offset += 100

def testingGui():
    window = Tk()
    window.title("Mäluhalduse planeerimise algoritmid")
    window.resizable(False, False)
    window.geometry("1000x750")

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

    tahvel = Canvas(window, width=1000, height=180+350, background="white")
    tahvel.place(x=0, y=220)

    getPattern = lambda n: preDefPattern(n) if n in [0,1,2] else patternFromUserEntry.get()

    button_FCFS = ttk.Button(window, text="FF", command = lambda: runAlgorithm("FF", tahvel, getPattern(chosenPattern.get())))
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