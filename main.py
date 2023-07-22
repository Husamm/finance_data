from send_email import EmailReport

subject = "An email with attachment from Python"
body = "This is an email with attachment sent from Python"
sender_email = "husamdevacc183@gmail.com"
receiver_email = "husamm456@gmail.com"
password = 'jobtkqatnghccmoy'

em = EmailReport()
em.attached_file_path = 'meta.csv'
em.email_body = 'stam'
em.sender_email = sender_email
em.receiver_email = receiver_email
em.subject = subject

em.send()
