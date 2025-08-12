from Sharepoint import SharePoint


def main():
    # Instancia a classe e faz as operações internas automaticamente
    sharepoint = SharePoint()

    # Upload de um arquivo
    # sharepoint.upload_file(r"C:\Users\BrunoFerreiradeSousa\Downloads\RC_UISA_MTUINOENTR101_19-11-24.pdf", "RC_UISA_MTUINOENTR101_19-11-24.pdf")
    # sharepoint.upload_file()
    # sharepoint.upload_file_onedrive(r"C:\Users\BrunoFerreiradeSousa\Downloads\RC_UISA_MTUINOENTR101_19-11-24.pdf", "Documents")
    
    # Primeiro caso de uso
    # sharepoint.upload_file("Paraty Tecnologia", "Documentos", "Teste", r"C:\Users\BrunoFerreiradeSousa\Downloads\Informe Energia - Semana 3 - Jan25.pdf", "Boleto_teste.pdf")

    # Segundo caso de uso
    #  sharepoint.upload_file("Paraty_Energia", "Comercializacao_e_Servicos", "Gestão de Clientes/Relatório de Medição - Novo/23-01-25", r"C:\Users\BrunoFerreiradeSousa\Downloads\Informe Energia - Semana 3 - Jan25.pdf", "Arquivo_teste.pdf", "Paraty_SP")

    # Delete primeiro caso de uso
    # sharepoint.delete_file("Paraty Tecnologia", "Documentos", "Teste", "Boleto_teste.pdf")

    # Delete segundo caso de uso
    # sharepoint.delete_file("Paraty_Energia", "Comercializacao_e_Servicos", "Gestão de Clientes", "Informe Energia - Semana 3 - Jan25.pdf", "Paraty_SP")

    # Download primeiro caso
    # sharepoint.download_file("Paraty Tecnologia", "Documentos", "Teste", r"C:\Users\BrunoFerreiradeSousa\Downloads", "Teste.xlsx")

    # Download segundo caso
    # sharepoint.download_file("Paraty_Energia", "Comercializacao_e_Servicos", "Gestão de Clientes", r"C:\Users\BrunoFerreiradeSousa\Downloads", "Senhas sites e cadastros.docx", "Paraty_SP")

    # Upload onedrive 
    # sharepoint.upload_file_onedrive("bruno.ferreira@paratyenergia.com.br", r"C:\Users\BrunoFerreiradeSousa\Downloads\Informe Energia - Semana 3 - Jan25.pdf", "Teste.pdf")

    # Download onedrive
    # sharepoint.download_file_onedrive("bruno.ferreira@paratyenergia.com.br", "Documentos/Teste.pdf", r"C:\Users\BrunoFerreiradeSousa\Downloads", "Teste.pdf")

    # Create item list
    # sharepoint.create_item_list("Paraty Tecnologia", "Teste", {"Title": "valor", "Coluna2": "valor"})

    # Read item list
    # print(sharepoint.read_list("Paraty Tecnologia", "Teste"))

    # Update item list
    # sharepoint.update_item_list("Paraty Tecnologia", "Teste", 5, {"Title": "Valor new", "Coluna2": "Valor new2"})

    # Delete item list
    # sharepoint.delete_item_list("Paraty Tecnologia", "Teste", 7)
    
    # Teste
    # sharepoint.list_files_sharepoint("Paraty_Energia", "Geracao_e_BusDev", "0. Mascarenhas/Regulatório e Comercialização", subsite_name="Paraty_SP")

    # Envio de email
    sharepoint.email_send(destinatario="brunoferreiraj3@gmail.com", cc="bruno.ferreira@paratyenergia.com.br", assunto="Teste", corpo_html="<p>Nenhum</p>", caixa_saida="bruno.ferreira@paratyenergia.com.br", anexos=r"C:\Users\BrunoFerreiradeSousa\Downloads\Informe Energia - Semana 3 - Fev25.pdf, C:\Users\BrunoFerreiradeSousa\Downloads\Paraty NFe 2001.pdf")
    

if __name__ == "__main__":
    main()

