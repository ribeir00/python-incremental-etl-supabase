import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import os
import json
load_dotenv()
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
PATH_DATA = os.getenv("PATH_DATA","./dados")
os.makedirs(PATH_DATA, exist_ok=True)
supabase = create_client(URL,KEY)
response_rpc= supabase.rpc("get_tables").execute()
names = [item['table_name'] for item in response_rpc.data if item ['table_name'] != 'controle_extracao']
final_table = {}
for name in names:
    nome_arquivo = os.path.join(PATH_DATA, f"{name}_historico.json")
    if not os.path.exists(nome_arquivo):
        data_referencia = "1900-01-01T00:00:00+00"
    else:
        res_controle = supabase.table("controle_extracao").select("ultima_atualizacao").eq("nome_tabela", name).execute()
        if len(res_controle.data) > 0:
            data_referencia = res_controle.data[0]['ultima_atualizacao']
        else:
            data_referencia = "1900-01-01T00:00:00+00"
    res = supabase.table(name).select("*").gt("created_at", data_referencia).execute()
    if res.data:
        historico_completo = []
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                historico_completo = json.load(f)      
        historico_completo.extend(res.data)
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(historico_completo, f, ensure_ascii=False, indent=4)
        df_novos = pd.DataFrame(res.data)
        nova_data_max = df_novos['created_at'].max()
        supabase.table("controle_extracao").upsert({
            "nome_tabela": name, 
            "ultima_atualizacao": str(nova_data_max)
        }).execute()
        print(f"✅ {name}: {len(res.data)} registos novos adicionados ao {nome_arquivo}.")
    else:
        print(f"⏸️ {name}: Sem novidades.")