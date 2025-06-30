from juego3 import Juego


def main():
    juego = Juego()

    while True:
        juego.mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            # Lógica para nueva partida
            nombre = input("\nIngrese su nombre: ").strip()
            apellido = input("Ingrese su apellido: ").strip()
            juego.jugador_actual = f"{nombre} {apellido}"
            
            juego.mostrar_dificultades()
            while True:
                try:
                    opcion = int(input("\nSeleccione dificultad (1-4): "))
                    dificultades = list(juego.api.dificultad.keys())
                    if 1 <= opcion <= 4:
                        juego.iniciar_juego(dificultades[opcion-1], juego.jugador_actual)
                        break
                    print("¡Opción inválida!")
                except ValueError:
                    print("Ingrese un número válido")
            
            # Bucle principal del juego
            while juego.jugando:
                juego.mostrar_tablero()
                
                try:
                    while True:
                        fila = int(input("\nFila (1-{}): ".format(juego.tablero.filas))) -1
                        if fila + 1 <= juego.tablero.filas and fila + 1 > 0:
                            break
                        else:
                            print("Fila fuera de los limites, ingrese otro numero")

                    while True:
                        col = int(input("Columna (1-{}): ".format(juego.tablero.columnas)))-1 
                        if col + 1 <= juego.tablero.columnas and col + 1 > 0:
                            break
                        else:
                            print("Columna fuera de los limites, ingrese otro numero")
                    

                    
                    accion = input("Acción (R: Revelar, M: Marcar, S: Salir): ").upper()
                    
                    resultado = juego.ejecutar_turno(accion, fila, col)
                    
                    if resultado == "mina":
                        juego.mostrar_tablero()
                        print("\n¡BOOM! ¡Has perdido!")
                        juego.finalizar_juego(False)
                        input("\nPresione Enter para continuar...")
                        break
                        
                    elif resultado == "victoria":
                        juego.mostrar_tablero()
                        print("\n¡FELICIDADES! ¡Has ganado!")
                        juego.finalizar_juego(True)
                        input("\nPresione Enter para continuar...")
                        break
                        
                except ValueError:
                    print("Ingrese valores válidos")
                    continue
                    
        elif opcion == '2':
            juego.mostrar_records()
        elif opcion == '3':
            print("¡Gracias por jugar!")
            break
        else:
            print("Opción no válida")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()