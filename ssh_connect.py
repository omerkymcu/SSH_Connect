import os
import subprocess
from tkinter import Tk, Label, Button, OptionMenu, StringVar, Frame, filedialog

def key_dosyalari_bul(klasor):
    return [f for f in os.listdir(klasor) if f.endswith('.key')]

def sunucuya_baglan(key_dosyasi, kullanici, ip_adresi):
    komut = f"ssh -i {key_dosyasi} {kullanici}@{ip_adresi}"
    subprocess.run(komut, shell=True)

def baglan_click():
    key_dosyasi = os.path.join(key_klasoru.get(), secili_key.get())
    sunucuya_baglan(key_dosyasi, kullanici, ip_adresi)

def refresh_keys():
    global key_secim_menu
    key_secim_menu["menu"].delete(0, "end")
    key_dosyalari = key_dosyalari_bul(key_klasoru.get())
    for dosya in key_dosyalari:
        key_secim_menu["menu"].add_command(label=dosya, command=lambda val=dosya: secili_key.set(val))

def browse_ssh_folder():
    klasor = filedialog.askdirectory()
    if klasor:
        key_klasoru.set(klasor)
        refresh_keys()

kullanici = "ubuntu"
ip_adresi = "129.151.80.155"

app = Tk()
app.title("SSH Connect")

label = Label(app, text="Instance:")
label.pack()

secili_key = StringVar(app)
secili_key.set("Anahtar Seç")

key_klasoru = StringVar(app)
key_klasoru.set("klasorun_yolu")  # Varsayılan anahtar dosyalarının bulunduğu klasör yolunu buraya giriniz.

key_dosyalari = key_dosyalari_bul(key_klasoru.get())
key_secim_menu = OptionMenu(app, secili_key, *key_dosyalari)
key_secim_menu.pack(side="left")

refresh_button = Button(app, text="Yenile", command=refresh_keys)
refresh_button.pack(side="left")

baglan_button = Button(app, text="Bağlan", command=baglan_click)
baglan_button.pack(side="left")

browse_button = Button(app, text="SSH Klasörü Seç", command=browse_ssh_folder)
browse_button.pack(side="left")

app.mainloop()
