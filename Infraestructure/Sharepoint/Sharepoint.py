# from config import TENANT_ID, CLIENT_ID, CLIENT_SECRET
import requests
import os
import time
import base64
from dotenv import load_dotenv

load_dotenv()

class SharePoint(object):

    def __init__(self):

        # Autenticação ao iniciar a classe
        self.token = self.create_token()

    def create_token(self):

        tenant_id = os.getenv('TENANT_ID')


        url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

        data = {
            'grant_type': 'client_credentials',
            'client_id': os.getenv('CLIENT_ID_SUB'),
            'client_secret': os.getenv('CLIENT_SECRET_SUB'),
            'scope': 'https://graph.microsoft.com/.default'
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            # Retorna o token de acesso
            return response.json().get('access_token')
        else:
            print("Erro ao buscar token")
            print(response.content)
            return None

    def get_id_user(self, mail_user):
        url = f"https://graph.microsoft.com/v1.0/users?$filter=mail eq '{mail_user}'"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(url, headers=headers)

        print(response.status_code)

        if response.status_code == 200:
                    
            json_data = response.json()

            for item in json_data["value"]:
                if item["mail"] == mail_user:
                    return item["id"]
            else:
                print(f"Erro ao buscar usuário: {response.content}")
            return None

    # Função para buscar o site_id com base no nome do site principal
    def get_site_id_by_name(self, search_name: str) -> str:
        url = "https://graph.microsoft.com/v1.0/sites"

        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()

            for item in json_data["value"]:
                if item["displayName"] == search_name:
                    return item["id"]
        else:
            print(f"Erro ao buscar site: {response.content}")
        return None
    
    # Função para buscar o subsite_id com base no nome do subsite
    def get_subsite_id_by_name(self, search_name, site_id) -> str:
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/sites"

        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            for item in json_data["value"]:
                if item["displayName"] == search_name:
                    return item["id"]
        else:
            print(f"Erro ao buscar subsite: {response.content}")
        return None

    # Função para buscar o drive_id com base no nome do drive
    def get_drive_id_by_name(self, site_id, search_name: str) -> str:
        if not site_id:
            print("Erro: Site ID não definido.")
            return None

        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"

        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            for item in json_data["value"]:
                if item["name"] == search_name:
                    return item["id"]
        else:
            print(f"Erro ao buscar drive ID: {response.content}")
        return None
    
    def get_list_id_by_name(self, site_id, search_name) -> str:
        
        url =  f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            for item in json_data["value"]:
                if item["displayName"] == search_name:
                    return item["id"]
        else:
            print(f"Erro ao buscar list ID: {response.content}")
        return None

    # Exemplo de método que usa o drive_id internamente
    def upload_file(self, site_name, drive_name, path_drive_name, path_file, file_name, subsite_name="") -> bool:
        # if not self.drive_id:
        #     print("Erro: Drive ID não encontrado.")
        #     return False

        site_id = self.get_site_id_by_name(site_name)

        if subsite_name != "":
            site_id = self.get_subsite_id_by_name(subsite_name, site_id)

        drive_id = self.get_drive_id_by_name(site_id, drive_name)

        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{path_drive_name}/{file_name}:/content"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/octet-stream"
        }

        with open(path_file, 'rb') as file:
            file_data = file.read()

        for _ in range(3):  # Tenta 3 vezes
            try:
                response = requests.put(url, headers=headers, data=file_data)
                break  # Sai do loop em caso de sucesso
            except ConnectionError:
                time.sleep(5)  # Aguardar 5 segundos antes de tentar novamente
        else:
            raise Exception("Falha ao enviar o arquivo após 3 tentativas.")

        if response.status_code == 201:
            print(f"Arquivo {path_file} enviado com sucesso.")
            return True
        else:
            print(f"Erro ao enviar arquivo: {response.content}")
            return False
        
    def delete_file(self, site_name, drive_name, path_drive_name, file_name, subsite_name="") -> bool:

        site_id = self.get_site_id_by_name(site_name)

        if subsite_name != "":
            site_id = self.get_subsite_id_by_name(subsite_name, site_id)

        drive_id = self.get_drive_id_by_name(site_id, drive_name)
    
        if not drive_id:
            print("Erro: Drive ID não encontrado.")
            return False

        # URL para deletar o arquivo no SharePoint
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{path_drive_name}/{file_name}"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        # Enviar requisição DELETE
        response = requests.delete(url, headers=headers)

        if response.status_code == 204:  # Status 204 indica sucesso sem conteúdo
            print(f"Arquivo {file_name} deletado com sucesso.")
            return True
        else:
            print(f"Erro ao deletar arquivo: {response.content}")
            return False
        
    def download_file(self, site_name, drive_name, path_drive_name, output_path, file_name, subsite_name=""):

        site_id = self.get_site_id_by_name(site_name)

        if subsite_name != "":
            site_id = self.get_subsite_id_by_name(subsite_name, site_id)

        drive_id = self.get_drive_id_by_name(site_id, drive_name)

        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{path_drive_name}/{file_name}:/content"

        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            with open(os.path.join(output_path,file_name), 'wb') as f:
                f.write(response.content)
            print(f"Arquivo {file_name} baixado com sucesso.")
            return True
        else:
            print(f"Erro ao baixar arquivo: {response.content}")
            return False

    def upload_file_onedrive(self, mail_user, path_file, path_onedrive):

        user_id = self.get_id_user(mail_user)

        url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/root:/{path_onedrive}:/content"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/octet-stream"
        }

        with open(path_file, 'rb') as file:
            file_data = file.read()

        response = requests.put(url, headers=headers, data=file_data)

        print(response.status_code)

        if response.status_code == 201:
            print(f"Arquivo {path_file} enviado com sucesso.")
            return True
        else:
            print(f"Erro ao enviar arquivo: {response.content}")
            return False
        
    def download_file_onedrive(self, mail_user, path_onedrive, output_path, file_name):

        user_id = self.get_id_user(mail_user)

        url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/root:/{path_onedrive}:/content"

        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            with open(os.path.join(output_path,file_name), 'wb') as f:
                f.write(response.content)
            print(f"Arquivo {file_name} baixado com sucesso.")
            return True
        else:
            print(f"Erro ao baixar arquivo: {response.content}")
            return False

    def create_item_list(self, site_name, list_name, content_list, subsite_name=""):
        site_id = self.get_site_id_by_name(site_name)

        if subsite_name != "":
            site_id = self.get_subsite_id_by_name(subsite_name, site_id)

        list_id = self.get_list_id_by_name(site_id, list_name)

        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # Convertendo o conteúdo para JSON, sem escapar os acentos
        # data_content = json.dumps(content_list, ensure_ascii=False)

        # Aqui a chave é 'fields' e o conteúdo deve ser o dicionário sem 'json.dumps()' aplicado a ele
        data = {
            "fields": content_list  # Passando diretamente o dicionário, sem json.dumps
        }

        # Requisição POST para criar o item
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            print("Item criado com sucesso!")
        else:
            print("Erro ao criar item:", response.status_code, response.text)

    def read_list(self, site_name, list_name, subsite_name=""):
 
        site_id = self.get_site_id_by_name(site_name)

        if subsite_name != "":
            site_id = self.get_subsite_id_by_name(subsite_name, site_id)

        list_id = self.get_list_id_by_name(site_id, list_name)

        itens_lista = []
 
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items?$expand=fields"
 
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
 
        response = requests.get(url, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            json_data = response.json()
 
            for item in json_data["value"]:
                itens_lista.append(item["fields"])
            return itens_lista
        else:
            print(f"Erro ao fazer leitura: {response.content}")
        return None
    
    def update_item_list(self, site_name, list_name, item_id, content_list, subsite_name=""):

        site_id = self.get_site_id_by_name(site_name)

        if subsite_name != "":
            site_id = self.get_subsite_id_by_name(subsite_name, site_id)

        list_id = self.get_list_id_by_name(site_id, list_name)

        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}/"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # data_content = json.loads(content_list)
        # print(data_content)

        data = {
            "fields": content_list
        }

        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Item modificado com sucesso!")
        else: 
            print("Erro ao modificar item:", response.status_code, response.text)

    def delete_item_list(self, site_name, list_name, item_id, subsite_name=""):

        site_id = self.get_site_id_by_name(site_name)

        if subsite_name != "":
            site_id = self.get_subsite_id_by_name(subsite_name, site_id)

        list_id = self.get_list_id_by_name(site_id, list_name)

        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}/"

        headers = {
            "Authorization": f"Bearer {self.token}",
            # "Content-Type": "application/json"
        }

        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            print("Item excluído com sucesso!")
        else: 
            print("Erro ao excluir item:", response.status_code, response.text)

    def list_files_sharepoint(self, site_name, drive_name, folder_path, subsite_name=""):
        site_id = self.get_site_id_by_name(site_name)

        if subsite_name != "":
            site_id = self.get_subsite_id_by_name(subsite_name, site_id)

        drive_id = self.get_drive_id_by_name(site_id, drive_name)

        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{folder_path}:/children"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(url, headers=headers)
        # response.raise_for_status()

        print(response.json()["value"])
        
        return response.json()["value"]
    
    def email_send(self, destinatario, assunto, corpo_html, caixa_saida, cc="", bcc="", anexos=""):
        def criar_lista_destinatarios(destinatarios_str):
            delimitadores = [',', ';']
    
            for delimitador in delimitadores:
                destinatarios_str = destinatarios_str.replace(delimitador, ',')
            
            destinatarios = [email.strip() for email in destinatarios_str.split(',') if email.strip()]
            
            destin_values = [{"emailAddress": {"address": email}} for email in destinatarios]
            return destin_values

        def converter_para_base64(caminho_arquivo):
            """Lê um arquivo e o converte para Base64"""
            try:
                with open(caminho_arquivo, "rb") as file:
                    arquivo_base64 = base64.b64encode(file.read()).decode('utf-8')
                return arquivo_base64
            except Exception as e:
                print(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
                return None

        destinatario_emails = criar_lista_destinatarios(destinatario)
        cc_emails = criar_lista_destinatarios(cc)
        bcc_emails = criar_lista_destinatarios(bcc)

        graph_api_url = f"https://graph.microsoft.com/v1.0/users/{caixa_saida}/sendMail"

        email_data = {
            "message": {
                "subject": assunto,
                "body": {
                    "contentType": "HTML",
                    "content": corpo_html
                },
                "toRecipients": destinatario_emails,
                "ccRecipients": cc_emails,
                "bccRecipients": bcc_emails,
                "from": {
                    "emailAddress": {
                        "address": caixa_saida
                    }
                }
            },
            "saveToSentItems": "true"
        }

        if anexos:
            anexos_lista = [arquivo.strip() for arquivo in anexos.replace(";", ",").split(",")]

            attachments = []
            for caminho in anexos_lista:
                if os.path.isfile(caminho):
                    nome_arquivo = os.path.basename(caminho)
                    conteudo_base64 = converter_para_base64(caminho)
                    
                    if conteudo_base64:
                        attachment = {
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "name": nome_arquivo,  # Nome do arquivo
                            "contentBytes": conteudo_base64  # Conteúdo do arquivo em Base64
                        }
                        attachments.append(attachment)
                else:
                    print(f"Arquivo não encontrado: {caminho}")

            if attachments:
                email_data["message"]["attachments"] = attachments

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(graph_api_url, headers=headers, json=email_data)
        
        if response.status_code == 202:
            print(f'E-mail enviado para {destinatario}')
        else:
            print(f'Erro ao enviar e-mail para {destinatario}: {response.status_code}')
            print(response.text)