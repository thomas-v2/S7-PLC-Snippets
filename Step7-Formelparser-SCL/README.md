# Step7-Formelparser-SCL

Dies ist ein Codebeispiel für einen einfachen Formelparser und Interpreter für arithmetische
Ausdrücke, geschrieben in SCL für Step7. Der Parser ist in Anlehnung an die Umsetzung aus dem Buch
Compilerbau von N. Wirth erstellt, welcher durch rekursiven Abstieg einen Ausdruck in Code für die
Stackmaschine übersetzt.
Er verarbeitet Formeln mit Integer-Zahlen und den 4 Variablen a, b, c und d. Die Variablen können
als Parameter am Interpreter-Baustein eingetragen werden, und die aktuellen Werte werden bei
Abarbeitung an entsprechender Stelle eingesetzt.

## Grammatik in EBNF
Der Parser unterstützt die folgende Grammatik:
```
expression = ["+" | "-"] term { ( "+" | "-" ) term }.
term = factor { ( "*" | "/" ) factor }.
factor = ident | number | "(" expression ")".
ident = "a" | "b" | "c" | "d" | "A" | "B" | "C" | "D".
number = digit { digit }.
digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9".
```

## Parser Fehlercodes

Die Funktion *parser* gibt an den Ausgängen *error* und *meldung* Fehlermeldungen aus,
die beim Parsen des Ausdrucks entstehen könnten:
- 1 = Fehlerhafter Integer Wert (>32767 oder <-32767 (nicht -32768!)
- 2 = Fehlerhafter Integer Wert (mehr als 5 Stellen)
- 3 = Schließende Klammer fehlt
- 4 = Syntax Fehler
- 5 = Unvollständiger Ausdruck

## Stackmaschine
Die Stackmaschine kennt 3 Befehle:
- LIT: Eine Zahlkonstante (Literal) auf dem Stapel ablegen (Zahlenwert in val).
- OPR: Operand. Der Operandentyp (+-*/) liegt in val. Die Operation wird mit den beiden
oberen Werten vom Stapel durchgeführt, und das Ergebnis auf dem Stapel angelegt.
- LOD: Legt einen Variablenwert (a, b, c oder d) auf dem Stapel ab.

## Umgehung der Rekursionsbeschränkung im SCL Compiler
Wegen des rekursiven Aufrufs von Funktionen gibt es Probleme beim Übersetzen des Codes für
den Parser aufgrund der folgenden Abhängigkeiten:

*term*: ruft *factor* auf<br>
*expression*: ruft *term* auf<br>
*factor*: ruft *expression* auf<br>

Es gibt zwei Möglichkeiten um den Code fehlerfrei zu übersetzen:
1. Es muss ein Funktionsaufruf beim ersten Übersetzungsvorgang auskommentiert werden,
z.B. *expression* in der Funktion *factor*
2. Leere Funktionsrümpfe erstellen, damit die Funktionsparameter bekannt sind. Die
Funktionen werden dann im weiteren Übersetzungsvorgang durch die mit dem vollständigen Code
ersetzt.

Unter den Übersetzungseinstellungen im SCL-Compiler lässt sich aktivieren, dass
Bausteinnummern automatisch erzeugt werden sollen. Ist das nicht aktiviert, so müssen die
Symbole vorher manuell in der Symboltabelle mit einer Nummer versehen werden.
Damit es bei automatischer Nummerierung zu keinen Konflikten mit den automatisch eingefügten
IEC-Bausteinen kommt, muss das Symbol CONCAT mit der Adresse FC2 angelegt werden. Ist das
vorbereitet, wird mit Übersetzen der Übersetzungssteuerdatei (*makefile.scl*) das vollständige Programm fehlerfrei
erzeugt (es lassen sich leider nicht die automatisch vergebenen Bausteinnummern einstellen).
Im Testprogramm muss die Formel im Datenbaustein-Variable „dbtest“.formel vom Typ String
eingegeben werden.
Beispiele:
```
2*(a+654)
40-d+3*a
(a+b)*(c+d)
100/2
```

## Probleme und Beschränkungen
- Es kann keine negative Zahl -32768 eingegeben werden, da das Minus als Negation erfasst wird
und die STRING_TO_INT Funktion im positiven Bereich nur Werte bis 32767 zulässt.
- Eine 300er CPU lässt eine maximale Schachtelungstiefe von 16 zu. Ein Ausdruck ohne Klammern
benötigt 5 Schachtelungen. Für jede Klammerebene kommen 3 Schachtelungen hinzu.
In der tiefsten Schachtelungsebene wird immer noch eine Unterfunktion (sym, get, string_i)
aufgerufen. Die Tiefe wird momentan nicht abgefragt, schlimmstenfalls geht die CPU in Stop.

## Authors

* **Thomas Wiens** - *Initial work (2011)* - [thomas-v2](https://github.com/thomas-v2)
