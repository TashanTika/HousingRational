# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 17:15:03 2020
@author: Tashan Tika
"""
from pathlib import Path
import os

root_dir = Path(__file__).resolve().parent #root directory

inp_url = "https://www.property24.com/for-sale/durban/kwazulu-natal/169"
chrome_path = os.path.join(root_dir, 'driver/chromedriver.exe')
all_records_export_path = os.path.join(root_dir, "p24_records/All Records.xlsx")
raw_file = os.path.join(root_dir, "p24_records/Address.csv")
coordinates = os.path.join(root_dir, "p24_records/coordinates.xlsx")
mapbox_token = os.path.join("pk.eyJ1IjoibmcxOTg0IiwiYSI6ImNraDlqMHgxZTByY3Ayd256bzlvcXp3OHAifQ.o2MXE6NacffhElGwSRjQIA")


