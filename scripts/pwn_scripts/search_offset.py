# Searches for the offset of a specific sequence within a cyclic pattern of bytes.

def search_offset_windbg(hex_str,file_path):
    hex_str = hex_str.strip().replace("0x",'')
    if len(hex_str) !=8:
            print("Input must be 4 bytes long")
            return -1
    search_bytes = bytes.fromhex(hex_str)[::-1]
    with open(file_path, 'rb') as f:
        file_contents = f.read()
    offset = file_contents.find(search_bytes)
    if offset == -1:
        print("Sequence not found in file")
        return -1
    print(f"Sequence found at offset: {offset}")
    return offset

search_offset_windbg("0x41414141", "cyclic_pattern.bin")