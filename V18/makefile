all: build/main.pdf

build:
	mkdir -p build

build/main.pdf: V18.tex | build
	lualatex --output-directory=build --interaction=nonstopmode --halt-on-error V18.tex
	biber build/V18
	lualatex --output-directory=build --interaction=nonstopmode --halt-on-error V18.tex
	lualatex --output-directory=build --interaction=nonstopmode --halt-on-error V18.tex

light: V18.tex | build
	lualatex --output-directory=build --interaction=nonstopmode --halt-on-error V18.tex

clean:
	rm -rf build

.PHONY: all clean light
