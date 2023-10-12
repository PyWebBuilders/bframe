rd /S /Q src\bframe.egg-info
del /Q dist\*
python -m build
python -m twine upload dist/*