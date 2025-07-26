# 🌤 Intelligent Weather Detector App

## 🔍 Description

A serverless weather monitoring and alerting system that:
- Collects weather data from wttr.in
- Stores logs in Azure Blob Storage
- Sends daily weather summaries via email (6 AM)
- Will include intelligent alerting logic and multi-channel notifications (SMS, Telegram, WhatsApp)
- Future plans include adding a web/mobile dashboard and ML-based forecasting

---

## 📦 Current Components

### 1. **Weather Logging Function**
- Trigger: Every 30 minutes
- Logs: Current temp, tomorrow’s temp (12PM), city-specific
- Storage: Appends to `weather.log` in Azure Blob

### 2. **Daily Email Function** *(Planned)*
- Trigger: 6:00 AM UTC
- Sends: Email with current weather and forecast
- Service: SendGrid (or other)

---

## 🧭 Roadmap

### ✅ Phase 1: MVP + Email
- [x] Azure TimerTrigger to collect weather
- [ ] Send weather summary via email
- [ ] Include humidity, wind, and condition in logs

### 📲 Phase 2: App Frontend
- Web/mobile dashboard
- View logs, alerts, and settings

### 📤 Phase 3: Alerts & Notifications
- Rule-based alerts
- Multi-channel (email, SMS, Telegram, WhatsApp)

### 🧠 Phase 4: Intelligence & ML
- Train on historical data
- Add predictive logic
- Generate plain-language insights

---

## 🔧 Environment Variables

| Name                         | Description                          |
|------------------------------|--------------------------------------|
| `AZURE_STORAGE_CONNECTION_STRING` | For accessing blob storage         |
| `CITY_NAME`                  | Default city for weather data       |
| `TIMER_SCHEDULE`             | CRON for log function (UTC)         |
| `SENDGRID_API_KEY`           | For sending email notifications     |
| `EMAIL_RECIPIENT`            | Who to send daily summaries to      |
| `BLOB_CONTAINER_NAME`        | Default: `weather-logs`             |

---

## ⏰ CRON Schedules

| Function        | Schedule           | Description             |
|-----------------|--------------------|-------------------------|
| Weather Logger  | `0 */30 * * * *`   | Every 30 minutes        |
| Email Sender    | `0 0 6 * * *`      | Every day at 6 AM UTC   |

---

## 🔮 Future Considerations

- Daily logs in separate files: `weather_YYYYMMDD.log`
- HTML email formatting
- React frontend with weather history
- Alert preference settings per user
- Graph analytics dashboard
