import sys
import os

async def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)
