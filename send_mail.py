import smtplib
import config
from email.mime.text import MIMEText


def send_mail(student, lect, rating, comments, muddiest, date):

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL_ADDRESS, config.PASSWORD)
    message = f"Subject: New Feedback Submission \n\n you have a new submission from student: {student} who gave you a rating of {rating} and has left the following comment: {comments}. Additionally the student has demonstrated difficulties regarding: {muddiest}."
    server.sendmail(config.EMAIL_ADDRESS, "najafiannice@gmail.com", message)
    server.quit()
