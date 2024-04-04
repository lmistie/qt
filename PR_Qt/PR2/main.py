import smtplib                                              # Импортируем библиотеку по работе с SMTP
import os                                                   # Функции для работы с операционной системой, не зависящие от используемой операционной системы
import ssl                                                  # Для создания безопасного контекста SSL
import sys                                                  # Для передачи аргументов командной строки
import smtplib                                              # Импортируем библиотеку по работе с SMTP

from PyQt5 import uic, QtWidgets, QtCore, QtGui                    # Импортируем uic и QtWidgets из пакета PyQt5
from PyQt5.QtWidgets import QFileDialog                     # Импортируем класс для работы с диалоговыми окнами
from email import encoders                                  # Импортируем модуль для энкодирования

# Добавляем необходимые подклассы - MIME-типы
import mimetypes                                            # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                  # Импортируем энкодер
from email.mime.base import MIMEBase                        # Общий тип
from email.mime.text import MIMEText                        # Текст/HTML
from email.mime.image import MIMEImage                      # Изображения
from email.mime.audio import MIMEAudio                      # Аудио
from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект
from email.message import EmailMessage                      # Импортируем класс EmailMessage

current_dir = os.path.dirname(os.path.abspath(__file__))
ui_file_path = os.path.join(current_dir, 'main1.ui')

# Дальше cоздаю класс App для отправки письма через форму
class App(QtWidgets.QMainWindow):                                               # Создаем класс App, наследуемый от класса QtWidgets.QMainWindow
    def __init__(self):                                                         # Конструктор класса
        super().__init__()                                                      # Вызов конструктора родительского класса
        # uic.loadUi('C:/Users/Roman/Desktop/Mirea/PR_Qt/PR2/main1.ui', self)     # Загрузка интерфейса из файла ui
        uic.loadUi(ui_file_path, self)
        self.btn_send.clicked.connect(self.send_email)                          # Подключение кнопки к функции send_email
        self.btn_load.clicked.connect(self.open_file)                           # Подключение кнопки "open_file" к функции open_file
        self.model = QtGui.QStandardItemModel(self.listView)                    # Создаем модель
    
    def open_file(self):                                            # Функция для открытия файла
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, u'Open file', "", filter="All files (*.*)")
        if filename:                                                # Если файл выбран
            self.path = filename                                    # Сохраняем путь к файлу
            base_name = os.path.basename(self.path)                 # Получаем только имя файла и его расширение
            item = QtGui.QStandardItem(base_name)                   # Создаем элемент
            self.model.appendRow(item)                              # Добавляем элемент в модель
            self.listView.setModel(self.model)                      # Устанавливаем модель для listView
            
    
    def process_attachement(self, msg, files):                          # Функция по обработке списка, добавляемых к сообщению файлов
        for f in files:
            if os.path.isfile(f):                                       # Если файл существует
                self.attach_file(msg,f)                                 # Добавляем файл к сообщению
            elif os.path.exists(f):                                     # Если путь не файл и существует, значит - папка
                dir = os.listdir(f)                                     # Получаем список файлов в папке
                for file in dir:                                        # Перебираем все файлы и...
                    self.attach_file(msg,f+"/"+file)                    # добавляем каждый файл к сообщению
    
    def attach_file(self, msg, filepath):                             # Функция по добавлению конкретного файла к сообщению
        filename = os.path.basename(filepath)                   # Получаем только имя файла
        ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
        if ctype is None or encoding is not None:               # Если тип файла не определяется
            ctype = 'application/octet-stream'                  # Будем использовать общий тип
        maintype, subtype = ctype.split('/', 1)                 # Получаем тип и подтип
        if maintype == 'text':                                  # Если текстовый файл
            with open(filepath) as fp:                          # Открываем файл для чтения
                file = MIMEText(fp.read(), _subtype=subtype)    # Используем тип MIMEText
            fp.close()                                          # После использования файл обязательно нужно закрыть
        elif maintype == 'image':                               # Если изображение
            with open(filepath, 'rb') as fp:
                file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'audio':                               # Если аудио
            with open(filepath, 'rb') as fp:
                file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:                                                   # Неизвестный тип файла
            with open(filepath, 'rb') as fp:
                file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
                file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()
            encoders.encode_base64(file)                        # Содержимое должно кодироваться как Base64
        file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
        msg.attach(file)                                        # Присоединяем файл к сообщению
    
    def send_email(self):                                                       # Функция для отправки письма
        addr_from = self.addr_from.text()                                       # Адрес отправителя
        password = self.password.text()                                         # Пароль отправителя
        addr_to = self.addr_to.text()                                           # Получатель
        msg_subj = self.msg_subj.text()                                         # Тема сообщения
        msg_text = self.msg_text.toPlainText()                                  # Текст сообщения
        combo = self.comboBox.currentIndex()                                    # Выбор почтового сервиса
        #list = self.listView.text()                                             # Список файлов
    
        if combo == 0:                                              # Если выбран Яндекс
            server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)        # Создаем объект SMTP     
        elif combo == 1:                                            # Если выбран Mail.ru
            server = smtplib.SMTP('smtp.mail.ru', 25)               # Создаем объект SMTP            
            server.starttls()                                       # Начинаем шифрованный обмен по TLS
        elif combo == 2:                                            # Если выбран gmail
            server = smtplib.SMTP('smtp.gmail.com', 587)            # Создаем объект SMTP 
            server.starttls()                                       # Начинаем шифрованный обмен по TLS
            
        log = False                                                 # Флаг проверки входа
        if not log:                                                 # Если не авторизовались
            try:                                                    # Пробуем
                server.login(addr_from, password)                   # Авторизоваться
                print('Подключение выполнено успешно.\n')           # Если получилось, то выводим сообщение
            except:                                                 # Если не получилось
                print('Неверные данные отправителя.\n')             # Выводим сообщение
                return                                              # Выходим из функции
            
        msg = MIMEMultipart()                                       # Создаем объект сообщения
        # теперь формируем сообщение
        msg['From'] = addr_from                                     # Адресат
        msg['To'] = addr_to                                         # Получатель
        msg['Subject'] = msg_subj                                   # Тема сообщения
        msg.attach(MIMEText(msg_text))                              # Добавляем в сообщение текст
        self.process_attachement(msg, list)                         # Добавляем в сообщение файлы
        server.quit()                                               # Выходим из почтового ящика
        
'''
def open_file(self):                                            # Функция для открытия файла
    filename = QtCore.QtFileDialog.getOpenFileName(self, u'Open file', '')[0] # Открываем диалоговое окно для выбора файла
    if filename:                                                # Если файл выбран
        self.listView.addItem(filename)                         # Добавляем его в список файлов
        
def process_attachement(msg, files):                        # Функция по обработке списка, добавляемых к сообщению файлов
    for f in files:
        if os.path.isfile(f):                               # Если файл существует
            attach_file(msg,f)                              # Добавляем файл к сообщению
        elif os.path.exists(f):                             # Если путь не файл и существует, значит - папка
            dir = os.listdir(f)                             # Получаем список файлов в папке
            for file in dir:                                # Перебираем все файлы и...
                attach_file(msg,f+"/"+file)                 # ...добавляем каждый файл к сообщению

def attach_file(msg, filepath):                             # Функция по добавлению конкретного файла к сообщению
    filename = os.path.basename(filepath)                   # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:               # Если тип файла не определяется
        ctype = 'application/octet-stream'                  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)                 # Получаем тип и подтип
    if maintype == 'text':                                  # Если текстовый файл
        with open(filepath) as fp:                          # Открываем файл для чтения
            file = MIMEText(fp.read(), _subtype=subtype)    # Используем тип MIMEText
        fp.close()                                          # После использования файл обязательно нужно закрыть
    elif maintype == 'image':                               # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'audio':                               # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:                                                   # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
            file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
        fp.close()
        encoders.encode_base64(file)                        # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
    msg.attach(file)                                        # Присоединяем файл к сообщению
'''
    
if __name__ == '__main__':                                  # Если файл запущен, а не импортирован
    app = QtWidgets.QApplication(sys.argv)                  # Создаем приложение
    ex = App()                                              # Создаем объект класса App
    ex.show()                                               # Показываем окно
    sys.exit(app.exec_())                                   # Запускаем приложение
