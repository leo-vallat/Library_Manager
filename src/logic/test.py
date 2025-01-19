from mutagen.id3 import ID3, APIC, error
from mutagen.wave import WAVE

def add_artwork_to_wav(wav_file, image_file):
    try:
        # Load the WAV file with ID3 tagging support
        audio = WAVE(wav_file)

        # If the file doesn't already have ID3 tags, add them
        if audio.tags is None:
            audio.add_tags()

        # Add the image as album art
        with open(image_file, 'rb') as img:
            audio.tags.add(
                APIC(
                    encoding=3,         # 3 is for UTF-8
                    mime='image/jpeg',  # MIME type for jpg images
                    type=3,             # 3 is for album art
                    desc='Cover',
                    data=img.read()     # Image data
                )
            )

        # Save the changes
        audio.save()
        print(f"Artwork added successfully to {wav_file}!")
    except error as e:
        print(f"Error: {e}")
        
# Example usage
wav_path = "/Users/leopold/Library/Mobile Documents/com~apple~CloudDocs/Musique/Transfert Musique/2024 % Run Away (Shutdown Festival 2024 Anthem) % Vertile % Run Away (Shutdown Festival 2024 Anthem).wav"
image_path = "/Users/leopold/Library/Mobile Documents/com~apple~CloudDocs/Projets/Python/Musique/LibraryManager/ressources/artwork/Run Away (Shutdown Festival 2024 Anthem)-Vertile.jpeg"



add_artwork_to_wav(wav_path, image_path)

