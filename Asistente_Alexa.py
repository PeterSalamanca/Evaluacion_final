import speech_recognition as sr
import pyttsx3, pywhatkit, wikipedia, datetime
import subprocess as sp
import cv2


from datetime import date, time, datetime
from random import choice
from metodo_correo import send_email


name = "alexa"


engine = pyttsx3.init()

# Configurar velocidad
engine.setProperty('rate', 130)

# Configurar Volumen
engine.setProperty('volume', 2.0)


voices = engine.getProperty("voices")
engine.setProperty("voices", voices[0].id)

sites = {
    "navegador":"google.com",
}

opening_text = [
    "Genial, estoy en ello.",
    "Entendido, trabajaré en ello.",
    "Deme un segundo apreciado usuario.",
    "Permitame un momento, estoy en ello",
]

def talk(text):
    engine.say(text)
    engine.runAndWait()
 
def listen():
    listener = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            talk("Escuchando ....")
            
            listener.pause_threshold = 1
            print("Escuchando ....")
            listener.adjust_for_ambient_noise(source)
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()    
            if name in rec:
                rec = rec.replace(name, "") 


    except sr.UnknownValueError:
        print("No te entendí, intenta de nuevo ")
        pass
    return rec

def saludo():
    # Saluda al usuario de acuerdo a la hora actual
    
    hour = datetime.now().hour
    if (hour >= 1) and (hour < 12):
        print(f"Buenos días apreciado usuario")
        talk(f"Buenos días apreciado usuario")

    elif (hour >= 12) and (hour < 18):
        print(f"Buenas tardes apreciado usuario")
        talk(f"Buenas tardes apreciado usuario")
    elif (hour >= 18) and (hour < 24):
        print(f"Buenas noches apreciado usuario")
        talk(f"Buenas noches apreciado usuario")

    print(f"Mi nombre es {name}., como puedo ayudarte?")
    talk(f"Mi nombre es {name}., como puedo ayudarte?")
    


def run_alexa():
    while True:
        try:
            rec = listen()
            print(rec)

        except UnboundLocalError:
            talk("No te entendí, intenta de nuevo ")

        
        if "reproduce" in rec:
            talk(choice(opening_text))
            music = rec.replace("reproduce", "").strip()
            pywhatkit.playonyt(music)
            talk(f"Reproduciendo {music}.")

        elif "tómame una foto" in rec:
            talk(choice(opening_text))
            talk("Abriendo Cámara")
            cam = cv2.VideoCapture(0)
            img_counter = 0

            while True:
                ret,frame = cam.read() 
                cv2.imshow("video", frame)
                if not ret:
                    break 
                if cv2.waitKey(1) & 0xFF == ord('a'):
                    img_name = "imagen_{}.png".format(img_counter) 
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name)) 
                    img_counter += 1
                if cv2.waitKey(2) & 0xFF == ord('q'):
                    break

            cam.release() 
            cv2.destroyAllWindows()           

        elif "busca" in rec:
            buscar = rec.replace("busca", "")
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(buscar, 1)
            print(buscar + ": "+ wiki)
            talk(wiki)
            

        elif "abre" in rec:
            talk(choice(opening_text))
            for site in sites:
                if site in rec:
                    sp.call(f"start chrome.exe {sites[site]}", shell=True)
                    talk(f"Abriendo {site}")   

        elif "fecha actual" in rec:
            talk(choice(opening_text))
            tiempo = datetime.now()
            
            print("La fecha actual es: "+ tiempo.strftime("%d/%m/%Y %H:%M:%S"))
            talk("La fecha actual es: "+ tiempo.strftime("%d/%m/%Y %H:%M:%S"))

         elif "enviar un correo" in rec:
            talk("A que correo desea enviar el mensaje? Por favor ingreselo en la consola: ")
            email_receiver = input("Dirección de correo destino: ")
            talk("Por favor indique el asunto ")
            subject = listen().lower()
            print(subject)
            talk("Por favor indique el mensaje a enviar: ")
            body = listen().lower()
            print(body)
            send_email(email_receiver, subject, body)
            talk("He enviado el correo, apreciado usuario.")
            


        elif "salir" or "detener" in rec:
            hora = hora = datetime.now().hour
            if hora >= 18 and hora < 24:
                talk("Que tenga una buena noche, cuidese!")
            else:
                talk('Que tenga un buen día, vuelva pronto')
        exit() 


            


if __name__ == "__main__":
    saludo()
    while True:
        run_alexa()
