import argparse
import random
import claseUtil as util
from claseCache import Cache
from claseMemory import Memory

#-Lee un byte de la caché---------------------------------------------------------------------------------------------------------------------

def read(address, memory, cache):
    cache_block = cache.read(address)

    if cache_block:
        global hits
        hits += 1
    else:
        block = memory.get_block(address)
        victim_info = cache.load(address, block)
        cache_block = cache.read(address)

        global misses
        misses += 1

        # Escribe el bloque de la línea víctima en la memoria si es reemplazado
        if victim_info:
            memory.set_block(victim_info[0], victim_info[1])

    return cache_block[cache.get_offset(address)]

#-Escribe un byte en la caché---------------------------------------------------------------------------------------------------------------------

def write(address, byte, memory, cache):
    written = cache.write(address, byte)

    if written:
        global hits
        hits += 1
    else:
        global misses
        misses += 1

    if args.WRITE == Cache.writet:
        # Escribe el bloque en la memoria
        block = memory.get_block(address)
        block[cache.get_offset(address)] = byte
        memory.set_block(address, block)
    elif args.WRITE == Cache.writeb:
        if not written:
            # Escribe el bloque en la caché
            block = memory.get_block(address)
            cache.load(address, block)
            cache.write(address, byte)

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

hits = 0
misses = 0

memory = Memory(mem_size, block_size)
cache = Cache(cache_size, mem_size, block_size,
              mapping, args.REPLACE, args.WRITE)

mapping_str = "2^{0}-vías asociativas".format(args.MAPPING)
print("\nTamaño de la memoria: " + str(mem_size) +
      " bytes (" + str(mem_size // block_size) + " bloques)")
print("Tamaño de la caché: " + str(cache_size) +
      " bytes (" + str(cache_size // block_size) + " líneas)")
print("Tamaño de bloque: " + str(block_size) + " bytes")
print("Política de mapeo: " + ("directo" if mapping == 1 else mapping_str) + "\n")

command = None

#-Bucle principal para operaciones---------------------------------------------------------------------------------------------------------------------

while (command != "quit"):
    operation = input("> ")
    operation = operation.split()

    try:
        command = operation[0]
        params = operation[1:]

        if command == "read" and len(params) == 1:
            address = int(params[0])
            byte = read(address, memory, cache)

            print("\nByte 0x" + util.hex_str(byte, 2) + " leído desde " +
                  util.bin_str(address, args.MEMORY) + "\n")

        elif command == "write" and len(params) == 2:
            address = int(params[0])
            byte = int(params[1])

            write(address, byte, memory, cache)

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
    except:
        print("\nERROR: sintaxis incorrecta\n")