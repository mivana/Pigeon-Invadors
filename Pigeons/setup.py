from cx_Freeze import setup, Executable

base = None


executables = [Executable("igrica.py", base=base)]

packages = ["PyQt5"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "<any name>",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)