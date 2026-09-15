#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generuje statyczne pliki .ics dla zajec (kazdy poniedzialek, 17:00-17:50).

Po co statyczne pliki, a nie generowanie w przegladarce:
iOS Safari blokuje nawigacje do data: URI, a Blob z atrybutem download
ladnie ladzie w Plikach zamiast otworzyc sie w Kalendarzu. Prawdziwy plik
serwowany przez https z naglowkiem text/calendar otwiera sie na iPhonie
wprost w aplikacji Kalendarz.

Uzycie:  python3 build-ics.py
Odpalic ponownie, gdy skoncza sie wygenerowane terminy (patrz DO kolo konca).
"""
import datetime, io, os, pathlib

OD = datetime.date(2026, 9, 7)    # pierwszy poniedzialek zajec
DO = datetime.date(2028, 12, 31)  # generujemy z duzym zapasem
OUT = pathlib.Path(__file__).parent / "cal"

TYTUL = "Joga vinyasa z Jagodą"
MIEJSCE = "Kangur Gym, al. Solidarności 14, Wieruszów"
OPIS = "Zajęcia jogi vinyasa, poziom otwarty, 50 minut."
URL = "https://byjagoda.github.io"

SZABLON = """BEGIN:VCALENDAR\r
VERSION:2.0\r
PRODID:-//by Jagoda//joga//PL\r
CALSCALE:GREGORIAN\r
METHOD:PUBLISH\r
BEGIN:VTIMEZONE\r
TZID:Europe/Warsaw\r
BEGIN:STANDARD\r
DTSTART:19701025T030000\r
TZOFFSETFROM:+0200\r
TZOFFSETTO:+0100\r
TZNAME:CET\r
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU\r
END:STANDARD\r
BEGIN:DAYLIGHT\r
DTSTART:19700329T020000\r
TZOFFSETFROM:+0100\r
TZOFFSETTO:+0200\r
TZNAME:CEST\r
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU\r
END:DAYLIGHT\r
END:VTIMEZONE\r
BEGIN:VEVENT\r
UID:{d}-joga@byjagoda.github.io\r
DTSTAMP:{stamp}\r
DTSTART;TZID=Europe/Warsaw:{d}T170000\r
DTEND;TZID=Europe/Warsaw:{d}T175000\r
SUMMARY:{tytul}\r
LOCATION:{miejsce}\r
DESCRIPTION:{opis}\r
URL:{url}\r
BEGIN:VALARM\r
TRIGGER:-PT2H\r
ACTION:DISPLAY\r
DESCRIPTION:Joga za 2 godziny\r
END:VALARM\r
END:VEVENT\r
END:VCALENDAR\r
"""

def esc(t):
    # RFC 5545: przecinek, srednik i backslash trzeba eskejpowac
    return t.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;")

def main():
    OUT.mkdir(exist_ok=True)
    stamp = datetime.datetime(2026, 9, 15, 12, 0, 0).strftime("%Y%m%dT%H%M%SZ")
    d = OD
    while d.weekday() != 0:
        d += datetime.timedelta(days=1)
    n = 0
    while d <= DO:
        key = d.strftime("%Y%m%d")
        tresc = SZABLON.format(d=key, stamp=stamp, tytul=esc(TYTUL),
                               miejsce=esc(MIEJSCE), opis=esc(OPIS), url=URL)
        io.open(OUT / ("joga-%s.ics" % key), "w", encoding="utf-8", newline="").write(tresc)
        n += 1
        d += datetime.timedelta(days=7)
    print("Wygenerowano %d plikow w %s (do %s)" % (n, OUT, DO))

if __name__ == "__main__":
    main()
