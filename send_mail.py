from email.mime.image import MIMEImage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import qrcode

from pass_gen import pass_gen

# Set up the email parameters
sender = "regalia.rcciit.official@hotmail.com"
# recipients = ["cse2020067@rcciit.org.in"]
subject = "Regalia 2023 - Please go through the email carefully"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Log in to the SMTP server
server = smtplib.SMTP("smtp-mail.outlook.com", 587)
server.starttls()
server.login(sender, "rcciitregalia123@")

# Open the CSV file
with open("data.csv", "r", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")

    # Open the log file in append mode
    with open("log.txt", "a") as log:

        # Loop through each row in the CSV file
        for row in reader:
            # Print all the columns in the current row
            print(row)

            try:
                # Add data to the QR code
                qr.add_data([row[1], row[2]])
                qr.make(fit=True)

                # Create an image from the QR code
                img = qr.make_image(fill_color="black", back_color="white")

                # Save the image as a PNG file
                img.save("qr_code.png")

                # resets qr code data
                qr.clear()

                # Open the image file and read its contents
                with open("qr_code.png", "rb") as f:
                    img_data = f.read()

                # Create the message
                msg = MIMEMultipart()
                msg["From"] = sender
                msg["To"] = row[2]
                msg["Subject"] = subject

                # msg.attach(MIMEText(body, "plain"))
                msg.attach(MIMEText(pass_gen(row[0], row[1], row[2]), "html"))

                # add attachment
                msg.attach(MIMEImage(img_data, name="pass_qr.png"))

                # Send the message
                server.sendmail(sender, row[2], msg.as_string())
                print("sent -> " + row[2])
                # Append a new line to the file
                log.write("sent -> " + row[2] + "\n")

            except Exception as e:
                print("failed -> " + row[2] + str(e))
                log.write("failed -> " + row[2] + str(e) + "\n")

server.quit()
