from nest.core import Injectable
from src.modules.aneel.aneel_tasks import executar_automacao_aneel
from src.config.celery_app import app as celery_app

import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

@Injectable()
class AneelService:
    
    def iniciar_automacao(self, cnpj_busca: str) -> dict:
        print(f"SERVICE: Enviando tarefa para a fila com o CNPJ '{cnpj_busca}'")
        tarefa = executar_automacao_aneel.delay(cnpj_busca)
        return {"mensagem": "Tarefa de automação iniciada com sucesso.", "id_da_tarefa": tarefa.id}

    def verificar_status(self, id_da_tarefa: str) -> dict:
        """
        Usa o ID para criar um objeto 'AsyncResult' a partir da nossa app Celery,
        que sabe onde está o backend de resultados (Redis).
        """
        resultado_tarefa = celery_app.AsyncResult(id_da_tarefa)
        
        if resultado_tarefa.ready():
            return {
                "id": id_da_tarefa,
                "status": resultado_tarefa.state, # Retorna 'SUCCESS' ou 'FAILURE'
                "resultado": resultado_tarefa.result # Retorna o dicionário que a tarefa retornou
            }
        else:
            # A tarefa ainda não terminou
            return {
                "id": id_da_tarefa,
                "status": resultado_tarefa.state, # Retorna 'PENDING' ou 'STARTED'
                "resultado": "A tarefa ainda está sendo processada."
            }
            
    def obter_dados_boleto(self, cnpj_busca: str) -> dict:
        
        DOMINIO_ANEEL = "https://sistemas.aneel.gov.br"
        URL_BASE_APP = f"{DOMINIO_ANEEL}/concessionarios/taxafiscalizacao/aplicativo/"
        URL_BASE_EXTRANET = f"{URL_BASE_APP}Extranet/"
        URL_PAGINA_BUSCA_CNPJ = f"{URL_BASE_EXTRANET}Concessionario_selecao_passo1_cnpj.asp"
        URL_ENVIO_BUSCA = f"{URL_BASE_EXTRANET}Concessionario_selecao_Passo2.asp"
        URL_ENVIO_SELECAO = f"{URL_BASE_EXTRANET}concessionario_agrupamento.asp"
        
        """
        Função de serviço que busca um empreendedor por CNPJ, filtra o resultado
        correto de uma lista potencialmente grande, itera sobre as usinas e 
        retorna um JSON com os dados dos boletos.
        """
        print(f"SERVICE (SYNC): Iniciando busca síncrona para o CNPJ: '{cnpj_busca}'...")
        
        resultados_gerais = []
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        })
        
        try:
            session.get(URL_PAGINA_BUSCA_CNPJ)
            payload_busca = {'txtCNPJ': cnpj_busca, 'consulta': 'nova'}
            response_busca = session.post(URL_ENVIO_BUSCA, data=payload_busca, headers={'Referer': URL_PAGINA_BUSCA_CNPJ})
            response_busca.raise_for_status()

            # --- ETAPA 2: Coletar e FILTRAR os Empreendedores encontrados ---
            soup_lista_empresas = BeautifulSoup(response_busca.text, 'lxml')
            select_empreendedor = soup_lista_empresas.find('select', {'name': 'lbxDeclarante'})
            if not select_empreendedor:
                return {"sucesso": False, "erro": "A página de resposta da busca não continha a lista de empreendedores."}
            
            options_empreendedores = select_empreendedor.find_all('option')
            if not options_empreendedores:
                return {"sucesso": False, "erro": "A lista de empreendedores retornada está vazia."}
            
            # --- BLOCO DE FILTRAGEM ---
            print(f"Recebidas {len(options_empreendedores)} empresas do servidor. Filtrando pelo CNPJ '{cnpj_busca}'...")
            
            # Limpa o CNPJ buscado para comparação (remove '.', '/', '-')
            cnpj_limpo = re.sub(r'[^\d]', '', cnpj_busca)
            
            empreendedores_a_processar = []
            for option in options_empreendedores:
                texto_completo = (option.text or "").strip()
                # Verifica se o CNPJ limpo existe no texto da opção
                if cnpj_limpo in re.sub(r'[^\d]', '', texto_completo):
                    valor = (option.get('value') or "").strip()
                    empreendedores_a_processar.append({'nome_exibido': texto_completo, 'valor': valor})
            
            if not empreendedores_a_processar:
                return {"sucesso": False, "erro": f"Nenhum empreendedor encontrado para o CNPJ '{cnpj_busca}' após a filtragem."}
            # --- FIM DO BLOCO DE FILTRAGEM ---

            print(f"Encontrados {len(empreendedores_a_processar)} empreendedores após o filtro. Iniciando extração...")

            # --- LOOP EXTERNO: Para cada Empreendedor ---
            for i, empreendedor in enumerate(empreendedores_a_processar):
                print(f"\n--- Processando Empreendedor {i+1}/{len(empreendedores_a_processar)}: {empreendedor['nome_exibido']} ---")
                try:
                    payload_selecao = {'lbxDeclarante': empreendedor['valor']}
                    response_agrupamento = session.post(URL_ENVIO_SELECAO, data=payload_selecao, headers={'Referer': response_busca.url})
                    response_agrupamento.raise_for_status()

                    soup_agrupamento = BeautifulSoup(response_agrupamento.text, 'lxml')
                    links_usinas = soup_agrupamento.find_all('a', href=re.compile(r'EmitirGRU\.asp'))
                    
                    if not links_usinas:
                        print("Nenhuma usina/entidade com boleto encontrada para este empreendedor.")
                        continue

                    print(f"Encontradas {len(links_usinas)} usinas/entidades. Extraindo dados...")

                    # --- LOOP INTERNO: Para cada Usina/Entidade ---
                    for j, link in enumerate(links_usinas):
                        nome_usina = (link.text or f"Usina {j+1}").strip()
                        try:
                            url_pagina_emissao = urllib.parse.urljoin(response_agrupamento.url, link['href'])
                            response_emissao = session.get(url_pagina_emissao, headers={'Referer': response_agrupamento.url})
                            response_emissao.raise_for_status()
                            
                            soup_final = BeautifulSoup(response_emissao.text, 'lxml')
                            tag_competencia = soup_final.find('select', {'name': 'cbCompetencia'}).find('option')
                            if not tag_competencia: raise Exception("Dados de competência não encontrados.")
                            
                            valor_competencia = tag_competencia['value']
                            data_vencimento = soup_final.find('input', {'name': 'DataVencimento_req'})['value']
                            partes = valor_competencia.split('|')
                            
                            dados_usina = {
                                "empreendedor": empreendedor['nome_exibido'], "usina": nome_usina,
                                "status": "Sucesso", "valor_boleto": float(partes[1].replace(',', '.')),
                                "data_vencimento": data_vencimento, "mes_competencia": partes[6],
                            }
                            resultados_gerais.append(dados_usina)
                            print(f"  - Dados da usina '{nome_usina}' extraídos com sucesso. ✅")
                        except Exception as e_usina:
                            resultados_gerais.append({"empreendedor": empreendedor['nome_exibido'], "usina": nome_usina, "status": "Falha", "motivo": str(e_usina)})
                
                except Exception as e_empreendedor:
                    resultados_gerais.append({"empreendedor": empreendedor['nome_exibido'], "status": "Falha Geral", "motivo": str(e_empreendedor)})

            return {"sucesso": True, "relatorio": resultados_gerais}

        except Exception as e:
            return {"sucesso": False, "erro": f"Ocorreu um erro inesperado: {e}"}