import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, 'icon.ico')

default_settings = {
    "discord_comments": {
        "1": "Connect to Discord? If set to true, application will try to connect to discord in order to set your presence.",
        "2": "Set it to false if you don't want to connect to Discord.",
        "3": "The default value is 'true'.",
        "4": "Enter your Discord Client ID. You can find it in your Discord Developer Portal.",
        "5": {
            "1":"Enter your Discord Large Image Key. You can find it in your Discord Developer Portal.",
            "2":"You can use links as well.",
            "3":"The default value is 'default_image'."
        }
    },
    "connect_to_discord": True,
    "discord_client_id": "1150680286649143356",
    "large_image_key": "default_image",
    "use_playing_status": False,

    "root_playlist_folder_comment": {
        "1": "Specify the directory where your playlists are saved. You can change this path if needed.",
        "2": "The default value is 'playlists'."
    },
    "root_playlist_folder": "playlists",
    "default_playlist_comment": "Enter the name of the default playlist that will be loaded initially. You can modify this name as required.",
    "default_playlist": "default",
    "colorization_color_comment": {
        "1": "Enter the hex color code of the accent color. You can modify this color as required.",
        "2": "If set to 'automatic' the application will use the system's accent color.",
        "3": "The default value is 'automatic'."
    },
    "colorization_color": "automatic"
}