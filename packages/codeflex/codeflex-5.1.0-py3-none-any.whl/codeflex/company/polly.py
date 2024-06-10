from codeflex.url import connect 

API_URL = "https://go.codeflex.com.co/polly"

HEADERS = { 
    "Content-Type": "application/json"
}
 
def audiodata(inputText, VoiceId,LanguageCode,TokenSub):
    jsonData = {
        "Accion": "CodeflexPolly",
        "Text": inputText,
        "VoiceId": VoiceId,
        "LanguageCode": LanguageCode,
        "TokenSub": TokenSub
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err
     

def download(inputText, VoiceId,LanguageCode,TokenSub):
    jsonData = {
        "Accion": "CodeflexPollyD",
        "Text": inputText,
        "VoiceId": VoiceId,
        "LanguageCode": LanguageCode,
        "TokenSub": TokenSub
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err     
