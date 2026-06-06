import xml.etree.ElementTree as ET
import unicodedata
import datetime
import os

def parse_horario(row):
    horarios_texto: list[str] = []
    horarios_formatado: list[dict] = []
    if row[12].text:
        horarios_texto.append(row[12].text.strip())
    for sub in row[12]:
        if sub.tail:
            horarios_texto.append(sub.tail.strip())

    for h_texto in horarios_texto:
        dia_num = h_texto[0]
        hora_raw = h_texto[2:6]
        creditos_num = h_texto[7]

        hora_format = f"{hora_raw[:2]}:{hora_raw[2:]}"

        horarios_formatado.append({
            "dia_semana": int(dia_num),
            "hora": hora_format,
            "creditos": int(creditos_num)
        })


    return horarios_formatado

    

def parse_to_dict(xml_files: list[str]):
    agora = datetime.datetime.now().strftime('"%d/%m/%y - %H:%M"')
    resultado = {"ultima_atualizacao": agora, "campi":{}}


    for filename in xml_files:
        # Pega os 3 últimos caracteres do nome do arquivo (ex: campus)
        chave_campus = os.path.basename(filename).split('_')[1].replace('.xml', '')
        resultado["campi"][chave_campus] = dict()
        try:
            with open(filename, "r", encoding="utf-8", errors="ignore") as inf:
                content = inf.read()
        except FileNotFoundError:
            print(f"Erro: Arquivo {filename} não encontrado.")
            continue

        # Split para lidar com múltiplos documentos XML concatenados
        split = content.split('<?xml version="1.0"?>')
        
        prev_codigo = None
        cur_materia = dict()
        materias = dict()

        for xml_str in split:
            if not xml_str.strip():
                continue
            
            try:
                # ET.fromstring aceita a string XML diretamente
                root = ET.fromstring(xml_str)
                # A estrutura de índices [1][1][2] foi mantida conforme o original
                # mas é sensível a mudanças no layout do CAGR
                rows = root[1][1][2]
            except (ET.ParseError, IndexError):
                continue

            for row in rows:
                codigo_disciplina = row[3].text
                nome_turma = row[4].text

                # Nome da disciplina e tratamento de <br />
                nome_disciplina = row[5].text if row[5].text else ""
                for sub in row[5]:
                    if sub.tail:
                        nome_disciplina = nome_disciplina + " " + sub.tail
                nome_disciplina = nome_disciplina.strip()

                horas_aula = int(row[6].text or 0)
                vagas_ofertadas = int(row[7].text or 0)
                vagas_ocupadas = int(row[8].text or 0)
                alunos_especiais = int(row[9].text or 0)
                
                try:
                    saldo_vagas = int(row[10].text or 0)
                except (TypeError, ValueError):
                    saldo_vagas = 0
                
                try:
                    pedidos_sem_vaga = int(row[11].text or 0)
                except (TypeError, ValueError):
                    pedidos_sem_vaga = 0

                horarios = parse_horario(row)

                professores = []
                if len(row[13]) > 0:
                    if not row[13][0].text and row[13].text:
                        professores.append(row[13].text.strip())
                
                for sub in row[13]:
                    if sub.attrib and sub.text: # Geralmente tags <a>
                        professores.append(sub.text.strip())
                    elif sub.tail:
                        professores.append(sub.tail.strip())

                if codigo_disciplina != prev_codigo:
                    # Normalização para ASCII (busca sem acentos)
                    nome_norm = unicodedata.normalize("NFKD", nome_disciplina)
                    nome_disciplina_ascii = nome_norm.encode("ascii", "ignore").decode("ascii")
                    
                    cur_materia = {
                        "codigo_disciplina": codigo_disciplina,
                        "nome_disciplina_ascii": nome_disciplina_ascii.upper(),
                        "nome_disciplina": nome_disciplina,
                        "turmas": [],
                    }
                    materias[codigo_disciplina] = cur_materia
                    prev_codigo = codigo_disciplina
                
                turma = {
                    "nome_turma": nome_turma,
                    "horas_aula": horas_aula,
                    "vagas_ofertadas": vagas_ofertadas,
                    "vagas_ocupadas": vagas_ocupadas,
                    "alunos_especiais": alunos_especiais,
                    "saldo_vagas": saldo_vagas,
                    "pedidos_sem_vaga": pedidos_sem_vaga,
                    "horarios": horarios,
                    "professores": professores,
                }
                cur_materia['turmas'].append(turma)

        resultado["campi"][chave_campus] = materias
    
    return resultado

        