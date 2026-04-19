from flask import Blueprint
from controllers.alunos_controller import listar, buscar, criar, atualizar, deletar

alunos_bp = Blueprint('alunos', __name__)

alunos_bp.route('/', methods=['GET'])(listar)
alunos_bp.route('/<int:aluno_id>', methods=['GET'])(buscar)
alunos_bp.route('/', methods=['POST'])(criar)
alunos_bp.route('/<int:aluno_id>', methods=['PUT'])(atualizar)
alunos_bp.route('/<int:aluno_id>', methods=['DELETE'])(deletar)
