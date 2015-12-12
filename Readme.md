Python Version 3.5

###Como executar:

 - Nas máquinas aonde estão armazedados os logs devera ser executado o arquivo "server.py"  
 - Isso irá deixar o programa para executando no servidor para realizar a leitura e escrita de logs  
 
  <code>>>> python server.py</code>

 - Após os servidores estarem executando, escolha uma máquina, pode ser a mesma onde estão rodando os servidores ou outra, e execute o seguinte comando:
 
  <code>>>> python log_processor.py -s "IPSERVER_1,IPSERVER_2"</code>  
  *substitua o IPSERVER_N, pelo endereço IP das máquinas
 
###Processador de Logs:

- O objetivo da aplicação é processar arquivos de logs em N máquinas e consolidar 
os logs salvando eles em uma única maquina separando por usuário.

ex:
  
<b>Exemplo de entrada: </b>   
177.126.180.83 - - [15/Aug/2013:13:54:38 -0300] "GET /meme.jpg HTTP/1.1" 200 2148 "-" "userid=5352b590-05ac-11e3-9923-c3e7d8408f3a"  
177.126.180.83 - - [15/Aug/2013:13:54:38 -0300] "GET /lolcats.jpg HTTP/1.1" 200 5143 "-"
"userid=f85f124a-05cd-11e3-8a11-a8206608c529"  
177.126.180.83 - - [15/Aug/2013:13:57:48 -0300] "GET /lolcats.jpg HTTP/1.1" 200 5143 "-"
"userid=5352b590-05ac-11e3-9923-c3e7d8408f3a"  

<b>Exemplo de saida:</b>  
No servidor 3 (por exemplo) há um arquivo chamado <i><b>/tmp/5352b590-05ac-11e3-9923-
c3e7d8408f3a</i></b> que contém as linhas:  
177.126.180.83 - - [15/Aug/2013:13:54:38 -0300] "GET /meme.jpg HTTP/1.1" 200 2148 "-"  
"userid=5352b590-05ac-11e3-9923-c3e7d8408f3a"
177.126.180.83 - - [15/Aug/2013:13:57:48 -0300] "GET /lolcats.jpg HTTP/1.1" 200 5143 "-"
"userid=5352b590-05ac-11e3-9923-c3e7d8408f3a"  

No servidor 2 (por exemplo) há um arquivo chamado    
<i><b>/tmp/f85f124a-05cd-11e3-8a11-a8206608c529</i></b> que contém a linha:  
177.126.180.83 - - [15/Aug/2013:13:54:38 -0300] "GET /lolcats.jpg HTTP/1.1" 200 5143 "-"
"userid=f85f124a-05cd-11e3-8a11-a8206608c529"  
