# database.py
import sqlite3

DB_PATH = r"C:\Users\prisc\OneDrive - tce.mg.gov.br\Projeto_Manuais_Automotivos_IA\data_output\FichasTecnicas.db"

def create_connection():
    return sqlite3.connect(DB_PATH)

def ensure_columns_exist():
    """
    Verifica se as colunas adicionais existem no banco.
    Se não existirem, cria cada uma.
    """
    novas_colunas = {
        "motor": "TEXT",
        "combustivel": "TEXT",
        "potencia_original": "TEXT",
        "potencia_cv": "REAL",
        "torque_original": "TEXT",
        "torque_kgfm": "REAL",
        "torque_nm": "REAL",
        "peso_kg": "REAL",
        "carga_util_kg": "REAL",
        "reboque_kg": "REAL",
        "tanque_l": "REAL",
        "porta_malas_original": "TEXT",
        "porta_malas_l": "REAL",
        "comprimento_mm": "REAL",
        "largura_mm": "REAL",
        "altura_mm": "REAL",
        "entre_eixos_mm": "REAL",
        "bateria_kwh": "REAL",
        "autonomia_km": "REAL",
        "manual_origem": "TEXT",
        "url_manual": "TEXT",
        "url_site": "TEXT",
        "url_imagem": "TEXT",
        "data_extracao": "TEXT",
        "ar_condicionado_automatico": "TEXT",
        "controle_tracao": "TEXT",
        "freios_abs": "TEXT",
        "airbags_laterais": "TEXT",
        "alarme": "TEXT",
        "vidros_travas_eletricas": "TEXT",
        "computador_de_bordo": "TEXT",
        "volante_ajuste_altura": "TEXT",
        "multimidia": "TEXT",
        "turbo": "TEXT",
        "direcao": "TEXT",
        "numero_lugares": "INTEGER",
        "numero_portas": "INTEGER",
        "tracao": "TEXT",
        "pneu": "TEXT",
        "transmissao": "TEXT",
        "cilindradas_cm3": "REAL",
        "tipo_veiculo": "TEXT",
        "data_processamento": "TEXT"
    }

    conn = create_connection()
    cursor = conn.cursor()

    # Busca colunas existentes
    cursor.execute("PRAGMA table_info(veiculos);")
    colunas_existentes = [col[1] for col in cursor.fetchall()]

    # Adiciona apenas as que não existem
    for coluna, tipo in novas_colunas.items():
        if coluna not in colunas_existentes:
            cursor.execute(f"ALTER TABLE veiculos ADD COLUMN {coluna} {tipo}")
            print(f"Coluna '{coluna}' criada.")

    conn.commit()
    conn.close()

def save_vehicle(vehicle):
    """
    Salva um veículo no banco. Garante que todas as colunas estejam presentes.
    """
    ensure_columns_exist()
    conn = create_connection()
    cursor = conn.cursor()

    # Gera dinamicamente as colunas e valores do dicionário
    colunas = []
    valores = []
    for chave, valor in vehicle.items():
        colunas.append(chave)
        valores.append(valor)

    colunas_str = ", ".join(colunas)
    placeholders = ", ".join(["?"] * len(valores))

    cursor.execute(f"INSERT INTO veiculos ({colunas_str}) VALUES ({placeholders})", valores)
    conn.commit()
    conn.close()
