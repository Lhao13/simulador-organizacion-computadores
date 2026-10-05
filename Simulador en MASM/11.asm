TITLE MASM Template						(main.asm)

INCLUDE Irvine32.inc
;---------segmento de datos---------
.data
;tamano de la cache, memoria y disco
tamano1 DWORD ?
tamano2 DWORD ?
tamano3 DWORD ?

;variable para saber si se quiere escribir o leer
escrioleer DWORD 2

;variable que se desea escribir o leer
escribir DWORD ?

;memorias principales
cache dd 20 DUP(?)
memoria dd 20 DUP(?)
disco dd 20 DUP(?)

presentecache DWORD 0
presentememoria DWORD 0
presentedisco DWORD 0

;tiempo
savetime DWORD ?

;Complemento
fallos DWORD 0
aciertos DWORD 0

;mensajes
msg1 BYTE 'Ponga el tamano de la cache(max 20): ',0
msg2 BYTE 'Ponga el tamano de la memoria(max 20): ',0
msg3 BYTE 'Ponga el tamano del disco(max 20): ',0
msg4 BYTE 'Ponga si quiere escribir(0) o leer(1) una direccion: ',0
msg5 BYTE 'Inserte un valor correcto',0
msvali1 BYTE 'Ponga un valor entre 20 y 1',0
msvali2 BYTE 'El valor debe ser mas bajo o igual al del disco',0
msvali3 BYTE 'El valor debe ser mas bajo o igual al de la memoria',0
;mensajes write
msgw1 BYTE 'Ponga el valor que desea escribir: ',0
msgw2 BYTE 'Escrito en cache: ',0
msgw3 BYTE 'Escrito en cache y memoria: ',0
msgw4 BYTE 'Escrito en cache, memoria y disco: ',0
;mensajes read
msgr1 BYTE 'Ponga el valor que desea leer: ',0
msgr2 BYTE 'Leido en cache: ',0
msgr3 BYTE 'Leido en memoria, moviendo cache: ',0
msgr4 BYTE 'Leido en disco, moviendo memoria y cache: ',0
msgr5 BYTE 'No se encontro el valor en la jerarquia',0
;mensajes de imprimir
msgI1 BYTE 'Cache: ',0
msgI2 BYTE 'Memoria: ',0
msgI3 BYTE 'Disco: ',0
msgI4 BYTE 'Tiempo en operaciones realizadas: ',0
msgI5 BYTE 'Aciertos: ',0
msgI6 BYTE 'Fallos: ',0

msg10 BYTE " ----------------------------------------------------------------------------------------------",0dh,0ah,0
msg11 BYTE "|  #####                                      #     #                                          |",0dh,0ah,0
msg12 BYTE "| #     #    ##     ####   #    #  ######     ##   ##  ######  #    #   ####   #####   #     # |",0dh,0ah,0
msg13 BYTE "| #         #  #   #    #  #    #  #          # # # #  #       ##  ##  #    #  #    #   #   #  |",0dh,0ah,0
msg14 BYTE "| #        #    #  #       ######  #####      #  #  #  #####   # ## #  #    #  #    #    # #   |",0dh,0ah,0
msg15 BYTE "| #        ######  #       #    #  #          #     #  #       #    #  #    #  #####      #    |",0dh,0ah,0
msg16 BYTE "| #     #  #    #  #    #  #    #  #          #     #  #       #    #  #    #  #   #      #    |",0dh,0ah,0
msg17 BYTE "|  #####   #    #   ####   #    #  ######     #     #  ######  #    #   ####   #    #     #    |",0dh,0ah,0
msg19 BYTE "|--------------------------------------------------------------------------------------------- ",0dh,0ah,0
msg20 BYTE "| #####                                 #                         | ",0dh,0ah,0
msg21 BYTE "| #     #  #####   #####   #    #       #        ######  #     #  | ",0dh,0ah,0
msg22 BYTE "| #     #    #    #        #  #         #        #    #  #     #  | ",0dh,0ah,0
msg23 BYTE "| #     #    #     #####   ####         #        #    #  #     #  | ",0dh,0ah,0
msg24 BYTE "| #     #    #          #  #  #         #        ######  #     #  | ",0dh,0ah,0
msg25 BYTE "| #     #    #    #     #  #   #        #        #   #   #     #  |",0dh,0ah,0
msg26 BYTE "| #####    #####   #####   #    #       #######  #    #   #####   |",0dh,0ah,0
msg27 BYTE "-------------------------------------------------------------------",0dh,0ah,0
msg68 BYTE "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-",0dh,0ah,0
msg69 BYTE "-----------------------------------------------",0dh,0ah,0
msg70 BYTE "| Ponga los siguientes valores para continuar |",0dh,0ah,0
msg71 BYTE "-----------------------------------------------",0dh,0ah,0
msg72 BYTE "| (0) --> ESCRIBIR una direccion|",0dh,0ah,0
msg73 BYTE "---------------------------------",0dh,0ah,0
msg74 BYTE "| (1) --> LEER una direccion    |",0dh,0ah,0
msg75 BYTE "---------------------------------",0dh,0ah,0
msg76 BYTE "---------------",0dh,0ah,0

;---------segmento de codigo---------
.code

imprimir PROC
    mov edx, OFFSET msg76
    call writestring
    mov edx, OFFSET msgI1;imprimir cache
    call writestring

    mov eax, tamano1
    call writeint

    call Crlf
    mov edx, OFFSET msg76
    call writestring

    mov ecx, 0
    .while (ecx < tamano1)
        mov al,'['
		call writeChar
        mov eax, cache[ecx*4]
        call writeint
        mov al,']'
        call writeChar
        call Crlf
        inc ecx
    .endw

    mov edx, OFFSET msg76
    call writestring
    mov edx, OFFSET msgI2;imprimir memoria
    call writestring

    mov eax, tamano2
    call writeint

    call Crlf
    mov edx, OFFSET msg76
    call writestring

    mov ecx, 0
    .while (ecx < tamano2)
        mov al,'['
		call writeChar
        mov eax, memoria[ecx*4]
        call writeint
        mov al,']'
        call writeChar
        call Crlf
        inc ecx
    .endw

    mov edx, OFFSET msg76
    call writestring
    mov edx, OFFSET msgI3;imprimir disco
    call writestring

    mov eax, tamano3
    call writeint

    call Crlf
    mov edx, OFFSET msg76
    call writestring

    mov ecx, 0
    .while (ecx < tamano3)
        mov al,'['
		call writeChar
        mov eax, disco[ecx*4]
        call writeint
        mov al,']'
        call writeChar
        call Crlf
        inc ecx
    .endw

    mov edx, OFFSET msg75
    call writestring

    mov edx, OFFSET msgI4;imprimir tiempo
    call writestring

    mov eax, savetime
    call writeint

    call Crlf
    mov edx, OFFSET msg75
    call writestring

    mov edx, OFFSET msgI5;imprimir aciertos
    call writestring

    mov eax, aciertos
    call writeint

    call Crlf
    mov edx, OFFSET msg75
    call writestring

    mov edx, OFFSET msgI6;imprimir fallos
    call writestring

    mov eax, fallos
    call writeint

    call Crlf
    mov edx, OFFSET msg75
    call writestring

    call Waitmsg
    call Clrscr
    ret
imprimir ENDP


looper PROC
    mov ecx, 0
    .while(tamano1>ecx)
        mov eax, cache[ecx*4]
        .IF (eax == escribir) ;si la direccion ya esta en la cache
            .while(ecx>0);mover los valores de la cache
                mov ebx, cache[ecx*4-4]
                mov cache[ecx*4], ebx;poner el valor en la siguiente posicion
                sub ecx, 1
            .endw
            mov ebx, escribir
            mov cache[0], ebx;poner el valor en la primera posicion
            mov ecx, tamano1;para salir del while
        .endif
        inc ecx
    .endw
    .IF(presentecache != 1);si no esta en la cache
        mov ecx, tamano1
        sub ecx, 1
        .while(ecx>0);mover los valores de la cache
            mov ebx, cache[ecx*4-4]
            mov cache[ecx*4], ebx;poner el valor en la siguiente posicion
            sub ecx, 1
        .endw
        mov ebx, escribir
        mov cache[0], ebx;poner el valor en la primera posicion
    .ENDIF
    ret
looper ENDP

write PROC
    mov edx, OFFSET msg75
    call writestring
    mov edx, OFFSET msgw1
	call writestring
    call Crlf
    mov edx, OFFSET msg75
    call writestring

    call readint
    mov escribir, eax

    CPUID
    RDTSC            ; read the clock
	push eax         ; save the start time

    mov ecx, 0
    .while(tamano1>ecx)
        mov eax, cache[ecx*4]
        .IF (eax == escribir) ;si la direccion ya esta en la cache
            mov presentecache, 1
            mov ecx, tamano1;para salir del while
        .endif
        inc ecx
    .endw
    mov ecx, 0
    .while(tamano2>ecx)
        mov eax, memoria[ecx*4]
        .IF (eax == escribir) ;si la direccion ya esta en la memoria
            mov presentememoria, 1
            mov ecx, tamano2;para salir del while
        .endif
        inc ecx
    .endw
    mov ecx, 0
    .while(tamano3>ecx)
        mov eax, disco[ecx*4]
        .IF (eax == escribir) ;si la direccion ya esta en el disco
            mov presentedisco, 1
            mov ecx, tamano3;para salir del while
        .endif
        inc ecx
    .endw

    .IF(presentecache == 1);si esta en la cache
        inc aciertos;incrementar aciertos
        call looper
        mov edx, OFFSET msgw2
	    call writestring

    .ELSEIF(presentememoria == 1);si esta en la memoria
        inc fallos;incrementar fallos
        call looper
        mov ecx, 0
        .while(tamano2>ecx)
            mov eax, memoria[ecx*4]
            .IF (eax == escribir) ;si la direccion ya esta en la memoria
                .while(ecx>0);mover los valores de la memoria
                    mov ebx, memoria[ecx*4-4]
                    mov memoria[ecx*4], ebx;poner el valor en la siguiente posicion
                    sub ecx, 1
                .endw
                mov ebx, escribir
                mov memoria[0], ebx;poner el valor en la primera posicion
                mov ecx, tamano2;para salir del while
            .endif
            inc ecx
        .endw

        mov edx, OFFSET msgw3
	    call writestring
    .ELSE
        inc fallos;incrementar fallos
        call looper
        ;mover los valores de la memoria
        mov ecx, tamano2
        sub ecx, 1
        .while(ecx>0)
            mov ebx, memoria[ecx*4-4]
            mov memoria[ecx*4], ebx
            sub ecx, 1
        .endw
        mov ebx, escribir
        mov memoria[0], ebx
        ;mover los valores del disco
        .IF(presentedisco != 1);si no esta en el disco
            mov ecx, tamano3
            sub ecx, 1
            .while(ecx>0);mover los valores del disco
                mov ebx, disco[ecx*4-4]
                mov disco[ecx*4], ebx;poner el valor en la siguiente posicion
                sub ecx, 1
            .endw
            mov ebx, escribir
            mov disco[0], ebx;poner el valor en la primera posicion
        .ENDIF

        mov edx, OFFSET msgw4
	    call writestring

    .ENDIF

    CPUID
    RDTSC             ; get end time
	pop ebx
	sub eax, ebx
    mov savetime, eax

    mov presentedisco, 0
    mov presentememoria, 0
    mov presentecache, 0
    call Crlf

    ;imprimir
    call Waitmsg
    call Clrscr
    call imprimir
    ret
write ENDP

;lecutura

read PROC
    mov edx, OFFSET msg75
    call writestring
    mov edx, OFFSET msgr1
    call writestring
    call Crlf
    mov edx, OFFSET msg75
    call writestring

    call readint
    mov escribir, eax

    CPUID
    RDTSC            ; read the clock
	push eax         ; save the start time

    mov ecx, 0
    .while(tamano1>ecx)
        mov eax, cache[ecx*4]
        .IF (eax == escribir) ;si la direccion ya esta en la cache
            mov presentecache, 1
            mov ecx, tamano1;para salir del while
        .endif
        inc ecx
    .endw
    mov ecx, 0
    .while(tamano2>ecx)
        mov eax, memoria[ecx*4]
        .IF (eax == escribir) ;si la direccion ya esta en la memoria
            mov presentememoria, 1
            mov ecx, tamano2;para salir del while
        .endif
        inc ecx
    .endw
    mov ecx, 0
    .while(tamano3>ecx)
        mov eax, disco[ecx*4]
        .IF (eax == escribir) ;si la direccion ya esta en el disco
            mov presentedisco, 1
            mov ecx, tamano3;para salir del while
        .endif
        inc ecx
    .endw

    .IF(presentecache == 1);si esta en la cache
        inc aciertos;incrementar aciertos
        mov edx, OFFSET msgr2
        call writestring

        call looper

    .ELSEIF(presentememoria == 1);si esta en memoria
        inc fallos;incrementar fallos
        mov edx, OFFSET msgr3
        call writestring

        call looper

    .ELSEIF(presentedisco == 1);si esta en disco
        inc fallos;incrementar fallos
        mov edx, OFFSET msgr4
        call writestring
        ;mover los valores a la cache
        call looper
        ;mover los valores a la memoria
        mov ecx, tamano2
        sub ecx, 1
        .while(ecx>0)
            mov ebx, memoria[ecx*4-4]
            mov memoria[ecx*4], ebx
            sub ecx, 1
        .endw
        mov ebx, escribir
        mov memoria[0], ebx

    .ELSE;si no esta en la jerarquia
        inc fallos;incrementar fallos
        mov edx, OFFSET msgr5
        call writestring
        mov ecx, 0

    .ENDIF

    CPUID
    RDTSC             ; get end time
	pop ebx
	sub eax, ebx
    mov savetime, eax

    mov presentedisco, 0
    mov presentememoria, 0
    mov presentecache, 0
    call Crlf

    call Waitmsg
    call Clrscr
    call imprimir
    ret
read ENDP

main proc

    mov edx,OFFSET msg10            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg11            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg12            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg13            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg14            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg15            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg16            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg17            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg19            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg20            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg21            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg22            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg23            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg24            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg25            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg26            ;Imprimir el texto
    call WriteString
    mov edx,OFFSET msg27            ;Imprimir el texto
    call WriteString
    
    call Waitmsg
    call Clrscr

salto:
    mov edx, OFFSET msg68
    call writestring
    mov edx, OFFSET msg3;imprimir disco
    call writestring
    call Crlf
    mov edx, OFFSET msg68
    call writestring

    call readint
    mov tamano3, eax
    
    .if(eax > 20)
        mov edx, OFFSET msvali1
        call writestring
        call Crlf
        call Waitmsg
        call Clrscr
        JMP salto
    .endif

    mov edx, OFFSET msg68
    call writestring
    mov edx, OFFSET msg2;imprimir memoria
    call writestring
    call Crlf
    mov edx, OFFSET msg68
    call writestring

    call readint
    mov tamano2, eax

    .IF(eax > tamano3)
        mov edx, OFFSET msvali2
        call writestring
        call Crlf
        call Waitmsg
        call Clrscr
        JMP salto
    .endif
    
    mov edx, OFFSET msg68
    call writestring
    mov edx, OFFSET msg1;imprimir cache
	call writestring
    call Crlf
    mov edx, OFFSET msg68
    call writestring

    call readint
    mov tamano1, eax

    .if(eax > tamano2)
        mov edx, OFFSET msvali3
        call writestring
        call Crlf
        call Waitmsg
        call Clrscr
        JMP salto
    .endif

    call Clrscr
	;bucle principal
    .while( escrioleer > 1 )
        mov edx, OFFSET msg69
        call writestring
        mov edx, OFFSET msg70
        call writestring
        mov edx, OFFSET msg71
        call writestring
        mov edx, OFFSET msg72
        call writestring
        mov edx, OFFSET msg73
        call writestring
        mov edx, OFFSET msg74
        call writestring
        mov edx, OFFSET msg75
        call writestring

        call readint
        .IF eax == 0
            call write
        .ELSEIF eax == 1
            call read
        .ELSE
            mov edx, OFFSET msg5
            call writestring
            call Waitmsg
		    call Clrscr
        .endif

    .endw


exit
main endp
end main