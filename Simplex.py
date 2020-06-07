def gerarTabela(numvar,numres):
    tabela = []
    aux = []
    for y in range(0, (numres + 1)):
        for x in range(0, ((numvar + numres) + 1)):
            aux.append(0)
        tabela.append(aux[:])
        aux.clear()
    return tabela

def montarTabela(numvar, numres, res, b, z):
    tabela = gerarTabela(numvar, numres)

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
    ### pivo guarda a linha(y) que entra e a coluna(x) que sai
    pivo = [-1, -1]
    for x in range(0, ((numvar + numres) + 1)):
        if (tabela[numres][x] < 0) and (tabela[numres][x] < num):
            num = tabela[numres][x]
            pivo[1] = x
    if num != 0:
        try:
            r = (tabela[0][numvar + numres] / tabela[0][pivo[1]])
        except Exception as erro:
            print(f'Problema {erro.__class__} na linha 39')
        else:
            pivo[0] = 0
            for y in range(0, numres):
                try:
                    aux = (tabela[y][numvar + numres] / tabela[y][pivo[1]])
                except Exception as erro:
                    continue
                    # print(f'Problema {erro.__class__} na linha 46')
                else:
                    if (r > aux):
                        r = aux
                        pivo[0] = y
    return pivo

def iteracao(oldTabela, numvar, numres):
    pivo = verificarIteracao(oldTabela, numvar, numres)
    if pivo[0] == -1:
        return oldTabela
    else:
        novaTabela = gerarTabela(numvar,numres)

        ### calcula linha do pivo (valor que eu quero da tabela anterior dividido pelo valor do pivo da tabela anterior)
        for x in range(0, ((numvar + numres) + 1)):
            novaTabela[pivo[0]][x] = (oldTabela[pivo[0]][x] / oldTabela[pivo[0]][pivo[1]])

        ### calcula coluna do pivo e as linhas delas (valor da linha do pivo multiplicado pelo valor na coluna do pivo da tabela anterior invertido, mais o valor que eu quero da tabela anterior)
        for y in range(0, (numres + 1)):
            if y != pivo[0]:
                for x in range(0, ((numvar + numres) + 1)):
                    novaTabela[y][x] = ((novaTabela[pivo[0]][x] * (oldTabela[y][pivo[1]] * -1)) + oldTabela[y][x])
        return novaTabela

def printaTabela(tabela, numvar, numres):
    for y in range(0, (numres +1)):
        for x in range(0, ((numvar+numres)+1)):
            print(f'[{tabela[y][x]:.2f}]', end='')
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
    if obj != True:
        zOriginal = []
    for i in range(0, numvar):
        if obj:
            z.append(float(input(f'Digite o valor da variavel X{i + 1}: ')))
        else:
            zOriginal.append(float(input(f'Digite o valor da variavel X{i + 1}: ')))
            z.append(zOriginal[i] * -1)
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
            printaTabela(iterac[0], numvar, numres)
            for i in range(1, (len(iterac) -2)):
                print(f'Iteracao {i}:')
                printaTabela(iterac[i], numvar, numres)
        print('Solucao Final:')
        printaTabela(iterac[len(iterac)-1], numvar, numres)