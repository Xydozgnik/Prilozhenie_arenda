#!/bin/sh
# Ежедневный бэкап данных PocketBase. Установка: добавить в crontab root на сервере:
#   17 4 * * * /opt/porog/deploy/backup.sh >> /var/log/porog-backup.log 2>&1
set -eu

BACKUP_DIR=/opt/backups
KEEP_DAYS=14
STAMP=$(date +%Y%m%d-%H%M%S)

mkdir -p "$BACKUP_DIR"

# Имя тома: <папка-проекта>_pb_data — определяем автоматически
VOLUME=$(docker volume ls --format '{{.Name}}' | grep '_pb_data$' | head -n 1)
if [ -z "$VOLUME" ]; then
  echo "Том pb_data не найден" >&2
  exit 1
fi

docker run --rm -v "$VOLUME":/data:ro -v "$BACKUP_DIR":/b alpine \
  tar czf "/b/pb_data-$STAMP.tar.gz" -C /data .

# Удаляем бэкапы старше KEEP_DAYS дней
find "$BACKUP_DIR" -name 'pb_data-*.tar.gz' -mtime +$KEEP_DAYS -delete

echo "OK: $BACKUP_DIR/pb_data-$STAMP.tar.gz"
