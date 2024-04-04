from flask import Flask, request, redirect, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__, template_folder="")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        addr_from = request.form['addr_from']
        password = request.form['password']
        addr_to = request.form['addr_to']
        msg_subj = request.form['msg_subj']
        msg_text = request.form['msg_text']
        
        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = addr_to
        msg['Subject'] = msg_subj
        msg.attach(MIMEText(msg_text, 'plain'))
        
        server.login(addr_from, password)
        server.sendmail(addr_from, [addr_to], msg.as_string())
        server.quit()
    
        return render_template('index.html')
    
    if request.method == 'GET':
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
