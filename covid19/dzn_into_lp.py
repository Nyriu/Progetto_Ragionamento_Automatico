# Convertitore da input .dzn nell'equivalente .lp
#Da formato .dzn
"""
K=3;
H=2;
M=2;
P=6;
O=3;
Q=8;
"""
#A formato .lp
"""
corridoi(        3).
stanze_per_lato( 2).

malato(1..       2).
positivo(1..     6).
osservazione(1.. 3).
quarantena(1..   8).
"""

import os

def dzn_to_lp(filename, dzn_dir, lp_dir):
    dzn_fpath = dzn_dir + filename
    content = open(dzn_fpath).read()
    content = content.replace("\n", "")
    content = content.replace(" ", "")

    assegn = content.split(";")
    assegn = [ x.split("=") for x in assegn if not x == "" ]
    key_values = { x[0]:x[1] for x in assegn }

    lp_enc = ""
    for k in key_values.keys():
        if int(key_values[k]) != 0:
            lp_enc += dzn_ids_to_lp[k]
            lp_enc += key_values[k]
            lp_enc += ").\n"

    os.makedirs(lp_dir, exist_ok=True)
    lp_fpath = lp_dir + filename.replace(dzn_ext, lp_ext)
    open(lp_fpath, "w+").write(lp_enc)








dzn_ids_to_lp = {
        "K":"corridoi(       ",# 3).
        "H":"stanze_per_lato(",# 2).
        "M":"malato(1..      ",# 2).
        "P":"positivo(1..    ",# 6).
        "O":"osservazione(1..",# 3).
        "Q":"quarantena(1..  " # 8).
        }








file_prefix = "input_"

dzn_ext = ".dzn"
lp_ext  = ".lp"

dzn_dir = "./inputs/"
lp_dir  = "./lp_inputs/"


dzn_ids = [ "K", "H", "M", "P", "O", "Q" ]
dzn_ass = "="
dzn_sep = ";"

for filename in os.listdir(dzn_dir):
    if "."+filename.split(".")[-1] == dzn_ext:
        dzn_to_lp(filename, dzn_dir, lp_dir)
