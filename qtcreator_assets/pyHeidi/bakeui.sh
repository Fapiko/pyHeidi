#!/bin/sh

#pyuic4 -o ../../src/pyheidi/ui/ui_mainwindow.py mainwindow.ui
pyuic4 -o ../../src/pyheidi/ui/ui_qtexteditlinenumber.py qtexteditlinenumber.ui
pyrcc4 -o ../../src/pyheidi/ui/resources_rc.py resources.qrc
