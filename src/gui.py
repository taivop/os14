from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from data_defs import *
from cpu_t_allocation_algorithms import *


def runAlgorithm(algorithm, canvas, patternString):
    processes = testPatternToArray(patternString)

    occupations = None
    if algorithm == "FCFS":
        occupations = allocate_FCFS(processes)
    elif algorithm == "SJF":
        occupations = allocate_SJF(processes)
    elif algorithm == "RR":
        occupations = allocate_RR(processes)
    elif algorithm == "MLQ":
        occupations = allocate_MLQ(processes)
    else:
        raise Exception("Trying to run an algorithm that doesn't exist: " + str(algorithm))

    waitTime = avgWaitTime(processes, occupations)
    print("average wait time: {:2f}".format(waitTime))
    showProcessesAndAvgWaitTime(processes, waitTime)
    drawProcessorOccupations(occupations, canvas)

def runCpuTimeAllocationApp():
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
    processesText.insert(INSERT, "\n" + "Keskmine ooteaeg: {:.2f}".format(waitTime) + "\n")

# joonistab tahvlile protsesse kujutavad ristkülikud numbrite ja protsesside nimedega
def drawProcessorOccupations(occupations, canvas):
    clearCanvas(canvas)

    box_left_x = 20
    kaugus = 0

    currentFill = True

    for i in range(len(occupations)):
        p_id = occupations[i][0]
        p_start_time = occupations[i][1]
        p_end_time = occupations[i][2]
        p_duration = p_end_time - p_start_time

        fill1 = "light cyan"
        fill2 = "pale turquoise"

        # swap colors for consecutive blocks
        if currentFill:
            fillColor = fill1
        else:
            fillColor = fill2
        currentFill = not currentFill

        rect_duration = canvas.create_rectangle(box_left_x, 60, box_left_x + p_duration * 16,100, fill=fillColor)

        rect_duration_center = box_left_x + p_duration * 8
        text_pid = canvas.create_text(rect_duration_center, 80, text=p_id, font="Arial 13 bold")

        m = canvas.create_text(box_left_x, 110, text=str(kaugus))
        kaugus += p_duration
        box_left_x += p_duration*16
    m = canvas.create_text(box_left_x, 110, text=str(kaugus))

def testingGui():
    window = Tk()
    window.title("Protsessoriaja planeerimise algoritmid")
    window.resizable(False, False)
    window.geometry("800x400")

    chosenPattern = IntVar()
    chosenPattern.set(0)
    Radiobutton(window, text="Muster 1:", variable=chosenPattern, value=0).place(x=10,y=40)
    Radiobutton(window, text="Muster 2:", variable=chosenPattern, value=1).place(x=10,y=70)
    Radiobutton(window, text="Muster 3:", variable=chosenPattern, value=2).place(x=10,y=100)
    Radiobutton(window, text="Oma muster:", variable=chosenPattern, value=3).place(x=10,y=130)

    silt_vali = ttk.Label(window, text="Vali või sisesta muster kujul \"saabus1,kestus1;saabus2,kestus2;...\"")
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

    tahvel = Canvas(window, width=800, height=180, background="white")
    tahvel.place(x=0, y=220)

    getPattern = lambda n: preDefPattern(n) if n in [0,1,2] else patternFromUserEntry.get()

    button_FCFS = ttk.Button(window, text="FCFS", command = lambda: runAlgorithm("FCFS", tahvel, getPattern(chosenPattern.get())))
    button_FCFS.place(x=10, y=190,height=25, width=80)

    button_SJF = ttk.Button(window, text="SJF", command = lambda: runAlgorithm("SJF", tahvel, getPattern(chosenPattern.get())))
    button_SJF.place(x=100, y=190,height=25, width=80)

    button_SRTF = ttk.Button(window, text="RR", command = lambda: runAlgorithm("RR", tahvel, getPattern(chosenPattern.get())))
    button_SRTF.place(x=190, y=190,height=25, width=80)

    button_RR = ttk.Button(window, text="MLQ", command = lambda: runAlgorithm("MLQ", tahvel, getPattern(chosenPattern.get())))
    button_RR.place(x=280, y=190,height=25, width=80)

    button_clear = ttk.Button(window, text="Puhasta väljund", command = lambda: clearCanvas(tahvel))
    button_clear.place(x=500, y=190,height=25, width=130)

    global processesText
    processesText = Text(window, width=40, height=9)
    processesText.place(x=450, y=30)

    window.mainloop()




runCpuTimeAllocationApp()