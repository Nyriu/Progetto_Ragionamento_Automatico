minizinc 008_covid19.mzn input_$1.dzn $2 > output_$1.txt;
python pretty.py output_$1.txt
