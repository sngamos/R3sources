# Generates a cyclic pattern of bytes for use in exploit development, used to find offsets in buffer overflows 
# based on the unique sequence of bytes read into the program's memory during exploitation.

def gen_cyclic_bytes(req_len):
    chars=b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    buffer = bytearray()
    byte_counter = 0
    index =0
    while byte_counter < req_len:
        for i in range(3):
            buffer.extend([chars[index%len(chars)]])
            byte_counter += 1
        buffer.extend([index])
        index +=1
    if len(buffer) > req_len:
        buffer = buffer[:req_len]
    return bytes(buffer)

