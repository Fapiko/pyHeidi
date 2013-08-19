#!/bin/sh

export PYQTDESIGNERPATH=$(pwd)/designer/widgets
export PYTHONPATH=$PYTHONPATH:$(pwd)/../../src/pyheidi/ui/custom_widgets

designer-qt4
