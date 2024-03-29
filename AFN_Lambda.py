from queue import LifoQueue
from AFN import AFN

class AFN_Lambda:
    def __init__(self, alfabeto=None, estados=None, estadoInicial=None, estadosAceptacion=None, delta=None,
                 nombreArchivo=None):
        if nombreArchivo:
            self.cargarDesdeArchivo(nombreArchivo)

        else:
            self.alfabeto = alfabeto
            self.estados = estados
            self.estadoInicial = estadoInicial
            self.estadosAceptacion = estadosAceptacion
            self.delta = delta
            self.estadosLimbo = []
            self.estadosInaccesibles = []

            self.estadosInaccesibles = self.hallarEstadosInaccesibles()
            for estado in self.delta:
                if len(self.delta.get(estado)) == 0:
                    self.estadosLimbo.append(estado)


    def cargarDesdeArchivo(self, nombreArchivo):
        self.alfabeto = []
        self.estados = []
        self.estadoInicial = None
        self.estadosAceptacion = []
        self.delta = {}
        self.estadosInaccesibles = []
        self.estadosLimbo = []

        with open(nombreArchivo, 'r') as f:
            lines = f.readlines()

            for i in range(len(lines)):
                if lines[i].strip() == '#alphabet':
                    current = lines[i+1]
                    j = i+1
                    while current.strip() != "#states":
                        if current.strip().__contains__("-"):
                            start, end = current.split('-')
                            start = start.strip()
                            end = end.strip()
                            lettersRange = [chr(x) for x in range(ord(start), ord(end)+1)]
                            for letter in lettersRange:
                                self.alfabeto.append(letter)
                        else:
                            self.alfabeto.append(current.strip())
                        j += 1
                        current = lines[j].strip()

                if lines[i].strip() == '#states':
                    while lines[i + 1].strip() != '#initial':
                        self.estados.append(lines[i + 1].strip())
                        i += 1

                if lines[i].strip() == '#initial':
                    self.estadoInicial = lines[i + 1].strip()
                    i += 1

                if lines[i].strip() == '#accepting':
                    while lines[i + 1].strip() != '#transitions':
                        self.estadosAceptacion.append(lines[i + 1].strip())
                        i += 1

                if lines[i].strip() == '#transitions':
                    # Primero, llenaremos cada índice de delta con diccionarios
                    for estado in self.estados:
                        self.delta.update({estado: {}})

                    while i < len(lines) and lines[i + 1].strip() != '':
                        source, letter = lines[i + 1].strip().split(':')
                        letter, targets = letter.split('>')

                        if ';' not in targets:
                            self.delta[source][letter] = targets
                        else:
                            targets = targets.split(';')
                            self.delta[source][letter] = targets
                        i += 1

            self.estadosInaccesibles = self.hallarEstadosInaccesibles()
            for estado in self.delta:
                if len(self.delta.get(estado)) == 0:
                    self.estadosLimbo.append(estado)


    def __str__(self):
        output = self.imprimirAFNLSimplificado()

        output += _simplePrintIteration(self.estadosInaccesibles, '#inaccesible')
        output += _simplePrintIteration(self.estadosLimbo, '#limbo')

        return output

    def imprimirAFNLSimplificado(self):
        output = '#!nfe\n'

        output += _simplePrintIteration(self.alfabeto, '#alphabet')
        output += _simplePrintIteration(self.estados, '#states')
        output += '#initial \n' + self.estadoInicial + '\n'
        output += _simplePrintIteration(self.estadosAceptacion, '#accepting')

        output += '#transitions \n'
        for estado in self.delta:
            transitions = self.delta.get(estado)
            listOfTransitions = list(transitions.items())

            for transition in listOfTransitions:
                target = transition[1]
                if type(target) == list:
                    auxTarget = target.copy()
                    target = ""
                    for i in range(0, len(auxTarget)):
                        target += auxTarget[i] + ";"
                    target = target.removesuffix(';')

                output += estado + ":" + transition[0] + ">" + target + "\n"

        return output

    def _simplePrintIteration(self, listToPrint: list[str], title: str) -> bool:  # Para ahorrarnos unas líneas de código en los métodos de imprimir el autómata
        output = title + '\n'
        for obj in listToPrint:
            output += obj + '\n'
        return output

    def exportar(self, nombreArchivo):
        with open(nombreArchivo, 'w') as f:
            f.write(str(self))

    def hallarEstadosInaccesibles(self) -> list[str]:
        isAccesible = {}
        for estado in self.estados:
            isAccesible.update({estado: False})
        stack = LifoQueue()
        currentState = self.estadoInicial

        allInaccesibleFound = False
        while not allInaccesibleFound:

            isAccesible[currentState] = True
            newAccesibleStates = []
            stateDelta = self.delta[currentState]
            targets = list(stateDelta.values())  # Hallamos los estados a los que hay transiciones desde este estado

            for target in targets:
                if type(target) == list:  # Si se trata de una lista de estados, se deben individualizar
                    for individualState in target:
                        newAccesibleStates.append(individualState)
                else:
                    newAccesibleStates.append(target)
            newAccesibleStates = list(dict.fromkeys(newAccesibleStates))

            for accesibleState in newAccesibleStates:
                if not isAccesible[accesibleState]:
                    stack.put(accesibleState)

            currentState = stack.get() if not stack.empty() else None  # Desapilamos
            allInaccesibleFound = True if currentState is None else False  # No hay más estados por recorrer

        inaccesibleStates = [state for state in isAccesible if not isAccesible[state]]
        # self.estadosInaccesibles = inaccesibleStates
        return inaccesibleStates

    def calcularLambdaClausura(self, st: str = None, states: list[str] = None):
        if st is not None and states is not None:
            print("Para calcular la lambda clausura, pasar, o solo un estado, o solo un conjunto de estados")

        if st is not None:
            states = [st]

        lambdaClosure = states.copy()  # Los estados mismos pertenecen a su lambda clausura
        for sta in states:
            stack = LifoQueue()

            currentState = sta
            allStatesFound = False
            while not allStatesFound:
                transitions = self.delta.get(currentState)
                lambdaStates = transitions.get('$')

                if lambdaStates is not None:
                    if type(lambdaStates) is not list:
                        lambdaStates = [lambdaStates]
                    for targetState in lambdaStates:
                        if not lambdaClosure.__contains__(targetState):
                            lambdaClosure.append(targetState)
                            stack.put(targetState)

                currentState = stack.get() if not stack.empty() else None
                allStatesFound = True if currentState is None else False

        return lambdaClosure

    def procesarCadena(self, cadena: str, toPrint=False) -> bool:
        for character in cadena:
            if character not in self.alfabeto:
                raise Exception("En la cadena se introdujo el carácter " + character + ", pero ese "  
                                "carácter no existe en el alfabeto del autómata: " + self.alfabeto.__str__())

        if toPrint:
            print(cadena + ":")

        noTransitionsFrom = self.estadosLimbo.copy()

        exploringStack = LifoQueue()
        printStack = LifoQueue()

        currentState = self.estadoInicial
        index = -1
        transitionsDone = 0

        stringAccepted = False
        searchFinished = False

        while not searchFinished:
            if currentState in self.estadosAceptacion and index+1 == len(cadena):
                stringAccepted = True
                searchFinished = True
            elif (currentState in noTransitionsFrom or index+1 == len(cadena)) and exploringStack.empty():
                stringAccepted = False
                searchFinished = True
            elif currentState in noTransitionsFrom or index+1 == len(cadena):
                phase = exploringStack.get()
                currentState = phase[2]
                index = phase[3]
                previousTransitionsDone = transitionsDone
                transitionsDone -= phase[4]
                for popTransition in range(0, previousTransitionsDone-transitionsDone):
                    printStack.get()
                previousState = phase[0]
                charToCurrentState = phase[1]
                printStack.put("(" + previousState + "," + charToCurrentState + ") --> " + currentState)
            else:
                currentChar = cadena[index+1]

                def pushIntoList(stateList, char):
                    if stateList is not None:
                        if type(stateList) is not list:
                            stateList = [stateList]
                        for st in stateList:
                            exploringStack.put([currentState, char, st, index, transitionsDone])

                transitions = self.delta.get(currentState)
                lambdaStates, charStates = transitions.get('$'), transitions.get(currentChar)

                pushIntoList(lambdaStates, '$')
                pushIntoList(charStates, currentChar)

                if exploringStack.empty():
                    noTransitionsFrom.append(currentState)
                else:
                    phase = exploringStack.get()
                    previousState = phase[0]
                    charToCurrentState = phase[1]
                    currentState = phase[2]

                    printStack.put("(" + previousState + "," + charToCurrentState + ") --> " + currentState)

                    index = phase[3]+1 if charToCurrentState != '$' else phase[3]
                    transitionsDone = phase[4]+1

        if toPrint:
            auxStack = LifoQueue()
            while not printStack.empty():
                auxStack.put(printStack.get())
            while not auxStack.empty():
                print(auxStack.get())

        return stringAccepted


    def procesarCadenaConDetalles(self, cadena: str) -> bool:
        return self.procesarCadena(cadena=cadena, toPrint=True)

    def AFN_LambdaToAFN(self):

        newDelta = {}  # El delta del nuevo autómata

        for estado in self.estados:
            # Primer paso: calcular la lambda clausura
            lambdaClosure = self.calcularLambdaClausura(estado)

            deltaState = {}  # Aquí guardaremos el delta del estado particular

            for character in self.alfabeto:
                # Segundo paso: calcular el delta de cada estado de la lambda clausura con el carácter
                if character != '$':
                    intermediateStates = []

                    for state in lambdaClosure:
                        targets = self.delta[state]
                        if character in targets:
                            target = targets[character]
                            if type(target) is list:
                                for subTarget in target:
                                    intermediateStates.append(subTarget)
                            else:
                                intermediateStates.append(target)

                    if len(intermediateStates) != 0:
                        # Tercer paso: calcular la lambda clausura de ese conjunto de estados:
                        targets = self.calcularLambdaClausura(states=intermediateStates)

                        # Cuarto paso: unir este nuevo target al delta de este estado con este carácter.
                        if len(targets) > 0:
                            deltaState[character] = targets[0] if len(targets) == 1 else targets

            newDelta[estado] = deltaState

        # print(self.delta)
        # print(newDelta)

        pass






'''
firstAFNL = AFN_Lambda(nombreArchivo="firstAFNLtest.NFE")

print(firstAFNL.alfabeto)
print(firstAFNL.estados)
print(firstAFNL.estadoInicial)
print(firstAFNL.estadosAceptacion)
print(firstAFNL.delta)
print(firstAFNL.hallarEstadosInaccesibles())

print('\n')
print(firstAFNL.__str__())
'''

secondAFNL = AFN_Lambda(nombreArchivo="secondAFNLtest.NFE")
secondAFNL.AFN_LambdaToAFN()
# print(secondAFNL.procesarCadena("0111012", True))
# print(secondAFNL.procesarCadena("2", True))
# print(secondAFNL.procesarCadena("11", True))
#print(secondAFNL.procesarCadena("102", True))

# print(secondAFNL.__str__())
# print(secondAFNL.imprimirAFNLSimplificado())
# secondAFNL.exportar("HolaMundo.nfe")

'''
print(secondAFNL.alfabeto)
print(secondAFNL.estados)
print(secondAFNL.estadoInicial)
print(secondAFNL.estadosAceptacion)
print(secondAFNL.delta)
print(secondAFNL.hallarEstadosInaccesibles())
'''

# print(secondAFNL.calcularLambdaClausura(states=['s0', 's6']))


#lambdaClosureAFNL = AFN_Lambda(nombreArchivo="lambdaClausuraTest.NFE")
'''
print(lambdaClosureAFNL.alfabeto)
print(lambdaClosureAFNL.estados)
print(lambdaClosureAFNL.estadoInicial)
print(lambdaClosureAFNL.estadosAceptacion)
print(lambdaClosureAFNL.delta)
print(lambdaClosureAFNL.hallarEstadosInaccesibles())
'''

'''
for state in lambdaClosureAFNL.estados:
    print(state + ":")
    print(lambdaClosureAFNL.calcularLambdaClausura(st=state))

print(lambdaClosureAFNL.calcularLambdaClausura(states=['s0', 's3']))
print(lambdaClosureAFNL.calcularLambdaClausura(states=['s5', 's6']))
'''

# toStringTestAFNL = AFN_Lambda(nombreArchivo="toStringTestAFNL")
# print(toStringTestAFNL.__str__())
