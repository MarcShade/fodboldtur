import pickle
import tkinter as tk

running = True

filename = 'betalinger.pk'

fodboldtur = {}
navne = []

with open(filename, 'rb') as infile:
    fodboldtur = pickle.load(infile)

for item in fodboldtur.items():
    navne.append(item[0])

egenbetaling = 4500

def afslut():
    with open(filename, 'wb') as outfile:
        pickle.dump(fodboldtur, outfile)
    print("Programmet er afsluttet!")

def printliste():
    for item in fodboldtur:
        beløb = fodboldtur[item]
        print(f"{item} har betalt {beløb} DKK og mangler at betale {egenbetaling - beløb} DKK\n")

def modtag_betaling():
    while True:
        navn = input("Indtast navn ('r' for at returnere til menuen): ").title()
        if navn == "r":
            return
        if navn in navne:
            break
        else:
            print("Navnet findes ikke")
    
    while True:
        try:
            beløb = float(input("Indtast beløbet der betales: "))
            fodboldtur[navn] += beløb
            print(f"{navn} har nu betalt i alt {fodboldtur[navn]} DKK")
            return
        except ValueError:
            print("Indtast en gyldig værdi for beløbet.")

def shame():
    sorteret_liste = sorted(fodboldtur.items(), key=lambda x: x[1])[:3]
    print("De tre medlemmer der har betalt mindst er:")
    for i, (navn, beløb) in enumerate(sorteret_liste, start=1):
        print(f"    {i}. {navn} med {beløb} kr")

root = tk.Tk()
root.title("Regnskabsværktøj til fodboldtur")


while running:
    print("\nMENU")
    print("1: Print liste")
    print("2: Afslut program")
    print("3: Modtag betaling")
    print("4: Vis dem, som har betalt mindst")

    valg = input("Indtast dit valg: ")

    if valg == '1':
        printliste()
    elif valg == '2':
        afslut()
        break
    elif valg == '3':
        modtag_betaling()
    elif valg == '4':
        shame()
    else:
        print("Ugyldigt valg!")
