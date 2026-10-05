import random
import claseUtil as util
from math import log
from claseLine import Line
import time

#-Clase de la cache del procesador---------------------------------------------------------------------------------------------------------------------
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

#-Lee un bloque de memoria de la caché.---------------------------------------------------------------------------------------------------------------------
    
    def read(self, address):

            start_time = time.time_ns()  # Tiempo inicial en nanosegundos
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

            end_time = time.time_ns()  # Tiempo final en nanosegundos
            read_time = end_time - start_time  # Tiempo de lectura en nanosegundos

            # Mostrar tiempo de lectura solo si es mayor que 0
            if read_time > 0:
                print(f"Tiempo de lectura: {read_time:.10f} nanosegundos")  # Mostrar tiempo de lectura en nanosegundos

            return line.data if line else line


#--Carga un bloque de memoria en la caché.--------------------------------------------------------------------------------------------------------------------

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

#-Escribe un byte en la caché.---------------------------------------------------------------------------------------------------------------------

    def write(self, address, byte):

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

#-Imprime una sección de la caché.---------------------------------------------------------------------------------------------------------------------

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

#-Dirección física de la línea de caché---------------------------------------------------------------------------------------------------------------------

    def get_physical_address(self, index):
        set_num = index // self._mapping_pol
        return ((self._lines[index].tag << self._tag_shift) +
                (set_num << self._set_shift))

#-Desplazamiento dentro de un conjunto a partir de una dirección física---------------------------------------------------------------------------------------------------------------------

    def get_offset(self, address):
        return address & (self._block_size - 1)

#-Etiqueta de la línea de caché a partir de una dirección física---------------------------------------------------------------------------------------------------------------------

    def _get_tag(self, address):
        return address >> self._tag_shift

#-Conjunto de líneas de caché a partir de una dirección física---------------------------------------------------------------------------------------------------------------------

    def _get_set(self, address):
        set_mask = (self._size // (self._block_size * self._mapping_pol)) - 1
        set_num = (address >> self._set_shift) & set_mask
        index = set_num * self._mapping_pol
        return self._lines[index:index + self._mapping_pol]

#-Actualiza el usoo de bits de cada linea de cache---------------------------------------------------------------------------------------------------------------------

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