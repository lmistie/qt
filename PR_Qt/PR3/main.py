import os
import sys
import smtplib
import csv
import mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from PyQt5 import uic, QtWidgets

def process_attachment(msg, files):
    for f in files:
        if os.path.isfile(f):
            attach_file(msg, f)
            print(f'File {f} attached')
        elif os.path.exists(f):
            directory = os.listdir(f)
            for file in directory:
                attach_file(msg, f + "/" + file)

def attach_file(msg, filepath):
    filename = os.path.basename(filepath)
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        with open(filepath) as fp:
            file = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'image':
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'audio':
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)
            file.set_payload(fp.read())
        fp.close()
    encoders.encode_base64(file)
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)

def send_email(server_index, addr_from, password, addr_to, msg_subj, msg_text, files):
    if server_index == 0:
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    elif server_index == 1:
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    elif server_index == 2:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 587)

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = msg_subj
    msg.attach(MIMEText(msg_text, 'plain'))
    
    log = False
    if not log:
        try:
            server.login(addr_from, password)
            print('Подключение выполнено успешно.\n')
        except:
            print('Неверные данные отправителя.\n')

    process_attachment(msg, files)
    server.sendmail(addr_from, [addr_to], msg.as_string())
    server.quit()

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file_path = os.path.join(current_dir, 'main1.ui')
        uic.loadUi(ui_file_path, self)
        # uic.loadUi('C:/Users/Roman/Desktop/Mirea/PR_Qt/PR3/main1.ui', self)
        self.addr_from.setText('romaniy11052001@mail.ru')
        self.password.setText('GDWYgRSwALRjesx9pGmf')
        self.btn_send.clicked.connect(self.send_email)
        self.btn_load.clicked.connect(self.open_file)

    def send_email(self):
        my_file = open("send.txt", "a")
        f = open(self.csv_name.text(), 'r')
        reader = csv.reader(f)
        for row in reader:
            row = row[0].split(';')
            addr_to = row[0]
            files = row[1:]
            send_email(server_index=self.comboBox.currentIndex(),
                       addr_from=self.addr_from.text(),
                       addr_to=addr_to,
                       password=self.password.text(),
                       msg_subj=self.msg_subj.text(),
                       msg_text=self.msg_text.toPlainText(),
                       files=files)
            my_file.write("\n Email {0}; Тема:{1}; Сообщение:{2}".format(addr_to,
                                                                           self.msg_subj.text(),
                                                                           self.msg_text.toPlainText()))
    def open_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть файл', '',
                                                         filter='csv (*.csv);;AllFiles (*)')
        if filename:
            self.csv_name.setText(filename[0])
        else:
            return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
