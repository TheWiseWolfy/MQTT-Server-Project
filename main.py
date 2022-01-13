import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from Model.Server import *

server = None
running = False
topicList = set()
topicDict = {}
last_iid = 0
max_nr = 0


def main():
    # setting title
    root = tk.Tk()
    root.title("MQTT Server")
    # setting window size
    width = 1290
    height = 897
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)

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
    GButton_991.place(x=970, y=450, width=291, height=69)

    GLineEdit_37 = tk.Entry(root)
    GLineEdit_37["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=10)
    GLineEdit_37["font"] = ft
    GLineEdit_37["fg"] = "#333333"
    GLineEdit_37["justify"] = "center"
    GLineEdit_37["text"] = "<font style=\"vertical - align: inherit;\"><font style=\"vertical - align: " \
                           "inherit;\"><font style=\"vertical - align: inherit;\"><font style=\"vertical - align: " \
                           "inherit;\">Entry</font></font></font></font> "
    GLineEdit_37.place(x=970, y=230, width=181, height=30)

    logs = tk.Listbox(root)
    logs["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=16)
    logs["font"] = ft
    logs["fg"] = "#333333"
    logs["justify"] = "center"
    logs.place(x=660, y=640, width=602, height=240)

    tree2 = ttk.Treeview(root, columns='topic', show='headings')
    tree2.heading('topic', text='Topic', anchor='w')
    tree2.place(x=10, y=640, width=603, height=242)

    GLabel_465 = tk.Label(root)
    ft = tkFont.Font(family='Times', size=10)
    GLabel_465["font"] = ft
    GLabel_465["fg"] = "#333333"
    GLabel_465["justify"] = "center"
    GLabel_465["text"] = "Port"
    GLabel_465.place(x=950, y=200, width=70, height=24)

    GButton_811 = tk.Button(root)
    GButton_811["bg"] = "#efefef"
    ft = tkFont.Font(family='Times', size=10)
    GButton_811["font"] = ft
    GButton_811["fg"] = "#000000"
    GButton_811["justify"] = "center"
    GButton_811["text"] = "Start"
    GButton_811.place(x=970, y=270, width=183, height=78)

    GButton_281 = tk.Button(root)
    GButton_281["bg"] = "#efefef"
    ft = tkFont.Font(family='Times', size=10)
    GButton_281["font"] = ft
    GButton_281["fg"] = "#000000"
    GButton_281["justify"] = "center"
    GButton_281["text"] = "Stop"
    GButton_281.place(x=970, y=370, width=184, height=70)

    GLabel_424 = tk.Label(root)
    ft = tkFont.Font(family='Times', size=10)
    GLabel_424["font"] = ft
    GLabel_424["fg"] = "#333333"
    GLabel_424["justify"] = "center"
    GLabel_424["text"] = "Server log"
    GLabel_424.place(x=650, y=610, width=70, height=24)

    GLabel_921 = tk.Label(root)
    ft = tkFont.Font(family='Times', size=10)
    GLabel_921["font"] = ft
    GLabel_921["fg"] = "#333333"
    GLabel_921["justify"] = "center"
    GLabel_921["text"] = "Last 10 entries"
    GLabel_921.place(x=10, y=610, width=93, height=30)

    columns = ('client_id', 'topics')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.heading('client_id', text='Client ID')
    tree.heading('topics', text='Subscribed topics')
    tree.grid(row=0, column=0, sticky='nsew')
    tree.place(x=20, y=40, width=926, height=561)

    def startServer():
        global server
        server = MQTTServer(tree, logs)
        global running
        running = True

    GButton_811["command"] = startServer

    def addClient(event):
        tree.delete(*tree.get_children())
        global count, last_iid, max_nr
        last_iid = 1
        count = 1
        for client in server.clientManager.activeClients.values():
            tree.insert('', tk.END, values=(client.clientID, client.associatedSession.subscribedTopics))
            for topic in server.clientManager.topicEntry.keys():
                topicList.add(topic)

        for topic in topicList:
            topicDict.update({count: topic})
            count += 1

        tree2.delete(*tree2.get_children())
        for elem in topicDict:
            tree2.insert('', tk.END, values=(topicDict.get(elem),), iid=elem, open=False)
            last_iid += 1

        max_nr = 0
        insertChildren()

    def insertChildren():
        global last_iid, max_nr
        for elem in server.clientManager.topicEntry:
            for val in reversed(server.clientManager.topicEntry[elem]):
                if max_nr < 10:
                    tree2.insert(get_key(topicDict, elem), tk.END, values=("   " + val,), iid=last_iid, open=False)
                    max_nr += 1
                    last_iid += 1

    tree.bind("<<CONNECT>>", addClient)
    tree.bind("<<PUBLISH>>", addClient)
    tree.bind("<<SUBSCRIBE>>", addClient)
    tree.bind("<<DISCONNECT>>", addClient)

    def stopServer():
        global running
        global server
        if running is True:
            server.serverISKill()
            running = False
            server = None
        tree.delete(*tree.get_children())
        tree2.delete(*tree2.get_children())

    def disconnectClient():
        global server
        for client in server.clientManager.activeClients:
            if tree.item(tree.selection()[0], "value")[0] == server.clientManager.activeClients.get(client).clientID:
                server.clientManager.clientSafelyDisconnected(
                    server.clientManager.activeClients.get(client).associatedSocket)
                break

    def destroy():
        stopServer()
        root.destroy()

    GButton_991["command"] = disconnectClient
    GButton_281["command"] = stopServer
    root.protocol("WM_DELETE_WINDOW", destroy)
    root.mainloop()


def get_key(dict, val):
    for key, value in dict.items():
        if val == value:
            return key


if __name__ == '__main__':
    main()

# Server MQTT
# Vizualizare clienți conectați și abonați, deconectare forțată client   -naah
# Vizualizarea istoricului pentru ultimele 10 valori publicate/topic    -naah
# Autentificare clienți   -naah
# Implementare mecanism KeepAlive   -YES
# Implementare QoS 0,1,2  -naah
# Implementare funcție de reținere (retain) a mesajelor  -trying my best
# Implementare mecanism LastWill  -YES
