# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'factorio_game_export_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_FactorioGameExportDialog(object):
    def setupUi(self, FactorioGameExportDialog):
        if not FactorioGameExportDialog.objectName():
            FactorioGameExportDialog.setObjectName(u"FactorioGameExportDialog")
        FactorioGameExportDialog.resize(527, 338)
        self.gridLayout = QGridLayout(FactorioGameExportDialog)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line = QFrame(FactorioGameExportDialog)
        self.line.setObjectName(u"line")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 7, 0, 1, 2)

        self.input_file_label = QLabel(FactorioGameExportDialog)
        self.input_file_label.setObjectName(u"input_file_label")

        self.gridLayout.addWidget(self.input_file_label, 2, 0, 1, 1)

        self.output_file_label = QLabel(FactorioGameExportDialog)
        self.output_file_label.setObjectName(u"output_file_label")

        self.gridLayout.addWidget(self.output_file_label, 4, 0, 1, 1)

        self.output_file_edit = QLineEdit(FactorioGameExportDialog)
        self.output_file_edit.setObjectName(u"output_file_edit")

        self.gridLayout.addWidget(self.output_file_edit, 6, 0, 1, 1)

        self.auto_save_spoiler_check = QCheckBox(FactorioGameExportDialog)
        self.auto_save_spoiler_check.setObjectName(u"auto_save_spoiler_check")

        self.gridLayout.addWidget(self.auto_save_spoiler_check, 9, 0, 1, 1)

        self.output_file_button = QPushButton(FactorioGameExportDialog)
        self.output_file_button.setObjectName(u"output_file_button")

        self.gridLayout.addWidget(self.output_file_button, 6, 1, 1, 1)

        self.accept_button = QPushButton(FactorioGameExportDialog)
        self.accept_button.setObjectName(u"accept_button")

        self.gridLayout.addWidget(self.accept_button, 13, 0, 1, 1)

        self.input_file_edit = QLineEdit(FactorioGameExportDialog)
        self.input_file_edit.setObjectName(u"input_file_edit")

        self.gridLayout.addWidget(self.input_file_edit, 3, 0, 1, 1)

        self.cancel_button = QPushButton(FactorioGameExportDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.gridLayout.addWidget(self.cancel_button, 13, 1, 1, 1)

        self.description_label = QLabel(FactorioGameExportDialog)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setWordWrap(True)

        self.gridLayout.addWidget(self.description_label, 0, 0, 1, 2)

        self.input_file_button = QPushButton(FactorioGameExportDialog)
        self.input_file_button.setObjectName(u"input_file_button")

        self.gridLayout.addWidget(self.input_file_button, 3, 1, 1, 1)

        self.line_2 = QFrame(FactorioGameExportDialog)
        self.line_2.setObjectName(u"line_2")
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 1, 0, 1, 2)


        self.retranslateUi(FactorioGameExportDialog)

        QMetaObject.connectSlotsByName(FactorioGameExportDialog)
    # setupUi

    def retranslateUi(self, FactorioGameExportDialog):
        FactorioGameExportDialog.setWindowTitle(QCoreApplication.translate("FactorioGameExportDialog", u"Game Patching", None))
        self.input_file_label.setText(QCoreApplication.translate("FactorioGameExportDialog", u"Game Directory", None))
        self.output_file_label.setText(QCoreApplication.translate("FactorioGameExportDialog", u"Output Directory", None))
        self.output_file_edit.setPlaceholderText(QCoreApplication.translate("FactorioGameExportDialog", u"Path where to place the mod folder", None))
        self.auto_save_spoiler_check.setText(QCoreApplication.translate("FactorioGameExportDialog", u"Include a spoiler log on same directory", None))
        self.output_file_button.setText(QCoreApplication.translate("FactorioGameExportDialog", u"Select Folder", None))
        self.accept_button.setText(QCoreApplication.translate("FactorioGameExportDialog", u"Accept", None))
        self.input_file_edit.setPlaceholderText(QCoreApplication.translate("FactorioGameExportDialog", u"Path to Factorio folder", None))
        self.cancel_button.setText(QCoreApplication.translate("FactorioGameExportDialog", u"Cancel", None))
        self.description_label.setText(QCoreApplication.translate("FactorioGameExportDialog", u"<html><head/><body><p>In order to create the randomizer mod, a copy of Factorio itself is needed.</p></body></html>", None))
        self.input_file_button.setText(QCoreApplication.translate("FactorioGameExportDialog", u"Select Folder", None))
    # retranslateUi

