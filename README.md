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
El algoritmo del Vecino Más Cercano es una heurística greedy que genera una solución inicial rápida. La idea principal es elegir la ciudad más cercana a la actual que aún no haya sido visitada, y repetir hasta completar el recorrido.

#### Ventajas 
- **Simplicidad**: Es fácil de entender e implementar, con una complejidad computacional de $O(n^2)$ donde $n$ es el número de ciudades.
- **Rapidez**: Produce soluciones en tiempos muy cortos, lo que lo hace adecuado para generar soluciones iniciales en métodos más avanzados.
#### Desventajas 
- **Miopía**: Al tomar decisiones solo basadas en la ciudad más cercana, puede llevar a soluciones subóptimas. Ejemplo: En instancias donde las ciudades están distribuidas en clústeres, puede ignorar trayectorias más eficientes en favor de rutas locales.
- **Calidad**: La solución suele estar lejos del óptimo global, con errores de hasta un 25-30% respecto al mejor resultado en problemas grandes.
#### Justificación 
A pesar de sus desventajas, esta heurística es un excelente punto de partida. Muchas metaheurísticas (como 2-Opt, Tabú o Recocido Simulado) utilizan soluciones generadas por el Vecino Más Cercano como inicialización, debido a su rapidez y facilidad de cálculo.
#### Pseudocódigo:
```plaintext
Inicializar ciudad inicial y marcarla como visitada.
Mientras existan ciudades no visitadas:
    Encontrar la ciudad más cercana no visitada.
    Añadirla a la ruta y marcarla como visitada.
Regresar a la ciudad inicial.
```
### 2. 2-Opt
El 2-Opt es una heurística de búsqueda local que mejora una solución inicial invirtiendo subrutas dentro del recorrido. El objetivo es eliminar intersecciones en la ruta, lo que suele resultar en trayectorias más cortas.
- **Parámetro**: Máximo de iteraciones = 1000.
- **Ventaja**: Mejora la calidad del recorrido inicial.
#### Ventajas 
- **Calidad de las soluciones**: Tiende a reducir significativamente la longitud del recorrido inicial, acercándose al óptimo global en problemas pequeños o medianos.
- **Implementación sencilla**: Aunque explora todas las posibles combinaciones de inversión de subrutas, el proceso es intuitivo y fácilmente optimizable.
#### Desventajas 
- **Eficiencia**: Con una complejidad de $O(n^2)$ por iteración, puede ser costoso en problemas con muchas ciudades si no se limita el número de iteraciones.
- **Estancamiento en mínimos locales**: Puede quedar atrapado en un óptimo local, ya que no tiene mecanismos para explorar soluciones subóptimas.
#### Justificación 
El 2-Opt es ideal para mejorar soluciones iniciales, ya que logra un balance entre calidad y tiempo de ejecución. Aunque no garantiza encontrar el óptimo global, es una herramienta estándar en la optimización de rutas.

#### Pseudocódigo 
```plaintext
Inicializar con la ruta del Vecino Más Cercano.
Mientras exista mejora:
    Para cada par de ciudades:
        Generar una nueva ruta invirtiendo un segmento.
        Si la distancia mejora, actualizar la solución.
```
### 3. Búsqueda Tabú 
La Búsqueda Tabú es una metaheurística que mejora sobre la búsqueda local al incorporar una lista de movimientos "prohibidos" (tabú) para evitar ciclos o revisitar soluciones ya exploradas. Esto le permite escapar de mínimos locales y explorar más el espacio de soluciones.
- **Parámetros**: Tenencia tabú = 30, iteraciones sin mejora = 25.
- **Ventaja**: Escapa de mínimos locales.
#### Ventajas
- **Exploración** efectiva: La lista tabú introduce diversificación, ayudando a escapar de mínimos locales y explorar soluciones subóptimas.
- **Flexibilidad**: Puede adaptarse mediante la configuración de parámetros, como la tenencia tabú (cuántos movimientos se prohíben) o las condiciones de aspiración (permitir movimientos tabú si mejoran el óptimo).
#### Desventajas 
- **Complejidad**: Ajustar los parámetros adecuados (tenencia tabú, criterios de terminación) puede ser un desafío.
- **Costo computacional**: La gestión de la lista tabú y la evaluación de soluciones vecinas puede incrementar el tiempo de ejecución.
#### Justificación
La Búsqueda Tabú es una poderosa herramienta para superar los límites de los métodos locales simples, como el 2-Opt. Es particularmente útil en problemas grandes donde los mínimos locales son un problema común. Sin embargo, requiere más esfuerzo en diseño y parametrización.
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
El Recocido Simulado (Simulated Annealing) es una metaheurística inspirada en el proceso de enfriamiento de los metales. Combina exploración global y búsqueda local aceptando soluciones subóptimas basadas en una probabilidad controlada por la "temperatura", que disminuye gradualmente.
- **Parámetros**: Temperatura inicial = 1000, factor de enfriamiento = 0.99.
- **Ventaja**: Evita quedar atrapado en mínimos locales.
#### Ventajas 
- **Escapa de mínimos locales**: Gracias a la aceptación probabilística de peores soluciones, puede encontrar mejores óptimos en comparación con métodos puramente locales.
- **Simplicidad conceptual**: Aunque requiere varios parámetros (temperatura inicial, factor de enfriamiento, iteraciones por nivel), es fácil de implementar.
#### Desventajas 
- **Dependencia de parámetros**: Elegir una temperatura inicial adecuada y un factor de enfriamiento es crítico. Parámetros mal ajustados pueden dar soluciones de baja calidad o tiempos de ejecución innecesariamente largos.
- **Costo computacional**: Aunque menos costoso que algoritmos más complejos (como los genéticos), puede ser más lento que 2-Opt o Tabú en problemas pequeños.
#### Justificación 
El Recocido Simulado es ideal para problemas en los que se prioriza la exploración del espacio de búsqueda. Es particularmente útil en instancias donde los mínimos locales son frecuentes. Sin embargo, su eficiencia depende de la calibración adecuada de parámetros, lo que puede ser un desafío.
#### Pseudocódigo 
```plaintext
Inicializar solución y temperatura.
Mientras la temperatura sea mayor que un umbral:
    Generar una solución vecina aleatoria.
    Si mejora o cumple el criterio probabilístico, actualizar solución.
    Reducir la temperatura.
```

### 5. Comparación general entre métodos 
| Método | Ventajas |	Desventajas |	Escenarios ideales |
| --- | --- | --- | --- |
| Vecino Más Cercano	| Simplicidad, rapidez	| Calidad subóptima, miopía |	Generación rápida de soluciones iniciales. |
| 2-Opt |	Mejora significativa de soluciones iniciales	| Puede estancarse en mínimos locales	 | Problemas pequeños a medianos. |
| Búsqueda Tabú |	Escapa de mínimos locales, flexible |	Costo computacional y parametrización compleja	| Problemas grandes con muchos mínimos locales. |
| Recocido Simulado	| Explora soluciones globales, adaptable |	Dependencia de parámetros, costo computacional |	Problemas medianos a grandes. |
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
#### Qatar 
##### 2 - Opt 
![image](https://github.com/user-attachments/assets/c3cb8e83-5481-4af0-b391-2506864cb04d)

#####  Búsqueda Tabú
![image](https://github.com/user-attachments/assets/69668adf-adf7-424e-9e2e-6394371ca7f0)

##### Recocido Simulado 
![image](https://github.com/user-attachments/assets/1c470c45-6044-477c-a170-df1623a5dc56)


--- 

## Código implementado 
El código implementado está disponible en [este repositorio](https://github.com/ABellesia/IDO.git)

---
## Referencias 
1. Gutin, G., & Punnen, A. P. (Eds.). (2006). The Traveling Salesman Problem and Its Variations. Springer.
2. Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). Optimization by Simulated Annealing. Science, 220(4598), 671-680.
3. Johnson, D. S., & McGeoch, L. A. (1997). The Traveling Salesman Problem: A Case Study in Local Optimization. Handbook of Approximation Algorithms and Metaheuristics. Chapman & Hall/CRC.

