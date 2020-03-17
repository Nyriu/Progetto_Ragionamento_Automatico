./clean.sh;
echo "Compilo una volta";
pdflatex main.tex >> tmp;
echo "Compilo una seconda volta";
pdflatex main.tex >> tmp;
./clean.sh;
rm tmp;
