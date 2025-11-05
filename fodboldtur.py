import pickle
import tkinter as tk
from tkinter import messagebox

filename = 'betalinger.pk'
egenbetaling = 4500

try:
    with open(filename, 'rb') as infile:
        fodboldtur = pickle.load(infile)
except (FileNotFoundError, EOFError):
    fodboldtur = {}

navne = list(fodboldtur.keys())

def gem_data():
    with open(filename, 'wb') as outfile:
        pickle.dump(fodboldtur, outfile)

def afslut():
    gem_data()
    messagebox.showinfo("Afslutning", "Programmet er afsluttet!")
    root.destroy()

def vis_oversigt():
    skift_vindue()
    tk.Label(root, text="Oversigt over betalinger", font=("Arial", 16, "bold")).pack(pady=10)
    tekst = tk.Text(root, width=60, height=15)
    tekst.pack(pady=10)
    for navn, beløb in fodboldtur.items():
        tekst.insert(tk.END, f"{navn} har betalt {beløb} DKK og mangler {egenbetaling - beløb} DKK\n")
    tekst.config(state='disabled')
    tk.Button(root, text="Tilbage til menu", command=menu).pack(pady=10)

def registrer_betaling():
    skift_vindue()
    tk.Label(root, text="Registrér betaling", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(root, text="Navn:").pack()
    navn_var = tk.StringVar(value=navne[0] if navne else "")
    navne_menu = tk.OptionMenu(root, navn_var, *navne)
    navne_menu.pack(pady=5)

    tk.Label(root, text="Beløb der betales:").pack()
    beløb_entry = tk.Entry(root)
    beløb_entry.pack(pady=5)

    def registrér():
        navn = navn_var.get()
        try:
            beløb = float(beløb_entry.get())
            fodboldtur[navn] += beløb
            gem_data()
            messagebox.showinfo("Succes", f"{navn} har nu betalt i alt {fodboldtur[navn]} DKK.")
            menu()
        except ValueError:
            messagebox.showerror("Fejl", "Indtast et gyldigt tal.")
        except KeyError:
            messagebox.showerror("Fejl", "Navnet findes ikke i listen.")

    tk.Button(root, text="Gem betaling", command=registrér).pack(pady=5)
    tk.Button(root, text="Tilbage til menu", command=menu).pack(pady=10)

def shame():
    skift_vindue()
    tk.Label(root, text="Top 3 slackere", font=("Arial", 16, "bold")).pack(pady=10)
    tekst = tk.Text(root, width=60, height=10)
    tekst.pack(pady=10)
    if fodboldtur:
        sorteret = sorted(fodboldtur.items(), key=lambda x: x[1])[:3]
        for i, (navn, beløb) in enumerate(sorteret, start=1):
            tekst.insert(tk.END, f"{i}. {navn} med {beløb} DKK\n")
    else:
        tekst.insert(tk.END, "Ingen data tilgængelig.")
    tekst.config(state='disabled')
    tk.Button(root, text="Tilbage til menu", command=menu).pack(pady=10)

def skift_vindue():
    for widget in root.winfo_children():
        widget.destroy()

def menu():
    skift_vindue()
    tk.Label(root, text="MENU", font=("Arial", 20, "bold")).pack(pady=20)
    tk.Button(root, text="Oversigt over betalinger", width=25, command=vis_oversigt).pack(pady=5)
    tk.Button(root, text="Registrér ny betaling", width=25, command=registrer_betaling).pack(pady=5)
    tk.Button(root, text="De langsomme betalere", width=25, command=shame).pack(pady=5)
    tk.Button(root, text="Afslut", width=25, command=afslut).pack(pady=5)

root = tk.Tk()
root.title("Regnskabsværktøj til fodboldtur")
root.geometry("500x500")
menu()
root.mainloop()
