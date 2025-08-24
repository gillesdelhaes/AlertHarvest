#!/bin/sh
set -e

# ----------------------------
# Wait for Redis
# ----------------------------
echo "Waiting for Redis..."
while ! python -c "import socket; s=socket.socket(); s.connect(('redis', 6379))"; do
    echo "Redis is unavailable - sleeping"
    sleep 1
done
echo "Redis is up!"

# ----------------------------
# Run migrations
# ----------------------------
echo "Applying Django migrations..."
python manage.py migrate

# ----------------------------
# Create default superuser if it doesn't exist
# ----------------------------
echo "Create default django superuser"
echo "Creating superuser with:"
echo "  username=$DJANGO_SUPERUSER_USERNAME"
echo "  email=$DJANGO_SUPERUSER_EMAIL"
if [ "$DJANGO_CREATE_SUPERUSER" = "1" ]; then
  if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py shell <<PYTHON
from django.contrib.auth import get_user_model
User = get_user_model()
username = "$DJANGO_SUPERUSER_USERNAME"
email = "$DJANGO_SUPERUSER_EMAIL"
password = "$DJANGO_SUPERUSER_PASSWORD"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created")
else:
    print(f"Superuser '{username}' already exists")
PYTHON
  else
    echo "⚠️ Missing superuser env vars, skipping superuser creation"
  fi
fi

# ----------------------------
# Collect static files
# ----------------------------
echo "Collecting static files..."
python manage.py collectstatic --noinput

# ----------------------------
# Execute the command passed in compose
# ----------------------------
exec "$@"