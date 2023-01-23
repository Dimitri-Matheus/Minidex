import pypokedex
import urllib3
import PIL.Image
from io import BytesIO
from main import pokemon_image, pokemon_name, pokemon_id, pokemon_type, search, warning

def get_pokemon_info(sprite):
    try:
        pokemon = pypokedex.get(name=sprite)
    except:
        pokemon = pypokedex.get(id=sprite)
    return pokemon

def download_pokemon_image(pokemon):
    http = urllib3.PoolManager()
    response = http.request('GET', pokemon.sprites.front.get('default'))
    image = PIL.Image.open(BytesIO(response.data))
    return image

def configure_pokemon_data(pokemon, size=(50,50)):
    #Configuração das imagens
    image = image.resize(size, resample=PIL.Image.LANCZOS)
    img = PIL.ImageTk.PhotoImage(image)
    pokemon_image.configure(image=img)
    pokemon_image.image = img

    #Configuração das informações
    pokemon_name.configure(text=f'{pokemon.name}')
    pokemon_type.configure(text=' - '.join([t for t in pokemon.types]))
    pokemon_id.configure(text=f'{pokemon.dex}')

def load_pokemon(size=(50, 50)):
    sprite = search.get()
    pokemon = get_pokemon_info(sprite)
    image = download_pokemon_image(pokemon)
    configure_pokemon_data(pokemon, size)
    warning.configure(text=f'O {pokemon.name} foi encontrado com sucesso na database!'.upper())

