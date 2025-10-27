## Prerequisites

Make sure you have the following installed:

- **PHP 8.1+**
- **Composer**
- **Node.js & npm**
- **Git**
- **Supabase account** (I'll send an invitation email soon)

---

## ⚙️ Setup Instructions

1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>


2. Copy the Example Environment File

Copy the example .env file and make your own configuration file:

cp .env.example .env

After doing this, to make the process easier, select all and paste the following code in .env file:

APP_NAME=Laravel
APP_ENV=local
APP_KEY=base64:ieDlE6P7ou5LrUXqVhaI/o2846oeOTi9nEjWkRAcIKs=
APP_DEBUG=true
APP_URL=http://127.0.0.1:8000

APP_LOCALE=en
APP_FALLBACK_LOCALE=en
APP_FAKER_LOCALE=en_US

APP_MAINTENANCE_DRIVER=file

PHP_CLI_SERVER_WORKERS=4

BCRYPT_ROUNDS=12

LOG_CHANNEL=stack
LOG_STACK=single
LOG_DEPRECATIONS_CHANNEL=null
LOG_LEVEL=debug

DB_CONNECTION=sqlite
# DB_HOST=127.0.0.1
# DB_PORT=3306
# DB_DATABASE=laravel
# DB_USERNAME=root
# DB_PASSWORD=

SESSION_DRIVER=file
SESSION_LIFETIME=120
SESSION_ENCRYPT=false
SESSION_PATH=/
SESSION_DOMAIN=null

BROADCAST_CONNECTION=log
FILESYSTEM_DISK=local
QUEUE_CONNECTION=database

CACHE_STORE=file

MEMCACHED_HOST=127.0.0.1

REDIS_CLIENT=phpredis
REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

MAIL_MAILER=log
MAIL_SCHEME=null
MAIL_HOST=127.0.0.1
MAIL_PORT=2525
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_FROM_ADDRESS="hello@example.com"
MAIL_FROM_NAME="${APP_NAME}"

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=
AWS_USE_PATH_STYLE_ENDPOINT=false

VITE_APP_NAME="${APP_NAME}"

VITE_SUPABASE_URL=https://lmqguixutnwruuckvqpj.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxtcWd1aXh1dG53cnV1Y2t2cXBqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEwMzE2MDYsImV4cCI6MjA3NjYwNzYwNn0.djIlwRwr7iwtRtvS3Ayh9-8I9b7sX42kiYAFhg_-goE






3. Install Dependencies
Backend (Laravel):
composer install

Frontend (Vite):
npm install

4. Generate Application Key
php artisan key:generate

5. Run the Development Servers
Laravel backend:
php artisan serve


In a separate terminal:
npm run dev


Visit:
http://127.0.0.1:8000
