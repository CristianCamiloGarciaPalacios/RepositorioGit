class AFPN:
    def __init__(self, estados=None, estadoInicial=None, estadosAceptacion=None, alfabetoCinta=None, alfabetoPila=None, delta=None, nombreArchivo=None):
        if nombreArchivo:
            self.cargar_desde_archivo(nombreArchivo)
        else:
            self.estados = estados
            self.estadoInicial = estadoInicial
            self.estadosAceptacion = estadosAceptacion
            self.alfabetoCinta = alfabetoCinta
            self.alfabetoPila = alfabetoPila
            self.delta = dict(delta)

    def cargar_desde_archivo(self, nombreArchivo):
        self.estados = []
        self.estadoInicial = None
        self.estadosAceptacion = []
        self.alfabetoCinta = []
        self.alfabetoPila = []
        self.delta = {}

        with open(nombreArchivo, 'r') as f:
            lines = f.readlines()

            for i in range(len(lines)):
                if lines[i].strip() == '#states':
                    while lines[i+1].strip() != '#initial':
                        self.estados.append(lines[i+1].strip())
                        i += 1

                if lines[i].strip() == '#initial':
                    self.estadoInicial = lines[i+1].strip()
                    i += 1

                if lines[i].strip() == '#accepting':
                    while lines[i+1].strip() != '#tapeAlphabet':
                        self.estadosAceptacion.append(lines[i+1].strip())
                        i += 1

                if lines[i].strip() == '#tapeAlphabet':
                    while lines[i+1].strip() != '#stackAlphabet':
                        if '-' in lines[i+1].strip():
                            start, end = lines[i+1].strip().split('-')
                            for x in range(ord(start), ord(end) + 1):
                                if chr(x) not in self.alfabetoCinta:
                                    self.alfabetoCinta.append(chr(x))
                        else:
                            x = chr(ord(lines[i+1].strip()))
                            if x not in self.alfabetoCinta:
                                self.alfabetoCinta.append(x)
                        i += 1

                if lines[i].strip() == '#stackAlphabet':
                    while lines[i+1].strip() != '#transitions':
                        if '-' in lines[i+1].strip():
                            start, end = lines[i+1].strip().split('-')
                            for x in range(ord(start), ord(end) + 1):
                                if chr(x) not in self.alfabetoPila:
                                    self.alfabetoPila.append(chr(x))
                        else:
                            x = chr(ord(lines[i+1].strip()))
                            if x not in self.alfabetoPila:
                                self.alfabetoPila.append(x)
                        i += 1
                if lines[i].strip() == '#transitions':
                    i += 1
                    while i < len(lines) and lines[i].strip() != '':
                        source, target = lines[i].strip().split('>')
                        sourceState, sourceLetter, sourceCharacter = source.split(
                            ':')
                        target = target.split(';')
                        if sourceState not in self.delta:
                            self.delta[sourceState] = {}
                        if sourceLetter not in self.delta[sourceState]:
                            self.delta[sourceState][sourceLetter] = {}
                        if sourceCharacter not in self.delta[sourceState][sourceLetter]:
                            self.delta[sourceState][sourceLetter][sourceCharacter] = [
                            ]
                        for transicion in target:
                            self.delta[sourceState][sourceLetter][sourceCharacter].append(transicion.split(
                                ":"))
                        i += 1

    def __str__(self):
        output = "!pda\n"
        output += "#states\n"
        output += "\n".join(sorted(self.estados)) + "\n"
        output += "#initial\n"
        output += str(self.estadoInicial) + "\n"
        output += "#accepting\n"
        output += "\n".join(sorted(self.estadosAceptacion)) + "\n"
        output += "#tapeAlphabet\n"
        i = 0
        while i in range(self.alfabetoCinta.__len__()):
            if i != self.alfabetoCinta.__len__()-1:
                if ord(self.alfabetoCinta[i+1]) == ord(self.alfabetoCinta[i])+1:
                    output += self.alfabetoCinta[i]+"-"
                    while True:
                        if i+1 < self.alfabetoCinta.__len__():
                            if ord(self.alfabetoCinta[i+1]) == ord(self.alfabetoCinta[i])+1:
                                i+=1
                            else:
                                break
                        else:
                            break
            output += self.alfabetoCinta[i]+"\n"
            i += 1
        output += "#stackAlphabet\n"
        i = 0
        while i in range(self.alfabetoPila.__len__()):
            if i != self.alfabetoPila.__len__()-1:
                if ord(self.alfabetoPila[i+1]) == ord(self.alfabetoPila[i])+1:
                    output += self.alfabetoPila[i]+"-"
                    while True:
                        if i+1 < self.alfabetoPila.__len__():
                            if ord(self.alfabetoPila[i+1]) == ord(self.alfabetoPila[i])+1:
                                i+=1
                            else:
                                break
                        else:
                            break
            output += self.alfabetoPila[i]+"\n"
            i += 1
        output += "#transitions\n"
        for estado in self.delta:
            for caracterCinta in self.delta[estado]:
                for caracterPila in self.delta[estado][caracterCinta]:
                    output += f'{estado}:{caracterCinta}:{caracterPila}>'
                    for transicion in self.delta[estado][caracterCinta][caracterPila]:
                        output += f'{transicion[0]}:{transicion[1]};'
                    output = output.rstrip(';')
                    output += '\n'
        return output
    
    def modificarPila(self, pila = [], operacion = '', parametro = ''):
        if operacion != parametro:
            if operacion == '$':
                pila.append(parametro)
            elif parametro == '$':
                pila.pop()
            else:
                pila.pop()
                pila.append(parametro)
    # def procesarCadena(self, cadena = ''):



afpn = AFPN(nombreArchivo='testAFPN.pda')
print(afpn)