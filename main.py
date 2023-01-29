# Modulos
import customtkinter
import pypokedex
import urllib3
from io import BytesIO
from tkinter import *
from tkinter import ttk
import PIL.Image, PIL.ImageTk
from data import change_theme, save_cache, load_cache, notification_change, notification_update, status

# Cores
black = '#444466'
white = '#feffff'
blue = '#6f9fbd'
red = '#ef5350'
gray = '#333432'
silver = '#D1D1D1'
value = '#38576b'
letter = '#403d3d'

# Criando a janela
window = customtkinter.CTk()
window.geometry('550x510')
window.resizable(width=False, height=False)
window.title('Pokedex')

ttk.Separator(window, orient="horizontal").grid(row=0, columnspan=1, ipadx=274)

# Criando o frame
frame_pokemon = customtkinter.CTkFrame(master=window, width=550, height=230)
frame_pokemon.grid(row=1, column=0)

# Configuração do tema padrão
customtkinter.set_default_color_theme('green')
theme_default = customtkinter.StringVar(value='Sistema')

# Criando do menu de opções
theme = customtkinter.CTkOptionMenu(master=window, values=['Sistema', 'Escuro', 'Claro'], command=change_theme, variable=theme_default, font=('Fixedsys', 10))
theme.configure(button_color=(white, gray), button_hover_color=(silver, letter), text_color=(gray, white), fg_color=(white, gray))
theme.configure(dropdown_font=('Fixedsys', 5), corner_radius=5)
theme.place(x=10, y=485, anchor=W)

# Local das imagens
pokeball = customtkinter.CTkImage(PIL.Image.open("C:/Users/dimit/Documents/GitHub/Pokedex-Modern/images/Pokeball.png"), size=(100, 100))
pokemon_image = customtkinter.CTkLabel(master=frame_pokemon, text='', image=pokeball)
pokemon_image.place(relx=0.5, rely=0.6, anchor=CENTER)

# Nome
pokemon_name = customtkinter.CTkLabel(master=frame_pokemon, text='Pokedex Modern', font=('Fixedsys', 27), text_color=(gray, white))
pokemon_name.place(x=275, y=20, anchor=CENTER)

# Tipo
pokemon_type = customtkinter.CTkLabel(master=frame_pokemon, text='Digite o nome ou id do seu pokemon!', font=('Fixedsys', 21), text_color=(gray, white))
pokemon_type.place(x=275, y=45, anchor=CENTER)

# ID
pokemon_id = customtkinter.CTkLabel(master=frame_pokemon, text='', font=('Fixedsys', 21), text_color=(gray, white))
pokemon_id.place(x=275, y=65, anchor=CENTER)

# A Função que vai gerar os pokemons
def load_pokemon(size=(50, 50)):
    if notification_update:
        window.after_cancel(notification_update)

    # Carregando o cache
    image_cache = load_cache()

    sprite = search.get()
    try:
        pokemon = pypokedex.get(name=sprite)
    except:
        pokemon = pypokedex.get(id=sprite)
    warning.configure(text=f'O {pokemon.name} foi encontrado com sucesso na database!'.upper())

    pokemon_url = pokemon.sprites.front.get('default')

    # Recuperação do cache das imagens
    if pokemon_url in image_cache:
        image = image_cache[pokemon_url]

    # Criação do cache das imagens
    else:
        http = urllib3.PoolManager()
        response = http.request('GET', pokemon_url)
        image = PIL.Image.open(BytesIO(response.data))
        image_cache[pokemon_url] = image
        save_cache() # Carregando cache salvo


    #Configuração das imagens
    image = image.resize(size, resample=PIL.Image.LANCZOS)
    img = PIL.ImageTk.PhotoImage(image)
    pokemon_image.configure(image=img)
    pokemon_image.image = img

    #Configuração das informações
    pokemon_name.configure(text=f'{pokemon.name}')
    pokemon_type.configure(text=' - '.join([t for t in pokemon.types]))
    pokemon_id.configure(text=f'{pokemon.dex}')


# Criando o aviso
warning = customtkinter.CTkLabel(master=window, text='', font=('Fixedsys', 15), width=170, height=40, corner_radius=5, fg_color=(white, gray))
warning.place(x=275, y=440, anchor=CENTER)

# Configuração do status da mensagem e seu tempo
def notification_set(label, interval):
    global status, notification_update
    status = notification_change(label, status)
    notification_update = window.after(interval, notification_set, label, interval)
notification_set(warning, 7000)

# A validação do enter
def validate_enter(event):
    load_pokemon(size=(150, 150))

# Criando a pesquisa
search = customtkinter.CTkEntry(master=window, placeholder_text='Nome ou ID', font=('Fixedsys', 10))
search.place(x=275, y=310, anchor=CENTER)
search.bind('<Return>', validate_enter)

# Criando o botão de procurar pokemons
button_load = customtkinter.CTkButton(master=window, width=120, height=32,text='Carregar Pokemon', font=('Fixedsys', 10), hover_color=value, command=lambda: load_pokemon(size=(150, 150)))
button_load.place(x=275, y=350, anchor=CENTER)

# Criando o reset de valores
def reset_values():
    pokemon_name.configure(text='Pokedex Modern')
    pokemon_type.configure(text='Digite o nome ou id do seu pokemon!')
    pokemon_id.configure(text='')
    pokemon_image.configure(image=pokeball, text='')
    notification_set(warning, 7000)
    search.delete(0, 'end')

reset_button = customtkinter.CTkButton(master=window, text='Redefinir', font=('Fixedsys', 10), fg_color=red, hover_color=value, command=reset_values)
reset_button.place(x=275, y=390, anchor=CENTER)


window.mainloop()