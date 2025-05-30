from dataclasses import dataclass, field
from typing import List
import itertools

@dataclass
class ResultadoAcceso:
    elemento: int
    costo: int
    nueva_configuracion: List[int]

@dataclass
class ResultadoSecuencia:
    secuencia: List[int]
    costo_total: int
    resultados_acceso: List[ResultadoAcceso] = field(default_factory=list)

@dataclass
class AlgoritmoMTF:
    lista_inicial: List[int]
    lista_actual: List[int] = field(init=False)

    def __post_init__(self):
        self.lista_actual = self.lista_inicial.copy()

    def reiniciar(self):
        self.lista_actual = self.lista_inicial.copy()

    def acceder(self, elemento: int) -> ResultadoAcceso:
        if elemento not in self.lista_actual:
            raise ValueError(f"Elemento {elemento} no está en la lista")

        posicion = self.lista_actual.index(elemento)
        costo = posicion + 1
        self.lista_actual.pop(posicion)
        self.lista_actual.insert(0, elemento)

        return ResultadoAcceso(elemento, costo, self.lista_actual.copy())

    def procesar_secuencia(self, secuencia: List[int], mostrar: bool = True) -> ResultadoSecuencia:
        self.reiniciar()
        resultado = ResultadoSecuencia(secuencia, 0)

        if mostrar:
            print(f"Lista inicial: {self.lista_actual}")
            print("-" * 60)

        for i, solicitud in enumerate(secuencia):
            resultado_acceso = self.acceder(solicitud)
            resultado.resultados_acceso.append(resultado_acceso)
            resultado.costo_total += resultado_acceso.costo

            if mostrar:
                print(f"Solicitud {i+1}: {solicitud}")
                print(f"  Costo: {resultado_acceso.costo}")
                print(f"  Nueva configuración: {resultado_acceso.nueva_configuracion}")
                print("-" * 60)

        if mostrar:
            print(f"\nCosto total de acceso: {resultado.costo_total}")

        return resultado

@dataclass
class AlgoritmoIMTF:
    lista_inicial: List[int]
    lista_actual: List[int] = field(init=False)
    secuencia: List[int] = field(default_factory=list)
    indice_actual: int = field(default=0)

    def __post_init__(self):
        self.lista_actual = self.lista_inicial.copy()

    def reiniciar(self):
        self.lista_actual = self.lista_inicial.copy()
        self.indice_actual = 0

    def establecer_secuencia(self, secuencia: List[int]):
        self.secuencia = secuencia
        self.indice_actual = 0

    def _debe_mover_al_frente(self, elemento: int, posicion: int) -> bool:
        if posicion == 0:
            return False

        inicio = self.indice_actual + 1
        fin = min(inicio + posicion, len(self.secuencia))

        if inicio < len(self.secuencia):
            siguientes = self.secuencia[inicio:fin]
            return elemento in siguientes

        return False

    def acceder(self, elemento: int) -> ResultadoAcceso:
        if elemento not in self.lista_actual:
            raise ValueError(f"Elemento {elemento} no está en la lista")

        posicion = self.lista_actual.index(elemento)
        costo = posicion + 1
        mover = self._debe_mover_al_frente(elemento, posicion)

        if mover:
            self.lista_actual.pop(posicion)
            self.lista_actual.insert(0, elemento)

        self.indice_actual += 1

        return ResultadoAcceso(elemento, costo, self.lista_actual.copy())

    def procesar_secuencia(self, secuencia: List[int], mostrar: bool = True) -> ResultadoSecuencia:
        self.reiniciar()
        self.establecer_secuencia(secuencia)
        resultado = ResultadoSecuencia(secuencia, 0)

        if mostrar:
            print(f"Lista inicial: {self.lista_actual}")
            print("-" * 60)

        for i in range(len(secuencia)):
            solicitud = secuencia[i]
            resultado_acceso = self.acceder(solicitud)
            resultado.resultados_acceso.append(resultado_acceso)
            resultado.costo_total += resultado_acceso.costo

            if mostrar:
                print(f"Solicitud {i+1}: {solicitud}")
                print(f"  Costo: {resultado_acceso.costo}")
                print(f"  Nueva configuración: {resultado_acceso.nueva_configuracion}")
                print("-" * 60)

        if mostrar:
            print(f"\nCosto total de acceso: {resultado.costo_total}")

        return resultado

@dataclass
class ResultadoOptimizacion:
    secuencia: List[int]
    costo: int
    es_minimo: bool

def encontrar_mejor_secuencia(lista_inicial: List[int], longitud: int) -> ResultadoOptimizacion:
    mejor = [lista_inicial[0]] * longitud
    mtf = AlgoritmoMTF(lista_inicial)
    resultado = mtf.procesar_secuencia(mejor, mostrar=False)
    return ResultadoOptimizacion(mejor, resultado.costo_total, True)

def encontrar_peor_secuencia(lista_inicial: List[int], longitud: int) -> ResultadoOptimizacion:
    peor = [lista_inicial[-1]] * longitud
    mtf = AlgoritmoMTF(lista_inicial)
    resultado = mtf.procesar_secuencia(peor, mostrar=False)
    return ResultadoOptimizacion(peor, resultado.costo_total, False)

def main():
    print("=" * 80)
    print("PROYECTO 3 - ALGORITMOS MTF e IMTF")
    print("=" * 80)

    lista = [0, 1, 2, 3, 4]

    print("\n1. ALGORITMO MTF - Primera secuencia")
    print("=" * 80)
    secuencia1 = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
    mtf1 = AlgoritmoMTF(lista)
    resultado1 = mtf1.procesar_secuencia(secuencia1)

    print("\n\n2. ALGORITMO MTF - Segunda secuencia")
    print("=" * 80)
    secuencia2 = [4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4]
    mtf2 = AlgoritmoMTF(lista)
    resultado2 = mtf2.procesar_secuencia(secuencia2)

    print("\n\n3. SECUENCIA DE COSTO MÍNIMO (20 solicitudes)")
    print("=" * 80)
    mejor = encontrar_mejor_secuencia(lista, 20)
    print(f"Mejor secuencia: {mejor.secuencia}")
    print(f"Costo mínimo total: {mejor.costo}")

    print("\n\n4. SECUENCIA DE COSTO MÁXIMO - PEOR CASO (20 solicitudes)")
    print("=" * 80)
    peor = encontrar_peor_secuencia(lista, 20)
    print(f"Peor secuencia: {peor.secuencia}")
    print(f"Costo máximo total: {peor.costo}")

    print("\n\n5. ALGORITMO MTF - Secuencia repetitiva de 2")
    print("=" * 80)
    secuencia5a = [2] * 20
    mtf5a = AlgoritmoMTF(lista)
    resultado5a = mtf5a.procesar_secuencia(secuencia5a)

    print("\n\nSecuencia repetitiva de 3:")
    print("=" * 80)
    secuencia5b = [3] * 20
    mtf5b = AlgoritmoMTF(lista)
    resultado5b = mtf5b.procesar_secuencia(secuencia5b, mostrar=False)
    print(f"Costo total para secuencia de 3's: {resultado5b.costo_total}")

    print("\nPATRÓN OBSERVADO:")
    print("Cuando hay una repetición de 20 elementos del mismo valor:")
    print("- El primer acceso tiene un costo igual a la posición inicial del elemento")
    print("- Los siguientes 19 accesos tienen costo 1")
    print(f"- Para elemento 2: costo = 3 + 19*1 = 22")
    print(f"- Para elemento 3: costo = 4 + 19*1 = 23")

    print("\n\n6. ALGORITMO IMTF - Comparación con MTF")
    print("=" * 80)
    print("\nIMTF con la MEJOR secuencia de MTF:")
    print("-" * 60)
    imtf_mejor = AlgoritmoIMTF(lista)
    resultado_imtf_mejor = imtf_mejor.procesar_secuencia(mejor.secuencia, mostrar=False)
    print(f"Secuencia: {mejor.secuencia}")
    print(f"Costo IMTF: {resultado_imtf_mejor.costo_total}")
    print(f"Costo MTF: {mejor.costo}")
    print(f"Diferencia: {resultado_imtf_mejor.costo_total - mejor.costo}")

    print("\nIMTF con la PEOR secuencia de MTF:")
    print("-" * 60)
    imtf_peor = AlgoritmoIMTF(lista)
    resultado_imtf_peor = imtf_peor.procesar_secuencia(peor.secuencia, mostrar=False)
    print(f"Secuencia: {peor.secuencia}")
    print(f"Costo IMTF: {resultado_imtf_peor.costo_total}")
    print(f"Costo MTF: {peor.costo}")
    print(f"Diferencia: {resultado_imtf_peor.costo_total - peor.costo}")

    print("\n\n" + "=" * 80)
    print("RESUMEN DE RESULTADOS")
    print("=" * 80)
    print(f"1. Costo secuencia 1 (MTF): {resultado1.costo_total}")
    print(f"2. Costo secuencia 2 (MTF): {resultado2.costo_total}")
    print(f"3. Costo mínimo (20 solicitudes): {mejor.costo}")
    print(f"4. Costo máximo (20 solicitudes): {peor.costo}")
    print(f"5. Costo secuencia de 2's: {resultado5a.costo_total}")
    print(f"   Costo secuencia de 3's: {resultado5b.costo_total}")
    print(f"6. IMTF vs MTF:")
    print(f"   - Con mejor secuencia: IMTF={resultado_imtf_mejor.costo_total}, MTF={mejor.costo}")
    print(f"   - Con peor secuencia: IMTF={resultado_imtf_peor.costo_total}, MTF={peor.costo}")

if __name__ == "__main__":
    main()
