import sys

from Model.Server import MQTTServer
import tkinter as tk
import tkinter.font as tkFont


class App:
    server = None
    running = False
    GListBox_787= None
    def __init__(self, root):
        # setting title
        root.title("undefined")
        # setting window size
        width = 623
        height = 897
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GListBox_787 = tk.Listbox(root)
        GListBox_787["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GListBox_787["font"] = ft
        GListBox_787["fg"] = "#333333"
        GListBox_787["justify"] = "center"
        GListBox_787.place(x=10, y=40, width=291, height=200)

        GLabel_952 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_952["font"] = ft
        GLabel_952["fg"] = "#333333"
        GLabel_952["justify"] = "center"
        GLabel_952["text"] = "Client List"
        GLabel_952.place(x=10, y=10, width=70, height=24)

        GButton_991 = tk.Button(root)
        GButton_991["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        GButton_991["font"] = ft
        GButton_991["fg"] = "#000000"
        GButton_991["justify"] = "center"
        GButton_991["text"] = "Disconnect client"
        GButton_991.place(x=10, y=250, width=291, height=69)
        GButton_991["command"] = self.GButton_991_command

        GLineEdit_37 = tk.Entry(root)
        GLineEdit_37["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GLineEdit_37["font"] = ft
        GLineEdit_37["fg"] = "#333333"
        GLineEdit_37["justify"] = "center"
        GLineEdit_37.place(x=370, y=40, width=181, height=30)

        GListBox_73 = tk.Listbox(root)
        GListBox_73["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GListBox_73["font"] = ft
        GListBox_73["fg"] = "#333333"
        GListBox_73["justify"] = "center"
        GListBox_73.place(x=10, y=360, width=602, height=240)

        GListBox_112 = tk.Listbox(root)
        GListBox_112["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GListBox_112["font"] = ft
        GListBox_112["fg"] = "#333333"
        GListBox_112["justify"] = "center"
        GListBox_112.place(x=10, y=640, width=603, height=242)

        GLabel_465 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_465["font"] = ft
        GLabel_465["fg"] = "#333333"
        GLabel_465["justify"] = "center"
        GLabel_465["text"] = "Port"
        GLabel_465.place(x=370, y=10, width=70, height=24)

        GButton_811 = tk.Button(root)
        GButton_811["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        GButton_811["font"] = ft
        GButton_811["fg"] = "#000000"
        GButton_811["justify"] = "center"
        GButton_811["text"] = "Start"
        GButton_811.place(x=370, y=80, width=183, height=78)
        GButton_811["command"] = self.GButton_811_command

        GButton_281 = tk.Button(root)
        GButton_281["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        GButton_281["font"] = ft
        GButton_281["fg"] = "#000000"
        GButton_281["justify"] = "center"
        GButton_281["text"] = "Stop"
        GButton_281.place(x=370, y=170, width=184, height=70)
        GButton_281["command"] = self.GButton_281_command

        GLabel_424 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_424["font"] = ft
        GLabel_424["fg"] = "#333333"
        GLabel_424["justify"] = "center"
        GLabel_424["text"] = "Server log"
        GLabel_424.place(x=10, y=330, width=70, height=24)

        GLabel_921 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_921["font"] = ft
        GLabel_921["fg"] = "#333333"
        GLabel_921["justify"] = "center"
        GLabel_921["text"] = "Last 10 entries"
        GLabel_921.place(x=10, y=610, width=93, height=30)

    def GButton_991_command(self):
        print("dis client")

    def GButton_811_command(self):
        App.server = MQTTServer()
        self.running= True

    def GButton_281_command(self):
        if self.running is True:
            App.server.serverISKill()
            self.running = False

    @staticmethod
    def add_element(self,str):
        self.GListBox_787.insert(str)

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()
    sys.exit()

if __name__ == "__main__":
    main()

# Server MQTT
# Vizualizare clienți conectați și abonați, deconectare forțată client   -naah
# Vizualizarea istoricului pentru ultimele 10 valori publicate/topic    -naah
# Autentificare clienți   -naah
# Implementare mecanism KeepAlive   -YES
# Implementare QoS 0,1,2  -naah
# Implementare funcție de reținere (retain) a mesajelor  -trying my best
# Implementare mecanism LastWill  -YES