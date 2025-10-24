# main.py
from analyzer_pdf import process_pdf  # função que processa PDFs e retorna lista de veículos
import sqlite3
import os

# Caminho do banco de dados
DB_PATH = r"C:\Users\prisc\OneDrive - tce.mg.gov.br\Projeto_Manuais_Automotivos_IA\data_output\FichasTecnicas.db"

# Função para criar conexão com SQLite
def create_connection():
    # Garante que a pasta 'data' exista
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

# Função para salvar um veículo no banco
def save_vehicle(vehicle):
    conn = create_connection()
    cursor = conn.cursor()

    # Cria a tabela caso não exista
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT,
            modelo TEXT,
            ano INTEGER,
            manual_url TEXT,
            site_url TEXT,
            imagem_urls TEXT
        )
    """)

    # Insere os dados do veículo
    cursor.execute("""
        INSERT INTO veiculos (marca, modelo, ano, manual_url, site_url, imagem_urls)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        vehicle['marca'],
        vehicle['modelo'],
        vehicle['ano'],
        vehicle['manual_url'],
        vehicle['site_url'],
        vehicle['imagem_urls']
    ))

    conn.commit()
    conn.close()

def main():
    print("Iniciando o processamento de PDFs...")

    # Processa os PDFs e retorna lista de veículos
    vehicles = process_pdf()  

    # Salva cada veículo no banco
    for vehicle in vehicles:
        save_vehicle(vehicle)

    print(f"Processamento concluído! {len(vehicles)} veículos salvos no banco.")

if __name__ == "__main__":
    main()

