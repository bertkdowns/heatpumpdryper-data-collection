# Deletes all data in the influx database.

docker compose exec influxdb influx delete \
  --bucket bucket1 \
  --start '1970-01-01T00:00:00Z' \
  --stop "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \