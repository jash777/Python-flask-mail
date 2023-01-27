from flask import Flask, request, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def send_email():
    if request.method == "POST":
        from_address = request.form.get('from_address')
        if from_address is None:
            return "from_address is missing"
        to_address = request.form.get('to_address')
        if to_address is None:
            return "to_address is missing"
        subject = request.form['subject']
        message = request.form['message']
        cc_email = request.form['cc_email']
        bcc_email = request.form['bcc_email'] 
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Cc'] = cc_email
        msg['Bcc'] = bcc_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        attachment = request.files.get('attachment')
        print(attachment)
        if attachment:
            part = MIMEBase('application', "octet-stream")
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=attachment.filename)
            msg.attach(part)

        print(attachment)
        server = smtplib.SMTP('smtp-relay.sendinblue.com', 587)
        server.starttls()
        server.login('***************', '***************' )
        text = msg.as_string()
        server.sendmail(from_address, [to_address, cc_email, bcc_email], text)
        server.quit()
    return render_template('email_form.html')

    
if __name__ == '__main__':
    app.run(debug=True)
