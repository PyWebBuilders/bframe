rd /S /Q build
rd /S /Q bframe.egg-info
del /Q dist\*
python setup.py bdist_wheel
python -m twine upload dist/*