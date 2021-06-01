# Projekt SPG - Solitaire
Na tento projekt vytvoríme pythonovú implementáciu hry solitaire. Pre túto hru sme sa rozhodli, pretože má jednoduché pravidlá, množstvo rôznych variácií, a možnosti na využitie objektovo orientovaného programovania.

## Ciele implementácie
Do termínu odovzdania chceme stihnúť nasledujúce veci:
- <b>Funkčnú hru.</b><br>
Malo by byť možné začať a ukončiť hru podľa pravidiel.
- <b>Ukladanie hier.</b><br>
Bude možné hranú hru uložiť a načítať. Teda sa dá hrať tá istá hra aj pri viacerých otvoreniach programu.
- <b>Hlavné menu.</b><br>
Menu by malo umožniť výber vytvorenia novej hry, načítania už začatej hry, a prípadne výberu varianty solitairu (ak budú implementované).
- <b>Grafický Interface.</b><br>
Hrajúca osoba by mala byť schopná vidieť stav hry vo vizuálnej podobe. Tiež by sa s hrou malo dať interagovať pohodlným spôsobom.

## Spôsob implementácie
- Je vytvorený class `Game`. Objekt tohoto typu ukladá všetky pozície kariet. Okrem toho má priradený vlastný objekt typu `Drawer`, ktorý je zodpovedný za vykreslovanie kariet a interakciu s užívateľom.
- Objekt typu `Game` ukladá karty do objektov typu `Stack` -- karty sa nachádzajú v kôpkach, teda táto dátová štruktúra je ideálna.
- Karty sú objekty typu `Card`. Tento objekt ukladá základné vlastnosti kariet -- ich hodnotu a farbu, a či sú odkryté alebo nie.
- Okrem toho existujú nasledujúce classes, ktoré riešia pozíciu kariet na hracej ploche:
  - `TableauCard`, pokiaľ je karta na hlavnej časti plochy,
  - `FoundationCard`, pokial je karta na kôpkach jedej farby,
  - `WasteCard`, pokiaľ je karta na odkrytej kôpke doberacieho balíčku,
  - `DeckCard`, pokiaľ je karta na zakrytej kôpke doberacieho balíčku.
- Všetky tieto classes inheritujú classu `Card`.
