# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 10:03:45 2020

@author: joedattoli
"""

import tkinter as tk
from time import sleep
import pandas as pd
from PIL import ImageTk,Image
from platform import system
from datetime import datetime





def on_exit():
    vari = tk.messagebox.askyesno('WARNING','Do you want to save all before closing?')
    if (vari  == True):
        submit_to_full()
        tk.messagebox.showinfo('Complete', 'SAVING COMPLETE')
        sleep(2)
        root.destroy()
    else:
        df_backup = pd.read_csv(r'swing_stats_temp.csv')
        df_backup.to_csv(r'swing_stats_backup.csv')        
        root.destroy()
        

def close_all():
    pass
    ## have it submit to a temp file for recovery....
    
def submit_to_full():
   
    df_full = pd.read_csv(r'swing_stats_full.csv')
    df_temp = pd.read_csv(r'swing_stats_temp.csv')
    df_backup = df_temp
    
    df_full = df_full.append(df_temp, ignore_index = True)
    df_full.to_csv(r'swing_stats_full.csv', index = False)
    df_backup.to_csv(r'swing_stats_backup.csv', index = False)
    
def temp_recall():
    df = pd.read_csv(r'swing_stats_temp.csv' )

    row = df.iloc[(len(df.index)-1)]

    df = df.drop(index = [(len(df.index)-1)])

    df.to_csv(r'swing_stats_temp.csv', index = False )
    return row

def temp_writer(info):
    
    app_dict = {'Log_DT': datetime.now(),'Batter': info[0],'Pitcher': info[1], 'Count': info[2],
                'Pitch_Type': info[3],'Result': info[4], 'IO': info[5]}
    app_series = pd.Series(app_dict)
    #print(app_series)
    df = pd.read_csv(r'swing_stats_temp.csv' )
    #print(df)
    df = df.append(app_series, ignore_index = True)
    df.to_csv(r'swing_stats_temp.csv', index = False)
    
class App_Main_Window(tk.Frame):
    def __init__(self,parent):
        super(App_Main_Window,self).__init__(parent)
        

        
        self.Batter_label = tk.Label(self, text = 'Batter last Name')
        self.Pitcher_label = tk.Label(self, text = 'Pitcher last Name')
        self.Count_label = tk.Label(self, text = 'Count')
        self.PMF_label = tk.Label(self, text = 'Result') 
        self.IO_label = tk.Label(self, text = 'In-Zone or Out-Zone')
        self.Pitch_label = tk.Label(self, text = 'Pitch Type')        
        self.empty_label = tk.Label(self,text ='')
        
        

        self.Batter_label.grid(row = 0 , column = 0, sticky = 'nswe')
        self.Pitcher_label.grid(row = 0 , column = 1, sticky = 'nswe')
        self.Count_label.grid(row = 0 , column = 2, sticky = 'nswe')
        self.PMF_label.grid(row = 0 , column = 4, sticky = 'nswe')
        self.IO_label.grid(row = 0 , column = 5, sticky = 'nswe')
        self.Pitch_label.grid(row = 0 , column = 3, sticky = 'nswe')
        self.empty_label.grid(row = 2, sticky = 'nswe')
        
        self.Batter_var = tk.StringVar()
        self.Pitcher_var = tk.StringVar()        
        self.count_var = tk.StringVar()
        self.PMF_var = tk.StringVar()
        self.IO_var = tk.StringVar()
        self.pitch_var = tk.StringVar()
        
        count_choices = ['0-0','0-1','0-2','1-0','1-1','1-2','2-0','2-1','2-2','3-0','3-1','3-2']
        pmf_choices   = ['--------','BIP' ,'Foul', 'Whiff', 'Take' ]
        IO_choices   =  ['--------','In Zone' ,'Out Zone', 'Boarder']
        pitch_choices = ['--------','FB', 'CB' , 'SL', 'CH']
        self.count_var.set('0-0')
        self.PMF_var.set('--------')
        self.IO_var.set('--------')
        self.pitch_var.set('--------')
        
        self.Batter_entry = tk.Entry(self, textvariable = self.Batter_var)
        self.Pitcher_entry = tk.Entry(self, textvariable = self.Pitcher_var)
        self.Count_entry = tk.OptionMenu(self, self.count_var, *count_choices)
        self.PMF_entry = tk.OptionMenu(self, self.PMF_var, *pmf_choices) 
        self.IO_entry = tk.OptionMenu(self, self.IO_var, *IO_choices)
        self.pitch_entry = tk.OptionMenu(self, self.pitch_var, *pitch_choices)

        self.Batter_entry.grid(row = 1 , column = 0 , padx = 10, sticky = 'nswe')
        self.Pitcher_entry.grid(row = 1 , column = 1, padx = 10, sticky = 'nswe')
        self.Count_entry.grid(row = 1 , column = 2, padx = 10, sticky = 'nswe')
        self.PMF_entry.grid(row = 1 , column = 4, padx = 10, sticky = 'nswe')
        self.IO_entry.grid(row = 1 , column = 5, padx = 10, sticky = 'nswe')
        self.pitch_entry.grid(row = 1 , column = 3, padx = 10, sticky = 'nswe')
        
        self.submit_button =tk.Button(self, command = self.submit_choices, text = 'Submit Stats')
        self.submit_button.grid(row=3,column=0, padx = 6)
        
        self.resetAB_button =tk.Button(self, command = self.resetAB, text = 'Reset AB')
        self.resetAB_button.grid(row=3,column=2, padx = 6)
        
        self.recall_button = tk.Button(self,command= self.recall_last_entry, text = 'Recall Last')
        self.recall_button.grid(row=3,column=4, padx = 6)
        
        self.save_button = tk.Button(self,command= self.save_and_close, text = 'Save All and Close')
        self.save_button.grid(row=4,column=2, padx = 6, pady =15)
        
        self.status_label = tk.Label(self,bd =1, relief = tk.SUNKEN, anchor= tk.W, text = 'Awaiting Pitch')
        self.status_label.grid(row=5, columnspan =6, sticky = 'we')

        self.grid_columnconfigure(index = 0, minsize = 110, weight = 1)
        self.grid_columnconfigure(index = 1, minsize = 110, weight = 1)
        self.grid_columnconfigure(index = 2, minsize = 110, weight = 1)
        self.grid_columnconfigure(index = 3, minsize = 110, weight = 1)
        self.grid_columnconfigure(index = 4, minsize = 110, weight = 1)
        self.grid_columnconfigure(index = 5, minsize = 110, weight = 1)

        
    def resetAB(self):

        self.Batter_entry.delete(0 , tk.END)
        self.count_var.set('0-0')
        self.PMF_var.set('--------')
        self.IO_var.set('--------')
        self.pitch_var.set('--------')

    def recall_last_entry(self):
        self.status_label.config(text = "Recalled Last Entry. Edit and Re-submit!")
        self.status_label.update_idletasks()
        recall = temp_recall()
        self.Batter_entry.delete(0 , tk.END)
        self.Pitcher_entry.delete(0 ,tk.END)        
        
        self.Batter_entry.insert(0 , recall[0])
        self.Pitcher_entry.insert(0 , recall[1])
        self.count_var.set(recall[2])
        self.PMF_var.set(recall[3])
        self.IO_var.set(recall[4])
        self.pitch_var.set(recall[5])

    def submit_choices(self):
        self.status_label.config(text = "Saving Pitch")
        self.status_label.update_idletasks()
        sleep(1)
        temp_writer(self.get_all())
        self.status_label.config(text = "Done")
        self.status_label.update_idletasks()
        sleep(1)
        self.status_label.config(text = "Awaiting Pitch")
        self.status_label.update_idletasks()
    def save_and_close(self):
        submit_to_full()
        self.status_label.config(text = "Saving All Pitches From This Log Session")
        self.status_label.update_idletasks()
        sleep(3)
        tk.messagebox.showinfo('Goodbye','All Saved. Goodbye!')
        self.status_label.config(text = "Closing")
        self.status_label.update_idletasks()
        sleep(1)
        
        root.destroy()

    def get_all(self):
        return[self.Batter_var.get(),self.Pitcher_var.get(), self.count_var.get(), self.PMF_var.get(), self.IO_var.get(), self.pitch_var.get()]
if __name__ == "__main__":  
    temp_ = pd.DataFrame(columns = ['Batter','Pitcher', 'Count', 'Pitch_Type','Result', 'IO'])
    temp_.to_csv(r'swing_stats_temp.csv', index = False)
    root = tk.Tk()
    root.title("Offensive Stats Platform  v0.0.1 Pre-Alpha")
    
    
    root.wm_protocol('WM_DELETE_WINDOW', func = on_exit)
    canvas = tk.Canvas(root, width = 150, height = 150)  
    canvas.grid(row =0)
    if (system() == 'Darwin'):
        img = ImageTk.PhotoImage(Image.open(r'/Users/joedattoli/Documents/GitHub/BB_SCOREBOOK_CSVINPUT_HELPER/main_logo.png'))  
    elif(system() == 'Windows'):
        img = ImageTk.PhotoImage(Image.open(r"C:\Users\joedattoli\Documents\GitHub\radialdefensivechart\main_logo.png"))  
    canvas.create_image(75, 75, image=img) 
    app = App_Main_Window(root)
    app.grid(row=1)
    root.columnconfigure(0,weight =1)
    root.columnconfigure(1,weight =1)
    root.rowconfigure(0,weight =1)
    root.rowconfigure(1,weight =1)
  



    root.mainloop()
        