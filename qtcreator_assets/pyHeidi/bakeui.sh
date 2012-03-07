#!/bin/sh

pyuic4 -o ../../src/pyheidi/ui/ui_mainwindow.py mainwindow.ui
pyrcc4 -o ../../src/pyheidi/ui/resources_rc.py resources.qrc