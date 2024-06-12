import requests
import json
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from requests_html import HTMLSession

# Function to generate key using PBKDF2
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def decrypt(data, key, handle_padding_error=False):
    salt = data[:16]
    iv = data[16:32]
    ciphertext = data[32:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Attempt to unpad the data
    try:
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return unpadded_data
    except ValueError as e:
        if handle_padding_error:
            # If padding error occurs, return decrypted data without padding
            return decrypted_data
        else:
            raise e  # Re-raise the exception if not handling padding error

def XGRCViewTable(username, password, table, api_key):
    # Define the URL
    url = 'https://awesomeapi.xgrc.cloud/XGRC_TableView?query=Hakware:Allow'

    try:
        # Create an HTMLSession object
        session = HTMLSession()

        # Define headers
        headers = {
            "username": username,
            "password": password,
        }

        # Define query parameters
        params = {
            "TableName": table
        }

        # Make a GET request to the URL
    
        response = session.get(url,headers=headers, params=params)


        

        # Check if the response status code is 200
        if response.status_code == 200:
            # Extract the JSON object from the response
            try:
                json_response = response.json()
            except json.decoder.JSONDecodeError:
                print("Error: Invalid JSON data returned by the server.")
                
                exit()

            # Extract the encrypted data (XGRC_Object) from the JSON response
            encrypted_data_b64 = json_response.get('XGRC_Object')

            # Decode the base64 encoded ciphertext
            encrypted_data = base64.b64decode(encrypted_data_b64)

            # Generate a key using the same password and salt used for encryption
            password = api_key
            salt = encrypted_data[:16]
            key = generate_key(password, salt)

            # Decrypt the ciphertext using the key
            #decrypted_data = decrypt(encrypted_data, key)
            decrypted_data = decrypt(encrypted_data, key, handle_padding_error=True)

            # Convert the decrypted data to JSON
            try:
                # Decode the decrypted data using UTF-8 encoding
                decrypted_json = decrypted_data.decode('utf-8')
            except UnicodeDecodeError:
                # If decoding as UTF-8 fails, attempt to load the JSON data without assuming any encoding
                try:
                    decrypted_json = decrypted_data.decode()
                except UnicodeDecodeError:
                    return("Error: Unable to decode the decrypted data.")
                    
            # Print the decrypted JSON object
            return("Decrypted JSON:", decrypted_json)
        else:
            return("Error: Request failed with status code", response.status_code)
            
    except requests.exceptions.RequestException as e:
        return("Error:", e)
        


def XGRCSPView(username, password, SPName, api_key):
    # Define the URL
    url = 'https://awesomeapi.xgrc.cloud/XGRC_SPView?query=Hakware:Allow'

    try:
        # Create an HTMLSession object
        session = HTMLSession()

        # Define headers
        headers = {
            "username": username,
            "password": password,
        }

        # Define query parameters
        params = {
            "SPName": SPName
        }

        # Make a GET request to the URL
    
        response = session.get(url,headers=headers, params=params)


        

        # Check if the response status code is 200
        if response.status_code == 200:
            # Extract the JSON object from the response
            try:
                json_response = response.json()
            except json.decoder.JSONDecodeError:
                print("Error: Invalid JSON data returned by the server.")
                
                exit()

            # Extract the encrypted data (XGRC_Object) from the JSON response
            encrypted_data_b64 = json_response.get('XGRC_Object')

            # Decode the base64 encoded ciphertext
            encrypted_data = base64.b64decode(encrypted_data_b64)

            # Generate a key using the same password and salt used for encryption
            password = api_key
            salt = encrypted_data[:16]
            key = generate_key(password, salt)

            # Decrypt the ciphertext using the key
            #decrypted_data = decrypt(encrypted_data, key)
            decrypted_data = decrypt(encrypted_data, key, handle_padding_error=True)

            # Convert the decrypted data to JSON
            try:
                # Decode the decrypted data using UTF-8 encoding
                decrypted_json = decrypted_data.decode('utf-8')
            except UnicodeDecodeError:
                # If decoding as UTF-8 fails, attempt to load the JSON data without assuming any encoding
                try:
                    decrypted_json = decrypted_data.decode()
                except UnicodeDecodeError:
                    return("Error: Unable to decode the decrypted data.")
                    
            # Print the decrypted JSON object
            return("Decrypted JSON:", decrypted_json)
        else:
            return("Error: Request failed with status code", response.status_code)
            
    except requests.exceptions.RequestException as e:
        return("Error:", e)
        




















