from youtube_transcript_api import YouTubeTranscriptApi


def youtube_subtitle(data):
    # Replace 'youtube_video_url' with the URL of the YouTube video you want to extract subtitles from
    # youtube_video_url = input("Input the youtube video link: ")

    video_id = data.split('v=')[-1]
    try:
        subtitle = ""
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        for sub in srt:
            subtitle += sub["text"] + " "
        return subtitle
    except Exception as e:
        return 0
