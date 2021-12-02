# -*- coding: utf-8 -*-
#
# Dieses Programm dient dazu, ein AWL-Programm
# in Lade/Tranfersequenzen zu übersetzen, um es
# im Temp-Bereich abzulegen.
# Ziel ist ein Quine-Programm.

awl_fobj = open("quine-generator.awl")
awl = ""
for line in awl_fobj:
    line = line.lstrip().rstrip()    # Alle Leerzeichen am Anfang und Ende entfernen
    # Alle sonstigen doppelten Leerzeichen entfernen
    while '  ' in line:
        line = line.replace('  ', ' ')
    awl = awl + line + "\n"
awl_fobj.close()

i = 0
outawl = ""
while i < len(awl):
    outawl += "L '"
    # in 4er Blöcke zum Laden/Transferieren zerlegen. Das Programm muss mit einem
    # gefüllten 4er Block enden. Ggf. Sprunglabels verlängern.
    for j in range(4):      
        if i + j >= len(awl):
            break
        s = awl[i + j]
        # Zeichen escapen
        s = s.replace("'", "$'")
        s = s.replace("\n", "$R")
        outawl += s
    outawl += "'\n"
    outawl += "T LD " + str(i) + "\n"
    i = i + 4

print (outawl)

