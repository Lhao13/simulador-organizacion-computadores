from math import log
import random
import time
import argparse
import timeit

class util:
    #---------------------------------------------------------------------------

    def rand_byte():

        return random.randint(0, 0xFF)

    #---------------------------------------------------------------------------

    def dec_str(integer, width):

        return "{0:0>{1}}".format(integer, width)

    #---------------------------------------------------------------------------

    def bin_str(integer, width):

        return "{0:0>{1}b}".format(integer, width)

    #---------------------------------------------------------------------------

    def hex_str(integer, width):

        return "{0:0>{1}X}".format(integer, width)
    

class Line:

    def __init__(self, size):
        self.use = 0
        self.modified = 0
        self.valid = 0
        self.tag = 0
        self.data = [0] * size


# Clase de la cache del procesador
class Cache:
    # Políticas de mapeo
    writeb = "WB"
    writet = "WT"
    
    # Políticas de reemplazo
    LRU = "LRU"
    LFU = "LFU"
    FIFO = "FIFO"
    RAND = "RAND"

    def __init__(self, size, mem_size, block_size, mapping_pol, replace_pol,
                 write_pol):
        
        self._lines = [Line(block_size) for i in range(size // block_size)]

        self._mapping_pol = mapping_pol  # Política de mapeo
        self._replace_pol = replace_pol  # Política de reemplazo
        self._write_pol = write_pol  # Política de escritura

        self._size = size  # Tamaño de la caché
        self._mem_size = mem_size  # Tamaño de la memoria
        self._block_size = block_size  # Tamaño del bloque

        # Desplazamiento de bits para la etiqueta de la línea de caché
        self._tag_shift = int(log(self._size // self._mapping_pol, 2))
        # Desplazamiento de bits para el conjunto de líneas de caché
        self._set_shift = int(log(self._block_size, 2))

    # Lee un bloque de memoria de la caché
    def read(self, address):
        tag = self._get_tag(address)  # Tag de la línea de caché
        set = self._get_set(address)  # Conjunto de líneas de caché
        line = None

        # Buscar la línea de caché dentro del conjunto
        for candidate in set:
            if candidate.tag == tag and candidate.valid:
                line = candidate
                break

        # Actualizar bits de uso de la línea de caché
        if line:
            if self._replace_pol == Cache.LRU:
                self._update_use(line, set)

        return line.data if line else line

    # Carga un bloque de memoria en la caché
    def load(self, address, data):
        tag = self._get_tag(address)  # Etiqueta de la línea de caché
        set = self._get_set(address)  # Conjunto de líneas de caché
        victim_info = None

        # Selecciona la víctima
        if (self._replace_pol == Cache.LRU or
            self._replace_pol == Cache.LFU or
            self._replace_pol == Cache.FIFO):
            victim = set[0]

            for index in range(len(set)):
                if set[index].use < victim.use:
                    victim = set[index]

            victim.use = 0

            if self._replace_pol == Cache.FIFO:
                self._update_use(victim, set)
        elif self._replace_pol == Cache.RAND:
            index = random.randint(0, self._mapping_pol - 1)
            victim = set[index]

        # Almacena la información de la víctima si está modificada
        if victim.modified:
            victim_info = (index, victim.data)

        # Reemplaza la víctima
        victim.modified = 0
        victim.valid = 1
        victim.tag = tag
        victim.data = data

        return victim_info

    # Escribe un byte en la caché
    def write(self, address, byte):
        start_time = time.time_ns()  # Tiempo inicial en nanosegundos

        tag = self._get_tag(address)  # Etiqueta de la línea de caché
        set = self._get_set(address)  # Conjunto de líneas de caché
        line = None

        # Busca la línea de caché dentro del conjunto
        for candidate in set:
            if candidate.tag == tag and candidate.valid:
                line = candidate
                break

        # Actualiza los datos de la línea de caché
        if line:
            line.data[self.get_offset(address)] = byte
            line.modified = 1

            if (self._replace_pol == Cache.LRU or
                self._replace_pol == Cache.LFU):
                self._update_use(line, set)

        return True if line else False

    # Imprime una sección de la caché
    def print_section(self, start, amount):
        line_len = len(str(self._size // self._block_size - 1))
        use_len = max([len(str(i.use)) for i in self._lines])
        tag_len = int(log(self._mapping_pol * self._mem_size // self._size, 2))
        address_len = int(log(self._mem_size, 2))

        if start < 0 or (start + amount) > (self._size // self._block_size):
            raise IndexError

        print("\n" + " " * line_len + " " * use_len + " U M V T" +
              " " * tag_len + "<DATA @ ADDRESS>")

        for i in range(start, start + amount):
            print(util.dec_str(i, line_len) + ": " +
                  util.dec_str(self._lines[i].use, use_len) + " " +
                  util.bin_str(self._lines[i].modified, 1) + " " +
                  util.bin_str(self._lines[i].valid, 1) + " " +
                  util.bin_str(self._lines[i].tag, tag_len) + " <" +
                  " ".join([util.hex_str(i, 2) for i in self._lines[i].data]) + " @ " +
                  util.bin_str(self.get_physical_address(i), address_len) + ">")
        print()

    # Dirección física de la línea de caché
    def get_physical_address(self, index):
        set_num = index // self._mapping_pol
        return ((self._lines[index].tag << self._tag_shift) +
                (set_num << self._set_shift))

    # Desplazamiento dentro de un conjunto a partir de una dirección física
    def get_offset(self, address):
        return address & (self._block_size - 1)

    # Etiqueta de la línea de caché a partir de una dirección física
    def _get_tag(self, address):
        return address >> self._tag_shift

    # Conjunto de líneas de caché a partir de una dirección física
    def _get_set(self, address):
        set_mask = (self._size // (self._block_size * self._mapping_pol)) - 1
        set_num = (address >> self._set_shift) & set_mask
        index = set_num * self._mapping_pol
        return self._lines[index:index + self._mapping_pol]

    # Actualiza el uso de bits de cada línea de caché
    def _update_use(self, line, set):
        if (self._replace_pol == Cache.LRU or
            self._replace_pol == Cache.FIFO):
            use = line.use

            if line.use < self._mapping_pol:
                line.use = self._mapping_pol
                for other in set:
                    if other is not line and other.use > use:
                        other.use -= 1
        elif self._replace_pol == Cache.LFU:
            line.use += 1

#RAM-----------------------------------------------------------------------------------------------------------------------------
# Clase para simular la RAM
class RAM:
    def __init__(self, size, block_size):
        self.size = size
        self.block_size = block_size
        self.memory = {}

    def load(self, address, block):
        block_address = address // self.block_size
        self.memory[block_address] = block
        return block

    def is_full(self):
        return len(self.memory) >= self.size // self.block_size

    def get_block(self, address):
        block_address = address // self.block_size
        return self.memory.get(block_address, None)

    def set_block(self, address, block):
        block_address = address // self.block_size
        self.memory[block_address] = block



#-Clase de la memoria---------------------------------------------------------------------------------------------------------------------
class Memory:

    def __init__(self, size, block_size):
        self._size = size  # Memory size
        self._block_size = block_size  # Block size
        self._data = [util.rand_byte() for i in range(size)]

    #----Imprimir una sección de la memoria principal------------------------------------------------------------------------------------------------------------------

    def print_section(self, start, amount):

        address_len = len(str(self._size - 1))
        start = start - (start % self._block_size)
        amount *= self._block_size

        if start < 0 or (start + amount) > self._size:
            raise IndexError

        print()
        for i in range(start, start + amount, self._block_size):
            print(util.dec_str(i, address_len) + ": " +
                  " ".join([util.hex_str(i, 2) for i in self.get_block(i)]))
        print()

    #----Obtener el bloque de memoria principal------------------------------------------------------------------------------------------------------------------

    def get_block(self, address):

        start = address - (address % self._block_size)  # Start address
        end = start + self._block_size  # End address

        if start < 0 or end > self._size:
            raise IndexError

        return self._data[start:end]

    #----Establecer el bloque de memoria principal------------------------------------------------------------------------------------------------------------------

    def set_block(self, address, data):

        start = address - (address % self._block_size)  # Start address
        end = start + self._block_size  # End address

        if start < 0 or end > self._size:
            raise IndexError

        self._data[start:end] = data

#Simulador
#-Lee un byte de la caché---------------------------------------------------------------------------------------------------------------------

def read(address, memory, cache, ram):
    t_0 = timeit.default_timer()

    # Intenta leer desde la caché
    cache_block = cache.read(address)

    if cache_block:
        global hits
        hits += 1
        print("Data read from cache")
    else:
        # Si no está en caché, intenta desde la RAM
        block = ram.get_block(address)
        if block:
            cache.load(address, block)
            cache_block = cache.read(address)
            print("Data read from RAM")
        else:
            # Si no está en la RAM, lee desde la memoria principal
            block = memory.get_block(address)
            cache.load(address, block)
            cache_block = cache.read(address)
            print("Data read from memory")

    t_1 = timeit.default_timer()
    elapsed_time = round((t_1 - t_0) * 10 ** 6, 3)
    print(f"Elapsed time: {elapsed_time} µs")

    return cache_block[cache.get_offset(address)]

# Escribe un byte en la caché y posiblemente en la RAM
def write(address, byte, memory, cache, ram):
    t_0 = timeit.default_timer()

    # Intenta escribir en la caché
    written = cache.write(address, byte)

    if written:
        global hits
        hits += 1
    else:
        global misses
        misses += 1

    # Si se usa la política de escritura write-back, también actualiza la RAM
    if args.WRITE == Cache.writeb:
        if not written:
            block = memory.get_block(address)
            ram.load(address, block)  # Carga el bloque en la RAM
            cache.load(address, block)
            cache.write(address, byte)

    t_1 = timeit.default_timer()
    elapsed_time = round((t_1 - t_0) * 10 ** 6, 3)
    print(f"Elapsed time: {elapsed_time} µs")


#-Definición de políticas de reemplazo y escritura---------------------------------------------------------------------------------------------------------------------

replacement_policies = ["LRU"]
write_policies = ["WB", "WT"]

parser = argparse.ArgumentParser(description="Simula la caché de una CPU.")

parser.add_argument("MEMORY", metavar="MEMORY", type=int,
                    help="Tamaño de la memoria principal en 2^N bytes")
parser.add_argument("CACHE", metavar="CACHE", type=int,
                    help="Tamaño de la caché en 2^N bytes")
parser.add_argument("BLOCK", metavar="BLOCK", type=int,
                    help="Tamaño de un bloque de memoria en 2^N bytes")
parser.add_argument("MAPPING", metavar="MAPPING", type=int,
                    help="Política de mapeo para la caché en 2^N vías")
parser.add_argument("REPLACE", metavar="REPLACE", choices=replacement_policies,
                    help="Política de reemplazo para la caché {"+", ".join(replacement_policies)+"}")
parser.add_argument("WRITE", metavar="WRITE", choices=write_policies,
                    help="Política de escritura para la caché {"+", ".join(write_policies)+"}")

args = parser.parse_args()



mem_size = 2 ** args.MEMORY
cache_size = 2 ** args.CACHE
block_size = 2 ** args.BLOCK
mapping = 2 ** args.MAPPING
ram_size = mem_size // 2
ram_block_size = 2 ** args.BLOCK

# Calcula el tamaño de la memoria RAM
ram_memory_size = ram_size * ram_block_size

hits = 0
misses = 0

memory = Memory(mem_size, block_size)
cache = Cache(cache_size, mem_size, block_size,
              mapping, args.REPLACE, args.WRITE)
ram = RAM(ram_size, ram_block_size)

mapping_str = "2^{0}-vías asociativas".format(args.MAPPING)
print("\nTamaño de la memoria: " + str(mem_size) +
      " bytes (" + str(mem_size // block_size) + " bloques)")
print("Tamaño de la memoria RAM: " + str(ram_size) +
      " bytes (" + str(ram_size // ram_block_size) + " bloques)")
print("Tamaño de la caché: " + str(cache_size) +
      " bytes (" + str(cache_size // block_size) + " líneas)")
print("Tamaño de bloque: " + str(block_size) + " bytes")
print("Política de mapeo: " + ("directo" if mapping == 1 else mapping_str) + "\n")

command = None

#-Bucle principal para operaciones---------------------------------------------------------------------------------------------------------------------

# Bucle principal para operaciones
while (command != "quit"):
    operation = input("> ")
    operation = operation.split()

    try:
        command = operation[0]
        params = operation[1:]

        if command == "read" and len(params) == 1:
            address = int(params[0])
            byte = read(address, memory, cache, ram)

            print("\nByte 0x" + util.hex_str(byte, 2) + " leído desde " +
                  util.bin_str(address, args.MEMORY) + "\n")

        elif command == "write" and len(params) == 2:
            address = int(params[0])
            byte = int(params[1])

            write(address, byte, memory, cache, ram)

            print("\nByte 0x" + util.hex_str(byte, 2) + " escrito en " +
                  util.bin_str(address, args.MEMORY) + "\n")

        elif command == "randread" and len(params) == 1:
            amount = int(params[0])

            for i in range(amount):
                address = random.randint(0, mem_size - 1)
                read(address, memory, cache)

            print("\n" + str(amount) + " bytes leídos de la memoria\n")

        elif command == "randwrite" and len(params) == 1:
            amount = int(params[0])

            for i in range(amount):
                address = random.randint(0, mem_size - 1)
                byte = util.rand_byte()
                write(address, byte, memory, cache)

            print("\n" + str(amount) + " bytes escritos en la memoria\n")

        elif command == "printcache" and len(params) == 2:
            start = int(params[0])
            amount = int(params[1])

            cache.print_section(start, amount)

        elif command == "printmem" and len(params) == 2:
            start = int(params[0])
            amount = int(params[1])

            memory.print_section(start, amount)

        elif command == "stats" and len(params) == 0:
            ratio = (hits / ((hits + misses) if misses else 1)) * 100

            print("\nAciertos: {0} | Fallos: {1}".format(hits, misses))
            print("Ratio de Aciertos/Fallos: {0:.2f}%".format(ratio) + "\n")

        elif command != "quit":
            print("\nERROR: comando inválido\n")

    except IndexError:
        print("\nERROR: fuera de límites\n")