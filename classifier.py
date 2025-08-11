# Mostly and export from Google Cloud Vertex AI Studio circa May 2024

import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models

def classify_torrent(filename, hint=""):
  vertexai.init(project="light-tribute-424623-e0", location="us-west1")
  model = GenerativeModel(
#    "gemini-1.5-flash-001", # JRW Mar 18, 2025 - Discontinued in favor of gemini-2.0-flash-lite as per google email
     "gemini-2.0-flash-lite",
  )

  hint_text = f"\nHint: {hint}" if hint is not None else ""

  responses = model.generate_content(
      [f"""You are a name classifier. You take as input the raw name of a media file and you output a path where the media should be stored. 

Movies should be in the \"Movies\" parent folder with the filename being the name of the movie in Title Case, followed by the year in parenthesis, then the file extension to match the input. 

TV Shows should be stored in the \"TV Shows\" parent folder, with a subfolder for the name of the TV show, a subfolder for the season, and a filename with the name of the TV Show in Title Case followed by the season and episode number and finally with the same extension as the input. The name of the episode should not be included. 

TV Show specials should be placed in a \"Specials\" subfolder under the name of the TV show subfolder with the filename being the name of the TV show followed by the name of the special, then the same extension as the input.

Take into account any hints if they are provieded.

You only output the path of the new location and nothing else. You do not output code.

Raw filename: The.Princess.Bride.1987.720p.BluRay.x264-FOON.mkv
Correct path: Movies/The Princess Bride (1987).mkv

Raw filename: whose line is it anyway (s07e17) (e7017) - loki.avi
Correct path: TV Shows/Whose Line Is It Anyway/Season 07/Whose Line Is It Anyway - s07e17.avi

Raw filename: Seinfeld.S06E05.The.Couch.720p.HULU.WEBRip.AAC2.0.H.264-NTb.mkv
Correct path: TV Shows/Seinfeld/Season 06/Seinfeld - s06e05.mkv

Raw filename: Human Giant - Stand Up - Aziz Ansari, Bootleg of Redlight Room, 1 of 4 (Shitlist.com).avi
Correct path: TV Shows/Human Giant/Specials/Extras/Human Giant - Stand Up Aziz Ansari Bootleg Of Redlight Room 1 Of 4 Shitlist Com.avi

Hint: This filename is wong, consider this to be the Matrix (1999) movie
Raw filename: tmnt.mkv
Correct path: Movies/The Matrix (1999).mkv

Raw filename: Fight.Club.1999.720p.BluRay.DTS-ES.x264-DON.mkv
Correct path: Movies/Fight Club (1999).mkv
{hint_text}
Raw filename: {filename}
Correct path:
"""],
      generation_config=generation_config,
      safety_settings=safety_settings,
  )

  return responses.candidates[0].text.strip()


generation_config = {
    "max_output_tokens": 438,
    "temperature": 0.3,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

