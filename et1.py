import functools
import time
from datetime import datetime


def loguj_czas(funkcja):
    """Dekorator wypisujący czas przed i po wywołaniu funkcji."""

    @functools.wraps(funkcja)
    def opakowanie(*args, **kwargs):
        start = time.perf_counter()
        print(f"[{datetime.now():%H:%M:%S}] Start: {funkcja.__name__}")

        wynik = funkcja(*args, **kwargs)

        czas = time.perf_counter() - start
        print(
            f"[{datetime.now():%H:%M:%S}] Koniec: {funkcja.__name__} "
            f"(trwało {czas:.3f} s)"
        )
        return wynik

    return opakowanie


class ETL:
    def __init__(self, nazwa_pliku):
        self.nazwa_pliku = nazwa_pliku

    def wczytaj(self):
        
        with open(self.nazwa_pliku, encoding="utf-8-sig") as plik:
            for linia in plik:
                linia = linia.strip()

                
                if not linia:
                    continue

                
                wiersz = [pole.strip() for pole in linia.split(",")]

                if len(wiersz) != 8:
                    raise ValueError(
                        f"Oczekiwano 8 kolumn, otrzymano {len(wiersz)}."
                    )

                yield wiersz

    def przeksztalc(self, wiersze):
        for wiersz in wiersze:
            numer = int(wiersz[0])

            
            liczby = [
                float(pole)
                for pole in wiersz[1:]
                if pole != "-"
            ]

            
            braki = [
                indeks
                for indeks, pole in enumerate(wiersz[1:], start=1)
                if pole == "-"
            ]

            suma = sum(liczby)

            if liczby:
                srednia = suma / len(liczby)
            else:
                srednia = None

            yield numer, suma, srednia, braki

    def zapisz(self, wyniki):
        with (
            open("values.csv", "w", encoding="utf-8") as wartosci,
            open("missing_values.csv", "w", encoding="utf-8") as braki,
        ):
            wartosci.write("numer,suma,srednia\n")
            braki.write("numer,indeksy_brakow\n")

            for numer, suma, srednia, indeksy in wyniki:
                if srednia is None:
                    srednia_tekst = ""
                else:
                    srednia_tekst = f"{srednia:.6f}"

                wartosci.write(
                    f"{numer},{suma:.6f},{srednia_tekst}\n"
                )

                indeksy_tekst = ";".join(str(i) for i in indeksy)
                braki.write(f"{numer},{indeksy_tekst}\n")

        print("Utworzono values.csv oraz missing_values.csv")

    @loguj_czas
    def uruchom(self):
        wiersze = self.wczytaj()
        wyniki = self.przeksztalc(wiersze)
        self.zapisz(wyniki)


if __name__ == "__main__":
    try:
        proces = ETL("moj_plik.txt")
        proces.uruchom()
    except ValueError as blad:
        print(f"Błąd danych: {blad}")
    except OSError as blad:
        print(f"Błąd odczytu lub zapisu pliku: {blad}")