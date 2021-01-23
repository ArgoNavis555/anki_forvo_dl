import os
import anki
from typing import List
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from anki_forvo_dl.Forvo import Pronunciation
from anki_forvo_dl.Util import CustomScrollbar


class PronunciationWidget(QWidget):
    def __init__(self, pronunciation: Pronunciation, select_pronunciation, parent=None):
        from anki_forvo_dl import asset_dir
        super(PronunciationWidget, self).__init__(parent)
        container = QWidget(self)
        container.setFixedWidth(450)
        container.setFixedHeight(100)
        container.setStyleSheet("background-color: #F4FAFF; margin: 0; padding: 0; border-radius: 10px")

        layout = QHBoxLayout(container)
        layout.setContentsMargins(30, 10, 30, 10)
        btn = QPushButton("")
        btn.setFixedWidth(40)
        btn.setFixedHeight(40)
        btn.setIcon(QIcon(os.path.join(asset_dir, "play_button.png")))
        btn.setIconSize(QSize(40, 40))
        btn.clicked.connect(lambda: anki.sound.play(pronunciation.audio))

        layout.addWidget(btn)

        layout.addSpacing(20)

        word_info_layout = QVBoxLayout()

        word = QLabel(pronunciation.word)
        word_info_layout.addWidget(word)
        word.setStyleSheet("font-size: 24px; font-weight: bold")
        more_info = QLabel("by " + pronunciation.user)
        word_info_layout.addWidget(more_info)
        word_info_layout.setContentsMargins(0, 15, 0, 15)
        layout.addLayout(word_info_layout)
        layout.addStretch()


        btn_select = QPushButton("")
        btn_select.setFixedWidth(40)
        btn_select.setFixedHeight(40)
        btn_select.setIcon(QIcon(os.path.join(asset_dir, "checkmark.png")))
        btn_select.setIconSize(QSize(40, 40))
        btn_select.clicked.connect(lambda: select_pronunciation(pronunciation))
        layout.addWidget(btn_select)



        vbox = QVBoxLayout()
        vbox.addWidget(container)
        vbox.setContentsMargins(15, 15, 15, 0)
        self.setLayout(vbox)


class AddSingle(QDialog):
    def __init__(self, parent, pronunciations: List[Pronunciation]):
        super().__init__(parent)
        from anki_forvo_dl import asset_dir

        font_db = QFontDatabase()
        font_db.addApplicationFont(os.path.join(asset_dir, "IBMPlexSans-Bold.ttf"))
        font_db.addApplicationFont(os.path.join(asset_dir, "IBMPlexSans-Italic.ttf"))
        font_db.addApplicationFont(os.path.join(asset_dir, "IBMPlexSans-Regular.ttf"))

        self.selected_pronunciation: Pronunciation = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.description = "<h1>anki_forvo_dl</h1><p>Please select the audio you want to add.</p>"
        self.description_label = QLabel(text=self.description)
        self.description_label.setAlignment(Qt.AlignCenter)
        # self.description_label.setFont(QFont("IBM Plex Sans"))
        self.layout.addWidget(self.description_label)

        self.setStyleSheet("""
            font-family: IBM Plex Sans;
        """)
        # Create the list
        pronunciation_list = QListWidget()
        pronunciation_list.setStyleSheet("""
        border: none;
        background-color: #C5D4E2;
        """)
        # Add to list a new item (item is simply an entry in your list)

        for pronunciation in pronunciations:
            item = QListWidgetItem(pronunciation_list)
            # Instanciate a custom widget
            item_widget = PronunciationWidget(pronunciation, select_pronunciation=self.select_pronunciation)
            item.setSizeHint(item_widget.minimumSizeHint())
            # Associate the custom widget to the list entry
            pronunciation_list.setItemWidget(item, item_widget)

        pronunciation_list.setFixedWidth(480)
        pronunciation_list.setMinimumHeight(500)
        pronunciation_list.setVerticalScrollBar(CustomScrollbar())
        pronunciation_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        pronunciation_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        pronunciation_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.setMaximumHeight(1000)

        self.layout.addWidget(pronunciation_list)
        self.adjustSize()

    def select_pronunciation(self, pronunciation: Pronunciation):
        self.selected_pronunciation = pronunciation
        self.close()


#
# def main():
#     app = QApplication(sys.argv)
#     prons = [
#         Pronunciation("ja", "strawberrybrown", "Female from Japan", 2345234, 4, "", False, "None"),
#         Pronunciation("ja", "strawberrybrown", "Female from Japan", 2345234, 4, "", False, "None"),
#         Pronunciation("ja", "strawberrybrown", "Female from Japan", 2345234, 4, "", False, "None"),
#         Pronunciation("ja", "strawberrybrown", "Female from Japan", 2345234, 4, "", False, "None"),
#         Pronunciation("ja", "strawberrybrown", "Female from Japan", 2345234, 4, "", False, "None"),
#         Pronunciation("ja", "strawberrybrown", "Female from Japan", 2345234, 4, "", False, "None")
#     ]
#     main = AddSingle(parent=None, pronunciations=prons)
#     main.show()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()