# Submódulo Sharepoint

Este projeto é uma ferramenta para fazer upload, download e eclusão de arquivos do SharePoint e do OneDrive usando a API Microsoft Graph. Ele autentica via OAuth2 com credenciais de cliente e permite buscar sites e subsites do SharePoint.

## Requisitos

- **Python 3.9**
- **Bibliotecas necessárias** (definidas no `requirements.txt`):
  - `requests`

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
3. Crie um arquivo `.env` para armazenar as credenciais do cliente para autenticação OAuth2:
   ```
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret
   ```

## Tags e versionamento
Para garantir um versionamento eficiente e rastreável do código, utilizamos tags no Git. As tags permitem marcar versões específicas do projeto, facilitando rollback, deploys e a rastreabilidade das mudanças.

Utilizamos a versão estável cujo propósito era simplesmente fazer tranferências de arquivos e ler listas do sharepoint como ponto de partida com a tag `v1.0.0`.
### Convenção de versionamento
Seguimos a Semantic Versioning (SemVer) no formato MAJOR.MINOR.PATCH:
- MAJOR: Mudanças incompatíveis com versões anteriores.
- MINOR: Novas funcionalidades compatíveis com versões anteriores.
- PATCH: Correções de bugs e pequenas melhorias sem impacto na compatibilidade.

## Uso

### Inicialização da Classe SharePoint

A classe `SharePoint` é responsável por gerenciar a autenticação e as operações de upload de arquivos.

### Funções utilizadas para manipulação de arquivos e dados

### 1. `upload_file(self, site_name, drive_name, path_drive_name, path_file, file_name, subsite_name="")`<br>
Faz o upload de um arquivo para a biblioteca SharePoint. Recebe 6 parâmetros:

- `site_name`: Nome do site no qual irá fazer upload do arquivo
- `drive_name`: Nome da biblioteca de documentos no qual irá fazer upload do arquivo
- `path_drive_name`: Caminho no Sharepoint onde irá fazer upload do arquivo
- `path_file`: Caminho local para o arquivo.
- `file_name`: Nome do arquivo que será salvo no SharePoint.
- `subsite_name`: Argumento opcional para que, quando for um caso de uso com subsite, utilizar esse parâmetro

### Exemplos
1. Upload para um site principal:
   ```python
   # Obs.: Caso o caminho passado como no exemplo abaixo não exista as pastas passadas, ele as cria automaticamente e salva o arquivo nela.

   #Variáveis de ambiente que estarão no .env
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret

   sharepoint = SharePoint()
   sharepoint.upload_file("Paraty Tecnologia", "Documentos", "Teste", r"C:\Users\BrunoFerreiradeSousa\Downloads\Teste.pdf", "Teste.pdf")
   ```
2. Upload para subsite:
   ```python
   # Obs.: Caso o caminho passado como no exemplo abaixo não exista as pastas passadas, ele as cria automaticamente e salva o arquivo nela.

   #Variáveis de ambiente que estarão no .env
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret

   sharepoint = SharePoint()
   sharepoint.upload_file("Paraty_Energia", "Comercializacao_e_Servicos", "Gestão de Clientes/Relatório de Medição - Novo/23-01-25", r"C:\Users\BrunoFerreiradeSousa\Downloads\Teste.pdf", "Teste.pdf", "Paraty_SP")
   ```

### 2. `delete_file(self, site_name, drive_name, path_drive_name, file_name, subsite_name="")`

Deleta arquivos de uma biblioteca do sharepoint. Recebe 5 parâmetros:

- `site_name`: Nome do site no qual irá fazer a exclusão do arquivo
- `drive_name`: Nome da biblioteca de documentos na qual irá fazer a exclusão dos arquivos
- `path_drive_name`: Caminho no Sharepoint onde irá fazer a exclusão do arquivo
- `file_name`: Nome do arquivo que irá apagar
- `subsite_name:` Argumento opcional para que, quando for um caso de uso com subsite, utilizar esse parâmetro

### Exemplo:

```python
   #Variáveis de ambiente que estarão no .env
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret

   sharepoint = Sharepoint()
   sharepoint.delete_file("Paraty Tecnologia", "Documentos", "Teste", "Teste.pdf")
```

### 3. `download_file(self, site_name, drive_name, path_drive_name, output_path, file_name, subsite_name="")`

Faz o download de um arquivo do sharepoint. Recebe 6 parâmetros:

- `site_name`: Nome do site no qual irá fazer download do arquivo
- `drive_name`: Nome da biblioteca de documentos na qual irá fazer o download do arquivo
- `path_drive_name`: Caminho no Sharepoint onde irá fazer o download do arquivo
- `output_path`: Caminho onde o arquivo será salvo
- `file_name`: Nome do arquivo que será salvo + tipo de arquivo(.pdf, .xlsx, etc) 
- `subsite_name:` Argumento opcional para que, quando for um caso de uso com subsite, utilizar esse parâmetro

### Exemplo:

```python
   #Variáveis de ambiente que estarão no .env
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret

   sharepoint = SharePoint()
   sharepoint.download_file("Paraty Tecnologia", "Documentos", "Teste", r"C:\Users\BrunoFerreiradeSousa\Downloads", "Teste.xlsx")
```

### 4. `upload_file_onedrive(self, mail_user, path_file, path_onedrive)`
Salva um arquivo no onedrive do usuário desejado. Possui 3 parâmetros:

- `mail_user`: Email do usuário no qual irá fazer o upload
- `path_file`: Caminho do arquivo onde o arquivo está
- `path_onedrive`: Caminho no qual onde será salvo no onedrive

### Exemplo:

```python
   #Variáveis de ambiente que estarão no .env
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret

   sharepoint = Sharepoint()
   sharepoint.upload_file_onedrive("teste@paratyenergia.com.br",r"C:\Users\BrunoFerreiradeSousa\Downloads\teste.pdf", "Documentos/teste")
```

### 5. `download_file_onedrive(self, mail_user, path_onedrive, output_path, file_name)`
Salva um arquivo do onedrive do usuário desejado. Possui 4 parâmetros:

- `mail_user`: Email do usuário no qual irá fazer o download
- `path_onedrive`: Caminho onde o arquivo está no Onedrive
- `output_path`: Caminho onde o arquivo será salvo
- `file_name`: Nome do arquivo que será salvo + tipo de arquivo(.pdf, .xlsx, etc)

### Exemplo:

```python
   #Variáveis de ambiente que estarão no .env
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret

   sharepoint = Sharepoint()
   sharepoint.download_file_onedrive("teste@paratyenergia.com.br", "Documentos/teste", r"C:\Users\BrunoFerreiradeSousa\Downloads", "teste.pdf")
```

### 6. `create_item_list(self, site_name, list_name, content_list, subsite_name=""):`

Cria um item numa lista do sharepoint existente. Possui 4 parâmetros:

- `site_name`: Nome do site no qual irá criar o item na lista
- `list_name`: Nome da lista no qual irá criar o item
- `content_list`: Conteúdo que será criado na lista
- `subsite_name`: Argumento opcional para que, quando for um caso de uso com subsite, utilizar esse parâmetro
 
### Exemplo:

```python
   #Variáveis de ambiente que estarão no .env
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret

   sharepoint = Sharepoint()
   # Obs.: A primeira coluna sempre terá o nome 'Title' por mais que seja mudada no sharepoint
   sharepoint.create_item_list("Paraty Tecnologia", "Teste", {"Title": "valor", "Coluna2": "valor"})
```

### 7. `read_list(self, site_name, list_name, subsite_name="")`

Faz a leitura dos itens que estão na lista desejada. Possui 3 parâmetros:

- `site_name`: Nome do site no qual irá ler a lista
- `list_name`: Nome da lista na qula será lida
-  `subsite_name`: Argumento opcional para que, quando for um caso de uso com subsite, utilizar esse parâmetro

### Exemplo:

```python
   #Variáveis de ambiente que estarão no .env
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret

   sharepoint = Sharepoint()
   sharepoint.read_list("Paraty Tecnologia", "Teste")
```

### 8. `update_item_list(self, site_name, list_name, item_id, content_list, subsite_name="")`
Atualiza algum item já existente na lista. Possui 5 parâmetros:

- `site_name`: Nome do site no qual irá atualizar o item da lista
- `list_name`: Nome da lista na qual irá atualizar o item
- `item_id`: id do item na lista. Geralmente fica numa linha oculta do sharepoint por padrão e é criado automaticamente.
- `content_list`: Conteúdo que será  mandado para atualizar na lista
- `subsite_name`: Argumento opcional para que, quando for um caso de uso com subsite, utilizar esse parâmetro

### Exemplo:

```python
   #Variáveis de ambiente que estarão no .env
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret

   sharepoint = Sharepoint()
   sharepoint.update_item_list("Paraty Tecnologia", "Teste", 5, {"Title": "Valor new", "Coluna2": "Valor new2"})
```

### 9. `delete_item_list(self, site_name, list_name, item_id, subsite_name="")`

Deleta um item já existente na lista. Possui 4 parâmetros:

- `site_name`: Nome do site no qual irá excluir o item da lista
- `list_name`: Nome da lista na qual irá excluir o item
- `item_id`: id do item na lista. Geralmente fica numa linha oculta do sharepoint por padrão e é criado automaticamente.
- `subsite_name`: Argumento opcional para que, quando for um caso de uso com subsite, utilizar esse parâmetro

### Exemplo:

```python
   #Variáveis de ambiente que estarão no .env
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret

   sharepoint = Sharepoint()
   sharepoint.delete_item_list("Paraty Tecnologia", "Teste", 7)
```

### 10. `email_send(self, destinatario, assunto, corpo_html, caixa_saida, cc="", bcc="", anexos="")`

Faz envio de email. Possui 7 parâmetros:

- `destinatario`: Email das pessoas a quem deseja fazer o envio. (Delimitador por "," ou ";")
- `assunto`: Assunto do email
- `corpo_html`: Corpo do email em html
- `caixa_saida`: De qual caixa/em nome de quem será enviado o email
- `cc`: Email das pessoas que estarão em cópia (Parâmetro opcional)
- `bcc`: Email das pessoas que estarão em cópia oculta (Parâmetro opcional)
- `anexos`: Caminho de onde estão os arquivos que serão anexados no email (Parâmetro opcional)

### Exemplo:
```python
   #Variáveis de ambiente que estarão no .env
   TENANT_ID=seu-tenant-id
   CLIENT_ID_SUB=seu-client-id
   CLIENT_SECRET_SUB=seu-client-secret

   sharepoint = Sharepoint()
   sharepoint.email_send(destinatario="teste@gmail.com", cc="bruno.ferreira@paratyenergia.com.br", assunto="Teste", corpo_html="<p>Nenhum</p>", caixa_saida="bruno.ferreira@paratyenergia.com.br", anexos=r"C:\Users\usuário\Downloads\Teste.pdf, C:\Users\usuário\Downloads\Teste2.pdf")
```

### Observação importante
Na Paraty hoje utilizamos bibliotecas de documentos principais que estão criadas num subsite.

`Paraty_Energia` seria o site pai e `Paraty_SP` e `Mascarenhas` os sites filhos (subsites).

Então, caso queira enviar algum documento numa biblioteca que está na lista abaixo, é necessário informar o site `Paraty_Energia` e também o subsite na chamada da classe. 

Lista de bibliotecas encontradas nos subsites:
#### Paraty_SP

- Administrativo
- Comercializacao_e_Servicos
- Geracao_e_BusDev
- Recursos_Humanos
- Juridico
- Financeiro
- Publica

#### Mascarenhas

- Mascarenhas
- Mascarenhas_Historico
- Mascarenhas_RH