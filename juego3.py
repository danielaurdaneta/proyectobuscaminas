from api3 import API_Configuracion
from tablero3 import Tablero
import time
from casilla3 import CasillaMina, CasillaVacia
import os
import json

class Juego:
    def __init__(self):
        self.api = API_Configuracion()
        self.tablero = None
        self.minas_restantes = 0
        self.jugando = False
        self.tiempo_inicio = 0
        self.config_actual = None
        self.jugador_actual = None


    @staticmethod
    def limpiar_pantalla():
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_menu_principal(self):
        """Muestra el menu con opciones principales"""
        self.limpiar_pantalla()
        print("\n" + "═" * 50)
        print(" BUSCAMINAS ".center(50, '★'))
        print("═" * 50)
        print("1. Nueva partida")
        print("2. Ver records")
        print("3. Salir")
        print("═" * 50)

    def mostrar_tablero(self):
        """Muestra el tablero completo con formato mejorado (visualmente)"""
        self.limpiar_pantalla()
        
        print(f"\n{' MINAS RESTANTES: ' + str(self.minas_restantes):<25}", end="")
        print(f"{'TIEMPO: ' + str(self.obtener_tiempo()) + ' segundos':>25}")
        
        print("   " + " ".join(f"{i+1:2}" for i in range(self.tablero.columnas)))
        print("   " + "─" * (self.tablero.columnas * 3 - 1))
        
        for f in range(self.tablero.filas):
            print(f"{f+1:2}│", end="")
            for c in range(self.tablero.columnas):
                casilla = self.tablero.casillas[f][c]
                if casilla.revelada:
                    if isinstance(casilla, CasillaMina):
                        print(" 💣", end="")
                    else:
                        print(f" {casilla.minas_colindantes} " if casilla.minas_colindantes > 0 else " 0 ", end="")
                else:
                    if casilla.marca == 'bandera':
                        print(" 🚩", end="")
                    elif casilla.marca == 'interrogante':
                        print(" ❓", end="")
                    else:
                        print(" ■ ", end="")
            print()

    def mostrar_dificultades(self):
        """Muestra dificultades que conducen a la api"""
        print("\nSeleccione dificultad:")
        for i, (key, value) in enumerate(self.api.dificultad.items(), 1):
            print(f"{i}. {value}")

    # Métodos existentes (modificados para usar los nuevos)
    def iniciar_juego(self, dificultad, jugador):
        self.config_actual = self.api.get_config(dificultad)
        self.jugador_actual = jugador
        self.minas_restantes = self.config_actual["minas"]
        self.tablero = Tablero(
            filas=self.config_actual["filas"],
            columnas=self.config_actual["columnas"],
            cantidad_minas=self.config_actual["minas"]
        )
        self.jugando = True
        self.tiempo_inicio = time.time()
        return self.config_actual
    
    def ejecutar_turno(self, accion, fila, columna):
        """realiza las acciones dentro del juego"""
        if not self.jugando:
            return False
            
        casilla = self.tablero.casillas[fila][columna]
        
        if accion == 'R':  # Revelar
            if self.tablero.casillas[fila][columna].es_bandera():
                print("¡Quita la bandera primero!")
                return False
            self.tablero.revelar_casilla(fila, columna)
                
            if casilla.revelar():
                self.jugando = False
                return "mina"
            
            if isinstance(self.tablero.casillas[fila][columna], CasillaMina):
                return "mina"

            if self.verificar_victoria():
                self.jugando = False
                return "victoria"
                
        elif accion == 'M':  # Marcar
            if casilla.revelada:
                print("No se puede marcar casilla revelada")
                return False    

            while True:
                if self.minas_restantes > 0:
                    tipo_de_marca = input("1.🚩 \n2.❓ \n3. Quitar marca \n4. Volver \n-->")
                    if tipo_de_marca == "1":
                        casilla.marcar('bandera')
                        self.minas_restantes -= 1
                        break
                    elif tipo_de_marca == "2":
                        casilla.marcar('interrogante')
                        self.minas_restantes += 1
                        break
                    elif tipo_de_marca == "3":
                        if casilla.marca is None:
                            print("Opción inválida")
                        else:
                            casilla.quitar_marca()
                            break
                    elif tipo_de_marca == "4":
                        break
                    else:
                        print("Opción inválida")
            
        
        elif accion == "S":
            return False
                
        return False

    def verificar_victoria(self):
        """Si el usuario gano el juego"""
        for fila in self.tablero.casillas:
            for casilla in fila:
                if not isinstance(casilla, CasillaMina) and not casilla.revelada:
                    return False
        return True

    def finalizar_juego(self, victoria):
        """Maneja el final del juego y guarda récords si es victoria"""
            
        self.jugando = False
        tiempo = self.obtener_tiempo()
        
        if victoria == True:
            print(f"\n¡Victoria! Tiempo: {tiempo} segundos")
            self.api.guardar_record(
                jugador=self.jugador_actual,
                tiempo=tiempo,
                config=self.config_actual
            )

        else:
            print("\n¡Has perdido! Una mina explotó.")


    def mostrar_records(self):
        """accediendo al archivo json de los records"""
        self.limpiar_pantalla()
        try:
            with open('records.json', 'r') as f:
                records = json.load(f)
                # Asegurarse que los tiempos son números y ordenar
                records = sorted(records, key=lambda x: float(x['time']))[:3]
        except FileNotFoundError:
            records = []
            print("\nEl archivo de records no existe aún")
        except json.JSONDecodeError:
            records = []
            print("\nError leyendo los records (archivo corrupto)")
        except Exception as e:
            records = []
            print(f"\nError inesperado: {str(e)}")
        
        print("\nMEJORES TIEMPOS")
        print("═" * 50)
        if not records:
            print("No hay records registrados aún")
        else:
            for i, record in enumerate(records, 1):
                # Formatear el tiempo a 2 decimales
                tiempo = float(record['time'])
                print(f"{i}. {record['first_name']} {record['last_name']} - {tiempo:.2f}s - Tablero: {record['config']['filas']}*{record['config']['columnas']} - Minas: {record['config']['minas']}")
        
        input("\nPresione Enter para continuar...")

    def obtener_tiempo(self): 
        """Calcula el tiempo transcurrido"""
        return int(time.time() - self.tiempo_inicio) 


