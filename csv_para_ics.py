import csv
from ics import Calendar, Event, Attendee, Organizer
from datetime import datetime
from zoneinfo import ZoneInfo # <- 1. IMPORTAR ZONEINFO

def converter_csv_para_ics_detalhado(arquivo_csv, arquivo_ics):
    """
    Converte um arquivo CSV com informações detalhadas de eventos 
    para um arquivo ICS, incluindo organizador, convidados e categorias.
    """
    c = Calendar()
    
    # 2. DEFINIR O FUSO HORÁRIO DE BRASÍLIA
    fuso_horario_brasilia = ZoneInfo("America/Sao_Paulo")

    with open(arquivo_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';') 
        
        for row in reader:
            e = Event()
            
            e.name = row['Titulo']
            
            formato_data = '%Y-%m-%d %H:%M:%S'
            
            # Lê a data/hora como "ingênua" (sem fuso)
            inicio_ingenuo = datetime.strptime(row['Data Inicio'], formato_data)
            fim_ingenuo = datetime.strptime(row['Data Fim'], formato_data)
            
            # 3. ANEXA O FUSO HORÁRIO ÀS DATAS
            e.begin = inicio_ingenuo.replace(tzinfo=fuso_horario_brasilia)
            e.end = fim_ingenuo.replace(tzinfo=fuso_horario_brasilia)
            
            e.description = row.get('Descrição', '')
            
            if row.get('Organizador E-mail'):
                e.organizer = Organizer(
                    common_name=row.get('Organizador Nome', ''),
                    email=row['Organizador E-mail']
                )
            
            if row.get('convidados_email'):
                emails_convidados = row['convidados_email'].split(';')
                for email in emails_convidados:
                    if email.strip(): 
                        e.add_attendee(Attendee(email=email.strip()))

            if row.get('Categorias'):
                categorias_limpas = row['Categorias'].strip('"')
                e.categories = set(categorias_limpas.split(';'))

            c.events.add(e)

    with open(arquivo_ics, 'w', encoding='utf-8') as f:
        f.writelines(c)

# Exemplo de uso
if __name__ == "__main__":
    # Geração do primeiro calendário
    nome_arquivo_csv = 'noven_completo.csv'
    nome_arquivo_ics = 'calendario_noven.ics'
    converter_csv_para_ics_detalhado(nome_arquivo_csv, nome_arquivo_ics)
    print(f"Arquivo '{nome_arquivo_ics}' criado com sucesso a partir de '{nome_arquivo_csv}'!")
    
    # Geração do segundo calendário
    nome_arquivo_csv = 'noven_desenvolvimento.csv'
    nome_arquivo_ics = 'calendario_noven_desenvolvimento.ics'
    converter_csv_para_ics_detalhado(nome_arquivo_csv, nome_arquivo_ics)
    print(f"Arquivo '{nome_arquivo_ics}' criado com sucesso a partir de '{nome_arquivo_csv}'!")

    # Geração do terceiro calendário
    nome_arquivo_csv = 'patoge_verao.csv'
    nome_arquivo_ics = 'calendario_patoge.ics'
    converter_csv_para_ics_detalhado(nome_arquivo_csv, nome_arquivo_ics)
    print(f"Arquivo '{nome_arquivo_ics}' criado com sucesso a partir de '{nome_arquivo_csv}'!")
    
    # Geração do quarto calendário
    nome_arquivo_csv = 'patoge_desenvolvimento.csv'
    nome_arquivo_ics = 'calendario_patoge_desenvolvimento.ics'
    converter_csv_para_ics_detalhado(nome_arquivo_csv, nome_arquivo_ics)
    print(f"Arquivo '{nome_arquivo_ics}' criado com sucesso a partir de '{nome_arquivo_csv}'!")
