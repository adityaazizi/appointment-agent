import pandas as pd
from pydantic import BaseModel
from fastapi import HTTPException
import os

CSV_FILE = 'appointments.csv'

# Ensure the CSV file exists
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Name", "Date", "Start", "End"])
    df.to_csv(CSV_FILE, index=False)


class CRUD:
    @staticmethod
    def read_csv():
        return pd.read_csv(CSV_FILE)

    @staticmethod
    def write_csv(df):
        df.to_csv(CSV_FILE, index=False)

    @staticmethod
    def create_appointment(Name, Date, Start, End):
        df = CRUD.read_csv()

        # Convert times to datetime objects for comparison
        new_start = pd.to_datetime(f"{Date} {Start}")
        new_end = pd.to_datetime(f"{Date} {End}")

        # Check for overlapping appointments
        for index, row in df.iterrows():
            existing_start = pd.to_datetime(f"{row['Date']} {row['Start']}")
            existing_end = pd.to_datetime(f"{row['Date']} {row['End']}")
            if new_start < existing_end and new_end > existing_start:
                return "Appointment time overlaps with an existing appointment."
            
                
        new_data = {
            "Name": Name,
            "Date": Date,
            "Start": Start,
            "End": End
        }
        df = df._append(new_data, ignore_index=True)
        CRUD.write_csv(df)
        
        return "Appointment was Added"
