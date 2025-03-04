import os
import time
import hashlib
import numpy as np
import scipy.stats
import pydicom
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import pandas as pd

# Función para calcular la entropía de Shannon
def shannon_entropy(data):
    _, counts = np.unique(list(data), return_counts=True)
    probs = counts / counts.sum()
    return scipy.stats.entropy(probs, base=2)

# Función para calcular el hash SHA-256
def calculate_hash(data):
    return hashlib.sha256(data).hexdigest()

# Función de cifrado y descifrado con AES-GCM
def encrypt_aes_gcm(data, key):
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    start_time = time.time()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    encrypt_time = (time.time() - start_time) * 1000  # Convertir a ms
    return ciphertext, tag, iv, encrypt_time

def decrypt_aes_gcm(ciphertext, tag, key, iv):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    start_time = time.time()
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    decrypt_time = (time.time() - start_time) * 1000  # Convertir a ms
    return plaintext, decrypt_time

# Cargar archivos DICOM desde la misma carpeta del script
dicom_files = {
    "100Kb": ("cai3\primero.dcm", 12),
    "500Kb": ("cai3\segundo.dcm", 46),
    "1000Kb": ("cai3\mil.dcm", 24),
    "1500Kb": ("cai3\cuarto.dcm", 18)
}

# Claves aleatorias para cada algoritmo
keys = {
    "AES-128-GCM": get_random_bytes(16),
    "AES-256-GCM": get_random_bytes(32),
    "ChaCha20": get_random_bytes(32)
}

# Almacenar resultados
results = {algo: {"Conf": [], "Int": [], "T_cif": [], "T_descif": []} for algo in keys}

# Procesar cada imagen DICOM con cada algoritmo
for size, (filename, repetitions) in dicom_files.items():
    if os.path.exists(filename):
        dicom_data = pydicom.dcmread(filename).PixelData

        if dicom_data:  # Check if dicom_data is not empty
            for _ in range(repetitions):
                for algo in keys:
                    key = keys[algo]

                    try:
                        # Cifrar
                        ciphertext, tag, iv, encrypt_time = encrypt_aes_gcm(dicom_data, key)

                        # Calcular entropía del cifrado
                        entropy = shannon_entropy(ciphertext)

                        # Descifrar
                        decrypted_data, decrypt_time = decrypt_aes_gcm(ciphertext, tag, key, iv)

                        # Calcular integridad (hash)
                        original_hash = calculate_hash(dicom_data)
                        decrypted_hash = calculate_hash(decrypted_data)
                        integrity = 100 if original_hash == decrypted_hash else 0

                        # Almacenar resultados
                        results[algo]["Conf"].append(entropy)
                        results[algo]["Int"].append(integrity)
                        results[algo]["T_cif"].append(encrypt_time)
                        results[algo]["T_descif"].append(decrypt_time)
                    except Exception as e:
                        print(f"Error processing {filename} with {algo}: {e}")
        else:
            print(f"Warning: {filename} is empty or could not be read correctly.")
    else:
        print(f"Warning: {filename} does not exist.")

# Calcular promedios
summary_results = {
    algo: {
        "Conf": np.mean(results[algo]["Conf"]),
        "Int": np.mean(results[algo]["Int"]),
        "T_cif": np.mean(results[algo]["T_cif"]),
        "T_descif": np.mean(results[algo]["T_descif"])
    }
    for algo in keys
}

# Mostrar resultados


df_results = pd.DataFrame(summary_results).T
df_results.columns = ["Entropía (Conf)", "Integridad (%)", "Tiempo Cifrado (ms)", "Tiempo Descifrado (ms)"]
print(df_results)

# Guardar los resultados en un CSV
df_results.to_csv("resultados_cifrado.csv", index=True)
