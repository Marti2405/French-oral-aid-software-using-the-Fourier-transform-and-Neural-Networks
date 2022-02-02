import scipy.io.wavfile as wf
import scipy
import scipy.fftpack as fftpk
import numpy as np
from matplotlib import pyplot as plt
import os , sys
import math

# class to remove output text for a command
class suppress_output:
    def __init__(self, suppress_stdout=False, suppress_stderr=False):
        self.suppress_stdout = suppress_stdout
        self.suppress_stderr = suppress_stderr
        self._stdout = None
        self._stderr = None

    def __enter__(self):
        devnull = open(os.devnull, "w")
        if self.suppress_stdout:
            self._stdout = sys.stdout
            sys.stdout = devnull

        if self.suppress_stderr:
            self._stderr = sys.stderr
            sys.stderr = devnull

    def __exit__(self, *args):
        if self.suppress_stdout:
            sys.stdout = self._stdout
        if self.suppress_stderr:
            sys.stderr = self._stderr

# this procedure shows the averaged fft graph of the .wav input file // ->(number_of_files_to_compare , file_1, file_2 ,..., file_n)
def show_averaged_fourier_graph(n,*args):

    # for each .wav file 
    for graph in range(1,n+1):

        #fast fourier transform of input signal

        with suppress_output(suppress_stdout=True, suppress_stderr=True):
            #we don't print the output message of this function
            s_rate , signal = wf.read(args[graph-1])
        
        FFT = np.abs(fftpk.fft(signal))
        freqs = fftpk.fftfreq(len(FFT), (1.0/s_rate))
        
        try :
            FFT = FFT[:,0]
        except :
            pass
        
        
        # doing an average of the values between the frequences n and n+0.5
        a = 0.5
        res = []
        sum = 0
        den = 0
        for i,f in enumerate(freqs[range(len(FFT)//2)]):
            if f <= a:
                sum += FFT[i]
                den+=1
            else:
                if den == 0:
                    res.append(0)
                else:
                    res.append(sum/den)
                
                if f <= a + 0.5 :
                    sum = FFT[i]
                    den = 1
                    a +=0.5
                else :
                    res.append(0)
                    sum = 0
                    den = 0
                    a +=1
        
        # new frequences for res, used to visualise the graph of the output with matplotlib
        freqs = np.arange(0.0,20000,0.5)
        while len(res) < 40000:
            res.append(0)
        
        # plot of the figure n
        plt.subplot(math.ceil(n/math.ceil(n/2)),math.ceil(n/2),graph)
        plt.plot(freqs, res[:40000])
        plt.xlabel("Frequence (Hz)")
        plt.ylabel("Amplitude")
        plt.xlim([0,1500])
        plt.ylim(bottom = 0)
        plt.title(((args[graph-1]).split("\\")[-1]).split(".")[0])
        
    graphs = [((args[i]).split("\\")[-1]).split(".")[0] for i in range(graph)]
    print("Showing graphs of :" , *graphs, sep=' | ')

    #show figure
    plt.show()


# test with some audio samples

def get_loc (nom):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return os.path.join(__location__, f'audio_samples\\{nom}.wav')

# Disponible samples
fichiers = []
for fichier in os.listdir("C:\\Users\\marti\\Desktop\\Dossiers\\Coding\\Projet 2MIC_S2\\audio_samples"):
    fichiers.append(fichier.split(".")[0])

print("Disponible samples :", *fichiers, sep=" | ")

# showing the fft averaged graph
show_averaged_fourier_graph(8,get_loc("v1"),get_loc("f1"),get_loc("vet"),get_loc("fet"),get_loc("v2"),get_loc("f2"),get_loc("v3"),get_loc("f3"))

