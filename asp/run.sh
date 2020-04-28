LP_DIR=./lp_inputs

for f in $LP_DIR/input_*.lp do
    clingo covid19.lp $f
done

