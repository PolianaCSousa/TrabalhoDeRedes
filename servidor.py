import socket
from time import time, sleep

#VARIÁVEIS
qtd_pacotes = 0
bufferSize = 1440
dados = []
for i in range(1440):
    dados.append(0)  # "vetor" de dados que será enviado

print("BEM VINDO!")
ipServidor = input('Informe o IP servidor: ')
ipCliente = input('Informe o IP do cliente: ')

#PORTOS E IPS USADOS
PortoControle = 50000
Porto1Dados = 5050  # porto para o soquete que enviará dados
Porto2Dados = 5051  # porto para o soquete que receberá dados
Porto3Dados = 5052  #porto para o soquete UDP usado para cálculo da vazão
PortoClientePing = 5053 #porto do cliente que receberá a mensagem de ping de volta
PortoServidorPing = 5054 #porto do servidor que receberá a mensagem de ping do clientes
PortoResultados = 5055 #porto do servidor que receberá os dados calculados pelo cliente

#Soquete TCP para controle dos dados
soqueteTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria o soquete do servidor
soqueteTCP.bind((ipServidor, PortoControle)) #soquete foi associado ao ip e ao número de porto do servidor
soqueteTCP.listen() #a partir daqui o soquete está ouvindo as requisições do cliente
conexaoControle, endereco = soqueteTCP.accept() # aceita a conexão

#recebe a primeira mensagem de controle
dadoCliente = conexaoControle.recv(1024)
print(dadoCliente.decode())


#------------TESTE LARGURA DE BANDA--------------
#soquete que receberá os dados
TCP1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP1.bind((ipServidor, Porto1Dados))
TCP1.listen()
conexaoTCP1, endereco1 = TCP1.accept()
#recebendo os dados
TCP1.settimeout(4)
start = time()
while(time() - start < 10):
    try:
        dadoCliente1 = conexaoTCP1.recv(1024)
        qtd_pacotes += 1
    except (TimeoutError, RuntimeError):
        pass
conexaoTCP1.close() #fim da conexao que recebeu os dados
print("Recebi os pacotes do upload...")

#cálculo da vazão para upload
upload = (qtd_pacotes * 101824) / 10 #quantidade de bits recebidos por segundo
Uploadmbps = upload / 1000000 #converte para mbits (1 megabit possui 1000000 de bits)

sleep(1)
#soquete que enviará os dados
TCP2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP2.connect((ipCliente, Porto2Dados))
# enviando os dados
start = time()
while (time() - start < 10):
    TCP2.send(bytes(dados))
print('Enviei os pacotes para download...')


#------------ VAZÃO DA REDE -----------
UDP1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket UDP que receberá os dados
UDP1.bind((ipServidor, Porto3Dados))
UDP1.settimeout(4)

start = time()
while (time() - start < 10):  # recebendo os dados
    try:
        mensagemRecebida, enderecoServidor = UDP1.recvfrom(bufferSize)
        qtd_pacotes += 1
    except (TimeoutError, RuntimeError):
        pass
print("Recebi os pacotes para calcular a vazão da rede...")

UDP1.close()


#------------ LATÊNCIA DA REDE "ping" ------------
#soquete que receberá o ping e devolverá para o cliente
UDP2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP2.bind((ipServidor, PortoServidorPing))
mensagemRecebida2, enderecoCliente = UDP2.recvfrom(1)
UDP2.sendto(mensagemRecebida2, (ipCliente, PortoClientePing))

print('Recebi e reenviei o ping...')
sleep(2)


#------- RECEBENDO OS RESULTADOS OBTIDOS PELO CLIENTE -------
#soquete que receberá os resultados que foram calculados pelo cliente
TCPresultados = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPresultados.bind((ipServidor, PortoResultados))
TCPresultados.listen()
conexaoResultados, end = TCPresultados.accept()
#recebendo os resultados
resultados = conexaoResultados.recv(1024)
resultados = resultados.decode('utf8') #decodifica o dado recebido para string
resultados = eval(resultados) #converte a string em lista novamente

#cálculo da vazão da rede
vazao = (qtd_pacotes * 101824) / 10 #quantidade de bits recebidos por segundo
Vazaombps = vazao / 1000000 #converte para mbtis (1 megabit possui 1000000 de bits)

print("\nFinalizando os cálculos...\n")
sleep(3)

print("--- * --- * --- RESULTADOS --- * --- * ---\n")
print("Vazão de upload: %.2f mbps\nVazão de download: %.2f mbps\nVazão da rede: %.2f mbps\nLatência da rede: %.2f ms\n\n"%(Uploadmbps, resultados[0], Vazaombps, resultados[1]))

#recebe a segunda mensagem de controle
dadoCliente = conexaoControle.recv(1024)
print(dadoCliente.decode())
conexaoControle.close()
