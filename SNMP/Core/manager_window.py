import threading
from tkinter import *

from Requests.ReceiveTrap import ReceiveTrap
from Requests.GetRequest import GetRequest
from Requests.SetRequest import SetRequest

def startWindow():
    # Configurare fereastră principală
    window = Tk()
    window.title("Interfață Manager SNMP")
    window.geometry("700x400")
    window.configure(bg='#fff2e6')  # Fundal portocaliu pal

    # Titlu vibrant
    title_label = Label(
        window,
        text="Manager SNMP",
        font=('Comic Sans MS', 24, 'bold'),
        bg='#fff2e6',
        fg='#ff6600'
    )
    title_label.pack(pady=20)

    # Cadru pentru butoane
    button_frame = Frame(window, bg='#ffe6cc', relief=RAISED, borderwidth=3)
    button_frame.pack(pady=20, padx=20)

    # Butoane
    Button(
        button_frame, text="Get Request", command=GetRequest,
        bg="#ff9933", fg="white", font=('Helvetica', 14), width=20, height=2
    ).grid(row=0, column=0, padx=15, pady=10)

    Button(
        button_frame, text="Set Request", command=SetRequest,
        bg="#ff6600", fg="white", font=('Helvetica', 14), width=20, height=2
    ).grid(row=0, column=1, padx=15, pady=10)

    # Separator decorativ
    separator = Frame(window, height=2, bd=1, relief=SUNKEN, bg="#ff6600")
    separator.pack(fill="x", padx=20, pady=10)

    # Footer
    footer_label = Label(
        window,
        text="SNMP Manager - Interfață Grafică",
        bg='#fff2e6',
        fg='#cc4400',
        font=('Helvetica', 12, 'italic')
    )
    footer_label.pack(side=BOTTOM, pady=10)

    threading.Thread(target=ReceiveTrap).start()

    window.mainloop()
