import json
import smtplib
from kafka import KafkaConsumer, KafkaProducer

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
ALERT_TOPIC = 'alerts'
SUPPRESSION_TOPIC = 'suppressions'

# Email configuration
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_USER = 'alert@company.com'
EMAIL_PASS = 'password'

# Function to send email notifications
def send_email(subject, body, to_email):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(EMAIL_USER, to_email, message)

# Kafka Consumer for alerts
consumer = KafkaConsumer(
    ALERT_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Kafka Producer for suppressions
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Alert processing loop
for message in consumer:
    alert = message.value
    
    # Check if the alert is suppressed
    suppression_check = producer.send(SUPPRESSION_TOPIC, {'alert_id': alert['id']})
    suppression_response = suppression_check.get(timeout=10)

    if suppression_response.value != b'suppressed':
        # Send email notification for active alerts
        send_email(
            subject=f"Alert: {alert['severity']} - {alert['description']}",
            body=f"Details:\n{json.dumps(alert, indent=2)}",
            to_email='oncall@company.com'
        )


