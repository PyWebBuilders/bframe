del /Q dist\*
python setup.py bdist_wheel
python -m twine upload dist/*