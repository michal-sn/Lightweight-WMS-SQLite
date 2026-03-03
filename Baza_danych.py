import sqlite3


def stworz_tabele():
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Firmy (
            nip TEXT PRIMARY KEY NOT NULL,
            nazwa TEXT NOT NULL,
            adres TEXT NOT NULL,
            wlsc TEXT NOT NULL,
            telefon TEXT NOT NULL,
            opis TEXT,
            wartosc REAL,
            zamowienia INT)""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Szczegoly_Zamowien (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT NOT NULL,
            waga_jedn REAL NOT NULL,
            wartosc_jedn REAL NOT NULL,
            ilosc INT NOT NULL,
            opis TEXT,
            waga_calk REAL,
            wartosc_calk REAL,
            dodane_przez TEXT,
            data_dodania DATETIME DEFAULT (datetime('now','localtime')),
            nip_firmy TEXT,
            FOREIGN KEY (nip_firmy) REFERENCES Firmy (nip) ON DELETE CASCADE)""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Uzytkownicy (
            login TEXT PRIMARY KEY NOT NULL,
            haslo TEXT NOT NULL)""")
    c.commit()
    c.close()


def pobierz_nazwe_uzytkownika(login):
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()
    cursor.execute("SELECT login FROM Uzytkownicy WHERE login=?", (login,))
    dane = cursor.fetchall()
    c.close()
    return dane


def pobierz_haslo_uzytkownika(login):
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()
    cursor.execute("SELECT haslo FROM Uzytkownicy WHERE login=?", (login,))
    dane = cursor.fetchall()
    c.close()
    return dane


def zarejestruj_uzytkownika(login, haslo_hash):
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()
    cursor.execute("INSERT INTO Uzytkownicy VALUES (?,?)", (login, haslo_hash))
    c.commit()
    c.close()


def pobierz_dane_firmy():
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()
    cursor.execute("SELECT nip, nazwa, adres, wlsc, telefon, opis, wartosc, zamowienia FROM Firmy")
    dane = cursor.fetchall()
    c.close()
    return dane


def dodaj_pozycje_do_bazy_firmy(nip, nazwa, adres, wlsc, telefon, opis, wartosc, zamowienia):
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()

    cursor.execute("""
        INSERT INTO Firmy (nip, nazwa, adres, wlsc, telefon, opis, wartosc, zamowienia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                   (nip, nazwa, adres, wlsc, telefon, opis, wartosc, zamowienia))

    c.commit()
    c.close()


def usun_pozycje_firmy(numer):
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("DELETE FROM Firmy WHERE nip = ?", (numer,))
    c.commit()
    c.close()


def zaaktualizuj_pozycje_w_bazie_firmy(nowa_nazwa, nowy_adres, nowy_wlsc, nowy_telefon, nowy_opis, nip):
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()
    cursor.execute("UPDATE Firmy SET nazwa = ?, adres = ?, wlsc = ?, telefon = ?, opis = ? WHERE nip = ?",
                   (nowa_nazwa, nowy_adres, nowy_wlsc, nowy_telefon, nowy_opis, nip))
    c.commit()
    c.close()


def aktualizuj_wartosci_i_liczbe_zamowien_firmy():
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()

    zapytanie_wartosc = """
    UPDATE Firmy SET wartosc = (
        SELECT COALESCE(SUM(wartosc_calk), 0) FROM Szczegoly_Zamowien
        WHERE Szczegoly_Zamowien.nip_firmy = Firmy.nip
    )
    """
    cursor.execute(zapytanie_wartosc)

    zapytanie_zamowienia = """
    UPDATE Firmy SET zamowienia = (
        SELECT COUNT(*) FROM Szczegoly_Zamowien
        WHERE Szczegoly_Zamowien.nip_firmy = Firmy.nip
    )
    """
    cursor.execute(zapytanie_zamowienia)

    c.commit()
    c.close()


def sprawdz_czy_istnieje_firmy(numer):
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()
    cursor.execute("SELECT COUNT (*) FROM Firmy WHERE nip = ?",
                   (numer,))
    wynik = cursor.fetchone()
    c.close()
    return wynik[0] > 0


def pobierz_szczegoly_zamowien(nip_firmy):
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()
    cursor.execute("""
        SELECT id, nazwa, waga_jedn, wartosc_jedn, ilosc, opis,
        (waga_jedn * ilosc) as waga_calk,
        (wartosc_jedn * ilosc) as wartosc_calk,
        dodane_przez, data_dodania
        FROM Szczegoly_Zamowien WHERE nip_firmy = ?""", (nip_firmy,))
    dane = cursor.fetchall()
    c.close()
    return dane


def dodaj_szczegol_zamowienia(nazwa, waga_jedn, wartosc_jedn, ilosc, opis, dodane_przez, nip_firmy):
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()

    waga_calk = waga_jedn * ilosc
    wartosc_calk = wartosc_jedn * ilosc

    cursor.execute("""INSERT INTO Szczegoly_Zamowien (nazwa, waga_jedn, wartosc_jedn, ilosc, opis, waga_calk, 
    wartosc_calk, dodane_przez, nip_firmy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (nazwa, waga_jedn, wartosc_jedn, ilosc, opis, waga_calk, wartosc_calk, dodane_przez, nip_firmy))

    c.commit()
    c.close()


def usun_szczegol_zamowienia(id_szczegolu):
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()
    cursor.execute("DELETE FROM Szczegoly_Zamowien WHERE id = ?", (id_szczegolu,))
    c.commit()
    c.close()


def aktualizuj_szczegol_zamowienia(nowa_nazwa, nowa_waga_jedn, nowa_wartosc_jedn, nowa_ilosc, nowy_opis, id_szczegolu):
    c = sqlite3.connect("Baza_danych.db")
    cursor = c.cursor()

    nowa_waga_calk = nowa_waga_jedn * nowa_ilosc
    nowa_wartosc_calk = nowa_wartosc_jedn * nowa_ilosc

    cursor.execute("""
        UPDATE Szczegoly_Zamowien
        SET nazwa = ?, waga_jedn = ?, wartosc_jedn = ?, ilosc = ?, opis=?, waga_calk = ?, wartosc_calk = ? 
        WHERE id = ?""",
                   (nowa_nazwa, nowa_waga_jedn, nowa_wartosc_jedn, nowa_ilosc, nowy_opis, nowa_waga_calk,
                    nowa_wartosc_calk, id_szczegolu))

    c.commit()
    c.close()


stworz_tabele()
