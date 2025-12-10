import json

from typing import Any


def show():
    with open("stats.json", "r", encoding="utf-8") as f:
        data: dict[str, dict[str, Any]] = json.load(f)

    top_guilds = sorted(data["guilds"].values(),
                        key=lambda x: x["count"], reverse=True)
    top_channels = sorted(data["channels"].values(),
                          key=lambda x: x["count"], reverse=True)
    top_emojis = sorted(data["emotes"],
                        key=lambda k: data["emotes"][k], reverse=True)
    total_emojis = sum(data["emotes"].values())
    total_messages = data["messages"]["total_count"]

    print(f"""
Messages Sent: {total_messages}
Top Server: {top_guilds[0]["name"]}
Emojis Used: {total_emojis}
Favorite Emoji: {top_emojis[0]}
    """)

    print("Top Emojis:")
    for i in range(5):
        print(f"#{i+1} {top_emojis[i]}")


if __name__ == "__main__":
    show()
