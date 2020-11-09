# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 11:19:46 2020

@author: joedattoli
"""
import pandas as pd

def main():
    counting_stats = pd.DataFrame(columns = ['Log_DT','Batter','Pitcher', 'Count', 'Pitch_Type', 'Result','IO'])
    try:
        df = pd.read_csv(r'swing_stats_full.csv')
    except:
        pass
    
    counting_stats.to_csv(r'swing_stats_full.csv', index = False)
    counting_stats.to_csv(r'swing_stats_backup.csv', index = False)
    counting_stats.to_csv(r'swing_stats_temp.csv', index = False)
    try:
        df.to_csv(r'full_backup.csv', index = False)
    except NameError:
        pass