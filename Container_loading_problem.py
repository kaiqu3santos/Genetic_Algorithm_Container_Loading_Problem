from vpython import *

from random import choice
import random

listaCaixas = []

def inputBox(position,cor):
  listaCaixas.append(box (pos=position, size=vector(120, 120, 120),  color = cor))

cor = [color.red,color.green,color.magenta,color.purple,
      color.blue,color.orange,color.cyan,color.white]
      
posicoesCais = {
            'a10': (vector(-10,130,42)),'a11': (vector(120,130,42)),'a12': (vector(250,130,42)),
            'a13': (vector(-10,130,165)),'a14': (vector(120,130,165)),'a15': (vector(250,130,165)),
            'a16': (vector(-10,130,290)),'a17': (vector(120,130,290)),'a18': (vector(250,130,290)),
            'a1': (vector(-10,10,42)),'a2': (vector(120,10,42)),'a3': (vector(250,10,42)),
            'a4': (vector(-10,10,165)),'a5': (vector(120,10,165)),'a6': (vector(250,10,165)),
            'a7': (vector(-10,10,290)),'a8': (vector(120,10,290)),'a9': (vector(250,10,290))}
posicoesBalsa = {'a10': (vector(-50,170,-350)),'a11': (vector(80,170,-350)),'a12': (vector(210,170,-350)),
            'a13': (vector(-50,170,-225)),'a14': (vector(80,170,-225)),'a15': (vector(210,170,-225)),
            'a16': (vector(-50,170,-100)),'a17': (vector(80,170,-100)),'a18': (vector(210,170,-100)),
            'a1': (vector(-50,55,-350)),'a2': (vector(80,55,-350)),'a3': (vector(210,55,-350)),
            'a4': (vector(-50,55,-225)),'a5': (vector(80,55,-225)),'a6': (vector(210,55,-225)),
            'a7': (vector(-50,55,-100)),'a8': (vector(80,55,-100)),'a9': (vector(210,55,-100))}

def start(lista):
  def moveY(o,v):
      while o.pos.y !=posicoesBalsa['a'+v].y:
        rate(300)
        if o.pos.y >=posicoesBalsa['a'+v].y:
          o.pos.y -=1
        else:
          o.pos.y +=1
  def moveX(o,v):
    while o.pos.x !=posicoesBalsa['a'+v].x:
      rate(300)
      if o.pos.x >=posicoesBalsa['a'+v].x:
          o.pos.x -=1
      else:
          o.pos.x +=1
  def moveZ(o,v):
    while o.pos.z !=posicoesBalsa['a'+v].z:
      rate(300)
      if o.pos.z >=posicoesBalsa['a'+v].z:
          o.pos.z -=1
      else:
          o.pos.z +=1
  
  n = 0
  for i in range(len(lista)):
    while listaCaixas[n].pos.y <=320:
      rate(300)
      listaCaixas[i].pos.y +=1
    moveX(listaCaixas[i],str(lista[i]))
    moveZ(listaCaixas[i],str(lista[i]))
    moveY(listaCaixas[i],str(lista[i]))
    n+=1

def gerarIndividuo(base):
    individuo = base.copy()
    random.shuffle(individuo)
    return individuo


def novaGeracao(quantIndividuos, geracaoAnterior=[]):
    global melhorIndividuo
    geracao = []
    if not geracaoAnterior:
        base = list(range(1,19))
        for i in range(quantIndividuos):
            individuo = gerarIndividuo(base)
            fit = fitness(individuo)
            if not validarCromossomo(individuo):
                fit //= 2
            geracao.append([individuo, fit])

            if fit > melhorIndividuo[1]:
                melhorIndividuo = [individuo, fit]

    else:
        for i in range(quantIndividuos):
            pai1 = selecionarIndividuo(geracaoAnterior)
            pai2 = selecionarIndividuo(geracaoAnterior)
            filho = cruzamento(pai1,pai2)
            fit = fitness(filho)
            if not validarCromossomo(filho):
                fit //= 2
            geracao.append([filho, fit])

            if fit > melhorIndividuo[1]:
                melhorIndividuo = [filho, fit]

    return geracao


def selecionarIndividuo(geracao):
    soma = 0
    for individuo in geracao:
        soma += individuo[1]

    numero = random.randint(1, soma)

    for i in range(len(geracao)):
        numero -= geracao[i][1]
        if numero <= 0:
            return geracao[i][0]


def cruzamento(individuo1, individuo2):
    corte = random.randint(1,17)

    novoindividuo = individuo1[:corte]
    for i in range(18):
        if individuo2[i] not in novoindividuo:
            novoindividuo.append(individuo2[i])

    ProbMutacao = random.randint(1,100)
    if ProbMutacao <= 15:
        gene1 = random.randint(0,17)
        gene2 = random.randint(0,17)
        novoindividuo[gene1], novoindividuo[gene2] = novoindividuo[gene2], novoindividuo[gene1]
    return novoindividuo


def validarCromossomo(cromossomo):
    lista = []
    for i in range(18):
        gene = cromossomo[i]
        if gene < 10:
            lista.append(gene)
        else:
            if (gene-9) not in lista:
                return False
    return True


def fitness(cromossomo):
    class Balsa:
        def __init__(self):
            self.matrix = [[[0,0] for i in range(3)] for i in range(3)]
            self.quantidade = 0

        def addContainer(self, posi):
            i = (posi-1)//3 % 3
            j = (posi-1) % 3
            k = (posi-1)//9

            self.matrix[i][j][k] = 1
            self.quantidade += 1
                
        def calcExcentricity(self):
            coordenadas = [0, 0, 0]
            centroDeMassaInicial = [1, 1, 0]
            modDiferençaVetorial = 0
            for i in range(3):
                for j in range(3):
                    for k in range(2):
                        if self.matrix[i][j][k] == 1:
                            coordenadas[0] += i
                            coordenadas[1] += j
                            coordenadas[2] += k
            for i in range(3):
                coordenadas[i] /= self.quantidade
                modDiferençaVetorial += (centroDeMassaInicial[i] - coordenadas[i])**2
            
            return (modDiferençaVetorial)**(1/2)
        
    balsa = Balsa()
    excentricidades = []
    for i in cromossomo:
        balsa.addContainer(i)            
        excentricidades.append(balsa.calcExcentricity())
        
            
    return int((1 / sum(excentricidades))*100000)
try:
    quantIndividuos = 100
    quantGeracoes = 1000

    melhorIndividuo = [[],0]
    geracoes = []
    geracoes.append(novaGeracao(quantIndividuos))
    for i in range(quantGeracoes - 1):
        geracoes.append(novaGeracao(quantIndividuos, geracaoAnterior=geracoes[-1]))

    print(melhorIndividuo)
    scene = canvas(title='Melhor sequência: '+str(melhorIndividuo[0]),
     width=1000, height=600,
     center=vector(5,10,-50))
    
    porto = box (pos=vector(100,-120,180), size=vector(480, 150, 400),  color = color.white)
    navio = box (pos=vector(150,-145,-250), size=vector(1000, 280, 430),  color = color.yellow)
    partecima=box (pos=vector(450,130,-250), size=vector(250, 280, 300),  color = color.yellow)
    tras = box (pos=vector(-310,30,-250), size=vector(80, 80, 430),  color = color.yellow)
    lado =box (pos=vector(70,30,-440), size=vector(700, 80, 50),  color = color.yellow)
    pyramid(pos=vector(650,-145,-250), size=vector(300,280,400),color=color.yellow)
    rod = cylinder(pos=vector(460,250,-250),axis=vector(10,200,2), radius=100,color=color.yellow)
    rod.rotate(angle=pi/4, axis=vector(0,180,2), origin=vector(460,250,-250))
    for a in posicoesCais.keys():
        inputBox(posicoesCais[a],choice(cor))

    start(melhorIndividuo[0])
    
except RuntimeError or ZeroDivisionError:
    pass