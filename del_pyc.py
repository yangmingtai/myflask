#!/usr/bin/env python
import sys
import os


def del_pyc(current_item=None, ispyc=False):
    if current_item is None:
        current_item = sys.path[0]
    if os.path.isdir(current_item) and ispyc:
        print(current_item)
        for item in os.listdir(current_item):
            print('del' + os.path.join(current_item, item))
            os.remove(os.path.join(current_item, item))
        return
    elif os.path.isdir(current_item):
        for item in os.listdir(current_item):
            if item == '__pycache__':
                del_pyc(os.path.join(current_item, item), ispyc=True)
                os.rmdir(os.path.join(current_item, item))
            else:
                del_pyc(os.path.join(current_item, item), ispyc=False)
    else:
        return


if __name__ == '__main__':
    del_pyc()
