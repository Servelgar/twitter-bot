
#THIS BOT IS CREATED WITH ANOTHER FILE WITH THE KEYS AND TOKENS FROM THE API TWITTE

import tweepy
import random
import logging
import time
import os, os.path
from PIL import Image
from bd import *



from contra import *
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

try: 
    api.verify_credentials()
except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e


def randomImage(i):
    return random.randint(1,i)

def randomCadena(i):
    return random.randint(1,i)

def checkNumberFile(dir):
    list = os.listdir(dir)
    number_files = len(list)
    return number_files
    

def check_menciones(api, palabras, since_id):
    logger.info("Recolectando menciones")
    new_since_id = since_id
    txt = A_DIR+"\{}.jpg"
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if any(keyword in tweet.text.lower() for keyword in keywords):
            
            logger.info(f"Contestando a {tweet.user.name}")
            
            if not tweet.favorited:
                try:
                    tweet.favorite()
                except Exception as e:
                    logger.error("Error en fav", exc_info=True)
                    raise e               
                for x in range(2):
                    number = randomImage(checkNumberFile(A_DIR))
                    
                api.update_with_media(filename = txt.format(number),
                                      #filename = Image.open(txt.format(number)),
                                      status = "",
                                      in_reply_to_status_id=tweet.id,
                                      auto_populate_reply_metadata=True)
            else:
                logger.info(f"{tweet.user.name} ya ha sido contestado")

    return new_since_id

def tuitearInicioIntermedioFinal(api,inicio,intermedio,final):
    r1 = random.randint(0,len(inicio)-1)
    r2 = random.randint(0,len(intermedio)-1)
    r3 = random.randint(0,len(final)-1)
    
    logger.info(f"Tuiteando inicio-intermedio-final")
    try:
        api.update_status(status=inicio[r1]+intermedio[r2]+final[r3])
    except Exception as e:
        logger.error("Tweet repetido?", exc_info=True)
        raise e


def tuitearInicioFinal(api,inicio,final):
    r1 = random.randint(0,len(inicio)-1)
    r3 = random.randint(0,len(final)-1)
    
    logger.info(f"Tuiteando inicio-final")
    
    try:
        api.update_status(status=inicio[r1]+final[r3])
    except Exception as e:
        logger.error("Tweet repetido?", exc_info=True)
        raise e

def tuitearPregunta(api,inicio,intermedio,final):
    r1 = random.randint(0,len(inicio)-1)
    r2 = random.randint(0,len(intermedio)-1)
    r3 = random.randint(0,len(final)-1)
    
    logger.info(f"Tuiteando pregunta")
    try:
        api.update_status(status=inicio[r1]+intermedio[r2]+final[r3]+"?")
    except Exception as e:
        logger.error("Tweet repetido?", exc_info=True)
        raise e

def main(): 
    since_id = 1
    while True:
        rand = random.randint(1,4)
        if (rand == 1 or rand == 3 or rand == 4):
            since_id = check_menciones(api, ["cuando", "cuantos", "campaña", "cuántos", "Cuantos","para",
                                            "rol","juega","zaakori", "cual", "Cual", "Cuál", 
                                            "cuál", "050", "rodrigo", "abygail", "profeta",
                                            "bestia", "ahogada", "cuándo", "Rol",
                                            "sebastian","brujas","madison","cangrejo"], since_id)
            logger.info("Esperando...")
            time.sleep(30)
        else:
            r = random.randint(1,3)
            if(r == 1):
                tuitearInicioIntermedioFinal(api,INICIO_SUSTANTIVOS, INTERMEDIO_VERBO, FINAL_INTERMEDIO)
            elif(r == 2):
                tuitearInicioFinal(api,INICIO_SUSTANTIVOS,FINAL_VERBO)
            else:
                tuitearPregunta(api,INICIO_PREGUNTA,INTERMEDIO_PREGUNTA,FINAL_INTERMEDIO)
            logger.info("Tuiteado.")
            time.sleep(1000)

        

if __name__ == "__main__":
    main()
