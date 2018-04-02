import pytest
import pong
from  tkinter import *

root = Tk()

@pytest.fixture()
def canvas():
    return Canvas(root, width=600, height=600)


def test_something(self):
    self.assertEqual(True, False)



