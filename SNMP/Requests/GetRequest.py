from tkinter import *
import socket
from Protocol.packet_utils import encodeASN1, decodeASN1
from Utils.mib_utils import *

agentIp = '127.0.0.1'
conn = bytearray(agentIp, "utf-8")
bufferSize = 1024


def update_textbox(message):
    # Șterge conținutul vechi
    output_text.delete(1.0, END)

    # Calculăm numărul de linii goale necesare pentru centrare verticală
    textbox_height = int(output_text['height'])
    lines_required = (textbox_height - 1) // 2
    for _ in range(lines_required):
        output_text.insert(END, "\n")

    # Introducem mesajul principal
    output_text.insert(END, message)
    output_text.tag_add("center", 1.0, "end")


def GetRequest():
    window = Tk()
    window.title("Cereri SNMP")
    window.geometry("800x500")
    window.configure(bg='#f0f0ff')

    title_label = Label(
        window,
        text="Selectați informația dorită",
        font=('Comic Sans MS', 20, 'bold'),
        bg='#f0f0ff',
        fg='#6633ff'
    )
    title_label.pack(pady=10)

    # Cadru pentru butoane
    button_frame = Frame(window, bg='#e6e6ff', relief=RAISED, borderwidth=3)
    button_frame.pack(pady=10, padx=10)

    # Lista de comenzi pentru fiecare buton
    button_commands = [
        ("Nume", GetRequestName),
        ("Temperatura", GetRequestTemperatura),
        ("Ram % Usage", GetRequestRamPercent),
        ("Ram Gb Usage", GetRequestRamGB),
        ("Cpu Usage", GetRequestCpuUsage)
    ]

    # Crearea butoanelor
    for i, (text, command) in enumerate(button_commands):
        Button(
            button_frame,
            text=text,
            command=command,
            bg="#6699ff", fg="white", font=('Arial', 14),
            width=20, height=2
        ).grid(row=i // 2, column=i % 2, padx=15, pady=5)

    separator = Frame(window, height=2, bd=1, relief=SUNKEN, bg="#6633ff")
    separator.pack(fill="x", padx=20, pady=10)

    # Casetă text pentru afișare mesaje
    global output_text
    output_text = Text(
        window,
        height=6,
        width=40,
        bg="#ffffff",
        fg="#333333",
        font=('Arial', 14),
        wrap=WORD,
        relief=RIDGE,
        bd=2
    )
    output_text.tag_configure("center", justify="center")
    output_text.pack(padx=20, pady=5)

    # Buton Înapoi
    back_button_frame = Frame(window, bg='#f0f0ff')
    back_button_frame.pack(side=BOTTOM, pady=10)
    Button(
        back_button_frame, text="Înapoi", command=window.destroy,
        bg="#cc33ff", fg="white", font=('Helvetica', 14, 'bold'), width=15, height=2
    ).pack()

    window.mainloop()


def GetRequestCpuUsage():
    encoded_message = encodeASN1(oid="1.5", text="Null", val=0)

    UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPclient.sendto(encoded_message, (conn, 8080))

    data = UDPclient.recvfrom(bufferSize)[0]
    decoded = decodeASN1(data)
    text = f"CPU usage: {float(decoded[2]):.2f}%"
    update_textbox(text)


def GetRequestRamPercent():
    encoded_message = encodeASN1(oid="1.3", text="Null", val=0)

    UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPclient.sendto(encoded_message, (conn, 8080))

    data = UDPclient.recvfrom(bufferSize)[0]
    decoded = decodeASN1(data)
    text = f"RAM Usage: {float(decoded[2]):.2f}%"
    update_textbox(text)


def GetRequestRamGB():
    encoded_message = encodeASN1(oid="1.4", text="Null", val=0)

    UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPclient.sendto(encoded_message, (conn, 8080))

    data = UDPclient.recvfrom(bufferSize)[0]
    decoded = decodeASN1(data)
    text = f"RAM Usage: {float(decoded[2]):.2f} GB"
    update_textbox(text)


def GetRequestName():
    encoded_message = encodeASN1(oid="1.2", text="Null", val=0)

    UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPclient.sendto(encoded_message, (conn, 8080))

    data = UDPclient.recvfrom(bufferSize)[0]
    decoded = decodeASN1(data)
    text = f"Numele agentului: {decoded[1]}"
    update_textbox(text)


def GetRequestTemperatura():
    encoded_message = encodeASN1(oid="1.1", text="Null", val=0)

    UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPclient.sendto(encoded_message, (conn, 8080))

    data = UDPclient.recvfrom(bufferSize)[0]
    decoded = decodeASN1(data)
    value = float(decoded[2])

    # Determinăm unitatea de măsură
    if value > 273:
        temperature = f"{value:.2f} °K"
    elif value > 100:
        temperature = f"{value:.2f} °F"
    else:
        temperature = f"{value:.2f} °C"

    update_textbox(f"Temperatura: {temperature}")