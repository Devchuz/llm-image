import requests

# URL de la solicitud
url = 'https://devchuz-llm-image.hf.space/classify-skin-tone/'

# Archivo de imagen que deseas enviar
image_path = 'test.png'

# Encabezados
headers = {
    'accept': 'application/json'
}

# Abrir el archivo de imagen y hacer la solicitud POST
with open(image_path, 'rb') as image_file:
    # Crear los datos para la solicitud (en este caso, multipart/form-data)
    files = {
        'file': (image_path, image_file, 'image/png')
    }

    # Hacer la solicitud POST
    response = requests.post(url, headers=headers, files=files)

# Imprimir el resultado de la solicitud
print(response.status_code)
print(response.json())
