import argparse
from jrnl2tumblr.importer import read_jrnl_file
from jrnl2tumblr.tumblr import create_tumblr_client, post_entries_to_tumblr

def obtain_oauth_credentials():
    print("Por favor, ingresa tus credenciales de OAuth proporcionadas por Tumblr:")
    consumer_key = input("Consumer key: ")
    consumer_secret = input("Consumer secret: ")
    oauth_token = input("OAuth token: ")
    oauth_secret = input("OAuth secret: ")
    return consumer_key, consumer_secret, oauth_token, oauth_secret

def main():
    # Configuración del parser de argumentos
    parser = argparse.ArgumentParser(description='Importa entradas de jrnl a Tumblr.')
    parser.add_argument('jrnl_file', help='Ruta al archivo JSON exportado por jrnl')
    parser.add_argument('blog_name', help='Nombre del blog de Tumblr')

    # Parseo de los argumentos
    args = parser.parse_args()

    # Lectura del archivo jrnl
    entries = read_jrnl_file(args.jrnl_file)['entries']

    # Obtener credenciales de OAuth
    consumer_key, consumer_secret, oauth_token, oauth_secret = obtain_oauth_credentials()

    # Creación del cliente de Tumblr
    client = create_tumblr_client(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_secret
    )

    # Publicación de las entradas en Tumblr
    post_entries_to_tumblr(entries, client, args.blog_name)

if __name__ == '__main__':
    main()
