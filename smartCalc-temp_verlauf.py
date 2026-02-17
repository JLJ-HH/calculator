# ================================
# smartCalc-temp_verlauf.py
# Erweiterung: Rechenverlauf im RAM speichern und anzeigen
# ================================

import math       # Für mathematische Funktionen: sin, cos, sqrt, log, etc.
import re         # Für reguläre Ausdrücke: Funktionen erkennen und ersetzen
import tkinter as tk               # GUI-Bibliothek
from tkinter import messagebox     # Popup-Fenster für Infos

# ================================
# Klasse: RechenParser
# ================================
class RechenParser:
    """Verarbeitet mathematische Ausdrücke und berechnet das Ergebnis"""
    
    # Zulässige Zeichen für die Eingabe (alles, was eval() auswerten darf)
    erlaubte_zeichen = "0123456789.+-*/()%^√πe sintgloarcexpn"
    
    @staticmethod
    def berechne(eingabe):
        """
        Berechnet mathematischen Ausdruck als String.
        Rückgabe:
          - float/int, falls korrekt
          - Fehlermeldung als String bei Fehlern
        """
        # 1️⃣ Ungültige Zeichen prüfen
        if any(c not in RechenParser.erlaubte_zeichen for c in eingabe.lower()):
            return "Ungültige Zeichen"
        
        try:
            # 2️⃣ Potenzen: ^ → **
            eingabe = eingabe.replace("^", "**")
            
            # 3️⃣ Wurzel √ behandeln: √9 → math.sqrt(9)
            while "√" in eingabe:
                pos = eingabe.find("√")
                zahl = ""
                i = pos + 1
                while i < len(eingabe) and (eingabe[i].isdigit() or eingabe[i] == "."):
                    zahl += eingabe[i]
                    i += 1
                if not zahl:
                    return "Fehler bei √"
                eingabe = eingabe[:pos] + f"math.sqrt({zahl})" + eingabe[pos+1+len(zahl):]
            
            # 4️⃣ Prozent behandeln: 50% → 50/100
            eingabe = re.sub(r"(\d+(\.\d+)?)%", r"(\1/100)*", eingabe)
            
            # 5️⃣ Konstanten ersetzen: π → math.pi, e → math.e
            eingabe = eingabe.replace("π", "math.pi").replace("e", "math.e")
            
            # 6️⃣ Funktionen: sin, cos, tan, log, ln, exp, arcsin, arccos, arctan
            funktionen = {
                r"sin\(([^)]+)\)": r"math.sin(math.radians(\1))",
                r"cos\(([^)]+)\)": r"math.cos(math.radians(\1))",
                r"tan\(([^)]+)\)": r"math.tan(math.radians(\1))",
                r"log\(([^)]+)\)": r"math.log10(\1)",
                r"ln\(([^)]+)\)": r"math.log(\1)",
                r"exp\(([^)]+)\)": r"math.exp(\1)",
                r"arcsin\(([^)]+)\)": r"math.degrees(math.asin(\1))",
                r"arccos\(([^)]+)\)": r"math.degrees(math.acos(\1))",
                r"arctan\(([^)]+)\)": r"math.degrees(math.atan(\1))"
            }
            
            for pattern, ersatz in funktionen.items():
                eingabe = re.sub(pattern, ersatz, eingabe)
            
            # 7️⃣ Ausdruck auswerten
            ergebnis = eval(eingabe)
            
            # 8️⃣ Ergebnis runden, falls Float
            return round(ergebnis, 4) if isinstance(ergebnis, float) else ergebnis
        
        # 9️⃣ Fehlerbehandlung
        except ZeroDivisionError:
            return "Division durch 0"
        except Exception:
            return "Ungültige Rechnung"


# ================================
# Klasse: VerlaufManager
# ================================
class VerlaufManager:
    """
    Speichert Rechenverlauf nur im RAM (temporär).
    Zeigt den Verlauf in einem großen scrollbaren Fenster.
    """
    
    def __init__(self):
        self.eintraege = []  # Liste für Verlaufseinträge
    
    def speichern(self, eingabe, ergebnis):
        """Fügt neue Rechnung dem Verlauf hinzu"""
        self.eintraege.append(f"{eingabe} = {ergebnis}")
    
    def anzeigen(self, master=None):
        """
        Öffnet ein neues Fenster, um den Verlauf groß und scrollbar darzustellen.
        master: Parent-Fenster (üblicherweise root)
        """
        if not self.eintraege:
            messagebox.showinfo("Verlauf", "Noch keine Rechnungen.")
            return
        
        # Neues Fenster erstellen
        fenster = tk.Toplevel(master)
        fenster.title("Rechenverlauf")
        fenster.geometry("400x300")
        
        # Textfeld für Einträge
        text = tk.Text(fenster, font=("Arial", 14))
        text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar hinzufügen
        scrollbar = tk.Scrollbar(fenster, command=text.yview)
        scrollbar.pack(side="right", fill="y")
        text.config(yscrollcommand=scrollbar.set)
        
        # Alle Einträge einfügen
        for eintrag in self.eintraege:
            text.insert("end", eintrag + "\n")
        
        text.config(state="disabled")  # nur lesen
    
    def loeschen(self):
        """Leert den Verlauf nach Bestätigung"""
        if messagebox.askyesno("Verlauf löschen", "Wirklich löschen?"):
            self.eintraege.clear()


# ================================
# Klasse: TaschenrechnerGUI
# ================================
class TaschenrechnerGUI:
    """GUI für wissenschaftlichen Taschenrechner"""
    
    def __init__(self):
        # 1️⃣ Hauptfenster
        self.root = tk.Tk()
        self.root.title("Taschenrechner Wissenschaft (Online)")
        self.root.resizable(True, True)
        
        # 2️⃣ Parser und Verlaufmanager initialisieren
        self.parser = RechenParser()
        self.verlauf = VerlaufManager()
        self.dark_mode = False  # Standard hell
        
        # 3️⃣ Display-Variable für Entry
        self.display_var = tk.StringVar()
        
        # 4️⃣ GUI aufbauen
        self._gui_bauen()
        self._events_binden()
    
    # ----------------------------
    # GUI Aufbau
    # ----------------------------
    def _gui_bauen(self):
        # Display
        self.display = tk.Entry(
            self.root, textvariable=self.display_var,
            font=("Arial", 22), bd=5, relief="sunken",
            justify="right", state="readonly"
        )
        self.display.pack(fill="x", padx=8, pady=8)
        
        # Button-Frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()
        
        # Button-Definition
        self.buttons = [
            ['7','8','9','/','C',''],
            ['4','5','6','*','DEL',''],
            ['1','2','3','-','√',''],
            ['0','.','%','+','^',''],
            ['(',')','π','e','ln','exp'],
            ['sin','cos','tan','arcsin','arccos','arctan'],
            ['log','Verlauf','Löschen','Dark/Light','Shortcuts','=']
        ]
        
        # Farben für spezielle Buttons
        self.farben = {
            'C': '#ff6b6b', 'DEL': '#ffd93d', '=': '#6bcb77',
            'Löschen': '#ff6b6b', 'Verlauf': '#4d96ff',
            'Dark/Light': '#ffa500', 'Shortcuts': '#8a2be2',
            'sin': '#d8bfd8', 'cos': '#d8bfd8', 'tan': '#d8bfd8',
            'log': '#d8bfd8', 'ln': '#d8bfd8', 'exp': '#d8bfd8',
            'arcsin': '#dda0dd', 'arccos': '#dda0dd', 'arctan': '#dda0dd',
            'π': '#f0e68c', 'e': '#f0e68c'
        }
        
        self._buttons_erstellen()
    
    def _buttons_erstellen(self):
        """Erstellt Buttons dynamisch und ordnet Funktion zu"""
        for r, row in enumerate(self.buttons):
            for c, text in enumerate(row):
                if not text: continue
                cmd = self._befehl_fuer_button(text)
                btn = tk.Button(
                    self.button_frame, text=text, width=7, height=2,
                    font=("Arial", 14),
                    bg=self.farben.get(text, "#e0e0e0"),
                    command=cmd
                )
                btn.grid(row=r, column=c, padx=3, pady=3)
    
    def _befehl_fuer_button(self, text):
        """Ordnet spezielle Funktionen den Buttons zu"""
        befehle = {
            'C': self.clear_entry,
            'DEL': self.delete_last,
            '=': self.calculate,
            'Verlauf': lambda: self.verlauf.anzeigen(self.root),
            'Löschen': self.verlauf.loeschen,
            'Dark/Light': self.toggle_dark,
            'Shortcuts': self.shortcut_overlay
        }
        # Standard: Button tippt Text ins Display
        return befehle.get(text, lambda: self.update_display(text))
    
    # ----------------------------
    # Tastatur-Events
    # ----------------------------
    def _events_binden(self):
        """Bindet Tastenanschläge an Funktionen"""
        self.root.bind("<Key>", self.tastatur)
    
    # ----------------------------
    # GUI Methoden
    # ----------------------------
    def update_display(self, wert):
        """Fügt einen Wert ans Display an"""
        self.display.config(state="normal")
        self.display_var.set(self.display_var.get() + str(wert))
        self.display.config(state="readonly")
    
    def clear_entry(self):
        """Display leeren"""
        self.display.config(state="normal")
        self.display_var.set("")
        self.display.config(state="readonly")
    
    def delete_last(self):
        """Letztes Zeichen löschen"""
        self.display.config(state="normal")
        self.display_var.set(self.display_var.get()[:-1])
        self.display.config(state="readonly")
    
    def calculate(self):
        """Berechnet Eingabe und speichert Ergebnis im Verlauf"""
        eingabe = self.display_var.get()
        ergebnis = self.parser.berechne(eingabe)
        self.display_var.set(str(ergebnis))
        if isinstance(ergebnis, (int, float)):
            self.verlauf.speichern(eingabe, ergebnis)
    
    def toggle_dark(self):
        """Wechselt zwischen Dark Mode und Light Mode"""
        self.dark_mode = not self.dark_mode
        bg = "#222" if self.dark_mode else "#f0f0f0"
        fg = "#fff" if self.dark_mode else "#000"
        self.display.config(bg=bg, fg=fg)
        for btn in self.button_frame.winfo_children():
            btn.config(
                bg=self.farben.get(btn['text'], "#888") if not self.dark_mode else "#555",
                fg=fg
            )
    
    def shortcut_overlay(self):
        """Popup mit Tastatur-Shortcuts"""
        msg = ("Tastatur Shortcuts:\n"
               "Enter = =\nBackspace = DEL\nEscape = C\n"
               "Zahlen + Operatoren direkt tippen\n"
               "sin(x), cos(x), etc. funktionieren")
        messagebox.showinfo("Shortcuts", msg)
    
    def tastatur(self, event):
        """Verarbeitet Tastatur-Input"""
        if event.keysym == "Return":
            self.calculate(); return "break"
        elif event.keysym == "BackSpace":
            self.delete_last(); return "break"
        elif event.keysym == "Escape":
            self.clear_entry(); return "break"
        elif event.char in "0123456789+-*/().%^πe":
            self.update_display(event.char); return "break"
    
    def starten(self):
        """Startet die GUI-Schleife"""
        self.root.mainloop()


# ================================
# Programmstart
# ================================
if __name__ == "__main__":
    app = TaschenrechnerGUI()
    app.starten()
