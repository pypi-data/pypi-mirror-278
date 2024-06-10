from codeflex.url import connect 

API_URL = "https://api.codeflex.com.co/correo"

HEADERS = { 
    "Content-Type": "application/json"
}
 
def ses(Subject, Sender, From, Html, To, TokenSub):
    jsonData = {
        "Subject": Subject,
        "Remitente": Sender,  
        "From": From,
        "Html": Html,
        "To": To,
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