from pathlib import Path
import datetime
import win32com.client
import re

# Create output folder
output_dir = Path.cwd() / "Output"
output_dir.mkdir(parents=True, exist_ok=True)

# Connect to outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Connect to folder
inbox = outlook.Folders("mockticketingsystem@outlook.com").Folders("Inbox")

# Get messages
messages = inbox.Items

for message in messages:
    subject = message.Subject
    body = message.body
    emailAddress = message.SenderEmailAddress
    senderName = message.SenderName

    # Create separate folder for each message, exclude special characters and timestampe
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    target_folder = output_dir / re.sub('[^0-9a-zA-Z]+', '', subject) / current_time
    target_folder.mkdir(parents=True, exist_ok=True)

    # Write body to text file
    Path(target_folder / "EMAIL_BODY.txt").write_text(str(body))

    Path(target_folder / "EMAIL_SUBJECT.txt").write_text(str(subject))

    Path(target_folder / "EMAIL_SENDER.txt").write_text(str(emailAddress))

    Path(target_folder / "SENDER_NAME.txt").write_text(str(senderName))

# Save attachments and exclude special      ||| Commenting out until Attachment functionality where I want it
   # for attachment in attachments:
    #    filename = re.sub('[^0-9a-zA-Z\\.]+', '', attachment.FileName)
     #   attachment.SaveAsFile(target_folder / filename)