# Modulos
import customtkinter
import pypokedex
import urllib3
from io import BytesIO
from tkinter import *
from tkinter import ttk
import PIL.Image, PIL.ImageTk
from fuction import load_pokemon

# Temas
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')
black = "#444466"
white = "#feffff"
blue = "#6f9fbd"
red = "#ef5350"
gray = '#333432'
value = "#38576b"
letter = "#403d3d"

# Criando a janela
window = customtkinter.CTk()
window.geometry('550x510')
window.title('Pokedex')

ttk.Separator(window, orient="horizontal").grid(row=0, columnspan=1, ipadx=274)

# Criando o frame
frame_pokemon = customtkinter.CTkFrame(master=window, width=550, height=230)
frame_pokemon.grid(row=1, column=0)

# Local da imagem
pokeball = customtkinter.CTkImage(PIL.Image.open("C:/Users/dimit/Documents/GitHub/Pokedex-Modern/pokeball/Poké_Bal.png"), size=(100, 100))
pokemon_image = customtkinter.CTkLabel(master=frame_pokemon, text='', image=pokeball)
pokemon_image.place(relx=0.5, rely=0.6, anchor=CENTER)

# Nome
pokemon_name = customtkinter.CTkLabel(master=frame_pokemon, text='Pokedex Modern', font=('Fixedsys', 27), text_color=white)
pokemon_name.place(x=275, y=20, anchor=CENTER)

# Tipo
pokemon_type = customtkinter.CTkLabel(master=frame_pokemon, text='Digite o nome ou id do seu pokemon!', font=('Fixedsys', 21), text_color=white)
pokemon_type.place(x=275, y=45, anchor=CENTER)

# ID
pokemon_id = customtkinter.CTkLabel(master=frame_pokemon, text='', font=('Fixedsys', 21), text_color=white)
pokemon_id.place(x=275, y=65, anchor=CENTER)

# Criando o aviso
warning = customtkinter.CTkLabel(master=window, text='Créditos: Dimitri', font=('Fixedsys', 15), width=170, height=40, corner_radius=5, fg_color=(white, gray))
warning.place(x=275, y=450, anchor=CENTER)

# Criando a pesquisa
search = customtkinter.CTkEntry(master=window, placeholder_text='Nome ou ID', font=('Fixedsys', 10))
search.place(x=275, y=310, anchor=CENTER)

# Criando o botão de procurar pokemons
button_load = customtkinter.CTkButton(master=window, width=120, height=32,text='Carregar Pokemon', font=('Fixedsys', 10), hover_color=value, command=lambda: load_pokemon(size=(150, 150)))
button_load.place(x=275, y=350, anchor=CENTER)

# Criando o reset de valores
def reset_values():
    pokemon_name.configure(text='Pokedex Modern')
    pokemon_type.configure(text='Digite o nome ou id do seu pokemon!')
    pokemon_id.configure(text='')
    pokemon_image.configure(image=pokeball, text='')
    warning.configure(text='Créditos: Dimitri')
    search.delete(0, 'end')

reset_button = customtkinter.CTkButton(master=window, text='Redefinir', font=('Fixedsys', 10), fg_color=red, hover_color=value, command=reset_values)
reset_button.place(x=275, y=390, anchor=CENTER)

window.mainloop()