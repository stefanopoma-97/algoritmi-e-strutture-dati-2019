
import pickle
from Classi.Automa.automa import *
from Classi.Automa.rete import *



def salva_automa_su_file(automa, cartella, filename):
    '''Salva l'automa su un file. Utilizzabile poi per importare nel programma l'automa stesso'''
    with open('Output/'+cartella+'/'+filename, 'wb') as config_dictionary_file:
        # Step 3
        pickle.dump(automa, config_dictionary_file)

def salva_automa_su_file_txt(automa, cartella, filename):
    '''Salva l'automa in un file txt, rispettando il formato corretto
    è quindi possibile utilizzare il file generato per importare l'automa durante una nuova esecuzione del programma'''
    file_txt = open('Output/'+cartella+'/'+filename+".txt", "w")
    file_txt.write(automa.to_string_txt())
    file_txt.close()

def carica_automa_da_file(cartella, filename):
    '''Carica un automa da un file generato in precedenza'''
    with open('Output/'+cartella+'/'+filename, 'rb') as config_dictionary_file:
        automa_load = pickle.load(config_dictionary_file)
        return automa_load


def salva_rete_su_file(rete, cartella, filename):
    '''Salva la rete su un file. Utilizzabile poi per importare nel programma la rete stessa'''
    with open('Output/'+cartella+'/'+filename, 'wb') as config_dictionary_file:
        pickle.dump(rete, config_dictionary_file)

def salva_rete_su_file_txt(rete, cartella, filename):
    '''Salva la rete in un file txt, rispettando il formato corretto
    è quindi possibile utilizzare il file generato per importare la rete durante una nuova esecuzione del programma'''
    file_txt = open('Output/'+cartella+'/'+filename+".txt", "w")
    file_txt.write(rete.to_string_txt())
    file_txt.close()

def salva_links_su_file_txt(rete, cartella, filename):
    '''Salva i links in un file txt, rispettando il formato corretto
    è quindi possibile utilizzare il file generato per importare i link durante una nuova esecuzione del programma'''
    file_txt = open('Output/'+cartella+'/'+filename+".txt", "w")
    file_txt.write(rete.to_string_link_txt())
    file_txt.close()

def carica_rete_da_file(cartella, filename):
    '''Carica la rete da un file generato in precedenza'''
    with open('Output/'+cartella+'/'+filename, 'rb') as config_dictionary_file:
        rete_load = pickle.load(config_dictionary_file)
        return rete_load