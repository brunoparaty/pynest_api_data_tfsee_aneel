from src.config.celery_app import app as celery_app
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import os
import time
from datetime import datetime, timedelta
from Infraestructure.Sharepoint.Sharepoint import SharePoint

@celery_app.task
def executar_automacao_aneel(cnpj_busca: str):
    """
    Tarefa Celery que busca um empreendedor por CNPJ, itera sobre todas as suas
    usinas/entidades, baixa o boleto TFSEE em PDF para cada uma e faz o upload
    para uma pasta dinâmica no SharePoint.
    """
    pasta_destino_local = "Boletos_PDF_ANEEL"
    print(f"WORKER: Iniciando automação para o CNPJ: '{cnpj_busca}'...")
    
    resultados_gerais = []
    try:
        sp = SharePoint() 
    except Exception as e:
        return {"sucesso": False, "erro": f"Falha ao inicializar a conexão com o SharePoint: {e}"}

    hoje = datetime.today()
    ano_atual_str = hoje.strftime("%Y")
    primeiro_dia_mes_atual = hoje.replace(day=1)
    mes_referencia_dt = primeiro_dia_mes_atual - timedelta(days=1)
    mes_referencia_str = mes_referencia_dt.strftime("%m")
    ano_mes_arquivo = hoje.strftime("%y") + mes_referencia_dt.strftime("%m")

    with sync_playwright() as p:
        # Configuração otimizada para economizar memória (512MB)
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-dev-shm-usage',      # Evita usar /dev/shm (importante!)
                '--no-sandbox',                 # Remove sandbox
                '--disable-setuid-sandbox',
                '--disable-gpu',                # Desabilita GPU
                '--disable-software-rasterizer',
                '--disable-extensions',
                '--disable-background-networking',
                '--disable-default-apps',
                '--disable-sync',
                '--single-process',             # ⭐ Crucial para 512MB!
                '--no-zygote',
                '--disable-accelerated-2d-canvas',
                '--memory-pressure-off'
            ]
        )
        context = browser.new_context(**p.devices['Desktop Chrome'])
        page = context.new_page()

        try:
            # --- Etapa 1: Navegação e Busca por CNPJ ---
            url_inicial = "https://sistemas.aneel.gov.br/concessionarios/taxafiscalizacao/aplicativo/default.asp?flag=2"
            page.goto(url_inicial, timeout=60000)

            close_button_locator = page.locator('#myModal .close')
            try:
                close_button_locator.wait_for(state='visible', timeout=15000)
                close_button_locator.click()
            except PlaywrightTimeoutError:
                print("Nenhum pop-up de 'Atenção' encontrado.")
            
            frame = page.frame(name="main")
            if not frame: frame = page
            
            print("Clicando em 'Emitir GRU por CNPJ/CPF'...")
            frame.locator("a:has-text('Emitir GRU por CNPJ/CPF')").click()
            
            campo_busca_seletor = 'input#txtCnpjCpf'
            frame.wait_for_selector(campo_busca_seletor, timeout=30000).fill(cnpj_busca)
            frame.locator('input[value="Avançar"]').click()
            
            seletor_empreendedores = 'select[name="lbxDeclarante"] option'
            frame.wait_for_selector(seletor_empreendedores, timeout=30000)
            
            count_empreendedores = frame.locator(seletor_empreendedores).count()
            if count_empreendedores == 0:
                raise Exception(f"Nenhum empreendedor encontrado para o CNPJ '{cnpj_busca}'")

            print(f"Encontrados {count_empreendedores} empreendedores. Iniciando processamento...")

            # --- LOOP EXTERNO: Para cada Empreendedor encontrado ---
            for i in range(count_empreendedores):
                frame = page.frame(name="main")
                if not frame: frame = page
                
                empreendedor_option = frame.locator(seletor_empreendedores).nth(i)
                nome_empreendedor = (empreendedor_option.text_content() or "").strip()
                
                print(f"\n--- Processando Empreendedor {i+1}/{count_empreendedores}: {nome_empreendedor} ---")
                frame.locator('select[name="lbxDeclarante"]').select_option(index=i)
                frame.locator('input[value="Avançar"]').click()
                
                # --- Coleta de Usinas/Entidades ---
                seletor_usinas = 'a[href*="EmitirGRU.asp"]'
                frame.wait_for_selector(seletor_usinas, timeout=30000)
                count_usinas = frame.locator(seletor_usinas).count()
                
                if count_usinas == 0:
                    print(f"Nenhuma usina/entidade encontrada para {nome_empreendedor}. Retornando...")
                    resultados_gerais.append({"empreendedor": nome_empreendedor, "status": "Falha", "motivo": "Nenhuma usina/entidade com boleto disponível."})
                    frame.go_back()
                    frame.wait_for_load_state('networkidle')
                    continue 

                print(f"Encontradas {count_usinas} usinas/entidades. Processando boletos...")

                # --- LOOP INTERNO: Para cada Usina/Entidade encontrada ---
                for j in range(count_usinas):
                    try:
                        frame = page.frame(name="main")
                        if not frame: frame = page
                        
                        usina_link = frame.locator(seletor_usinas).nth(j)
                        nome_usina = (usina_link.text_content() or f"usina_{j+1}").strip()
                        print(f"Processando usina {j+1}/{count_usinas}: {nome_usina}")
                        
                        usina_link.click()
                        
                        # --- Fluxo de Download e Upload ---
                        frame.wait_for_selector('input[value="Gerar Arrecadação"]', timeout=30000)
                        with page.context.expect_page() as new_page_info:
                            frame.locator('input[value="Gerar Arrecadação"]').click()
                        
                        boleto_page = new_page_info.value
                        boleto_page.wait_for_load_state('networkidle')
                        
                        ok_button_final = boleto_page.locator('button#Continuar')
                        ok_button_final.wait_for(state='visible', timeout=60000)
                        ok_button_final.click()
                        
                        boleto_page.wait_for_load_state('domcontentloaded', timeout=60000)
                        time.sleep(5)

                        os.makedirs(pasta_destino_local, exist_ok=True)
                        nome_arquivo_limpo = nome_usina.replace('/','-')
                        nome_arquivo = f"TFSEE {nome_arquivo_limpo} {ano_mes_arquivo} {cnpj_busca}.pdf"
                        caminho_local_completo = os.path.join(pasta_destino_local, nome_arquivo)
                        
                        boleto_page.pdf(path=caminho_local_completo, print_background=True)
                        print(f"PDF salvo localmente em: {caminho_local_completo}")
                        
                        # Upload imediato para o SharePoint
                        print("Enviando arquivo para o SharePoint...")
                        pasta_sharepoint = f"Gestão de Clientes/Taxa de Fiscalização ANEEL/{ano_atual_str}/{mes_referencia_str}"
                        sp.upload_file("Paraty_Energia", "Comercializacao_e_Servicos", pasta_sharepoint, caminho_local_completo, nome_arquivo, "Paraty_SP")
                        print("Upload para o SharePoint concluído com sucesso. ✅")
                        
                        resultados_gerais.append({"empreendedor": nome_empreendedor, "usina": nome_usina, "status": "Sucesso", "arquivo_local": caminho_local_completo})
                        
                        boleto_page.close()
                        
                    except Exception as e_usina:
                        print(f"!!! Falha ao processar a usina '{nome_usina}': {e_usina}")
                        resultados_gerais.append({"empreendedor": nome_empreendedor, "usina": nome_usina, "status": "Falha", "motivo": str(e_usina)})
                    finally:
                        # Garante que sempre voltamos para a página de seleção de usinas
                        frame.go_back()
                        frame.wait_for_load_state('networkidle')

                # Volta para a página de seleção de empreendedores
                print(f"Finalizado o processamento para {nome_empreendedor}. Retornando...")
                frame.go_back()
                frame.wait_for_load_state('networkidle')

            browser.close()
            return {"sucesso": True, "relatorio": resultados_gerais}

        except Exception as e:
            browser.close()
            return {"sucesso": False, "erro": str(e)}