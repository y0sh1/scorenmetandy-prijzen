# Scoren met Andy Prijzen Checker

Dit project is een Python-applicatie die brandstofprijzen van de website "Scoren met Andy" (scorenmetandy.nl) extraheert en deze informatie via een Slack-webhook verstuurt.

## Installatie

1. Zorg ervoor dat u Docker en Docker Compose op uw machine hebt geïnstalleerd.
2. Clone deze repository naar uw lokale machine.

```bash
git clone <uw-repository-url>
cd <uw-repository-directory>
```

## Configuratie

Stel de Slack Webhook URL in als een omgevingsvariabele. U kunt dit doen door een `.env` bestand te maken in de hoofdmap van het project:

```env
SLACK_WEBHOOK_URL=uw_slack_webhook_url_hier
```

## Gebruik

Start de Docker containers met behulp van Docker Compose:

```bash
docker-compose up --build
```

De service zal nu de brandstofprijzen extraheren en deze via de geconfigureerde Slack-webhook versturen.

## Technische Details

- Gebruikt Python met de `requests` en `BeautifulSoup` libraries om webpagina's uit te lezen en data te verwerken.
- Docker en Docker Compose zorgen voor een gemakkelijke setup en uitvoering van de service.
