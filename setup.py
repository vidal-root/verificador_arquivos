import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.

packages = [
    'PySimpleGUI',
    'datetime',
    'time',
    'os'
]

options = {
    'build_exe': {
        'packages': packages
    },
}

setup(
    name="Verificador de Arquivos",
    version="0.1",
    description="App que verifica a modificação em arquivos",
    options=options,
    executables=[Executable("app.py", icon="icon.ico", base="Win32GUI")]
)
