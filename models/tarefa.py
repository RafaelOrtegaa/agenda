from models.database import Database
from typing import Self, Any
from sqlite3 import Cursor


class Tarefa:
    def __init__(self: Self, titulo_tarefa: str = None, data_conclusao: str = None, id_tarefa: int = None) -> None:
        self.titulo_tarefa: str = titulo_tarefa
        self.data_conclusao: str = data_conclusao
        self.id_tarefa: int = id_tarefa
    

    # Sem o conceito de sobrecarga
    # Tarefa(titulo_tarefa="Nova tarefa")
    # Tarefa(titulo_tarefa="Outra tarefa", data_conclusao="2026-02-03")
    # Tarefa(id_tarefa=1)

    @classmethod
    def id(cls, id: int):
        with Database('./data/tarefas.sqlite3') as db:
            query: str = 'SELECT titulo_tarefa, data_conclusao FROM tarefas WHERE id = ?;'
            params: tuple = (id,)
            resultado = db.buscar_tudo(query, params)
            # resultado = [["titulo_tarefa", "data_conclusao"]]

            # Desempacotamento de coleção
            [[titulo, data]] = resultado

        return cls(id_tarefa=id, titulo_tarefa=titulo, data_conclusao=data)
    
    # Simulando o conceito de sobrecarga
    # Tarefa('Título da Tarefa')
    # Tarefa('Título da Tarefa', '2026-02-03')
    # Tarefa.id_tarefa(1)

    def salvar_tarefa(self: Self) -> None:
        with Database('./data/tarefas.sqlite3') as db:
            query: str = "INSERT INTO tarefas (titulo_tarefa, data_conclusao) VALUES (?, ?);"
            params: tuple = (self.titulo_tarefa, self.data_conclusao)
            db.executar(query, params)

    @staticmethod
    def obter_tarefas() -> list[Self]:
        with Database('./data/tarefas.sqlite3') as db:
            query: str = 'SELECT titulo_tarefa, data_conclusao FROM tarefas;'
            resultados: list[Any] = db.buscar_tudo(query)
            tarefas: list[Self] = [Tarefa(titulo, data) for titulo, data in resultados]
            return tarefas
        
    def excluir_tarefa(self) -> Cursor:
        with Database('./data/tarefas.sqlite3') as db:
            query: str = 'DELETE FROM tarefas WHERE id = ?;'
            params: tuple = (self.id_tarefa,)
            resultado: Cursor = db.executar(query, params)
            return resultado 
    