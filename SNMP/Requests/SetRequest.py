from tkinter import *
import socket
from Protocol.packet_utils import encodeASN1, decodeASN1  # Funcții pentru codificare/decodare SNMP

def SetRequest():
    window = Tk()
    window.title("Setare Informații SNMP")
    window.geometry("700x400")
    window.configure(bg='#ffe5e5')

    title_label = Label(
        window,
        text="Setează Parametrii SNMP",
        font=('Comic Sans MS', 20, 'bold'),
        bg='#ffe5e5',
        fg='#ff3333'
    )
    title_label.pack(pady=20)

    # Cadru colorat pentru butoane
    button_frame = Frame(window, bg='#ffcccc', relief=RAISED, borderwidth=3)
    button_frame.pack(pady=20, padx=20)

    Button(
        button_frame, text="Setează Nume", command=setRequestName,
        bg="#ff66b2", fg="white", font=('Arial', 14), width=20, height=2
    ).grid(row=0, column=0, padx=15, pady=10)

    Button(
        button_frame, text="Setează Temperatură", command=setRequestTemperature,
        bg="#ff66b2", fg="white", font=('Arial', 14), width=20, height=2
    ).grid(row=0, column=1, padx=15, pady=10)

    separator = Frame(window, height=2, bd=1, relief=SUNKEN, bg="#ff3333")
    separator.pack(fill="x", padx=20, pady=10)

    # Buton Înapoi
    Button(
        window, text="Înapoi", command=window.destroy,
        bg="#ff3333", fg="white", font=('Helvetica', 14, 'bold'), width=15, height=2
    ).pack(pady=20)

    window.mainloop()

def introdusNume(inputtxt):
    nume = inputtxt.get("1.0", "end-1c")
    conn = '127.0.0.1'

    UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    encoded_message = encodeASN1(oid="2.1", text=nume, val=0)
    UDPclient.sendto(encoded_message, (conn, 8080))

    data = UDPclient.recvfrom(1024)[0]
    text = decodeASN1(data)[1]
    print("Numele a fost schimbat în ", text)

def setRequestName():
    window = Tk()
    window.title("Introduceți Numele")
    window.geometry("700x400")
    window.configure(bg='#ccffcc')

    # Titlu
    Label(
        window, text="Introduceți Numele Agentului SNMP",
        bg='#ccffcc', fg='#006600', font=('Comic Sans MS', 18, 'bold')
    ).pack(pady=20)

    # Input pentru nume
    inputtxt = Text(window, height=1, width=40, bg="white", font=('Helvetica', 14))
    inputtxt.pack(pady=10)

    # Buton pentru a seta numele
    Button(
        window, text="Setează Nume", command=lambda: introdusNume(inputtxt),
        bg="#33cc33", fg="white", font=('Helvetica', 14), width=15
    ).pack(pady=20)

    # Buton Înapoi
    Button(
        window, text="Înapoi", command=window.destroy,
        bg="#006400", fg="white", font=('Helvetica', 14), width=15
    ).pack(pady=20)

    window.mainloop()

def setRequestTemperature():
    window = Tk()
    window.title("Setare Temperatură")
    window.geometry("700x400")
    window.configure(bg='#e6f2ff')

    # Titlu
    Label(
        window, text="Alegeți Unitatea de Temperatură",
        bg='#e6f2ff', fg='#004080', font=('Comic Sans MS', 18, 'bold')
    ).pack(pady=20)

    # Stil butoane
    button_style = {"bg": "#3385ff", "fg": "white", "font": ('Helvetica', 14), "width": 20, "height": 2}

    # Opțiuni pentru temperatură
    Button(window, text="Celsius", command=lambda: changeTemperature("Celsius"), **button_style).pack(pady=10)
    Button(window, text="Fahrenheit", command=lambda: changeTemperature("Fahrenheit"), **button_style).pack(pady=10)
    Button(window, text="Kelvin", command=lambda: changeTemperature("Kelvin"), **button_style).pack(pady=10)

    # Buton Înapoi
    Button(
        window, text="Înapoi", command=window.destroy,
        bg="#004080", fg="white", font=('Helvetica', 14, 'bold'), width=15
    ).pack(pady=20)

    window.mainloop()

def changeTemperature(temp):
    conn = '127.0.0.1'
    UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    encoded_message = encodeASN1(oid="2.2", text=temp, val=0)
    UDPclient.sendto(encoded_message, (conn, 8080))

    data = UDPclient.recvfrom(1024)[0]
    text = decodeASN1(data)[1]
    print("Temperatura a fost schimbată în ", text)