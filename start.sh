#!/bin/sh
# This script is used to start the services in the Docker container.

# Start the celery worker in the background
echo "Starting Celery worker..."
celery -A Core.Integrations.Schedular worker --loglevel=info &

# Start the celery beat scheduler in the background
echo "Starting Celery beat scheduler..."
celery -A Core.Integrations.Schedular beat -S redbeat.RedBeatScheduler --loglevel=info &

# Start the discord bot in the foreground
echo "Starting Discord bot..."
python -m Core.Integrations.discord_bot
