@echo off
pdflatex -output-directory=build V44.tex
cd build
for %%i in (*) do (
    if not "%%~xi"==".pdf" del "%%i"
)