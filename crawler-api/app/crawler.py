import sys
import gzip
import io
import os
from urllib import request, parse
from http import cookiejar
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup


def find_id(xml_elem, target_id):
    for x in xml_elem:
        if x.get("id") == target_id:
            return x
        y = find_id(x, target_id)
        if y is not None:
            return y
    return None

def go_on(xml_elem):
    scroller = find_id(xml_elem, "formBusca:dataScroller1_table")
    if scroller is None:
        return False
    try:
        # Acessando a estrutura do scroller (ajuste conforme a estrutura do XML retornado)
        for x in scroller[0][0]:
            onclick = x.get("onclick")
            if onclick and "next" in onclick:
                return True
    except (IndexError, TypeError):
        pass
    return False


def fetch_data (semestre: str, output_path: str):
    # Configuração do CookieJar e Opener para Python 3
    jar = cookiejar.CookieJar()
    opener = request.build_opener(
        request.HTTPCookieProcessor(jar), 
        request.HTTPSHandler(debuglevel=0)
    )

    # Primeira requisição para pegar o ViewState
    url_base = "https://cagr.sistemas.ufsc.br/modules/comunidade/cadastroTurmas/"
    with opener.open(url_base) as resp:
        soup = BeautifulSoup(resp.read(), features="html.parser")
        view_state_element = soup.find("input", {"name": "javax.faces.ViewState"})
        if not view_state_element:
            print("Erro: Não foi possível encontrar o ViewState.")
            sys.exit(1)
        viewState = view_state_element["value"]

    url_action = "https://cagr.sistemas.ufsc.br/modules/comunidade/cadastroTurmas/index.xhtml"

    # Dados do formulário
    page_form = {
        "AJAXREQUEST": "_viewRoot",
        "formBusca:selectSemestre": semestre,
        "formBusca:selectDepartamento": "",
        "formBusca:selectCampus": "1",
        "formBusca:selectCursosGraduacao": "0",
        "formBusca:codigoDisciplina": "",
        "formBusca:j_id135_selection": "",
        "formBusca:filterDisciplina": "",
        "formBusca:j_id139": "",
        "formBusca:j_id143_selection": "",
        "formBusca:filterProfessor": "",
        "formBusca:selectDiaSemana": "0",
        "formBusca:selectHorarioSemana": "",
        "formBusca": "formBusca",
        "autoScroll": "",
        "javax.faces.ViewState": viewState,
        "formBusca:dataScroller1": "1",
        "AJAX:EVENTS_COUNT": "1",
    }

    arquivos_gerados = []
    campus_str = ["EaD", "FLO", "JOI", "CBS", "ARA"]
    if semestre >= "20141":
        campus_str.append("BLN")

    for campus_idx in range(1, len(campus_str)):
        campus_nome = campus_str[campus_idx]
        print(f"campus {campus_nome}")
        
        filename = os.path.join(output_path, f"{semestre}_{campus_nome}.xml")
        with open(filename, "w", encoding="utf-8") as outfile:
            page_form["formBusca:selectCampus"] = str(campus_idx)
            pagina = 1
            
            while True:
                page_form["formBusca:dataScroller1"] = str(pagina)
                
                # Codificar dados para POST
                data_encoded = parse.urlencode(page_form).encode("utf-8")
                req = request.Request(url_action, data=data_encoded)
                req.add_header("Accept-encoding", "gzip")
                
                with opener.open(req) as resp:
                    raw_data = resp.read()
                    
                    if resp.info().get("Content-Encoding") == "gzip":
                        with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as f:
                            data_bytes = f.read()
                    else:
                        data_bytes = raw_data

                # Decodificar para string para salvar no arquivo
                data_str = data_bytes.decode("utf-8", errors="ignore")
                outfile.write(data_str)
                
                # Parser XML
                # Nota: O suporte a entidades HTML no ET.XMLParser mudou no Python 3.
                # Se o XML for complexo, BeautifulSoup ou lxml seriam melhores, 
                # mas mantendo a lógica original:
                try:
                    xml_root = ET.fromstring(data_bytes)
                    if not go_on(xml_root):
                        break
                except ET.ParseError:
                    # Caso o XML venha malformado devido a entidades
                    break
                    
                pagina += 1

        arquivos_gerados.append(filename)

    return arquivos_gerados
