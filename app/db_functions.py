import sqlite3
import streamlit as st
import io

from datetime import datetime

import requests
import os
from pathlib import Path
import soundfile as sf
import shutil


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
            area TEXT, 
            language TEXT   
            
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
    wind_kmh, gust_kmh, wind_dir_deg, contact, area, language
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
            wind_kmh, gust_kmh, wind_dir_deg, contact, area, language
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
        """,
        (
            traffic_noise, other_noise, human_noise, natural_sounds,
            pleasant, chaotic, vibrant, uneventful,
            calm, annoying, eventful, monotonus,
            howtheplace, appropriate,
            audiorecording, comments, wereyouwearing, usuallywear,
            str(orario), precip_mm, temp_c, wcode,
            wind_kmh, gust_kmh, wind_dir_deg, contact, area, language
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

def database_backup(): 
    BACKUP_DIR = os.getenv("BACKUP_DIR", "/backup")

    backup_path = os.path.join(BACKUP_DIR, "backup_database_survey.db")
    conn = sqlite3.connect("soundscape_answer.db")
    #position = "/Users/lorenzo/codes/soundscape_data/backup_db"
    backup_conn = sqlite3.connect(backup_path)
    conn.backup(backup_conn)

    backup_conn.close()
    conn.close()
