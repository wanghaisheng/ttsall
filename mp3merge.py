from pydub import AudioSegment
import os

# Directory containing the MP3 files
directory = './results'

# List to store the audio segments
audio_segments = []
files=[]
# Iterate over the files in the directory


# # Concatenate the audio segments
# combined_audio = audio_segments[0]  # Start with the first audio segment
# for segment in audio_segments[1:]:
#     combined_audio += segment

# Export the combined audio as a new MP3 file

index='1-79,80-86,87-114,115-173,174-184,185-193,194-230,231-266,267-274'
startend =index.split(',')
supported_zh=['zh_female_qingxin', 'zh_male_chunhou', 'zh_male_rap', 'zh_female_sichuan', 'zh_female_zhubo', 'zh_male_zhubo', 'tts.other.BV021_streaming', 'tts.other.BV026_streaming', 'tts.other.BV025_streaming', 'zh_male_xiaoming', 'zh_female_story', 'tts.other.BV406_streaming', 'tts.other.BV407_streaming', 'tts.other.BV002_streaming', 'tts.BV701DialogMale.BV701_streaming', 'tts.BV123DialogMale.BV123_streaming', 'tts.BV120DialogMale.BV120_streaming', 'tts.BV119DialogMale.BV119_streaming', 'tts.BV115DialogFemale.BV115_streaming', 'tts.BV107DialogMale.BV107_streaming', 'tts.BV100DialogMale.BV100_streaming', 'tts.BV104DialogFemale.BV104_streaming', 'tts.BV004DialogMale.BV004_streaming', 'tts.BV113DialogFemale.BV113_streaming', 'tts.BV102DialogMale.BV102_streaming', 'tts.other.BV405_streaming', 'tts.other.BV007_streaming', 'tts.other.BV419_streaming', 'tts.other.BV415_streaming', 'tts.other.BV408_streaming', 'tts.other.BV403_streaming', 'tts.other.BV158_streaming', 'tts.other.BR001_streaming', 'tts.other.BV411_streaming', 'tts.other.BV412_streaming', 'tts.other.BV418_streaming', 'tts.BV120DialogMale.BV120_streaming', 'tts.other.BV142_streaming', 'tts.other.BV143_streaming', 'tts.other.BV005_streaming', 'tts.other.BV064_streaming', 'tts.other.BV051_streaming', 'tts.other.BV063_streaming', 'tts.other.BV417_streaming', 'tts.other.BV050_streaming', 'tts.other.BV061_streaming', 'tts.other.BV401_streaming', 'tts.other.BV402_streaming', 'tts.other.BV006_streaming', 'tts.other.BV011_streaming', 'tts.other.BV012_streaming', 'tts.other.BV034_streaming', 'tts.other.BV033_streaming', 'tts.other.BV511_streaming', 'tts.other.BV505_streaming', 'tts.other.BV516_streaming', 'tts.other.BV138_streaming', 'tts.other.BV027_streaming', 'tts.other.BV502_streaming', 'tts.other.BV503_streaming', 'tts.other.BV506_streaming', 'tts.other.BV520_streaming', 'tts.other.BV523_streaming', 'tts.other.BV521_streaming', 'tts.other.BV531_streaming', 'tts.other.BV530_streaming', 'tts.other.BV065_streaming', 'tts.other.BV021_streaming', 'tts.other.BV210_streaming', 'tts.other.BV217_streaming', 'tts.other.BV213_streaming', 'tts.other.BV025_streaming', 'tts.other.BV026_streaming', 'tts.other.BV424_streaming', 'tts.other.BV212_streaming', 'tts.other.BV221_streaming', 'tts.other.BV423_streaming', 'tts.other.BV214_streaming']
for filename in os.listdir(directory):
    if filename.endswith('.mp3'):
        files.append(filename)
print('file count is:',len(files))
print('file count is:',len(supported_zh)*79)

if (len(files)==len(supported_zh)*79):
    print('file number is ok')
for i in startend:
    start =i.split('-')[0]
    end =i.split('-')[-1]
    start_index=int(start)
    end_index=int(end)
    print('processing no:',str(i))
    for speaker in supported_zh:
        print('speaker is :',speaker)
        if not speaker in ['tts.other.BV021_streaming','tts.other.BV026_streaming']:
            if not os.path.exists('./combines/'+speaker+str(i)+'.mp3'):
                audio_segments = []

                for j in range(start_index, end_index + 1):
                    filename=speaker+'-'+str(j)+".mp3"
                    file_path = os.path.join(directory, filename)
                    print('====',speaker+'-'+str(j)+".mp3")

                    # Load the MP3 file as an audio segment
                    audio_segment = AudioSegment.from_mp3(file_path)
                    audio_segments.append(audio_segment)
                combined_audio = audio_segments[0]  # Start with the first audio segment
                print('this series has',len(combined_audio))
                for segment in audio_segments[1:]:
                    combined_audio += audio_segment
                combined_audio.export('./combines/'+speaker+str(i)+'.mp3', format='mp3')
