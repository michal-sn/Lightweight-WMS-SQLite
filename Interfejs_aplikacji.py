import customtkinter as ctk
import tkinter as tk
import Baza_danych
from tktooltip import ToolTip
from tkinter import ttk, messagebox
import bcrypt

ctk.set_appearance_mode("dark")

mont10 = ("Montserrat", 10)
mont16_b = ("Montserrat", 16, "bold")
mont16 = ("Montserrat", 16)
mont16_u = ("Montserrat", 16, "underline")
mont30_b = ("Montserrat", 30, "bold")
mont40_b = ("Montserrat", 40, "bold")


def pokaz_komunikat(rodzaj, tytul, tresc, parent=None):
    top = tk.Toplevel(parent)
    top.withdraw()

    if rodzaj == "info":
        messagebox.showinfo(tytul, tresc, parent=top)
    elif rodzaj == "error":
        messagebox.showerror(tytul, tresc, parent=top)
    elif rodzaj == "warning":
        messagebox.showwarning(tytul, tresc, parent=top)
    elif rodzaj == "question":
        odpowiedz = messagebox.askquestion(tytul, tresc, parent=top)
        top.destroy()
        return odpowiedz

    top.destroy()


class OknoLogowania(ctk.CTkToplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.geometry("500x400")
        self.resizable(False, False)
        self.login_entry = None
        self.haslo_entry = None
        self.okno = None
        self.result = None

        self.okno_zaloguj()
        self.protocol("WM_DELETE_WINDOW", self.zakmniecie_okna)
        self.wycentruj_okno()
        self.grab_set()

    def okno_zarejestruj(self):
        self.inicjalizuj_interfejs("REJESTRACJA", self.zarejestruj, "Zarejestruj się", "Zaloguj się", self.okno_zaloguj)

    def okno_zaloguj(self):
        self.inicjalizuj_interfejs(" LOGOWANIE", self.zaloguj, "Zaloguj się", "Zarejestruj się", self.okno_zarejestruj)

    def inicjalizuj_interfejs(self, naglowek, akcja_przycisku, tekst_przycisku, tekst_przycisku_alt, akcja_przycisku_alt):
        self.okno = ctk.CTkFrame(self, fg_color="#242424")
        self.okno.place(relx=0, rely=0, relwidth=1, relheight=1)

        ctk.CTkLabel(self.okno, font=mont40_b, text=naglowek, text_color="#3074b2").place(x=100, y=30)

        self.login_entry = ctk.CTkEntry(self.okno,
                                        font=mont16,
                                        placeholder_text="Login",
                                        placeholder_text_color="#808080",
                                        width=250,
                                        height=50)
        self.login_entry.place(x=120, y=100)

        self.haslo_entry = ctk.CTkEntry(self.okno,
                                        show="*",
                                        font=mont16,
                                        placeholder_text="Hasło",
                                        placeholder_text_color="#808080",
                                        width=250,
                                        height=50)
        self.haslo_entry.place(x=120, y=180)

        glowny_przycisk = ctk.CTkButton(self.okno,
                                        font=mont16_b,
                                        text=tekst_przycisku,
                                        command=akcja_przycisku,
                                        cursor="hand2",
                                        width=250,
                                        height=40)
        glowny_przycisk.place(x=120, y=260)

        ctk.CTkLabel(self.okno,
                     font=mont16,
                     text="Nie posiadasz konta?" if naglowek == " LOGOWANIE" else "Posiadasz już konto?").place(x=90,
                                                                                                                y=320)

        przycisk_alt = ctk.CTkButton(self.okno,
                                     font=mont16_u,
                                     text=tekst_przycisku_alt,
                                     command=akcja_przycisku_alt,
                                     cursor="hand2", fg_color="#242424",
                                     hover_color="#242424",
                                     text_color="#3074b2",
                                     height=40)
        przycisk_alt.place(x=260, y=315)

    def zarejestruj(self):
        login = self.login_entry.get().strip()
        haslo = self.haslo_entry.get().strip()

        if login and haslo:
            dane_uzytkownika = Baza_danych.pobierz_nazwe_uzytkownika(login)
            if dane_uzytkownika:
                pokaz_komunikat("error", "Błąd", "Użytkownik o takiej nazwie już istnieje")
            else:
                encode_haslo = haslo.encode("utf-8")
                haslo_hash = bcrypt.hashpw(encode_haslo, bcrypt.gensalt())
                Baza_danych.zarejestruj_uzytkownika(login, haslo_hash)
                pokaz_komunikat("info", "Informacja", "Konto zostało dodane")
        else:
            pokaz_komunikat("error", "Błąd", "Oba pola muszą być wypełnione!")

    def zaloguj(self):
        login = self.login_entry.get().strip()
        haslo = self.haslo_entry.get().strip()
        if login and haslo:
            dane_hasla = Baza_danych.pobierz_haslo_uzytkownika(login)
            if dane_hasla:
                zahashowane_haslo = dane_hasla[0][0]
                if bcrypt.checkpw(haslo.encode("utf-8"), zahashowane_haslo):
                    pokaz_komunikat("info", "Informacja", f"Zalogowano jako {login}")
                    self.zastosuj()
                else:
                    pokaz_komunikat("error", "Błąd", "Niepoprawne hasło")
            else:
                pokaz_komunikat("error", "Błąd", "Niepoprawne dane logowania")
        else:
            pokaz_komunikat("error", "Błąd", "Oba pola muszą być wypełnione!")

    def wycentruj_okno(self):
        self.update_idletasks()
        szer = self.winfo_width()
        wys = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (szer // 2)
        y = (self.winfo_screenheight() // 2) - (wys // 2)
        self.geometry(f'{szer}x{wys}+{x}+{y}')

    def zastosuj(self):
        login = self.login_entry.get().strip()
        self.result = login
        self.destroy()

    def zakmniecie_okna(self):
        self.result = None
        self.destroy()


class GlownyInterfejs(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Asortyment magazynowy")
        self.geometry("1500x680")
        self.resizable(True, False)

        self.nip_wpr = None
        self.nazwa_wpr = None
        self.adres_wpr = None
        self.wlsc_wpr = None
        self.telefon_wpr = None
        self.opis_wpr = None
        self.widok_danych_firmy = None
        self.dodaj_prz = None
        self.wyczysc_prz = None
        self.zaaktualizuj_prz = None
        self.usun_prz = None
        self.zamowienia_prz = None
        self.pasekv = None
        self.aktualny_hover_wiersza = None
        self.aktualny_hover_kolumny = None
        self.aktualny_tooltip = None
        self.uzytkownik = self.zaloguj()

        self.wycentruj_okno()
        self.stworz_interfejs()
        self.odswiez_widok_danych()

    def wycentruj_okno(self):
        self.update_idletasks()
        szer = self.winfo_width()
        wys = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (szer // 2)
        y = (self.winfo_screenheight() // 2) - (wys // 2)
        self.geometry(f'{szer}x{wys}+{x}+{y}')

    def zaloguj(self):
        dialog = OknoLogowania(self, "Logowanie")
        self.wait_window(dialog)
        if dialog.result:
            uzytkownik = dialog.result
            return f"{uzytkownik}"
        else:
            self.destroy()
            return None

    def stworz_interfejs(self):
        self.stworz_etykiety()
        self.stworz_wpr()
        self.stworz_przyciski()
        self.stworz_widokdanych()

    def szczegoly_zamowien(self):
        wybrane_elementy = self.widok_danych_firmy.selection()
        if len(wybrane_elementy) == 1:
            wybrany_element = wybrane_elementy[0]
            wiersz = self.widok_danych_firmy.item(wybrany_element, "values")
            nip_firmy = wiersz[0]
            nazwa_firmy = wiersz[1]
            zamowienia = SzczegolyZamowien(self, "Szczegoly zamowien", self.uzytkownik, nip_firmy, nazwa_firmy)
            zamowienia.grab_set()
        else:
            pokaz_komunikat("error", "Błąd", "Musisz wybrać jedną firmę!")

    def stworz_etykiety(self):
        ctk.CTkLabel(self,
                     font=mont30_b,
                     text="ZARZĄDZANIE ZASOBAMI MAGAZYNOWYMI",
                     text_color="#3074b2").place(x=20, y=20)
        ctk.CTkLabel(self,
                     font=mont16,
                     text="Zalogowano jako ",
                     text_color="#999999").place(x=20, y=75)

        ctk.CTkLabel(self,
                     font=mont16,
                     text=self.uzytkownik,
                     text_color="#FFFFFF").place(x=160, y=75)

        sep = ttk.Separator(self, orient="horizontal")
        sep.place(x=20, y=70, relwidth=0.965)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="NR NIP*",
                     text_color="#f3f3f3").place(x=20, y=120)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="NAZWA FIRMY*",
                     text_color="#f3f3f3").place(x=20, y=180)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="ADRES",
                     text_color="#f3f3f3").place(x=20, y=227)
        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="SIEDZIBY*",
                     text_color="#f3f3f3").place(x=20, y=249)
        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="WŁAŚCICIEL*",
                     text_color="#f3f3f3").place(x=20, y=283)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="FIRMY*",
                     text_color="#f3f3f3").place(x=20, y=305)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="NUMER",
                     text_color="#f3f3f3").place(x=20, y=347)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="TELEFONU*",
                     text_color="#f3f3f3").place(x=20, y=369)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="OPIS",
                     text_color="#f3f3f3").place(x=20, y=420)

    def stworz_wpr(self):
        self.nip_wpr = ctk.CTkEntry(self,
                                    font=mont16,
                                    text_color="white",
                                    border_color="#afafaf",
                                    width=120)
        self.nip_wpr.place(x=180, y=120)

        self.nazwa_wpr = ctk.CTkEntry(self,
                                      font=mont16,
                                      text_color="white",
                                      border_color="#afafaf",
                                      width=120)
        self.nazwa_wpr.place(x=180, y=180)

        self.adres_wpr = ctk.CTkEntry(self,
                                      font=mont16,
                                      text_color="white",
                                      border_color="#afafaf",
                                      width=120)
        self.adres_wpr.place(x=180, y=240)

        self.wlsc_wpr = ctk.CTkEntry(self,
                                     font=mont16,
                                     text_color="white",
                                     border_color="#afafaf",
                                     width=120)
        self.wlsc_wpr.place(x=180, y=300)

        self.telefon_wpr = ctk.CTkEntry(self,
                                        font=mont16,
                                        text_color="white",
                                        border_color="#afafaf",
                                        width=120)
        self.telefon_wpr.place(x=180, y=360)

        self.opis_wpr = ctk.CTkEntry(self,
                                     font=mont16,
                                     text_color="white",
                                     border_color="#afafaf",
                                     width=120)
        self.opis_wpr.place(x=180, y=420)

    def stworz_przyciski(self):

        self.dodaj_prz = ctk.CTkButton(self,
                                       text="DODAJ POZYCJE",
                                       command=self.dodaj_pozycje,
                                       font=mont16_b,
                                       width=280,
                                       text_color="#FFFFFF",
                                       fg_color="#555555",
                                       hover_color="#777777",
                                       cursor="hand2",
                                       corner_radius=5,
                                       border_spacing=7)
        self.dodaj_prz.place(x=20, y=475)

        self.wyczysc_prz = ctk.CTkButton(self,
                                         text="WYCZYŚĆ FORMULARZ",
                                         command=self.wyczysc_for_i_odznacz,
                                         font=mont16_b,
                                         width=280,
                                         text_color="#FFFFFF",
                                         fg_color="#555555",
                                         hover_color="#777777",
                                         cursor="hand2",
                                         corner_radius=5,
                                         border_spacing=7)
        self.wyczysc_prz.place(x=20, y=520)

        self.zaaktualizuj_prz = ctk.CTkButton(self,
                                              text="ZAAKTUALIZUJ",
                                              command=self.zaaktualizuj_pozycje,
                                              font=mont16_b,
                                              width=280,
                                              text_color="#FFFFFF",
                                              fg_color="#555555",
                                              hover_color="#777777",
                                              cursor="hand2",
                                              corner_radius=5,
                                              border_spacing=7)
        self.zaaktualizuj_prz.place(x=20, y=565)

        self.usun_prz = ctk.CTkButton(self,
                                      text="USUŃ POZYCJE",
                                      command=self.usun_pozycje,
                                      font=mont16_b,
                                      width=280,
                                      text_color="#FFFFFF",
                                      fg_color="#555555",
                                      hover_color="#777777",
                                      cursor="hand2",
                                      corner_radius=5,
                                      border_spacing=7)
        self.usun_prz.place(x=20, y=610)

        self.zamowienia_prz = ctk.CTkButton(self,
                                            font=mont16_b,
                                            text="ZAMÓWIENIA",
                                            command=self.szczegoly_zamowien,
                                            width=130,
                                            text_color="white",
                                            fg_color="#00417F",
                                            hover_color="#3074b2",
                                            cursor="hand2",
                                            corner_radius=5,
                                            border_spacing=7)
        self.zamowienia_prz.place(x=1345, y=120)

    def stworz_widokdanych(self):
        styl = ttk.Style(self)
        styl.theme_use("clam")
        styl.configure("Treeview",
                       font=mont10,
                       foreground="white",
                       background="#242424",
                       fieldbackground="#242424")
        styl.map("Treeview", background=[("selected", "#545454")])

        self.widok_danych_firmy = ttk.Treeview(self, height=25)
        self.widok_danych_firmy["columns"] = ("nip", "nazwa", "adres", "wlsc", "telefon", "opis", "wartosc",
                                              "zamowienia")
        self.widok_danych_firmy.place(x=325, y=120)

        for kolumna in self.widok_danych_firmy["columns"]:
            self.widok_danych_firmy.bind(f"<Button-1>", lambda e, col=kolumna: self.brak_roszerzenia_kolumn(e, col))
            self.widok_danych_firmy.heading(kolumna, text=kolumna,
                                            command=lambda _kolumna=kolumna: self.sortuj_po_kolumnie(_kolumna,
                                                                                                     False))
        for wiersz_id in self.widok_danych_firmy.get_children(""):
            for kolumna in self.widok_danych_firmy["columns"]:
                wartosc_komorki = self.widok_danych_firmy.set(wiersz_id, kolumna)
                ToolTip(self.widok_danych_firmy, item=wiersz_id, column=kolumna, text=wartosc_komorki)

        self.widok_danych_firmy.heading("nip", text="Nr NIP")
        self.widok_danych_firmy.heading("nazwa", text="Nazwa Firmy")
        self.widok_danych_firmy.heading("adres", text="Adres siedziby")
        self.widok_danych_firmy.heading("wlsc", text="Właściciel firmy")
        self.widok_danych_firmy.heading("telefon", text="Nr. telefonu")
        self.widok_danych_firmy.heading("opis", text="Opis")
        self.widok_danych_firmy.heading("wartosc", text="Łączna wartość zamówień (zł)")
        self.widok_danych_firmy.heading("zamowienia", text="Liczba zamówień")

        self.widok_danych_firmy.column("#0", width=0, stretch=tk.NO)
        self.widok_danych_firmy.column("nip", anchor=tk.CENTER, width=90)
        self.widok_danych_firmy.column("nazwa", anchor=tk.CENTER, width=120)
        self.widok_danych_firmy.column("adres", anchor=tk.CENTER, width=120)
        self.widok_danych_firmy.column("wlsc", anchor=tk.CENTER, width=120)
        self.widok_danych_firmy.column("telefon", anchor=tk.CENTER, width=120)
        self.widok_danych_firmy.column("opis", anchor=tk.CENTER, width=140)
        self.widok_danych_firmy.column("wartosc", anchor=tk.CENTER, width=170)
        self.widok_danych_firmy.column("zamowienia", anchor=tk.CENTER, width=100)
        self.widok_danych_firmy.bind("<ButtonRelease>", self.wyswietl_dane_w_for)
        self.widok_danych_firmy.bind("<Motion>", self.hover)

        self.pasekv = ttk.Scrollbar(self, orient="vertical", command=self.widok_danych_firmy.yview)
        self.pasekv.place(x=1305, y=120, height=529)
        self.widok_danych_firmy.configure(yscrollcommand=self.pasekv.set)

    def sortuj_po_kolumnie(self, kolumna, odwrotnie):
        try:
            lista_danych = [(float(self.widok_danych_firmy.set(wiersz_id, kolumna)), wiersz_id)
                            for wiersz_id in self.widok_danych_firmy.get_children("")]
        except ValueError:
            lista_danych = [(str(self.widok_danych_firmy.set(wiersz_id, kolumna)), wiersz_id)
                            for wiersz_id in self.widok_danych_firmy.get_children("")]

        lista_danych.sort(reverse=odwrotnie)

        for index, (wartosc, wiersz_id) in enumerate(lista_danych):
            self.widok_danych_firmy.move(wiersz_id, "", index)

        self.widok_danych_firmy.heading(kolumna, command=lambda: self.sortuj_po_kolumnie(kolumna, not odwrotnie))

    def odswiez_widok_danych(self):
        dane_firmy = Baza_danych.pobierz_dane_firmy()
        self.widok_danych_firmy.delete(*self.widok_danych_firmy.get_children())
        for x in dane_firmy:
            self.widok_danych_firmy.insert("", tk.END, values=x)

    def wyswietl_dane_w_for(self, event):
        wybrane_elementy = self.widok_danych_firmy.selection()
        if len(wybrane_elementy) == 1:
            wybrany_element = wybrane_elementy[0]
            wiersz = self.widok_danych_firmy.item(wybrany_element, "values")
            self.wyczysc_for()
            self.nip_wpr.insert(0, wiersz[0])
            self.nazwa_wpr.insert(0, wiersz[1])
            self.adres_wpr.insert(0, wiersz[2])
            self.wlsc_wpr.insert(0, wiersz[3])
            self.telefon_wpr.insert(0, wiersz[4])
            self.opis_wpr.insert(0, wiersz[5])

    def wyczysc_for_i_odznacz(self):
        selected = self.widok_danych_firmy.selection()
        if selected:
            for item in selected:
                self.widok_danych_firmy.selection_remove(item)
        self.wyczysc_for()

    def wyczysc_for(self):
        self.nip_wpr.delete(0, tk.END)
        self.nazwa_wpr.delete(0, tk.END)
        self.adres_wpr.delete(0, tk.END)
        self.wlsc_wpr.delete(0, tk.END)
        self.telefon_wpr.delete(0, tk.END)
        self.opis_wpr.delete(0, tk.END)

    def hover(self, event):
        region = self.widok_danych_firmy.identify("region", event.x, event.y)
        if region == "cell":
            wiersz = self.widok_danych_firmy.identify_row(event.y)
            kolumna = self.widok_danych_firmy.identify_column(event.x)
            kolumna_index = int(kolumna.replace("#", "")) - 1

            if wiersz != self.aktualny_hover_wiersza or kolumna_index != self.aktualny_hover_kolumny:
                self.aktualny_hover_wiersza = wiersz
                self.aktualny_hover_kolumny = kolumna_index
                tooltip_text = self.widok_danych_firmy.item(wiersz)["values"][kolumna_index]
                self.pokaz_tooltip(event.x_root, event.y_root, tooltip_text)
        else:
            self.ukryj_tooltip()

    def pokaz_tooltip(self, x, y, text):
        self.ukryj_tooltip()
        x_offset = 10
        y_offset = 10
        tooltip_okno = tk.Toplevel(self)
        tooltip_okno.wm_overrideredirect(True)
        tooltip_okno.wm_geometry("+%d+%d" % (x + x_offset, y + y_offset))
        label = tk.Label(tooltip_okno, text=text, background="#242424", foreground="white")
        label.pack()
        self.aktualny_tooltip = tooltip_okno

    def ukryj_tooltip(self):
        if self.aktualny_tooltip:
            self.aktualny_tooltip.destroy()
            self.aktualny_tooltip = None

    def zaaktualizuj_pozycje(self):
        wybrany_element = self.widok_danych_firmy.focus()

        if not wybrany_element:
            pokaz_komunikat("error", "Błąd", "Musisz wybrać pozycję do zaaktualizowania!")
            return

        aktualny_nip = self.widok_danych_firmy.item(wybrany_element, "values")[0]

        nip = self.nip_wpr.get().strip()
        nazwa = self.nazwa_wpr.get().strip()
        adres = self.adres_wpr.get().strip()
        wlsc = self.wlsc_wpr.get().strip()
        telefon = self.telefon_wpr.get().strip()
        opis = self.opis_wpr.get().strip()

        if not (nazwa and adres and wlsc and telefon):
            pokaz_komunikat("error", "Błąd", "Uzupełnij wszystkie wymagane pola!")
            return

        elif nip != aktualny_nip:
            pokaz_komunikat("error", "Błąd", "Nie można zmienić numeru NIP!")
            return

        Baza_danych.zaaktualizuj_pozycje_w_bazie_firmy(nazwa, adres, wlsc, telefon, opis, nip)
        Baza_danych.aktualizuj_wartosci_i_liczbe_zamowien_firmy()
        self.odswiez_widok_danych()
        pokaz_komunikat("info", "Informacja", "Pozycja została zaaktualizowana")
        self.wyczysc_for()

    def dodaj_pozycje(self):
        nip = self.nip_wpr.get().strip()
        nazwa = self.nazwa_wpr.get().strip()
        adres = self.adres_wpr.get().strip()
        wlsc = self.wlsc_wpr.get().strip()
        telefon = self.telefon_wpr.get().strip()
        opis = self.opis_wpr.get().strip()
        wartosc = 0
        zamowienia = 0

        if not (nip and nazwa and adres and wlsc and telefon):
            pokaz_komunikat("error", "Błąd", "Uzupełnij wszystkie wymagane pola!")
            return

        elif len(nip) != 10 or not nip.isdigit():
            pokaz_komunikat("error", "Błąd", "Numer NIP musi być 10-cyfrowym ciągiem znaków!")
            return

        elif Baza_danych.sprawdz_czy_istnieje_firmy(nip):
            pokaz_komunikat("error", "Błąd", "Numer NIP już istnieje!")
            return

        Baza_danych.dodaj_pozycje_do_bazy_firmy(nip, nazwa, adres, wlsc, telefon, opis, wartosc, zamowienia)
        Baza_danych.aktualizuj_wartosci_i_liczbe_zamowien_firmy()
        self.odswiez_widok_danych()
        pokaz_komunikat("info", "Informacja", "Pozycja została dodana")
        self.wyczysc_for()

    def usun_pozycje(self):
        wybrane_elementy = self.widok_danych_firmy.selection()
        liczba_us = 0
        if not wybrane_elementy:
            pokaz_komunikat("title", "Błąd", "Musisz wybrać co najmniej jedną pozycję do usunięcia!")
            return

        odpowiedz = messagebox.askquestion("Potwierdzenie", "Czy chcesz usunąć wybrane pozycje?")
        if odpowiedz == "yes":
            for element in wybrane_elementy:
                liczba_us += 1
                numer = self.widok_danych_firmy.item(element, "values")[0]
                Baza_danych.usun_pozycje_firmy(numer)
                self.widok_danych_firmy.delete(element)

            Baza_danych.aktualizuj_wartosci_i_liczbe_zamowien_firmy()
            self.odswiez_widok_danych()
            pokaz_komunikat("info", "Informacja", f"Liczba usuniętych pozycji: {liczba_us}")

    def brak_roszerzenia_kolumn(self, event, col):
        if self.widok_danych_firmy.identify_region(event.x, event.y) == "separator":
            return "break"


class SzczegolyZamowien(ctk.CTkToplevel):
    def __init__(self, parent, title, uzytkownik, nip_firmy, nazwa_firmy):
        super().__init__(parent)
        self.title(title)
        self.geometry("1580x680")
        self.resizable(True, False)
        self.uzytkownik = uzytkownik
        self.nip_firmy = nip_firmy
        self.nazwa_firmy = nazwa_firmy

        self.nazwa_wpr = None
        self.wartosc_jedn_wpr = None
        self.ilosc_wpr = None
        self.widok_danych_zamowien = None
        self.dodaj_prz = None
        self.wyczysc_prz = None
        self.zaaktualizuj_prz = None
        self.usun_prz = None
        self.cofnij_prz = None
        self.pasekv = None
        self.aktualny_hover_wiersza = None
        self.aktualny_hover_kolumny = None
        self.aktualny_tooltip = None
        self.opis_wpr = None
        self.waga_jedn_wpr = None
        self.parent = parent

        self.wycentruj_okno()
        self.stworz_interfejs()
        self.odswiez_widok_danych()
        self.parent.odswiez_widok_danych()

    def wycentruj_okno(self):
        self.update_idletasks()
        szer = self.winfo_width()
        wys = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (szer // 2)
        y = (self.winfo_screenheight() // 2) - (wys // 2)
        self.geometry(f'{szer}x{wys}+{x}+{y}')

    def stworz_interfejs(self):
        self.stworz_etykiety()
        self.stworz_wpr()
        self.stworz_przyciski()
        self.stworz_widokdanych()

    def stworz_etykiety(self):
        ctk.CTkLabel(self,
                     font=mont30_b,
                     text=f"ZAMÓWIENIA - FIRMA {self.nazwa_firmy.upper()} ",
                     text_color="#b26d30").place(x=20, y=20)
        ctk.CTkLabel(self,
                     font=mont16,
                     text="Zalogowano jako ",
                     text_color="#999999").place(x=20, y=75)

        ctk.CTkLabel(self,
                     text=self.uzytkownik,
                     font=mont16,
                     text_color="#FFFFFF").place(x=160, y=75)

        sep = ttk.Separator(self, orient="horizontal")
        sep.place(x=20, y=70, relwidth=0.965)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="TOWAR*",
                     text_color="#f3f3f3").place(x=20, y=120)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="WAGA",
                     text_color="#f3f3f3").place(x=20, y=167)
        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="JEDN. (kg)*",
                     text_color="#f3f3f3").place(x=20, y=189)
        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="WARTOŚĆ",
                     text_color="#f3f3f3").place(x=20, y=227)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="JEDN. (zł)*",
                     text_color="#f3f3f3").place(x=20, y=249)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="ILOŚĆ*",
                     text_color="#f3f3f3").place(x=20, y=299)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="OPIS",
                     text_color="#f3f3f3").place(x=20, y=359)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text="NR NIP FIRMY",
                     text_color="#f3f3f3").place(x=20, y=419)

        ctk.CTkLabel(self,
                     font=mont16_b,
                     text=self.nip_firmy,
                     text_color="#242424",
                     fg_color="grey",
                     corner_radius=6,
                     width=120).place(x=180, y=420)

    def stworz_wpr(self):
        self.nazwa_wpr = ctk.CTkEntry(self,
                                      font=mont16,
                                      text_color="white",
                                      border_color="#afafaf",
                                      width=120)
        self.nazwa_wpr.place(x=180, y=120)

        self.waga_jedn_wpr = ctk.CTkEntry(self,
                                          font=mont16,
                                          text_color="white",
                                          border_color="#afafaf",
                                          width=120)
        self.waga_jedn_wpr.place(x=180, y=180)

        self.wartosc_jedn_wpr = ctk.CTkEntry(self,
                                             font=mont16,
                                             text_color="white",
                                             border_color="#afafaf",
                                             width=120)
        self.wartosc_jedn_wpr.place(x=180, y=240)

        self.ilosc_wpr = ctk.CTkEntry(self,
                                      font=mont16,
                                      text_color="white",
                                      border_color="#afafaf",
                                      width=120)
        self.ilosc_wpr.place(x=180, y=300)

        self.opis_wpr = ctk.CTkEntry(self,
                                     font=mont16,
                                     text_color="white",
                                     border_color="#afafaf",
                                     width=120)
        self.opis_wpr.place(x=180, y=360)

    def stworz_przyciski(self):

        self.dodaj_prz = ctk.CTkButton(self,
                                       text="DODAJ POZYCJE",
                                       command=self.dodaj_pozycje,
                                       font=mont16_b,
                                       width=280,
                                       text_color="#FFFFFF",
                                       fg_color="#555555",
                                       hover_color="#777777",
                                       cursor="hand2",
                                       corner_radius=5,
                                       border_spacing=7)
        self.dodaj_prz.place(x=20, y=475)

        self.wyczysc_prz = ctk.CTkButton(self,
                                         text="WYCZYŚĆ FORMULARZ",
                                         command=self.wyczysc_for_i_odznacz,
                                         font=mont16_b,
                                         width=280,
                                         text_color="#FFFFFF",
                                         fg_color="#555555",
                                         hover_color="#777777",
                                         cursor="hand2",
                                         corner_radius=5,
                                         border_spacing=7)
        self.wyczysc_prz.place(x=20, y=520)

        self.zaaktualizuj_prz = ctk.CTkButton(self,
                                              text="ZAAKTUALIZUJ",
                                              command=self.zaaktualizuj_pozycje,
                                              font=mont16_b,
                                              width=280,
                                              text_color="#FFFFFF",
                                              fg_color="#555555",
                                              hover_color="#777777",
                                              cursor="hand2",
                                              corner_radius=5,
                                              border_spacing=7)
        self.zaaktualizuj_prz.place(x=20, y=565)

        self.usun_prz = ctk.CTkButton(self,
                                      text="USUŃ POZYCJE",
                                      command=self.usun_pozycje,
                                      font=mont16_b,
                                      width=280,
                                      text_color="#FFFFFF",
                                      fg_color="#555555",
                                      hover_color="#777777",
                                      cursor="hand2",
                                      corner_radius=5,
                                      border_spacing=7)
        self.usun_prz.place(x=20, y=610)

        self.cofnij_prz = ctk.CTkButton(self,
                                        font=mont16_b,
                                        text="COFNIJ",
                                        command=self.zakmniecie_okna,
                                        width=130,
                                        text_color="white",
                                        fg_color="#7F3A00",
                                        hover_color="#B26D30",
                                        cursor="hand2",
                                        corner_radius=5,
                                        border_spacing=7)
        self.cofnij_prz.place(x=1410, y=120)

    def stworz_widokdanych(self):
        styl = ttk.Style(self)
        styl.theme_use("clam")
        styl.configure("Treeview",
                       font=mont10,
                       foreground="white",
                       background="#242424",
                       fieldbackground="#242424")
        styl.map("Treeview", background=[("selected", "#545454")])

        self.widok_danych_zamowien = ttk.Treeview(self, height=25)
        self.widok_danych_zamowien["columns"] = (
            "id", "nazwa", "waga_jedn", "wart_jedn", "ilosc", "opis", "waga_calk", "wartosc_calk", "dodane_przez",
            "data_dodania", "nip_firmy")
        self.widok_danych_zamowien.place(x=325, y=120)

        for kolumna in self.widok_danych_zamowien["columns"]:
            self.widok_danych_zamowien.bind(f"<Button-1>", lambda e, col=kolumna: self.brak_roszerzenia_kolumn(e, col))
            self.widok_danych_zamowien.heading(kolumna, text=kolumna,
                                               command=lambda _kolumna=kolumna: self.sortuj_po_kolumnie(_kolumna,
                                                                                                        False))
        for wiersz_id in self.widok_danych_zamowien.get_children(""):
            for kolumna in self.widok_danych_zamowien["columns"]:
                wartosc_komorki = self.widok_danych_zamowien.set(wiersz_id, kolumna)
                ToolTip(self.widok_danych_zamowien, item=wiersz_id, column=kolumna, text=wartosc_komorki)

        self.widok_danych_zamowien.heading("nazwa", text="Towar")
        self.widok_danych_zamowien.heading("waga_jedn", text="Waga jedn. (kg)")
        self.widok_danych_zamowien.heading("wart_jedn", text="Wartość jedn. (zł)")
        self.widok_danych_zamowien.heading("ilosc", text="Ilość")
        self.widok_danych_zamowien.heading("opis", text="Opis")
        self.widok_danych_zamowien.heading("waga_calk", text="Całk. waga (kg)")
        self.widok_danych_zamowien.heading("wartosc_calk", text="Całk. wartość (zł)")
        self.widok_danych_zamowien.heading("dodane_przez", text="Dodane przez")
        self.widok_danych_zamowien.heading("data_dodania", text="Data dodania")

        self.widok_danych_zamowien.column("#0", width=0, stretch=tk.NO)
        self.widok_danych_zamowien.column("id", width=0, stretch=tk.NO)
        self.widok_danych_zamowien.column("nip_firmy", width=0, stretch=tk.NO)
        self.widok_danych_zamowien.column("nazwa", anchor=tk.CENTER, width=80)
        self.widok_danych_zamowien.column("waga_jedn", anchor=tk.CENTER, width=120)
        self.widok_danych_zamowien.column("wart_jedn", anchor=tk.CENTER, width=120)
        self.widok_danych_zamowien.column("ilosc", anchor=tk.CENTER, width=80)
        self.widok_danych_zamowien.column("opis", anchor=tk.CENTER, width=130)
        self.widok_danych_zamowien.column("waga_calk", anchor=tk.CENTER, width=130)
        self.widok_danych_zamowien.column("wartosc_calk", anchor=tk.CENTER, width=130)
        self.widok_danych_zamowien.column("dodane_przez", anchor=tk.CENTER, width=120)
        self.widok_danych_zamowien.column("data_dodania", anchor=tk.CENTER, width=140)
        self.widok_danych_zamowien.bind("<ButtonRelease>", self.wyswietl_dane_w_for)
        self.widok_danych_zamowien.bind("<Motion>", self.hover)

        self.pasekv = ttk.Scrollbar(self, orient="vertical", command=self.widok_danych_zamowien.yview)
        self.pasekv.place(x=1370, y=120, height=529)
        self.widok_danych_zamowien.configure(yscrollcommand=self.pasekv.set)

    def sortuj_po_kolumnie(self, kolumna, odwrotnie):
        try:
            lista_danych = [(float(self.widok_danych_zamowien.set(wiersz_id, kolumna)), wiersz_id)
                            for wiersz_id in self.widok_danych_zamowien.get_children("")]
        except ValueError:
            lista_danych = [(str(self.widok_danych_zamowien.set(wiersz_id, kolumna)), wiersz_id)
                            for wiersz_id in self.widok_danych_zamowien.get_children("")]

        lista_danych.sort(reverse=odwrotnie)

        for index, (wartosc, wiersz_id) in enumerate(lista_danych):
            self.widok_danych_zamowien.move(wiersz_id, '', index)

        self.widok_danych_zamowien.heading(kolumna, command=lambda: self.sortuj_po_kolumnie(kolumna, not odwrotnie))

    def odswiez_widok_danych(self):
        stan_zamowien = Baza_danych.pobierz_szczegoly_zamowien(self.nip_firmy)
        self.widok_danych_zamowien.delete(*self.widok_danych_zamowien.get_children())
        for x in stan_zamowien:
            self.widok_danych_zamowien.insert("", tk.END, values=x)

    def wyswietl_dane_w_for(self, event):
        wybrane_elementy = self.widok_danych_zamowien.selection()
        if len(wybrane_elementy) == 1:
            wybrany_element = wybrane_elementy[0]
            wiersz = self.widok_danych_zamowien.item(wybrany_element, "values")
            self.wyczysc_for()
            self.nazwa_wpr.insert(0, wiersz[1])
            self.waga_jedn_wpr.insert(0, wiersz[2])
            self.wartosc_jedn_wpr.insert(0, wiersz[3])
            self.ilosc_wpr.insert(0, wiersz[4])
            self.opis_wpr.insert(0, wiersz[5])

    def wyczysc_for_i_odznacz(self):
        selected = self.widok_danych_zamowien.selection()
        if selected:
            for item in selected:
                self.widok_danych_zamowien.selection_remove(item)
        self.wyczysc_for()

    def wyczysc_for(self):
        self.nazwa_wpr.delete(0, tk.END)
        self.waga_jedn_wpr.delete(0, tk.END)
        self.wartosc_jedn_wpr.delete(0, tk.END)
        self.ilosc_wpr.delete(0, tk.END)
        self.opis_wpr.delete(0, tk.END)

    def hover(self, event):
        region = self.widok_danych_zamowien.identify("region", event.x, event.y)
        if region == "cell":
            wiersz = self.widok_danych_zamowien.identify_row(event.y)
            kolumna = self.widok_danych_zamowien.identify_column(event.x)
            kolumna_index = int(kolumna.replace("#", "")) - 1

            if wiersz != self.aktualny_hover_wiersza or kolumna_index != self.aktualny_hover_kolumny:
                self.aktualny_hover_wiersza = wiersz
                self.aktualny_hover_kolumny = kolumna_index
                tooltip_text = self.widok_danych_zamowien.item(wiersz)["values"][kolumna_index]
                self.pokaz_tooltip(event.x_root, event.y_root, tooltip_text)
        else:
            self.ukryj_tooltip()

    def pokaz_tooltip(self, x, y, text):
        self.ukryj_tooltip()
        x_offset = 10
        y_offset = 10
        tooltip_okno = tk.Toplevel(self)
        tooltip_okno.wm_overrideredirect(True)
        tooltip_okno.wm_geometry("+%d+%d" % (x + x_offset, y + y_offset))
        label = tk.Label(tooltip_okno, text=text, background="#242424", foreground="white")
        label.pack()
        self.aktualny_tooltip = tooltip_okno

    def ukryj_tooltip(self):
        if self.aktualny_tooltip:
            self.aktualny_tooltip.destroy()
            self.aktualny_tooltip = None

    def zaaktualizuj_pozycje(self):
        wybrany_element = self.widok_danych_zamowien.focus()

        if not wybrany_element:
            pokaz_komunikat("error", "Błąd", "Musisz wybrać pozycję do zaaktualizowania!")
            return

        wiersz = self.widok_danych_zamowien.item(wybrany_element, "values")
        id_szczegolu = wiersz[0]

        nazwa = self.nazwa_wpr.get().strip()
        waga_jedn = self.waga_jedn_wpr.get().strip()
        wartosc_jedn = self.wartosc_jedn_wpr.get().strip()
        ilosc = self.ilosc_wpr.get().strip()
        opis = self.opis_wpr.get().strip()

        if not (nazwa and waga_jedn and wartosc_jedn and ilosc):
            pokaz_komunikat("error", "Błąd", "Uzupełnij wszystkie wymagane pola!")
            return

        try:
            ilosc = int(ilosc)
            waga_jedn = float(waga_jedn)
            wartosc_jedn = float(wartosc_jedn)
        except ValueError:
            pokaz_komunikat("error", "Błąd",
                            "Waga i wartość muszą być liczbą zmiennoprzecinkową, a ilość całkowitą.")
            return

        Baza_danych.aktualizuj_szczegol_zamowienia(nazwa, waga_jedn, wartosc_jedn, ilosc, opis, id_szczegolu)
        Baza_danych.aktualizuj_wartosci_i_liczbe_zamowien_firmy()
        self.parent.odswiez_widok_danych()
        self.odswiez_widok_danych()
        pokaz_komunikat("info", "Informacja", "Pozycja została zaaktualizowana")
        self.wyczysc_for()

    def dodaj_pozycje(self):
        nazwa = self.nazwa_wpr.get().strip()
        waga_jedn = self.waga_jedn_wpr.get().strip()
        wartosc_jedn = self.wartosc_jedn_wpr.get().strip()
        ilosc = self.ilosc_wpr.get().strip()
        opis = self.opis_wpr.get().strip()

        if not (nazwa and waga_jedn and wartosc_jedn and ilosc):
            pokaz_komunikat("error", "Błąd", "Uzupełnij wszystkie wymagane pola!")
            return

        try:
            ilosc = float(ilosc)
            waga_jedn = float(waga_jedn)
            wartosc_jedn = float(wartosc_jedn)
        except ValueError:
            pokaz_komunikat("error", "Błąd",
                            "Waga i wartość muszą być liczbą zmiennoprzecinkową, a ilość całkowitą")
            return

        nip_firmy = self.nip_firmy

        Baza_danych.dodaj_szczegol_zamowienia(nazwa, waga_jedn, wartosc_jedn, ilosc, opis, self.uzytkownik,
                                              self.nip_firmy)
        Baza_danych.aktualizuj_wartosci_i_liczbe_zamowien_firmy()
        self.odswiez_widok_danych()
        self.parent.odswiez_widok_danych()
        pokaz_komunikat("info", "Informacja", "Pozycja została dodana")
        self.wyczysc_for()

    def usun_pozycje(self):
        wybrane_elementy = self.widok_danych_zamowien.selection()
        liczba_us = 0
        if not wybrane_elementy:
            pokaz_komunikat("error", "Błąd", "Musisz wybrać co najmniej jedną pozycję do usunięcia!")
            return

        odpowiedz = pokaz_komunikat("question", "Potwierdzenie", "Czy chcesz usunąć wybrane pozycje?")
        if odpowiedz == "yes":
            for element in wybrane_elementy:
                liczba_us += 1
                numer = self.widok_danych_zamowien.item(element, "values")[0]
                Baza_danych.usun_szczegol_zamowienia(numer)
                self.widok_danych_zamowien.delete(element)

            Baza_danych.aktualizuj_wartosci_i_liczbe_zamowien_firmy()
            self.odswiez_widok_danych()
            self.parent.odswiez_widok_danych()
            pokaz_komunikat("info", "Informacja", f"Liczba usuniętych pozycji: {liczba_us}")

    def zakmniecie_okna(self):
        self.destroy()

    def brak_roszerzenia_kolumn(self, event, col):
        if self.widok_danych_zamowien.identify_region(event.x, event.y) == "separator":
            return "break"


if __name__ == "__main__":
    app = GlownyInterfejs()
    app.mainloop()
