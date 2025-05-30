all: build/main.pdf

build:
	mkdir -p build

build/main.pdf: V61.tex | build
	lualatex --output-directory=build --interaction=nonstopmode --halt-on-error V61.tex
	biber build/V61
	lualatex --output-directory=build --interaction=nonstopmode --halt-on-error V61.tex
	lualatex --output-directory=build --interaction=nonstopmode --halt-on-error V61.tex

light: V61.tex | build
	lualatex --output-directory=build --interaction=nonstopmode --halt-on-error V61.tex

clean:
	rm -rf build

.PHONY: all clean light
