import smtplib

from email.mime.multipart import MIMEMultipart #pour ajouter plus d'information lors de l'envoie de l'emails

from email.mime.text import MIMEText # va permettre d'attcher du contenu texte a l'emails

import emails_config



def envoyer_email(emails_destimataire: str,sujet: str,message: str):

    multipart_message = MIMEMultipart()
    multipart_message["Subject"] = sujet
    multipart_message["From"] = emails_config.config_email
    multipart_message["To"] = emails_destimataire

    # pour attacher du contenu texte,pdf,image,html,lien(plain sous forme de texte ou html en utilisant des balise pour le style)
    multipart_message.attach(MIMEText(message, "plain"))

    # donner l'adresse et le port du serveur pour pouvoir se connecte
    serveur_mail = smtplib.SMTP(emails_config.config_server, emails_config.config_server_port)

    serveur_mail.starttls()#mettre en place le protocole tls

    # donner les informatios d'authenfier pour le logiin
    serveur_mail.login(emails_config.config_email, emails_config.config_password)

    # envoyer un mail
    serveur_mail.sendmail(emails_config.config_email, emails_destimataire, multipart_message.as_string())
    # mettre as_string pour envoyer en chaine de caractere

    # fermer la connexion
    serveur_mail.quit()





