# Simulador de jerarquía de memoria

Proyecto académico para explorar cómo se comportan una caché y los niveles de memoria ante operaciones de lectura y escritura. La propuesta plantea comparar implementaciones en un lenguaje de alto nivel y otro de bajo nivel; en esta carpeta se incluyen una implementación en Python y otra en ensamblador MASM.

**Fecha de implementación:** 2024/05  
**Integrantes de la propuesta:** Xavier Tandazo y Leandro Coral

## Implementaciones

### Python

El simulador de `SimuladorPy` representa la memoria principal y una caché configurable. Permite probar accesos individuales o aleatorios, observar secciones de la caché y la memoria, y consultar aciertos y fallos.

La configuración se expresa como potencias de dos: tamaño de memoria, tamaño de caché, tamaño de bloque y asociatividad. La interfaz de línea de comandos ofrece reemplazo LRU y políticas de escritura write-back (`WB`) y write-through (`WT`).

#### Requisitos

- Python 3
- No requiere paquetes externos

#### Ejecución

Desde la carpeta del proyecto:

```bash
cd SimuladorPy
python Simulador.py 10 6 2 1 LRU WB
```

Los argumentos representan, en orden:

| Argumento | Significado | Ejemplo |
| --- | --- | --- |
| `MEMORY` | Exponente del tamaño de memoria en bytes | `10` = 1024 bytes |
| `CACHE` | Exponente del tamaño de caché en bytes | `6` = 64 bytes |
| `BLOCK` | Exponente del tamaño de bloque en bytes | `2` = 4 bytes |
| `MAPPING` | Exponente del número de vías asociativas | `1` = 2 vías |
| `REPLACE` | Política de reemplazo habilitada en la interfaz | `LRU` |
| `WRITE` | Política de escritura | `WB` o `WT` |

Una vez iniciado, introduce un comando por línea:

| Comando | Acción |
| --- | --- |
| `read <direccion>` | Lee un byte de una dirección |
| `write <direccion> <valor>` | Escribe un valor en una dirección |
| `randread <cantidad>` | Lee direcciones aleatorias |
| `randwrite <cantidad>` | Escribe valores en direcciones aleatorias |
| `printcache <inicio> <cantidad>` | Muestra líneas de la caché |
| `printmem <inicio> <cantidad>` | Muestra bloques de memoria |
| `stats` | Muestra aciertos, fallos y el porcentaje de aciertos |
| `quit` | Termina el simulador |

### Ensamblador MASM

`Simulador en MASM/11.asm` contiene una versión de consola que permite configurar el tamaño de la caché, la memoria y el disco (hasta 20 posiciones por nivel), y realizar operaciones de lectura y escritura. Muestra el contenido de los niveles, los aciertos y fallos, y el tiempo medido con `CPUID` y `RDTSC`.

Para compilar y ejecutar esta versión se necesita Visual Studio con soporte MASM de 32 bits y la biblioteca Irvine32. Consulta `Simulador en MASM/Readme.txt` y `SimuladorPy/INSTRUCCIONES.txt` para las indicaciones disponibles. La biblioteca Irvine32 es una dependencia externa: el archivo ZIP local no se incluye en el repositorio.

## Alcance

El código disponible se centra en operaciones de caché y memoria desde una interfaz de consola. La propuesta también menciona coherencia MESI, ejecución multinúcleo y visualizaciones; esas capacidades no están implementadas en los archivos incluidos.
