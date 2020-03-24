 minizinc 004_covid19.mzn input_$1.dzn $2 |
   sed 's/0/--/g' | 

   sed 's/1/-M/g' |
   sed 's/2/-P/g' |
   sed 's/3/-O/g' |
   sed 's/4/-Q/g' |

   sed 's/5/MM/g' |
   sed 's/6/PP/g' |
   sed 's/7/QQ/g' ;
