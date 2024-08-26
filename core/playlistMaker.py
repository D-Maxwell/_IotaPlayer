import re, logging, json, os, random
from PyQt5.QtWidgets import QDialog, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class PlaylistManager:
    def __init__(self):
        self.playlists = {}
        self.shuffle_states = {}
        self.shuffled_songs = {}

        try:
            with open('./config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            print("Configuration file not found. Using default settings.")
            config = {"root_playlist_folder": "playlists"}
        except json.JSONDecodeError:
            print("Error decoding the configuration file.")
            config = {"root_playlist_folder": "playlists"}

        self.playlists_dir = config.get('root_playlist_folder', 'playlists')
        if not os.path.exists(self.playlists_dir):
            os.makedirs(self.playlists_dir)
            print(f"Created playlists directory: {self.playlists_dir}")

    def load_playlist(self, playlist_name):
        """Load a playlist by name from the playlists directory."""
        playlist_path = os.path.join(self.playlists_dir, f"{playlist_name}.json")
        
        if not os.path.isfile(playlist_path):
            raise FileNotFoundError(f"Playlist file not found: {playlist_path}")

        try:
            with open(playlist_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON in playlist file: {playlist_path}")
        except IOError as e:
            raise IOError(f"Error reading playlist file: {playlist_path}") from e

        playlist_name = data.get("playlist_name", playlist_name)
        playlist_image = data.get("playlist_large_image_key", None)
        songs = data.get("songs", [])

        self.playlists[playlist_name] = songs
        self.shuffle_states[playlist_name] = False
        self.shuffled_songs[playlist_name] = []

        return playlist_name, songs, playlist_image

    def shuffle_songs(self, playlist_name):
        """Shuffle the songs for a specific playlist."""
        if playlist_name in self.playlists:
            songs = self.playlists[playlist_name][:]
            random.shuffle(songs)
            self.shuffled_songs[playlist_name] = songs
            self.shuffle_states[playlist_name] = True


class PlaylistMaker(QDialog):
    def __init__(self, icon_path):
        super().__init__()
        self.icon_path = icon_path
        self.setWindowTitle("Iota Player • Playlist Maker")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, 1700, 900)
        
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        
        self.initUI()
    
    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Left frame layout
        self.left_frame = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(10)
        self.left_frame.setLayout(self.left_layout)
        self.left_frame.setFixedWidth(300)
        self.layout.addWidget(self.left_frame, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.folder_label = QLabel("Select folder containing songs:")
        self.left_layout.addWidget(self.folder_label)

        self.folder_path_label = QLabel("(folder name)")
        self.left_layout.addWidget(self.folder_path_label)

        self.select_folder_button = QPushButton("Select Folder")
        self.select_folder_button.setFixedWidth(150)
        self.select_folder_button.clicked.connect(self.select_folder)
        self.left_layout.addWidget(self.select_folder_button)

        self.playlist_name_label = QLabel("Enter playlist name:")
        self.left_layout.addWidget(self.playlist_name_label)

        self.playlist_name_input = QLineEdit()
        self.playlist_name_input.setPlaceholderText("Playlist Name")
        self.left_layout.addWidget(self.playlist_name_input)

        self.discord_large_image_key = QLabel("Set a playlist image (Discord presence):")
        self.left_layout.addWidget(self.discord_large_image_key)
        
        self.discord_large_image_key_input = QLineEdit()
        self.discord_large_image_key_input.setPlaceholderText("Use an image URL or an image key")
        self.left_layout.addWidget(self.discord_large_image_key_input)
        
        self.add_songs_label = QLabel("Add songs manually:")
        self.left_layout.addWidget(self.add_songs_label)

        self.artist_input = QLineEdit()
        self.artist_input.setPlaceholderText("Artist")
        self.left_layout.addWidget(self.artist_input)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")
        self.left_layout.addWidget(self.title_input)

        self.album_input = QLineEdit()
        self.album_input.setPlaceholderText("Album")
        self.left_layout.addWidget(self.album_input)

        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Genre")
        self.left_layout.addWidget(self.genre_input)

        self.picture_path_input = QLineEdit()
        self.picture_path_input.setPlaceholderText("Picture Path")
        self.left_layout.addWidget(self.picture_path_input)

        self.youtube_id_input = QLineEdit()
        self.youtube_id_input.setPlaceholderText("YouTube ID")
        self.left_layout.addWidget(self.youtube_id_input)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Song Path")
        self.left_layout.addWidget(self.path_input)

        self.button_layout = QHBoxLayout()
        self.left_layout.addLayout(self.button_layout)

        self.add_song_button = QPushButton("Add Song")
        self.add_song_button.clicked.connect(self.add_song)
        self.button_layout.addWidget(self.add_song_button)

        self.save_playlist_button = QPushButton("Save Playlist")
        self.save_playlist_button.clicked.connect(self.save_playlist)
        self.button_layout.addWidget(self.save_playlist_button)
        
        self.open_playlist_button = QPushButton("Open Existing Playlist")
        self.open_playlist_button.clicked.connect(self.open_playlist)
        self.button_layout.addWidget(self.open_playlist_button)

        self.note_information = QLabel(
            """
            <b>Notes:</b><br><br>
            <ul>
                <li><b>Select a folder</b> with songs to automatically populate the playlist or add songs manually.</li>
                <li><b>Add songs manually</b> by entering the artist, title, genre, picture path, YouTube ID (optional), and song path.</li>
                <li><b>Use the full path</b> to the song file when adding manually.</li>
                <li><b>Follow the file naming format</b> for automatic recognition:<br>
                    <i>Artist - Title [YouTube ID].mp3</i><br>
                    Example: <i>Adele - Hello [dQw4w9WgXcQ].mp3</i>
                </li>
                <li><b>To delete a song</b>, select the row in the table and press the <b>Delete</b> key on your keyboard.</li>
                <li><b>Click on a row</b> in the table to select a song before performing any actions.</li>
                <li><b>Double-click</b> on a cell in the table to <b>edit</b> its content.</li>
            </ul>
            """
        )

        self.note_information.setWordWrap(True)
        self.left_layout.addWidget(self.note_information)
        
        # Right frame layout
        self.right_frame = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_frame.setLayout(self.right_layout)
        self.layout.addWidget(self.right_frame)

        # Table view for song list
        self.song_table = QTableWidget()
        self.song_table.setColumnCount(8)
        self.song_table.setHorizontalHeaderLabels(["Artist", "Title", "Album", "Genre", "Picture Path", "Picture Link", "YouTube ID", "Song Path"])
        self.right_layout.addWidget(self.song_table)
        self.song_table.setColumnWidth(0, 150)
        self.song_table.setColumnWidth(1, 150)
        self.song_table.setColumnWidth(2, 150)
        self.song_table.setColumnWidth(3, 150)
        self.song_table.setColumnWidth(4, 150)
        self.song_table.setColumnWidth(5, 150)
        self.song_table.setColumnWidth(6, 150)
        self.song_table.setColumnWidth(7, 450)
        self.song_table.itemChanged.connect(self.update_song_data)
        self.songs = []

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            selected_indexes = self.song_table.selectionModel().selectedRows()
            if selected_indexes:
                for index in sorted(selected_indexes, reverse=True):
                    row = index.row()
                    self.song_table.removeRow(row)
                    if row < len(self.songs):
                        del self.songs[row]

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path_label.setText(folder)
            self.process_folder(folder)
    
    def process_folder(self, folder):
        self.songs = []
        self.song_table.setRowCount(0)
        song_files = [f for f in os.listdir(folder) if f.endswith(".mp3")]

        for filename in song_files:
            match = re.match(r'(.+) - (.+) \[([^\]]*)\]\.mp3$', filename)
            if match:
                artist, title, youtube_id = match.groups()
                song_path = os.path.join(folder, filename)
                self.songs.append({
                    "artist": artist,
                    "title": title,
                    "genre": "",  # Default empty genre
                    "album": "",  # Default empty album
                    "picture_path": "",  # Default empty picture path
                    "picture_link": "",  # Default empty picture link
                    "youtube_id": youtube_id,
                    "path": song_path.replace("\\", "/")
                })

        self.add_song_to_table()

    def add_song_to_table(self):
        self.song_table.setRowCount(len(self.songs))
        for row, song in enumerate(self.songs):
            artist = song.get('artist', 'Unknown Artist')
            title = song.get('title', 'Unknown Title')
            album = song.get('album', 'Unknown Album')
            genre = song.get('genre', 'Unknown Genre')
            picture_path = song.get('picture_path', '')
            picture_link = song.get('picture_link', '')
            youtube_id = song.get('youtube_id', '')
            path = song.get('path', '')

            self.song_table.setItem(row, 0, QTableWidgetItem(artist))
            self.song_table.setItem(row, 1, QTableWidgetItem(title))
            self.song_table.setItem(row, 2, QTableWidgetItem(album))
            self.song_table.setItem(row, 3, QTableWidgetItem(genre))
            self.song_table.setItem(row, 4, QTableWidgetItem(picture_path))
            self.song_table.setItem(row, 5, QTableWidgetItem(picture_link))
            self.song_table.setItem(row, 6, QTableWidgetItem(youtube_id))
            self.song_table.setItem(row, 7, QTableWidgetItem(path))

    def update_song_data(self, item):
        row = item.row()
        column = item.column()
        value = item.text()

        if row < len(self.songs):
            if column == 0:
                self.songs[row]['artist'] = value
            elif column == 1:
                self.songs[row]['title'] = value
            elif column == 2:
                self.songs[row]['album'] = value
            elif column == 3:
                self.songs[row]['genre'] = value
            elif column == 4:
                self.songs[row]['picture_path'] = value
            elif column == 5:
                self.songs[row]['picture_link'] = value
            elif column == 6:
                self.songs[row]['youtube_id'] = value
            elif column == 7:
                self.songs[row]['path'] = value

    def add_song(self):
        artist = self.artist_input.text().strip()
        title = self.title_input.text().strip()
        album = self.album_input.text().strip()
        genre = self.genre_input.text().strip()  # Get genre input
        picture_path = self.picture_path_input.text().strip()  # Get picture path input
        picture_link = self.picture_link_input.text().strip()
        youtube_id = self.youtube_id_input.text().strip()
        path = self.path_input.text().strip()

        if artist and title and path:
            song_data = {
                "artist": artist,
                "title": title,
                "album": album,
                "genre": genre,
                "picture_path": picture_path, 
                "picture_link": picture_link,
                "youtube_id": youtube_id,
                "path": path.replace("\\", "/")
            }
            self.songs.append(song_data)
            self.add_song_to_table()

    def save_playlist(self):
        playlist_name = self.playlist_name_input.text().strip() or "Untitled Playlist"
        discord_large_image_key = self.discord_large_image_key_input.text().strip()
        songs = self.songs

        if not songs:
            QMessageBox.warning(self, "Error", "Playlist cannot be empty")
            return

        playlist_data = {
            "playlist_name": playlist_name,
            "playlist_large_image_key": discord_large_image_key,
            "song_count": len(songs),
            "songs": songs
        }

        playlist_folder = self.config.get('root_playlist_folder', 'playlists')
        if not os.path.exists(playlist_folder):
            os.makedirs(playlist_folder)

        playlist_path = os.path.join(playlist_folder, f"{playlist_name}.json")
        with open(playlist_path, 'w') as f:
            json.dump(playlist_data, f, indent=4)

        QMessageBox.information(self, "Playlist Saved", f"Playlist '{playlist_name}' has been saved successfully!")
  
    def open_playlist(self):
        """Open a playlist from the available list in the playlists folder."""
        playlists_dir = self.config.get('root_playlist_folder', 'playlists')

        # Get a list of all available playlists
        available_playlists = [f for f in os.listdir(playlists_dir) if f.endswith(".json")]

        if not available_playlists:
            QMessageBox.information(self, "No Playlists", "No playlists found in the directory.")
            return

        # Create a dialog to list the available playlists
        dialog = QDialog(self)
        dialog.setWindowTitle("Select a Playlist")
        dialog.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout(dialog)

        list_widget = QListWidget(dialog)
        list_widget.addItems([os.path.splitext(p)[0] for p in available_playlists])
        layout.addWidget(list_widget)

        button_box = QHBoxLayout()
        layout.addLayout(button_box)

        select_button = QPushButton("Select", dialog)
        cancel_button = QPushButton("Cancel", dialog)
        button_box.addWidget(select_button)
        button_box.addWidget(cancel_button)

        def on_select():
            selected_playlist = list_widget.currentItem().text()
            dialog.accept()  # Close the dialog and proceed
            self.load_playlist(selected_playlist)  # Load the selected playlist

        def on_cancel():
            dialog.reject()  # Just close the dialog

        select_button.clicked.connect(on_select)
        cancel_button.clicked.connect(on_cancel)

        dialog.exec_()
                
    def load_playlist(self, playlist_name):
        """Load a playlist into the UI."""
        playlist_manager = PlaylistManager()
        try:
            playlist_name, songs, playlist_image = playlist_manager.load_playlist(playlist_name)
        except (FileNotFoundError, ValueError, IOError) as e:
            QMessageBox.critical(self, "Error Loading Playlist", str(e))
            return

        self.playlist_name_input.setText(playlist_name)
        self.discord_large_image_key_input.setText(playlist_image if playlist_image else "")

        self.songs = songs
        self.song_table.setRowCount(0)
        self.add_song_to_table()
            
        QMessageBox.information(self, "Playlist Loaded", f"Playlist '{playlist_name}' loaded successfully.")