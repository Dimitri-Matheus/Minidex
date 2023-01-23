# Modulos
import pypokedex
import urllib3
from io import BytesIO
import PIL.Image, PIL.ImageTk
from main import search, warning, pokemon_image, pokemon_id, pokemon_type, pokemon_name


# A Função que vai gerar os pokemons
def load_pokemon(size=(50, 50)):
    try:
        sprite = search.get()
        pokemon = pypokedex.get(name=sprite)
        http = urllib3.PoolManager()
        response = http.request('GET', pokemon.sprites.front.get('default'))
        image = PIL.Image.open(BytesIO(response.data))
        warning.configure(text=f'O {pokemon.name} foi encontrado com sucesso na database!'.upper())

    except:
        sprite = search.get()
        pokemon = pypokedex.get(id=sprite)
        http = urllib3.PoolManager()
        response = http.request('GET', pokemon.sprites.front.get('default'))
        image = PIL.Image.open(BytesIO(response.data))
    #Configuração das imagens
    image = image.resize(size, resample=PIL.Image.LANCZOS)
    img = PIL.ImageTk.PhotoImage(image)
    pokemon_image.configure(image=img)
    pokemon_image.image = img

    #Configuração das informações
    pokemon_name.configure(text=f'{pokemon.name}')
    pokemon_type.configure(text=' - '.join([t for t in pokemon.types]))
    pokemon_id.configure(text=f'{pokemon.dex}')