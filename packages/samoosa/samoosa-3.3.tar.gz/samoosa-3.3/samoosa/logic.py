from samoosa.youtube_subtitle import youtube_subtitle
from samoosa.summary_ai import summarise


# the main function, which manages the whole program.
def logic_samoosa(data):
    # using the code written in the youtube_subtitle function to extract the subtitle from the yt video.
    content = youtube_subtitle(data)
    # if there is any content returned, the execute the if statement.
    if content:
        # using the gemini ai to summarise the content.
        try:
            response = summarise(content)
        except Exception as e:
           return "There is some error."
        else:
            # outputting the response.
            return response

    else:
        # if there is no subtitle get returned then, output error.
        return "Sorry summarisation of this video is not possible."

