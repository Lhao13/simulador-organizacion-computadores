import claseUtil as util

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