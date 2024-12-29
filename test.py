from pyrogram import Client, filters, idle
import m3u8
import requests

# Replace with your actual Pyrogram API credentials
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"

app = Client(
    "jiocinemaripbot",
    bot_token="7574472282:AAEJ_T_pE6ZXnVZnxSIrW75XVvvYoSZU0FU",
    api_id="5360874",
    api_hash="4631f40a1b26c2759bf1be4aff1df710",
    sleep_threshold=30
)

# Global variables to store user selections and m3u8 URL
selected_quality = None
selected_language = None
m3u8_url = None
chat_id = None  # Store the chat ID to send messages back

@app.on_message(filters.command('start'))
def start_command(client, message):
    global chat_id
    chat_id = message.chat.id
    message.reply_text('Send me an m3u8 URL to get started.')


def m3u8_to_dict(m3u8_obj):
    """Converts an m3u8.model.M3U8 object to a dictionary."""

    m3u8_dict = {}
    for key, value in m3u8_obj.__dict__.items():
        if isinstance(value, list):
            # Convert lists of Playlist objects
            m3u8_dict[key] = [
                {
                    "stream_info": {
                        "bandwidth": p.stream_info.bandwidth,
                        "resolution": p.stream_info.resolution,
                        "codecs": p.stream_info.codecs,
                        "audio": p.stream_info.audio,
                        # Add other stream_info attributes as needed
                    },
                    # Add other Playlist attributes as needed
                }
                for p in value
            ]
        else:
            m3u8_dict[key] = value
    return m3u8_dict


@app.on_message(filters.private)
def handle_m3u8_url(client, message):
    global m3u8_url, chat_id
    m3u8_url = message.text
    chat_id = message.chat.id  # Update chat_id for each message

    try:
        playlist = m3u8.load(m3u8_url)

        qualities = set()
        languages = set()
        playlist = m3u8_to_dict(playlist)
        for playlist in playlist.playlists:
            qualities.add(playlist.stream_info.resolution)
            if playlist.stream_info.audio:
                languages.add(playlist.stream_info.audio)

        # Create buttons for quality and language selection (using inline queries)
        buttons = []
        for quality in qualities:
            buttons.append(
                {'text': f"{quality}", 'switch_inline_query_current_chat': f"quality:{quality}"}
            )
        for language in languages:
            buttons.append(
                {'text': f"{language}", 'switch_inline_query_current_chat': f"language:{language}"}
            )

        message.reply_text(
            'Select quality and language:',
            reply_markup={"inline_keyboard": [buttons]}
        )

    except Exception as e:
        message.reply_text(f"Error processing URL: {e}")


@app.on_message(filters.InlineQuery)
def handle_button_click(client, inline_query):
    global selected_quality, selected_language
    query = inline_query.query
    data = query.split(':')

    if data[0] == 'quality':
        selected_quality = data[1]
    elif data[0] == 'language':
        selected_language = data[1]

    # Answer the inline query with a placeholder result
    inline_query.answer(
        results=[
            {
                'type': 'article',
                'id': '1',
                'title': f"Selected: {query}",
                'input_message_content': {'message_text': f"Selected: {query}"}
            }
        ],
        cache_time=1
    )


@app.on_message(filters.command('done'))
def download(client, message):
    global m3u8_url, selected_quality, selected_language, chat_id
    if not all([m3u8_url, selected_quality, selected_language]):
        app.send_message(chat_id, "Please select quality and language first.")
        return

    try:
        # Construct the stream URL with selected quality and language
        stream_url = m3u8_url  # You'll need to modify this to include quality and language parameters

        # Download the stream using Pyrogram
        app.download_media(stream_url, file_name="download.mp4")

        # Send the downloaded file to the user
        app.send_document(chat_id, document="download.mp4")

    except Exception as e:
        app.send_message(chat_id, f"Error downloading: {e}")

app.start()
print("bot started")
idle()
app.stop()
