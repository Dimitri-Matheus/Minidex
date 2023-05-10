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
white = '#feffff'
gray = '#333432'
red = '#ef5350'

# A janela
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Personalizando a janela
        #self.configure(fg_color='') mudar a cor do segundo layout
        self.title('Minidex')
        self.geometry('550x510')
        self.resizable(width=False, height=False)
        ttk.Separator(master=self, orient="horizontal").grid(row=0, columnspan=1, ipadx=274)

        # Configuração do tema padrão
        customtkinter.set_default_color_theme('themes/standard.json') # Themes: "standard", "flamingo"
        self.theme_default = customtkinter.StringVar(value='Sistema')

        # Frame do pokemon
        self.frame_pokemon = customtkinter.CTkFrame(master=self, width=550, height=230)
        self.frame_pokemon.grid(row=1, column=0)

        # Local das imagens
        self.pokeball = customtkinter.CTkImage(PIL.Image.open('images/Pokeball.png'), size=(100, 100))
        self.pokemon_image = customtkinter.CTkLabel(master=self.frame_pokemon, text='', image=self.pokeball)
        self.pokemon_image.place(relx=0.5, rely=0.6, anchor=CENTER)

        # Nome
        self.pokemon_name = customtkinter.CTkLabel(master=self.frame_pokemon, text='Minidex', font=('Fixedsys', 27))
        self.pokemon_name.place(relx=0.5, rely=0.1, anchor=CENTER)

        # Tipo
        self.pokemon_type = customtkinter.CTkLabel(master=self.frame_pokemon, text='Digite o nome ou id do seu Pokémon!', font=('Fixedsys', 21))
        self.pokemon_type.place(relx=0.5, rely=0.2, anchor=CENTER)

        # ID
        self.pokemon_id = customtkinter.CTkLabel(master=self.frame_pokemon, text='', font=('Fixedsys', 21))
        self.pokemon_id.place(relx=0.5, rely=0.3, anchor=CENTER)

        # Funcionamento da tecla enter
        def validate_enter(event):
            load_pokemon(size=(150, 150))
        

        # Entrada de pesquisa
        self.search = customtkinter.CTkEntry(master=self, placeholder_text='Nome ou ID', font=('Fixedsys', 10))
        self.search.grid(row=2, column=0, sticky='n', padx=10, pady=15)
        self.search.bind('<Return>', validate_enter)

        # Botão de procurar pokemons
        self.button_load = customtkinter.CTkButton(master=self, width=120, height=32,text='Carregar Pokemon', font=('Fixedsys', 10), command=lambda: load_pokemon(size=(150, 150)))
        self.button_load.grid(row=3, column=0, sticky='s', padx=10, pady=5)

        # Adicionando o reset de valores
        def reset_values():
            self.pokemon_name.configure(text='Minidex')
            self.pokemon_type.configure(text='Digite o nome ou id do seu Pokémon!')
            self.pokemon_id.configure(text='')
            self.pokemon_image.configure(image=self.pokeball, text='')
            notification_set(self.notification, 7000)
            self.search.delete(0, 'end')


        # Botão de redefinir o programa
        self.reset_button = customtkinter.CTkButton(master=self, text='Redefinir', font=('Fixedsys', 10), fg_color=red, command=reset_values)
        self.reset_button.grid(row=4, column=0, sticky='s', padx=10, pady=5)

        # Local da notificação
        self.notification = customtkinter.CTkLabel(master=self, text='', font=('Fixedsys', 15), width=170, height=40, corner_radius=5, fg_color=(white, gray))
        self.notification.grid(row=5, column=0, sticky='s', padx=10, pady=10)

        # Menu de opções dos temas
        self.theme = customtkinter.CTkOptionMenu(master=self, values=['Sistema', 'Escuro', 'Claro'], command=change_theme, variable=self.theme_default, font=('Fixedsys', 10))
        self.theme.configure(dropdown_font=('Fixedsys', 5), corner_radius=5)
        self.theme.grid(row=6, column=0, sticky='sw', padx=10, pady=40)

        # Gerando os pokemons
        def load_pokemon(size=(50, 50)):
                if notification_update:
                    self.after_cancel(notification_update)

                # Carregando o cache
                image_cache = load_cache()

                sprite = self.search.get()
                try:
                    pokemon = pypokedex.get(name=sprite)
                except:
                    pokemon = pypokedex.get(id=sprite)
                self.notification.configure(text=f'O {pokemon.name} foi encontrado com sucesso na database!'.upper())

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
                self.pokemon_image.configure(image=img)
                self.pokemon_image.image = img

                #Configuração das informações
                self.pokemon_name.configure(text=f'{pokemon.name}')
                self.pokemon_type.configure(text=' - '.join([t for t in pokemon.types]))
                self.pokemon_id.configure(text=f'{pokemon.dex}')


        # Configuração do status da mensagem e seu tempo
        def notification_set(label, interval):
            global status, notification_update
            status = notification_change(label, status)
            notification_update = self.after(interval, notification_set, label, interval)
        notification_set(self.notification, 7000)


    # Adicionando o icone
    def iconbitmap(self, bitmap):
        self._iconbitmap_method_called = False
        super().wm_iconbitmap('images/Pokedex.ico')


if __name__ == "__main__":
    app = App()
    app.mainloop()