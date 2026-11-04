# Dataye: Consulta de Vazamentos de E-mail

API e página web em Flask que verificam se um e-mail aparece em vazamentos de dados conhecidos, usando a API pública do [XposedOrNot](https://xposedornot.com/).

> ⚠️ Consulte somente e-mails que sejam seus ou para os quais você tenha autorização.

## Funcionalidades

- Consulta de um e-mail em vazamentos conhecidos (nomes dos vazamentos, sem senhas ou dados sensíveis).
- Página web simples para fazer a consulta.
- Endpoint JSON para uso por outros programas.
- Validação do formato do e-mail.
- Limite de uma consulta a cada 5 segundos por IP, para evitar abuso da API externa.
- Histórico das consultas salvo em SQLite.

## Arquitetura

O projeto segue a **arquitetura hexagonal** (portas e adaptadores), mantendo a regra de negócio separada da API externa e do banco de dados:

```
├── app.py                  # Aplicação Flask (rotas)
├── domain/                 # Entidades e portas (interfaces)
├── casos_de_uso/           # Regras de negócio (consultar_email.py)
├── adapters/               # Implementações das portas
│   ├── xposedornot_adapter.py   # Consulta à API do XposedOrNot
│   └── sqlite_repository.py     # Persistência em SQLite
└── templates/index.html    # Página web
```

## Como rodar

Requisitos: Python 3.13.

```bash
git clone https://github.com/G-Leite/NOME-DO-REPOSITORIO.git
cd NOME-DO-REPOSITORIO
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000` no navegador. Não é necessária chave de API.

## API

### `POST /consultar`

Corpo (JSON):

```json
{ "email": "exemplo@example.com" }
```

Exemplo com curl:

```bash
curl -X POST http://127.0.0.1:5000/consultar -H "Content-Type: application/json" -d "{\"email\": \"exemplo@example.com\"}"
```

Resposta (`200`):

```json
{
  "email": "exemplo@example.com",
  "foi_vazado": true,
  "vazamentos": [
    { "fonte": "xposedornot", "nome": "NomeDoVazamento" }
  ]
}
```

Erros:

| Código | Motivo |
|--------|--------|
| `400` | E-mail ausente ou inválido. |
| `429` | Consulta repetida em menos de 5 segundos pelo mesmo IP. |

## Privacidade

O arquivo local `vazamentos.db` (ignorado pelo Git) guarda, para cada consulta, o **e-mail consultado**, a **data** e os **nomes dos vazamentos** encontrados. Não são armazenadas senhas nem outros dados sensíveis. Se for publicar uma instância, avise os usuários sobre esse armazenamento.

## Limitações e próximos passos

- Não há confirmação de que o e-mail pertence a quem consulta.
- O limite de consultas fica em memória e é reiniciado quando o servidor reinicia.
- Ideias: consultas periódicas com alerta por e-mail, painel por cliente, testes automatizados com mocks e uso de mais de uma fonte de dados.

## Fonte dos dados

Os dados vêm da API pública do [XposedOrNot](https://xposedornot.com/). Consulte os termos de uso deles antes de usar este projeto em produção.

## Licença

Distribuído sob a licença MIT. Consulte o arquivo `LICENSE`.
