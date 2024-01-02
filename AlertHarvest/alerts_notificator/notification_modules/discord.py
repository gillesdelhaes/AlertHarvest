import requests
import configparser

def read_discord_config(file_path='notification_config/discord.conf'):
    config = configparser.ConfigParser()
    try:
        with open(file_path, 'r') as config_file:
            config.read_file(config_file)
            discord_config = config['DiscordConfig']
    except FileNotFoundError:
        print(f"Config file not found: {file_path}")
        return None
    except KeyError:
        print(f"Error reading 'DiscordConfig' section from {file_path}")
        return None
    discord_config = config['DiscordConfig']
    
    webhook_url = discord_config.get('webhook_url')
    
    return webhook_url

def send_notification(alert):
    webhook_url = read_discord_config()
    body = f"Received alert notification: {alert.source}, {alert.location}, {alert.message}, {alert.last_occurrence}"
    payload = {'content': body}
    requests.post(webhook_url, json=payload)
