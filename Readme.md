GRUPO: Poliana, Leandro e João Paulo

Ao todo foram usados 6 soquetes:
1º SOQUETE (no código: TCPcontrole):  é um soquete TCP usado para controle , e envia mensagem para o servidor ao iniciar os testes e ao final dos testes envia novamente uma mensagem de finalização dos mesmos.
2º e 3º SOQUETES (no código: TCP1 e TCP2): são soquetes TCP usados para o cálculo da largura de banda. O primeiro soquete TCP usado para esse cálculo é responsável pelo upload (cliente envia para o servidor) e o segundo soquete é responsável pelo download (servidor envia para o cliente).
4º SOQUETE (no código: UDP1): é um soquete UDP usado no teste de vazão d rede (cliente envia para o servidor).
5º SOQUETE (no código: UDP2): é um soquete UDP usado no teste de latência da rede (cliente envia um byte para o servidor, e o servidor devolve esse byte).
6º SOQUETE (no código: TCPresultados): é um soquete TCP que tem a finalidade de enviar para o servidor os cálculos realizados pelo cliente. Nesse caso, o cliente calcula a vazão de download e a latência da rede. Esse soquete envia portanto, uma lista contendo o resultado desses cálculos para o servidor. 

OBS: 
Os dados enviados pelos soquetes usados nos testes de largura de banda e vazão é uma lista que possui tamanho igual a 1440 e é preenchida de zeros. Seu tamanho total em bytes após preenchida é de 12728 bytes ou seja, 101824 bits. 
Durante os testes de largura de banda e vazão, o dados são enviados por durante 10 segundos.
Ao final, os resultados de todos os cálculos são printados apenas no servidor.
