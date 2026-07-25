import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from config import (
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECEIVER,
    SMTP_SERVER,
    SMTP_PORT,
)


def send_email(results, report_file):

    strong = [x for x in results if x["Signal"] == "Strong Buy"]
    buy = [x for x in results if x["Signal"] == "Buy"][:3]
    watch = [x for x in results if x["Signal"] == "Watch"][:3]

    body = f"""
    <html>

    <body style="font-family:Arial">

    <h2>📈 Nifty 100 Swing Scanner</h2>

    <p>

    Stocks Scanned : <b>{len(results)}</b><br>

    Strong Buy : <b>{len(strong)}</b><br>

    Buy : <b>{len(buy)}</b><br>

    Watch : <b>{len(watch)}</b>

    </p>

    <hr>

    <h3>⭐ Strong Buy</h3>
    """

    if len(strong) == 0:
        body += "<p>No Strong Buy today.</p>"

    for stock in strong:

        body += f"""
        <p>

        <b>{stock['Symbol']}</b><br>

        CMP : ₹{stock['CMP']}<br>

        Entry : ₹{stock['Entry']}<br>

        Target : ₹{stock['Target']}<br>

        Stop Loss : ₹{stock['StopLoss']}<br>

        Score : {stock['Score']}<br>

        <a href="{stock['TradingView']}">TradingView</a> |
        <a href="{stock['Screener']}">Screener</a>

        </p>

        <hr>
        """

    body += "<h3>✅ Buy (Top 3)</h3>"

    for stock in buy:

        body += f"""
        <p>

        {stock['Symbol']}
        (Score {stock['Score']})

        </p>
        """

    body += "<h3>👀 Watch (Top 3)</h3>"

    for stock in watch:

        body += f"""
        <p>

        {stock['Symbol']}
        (Score {stock['Score']})

        </p>
        """

    body += """

    <br><br>

    Full HTML report attached.

    </body>

    </html>

    """

    message = MIMEMultipart()

    message["Subject"] = "📈 Nifty 100 Swing Scanner"

    message["From"] = EMAIL_SENDER

    message["To"] = EMAIL_RECEIVER

    message.attach(MIMEText(body, "html"))

    with open(report_file, "rb") as f:

        attach = MIMEApplication(f.read(), _subtype="html")

        attach.add_header(
            "Content-Disposition",
            "attachment",
            filename="SwingTradeReport.html",
        )

        message.attach(attach)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    server.starttls()

    server.login(
        EMAIL_SENDER,
        EMAIL_PASSWORD,
    )

    server.send_message(message)

    server.quit()

    print("\n✅ Email sent successfully!")