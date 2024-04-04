import sys
import os
from PyQt5 import uic, QtWidgets

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # ui_file_path = os.path.join(current_dir, 'main1.ui')
        # uic.loadUi(ui_file_path, self)
        uic.loadUi('/Users/lmistie/Desktop/RTU_MIREA/Магистратура/1_Курс/2_Семестр/Инструментальное программное обеспечение разработки и проектирования информационных систем/PR_Qt/PR6/main.ui', self)
        self.font_size = QtWidgets.QLabel()
        self.save.triggered.connect(self.save_file)
        self.open.triggered.connect(self.open_file)
        self.increase_font_action.clicked.connect(self.increase_font_size)
        self.decrease_font_action.clicked.connect(self.decrease_font_size)
        self.fontComboBox.currentFontChanged.connect(self.change_font)
    
    def open_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть файл')
        if file:
            encodings = ["utf-8", "latin-1", "cp1252"]
            content = None
            for encoding in encodings:
                try:
                    with open(file, "r", encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            if content is not None:
                self.textBrowser.setPlainText(content)
            else:
                QtWidgets.QMessageBox.warning(self, 'Открыть файл', 'Не получается открыть файл.')
    
    def save_file(self):
        current_widget = self.textBrowser
        content = current_widget.toPlainText()
        file_dialog = QtWidgets.QFileDialog()
        file_name, _ = file_dialog.getSaveFileName(self, "Сохранить файл", "", "All Files (*)")
        if file_name:
            with open(file_name, "w") as f:
                f.write(content)
            QtWidgets.QMessageBox.information(self, "Сохранено успешно", "Файл сохранен успешно.")
    
    def increase_font_size(self):
        current_widget = self.textBrowser
        cursor = current_widget.textCursor()
        format = cursor.charFormat()
        font = format.font()
        font_size = font.pointSize()
        font_size += 1
        self.font_size = self.findChild(QtWidgets.QLabel, 'size')
        font.setPointSize(font_size)
        format.setFont(font)
        self.font_size.setText(str(font_size))
        cursor.mergeCharFormat(format)
        current_widget.setFocus()
    
    def decrease_font_size(self):
        current_widget = self.textBrowser
        cursor = self.textBrowser.textCursor()
        format = cursor.charFormat()
        font = format.font()
        font_size = font.pointSize()
        font_size -= 1
        self.font_size = self.findChild(QtWidgets.QLabel, 'size')
        font.setPointSize(font_size)
        format.setFont(font)
        self.font_size.setText(str(font_size))
        cursor.mergeCharFormat(format)
        current_widget.setFocus()
    
    def change_font(self, font):
        current_widget = self.textBrowser
        text_cursor = current_widget.textCursor()
        format = text_cursor.charFormat()
        font_name = font.family()
        format.setFontFamily(font_name)
        text_cursor.mergeCharFormat(format)
        current_widget.setFocus()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
