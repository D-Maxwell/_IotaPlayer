# Music Player Application

A feature-rich music player application with playlist management, playback controls, song information display, volume and progress tracking, Discord integration, and more.

## Features

### TODO:
- **Move song slider:** So we can skip to a certain moment in the song.
    - Currently it only shows the current song progress. Can't move to a certain moment in the song.
- **Add favourites:** Add songs to a playlist as favourites.
- **Get MacOS accent color:** So we can use the system's accent color.

### Core Features

- **Playlists Management:**
  - **Load Playlist:** Load playlists from a specified directory.
  - **Reload Playlists:** Refresh the list of available playlists.
  - **Delete Playlist:** Remove a selected playlist.
  - **Create/Edit Playlist:** Use the [Playlist Maker](#playlist-maker) to create or edit playlists.

- **Music Playback Controls:**
  - **Play/Pause/Resume/Stop:** Start, pause, resume, or stop the currently playing song.
  - **Previous/Next:** Skip to the previous or next song in the playlist.
  - **Loop/Shuffle:** Toggle loop and shuffle modes.

- **Song Information:**
  - **Display Song Info:** Show details of the currently playing song (artist and title).
  - **Update Window Title:** Reflect the current song info and playlist in the window title.

- **Volume Control:**
  - **Adjust Volume:** Change playback volume via a slider.

- **Progress Tracking:**
  - **Track Progress:** Display and update the progress of the currently playing song.
  - **Format Time:** Convert elapsed time and total duration into a readable format.

- **Discord Integration:**
  - **Update Discord Status:** Display the current song info in Discord status.
  - **Check Discord Connection:** Monitor and display connection status to Discord.

- **Key Bindings:**
  - **Media Keys:** Handle media keys for play/pause, next, and previous track.

- **External Actions:**
  - **Open YouTube:** Open the YouTube video for the current song, if available.

### User Interface

- **Playlists and Songs Display:**
  - **Playlist List:** Show available playlists and their song counts.
  - **Song List:** Display the list of songs in the currently loaded playlist.

- **Controls and Layouts:**
  - **Control Buttons:** Various buttons for playback control, playlist management, and external actions.
  - **Sliders:** For adjusting volume and tracking song progress.
  - **Labels:** For displaying song info, playback time, and Discord status.

- **Dialogs:**
  - **Open Playlist Dialog:** Select and load playlists.

### Logging

- **Logging Setup:**
  - **Console Logging:** Output logs to the console.
  - **File Logging:** Save logs to a rotating file for persistent records.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/vorlie/vorlies-music-player.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd music-player
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure you have the necessary environment variables and configuration files:**
    - Create a `config.json` file with necessary configuration details.
        - Otherwise the application will generate a default configuration.
    - Add your Discord client ID in the appropriate place if needed.
        - The default value is '1150680286649143356'.

## Usage
0. **Install the required dependencies:**
    - If you already have python installed, skip this step.
        - [`Python`](https://www.python.org/downloads/)
        
    - Install the required dependencies.
        ```bash
        pip install -r requirements.txt --ignore-requires-python
        ```

1. **Run the application:**

    ```bash
    python main.py
    ```

2. **Control the application:**
    - Use the UI buttons to control playback, manage playlists, and access external actions.
    - Use media keys on your keyboard to control playback.

3. **Create/Edit Playlists:**
    - Access the Playlist Maker to create or edit playlists.

4. **Discord Integration:**
    - The application will automatically update your Discord status with the current song info if connected.

## Configuration

- **`config.json`:** Place your configuration settings here. Example:
    - If file is not present, application will create it with default values.
    ```json
    {   
        "discord_client_id_comment": "Enter your Discord Client ID. You can find it in your Discord Developer Portal. You can modify this ID as required. It will be used to connect to Discord and will change the name of the application that's seen in Discord. The default value is '1150680286649143356'.",
        "discord_client_id": "1150680286649143356",

        "root_playlist_folder_comment": "Specify the directory where your playlists are saved. You can change this path if needed. The default value is 'playlists'.",
        "root_playlist_folder": "playlists",

        "default_playlist_comment": "Enter the name of the default playlist that will be loaded initially. You can modify this name as required.",
        "default_playlist": "",

        "colorization_color_comment": "Enter the hex color code of the accent color. You can modify this color as required. The default value is 'automatic'. Which will use the system's colorization color.",
        "colorization_color": "automatic"
    }
    ```

- **Logging Configuration:**
    - In `musicplayer.py` there are commented logging configurations. Uncomment them to use them.
        - Logs are written to `combined_app.log` for application and discord logs.

## Playlist Maker

The `PlaylistMaker` class provides a user-friendly interface for creating and managing playlists. It allows users to select folders containing songs, add songs manually, and save playlists in JSON format. 

### Features

- **Select Folder**: Automatically populate the playlist with songs from a selected folder.
- **Add Songs Manually**: Enter song details manually including artist, title, YouTube ID, and song path.
- **Save Playlist**: Save the created playlist in JSON format.
- **Open Existing Playlist**: Load and edit an existing playlist.
- **Edit Songs**: Double-click on a song entry to edit its details.
- **Delete Songs**: Select a song and press the Delete key to remove it.

### How to Use

1. **Select Folder**:
   - Click on the "Select Folder" button to choose a folder containing MP3 files.
   - The application will automatically process the folder and add all MP3 files matching the naming pattern to the playlist.

2. **Add Songs Manually**:
   - Fill in the "Artist", "Title", "YouTube ID" (optional), and "Song Path" fields.
   - Click the "Add Song" button to add the song to the playlist.

3. **Save Playlist**:
   - Enter a name for the playlist in the "Enter playlist name" field.
   - Click the "Save Playlist" button to save the playlist as a JSON file.

4. **Open Existing Playlist**:
   - Click the "Open Existing Playlist" button to load a playlist.
   - Select the JSON file of the playlist you want to open.

5. **Edit and Delete Songs**:
   - To edit a song, double-click on the corresponding cell in the table.
   - To delete a song, select the row and press the Delete key.

### Naming Scheme

For automatic recognition, the song files in the selected folder should follow this naming scheme:
- **Artist**: The name of the artist.
- **Title**: The title of the song.
- **YouTube ID**: (Optional) The YouTube ID for the song.
    ```
    Artist - Title [YouTube ID].mp3
    ```
    **Example(s)**:
    ```
        Artist - Title [dQw4w9WgXcQ].mp3
        Artist (feat. Artist) - Title (Bass Boosted) [dQw4w9WgXcQ].mp3
    ```

### Example playlist json result

```json
{
    "playlist_name": "name_test",
    "song_count": 2,
    "songs": [
        {
            "artist": "Artist 1",
            "title": "Title 1",
            "youtube_id": "dQw4w9WgXcQ",
            "path": "C:\\Users\\USER\\Music\\FOLDER\\Artist 1 - Title 1 [dQw4w9WgXcQ].mp3",
            "playlist": "name_test"
        },
        {
            "artist": "Artist 2",
            "title": "Title 2",
            "youtube_id": "dQw4w9WgXcQ",
            "path": "C:\\Users\\USER\\Music\\FOLDER\\Artist 2 - Title 2 [dQw4w9WgXcQ].mp3",
            "playlist": "name_test"
        }
    ]
}
```

## Troubleshooting

- **Ensure all dependencies are installed:**
  Verify the installation of all required packages.
    ```
    PyQt5==5.15.10
    pygame==2.6.0
    pypresence==4.3.0
    mutagen==1.47.0
    pynput==1.7.7
    pyqtdarktheme==2.1.0

    # If planning to build from source
    pyinstaller==6.6.0
    ```

- **Check Discord connection:**
  Ensure your Discord client ID is correct and that you are connected to Discord.

- **Review logs:**
  Check `combined_app.log` for detailed logging information if issues arise.

## Contributing

Feel free to submit issues, propose enhancements, or contribute code through pull requests. Please follow the standard guidelines for contributions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Thanks

- **[PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro)**: A set of Python bindings for the Qt application framework, which provides the GUI capabilities for this application.
- **[qdarktheme](https://pypi.org/project/pyqtdarktheme/)**: A library for applying dark themes to PyQt5 applications, enhancing the visual appeal of the interface.
- **[pygame](https://www.pygame.org/)**: A cross-platform set of Python modules designed for writing video games, providing functionality for sound and music.
- **[pypresence](https://pypi.org/project/pypresence/)**: A Python library for integrating with Discord's Rich Presence, allowing you to display custom activity information.
- **[mutagen](https://mutagen.readthedocs.io/en/latest/)**: A Python module used for handling audio metadata, enabling the application to read and write metadata in audio files.
- **[pynput](https://pynput.readthedocs.io/en/latest/)**: A library for controlling and monitoring input devices, such as keyboards and mice.
- **[pyinstaller](https://www.pyinstaller.org/)**: A tool for converting Python applications into stand-alone executables, allowing for easier distribution and deployment.
