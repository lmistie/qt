import smtplib                                              # Импортируем библиотеку по работе с SMTP
import os                                                 # Функции для работы с операционной системой, не зависящие от используемой операционной системы
# import ssl                                                # Для создания безопасного контекста SSL
import sys                                                  # Для передачи аргументов командной строки
import smtplib                                              # Импортируем библиотеку по работе с SMTP

from PyQt5 import uic, QtWidgets                              # Импортируем uic и QtWidgets из пакета PyQt5
# Добавляем необходимые подклассы - MIME-типы
# import mimetypes                                            # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
# from email import encoders                                  # Импортируем энкодер
# from email.mime.base import MIMEBase                        # Общий тип
from email.mime.text import MIMEText                          # Текст/HTML
# from email.mime.image import MIMEImage                      # Изображения
# from email.mime.audio import MIMEAudio                      # Аудио
from email.mime.multipart import MIMEMultipart                # Многокомпонентный объект
# from email.message import EmailMessage                      # Импортируем класс EmailMessage

# current_dir = os.path.dirname(os.path.abspath(__file__))
# ui_file_path = os.path.join(current_dir, 'main.ui')


# Дальше cоздаю класс App для отправки письма через форму
class App(QtWidgets.QMainWindow):                                               # Создаем класс App, наследуемый от класса QtWidgets.QMainWindow
    def __init__(self):                                                         # Конструктор класса
        super().__init__()                                                      # Вызов конструктора родительского класса
        uic.loadUi("/Users/lmistie/Desktop/RTU_MIREA/Магистратура/1_Курс/2_Семестр/Инструментальное программное обеспечение разработки и проектирования информационных систем/PR_Qt/PR1/main.ui", self)      
        # uic.loadUi(ui_file_path, self)

        self.btn_send.clicked.connect(self.send_email)                          # Подключение кнопки к функции send_email
    
    def send_email(self):                                                       # Функция для отправки письма
        send_email(addr_to=self.addr_to.text(), msg_subj=self.msg_subj.text(),
                   msg_text=self.msg_text.toPlainText())                        # Вызов функции send_email с параметрами из формы
        
def send_email(addr_to, msg_subj, msg_text):
    addr_from = "romaniy11052001@mail.ru"                  # Отправитель
    password = "GDWYgRSwALRjesx9pGmf"                       # Пароль
    
    #addr_from = "romaniy11052001@yandex.ru "                # Отправитель yandex
    #password = "usaepmejsphosxkd"                           # Пароль от яндекса
    
    msg = MIMEMultipart()                                   # Создаем сообщение
    msg['From']    = addr_from                              # Адресат
    msg['To']      = addr_to                                # Получатель
    msg['Subject'] = msg_subj                               # Тема сообщения

    body = msg_text                                         # Текст сообщения
    msg.attach(MIMEText(body, 'plain'))                     # Добавляем в сообщение текст
    
    # ==== Yandex =====
    #server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)        # Создаем объект SMTP
    # =================
    
    # === Mail =====
    server = smtplib.SMTP('smtp.mail.ru', 25)               # Создаем объект SMTP
    server.starttls()                                       # Начинаем шифрованный обмен по TLS
    # ==============
    
    # ==== Gmail ====
    #server = smtplib.SMTP('smtp.gmail.com', 587)            # Создаем объект SMTP
    #server.starttls()                                       # Начинаем шифрованный обмен по TLS
    # ===============
    
    log = False                                             # Флаг проверки входа
    if not log:                                             # Если не авторизовались
        try:                                                # Пробуем
            server.login(addr_from, password)               # Авторизоваться
            print('Подключение выполнено успешно.\n')       # Если получилось, то выводим сообщение
        except:                                             # Если не получилось
            print('Неверные данные отправителя.\n')         # Выводим сообщение
            return                                          # Выходим из функции
    server.send_message(msg)                                # Отправляем сообщение
    print('Отправлено сообщение "{}" на тему "{}" на адрес {}.\n'.format(msg_text, msg_subj, addr_to)) # Выводим сообщение
    server.quit()                                           # Выходим
    
if __name__ == '__main__':                                  # Если файл запущен, а не импортирован
    app = QtWidgets.QApplication(sys.argv)                  # Создаем приложение
    ex = App()                                              # Создаем объект класса App
    ex.show()                                               # Показываем окно
    sys.exit(app.exec_())                                   # Запускаем приложение