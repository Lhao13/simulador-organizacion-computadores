import random

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