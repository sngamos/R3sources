# R3sources
A collection of interesting resources I thought might be useful next time.

## Learning Resources
1. [how2heap github repo](https://github.com/shellphish/how2heap)
    - Super informative repo for heap exploitation techniques.
2. [smashing the stack for fun and profit](/Docs/stack_smashing.pdf)
    - Classic article on stack exploitation.
3. [Basics of Windows shellcode writing](https://idafchev.github.io/exploit/2017/09/26/writing_windows_shellcode.html#find_dll)
    - Guide to writing Windows shellcode, including how to find DLLs and functions.
    - Uses PEB walking technique to locate kernel32.dll
4. [Introduction to Windows Shellcode Development](https://securitycafe.ro/2016/02/15/introduction-to-windows-shellcode-development-part-3/)
    - Uses PEB walking technique to locate `GetProcAddress` in kernel32.dll
    - Then uses `GetProcAddress` to resolve the addresses of other necessary functions.
    - More extensible than PEB walking every function

## Useful Blogposts
1. [pentestmonkey Reverse Shell Cheatsheet](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)
    - Great reverse shell commands

## Licence Keys/ Activating Products
1. [Massgrave](https://massgrave.dev/)
    - Site that provides scripts to activate Microsoft Office.
2. [Cracked IDA-Pro](https://drive.usercontent.google.com/download?id=1X7ZJP-7L_NqR8Hm3sjpnjLPnM3YldHDQ)
    - [Setup Guide](https://bbs.kanxue.com/thread-282846.htm) in Chinese.
    - Works on M series Macs and Windows (haven't tested on Linux).
    - Checked the signature, no malware.

## Useful Online Tools
1. [OCR2edit](https://www.ocr2edit.com)
    - Convert scanned PDFs to .txt outputs.
    - Can use this and github copilot to clean up texts.
2. [cyberchef](https://gchq.github.io/CyberChef/)
    - Great tool for encoding/decoding, encryption/decryption, and other data manipulation tasks.

## Reverse Engineering resources
### x86 Assembly
    - [x86 Instruction Set Reference](https://www.felixcloutier.com/x86/)
    - [x86 Opcode and Instruction Reference](https://ref.x86asm.net/coder32.html)
### MSDN
    - [MSDN x86 Assembly Reference](https://docs.microsoft.com/en-us/cpp/assembler/masm/microsoft-macro-assembler-reference?view=msvc-170)

    

## Some useful CVEs collections
> Word of caution: Any competent antivirus would have fingerprinted these exploits, **use at your own risk**.
> Windows Defender will flag them, you have to set exceptions for the file to be read.
### LPEs 
#### Copyfail
> lightweight 732 byte LPE exploit for Linux kernel 5.8-5.10.17, 5.11-5.11.11, 5.12-5.12.9, 5.13-5.13.12, 5.14-5.14.6, and 5.15-5.15.25

Website [here](https://copyfail.com)
script here: [copyfail](/CVEs/copyfail.py)

#### Copyfail K container escape
> adapted from copyfail, allows unprivileged containers to achieve node level code execution on kubernetes

Github repo: [here](https://github.com/Percivalll/Copy-Fail-CVE-2026-31431-Kubernetes-PoC)


