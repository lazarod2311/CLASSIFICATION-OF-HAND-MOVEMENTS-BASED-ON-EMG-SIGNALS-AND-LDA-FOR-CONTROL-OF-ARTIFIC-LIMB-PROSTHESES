import pandas as pd
import numpy as np
from scipy import signal as sg


class DataCaracteristics:
    def __init__(self, path):
        self.data = pd.read_csv(path,sep=';')
        self.data_carac = pd.DataFrame()
    
    def bandpass(self, fs, finf, fsup, dados, ordem):
        '''Função para filtragem da banda de passagem'''
        nyquist = 0.5*fs
        low = finf/nyquist
        high = fsup/nyquist
        b, a = sg.butter(ordem,[low,high], btype='band')
        y = sg.lfilter(b,a,dados)
        return y

    def bandstop(self, fs, fc, dados, Q):
        '''Função para filtragem notch'''
        b, a = sg.iirnotch(fc, Q, fs)
        y = sg.lfilter(b,a,dados)
        return y

    def rms(self, sig, w, fs, overlap=0):
        '''Função para calcular o RMS com janelas móveis'''
        n = int(fs*w)
        n_olap =  int(fs*overlap)
        rms = []
        i = sig.index.min()
        j = sig.index.min()
        ms = 0
        while (j <= sig.index.max()):
            ms = ms + sig[j]**2
            j += 1
            if j == (i+n):
                rms.append(np.sqrt(ms/n))
                ms = 0
                i += (n-n_olap)
                j -= n_olap
        return rms
    
    def var(self, sig, w, fs, overlap=0):
        '''Função para calcular a variância com janelas móveis sem sobreposição'''
        n = int(fs*w)
        n_olap =  int(fs*overlap)
        var = []
        i = sig.index.min()
        j = sig.index.min()
        ms = 0
        sig_mean = 0
        for k in range(j,j+n+1):
            sig_mean += sig[k]
        sig_mean = sig_mean/n
        while (j <= sig.index.max()):
            ms = ms + (sig[j]-sig_mean)**2
            j += 1
            if j == (i+n):
                var.append(ms/(n-1))
                ms = 0
                i += (n-n_olap)
                j -= n_olap
                if (j+n) <= sig.index.max():
                    sig_mean = 0
                    for k in range(j,j+n+1):
                        sig_mean += sig[k]
                    sig_mean = sig_mean/n
        return var
    
    def wl(self, sig, w, fs, overlap = 0):
        '''Função para calcular o comprimento de onda com janelas móveis sem sobreposição'''
        n = int(fs*w)
        n_olap =  int(fs*overlap)
        wl = []
        i = sig.index.min()
        j = sig.index.min()
        ms = 0
        while (j < sig.index.max()):
            ms = ms + np.abs(sig[j+1]-sig[j])
            j += 1
            if j == (i+n):
                wl.append(np.sqrt(ms/n))
                ms = 0
                i += (n-n_olap)
                j -= n_olap
        return wl
    
    def zcr(self, sig, w, fs, overlap=0):
        '''Função para calcular a taxa de cruzamentos por zero com janelas móveis'''
        n = int(fs*w)
        zcr = []
        j = sig.index.min()
        n_olap =  int(fs*overlap)
        while (j <= sig.index.max()):
            if j <= (sig.index.max() - n):
                zc = len(np.nonzero(np.diff(sig.iloc[j:j+n] > 0))[0])
                zcr.append(zc)
                j += (n-n_olap)
            else:
                j = sig.index.max()+1
        return zcr


