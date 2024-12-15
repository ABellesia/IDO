# Optimización de Rutas con Métodos Heurísticos y Metaheurísticos

## Formulación del Problema
El proyecto aborda el **Problema del Viajero (TSP)**, formulado desde el punto de vista de programación lineal como sigue:

- **Variables de decisión:**
  $x_{ij} = 1$ si el recorrido incluye el arco $(i,j)$; $x_{ij} = 0$ en caso contrario

- **Función objetivo:**  
  Minimizar la distancia total del recorrido: $\text{Minimizar: } \sum_{i=1}^n \sum_{j=1}^n c_{ij} x_{ij}$ donde $c_{ij}$ representa la distancia entre las ciudades $i$ y $j$.

- **Restricciones:**
  1. Cada ciudad debe ser visitada exactamente una vez:
     $$\sum_{j=1}^n x_{ij} = 1 \quad \forall i$$
  2. Cada ciudad tiene exactamente una llegada:
     $$\sum_{i=1}^n x_{ij} = 1 \quad \forall j$$
  3. Restricciones de subtour:
     $$u_i - u_j + n x_{ij} \leq n - 1 \quad \forall i, j, \, i \neq j$$

### Supuestos
- Todas las ciudades son visitadas exactamente una vez.
- Las distancias entre las ciudades son simétricas y definidas en un plano cartesiano.
- El recorrido comienza y termina en la misma ciudad.

---

## Métodos Implementados

### 1. Vecino Más Cercano
- Selecciona iterativamente la ciudad más cercana aún no visitada. Este método genera una solución inicial para los otros algoritmos.  
- **Ventaja:** Simplicidad.  
- **Desventaja:** Puede generar soluciones de baja calidad.  

#### Pseudocódigo:
```plaintext
Inicializar ciudad inicial y marcarla como visitada.
Mientras existan ciudades no visitadas:
    Encontrar la ciudad más cercana no visitada.
    Añadirla a la ruta y marcarla como visitada.
Regresar a la ciudad inicial.
```
### 2. 2-Opt
- Técnica de búsqueda local que invierte subrutas para mejorar la solución inicial.
- **Parámetro**: Máximo de iteraciones = 1000.
- **Ventaja**: Mejora la calidad del recorrido inicial.

#### Pseudocódigo 
```plaintext
Inicializar con la ruta del Vecino Más Cercano.
Mientras exista mejora:
    Para cada par de ciudades:
        Generar una nueva ruta invirtiendo un segmento.
        Si la distancia mejora, actualizar la solución.
```
### 3. Búsqueda Tabú 
- Utiliza una lista tabú para evitar ciclos y explorar soluciones subóptimas.
- **Parámetros**: Tenencia tabú = 30, iteraciones sin mejora = 25.
- **Ventaja**: Escapa de mínimos locales.

#### Pseudocódigo 
```plaintext
Inicializar solución y lista tabú.
Mientras no se alcance el límite:
    Generar soluciones vecinas.
    Seleccionar la mejor solución no tabú.
    Si mejora, actualizar solución y reiniciar el contador.
    Añadir el movimiento a la lista tabú.
```
### 4. Recocido Simulado 
- Metaheurística que utiliza una temperatura para aceptar soluciones subóptimas.
- **Parámetros**: Temperatura inicial = 1000, factor de enfriamiento = 0.99.
- **Ventaja**: Evita quedar atrapado en mínimos locales.

#### Pseudocódigo 
```plaintext
Inicializar solución y temperatura.
Mientras la temperatura sea mayor que un umbral:
    Generar una solución vecina aleatoria.
    Si mejora o cumple el criterio probabilístico, actualizar solución.
    Reducir la temperatura.
```
--- 
## Resultados 
### Tablas comparativas de métodos 
#### Qatar

| Método | Distancia optimizada | Tiempo de ejecución (s) |
| --- | --- | --- |
| 2 - Opt | XXX | XXX |
| Búsqueda Tabú | XXX | XXX |
| Recocido Simulado | XXX | XXX |

#### Uruguay

| Método | Distancia optimizada | Tiempo de ejecución (s) |
| --- | --- | --- |
| 2 - Opt | XXX | XXX |
| Búsqueda Tabú | XXX | XXX |
| Recocido Simulado | XXX | XXX |

#### Zimbabwe

| Método | Distancia optimizada | Tiempo de ejecución (s) |
| --- | --- | --- |
| 2 - Opt | XXX | XXX |
| Búsqueda Tabú | XXX | XXX |
| Recocido Simulado | XXX | XXX |

### Visualización
Se generaron gráficos para comparar visualmente las rutas optimizadas de cada método.

--- 

## Código implementado 
El código implementado está disponible en [este repositorio](https://github.com/ABellesia/IDO.git)

---
## Referencias 
1. Gutin, G., & Punnen, A. P. (Eds.). (2006). The Traveling Salesman Problem and Its Variations. Springer.
2. Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). Optimization by Simulated Annealing. Science, 220(4598), 671-680.
3. Johnson, D. S., & McGeoch, L. A. (1997). The Traveling Salesman Problem: A Case Study in Local Optimization. Handbook of Approximation Algorithms and Metaheuristics. Chapman & Hall/CRC.
