import zmq
import json
from time import sleep
from const import *

def server():
  # A lista agora é o estado mantido pelo servidor
  values = []
  context = zmq.Context()
  socket  = context.socket(zmq.REP)       # create reply socket
  socket.bind("tcp://*:"+ PORT)            # bind socket to address
  print(f"Servidor ZMQ iniciado na porta: {PORT}")

  while True:
    message = socket.recv()               # wait for incoming message
    
    try:
      # Decodifica a mensagem de bytes para string e depois para JSON
      data = json.loads(message.decode())
      command = data.get("command")
      args = data.get("args", [])
      
      print(f"Recebido comando: {command} com args: {args}")

      reply_data = {}

      # Lógica de roteamento dos comandos
      if command == "append":
        values.append(args[0])
        reply_data = {"status": "ok", "result": values}

      elif command == "insert":
        values.insert(args[0], args[1])
        reply_data = {"status": "ok", "result": values}

      elif command == "remove":
        try:
          values.remove(args[0])
          reply_data = {"status": "ok", "result": values}
        except ValueError:
          reply_data = {"status": "error", "message": "Valor nao encontrado"}

      elif command == "search":
        try:
          index = values.index(args[0])
          reply_data = {"status": "ok", "result": index}
        except ValueError:
          reply_data = {"status": "ok", "result": -1}

      elif command == "sort":
        reverse = args[0] if args else False
        values.sort(reverse=reverse)
        reply_data = {"status": "ok", "result": values}

      elif command == "values":
        reply_data = {"status": "ok", "result": values}

      elif command == "STOP":
        print("Servidor recebendo comando STOP.")
        reply_data = {"status": "ok", "message": "Servidor parando"}
        socket.send(json.dumps(reply_data).encode())
        break # Sai do loop
        
      else:
        reply_data = {"status": "error", "message": "Comando desconhecido"}

      # Codifica a resposta de JSON para string e depois para bytes
      socket.send(json.dumps(reply_data).encode())

    except json.JSONDecodeError:
      print("Erro: Mensagem invalida (nao e JSON).")
      reply = {"status": "error", "message": "Requisicao invalida"}
      socket.send(json.dumps(reply).encode())

  # Limpeza
  print("Servidor encerrado.")
  socket.close()
  context.term()

if __name__ == "__main__":
    server()
