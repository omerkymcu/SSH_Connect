import os
import subprocess
from tkinter import Tk, Label, Button, StringVar, Frame, filedialog, Menubutton, Menu

def key_dosyalari_bul(klasor):
    if klasor:
        return [f for f in os.listdir(klasor) if f.endswith('.key')]
    else:
        return []

def sunucuya_baglan(key_dosyasi, kullanici, ip_adresi):
    komut = f"ssh -i {key_dosyasi} {kullanici}@{ip_adresi}"
    terminal_komutu = f"osascript -e 'tell app \"Terminal\" to do script \"{komut}\"'"
    subprocess.run(terminal_komutu, shell=True)

def baglan_click():
    key_dosyasi = os.path.join(key_klasoru.get(), secili_key.get())
    sunucuya_baglan(key_dosyasi, kullanici, ip_adresi)

def refresh_keys():
    global key_secim_menu
    key_secim_menu.delete(0, "end")
    key_dosyalari = key_dosyalari_bul(key_klasoru.get())
    for dosya in key_dosyalari:
        key_secim_menu.add_command(label=dosya, command=lambda val=dosya: secili_key.set(val))

def browse_ssh_folder():
    klasor = filedialog.askdirectory()
    if klasor:
        key_klasoru.set(klasor)
        refresh_keys()

kullanici = "ubuntu"
ip_adresi = "129.151.80.155"

app = Tk()
app.title("SSH Connect")
app.geometry("800x600")

browse_button = Button(app, text="SSH Klasörü Seç", command=browse_ssh_folder)
browse_button.pack(side="left")

label = Label(app, text="Instance:")
label.pack(side="left")

secili_key = StringVar(app)
secili_key.set("Anahtar Seç")

key_klasoru = StringVar(app)
key_klasoru.set("")  # Varsayılan anahtar dosyalarının bulunduğu klasör yolunu boş bırakın.

key_dosyalari = key_dosyalari_bul(key_klasoru.get())

key_secim_menu_button = Menubutton(app, textvariable=secili_key, relief="raised")
key_secim_menu_button.pack(side="left")

key_secim_menu = Menu(key_secim_menu_button, tearoff=False)
key_secim_menu_button.configure(menu=key_secim_menu)
refresh_keys()

refresh_button = Button(app, text="Yenile", command=refresh_keys)
refresh_button.pack(side="left")

baglan_button = Button(app, text="Bağlan", command=baglan_click)
baglan_button.pack(side="left")

app.mainloop()
