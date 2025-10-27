import zmq
import json
from const import *

def main():
  context = zmq.Context()
  socket  = context.socket(zmq.REQ)       # create request socket

  # Corrigido: Adicionado ":" entre HOST e PORT
  connection_string = "tcp://" + HOST + ":" + PORT
  socket.connect(connection_string) 
  print(f"Cliente conectado a {connection_string}")

  # Função helper para enviar comandos JSON e receber respostas JSON
  def send_request(command, args=None):
    if args is None:
        args = []
    
    request_data = {"command": command, "args": args}
    # Envia o JSON como bytes
    socket.send(json.dumps(request_data).encode())
    
    # Recebe a resposta em bytes e converte para JSON
    reply_bytes = socket.recv()
    return json.loads(reply_bytes.decode())

  # --- Início dos Testes Interativos ---

  print("--- LISTA INICIAL ---")
  response = send_request("values")
  print("Lista atual:", response.get("result", "Erro"))

  # 1. Teste de APPEND
  print("\n--- 1. Teste de APPEND ---")
  value = int(input("Valor para adicionar (append): "))
  response = send_request("append", [value])
  print("Lista apos append:", response.get("result", "Erro"))

  # 2. Teste de INSERT
  print("\n--- 2. Teste de INSERT ---")
  insert_value = int(input("Valor para inserir: "))
  insert_index = int(input("Indice para inserir: "))
  response = send_request("insert", [insert_index, insert_value])
  print("Lista apos insert:", response.get("result", "Erro"))

  # 3. Teste de SEARCH
  print("\n--- 3. Teste de SEARCH ---")
  search_value = int(input("Valor para pesquisar: "))
  response = send_request("search", [search_value])
  result_index = response.get("result", -1)
  if result_index != -1:
    print(f"Valor {search_value} encontrado no indice: {result_index}")
  else:
    print(f"Valor {search_value} nao encontrado.")

  # 4. Teste de SORT
  print("\n--- 4. Teste de SORT ---")
  response = send_request("sort") # Ordena crescentemente
  print("Lista apos sort (crescente):", response.get("result", "Erro"))
  response = send_request("sort", [True]) # Ordena decrescentemente
  print("Lista apos sort (decrescente):", response.get("result", "Erro"))

  # 5. Teste de REMOVE
  print("\n--- 5. Teste de REMOVE ---")
  remove_value = int(input("Valor para remover: "))
  response = send_request("remove", [remove_value])
  if response.get("status") == "ok":
    print(f"Valor {remove_value} removido com sucesso.")
    print("Lista apos remove:", response.get("result", "Erro"))
  else:
    print(f"Erro: {response.get('message')}")

  # --- Fim dos Testes ---

  # Envia o comando para parar o servidor
  print("\n--- Parando o servidor ---")
  response = send_request("STOP")
  print(f"Resposta do servidor: {response.get('message')}")

  # Limpeza
  socket.close()
  context.term()

if __name__ == "__main__":
    main()
