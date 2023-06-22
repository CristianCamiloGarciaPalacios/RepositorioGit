from AFD import AFD
from AFN import AFN
from AFPN import AFPN
#from AFN_Lambda import AFN_Lambda
# from AFPD import AFPD
from queue import LifoQueue
from Alfabeto import Alfabeto
# from MT import MT
import ast
import random

class ClasePrueba:
    def __init__(self):
        pass
    
    def probarAFD(self):
        # Crear autómatas AFD
        #afd1 = AFD(nombreArchivo='evenA.DFA')
        #afd1 = AFD(nombreArchivo='evenB.DFA')
        #afd1 = AFD(nombreArchivo='testAFD.DFA')
        afd1 = AFD(nombreArchivo='testAFD2.DFA')

        #afd1 = AFD(afd1.alfabeto,afd1.estados,afd1.estadoInicial,afd1.estadosAceptacion,afd1.delta)
        # Procesar cadenas con y sin detalles
    
        cadena = 'aba'
        resultado_sin_detalles = afd1.procesar_cadena(cadena)
        resultado_con_detalles = afd1.procesar_cadena_con_detalles(cadena)
  
        print(f"\n--Procesamiento sin detalles de la cadena '{cadena}': {resultado_sin_detalles}")
        print(f"\n--Procesamiento con detalles de la cadena '{cadena}': {resultado_con_detalles}")
        # Procesar listas de cadenas
        print("\n--Procesamiento de lista de cadenas\n")
        lista_cadenas = ['aba', 'abbaa', 'abbabaabbbbb']
        nombre_archivo = 'resultados_lista_de_cadenas.txt'
        imprimir_pantalla = True
        afd1.procesarListaCadenas(lista_cadenas, nombre_archivo, imprimir_pantalla)
        
        # Generar archivos
        nombre_archivo1 = 'resultado_con_detalles.txt'
        nombre_archivo2 = 'resultado_sin_detalles.txt'
        afd1.exportar(nombre_archivo1)
        afd1.exportar(nombre_archivo2)
        print("\n--AFD\n")
        print(afd1)
        print("\n--AFD Completitud\n")
        print(afd1.verificarCorregirCompletitud())
        print("\n--AFD Imprimir simplificado\n")
        print(afd1.imprimirAFDSimplificado())
        print("\n--AFD Simplificado\n")
        print(afd1.simplificarAFD())
        
        
   

    def ProbarAFN(self):

        afn1 = AFN(nombreArchivo='AFNTest.txt')
        print("\n--AFN Completo\n")
        print(afn1)
        input()
        print("\n--AFN Simplificado\n")
        print(afn1.imprimirAFNSimplificado())
        input()
        print("\n--AFN estados inaccesibles\n")
        print(afn1.hallarEstadosInaccesibles())
        input()
        print("\n--Exportar AFN\n")
        nombre_archivo1 = 'resultado_exportar.NFA'
        afn1.exportar(nombre_archivo1)
        input()
        alfabeto = Alfabeto(afn1.alfabeto)
        cadena = 'bbaaaac'
        print(f"\nUn procesamiento con detalle de {cadena}\n")
        print(afn1.procesar_cadena_con_detalles(cadena))
        input()
        print(f"\nProcesamientos  posibles de la cadena {cadena}\n")
        afn1.computarTodosLosProcesamientos(cadena)
        input()
        print(f"\nProcesamiento  de lista de cadenas \n")
        lista_cadenas = [alfabeto.generar_cadena_aleatoria(3), alfabeto.generar_cadena_aleatoria(5), alfabeto.generar_cadena_aleatoria(10)]
        nombre_archivo = 'resultados_lista_de_cadenas'
        imprimir_pantalla = True
        afn1.procesarListaCadenas(lista_cadenas, nombre_archivo, imprimir_pantalla)

    def simplificacionAFN(self):
        afn1 = AFN(nombreArchivo='AFNTest.txt')
        print("\n--AFN Simplificado\n")
        print(afn1.imprimirAFNSimplificado())

    def probarAFNtoAFD(self):
        afn1 = AFN(nombreArchivo='AFNTest.txt') 
        print(f"AFN convertido a AFD\n")
        print(afn1.AFNtoAFD())
        input()
        cadena = 'dba'  
        print(f"Procesando cadena con detalle {cadena} convertido a AFD\n")
        print(afn1.procesarCadenaConDetallesConversion(cadena=cadena))
        input()
        print(f"Procesando lista {['aba', 'abbaa', 'dbbcdad']} convertido a AFD\n")
        print(afn1.procesarListaCadenasConversion(listaCadenas=['aba', 'abbaa', 'abbabaabbbbb'], nombreArchivo='resultados_lista_conversion', imprimirPantalla=True))


    def probarComplemento(self):
        afd1 = AFD(nombreArchivo='evenA.DFA')
        afd_complemento = afd1.hallarComplemento()
        print(f"AFD original '{afd1}'\n")
        print(f"\n\nAFD Complemento \n'{afd_complemento}'")

    def probarProductoCartesiano(self):
        # Crear los AFD a partir de los archivos
        afd1 = AFD(nombreArchivo='evenA.DFA')
        afd2 = AFD(nombreArchivo='evenB.DFA')

        # Producto cartesiano con intersección (∩)
        interseccion = afd1.hallarProductoCartesiano(afd1, afd2, 'interseccion')
        print("\n\nProducto Cartesiano con Interseccion:")
        print(interseccion)

        # Producto cartesiano con unión (∪)
        union = afd1.hallarProductoCartesiano(afd1, afd2, 'union')
        print("\n\nProducto Cartesiano con Union:")
        print(union)

        # # Producto cartesiano con diferencia (-)
        diferencia = afd1.hallarProductoCartesiano(afd1, afd2, 'diferencia')
        print("\n\nProducto Cartesiano con Diferencia Simetrica:")
        print(diferencia)

        # Dibujar el AFD resultante del producto cartesiano con intersección (∩)
        print("\n\nDiagrama del Producto Cartesiano de la Diferencia simetrica con la Interseccion:")
        producto_cartesiano = afd1.hallarProductoCartesiano(interseccion, diferencia, 'interseccion')
        print(producto_cartesiano)

    def probarSimplificacion(self):
        afd4 = AFD(nombreArchivo='minTest.DFA')
        print(f"\nAFD original \n")
        print(afd4)
        afd4.simplificarAFD()
        print(f"\nSimplificacion\n")
        print(afd4)
    def generar_cadenas_afn(self,afns):
        #Me gustaría que se generaran cadenas dependiendo del lenguaje de los afns (no todos tienen de lenguaje {a,b}) para poder hacer más pruebas
        cadenas_generadas = []
        for afn in afns:
            for _ in range(1000):
                tamano = random.randint(1, 10)  # Choose the size randomly
                cadena = ''.join(random.choices(['a', 'b'], k=tamano))  # Generate a random string
                print(cadena)
                cadenas_generadas.append(cadena)
        return cadenas_generadas
    
    def validarAFNtoAFD(self):
         afn1 = AFN(nombreArchivo='test1AFN.NFA') 
         afn2 = AFN(nombreArchivo='test2AFN.NFA')  
         afn3 = AFN(nombreArchivo='test3AFN.NFA')
         afn4 = AFN(nombreArchivo='test4AFN.NFA')
         afn5 = AFN(nombreArchivo='test5AFN.NFA')
         afns =[afn1,afn2,afn3,afn4,afn5]
         lista_cadenas = clase_prueba.generar_cadenas_afn(afns)
         afd1 = afn1.AFNtoAFD(imprimirTabla=False)
         afd2 = afn2.AFNtoAFD(imprimirTabla=False)
         afd3 = afn3.AFNtoAFD(imprimirTabla=False)
         afd4 = afn4.AFNtoAFD(imprimirTabla=False)
         afd5 = afn5.AFNtoAFD(imprimirTabla=False)
         print("Procesamiento AFN")
         contador_si_afn, contador_no_afn = afn1.procesarListaCadenas(lista_cadenas, 'resultados_AFN_cedenas_aleatorias.txt')

         print("AFN a AFD")
         afn_afd = afn1.AFNtoAFD()
         contador_si_afd, contador_no_afd = afn_afd.procesarListaCadenas(lista_cadenas, 'resultados_AFNtoAFD_cedenas_aleatorias.txt', True)
         print("Cantidad de cadenas aceptadas AFN :\n", contador_si_afn)
         print("Cantidad de cadenas rechazadas AFN:\n", contador_no_afn)
         print("Cantidad de cadenas aceptadas nuevo AFD :\n", contador_si_afd)
         print("Cantidad de cadenas rechazadas nuevo AFD:\n", contador_no_afd)

    def probarAFPN(self):
        afpn = AFPN(nombreArchivo='testAFPN.pda')
        print(f"\n--AFPN:\n")
        print(afpn)
        input()
        print(f"\n--Exportar AFPN:\n")
        afpn.exportar()
        input()
        print(f"\n--Procesar cadena con detalle AFPN:\n")
        afpn.procesarCadenaConDetalle(cadena="baabba")
        print('\n')
        afpn.procesarCadenaConDetalle(cadena="baaa")
        input()
        print(f"\n--Computar todos los procesamientos AFPN:\n")
        afpn.computarTodosLosProcesamientos(cadena="baabba", nombreArchivo='Todos los procesamientos AFPN')
        input()
        print(f"\n--Procesar lista cadenas AFPN:\n")
        afpn.procesarListaCadenas(listaCadenas=['', 'babab', 'abbbaa'])
        input()
        print(f"\n--Producto carteciano AFPN con AFD:\n")
        afd = AFD(nombreArchivo='testAFD.DFA')
        print(afpn.hallarProductoCartesianoConAFD(afd=afd))


    # def probarAFNLambda(self):
    # # Crear autómatas AFN-λ
    #     #firstAFNL = AFN_Lambda(nombreArchivo="firstAFNLtest.NFE")
    #     secondAFNL = AFN_Lambda(nombreArchivo="secondAFNLtest.NFE")
    #     lambdaClosureAFNL = AFN_Lambda(nombreArchivo="lambdaClausuraTest.NFE")
    #     #toStringTestAFNL = AFN_Lambda(nombreArchivo="toStringTestAFNL")

    #     # Calcular la λ-clausura de un estado
    #     lambdaClosureState = lambdaClosureAFNL.calcularLambdaClausura(states=['s0'])
    #     print("Lambda clausura de 's0':", lambdaClosureState)

    #     # Calcular la λλ-clausura de un conjunto de estados
    #     lambdaClosureStates = lambdaClosureAFNL.calcularLambdaClausura(states=["s0", "s3"])
    #     print("Lambda clausura de ['s0', 's3']:", lambdaClosureStates)
        
    #     # Procesar cadenas mostrando solo un procesamiento de aceptación
    #     print("Procesamiento de '01112012' en secondAFNL:")
    #     result = secondAFNL.procesarCadena("01112012", True)
    #     print("Aceptada:", result)

    #     # Procesar cadenas mostrando todos los procesamientos posibles
    #     print("Procesar cadenas mostrando todos los procesamientos posibles en AFN-λ")
    #     result = secondAFNL.procesarCadenaConDetalles("102")
    #     print("Aceptada:", result)

    #     # # Consultar los procesamientos de aceptación, abortados y de rechazo
    #     print("Consultar los procesamientos de aceptación, abortados y de rechazo AFN-λ")
    #     result = secondAFNL.procesarCadena("2")
    #     print("Aceptada:", result)

    #     # # Procesar listas de cadenas
    #     # cadenas = ["0111012", "2", "11"]
    #     # for cadena in cadenas:
    #     #     print("Procesamiento de", cadena, "en secondAFNL:")
    #     #     result = secondAFNL.procesarCadena(cadena, True)
    #     #     print("Aceptada:", result)

    #     # # Generar archivos
    #     # with open("toStringTestAFNL.NFE", "w") as file:
    #     #     file.write(toStringTestAFNL.__str__())

    # def probarAFPD(self):
    #     afpd1 = AFPD(nombreArchivo='AFPD_Test.txt')
    #     alfabeto = Alfabeto(afpd1.alfabetoCinta)
    #     cadena = alfabeto.generar_cadena_aleatoria(5)
    #     print("Procesamiento con detalle\n")
    #     afpd1.procesarCadenaConDetalles(cadena)
    #     print("Procesamiento de lista de cadenas\n")
    #     afpd1.procesarListaCadenas([alfabeto.generar_cadena_aleatoria(7),alfabeto.generar_cadena_aleatoria(2),alfabeto.generar_cadena_aleatoria(3)], "ResultadosAFPD.txt", True)
    
    # def probarAFPDProductoCartesianoAFD(self):
    #     afd1 = AFD(nombreArchivo='AFDParAParB.txt')
    #     afpd2 = AFPD(nombreArchivo='AFPD_Test.txt')
        
    #     #print(afd1.alfabeto,afpd2.alfabetoCinta)
    #     #print(afpd2.delta)
    #     afd_resultado = afpd2.hallarProductoCartesiano(afd1, afpd2, 'Y')
    #     print(afd_resultado)

    # def probarMT(self):
    #     #prueba usando TM de palindromes pares

    #     Turing = MT(nombreArchivo="MT.tm")  
    #     print(Turing.procesarCadenaConDetalles("ababa"))
    #     print(Turing.procesarCadena("ababa"))
    #     print(Turing.procesarFuncion("aabbaa"))
    #     Turing.procesarListaCadenas(["aaaa", "aabbaa", "ababa"], "resultadosTM.txt", True)
    #     print(Turing)
        
# Llamar a la función para probar el producto cartesiano

# Crear instancia de la clase ClasePrueba y ejecutar los método correspondiente
clase_prueba = ClasePrueba()
#-------------AFD-----------------
#clase_prueba.probarAFD()
#clase_prueba.probarComplemento()
#clase_prueba.probarSimplificacion()
#clase_prueba.probarProductoCartesiano()
#-------------AFN-----------------
# clase_prueba.ProbarAFN()
# input()
# clase_prueba.probarAFNtoAFD()
# clase_prueba.validarAFNtoAFD() #validacion con mas de 5000 cadenas

#------------AFNL--------------


#------------
#clase_prueba.probarProductoCartesiano()
#clase_prueba.probarSimplificacion()

#------------AFNL--------------


#clase_prueba.probarAFNLambda()
#-------------AFPD-----------------
#clase_prueba.probarAFPD()

#clase_prueba.probarAFPDProductoCartesianoAFD()

# clase_prueba.probarAFPDProductoCartesianoAFD()
#-------------AFPN-----------------
clase_prueba.probarAFPN()
#--------------MT------------------
#clase_prueba.probarMT()

#clase_prueba.probarAFPDProductoCartesianoAFD()
