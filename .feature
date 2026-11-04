# language: pt
Funcionalidade: Consultar vazamentos de e-mail

  Cenário: Consulta de um e-mail válido
    Dado que informo o e-mail "exemplo@example.com"
    Quando envio a consulta
    Então recebo o resultado da verificação

  Cenário: E-mail com formato inválido
    Dado que informo o e-mail "isso-nao-e-email"
    Quando envio a consulta
    Então recebo a mensagem de erro "e-mail ausente ou inválido"

  Cenário: Consultas seguidas em menos de 5 segundos
    Dado que acabei de fazer uma consulta
    Quando envio outra consulta em menos de 5 segundos
    Então a consulta é recusada com o código 429