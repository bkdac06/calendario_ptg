import csv
from ics import Calendar, Event, Attendee, Organizer
from datetime import datetime

def converter_csv_para_ics_detalhado(arquivo_csv, arquivo_ics):
    """
    Converte um arquivo CSV com informações detalhadas de eventos 
    para um arquivo ICS, incluindo organizador, convidados e categorias.
    """
    c = Calendar()

    with open(arquivo_csv, 'r', encoding='utf-8-sig') as f:
        # CORREÇÃO 1: Adicionado o delimitador ';'
        reader = csv.DictReader(f, delimiter=';') 
        
        for row in reader:
            e = Event()
            
            # Os nomes das colunas estão corretos conforme seu arquivo
            e.name = row['Titulo']
            
            # CORREÇÃO 2: Ajustado o formato da data para corresponder ao CSV
            formato_data = '%Y-%m-%d %H:%M:%S'  #'%d/%m/%Y %H:%M' 
            e.begin = datetime.strptime(row['Data Inicio'], formato_data)
            e.end = datetime.strptime(row['Data Fim'], formato_data)
            
            e.description = row.get('Descrição', '')
            
            # Adiciona o Organizador (usando o cabeçalho 'Organizador E-mail' do seu arquivo)
            #if row.get('Organizador E-mail'):
            #    e.organizer = Organizer(
            #        common_name=row.get('Organizador Nome', ''),
            #        email=row['Organizador E-mail']
            #    )
            
            # Adiciona os Convidados (Attendees)
            #if row.get('convidados_email'):
            #    emails_convidados = row['convidados_email'].split(';')
            #    for email in emails_convidados:
            #        if email.strip(): 
            #            e.add_attendee(Attendee(email=email.strip()))

            # Adiciona as Categorias
            if row.get('Categorias'):
                # Remove aspas se existirem
                categorias_limpas = row['Categorias'].strip('"')
                e.categories = set(categorias_limpas.split(';'))

            c.events.add(e)

    with open(arquivo_ics, 'w', encoding='utf-8') as f:
        f.writelines(c)

# Exemplo de uso
if __name__ == "__main__":
    nome_arquivo_csv = 'noven_completo.csv'
    nome_arquivo_ics = 'calendario_noven.ics'
    
    converter_csv_para_ics_detalhado(nome_arquivo_csv, nome_arquivo_ics)
    
    print(f"Arquivo '{nome_arquivo_ics}' criado com sucesso a partir de '{nome_arquivo_csv}'!")
    
    nome_arquivo_csv = 'noven_desenvolvimento.csv'
    nome_arquivo_ics = 'calendario_noven_desenvolvimento.ics'
    
    converter_csv_para_ics_detalhado(nome_arquivo_csv, nome_arquivo_ics)
    
    print(f"Arquivo '{nome_arquivo_ics}' criado com sucesso a partir de '{nome_arquivo_csv}'!")
