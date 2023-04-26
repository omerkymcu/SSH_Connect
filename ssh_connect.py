import os
import subprocess
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog, Menu, Menubutton, messagebox

CONFIG_FILE = "config.txt"

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
    kullanici = kullanici_adi.get()
    ip_adresi = ip_adres_girisi.get()

    if not kullanici:
        messagebox.showwarning("Kullanıcı Adı Eksik", "Lütfen bir kullanıcı adı girin.")
        return

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
        with open(CONFIG_FILE, "w") as config_file:
            config_file.write(klasor)

def load_ip_from_txt():
    try:
        ip_file_path = filedialog.askopenfilename(initialdir=key_klasoru.get(), filetypes=[("Text Files", "*.txt")])
        if ip_file_path:
            with open(ip_file_path, "r") as ip_file:
                ip_adres_girisi.delete(0, "end")
                ip_adres_girisi.insert(0, ip_file.read().strip())
    except FileNotFoundError:
        print("ip_address.txt dosyası bulunamadı.")

app = Tk()
app.title("SSH Connect")
app.geometry("400x400")

key_klasoru = StringVar(app)
try:
    with open(CONFIG_FILE, "r") as config_file:
        key_klasoru.set(config_file.read())
except FileNotFoundError:
    key_klasoru.set("")

browse_button = Button(app, text="SSH Klasörü Seç", command=browse_ssh_folder, width=20, height=2)
browse_button.place(relx=0.5, rely=0.1, anchor="center")

kullanici_adi_label = Label(app, text="Kullanıcı Adı:")
kullanici_adi_label.place(relx=0.15, rely=0.3, anchor="center")

kullanici_adi = StringVar(app)  # Bu satırı ekleyin
kullanici_adi.set("ubuntu")
kullanici_adi_girisi = Entry(app, textvariable=kullanici_adi)
kullanici_adi_girisi.place(relx=0.5, rely=0.3, anchor="center")

ip_adres_label = Label(app, text="IP Adresi:")
ip_adres_label.place(relx=0.15, rely=0.4, anchor="center")

ip_adres_girisi = Entry(app)
ip_adres_girisi.place(relx=0.5, rely=0.4, anchor="center")

load_ip_button = Button(app, text="TXT'den IP Yükle", command=load_ip_from_txt)
load_ip_button.place(relx=0.5, rely=0.45, anchor="center")

label = Label(app, text="Instance:")
label.place(relx=0.15, rely=0.6, anchor="center")

secili_key = StringVar(app)
secili_key.set("Anahtar Seç")

key_dosyalari = key_dosyalari_bul(key_klasoru.get())

key_secim_menu_button = Menubutton(app, textvariable=secili_key, relief="raised")
key_secim_menu_button.place(relx=0.5, rely=0.6, anchor="center")

key_secim_menu = Menu(key_secim_menu_button, tearoff=False)
key_secim_menu_button.configure(menu=key_secim_menu)
refresh_keys()

refresh_button = Button(app, text="Yenile", command=refresh_keys)
refresh_button.place(relx=0.7, rely=0.6, anchor="center")

baglan_button = Button(app, text="Bağlan", command=baglan_click)
baglan_button.place(relx=0.5, rely=0.8, anchor="center")

app.mainloop()

