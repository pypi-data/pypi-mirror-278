import google.generativeai as genai


def summarise(data):
    model = genai.GenerativeModel('gemini-pro')
    genai.configure(api_key="AIzaSyAUbtDaDvQxJnqdvyosOJnh1BoRlJEntSs")
    response = model.generate_content("Summarise the content: "+ data)
    return response.text
