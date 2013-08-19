#!/bin/sh

export PYQTDESIGNERPATH=$(pwd)/designer/widgets
export PYTHONPATH=$PYTHONPATH:$(pwd)/../../src/pyheidi/custom_widgets

designer-qt4
