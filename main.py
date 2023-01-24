# Modulos
import customtkinter
import pypokedex
import urllib3
from io import BytesIO
from tkinter import *
from tkinter import ttk
import PIL.Image, PIL.ImageTk
import pickle
import webbrowser

# Cores
black = "#444466"
white = "#feffff"
blue = "#6f9fbd"
red = "#ef5350"
gray = '#333432'
silver = '#D1D1D1'
value = "#38576b"
letter = "#403d3d"

# Cache das imagens geradas
image_cache = {}

# Status da notificação
status = 'default'

# Criando a janela
window = customtkinter.CTk()
window.geometry('550x510')
window.resizable(width=False, height=False)
window.title('Pokedex')

ttk.Separator(window, orient="horizontal").grid(row=0, columnspan=1, ipadx=274)

# Criando o frame
frame_pokemon = customtkinter.CTkFrame(master=window, width=550, height=230)
frame_pokemon.grid(row=1, column=0)

# Criação do sistema de temas
customtkinter.set_default_color_theme('green')
option_default = customtkinter.StringVar(value='Sistema')

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


theme = customtkinter.CTkOptionMenu(master=window, values=['Sistema', 'Escuro', 'Claro'], command=change_theme, variable=option_default, font=('Fixedsys', 10))
theme.configure(button_color=(white, gray), button_hover_color=(silver, letter), text_color=(gray, white), fg_color=(white, gray))
theme.configure(dropdown_font=('Fixedsys', 5), corner_radius=5)
theme.place(x=10, y=485, anchor=W)

# Local das imagens
pokeball = customtkinter.CTkImage(PIL.Image.open("C:/Users/dimit/Documents/GitHub/Pokedex-Modern/pokeball/Poké_Bal.png"), size=(100, 100))
pokeball_2 = customtkinter.CTkImage(PIL.Image.open("C:/Users/dimit/Documents/GitHub/Pokedex-Modern/pokeball/pokeball.png"), size=(32, 32))
pokeball_place = customtkinter.CTkLabel(master=window, text='', image=pokeball_2)

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

# Salvar o cache
def save_cache():
    with open('image_cache.pickle', 'wb') as handle:
        pickle.dump(image_cache, handle)

# Carregar o cache
def load_cache():
    try:
        with open('image_cache.pickle', 'rb') as handle:
            return pickle.load(handle)
    except:
        return {}


# A Função que vai gerar os pokemons
def load_pokemon(size=(50, 50)):
    if warning_time_update:
        window.after_cancel(warning_time_update)
        pokeball_place.lower()
        warning.configure()

    # Carregando o cache
    global image_cache
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
        print('Imagem recuperada do cache!')

    # Criação do cache das imagens
    else:
        http = urllib3.PoolManager()
        response = http.request('GET', pokemon_url)
        image = PIL.Image.open(BytesIO(response.data))
        image_cache[pokemon_url] = image
        save_cache() # Carregando cache salvo
        print('Imagem criada com sucesso!')


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

# Função da url
def url(event):
    webbrowser.open_new('https://github.com/Dimitri-Matheus')

warning_time_update = None
# A função para ficar mudando a mensagem
def warning_time(label, interval):
    global status, warning_time_update

    if status == 'default':
        label.configure(text="Créditos: Dimitri", text_color=(gray, white))
        pokeball_place.lower()
        label.unbind('<Button-1>')
        print('msg credits')
        status = 'theme' #Mudança da variável status 1

    elif status == 'theme':
        label.configure(text="Altere a aparência da sua pokedex!")
        print('msg theme')
        status = 'github' #Mudança da variável status 2

    elif status == 'github':
        label.configure(text="Se você gostou do meu projeto me siga no github!")
        print('msg github')
        status = 'link' #Mudança da variável status 3

    elif status == 'link':
        label.configure(text='GITHUB', text_color=(blue))
        pokeball_place.configure(bg_color=(white, gray))
        pokeball_place.place(x=220, y=440, anchor=CENTER)
        pokeball_place.lift()
        print('msg link')
        label.bind('<Button-1>', url)
        status = 'default' #Mudança da variável status 1

    warning_time_update = window.after(interval, warning_time, label, interval)


# Configuração do tempo determinado
warning_time(warning, 7000)

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
    warning_time(warning, 7000)
    search.delete(0, 'end')

reset_button = customtkinter.CTkButton(master=window, text='Redefinir', font=('Fixedsys', 10), fg_color=red, hover_color=value, command=reset_values)
reset_button.place(x=275, y=390, anchor=CENTER)

window.mainloop()