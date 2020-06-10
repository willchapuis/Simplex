def gerarMatriz(maxX, maxY):
    matriz = []
    aux = []
    for y in range(0, maxY):
        for x in range(0, maxX):
            aux.append(0)
        matriz.append(aux[:])
        aux.clear()
    return matriz

def montarTabela(numvar, numres, res, b, z):
    tabela = gerarMatriz(((numvar + numres) + 1), (numres + 1))

    ### coloca os valores das variaveis de decisao na tabela
    for y in range(0, (numres + 1)):
        for x in range(0, (numvar + 1)):
            if y < numres and x < numvar:
                tabela[y][x] = res[y][x]
            if y == numres and x < numvar:
                tabela[y][x] = (z[x] * -1)

    ### coloca os valores das folgas e da coluna B na tabela
    for y in range(0, numres):
        tabela[y][numvar + numres] = b[y]
        tabela[y][numvar + y] = 1;

    return tabela

def verificarIteracao(tabela, numvar, numres):
    num = 0
    ### pivo guarda a linha(y) que sai e a coluna(x) que vai entrar
    pivo = [-1, -1]
    for x in range(0, ((numvar + numres) + 1)):
        if (tabela[numres][x] < 0) and (tabela[numres][x] < num):
            num = tabela[numres][x]
            pivo[1] = x
    if num != 0:
        r = 0
        for y in range(0, numres):
            try:
                aux = (tabela[y][numvar + numres] / tabela[y][pivo[1]])
            except Exception:
                continue
            else:
                if (r > aux) or (r == 0):
                    r = aux
                    pivo[0] = y
    return pivo

def iteracao(oldTabela, numvar, numres):
    pivo = verificarIteracao(oldTabela, numvar, numres)
    if pivo[0] == -1:
        return oldTabela
    else:
        novaTabela = gerarMatriz(((numvar + numres) + 1), (numres + 1))

        ### calcula linha do pivo (valor que eu quero da tabela anterior dividido pelo valor do pivo da tabela anterior)
        for x in range(0, ((numvar + numres) + 1)):
            novaTabela[pivo[0]][x] = (oldTabela[pivo[0]][x] / oldTabela[pivo[0]][pivo[1]])

        ### calcula coluna do pivo e as linhas delas (valor da linha do pivo multiplicado pelo valor na coluna do pivo da tabela anterior invertido, mais o valor que eu quero da tabela anterior)
        for y in range(0, (numres + 1)):
            if y != pivo[0]:
                for x in range(0, ((numvar + numres) + 1)):
                    novaTabela[y][x] = ((novaTabela[pivo[0]][x] * (oldTabela[y][pivo[1]] * -1)) + oldTabela[y][x])
        return novaTabela

def calculaColunaBase(tabelas, numvar, numres):
    pivos = []
    base = []                                                               ### lista que vai guardar quem esta na base

    for i in range(numvar, (numvar+numres)):                                ### inicia a base somente com as folgas
        base.append(i)

    for i in range(0, (len(tabelas) - 1)):                                  ### ele pega todos os pivos entre as tabelas e guarda em uma lista chamada pivos
        pivos.append(verificarIteracao(tabelas[i], numvar, numres))

    for i in range(0, (len(pivos) - 1)):                                    ### troca a base de acordo as iterações
        base[pivos[i][0]] = pivos[i][1]

    return base

def calculoVariacao(tabela, numvar, numres, f):
    AR = [0, 0]
    aux = []
    for y in range(0, numres):
        try:
            aux.append(((tabela[y][numvar + numres] / tabela[y][f]) * -1))          # (B/F) * -1
        except Exception:
            continue
        else:
            if aux[len(aux) - 1] > 0 and aux[len(aux) - 1] > AR[0]:
                AR[0] = aux[len(aux) - 1]
            if aux[len(aux) - 1] < 0 and aux[len(aux) - 1] < AR[1]:
                AR[1] = aux[len(aux) - 1]

    return AR

def printaAnalise(analise, numvar, numres):
    maxY = numvar + numres + 1
    colunas = ['Variavel', 'Variavel (Tipo)', 'Inic. (Val)', 'Final (Val)', 'Basica(S/N)', 'Escasso', 'Sobra', 'Uso', 'P. Sombra', 'Custo Redu.', 'Aumentar', 'Reduzir', 'Maximo', 'Minimo']
    for x in range(0, 14):
        if x == 0:
            print(f'[{colunas[x]:^8}]', end=' ')
        else:
            print(f'[{colunas[x]:^11}]', end=' ')
    print()
    print('=*' * 98)
    for y in range(0, maxY):
        if y < numvar:
            var = 'X' + str(y + 1)
        elif y < numvar + numres:
            var = 'F' + str((y - numvar) + 1)
        elif y == numvar + numres:
            var = 'LUCRO'
        print(f'[{var:^8}]', end=' ')
        for x in range(0, 13):
            if (type(analise[y][x]) == float):
                print(f'[{analise[y][x]:^11.2f}]', end=' ')
            elif (type(analise[y][x]) == int):
                print(f'[{analise[y][x]:^11}]', end=' ')
            elif (type(analise[y][x]) == str):
                print(f'[{analise[y][x]:^11}]', end=' ')
        print()
    print()

def analiseSensibilidade(tabelas, numvar, numres):
    analise = gerarMatriz(13, ((numvar + numres) + 1))
    base = calculaColunaBase(tabelas, numvar, numres)
                                                                            ### y será as linhas e x as linhas da tabela sensibilidade
    for y in range(0, ((numvar+numres) + 1)):                               ### Tipo de Variavel
        if y < numvar:
            analise[y][0] = '    Decisao    '
        elif y < numvar+numres:
            analise[y][0] = '     Folga     '
        else:
            analise[y][0] = 'Funcao Objetivo'

    for y in range(0, ((numvar+numres) + 1)):                               ### Valor Inicial
        if y >= numvar and y < numvar + numres:     #   Folgas
            analise[y][1] = tabelas[0][y - numvar][numvar + numres]
        else:
            analise[y][1] = 0

    for y in range(0, ((numvar+numres) + 1)):                               ### Valor Final e Basica(Sim/Nao)
        for i in range(0, len(base)):
            if y == base[i]:                #   Base
                analise[y][2] = tabelas[(len(tabelas)) - 1][i][numvar + numres]
                analise[y][3] = 'Sim'
            if y == numvar + numres:        #   LUCRO
                analise[y][2] = tabelas[(len(tabelas)) - 1][numres][numvar + numres]
                analise[y][3] = 'Sim'
            if analise[y][3] != 'Sim' and i == (len(base) - 1):
                analise[y][2] = 0
                analise[y][3] = 'Nao'


    for y in range(0, ((numvar + numres) + 1)):                             ### Recurso Escasso, Sobra Recurso, Uso Recurso e Preço Sombra
        if y >= numvar and y < numvar + numres:         # Folgas
            if analise[y][2] == 0:      #   Valor final
                analise[y][4] = 'Sim'
                analise[y][5] = 0
            else:
                analise[y][4] = 'Nao'
                analise[y][5] = analise[y][2]
            analise[y][6] = analise[y][1] - analise[y][2]
            analise[y][7] = tabelas[(len(tabelas)) - 1][numres][y]
        else:
            for i in range(4, 8):
                analise[y][i] = '-'

    for y in range(0, ((numvar + numres) + 1)):                             ### Custo Reduzido
        if y < numvar:
            analise[y][8] = tabelas[(len(tabelas)) - 1][numres][y]
        else:
            analise[y][8] = '-'

    for y in range(0, ((numvar + numres) + 1)):                                     ### Calculo de variação de restrições
        if y >= numvar and y < numvar + numres:                     #   Folgas
            AR = calculoVariacao(tabelas[(len(tabelas)) - 1], numvar, numres, y)    ##  Retorna o quanto pode aumentar[0] ou reduzir[1]
            for i in range(9, 13):                                  #   Colunas Aumentar ao Minimo
                if i == 9 or i == 11:                               #   Colunas Aumentar e Maximo
                    if AR[0] == 0:
                        analise[y][i] = 'INF'
                    elif i == 9:
                        analise[y][i] = AR[0]
                    else:
                        analise[y][i] = analise[y][1] + AR[0]
                else:                                               #   Colunas Diminuir e Minimo
                    if AR[1] == 0:
                        analise[y][i] = 'INF'
                    elif i == 10:
                        analise[y][i] = abs(AR[1])                  #   Para nao ficar com o valor negativo
                    else:
                        analise[y][i] = analise[y][1] + AR[1]       #   Somar porque o valor de AR[1] esta negativo oque vai resultar em uma subtração
        else:
            for i in range(9, 13):
                analise[y][i] = '-'

    printaAnalise(analise, numvar, numres)

def printaTabela(matriz, maxX, maxY):
    for y in range(0, maxY):
        for x in range(0, maxX):
            if (type(matriz[y][x]) == float):
                print(f'[{matriz[y][x]:^10.2f}]', end=' ')
            elif (type(matriz[y][x]) == int):
                print(f'[{matriz[y][x]:^10}]', end=' ')
            elif (type(matriz[y][x]) == str):
                print(f'[{matriz[y][x]:^10}]', end=' ')
        print()
    print()

if __name__ == '__main__':
    ### numvar é o numero de variaveis de decisão(produtos)
    ### numres é o numero de restrições
    ### obj é booleano, se a função objetivo é: MIN(false) ou MAX(true)
    ### z é uma lista com os valores de cada variavel na função objetivo
    ### b é uma lista com os valores limites de cada restrição (<=)
    ### res é uma lista com os valores de cada variavel em cada restrição
    ### imp é booleano, pra saber se é uma solução: possivel(false) ou impossivel(true)
    ### result é booleano, se deve apresentar o resultado: final(false) ou passo a passo(true)
    ### iterac é uma lista com as matrizes/tabelas feitas
    ### terminou é booleano, pra saber quando chegou na resposta final(true)

    z = []
    b = []
    res = []
    iterac = []

    numvar = int(input('Digite o numero de variaveis de decisao: '))
    numres = int(input('Digite o numero de restricoes: '))
    print()

    obj = bool(int(input('MAX(1) ou MIN(0) ? ')))
    print()
    print('Funcao Objetivo:')
    for i in range(0, numvar):
        if obj:
            z.append(float(input(f'Digite o valor da variavel X{i + 1}: ')))
        else:
            z.append((float(input(f'Digite o valor da variavel X{i + 1}: '))) * -1)
    print()

    aux = []
    for f in range(0, numres):
        print(f'Restricao {f+1}:')
        for i in range(0, numvar):
            aux.append(float(input(f'Digite o valor da variavel X{i+1}: ')))
        b.append(float(input('Limite da restricao: ')))
        res.append(aux[:])
        aux.clear()
        print()

    imp = False
    for i in range(0, len(b)):
        if b[i] < 0:
            imp = True

    if imp:
        print('Solução Impossivel!')
    else:
        result = bool(int(input('Resultado final(0) ou só Passo a Passo(1) ? ')))
        print()

        ### Tabela Inicial
        iterac.append(montarTabela(numvar, numres, res, b, z))

        ### Iteracoes
        terminou = False
        while (terminou != True):
            iterac.append(iteracao(iterac[len(iterac)-1], numvar, numres))             ### quando nao tem solução melhor retorna a tabela de volta
            if (iterac[len(iterac)-2] == iterac[len(iterac)-1]):                       ### Se for a mesma tabela sai do loop
                terminou = True

        if result:
            print('Solucao basica inicial:')
            printaTabela(iterac[0], (numvar + numres) + 1, (numres + 1))
            input('Pressione qualquer tecla para continuar...')
            print()
            for i in range(1, (len(iterac) -2)):
                print(f'Iteracao {i}:')
                printaTabela(iterac[i], (numvar + numres) + 1, (numres + 1))
                input('Pressione qualquer tecla para continuar...')
                print()
        print('Solucao Final:')
        printaTabela(iterac[len(iterac) - 1], (numvar + numres) + 1, (numres + 1))

        if obj:
            print(f'O maior vaior de Z sera = {iterac[len(iterac)-1][numres][numvar + numres]}')
        else:
            print(f'O menor vaior de Z sera = {iterac[len(iterac) - 1][numres][numvar + numres] * -1}')
        print()

        analisa = bool(int(input('Deseja Analise de Sensibilidade(1) ou Não(0) ? ')))
        if analisa:
            print()
            analiseSensibilidade(iterac, numvar, numres)