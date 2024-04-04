import os
import sys
import smtplib
import mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from PyQt5 import uic, QtWidgets, QtGui

def process_attachement(msg, files):
    for f in files:
        if os.path.isfile(f):
            attach_file(msg, f)
            print(f'Файл {f} прикреплен')
        elif os.path.exists(f):
            directory = os.listdir(f)
            for file in directory:
                attach_file(msg, f + "/" + file)

def attach_file(msg, filepath):
    part = MIMEBase('application', "octet-stream")
    with open(filepath, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath))
    msg.attach(part)

def send_email(server_index, addr_from, password, msg_subj, msg_text, files):
    if server_index == 0:
        server = smtplib.SMTP('smtp.mail.ru', 25)          
        server.starttls() 
    elif server_index == 1:
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    elif server_index == 2:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 587)

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = 'romaniy11052001@mail.ru'
    msg['Subject'] = msg_subj
    msg.attach(MIMEText(msg_text, 'plain'))
    log = False
    if not log:
        try:
            server.login(addr_from, password)
            print('Подключение выполнено успешно.\n')
        except:
            print('Неверные данные отправителя.\n')
    process_attachement(msg, files)
    server.sendmail(addr_from, msg['To'], msg.as_string())
    server.quit()

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file_path = os.path.join(current_dir, 'main1.ui')
        uic.loadUi(ui_file_path, self)
        # uic.loadUi('C:/Users/Roman/Desktop/Mirea/PR_Qt/PR2/main1.ui', self)
        self.addr_from.setText('romaniy11052001@mail.ru')
        self.password.setText('GDWYgRSwALRjesx9pGmf')
        self.btn_send.clicked.connect(self.send_email)
        self.btn_load.clicked.connect(self.open_file)
        self.model = QtGui.QStandardItemModel(self.listView)

    def send_email(self):
        send_email(server_index=self.comboBox.currentIndex(),
                   addr_from=self.addr_from.text(),
                   password=self.password.text(),
                   msg_subj=self.msg_subj.text(),
                   msg_text=self.msg_text.toPlainText(),
                   files=[self.model.item(i).text() for i in range(self.model.rowCount())])

    def open_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть файл', '', 'AllFiles (*)')
        if filename:
            self.path = filename
            item = QtGui.QStandardItem(self.path[0])
            self.model.appendRow(item)      
            self.listView.setModel(self.model)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
