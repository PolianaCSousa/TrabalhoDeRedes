import socket
import sys
from time import time, sleep

#VARIÁVEIS
qtd_pacotes = 0
bufferSize = 1440
dados = []
for i in range(1440):
    dados.append(0)  # "vetor" de dados que será enviado
resultados = [] #lista que enviará os cálculos feitos pelo cliente para o servidor

# a função getsizeof me retorna o tamanho em bytes do objeto (nesse caso, a lista dados)
tamanhoDados = sys.getsizeof(dados)  # a lista dados possui um tamanho de  12728 bytes ou seja 101824 bits

#PORTOS E IPS USADOS
ipCliente = input('Informe o IP do cliente: ')
ipServidor = input('Informe o IP servidor: ')
PortoControle = 50000
Porto1Dados = 5050  # porto para o soquete que enviará dados
Porto2Dados = 5051  # porto para o soquete que receberá dados
Porto3Dados = 5052  #porto para o soquete UDP usado para cálculo da vazão
PortoclientePing = 5053 #porto do cliente que receberá a mensagem de ping de volta
PortoServidorPing = 5054 #porto do servidor que receberá a mensagem de ping do clientes
PortoResultados = 5055 #porto do servidor que receberá os dados calculados pelo cliente

#socket tcp para controle dos dados
TCPcontrole = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPcontrole.connect((ipServidor, PortoControle))
# Inicio da comunicação/controle
TCPcontrole.send(str.encode('Fazendo os cálculos...\n'))
sleep(1)


#------------TESTE LARGURA DE BANDA--------------
#soquete tcp que enviara dados
TCP1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP1.connect((ipServidor, Porto1Dados))
# enviando os dados
start = time()
while (time() - start < 10):
    TCP1.send(bytes(dados))

#soquete tcp que receberá os dados
TCP2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP2.bind((ipCliente, Porto2Dados))
TCP2.listen()
conexaoTCP2, endereco2 = TCP2.accept()
#recebendo os dados
TCP2.settimeout(4)
start = time()
while(time() - start < 10):
    try:
        dadoCliente2 = conexaoTCP2.recv(1024)
        qtd_pacotes += 1
    except (TimeoutError, RuntimeError):
        pass
conexaoTCP2.close()

#cálculo para a vazão de download
download = (qtd_pacotes * 101824) / 10 #quantidade de bits recebidos por segundo
mbps = download / 1000000 #converte para mbits (1 megabit possui 1000000 de bits)

resultados.append(mbps)


#------------ VAZÃO DA REDE -----------
UDP1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
start = time()
while(time() - start < 10):
    UDP1.sendto(bytes(dados), (ipServidor, Porto3Dados))


#------------ LATÊNCIA DA REDE "ping" ------------
#soquete que enviará o ping e receberá de volta do servidor
UDP2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP2.bind((ipCliente, PortoclientePing))

t0 = time() * 1000 #converte o tempo de segundos para milisegundos
UDP2.sendto(bytes(1), (ipServidor, PortoServidorPing))
mensagemRecebida, enderecoServidor = UDP2.recvfrom(1)
t1 = time() * 1000 #converte o tempo de segundos para milisegundos
ms = t1 - t0

resultados.append(ms)
sleep(4)

#------- ENVIANDO OS RESULTADOS OBTIDOS PARA O SERVIDOR -------
#socket tcp que enviará os resultados
TCPresultados = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPresultados.connect((ipServidor, PortoResultados))
# envia os resultados
resultados = str(resultados) #converte a lista em string
TCPresultados.send(str.encode(resultados))

#Fim da comunicação/controle
TCPcontrole.send(str.encode('Fim dos cálculos!\n'))