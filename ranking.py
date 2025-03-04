import numpy as np
import pandas as pd

# Algoritmos evaluados
algoritmos = ["AES-128-GCM", "AES-256-GCM", "ChaCha20"]

# Matriz de decisiones basada en los datos experimentales
decision_matrix = np.array([
    [7.999564, 100.0, 1.029341, 1.059415],  # AES-128-GCM
    [7.999566, 100.0, 1.151710, 0.967696],  # AES-256-GCM
    [7.999563, 100.0, 1.045849, 1.116636]   # ChaCha20
])

# Ponderaciones AHP normalizadas
ahp_weights = np.array([0.485, 0.301, 0.092, 0.122])

# Normalizar la matriz de decisiones para TOPSIS
norm_matrix = decision_matrix / np.linalg.norm(decision_matrix, axis=0)

# Ponderar la matriz normalizada con los pesos AHP
weighted_matrix = norm_matrix * ahp_weights

# Determinar la mejor y peor solución para cada criterio
ideal_best = np.max(weighted_matrix, axis=0)
ideal_worst = np.min(weighted_matrix, axis=0)

# Calcular las distancias a las soluciones ideales
distance_best = np.linalg.norm(weighted_matrix - ideal_best, axis=1)
distance_worst = np.linalg.norm(weighted_matrix - ideal_worst, axis=1)

# Calcular el coeficiente TOPSIS
topsis_score = distance_worst / (distance_best + distance_worst)

# Determinar el ranking final
ranking = np.argsort(topsis_score)[::-1]

# Crear DataFrame con los resultados
df_topsis = pd.DataFrame({
    "Algoritmo": algoritmos,
    "Score TOPSIS": topsis_score,
    "Ranking": ranking + 1  # Para que el ranking empiece en 1
}).sort_values(by="Ranking")

# Mostrar resultados
print(df_topsis)

# Guardar en CSV
df_topsis.to_csv("ranking_topsis.csv", index=False)
