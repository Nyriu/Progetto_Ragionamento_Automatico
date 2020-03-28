 minizinc 007_covid19.mzn input_$1.dzn $2 |
   sed 's/[^:=0-9.]0/--/g' | 

   sed 's/[^:=0-9.]1/-M/g' |
   sed 's/[^:=0-9.]2/-P/g' |
   sed 's/[^:=0-9.]3/-O/g' |
   sed 's/[^:=0-9.]4/-Q/g' |

   sed 's/[^:=0-9.]5/MM/g' |
   sed 's/[^:=0-9.]6/PP/g' |
   sed 's/[^:=0-9.]7/QQ/g' ;
