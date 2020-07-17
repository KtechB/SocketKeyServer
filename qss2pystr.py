import os

with open(os.path.join(os.path.curdir,"src\main\qss\style.qss"), "r") as f:
    style = f.read()

style = r'style = """'  + style[1:] + r'"""'

with open(os.path.join(os.path.curdir,"src\main\python\qss.py"), "w") as f:
    f.write(style )