from pydub import AudioSegment
import os

# Directory containing the MP3 files
directory = '/path/to/mp3/files/'

# List to store the audio segments
audio_segments = []

# Iterate over the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.mp3'):
        file_path = os.path.join(directory, filename)
        # Load the MP3 file as an audio segment
        audio_segment = AudioSegment.from_mp3(file_path)
        audio_segments.append(audio_segment)

# Concatenate the audio segments
combined_audio = audio_segments[0]  # Start with the first audio segment
for segment in audio_segments[1:]:
    combined_audio += segment

# Export the combined audio as a new MP3 file
combined_audio.export('/path/to/output.mp3', format='mp3')