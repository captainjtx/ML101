import sys
import os
import requests
import logging

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    logging.info("Downloading "+id + " to "+destination)
    logging.info("Please be patient, it may take a while...")
    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    logging.info("...")
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    
    logging.info("Done with " + id)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == "__main__":
    try:
        gid = sys.argv[1]
        out_fname = sys.argv[2]
        logging.info("Downloading google file id: " + gid)
        logging.info("Saving to: " + out_fname)
    except:
        logging.info("Please specify a google file id and filename to save !")
        
    download_file_from_google_drive(gid, out_fname) 
