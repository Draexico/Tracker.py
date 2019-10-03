from tkinter import *
import time
import pythoncom, pyHook

def Main():
    global root
    global hit_label
    global death_label
    global total_label
    global hit_label_number
    global death_label_number
    global check_total
    global hit_label_str
    global death_label_str
    global check_total_str

    root = Tk()
    root.title("Tracker")
    root.geometry("750x300")
    root.config(bg="black")
    root.resizable(False, False)

    stopWatch = StopWatch(root)
    stopWatch.grid(row = 0, column = 0)
    left_frame = Frame(root, bg = "black", padx = 20)
    left_frame.grid(row = 1, column = 0)
    right_frame = Frame(root, bg = "black")
    right_frame.grid(row=0, column = 1, padx = 20)
    
    Start = Button(left_frame,
                   text = "Start",
                   command = stopWatch.Start,
                   width = 10,
                   height = 2)
    Start.grid(row = 0, column = 1)
    Stop = Button(left_frame,
                   text = "Stop",
                   command = stopWatch.Stop,
                   width = 10,
                   height = 2)
    Stop.grid(row = 0, column = 2)
    Reset = Button(left_frame,
                   text = "Reset",
                   command = stopWatch.Reset,
                   width = 10,
                   height = 2)
    Reset.grid(row = 0, column = 3)
    Exit = Button(left_frame,
                   text = "Exit",
                   command = stopWatch.Exit,
                   width = 10,
                   height = 2)
    Exit.grid(row = 0, column = 4)


    hit_label = Label(right_frame, text = "Hits:", font = ("Arial", 18), fg = "white", bg = "black", padx = 20, pady = 10)
    hit_label.grid(row = 4, column = 2)
    
    death_label = Label(right_frame, text = "Deaths:", font = ("Arial", 18), fg = "white", bg = "black", padx = 20, pady = 10)
    death_label.grid(row = 5, column = 2)
    
    total_label = Label(right_frame, text = "Total:", font = ("Arial", 18), fg = "white", bg = "black", padx = 20, pady = 10)
    total_label.grid(row = 6, column = 2)

    hit_label_number = StringVar()
    hit_label_number.set(0)
    hit_label_str = Label(right_frame, font = ("Arial", 18), fg = "green", bg = "black", padx = 20, pady = 10, textvariable=hit_label_number)
    hit_label_str.grid(row = 4, column = 3)

    death_label_number = StringVar()
    death_label_number.set(0)
    death_label_str = Label(right_frame, font = ("Arial", 18), fg = "green", bg = "black", padx = 20, pady = 10, textvariable=death_label_number)
    death_label_str.grid(row = 5, column = 3)

    check_total = StringVar()
    check_total.set(0)
    check_total_str = Label(right_frame, font = ("Arial", 18), fg = "green", bg = "black", padx = 20, pady = 10, textvariable=check_total)
    check_total_str.grid(row = 6, column = 3)


    add_hits = Button(right_frame,
                      text = "Add Hits",
                      command = AddHits,
                      width = 10,
                      height = 2)
    add_hits.grid(row = 7, column = 1, padx = 10, pady = 10)
    
    add_deaths = Button(right_frame,
                        text = "Add Deaths",
                        command = AddDeaths,
                        width = 10,
                        height = 2)
    add_deaths.grid(row = 7, column = 2,padx = 10, pady = 10)
    

    counter_reset = Button(right_frame,
                           text = "Reset",
                           command = counterReset,
                           width = 10,
                           height = 2)
    counter_reset.grid(row = 7, column = 3, padx = 10, pady = 10)


    add_hits_keybind = Label(right_frame, text = "*", font = ("Arial", 16), fg = "green", bg = "black")
    add_hits_keybind.grid(row = 8, column = 1)

    add_deaths_keybind = Label(right_frame, text = "-", font = ("Arial", 16), fg = "green", bg = "black")
    add_deaths_keybind.grid(row = 8, column = 2)

    reset_keybind = Label(right_frame, text = "+", font = ("Arial", 16), fg = "green", bg = "black")
    reset_keybind.grid(row = 8, column = 3)
    
    root.mainloop()


class StopWatch(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.startTime = 0.0
        self.nextTime = 0.0
        self.onRunning = 0
        self.timestr = StringVar()
        self.MakeWidget()

    def MakeWidget(self):
        timeText = Label(self, textvariable=self.timestr, font=("times new roman", 50), fg="white", bg="black")
        self.SetTime(self.nextTime)
        timeText.pack(fill=X, expand=NO, pady=2, padx=2)

    def Updater(self):
        self.nextTime = time.time() - self.startTime
        self.SetTime(self.nextTime)
        self.timer = self.after(50, self.Updater)

    def SetTime(self, nextElap):
        minutes = int(nextElap / 60)
        seconds = int(nextElap - minutes * 60.0)
        miliSeconds = int((nextElap - minutes * 60.0 - seconds) * 100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, miliSeconds))

    def Start(self):
        if not self.onRunning:
            self.startTime = time.time() - self.nextTime
            self.Updater()
            self.onRunning = 1

    def Stop(self):
        if self.onRunning:
            self.after_cancel(self.timer)
            self.nextTime = time.time() - self.startTime
            self.SetTime(self.nextTime)
            self.onRunning = 0

    def Exit(self):
            root.destroy()
            exit()

    def Reset(self):
        self.startTime = time.time()
        self.nextTime = 0.0
        self.SetTime(self.nextTime)
    

if __name__ == '__main__':
    def OnKeyboardEvent(event):
        if event.Ascii == 42 :
            addhits = int(hit_label_number.get())
            addhits += 1
            hit_label_number.set(addhits)
            if addhits > 9 :
                hit_label_str.config(fg = "Yellow")
            if addhits > 29 :
                hit_label_str.config(fg = "Red")
                
            if hit_label_number or death_label_number > 0 :
                checktotal_hits = int(hit_label_number.get())
                checktotal_deaths = int(death_label_number.get())
                addtotal = checktotal_hits + checktotal_deaths
                check_total.set(addtotal)
            if addtotal > 9 :
                check_total_str.config(fg = "yellow")
            if addtotal > 29 :
                check_total_str.config(fg = "red")
                adddeaths = int(death_label_number.get())

        if event.Ascii == 45 :
            adddeaths = int(death_label_number.get())
            adddeaths += 10
            death_label_number.set(adddeaths)
            if adddeaths > 9 :
                death_label_str.config(fg = "Yellow")
            if adddeaths > 29 :
                death_label_str.config(fg = "Red")
                
            if hit_label_number or death_label_number > 0 :
                checktotal_hits = int(hit_label_number.get())
                checktotal_deaths = int(death_label_number.get())
                addtotal = checktotal_hits + checktotal_deaths
                check_total.set(addtotal)
            if addtotal > 9 :
                check_total_str.config(fg = "yellow")
            if addtotal > 29 :
                check_total_str.config(fg = "red")
        if event.Ascii == 43 :
                hit_label_number.set(0)
                death_label_number.set(0)
                check_total.set(0)
                hit_label_str.config(fg = "green")
                death_label_str.config(fg = "green")
                check_total_str.config(fg = "green")
        return True


    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()

    def AddHits() :
        addhits = int(hit_label_number.get())
        addhits += 1
        hit_label_number.set(addhits)
        if addhits > 9 :
            hit_label_str.config(fg = "Yellow")
        if addhits > 29 :
            hit_label_str.config(fg = "Red")
            
        if hit_label_number or death_label_number > 0 :
            checktotal_hits = int(hit_label_number.get())
            checktotal_deaths = int(death_label_number.get())
            addtotal = checktotal_hits + checktotal_deaths
            check_total.set(addtotal)
        if addtotal > 9 :
            check_total_str.config(fg = "yellow")
        if addtotal > 29 :
            check_total_str.config(fg = "red")
            
    def AddDeaths() :
        adddeaths = int(death_label_number.get())
        adddeaths += 10
        death_label_number.set(adddeaths)
        if adddeaths > 9 :
            death_label_str.config(fg = "Yellow")
        if adddeaths > 29 :
            death_label_str.config(fg = "Red")
            
        if hit_label_number or death_label_number > 0 :
            checktotal_hits = int(hit_label_number.get())
            checktotal_deaths = int(death_label_number.get())
            addtotal = checktotal_hits + checktotal_deaths
            check_total.set(addtotal)
        if addtotal > 9 :
            check_total_str.config(fg = "yellow")
        if addtotal > 29 :
            check_total_str.config(fg = "red")
        

    def counterReset() :
        hit_label_number.set(0)
        death_label_number.set(0)
        check_total.set(0)
        hit_label_str.config(fg = "white")
        death_label_str.config(fg = "white")
        check_total_str.config(fg = "white")


Main()

