# Развёртывание сервера «Порога»

Стек: **PocketBase** (API + БД + файлы) за **Caddy** (HTTPS, автоматические сертификаты Let's Encrypt). Хостинг: Selectel VDS.

## Что получится

- `https://porog-app.ru` — статика: страница-приглашение `i.html`, позже веб-экран арендатора (Flutter Web).
- `https://api.porog-app.ru` — API PocketBase; админка — `https://api.porog-app.ru/_/`.

## Подготовка (один раз)

1. Создать VDS в Selectel: Ubuntu 24.04, 1 vCPU / 1 ГБ RAM / 10 ГБ NVMe, публичный IPv4, SSH-ключ.
2. В DNS домена `porog-app.ru` создать A-записи на IP сервера:
   - `porog-app.ru` → IP
   - `www.porog-app.ru` → IP
   - `api.porog-app.ru` → IP
3. Подключиться по SSH и поставить Docker:
   ```sh
   curl -fsSL https://get.docker.com | sh
   ```
4. Забрать репозиторий и перейти в ветку сервера:
   ```sh
   git clone https://github.com/Xydozgnik/Prilozhenie_arenda.git /opt/porog
   cd /opt/porog && git checkout server
   ```

## Запуск

```sh
cd /opt/porog/deploy
mkdir -p www
cp ../i.html www/index.html
docker compose up -d --build
```

Caddy сам получит сертификаты, как только DNS укажет на сервер (проверка: `curl -I https://porog-app.ru`).

## После запуска

1. Открыть `https://api.porog-app.ru/_/` и создать админа PocketBase (первый вход предложит регистрацию).
2. Поставить бэкап в cron: `17 4 * * * /opt/porog/deploy/backup.sh >> /var/log/porog-backup.log 2>&1`
3. Отключить вход по паролю в SSH (оставить только ключи), включить `ufw`: разрешить 22, 80, 443.

## Обновление

```sh
cd /opt/porog && git pull
cd deploy && docker compose up -d --build
```

## Заметки

- Версия PocketBase фиксируется в `Dockerfile` (`PB_VERSION`); обновлять осознанно, читая changelog — до 1.0 возможны ломающие изменения.
- Бэкапы лежат в `/opt/backups` (14 дней). Для надёжности позже добавить выгрузку в S3 Selectel.
