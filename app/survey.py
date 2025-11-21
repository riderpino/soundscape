import sqlite3
import streamlit as st
import io

from datetime import datetime

import requests
import os
from pathlib import Path
import soundfile as sf
#from pydub import AudioSegment

#DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
#DATA_DIR.mkdir(parents=True, exist_ok=True)
#DB_PATH = DATA_DIR / "soundscape_answer.db"
#AUDIO_DIR = DATA_DIR / "audio"
#AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def init_table(): 
    conn = sqlite3.connect("soundscape_answer.db")  # Creates a new database file if it doesn’t exist
    cursor = conn.cursor()
    #First_Name CHAR(25) NOT NULL,
    table_creation_query = """
        CREATE TABLE IF NOT EXISTS SURVEY (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            traffic_noise TEXT,
            other_noise TEXT,
            human_noise TEXT, 
            natural_sounds TEXT, 
            pleasant TEXT, 
            chaotic TEXT, 
            vibrant TEXT, 
            uneventful TEXT,
            calm TEXT, 
            annoying TEXT, 
            eventful TEXT, 
            monotonus TEXT, 
            howtheplace TEXT, 
            appropriate TEXT,
            audiorecording CHAR(25), 
            comments CHAR(50),
            wereyouwearing CHAR(25), 
            usuallywear CHAR(25),
            orario TEXT,
            precip_mm REAL,
            temp_c REAL,
            wcode TEXT,
            wind_kmh REAL,
            gust_kmh REAL,
            wind_dir_deg REAL,
            contact TEXT, 
            area TEXT    
            
    );
"""
    cursor.execute(table_creation_query)
    print("Table is Ready")
    conn.close()




def write_table(
    traffic_noise, other_noise, human_noise, natural_sounds,
    pleasant, chaotic, vibrant, uneventful,
    calm, annoying, eventful, monotonus,
    howtheplace, appropriate,
    audiorecording, comments, wereyouwearing, usuallywear,
    orario, precip_mm, temp_c, wcode,
    wind_kmh, gust_kmh, wind_dir_deg, contact, area
): 
    conn = sqlite3.connect("soundscape_answer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO SURVEY (
            traffic_noise, other_noise, human_noise, natural_sounds,
            pleasant, chaotic, vibrant, uneventful,
            calm, annoying, eventful, monotonus,
            howtheplace, appropriate,
            audiorecording, comments, wereyouwearing, usuallywear,
            orario,  precip_mm, temp_c, wcode,
            wind_kmh, gust_kmh, wind_dir_deg, contact, area
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
        """,
        (
            traffic_noise, other_noise, human_noise, natural_sounds,
            pleasant, chaotic, vibrant, uneventful,
            calm, annoying, eventful, monotonus,
            howtheplace, appropriate,
            audiorecording, comments, wereyouwearing, usuallywear,
            str(orario), precip_mm, temp_c, wcode,
            wind_kmh, gust_kmh, wind_dir_deg, contact, area
        )
    )

    print("Data Inserted in the table: ")

    cursor.execute("SELECT * FROM SURVEY")
    for row in cursor.fetchall():
        print(row)

    conn.commit()
    conn.close()


def get_weather_vienna():
    lat, lon = 48.18781661987305,16.36805534362793
    url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,weather_code,precipitation,wind_speed_10m,wind_gusts_10m,wind_direction_10m"
            "&timezone=Europe/Vienna"
        )
    cur = requests.get(url, timeout=10).json()["current"]
    return {
            "temp_c": cur["temperature_2m"],
            "wcode": cur["weather_code"],
            "precip_mm": cur["precipitation"],
            "wind_kmh": cur["wind_speed_10m"],
            "gust_kmh": cur["wind_gusts_10m"],
            "wind_dir_deg": cur["wind_direction_10m"],
        }

  



def main():
    
    #if 'key' not in st.session_state:
     #   st.session_state['key'] = 'value'

    #read the area 
    area = st.query_params.get("area")

    print("url", area)

    #area = st.query_params
    init_table()

    st.title("Noise Perception Questionnaire")

    st.write("This study aims to understand the soundscape around us. I ask you to answer the survey based on your personal perception of the sound around you in this moment")

    # Define the options
    noise_levels = [
        "Not at all",
        "A little",
        "Moderately",
        "A lot",
        "Dominates completely"
    ]

    agree_disagree = [
        "Strongly Agree",
        "Agree",
        "Neither agree, nor disagree",
        "disagree",
        "Strongly disagree"
    ]

    good_not_good = [
        "very good",
        "good",
        "neither good, nor bad",
        "bad",
        "very bad"
    ]

    perfectly = [
        "not at all",
        "slightly",
        "moderately",
        "very", 
        "perfectly"
    ]


    
    CODE_MAP = {
        0:"Clear sky",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",
        45:"Fog",48:"Depositing rime fog",
        51:"Drizzle (light)",53:"Drizzle (moderate)",55:"Drizzle (dense)",
        56:"Freezing drizzle (light)",57:"Freezing drizzle (dense)",
        61:"Rain (slight)",63:"Rain (moderate)",65:"Rain (heavy)",
        66:"Freezing rain (light)",67:"Freezing rain (heavy)",
        71:"Snow (slight)",73:"Snow (moderate)",75:"Snow (heavy)",
        77:"Snow grains",
        80:"Rain showers (slight)",81:"Rain showers (moderate)",82:"Rain showers (violent)",
        85:"Snow showers (slight)",86:"Snow showers (heavy)",
        95:"Thunderstorm",96:"Thunderstorm + hail (slight/mod.)",99:"Thunderstorm + hail (heavy)"
    }

    try:
        w = get_weather_vienna()
        desc = CODE_MAP.get(w["wcode"], "N/A")
        
    except Exception as e:
        st.error(f"Weather unavailable: {e}")



    #with st.expander("📝 Noise Perception Questions"):
    with st.form("soundscape_form"):
        

        st.caption("To what extend do you presently hear the following four types of sounds?")
        
        # Question 1: Traffic noise
        traffic_noise = st.radio(
            "Traffic noise (E.g. cars, buses, trains, air planes)",
            noise_levels,
            index= None
        )

        

        # Question 2: Other noise
        other_noise = st.radio(
            "Other noise (E.g. sirens, construction, industry, loading of goods)?",
            noise_levels,
            index= None
        )

        human_noise = st.radio(
            "Sounds from human beings (e.g., conversation, laughter, children at play, footsteps)",
            noise_levels,
            index= None
        )
        natural_sounds = st.radio(
            "Natural sounds (e.g, singing birds, flowing water, wind in vegetation)",
            noise_levels,
            index= None
        )
        st.divider()
        st.caption("for each of the 8 scales below, to what extend do you agree or disagree that the present surrunding sound enviroment is...")

            # Select sliders: give ONE default value (not the whole list)
        pleasant = st.select_slider("pleasant?", options=agree_disagree, value="Neither agree, nor disagree")
        chaotic = st.select_slider("chaotic?", options=agree_disagree, value="Neither agree, nor disagree")
        vibrant = st.select_slider("vibrant?", options=agree_disagree, value="Neither agree, nor disagree")
        uneventful = st.select_slider("uneventful?", options=agree_disagree, value="Neither agree, nor disagree")
        calm = st.select_slider("calm?", options=agree_disagree, value="Neither agree, nor disagree")
        annoying = st.select_slider("annoying?", options=agree_disagree, value="Neither agree, nor disagree")
        eventful = st.select_slider("eventful?", options=agree_disagree, value="Neither agree, nor disagree")
        monotonus = st.select_slider("monotonus?", options=agree_disagree, value="Neither agree, nor disagree")

        st.divider()
        #st.caption("overall, how would you describe the present enviroment?.")
        howstheplace = st.radio(
            "Overall, how would you describe the present enviroment?",
            good_not_good,
            index= None
        )


        st.divider()
        appropriate = st.radio(
            "Overall, to what extent is the present surrounding sound enviroment appropriate to the present place?",
            perfectly,
            index= None
        )

        st.divider()
        #st.caption("overall, how would you describe the present enviroment?.")
        wereyouwearing = st.radio(
            "Were you wearing heaphones during this survey?",
            ["Yes", "No"], index=None
        )
        st.divider()

        #st.caption("overall, how would you describe the present enviroment?.")
        usuallywear = st.radio(
            "Do you usually wear noise cancelling headphones?",
            ["Yes", "No"], index=None
        )
        st.divider()

        audio_value = st.audio_input("Please record 30 seconds of audio with your device", sample_rate=48000)

        

        comments = st.text_area("Optional comment", placeholder="Can you specify the device that you are using (e.g. brand, model)?")
        contacts = st.text_area("Contact information", placeholder="If you are interested about the future of this project leave us a contact")
        
        submitted = st.form_submit_button("Submit") 


    if submitted: #add the only single submission
        #area = "luca"
        #st.markdown(f"[share]({area})")

        #print("get url", area)

        st.write(f"**Sky:** {desc}")
        st.json(w)  # simply prints it

        orario = datetime.now()
        #st.write(f"time {orario}")

        


        temp_c = w["temp_c"]
        wcode = w["wcode"]
        precip_mm = w["precip_mm"]
        wind_kmh = w["wind_kmh"]
        gust_kmh = w["gust_kmh"]
        wind_dir_deg = w["wind_dir_deg"]



        st.success("Thanks! Your responses have been recorded (not persisted here by default).")
        st.write("### Your Responses:")
        st.write(f"**Traffic noise:** {traffic_noise}")
        st.write(f"**Other noise:** {other_noise}")
        st.write(f"**Sounds from human being:** {human_noise}")
        st.write(f"**Natural sounds:** {natural_sounds}")

        st.write("### Perceptual scales")
        st.write(f"pleasant: {pleasant}")
        st.write(f"chaotic: {chaotic}")
        st.write(f"vibrant: {vibrant}")
        st.write(f"uneventful: {uneventful}")
        st.write(f"calm: {calm}")
        st.write(f"annoying: {annoying}")
        st.write(f"eventful: {eventful}")
        st.write(f"monotonus: {monotonus}")

        

        if comments.strip():
            st.write("### Comments")
            st.write(comments)
        if contacts.strip():
            st.write("### Contact informations")
            st.write(contacts)

        audio_name = "noaudio"
        if audio_value:
            audiodata, samplerate = sf.read(io.BytesIO(audio_value.getbuffer()))
            st.audio(audio_value)
            current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            str_current_datetime = str(current_datetime)
            audio_name = str_current_datetime+".ogg"

            #audio_path = AUDIO_DIR / audio_name
            sf.write(audio_name, audiodata, samplerate,format='ogg', subtype='vorbis')
            
            st.write("Audio recorded and saved successfully! ", audio_name)
            #with open(audio_name, "wb") as f:
                #f.write(audio_value.getbuffer())
                #st.write("Audio recorded and saved successfully! ", audio_name)
                #f.close()

        write_table(
            traffic_noise, other_noise, human_noise, natural_sounds,
            pleasant, chaotic, vibrant, uneventful,
            calm, annoying, eventful, monotonus,
            howstheplace, appropriate,
            audio_name, comments, wereyouwearing, usuallywear,
            orario,  precip_mm, temp_c, wcode,
            wind_kmh, gust_kmh, wind_dir_deg, contacts, area)

            
    

if __name__ == "__main__":
    main()
