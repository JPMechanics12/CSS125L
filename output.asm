section .text
   org 0x100
start:
   mov ax,3
   int 0x10
main:
mov ax,0000
mov bx,0000
mov cx,0000
mov dx,0000
  LEA DX,[msgn1]
  mov ah,0x09
  int 0x21
  LEA DX,[msgn1]
  mov ah,0x09
  int 0x21
  LEA DX,[msgn1]
  mov ah,0x09
  int 0x21
  int 0x20
section .data
msgn1: db 0x0A, 0x0D, "Hello World $"
msgn2: db 0x0A, 0x0D, "Hello World $"
msgn3: db 0x0A, 0x0D, "Hello World $"