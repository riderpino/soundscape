import sqlite3
import streamlit as st
import io

from datetime import datetime

import requests
import os
from pathlib import Path
import soundfile as sf
import shutil
import db_functions as mydb
import languages as lg
from zoneinfo import ZoneInfo  



st.session_state.is_submitted = False

def main():

   
    #supported_languages = ["en", "nl", "it"]
    #lang = request.accept_languages.best_match(supported_languages)
    language = st.selectbox("Choose your language:",("English", "Italiano", "Deutsch", "Français"),)
    

    if language == "English": 
        lang = "en"
    elif language == "Italiano": 
        lang = "it"
    elif language == "Deutsch":
        lang = "de"
    elif language ==  "Français": 
        lang = "fr"

    #st.write(lang)
    
    

    
  

    #read the area 
    area = st.query_params.get("area")

    print("url", area)

    #area = st.query_params
    mydb.init_table()

    st.title(lg.languages["text"]["titles"]["app_title"][lang])

    st.write(lg.languages["text"]["descriptions"]["study_description"][lang])

    # Define the options
    noise_levels = lg.languages["text"]["groups_of_scales"]["noise_levels"][lang]

    agree_disagree = lg.languages["text"]["groups_of_scales"]["agree_disagree"][lang]

    good_not_good = lg.languages["text"]["groups_of_scales"]["good_not_good"][lang]

    perfectly = lg.languages["text"]["groups_of_scales"]["appropriateness"][lang]


    
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
        w = mydb.get_weather_vienna()
        desc = CODE_MAP.get(w["wcode"], "N/A")
        
    except Exception as e:
        st.error(f"Weather unavailable: {e}")



    #with st.expander("📝 Noise Perception Questions"):
    with st.form("soundscape_form"):
        

        st.caption(lg.languages["text"]["titles"]["section_hear_types"][lang])
        
        # Question 1: Traffic noise
        traffic_noise = st.radio(
            lg.languages["text"]["question_descriptions"]["q_traffic_noise"][lang],
            noise_levels,
            index= None
        )
        # Question 2: Other noise
        other_noise = st.radio(
            lg.languages["text"]["question_descriptions"]["q_other_noise"][lang],
            noise_levels,
            index= None
        )

        human_noise = st.radio(
            lg.languages["text"]["question_descriptions"]["q_human_noise"][lang],
            noise_levels,
            index= None
        )
        natural_sounds = st.radio(
            lg.languages["text"]["question_descriptions"]["q_natural_sounds"][lang],
            noise_levels,
            index= None
        )
        st.divider()
        st.caption(lg.languages["text"]["titles"]["section_8_scales"][lang])

            # Select sliders: give ONE default value (not the whole list)
        pleasant = st.select_slider(lg.languages["text"]["question_descriptions"]["scale_label_pleasant"][lang], options=agree_disagree, value=agree_disagree[2])
        chaotic = st.select_slider(lg.languages["text"]["question_descriptions"]["scale_label_chaotic"][lang], options=agree_disagree, value=agree_disagree[2])
        vibrant = st.select_slider(lg.languages["text"]["question_descriptions"]["scale_label_vibrant"][lang], options=agree_disagree, value=agree_disagree[2])
        uneventful = st.select_slider(lg.languages["text"]["question_descriptions"]["scale_label_uneventful"][lang], options=agree_disagree, value=agree_disagree[2])
        calm = st.select_slider(lg.languages["text"]["question_descriptions"]["scale_label_calm"][lang], options=agree_disagree, value=agree_disagree[2])
        annoying = st.select_slider(lg.languages["text"]["question_descriptions"]["scale_label_annoying"][lang], options=agree_disagree, value=agree_disagree[2])
        eventful = st.select_slider(lg.languages["text"]["question_descriptions"]["scale_label_eventful"][lang], options=agree_disagree, value=agree_disagree[2])
        monotonus = st.select_slider(lg.languages["text"]["question_descriptions"]["scale_label_monotonus"][lang], options=agree_disagree, value=agree_disagree[2])

        st.divider()
        #st.caption("overall, how would you describe the present enviroment?.")
        howstheplace = st.radio(
            lg.languages["text"]["question_descriptions"]["q_overall_environment"][lang],
            good_not_good,
            index= None
        )


        st.divider()
        appropriate = st.radio(
            lg.languages["text"]["question_descriptions"]["q_appropriate_sound_environment"][lang],
            perfectly,
            index= None
        )

        st.divider()
        #st.caption("overall, how would you describe the present enviroment?.")
        wereyouwearing = st.radio(
            lg.languages["text"]["question_descriptions"]["q_were_you_wearing_headphones"][lang],
            lg.languages["text"]["groups_of_scales"]["yes_no"][lang], index=None
        )
        st.divider()

        #st.caption("overall, how would you describe the present enviroment?.")
        usuallywear = st.radio(
            lg.languages["text"]["question_descriptions"]["q_do_you_usually_wear_noise_cancelling"][lang],
            lg.languages["text"]["groups_of_scales"]["yes_no"][lang], index=None
        )
        st.divider()

        audio_value = st.audio_input(lg.languages["text"]["question_descriptions"]["q_audio_input"][lang], sample_rate=None)

        

        comments = st.text_area(lg.languages["text"]["question_descriptions"]["q_optional_comment"][lang], placeholder=lg.languages["text"]["question_descriptions"]["q_comments_placeholder"][lang])
        contacts = st.text_area(lg.languages["text"]["question_descriptions"]["q_contact_information"][lang], placeholder=lg.languages["text"]["question_descriptions"]["q_contacts_placeholder"][lang])
        
        submitted = st.form_submit_button("Submit") 


    if submitted and not st.session_state.is_submitted: #add the only single submission
        st.session_state.is_submitted = True
        #area = "luca"
        #st.markdown(f"[share]({area})")

        #print("get url", area)
        st.success(lg.languages["text"]["descriptions"]["feedback_thanks"][lang])
        #st.write(f"**Sky:** {desc}")
        #st.json(w)  # simply prints it

        orario = datetime.now()
        #st.write(f"time {orario}")

        


        temp_c = w["temp_c"]
        wcode = w["wcode"]
        precip_mm = w["precip_mm"]
        wind_kmh = w["wind_kmh"]
        gust_kmh = w["gust_kmh"]
        wind_dir_deg = w["wind_dir_deg"]



        
        st.write("### Your Responses:")
        st.write(f"**Traffic noise:** {traffic_noise}")
        st.write(f"**Other noise:** {other_noise}")
        st.write(f"**Sounds from human being:** {human_noise}")
        st.write(f"**Natural sounds:** {natural_sounds}")

        st.write("### Perceptual scales")
        st.write(f"{lg.languages["text"]["question_descriptions"]["scale_label_pleasant"][lang]}: {pleasant}")
        st.write(f"{lg.languages["text"]["question_descriptions"]["scale_label_chaotic"][lang]}: {chaotic}")
        st.write(f"{lg.languages["text"]["question_descriptions"]["scale_label_vibrant"][lang]}: {vibrant}")
        st.write(f"{lg.languages["text"]["question_descriptions"]["scale_label_uneventful"][lang]}: {uneventful}")
        st.write(f"{lg.languages["text"]["question_descriptions"]["scale_label_calm"][lang]}: {calm}")
        st.write(f"{lg.languages["text"]["question_descriptions"]["scale_label_annoying"][lang]}: {annoying}")
        st.write(f"{lg.languages["text"]["question_descriptions"]["scale_label_eventful"][lang]}: {eventful}")
        st.write(f"{lg.languages["text"]["question_descriptions"]["scale_label_monotonus"][lang]}: {monotonus}")

        

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


            tz = ZoneInfo("Europe/Vienna")
            current_datetime = datetime.now(tz).strftime("%d-%m-%Y-%H-%M-%S")
            str_current_datetime = str(current_datetime)

            if area != None: 
                audio_name = area+"-"+str_current_datetime+".wav"
            else:
                audio_name = "noarea-"+str_current_datetime+".wav"

            #audio_path = AUDIO_DIR / audio_name
            #sf.write(audio_name, audiodata, samplerate,format='ogg', subtype='vorbis')
            sf.write(audio_name, audiodata, samplerate,format='wav')
            #backup audio file

            BACKUP_DIR = os.getenv("BACKUP_DIR", "/backup")

            backup_name = os.path.join(BACKUP_DIR, audio_name)
            #backup_name = "/Users/lorenzo/codes/soundscape_data/" + audio_name
            shutil.copy(audio_name, backup_name )
            st.write("Audio recorded and saved successfully! ", audio_name)
            #with open(audio_name, "wb") as f:
                #f.write(audio_value.getbuffer())
                #st.write("Audio recorded and saved successfully! ", audio_name)
                #f.close()




        mydb.write_table(
            traffic_noise, other_noise, human_noise, natural_sounds,
            pleasant, chaotic, vibrant, uneventful,
            calm, annoying, eventful, monotonus,
            howstheplace, appropriate,
            audio_name, comments, wereyouwearing, usuallywear,
            orario,  precip_mm, temp_c, wcode,
            wind_kmh, gust_kmh, wind_dir_deg, contacts, area, lang)
        
        mydb.database_backup()

            
    

if __name__ == "__main__":
    main()
