# ----------------------------------------------------------------------------------------------------------------------
#  Copyright (c) 2022-2023.  Antonio Bulgheroni.
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ----------------------------------------------------------------------------------------------------------------------
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard

from expwizard.constants import fully_implemented_microscope
from expwizard.wizard_conclusion_page_ui import Ui_WizardPage


class ConclusionPage(QWizardPage, Ui_WizardPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)

        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(':/expwizard/glossy-microscope.png'))
        self.setPixmap(QWizard.LogoPixmap, QPixmap(':/expwizard/ec-logo.jpg'))

        self.registerField('start', self.start_checkbox)
        self.setFinalPage(True)

    def initializePage(self) -> None:

        if self.field('new_experiment'):
            self.message.setText(
                'You are all set! <br><br>'
                '<ul><li>An entry in the microscopy protocol list has been generated.'
                '<li>Folders have been created.'
                '<li>An experiment file has been generated.'
            )
        else:
            if self.field('microscope') in fully_implemented_microscope:
                self.message.setText(
                    'You are ready to restart your experiment! <br><br>'
                    'Select the Start autologbook check box to start right away.'
                )
            else:
                self.message.setText(
                    'You are ready to restart your experiment! <br><br>'
                    'Unfortunately your microscope is not yet included in the automatic documentation software, so '
                    'you will have to manually document your experiment.'
                )

        self.start_checkbox.setEnabled(self.field('microscope') in fully_implemented_microscope)
        self.start_checkbox.setChecked(self.field('microscope') in fully_implemented_microscope)

    def nextId(self) -> int:
        return -1
