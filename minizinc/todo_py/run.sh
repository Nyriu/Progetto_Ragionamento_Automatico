minizinc covid19.mzn ./inputs/input_$1.dzn $2 > tmp_$1.txt;
python pretty.py tmp_$1.txt;
rm tmp_$1.txt
