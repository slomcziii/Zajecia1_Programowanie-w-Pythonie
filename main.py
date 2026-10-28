import requests


class DownloadError(Exception):
    """Podstawowy wyjątek związany z pobieraniem pliku."""
    pass


class NotFoundError(DownloadError):
    """Nie znaleziono pliku — HTTP 404."""
    pass


class AccessDeniedError(DownloadError):
    """Brak dostępu do pliku — HTTP 403."""
    pass


def pobierz_plik(url, nazwa_pliku="latest.txt"):
    odpowiedz = requests.get(url, timeout=30)

    if odpowiedz.status_code == 404:
        raise NotFoundError(f"Nie znaleziono pliku: {url}")

    if odpowiedz.status_code == 403:
        raise AccessDeniedError(f"Brak dostępu do pliku: {url}")

    odpowiedz.raise_for_status()

    with open(nazwa_pliku, "wb") as plik:
        plik.write(odpowiedz.content)

    print(f"Zapisano plik: {nazwa_pliku}")


if __name__ == "__main__":
    url = "http://oleksandr-fedoruk.com/sggw/podyplomowe/403"

    try:
        pobierz_plik(url, "moj_plik.txt")
    except NotFoundError as blad:
        print(f"Błąd 404: {blad}")
    except AccessDeniedError as blad:
        print(f"Błąd 403: {blad}")
    except requests.exceptions.RequestException as blad:
        print(f"Błąd żądania HTTP: {blad}")
    except OSError as blad:
        print(f"Błąd zapisu pliku: {blad}")