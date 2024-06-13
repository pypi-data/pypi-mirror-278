import json
from os import getcwd, makedirs, path
from hnt_sap_gui import SapGui
from nf_jira import *

def test_homolog():

    with open("./devdata/json/expected_homolog.json", "r", encoding="utf-8") as nota_pedido_arquivo_json: data = json.load(nota_pedido_arquivo_json)

    result = SapGui().hnt_run_transaction(data) if "nota_pedido" in data else SapGui().hnt_run_transaction_FV60(data['fatura'])
    print(result)
    assert result is not None