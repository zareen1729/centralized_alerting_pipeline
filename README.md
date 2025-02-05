# Centralized Alerting Pipeline

## Overview
This project demonstrates a centralized alerting system to manage and suppress alerts efficiently.

## Architecture
Alert Ingestion API: Receives incoming alerts.

Alert Processor: Applies suppression rules and processes alerts.

Notification Service: Sends email notifications for active alerts.

## Architecture Diagram


```plaintext
+----------------------+       +--------------------------+       +------------------------+
|  Alert Ingestion API | ----> | Alert Processor (Rules)  | ----> | Notification Service   |
+----------------------+       +--------------------------+       +------------------------+
        (Flask)                    (Suppression Logic)               (Email Notifications)
