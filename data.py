# Módulos
import customtkinter
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
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
        open_error_window('Arquivo de cache não encontrado, reinicie o programa!')
        image_cache = {}
        save_cache()
    except:
        open_error_window('ERRO AO CARREGAR O CACHE!')
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
        status = 'theme' #Mudança da variável status 1

    elif status == 'theme':
        label.configure(text="Altere a aparência da sua pokedex!")
        status = 'github' #Mudança da variável status 2

    elif status == 'github':
        label.configure(text="Se você gostou do meu projeto me siga no github!")
        status = 'link' #Mudança da variável status 3

    elif status == 'link':
        label.configure(text='GITHUB')
        label.bind('<Button-1>', url)
        status = 'default' #Mudança da variável status 1

    return status


# Sistema de erro
def open_error_window(message):

    # Janela de erro
    window_2 = customtkinter.CTkToplevel()
    window_2.title('Atenção')
    window_2.resizable(width=False, height=False)
    window_2.geometry("450x180")

    # Carregando a imagem
    pikachu_image = customtkinter.CTkImage(Image.open('C:/Users/dimit/Documents/GitHub/Pokedex-Modern/images/pikachu_attention.png'), size=(100, 100))

    # Adicionando a imagem ao programa
    pikachu_place = customtkinter.CTkLabel(master=window_2, image=pikachu_image, text='')
    pikachu_place.pack(padx=10, pady=0.1)

    # A mensagem do erro
    msg_erro = customtkinter.CTkLabel(master=window_2, text=message, font=('Fixedsys', 10), text_color=('#ef5350'))
    msg_erro.pack(padx=10, pady=0.3)

    # O botão para sair
    exit = customtkinter.CTkButton(master=window_2, text='Sair', font=('Fixedsys', 10), fg_color='#ef5350', hover_color='#38576b', command=window_2.destroy)
    exit.pack(padx=10, pady=10)


    window_2.mainloop()

