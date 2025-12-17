Surveillance et analyse des logs Docker (prototype)

This workspace contains a small FastAPI app and a basic ELK + Filebeat setup to collect container logs.

Quick start

1. Build and start all services (FastAPI, MySQL, Elasticsearch, Kibana, Filebeat):

```bash
docker-compose up -d --build
```

2. Wait for services to start. Kibana: http://localhost:5601 — Elasticsearch: http://localhost:9200

3. Filebeat is configured to read Docker container logs from the host path `/var/lib/docker/containers` and ship them to Elasticsearch. If you run on Windows WSL or a different Docker setup, adjust the mount paths in `docker-compose.yml`.

Notes & next steps
- Load Filebeat index templates / dashboards: you can execute `docker exec filebeat filebeat setup` to load dashboards and index templates into Kibana/Elasticsearch.
- Configure retention / ILM in Elasticsearch: basic ILM is enabled in the Filebeat config but you should review ILM policies in Kibana Management > Stack Management > Index Lifecycle Policies.
- Alerts: set up Kibana alerts or use external tooling (Slack/email). Placeholders for alert webhook URLs are left out for security.
- For production use: enable security in Elasticsearch, provide credentials, set resource limits, and tune JVM options.

Files added:
- `docker-compose.yml` — adds `elasticsearch`, `kibana`, `filebeat` services
- `filebeat/filebeat.yml` — Filebeat configuration to collect Docker logs
"# fastapi_todo" 
