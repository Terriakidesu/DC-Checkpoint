import os
import re
import json
from glob import glob
from typing import Any, Generator

import emoji
from models import Channel, Message


MESSAGES_PATH = os.path.join("package", "Messages")


def get_messages_path():

    folders = glob(os.path.join(MESSAGES_PATH, "*"))
    folders = filter(lambda x: os.path.isdir(x), folders)

    return folders


def get_messages() -> Generator[tuple[Channel, list[Message]]]:
    for message_folder in get_messages_path():

        channel_json_path = os.path.join(message_folder, "channel.json")
        message_json_path = os.path.join(message_folder, "messages.json")

        with open(channel_json_path, "r", encoding="utf-8") as f:
            channel_json = json.load(f)

        with open(message_json_path, "r", encoding="utf-8") as f:
            messages_json = json.load(f)

        channel = Channel(**channel_json)
        messages = []

        for message_json in messages_json:

            messages.append(Message(**message_json))

        yield channel, messages


def main():

    emoji_regex = re.compile(r':[^:\s]+:', re.I)
    dc_emote_regex = re.compile(r'<a?:\w+:\d+>', re.I)

    stats: dict[str, dict[str, Any]] = {
        "channels": {

        },
        "guilds": {

        },
        "emotes": {

        },
        "messages": {
            "total_count": 0
        }
    }

    for channel, messages in get_messages():

        if channel.guild is None:
            continue

        stats["messages"]["total_count"] += len(messages)

        if stats["channels"].get(channel.id, False):
            stats["channels"][channel.id]["count"] += len(messages)
        else:
            stats["channels"][channel.id] = {
                "name": channel.name,
                "count": len(messages),
                "guild": channel.guild.name
            }

        guild_id = channel.guild.id

        if stats["guilds"].get(guild_id, False):
            stats["guilds"][guild_id]["count"] += len(messages)
        else:
            stats["guilds"][guild_id] = {
                "name": channel.guild.name,
                "count": len(messages)
            }

        for message in messages:

            content = message.Contents
            demojized = emoji.demojize(content)

            emotes: list[str] = dc_emote_regex.findall(demojized)

            for emote in emotes:
                if stats["emotes"].get(emote, False):
                    stats["emotes"][emote] += 1
                else:
                    stats["emotes"][emote] = 1

            emojis: list[str] = emoji_regex.findall(demojized)

            for emoji_name in emojis:

                if _ := emoji.get_emoji_by_name(name=emoji_name, language="en"):

                    if stats["emotes"].get(emoji_name, False):
                        stats["emotes"][emoji_name] += 1
                    else:
                        stats["emotes"][emoji_name] = 1

    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=4)


if __name__ == "__main__":
    main()
