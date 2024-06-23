from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
from io import BytesIO

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
)

async def send_measurement_email(email_to: str, measurement_pdf: BytesIO):
    message = MessageSchema(
        subject="Your Measurement Report",
        recipients=[email_to],
        body="Please find attached your measurement report.",
        attachments=[{
            "file": measurement_pdf,
            "filename": "measurement_report.pdf",
            "headers": {
                "Content-Disposition": "attachment; filename=measurement_report.pdf",
                "Content-Type": "application/pdf",
            },
        }]
    )

    fm = FastMail(conf)
    await fm.send_message(message)