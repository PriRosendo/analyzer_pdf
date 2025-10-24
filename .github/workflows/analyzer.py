import sqlite3
import requests
from datetime import datetime
from pathlib import Path
import fitz  # PyMuPDF

DB_PATH = r"C:\Users\prisc\OneDrive - tce.mg.gov.br\Projeto_Manuais_Automotivos_IA\data_output\FichasTecnicas.db"
PDF_FOLDER = r"C:\Users\prisc\OneDrive - tce.mg.gov.br\Projeto_Manuais_Automotivos_IA\data_output\PDFs"

# Garantir que a pasta exista
Path(PDF_FOLDER).mkdir(parents=True, exist_ok=True)

def get_veiculos_para_processar():
    """Retorna os veículos cujo data_processamento ainda está vazio"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verifica se a coluna data_processamento existe, se não cria
    cursor.execute("PRAGMA table_info(veiculos)")
    colunas = [col[1] for col in cursor.fetchall()]
    if "data_processamento" not in colunas:
        cursor.execute("ALTER TABLE veiculos ADD COLUMN data_processamento TEXT")
        conn.commit()

    # Seleciona veículos que ainda não foram processados
    cursor.execute("""
        SELECT id, marca, modelo, ano, manual_url
        FROM veiculos
        WHERE data_processamento IS NULL OR data_processamento = ''
    """)
    veiculos = cursor.fetchall()
    conn.close()
    return veiculos

def baixar_pdf(url, vehicle_id):
    """Faz download do PDF da URL e salva localmente"""
    if not url or url.lower() == "não aplicável nesta etapa":
        print(f"Veículo {vehicle_id}: sem URL de PDF")
        return None

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        pdf_path = Path(PDF_FOLDER) / f"{vehicle_id}.pdf"
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        print(f"PDF baixado: {pdf_path}")
        return str(pdf_path)
    except requests.RequestException as e:
        print(f"Erro ao baixar PDF do veículo {vehicle_id}: {e}")
        return None

def extrair_texto_pdf(pdf_path):
    """Extrai todo o texto do PDF usando PyMuPDF"""
    texto_completo = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            texto_completo += page.get_text("text") + "\n"
        doc.close()
        return texto_completo
    except Exception as e:
        print(f"Erro ao extrair texto do PDF {pdf_path}: {e}")
        return None

def atualizar_data_processamento(vehicle_id):
    """Marca o veículo como processado no banco"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE veiculos SET data_processamento = ? WHERE id = ?", (agora, vehicle_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    veiculos = get_veiculos_para_processar()
    print(f"{len(veiculos)} veículos para processar")

    for vehicle in veiculos:
        vehicle_id, marca, modelo, ano, manual_url = vehicle
        print(f"\nProcessando veículo {marca} {modelo} ({ano}) - ID {vehicle_id}")

        pdf_path = baixar_pdf(manual_url, vehicle_id)
        if not pdf_path:
            continue

        texto_pdf = extrair_texto_pdf(pdf_path)
        if texto_pdf:
            print(f"Texto extraído do PDF (primeiros 500 caracteres):\n{texto_pdf[:500]}")

            # =========================
            # Aqui você integraria o ML clássico para extrair os campos desejados
            # Por exemplo: potencia, torque, cilindradas, numero de portas, etc.
            # =========================

            # Atualiza data de processamento no banco
            atualizar_data_processamento(vehicle_id)
            print(f"Veículo {vehicle_id} marcado como processado.\n")
