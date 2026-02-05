import smtplib

EMAIL = "Vydehiswamy2@gmail.com"
PASSWORD = "svhc emod eadp qgzt"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL, PASSWORD)
print("LOGIN SUCCESS")
server.quit()
