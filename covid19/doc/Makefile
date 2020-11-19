.PHONY : compile clean all

all: compile clean

compile:
	@echo "Compilo una volta";
	@pdflatex main.tex >> tmp;
	@echo "Compilo una seconda volta";
	@pdflatex main.tex >> tmp;

clean:
	@echo "Pulisco"
	@rm -f tmp *.aux *.fls *.log *.out *.toc *.synctex.gz *.fdb_latexmk *.bbl *.blg *.bcf *.run.xml *.run.xml *.*busy*
