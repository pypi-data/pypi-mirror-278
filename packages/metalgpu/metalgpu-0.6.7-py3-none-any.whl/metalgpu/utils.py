import numpy as np
import ctypes

# table[0]: Metal type, table[1]: numpy type, table[2]: ctypes type, table[2:]: Unspecified
tables = [
    ["int", np.int32, ctypes.c_int],
    ["float", np.float32, ctypes.c_float],
    ["short", np.int16, ctypes.c_int16],
    ["bool", np.bool_, ctypes.c_bool, np.byte],
    ["uint", np.uint32, ctypes.c_uint, "uint32"],
    ["long", np.int64, ctypes.c_long, "int64", "int64_t"],
    ["uint64_t", np.uint64, ctypes.c_ulong, "uint64"]
]


def anyToMetal(receivedType):
    for table in tables:
        if receivedType in table:
            return table[0]


def anyToCtypes(receivedType):
    for table in tables:
        if receivedType in table:
            return table[2]


def anyToNumpy(receivedType):
    for table in tables:
        if receivedType in table:
            return table[1]
