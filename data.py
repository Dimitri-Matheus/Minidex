# Módulos
import customtkinter
from tkinter import *
import PIL.Image, PIL.ImageTk
import pickle
import webbrowser

# Sistema de temas
def change_theme(value):
    if value == 'Escuro':
        # Configuração para o tema escuro
        customtkinter.set_appearance_mode("dark")
    elif value == 'Claro':
        # Configuração para o tema claro
        customtkinter.set_appearance_mode("light")
    else:
        # Configuração para o tema do sistema
        customtkinter.set_appearance_mode("system")


# Sistema de cache das imagens
image_cache = {}

# Salvar o cache
def save_cache():
    with open('image_cache.pickle', 'wb') as handle:
        pickle.dump(image_cache, handle)
        print('Cache salvo com sucesso!')

# Carregar o cache
def load_cache():
    global image_cache

    try:
        with open('image_cache.pickle', 'rb') as handle:
            global image_cache
            image_cache = pickle.load(handle)
            print("Cache carregado com sucesso!")
            return image_cache
    except FileNotFoundError:
        print("Arquivo de cache não encontrado, criando um novo...")
        image_cache = {}
        save_cache()
    except:
        print("Ocorreu um erro ao carregar o cache.")
        return {}

# Sistema do aviso interativo
notification_update = None
status = 'default'

# Abrir o Github
def url(event):
    webbrowser.open_new('https://github.com/Dimitri-Matheus')


# Mudança do status da mensagem
def notification_change(label, status):
    if status == 'default':
        label.configure(text="Créditos: Dimitri")
        label.unbind('<Button-1>')
        print('msg 1')
        status = 'theme' #Mudança da variável status 1

    elif status == 'theme':
        label.configure(text="Altere a aparência da sua pokedex!")
        print('msg 2')
        status = 'github' #Mudança da variável status 2

    elif status == 'github':
        label.configure(text="Se você gostou do meu projeto me siga no github!")
        print('msg 3')
        status = 'link' #Mudança da variável status 3

    elif status == 'link':
        label.configure(text='GITHUB')
        label.bind('<Button-1>', url)
        print('msg 4')
        status = 'default' #Mudança da variável status 1

    return status

