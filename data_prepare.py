import wfdb 
import pandas as pd
import requests
import plotly.express as px
import plotly.io as pio
from tqdm import tqdm
pio.renderers.default = "browser"

class DataPreprocess:
    
    def __init__(self):
        self.df = pd.DataFrame()
        self.df_ruido = pd.DataFrame()
        
    
    def read_and_prepare(self, chanels, subject):
        '''Função para obter os dados e realizar a anotação das colunas'''
        if subject < 10:
            subject = '0' + str(subject)
        for session in [1,2]:  
            self.df_2 = pd.DataFrame()
            self.df_2_ruido = pd.DataFrame()
            target_url = 'https://physionet.org/files/hd-semg/1.0.0/pr_dataset/subject{0}_session{1}/label_dynamic.txt?download'.format(subject,session)
            labels = requests.get(target_url).text.split(',')
            for i in range(0,len(labels)):
                self.ch = []
                if (labels[i] == '12') or (labels[i] == '28') or (labels[i] == '30') or (labels[i] == '31'):
                    self.df_aux = pd.DataFrame()
                    self.df_aux_ruido = pd.DataFrame()
                    self.data = wfdb.rdrecord('dynamic_raw_sample{0}'.format(i+1), channels=chanels, pn_dir='hd-semg/pr_dataset/subject{1}_session{0}/'.format(session,subject))
                    self.signals, self.fields = wfdb.rdsamp('dynamic_raw_sample{0}'.format(i+1), channels=chanels, pn_dir='hd-semg/pr_dataset/subject{1}_session{0}/'.format(session,subject))
                    index = int(self.fields['fs']*0.25)
                    for j in range(0,len(self.signals[0])):
                        self.ch.append(list([row [j] for row in self.signals]))
                        self.df_aux['s{0}_ch{1}'.format(session,j+1)] = self.ch[j][index:]
                        self.df_aux['movement'] = labels[i]
                        self.df_aux_ruido['s{0}_ch{1}'.format(session,j+1)] = self.ch[j][:index]
                        self.df_aux_ruido['movement'] = labels[i]
                    self.df_2 = pd.concat([self.df_2, self.df_aux], ignore_index=True)
                    self.df_2_ruido = pd.concat([self.df_2_ruido, self.df_aux_ruido], ignore_index=True)
            for j in range(0,len(chanels)):
                self.df['s{0}_ch{1}'.format(session,j+1)] = self.df_2['s{0}_ch{1}'.format(session,j+1)]
                self.df_ruido['s{0}_ch{1}'.format(session,j+1)] = self.df_2_ruido['s{0}_ch{1}'.format(session,j+1)]
            self.df['movement'] = self.df_2['movement']
            self.df_ruido['movement'] = self.df_2_ruido['movement']
            
    def save_csv(self, data, name, _type = 'data'):
        '''Função para salvar os dados em csv'''
        data.to_csv(name, sep=';', index = False)
    
    
    def line_plot(self, df, x, y, title):
        '''Função para plotar os sinais'''
        fig = px.line(df, y = [y], title = title)
        fig.show()
        
chanels16 = [113,114,115,116,117,118,119,120,241,242,243,244,245,246,247,248]
dp = DataPreprocess()
for i in tqdm(range(1,21)):
    dp.read_and_prepare(chanels=chanels16, subject=i)
    dp.save_csv(dp.df,"dados/sinais_subject{0}.csv".format(i))
    #dp.save_csv(dp.df_ruido,"dados/ruido_subject{0}.csv".format(i))




