# -*- coding: utf-8 -*-
from PySide2 import QtCore
from PySide2.QtWidgets import QWidget, QGridLayout, QListWidget, QAbstractItemView, QSlider, QLabel


class Layers(QListWidget):
    """ Class for layer widget to allow update of viewer when order of layers is changed.
    """
    def __init__(self, viewer):
        super(Layers, self).__init__()
        self.viewer = viewer

        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def dropEvent(self, event):
        """ Override to update viewer when order changes.
        """
        super(QListWidget, self).dropEvent(event)
        self.viewer.update()



class LayerManager(QWidget):
    """ Class to manage the layers of a viewer. Allow to change the order of layers by drag and drop.
    """
    def __init__(self, viewer):
        super(LayerManager, self).__init__()


        self.selected_layer = None

        self.viewer = viewer
        self.layers = dict()

        self.layer_widget = Layers(self.viewer)
        self.alpha_slider = QSlider(QtCore.Qt.Horizontal)
        self.alpha_label = QLabel(f"Select Layer to change Opacity")

        layout = QGridLayout()
        layout.addWidget(self.layer_widget, 0, 0, 1, 1)
        layout.addWidget(self.alpha_label, 1, 0, 1, 1)
        layout.addWidget(self.alpha_slider, 2, 0, 1, 1)
        self.setLayout(layout)

        self.layer_widget.itemClicked.connect(self.select_layer)
        self.alpha_slider.valueChanged.connect(self.slider_changed)
        self.alpha_slider.setValue(99)



    def add_layer(self, layer, name):
        """ Add new layer to be managed.

        Args:
            layer (Object): object that implements a draw function.
            name (str): String which is the name of the layer.
        """
        self.layers[name] = {"layer": layer,
                             "alpha": 1}

        self.layer_widget.addItem(name)

    def get_layers(self):
        """ Get list of layers representing the order of the LayerManager in the UI.

        Returns:
            [Objects]: objects which implement a draw function
        """
        names = [self.layer_widget.item(i).data(0) for i in range(self.layer_widget.count())]
        result = [(self.layers[name]["layer"], self.layers[name]["alpha"]) for name in names]
        return result

    def select_layer(self, item):
        """ Select a layer to change opacity.

        Args:
            item: item of the list
        """
        name = item.data(0)
        self.selected_layer = name
        self.alpha_label.setText(f"Opacity ({self.selected_layer}):")

        # set slider to current value
        value = self.layers[name]["alpha"]
        value = value*100 - 1
        self.alpha_slider.setValue(value)

    def slider_changed(self, value):
        """ Callback when the opacity slider was moved.

        Args:
            value (int): slider value 0-99
        """
        value = (value+1) / 100
        if self.selected_layer in self.layers:
            self.layers[self.selected_layer]["alpha"] = value
        self.viewer.update()

