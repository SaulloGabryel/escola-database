from flask import Blueprint
from controllers.cursos_controller import listar, buscar, criar, atualizar, deletar
from controllers.matriculas_controller import alunos_do_curso

cursos_bp = Blueprint('cursos', __name__)

cursos_bp.route('/', methods=['GET'])(listar)
cursos_bp.route('/<int:curso_id>', methods=['GET'])(buscar)
cursos_bp.route('/', methods=['POST'])(criar)
cursos_bp.route('/<int:curso_id>', methods=['PUT'])(atualizar)
cursos_bp.route('/<int:curso_id>', methods=['DELETE'])(deletar)
cursos_bp.route('/<int:curso_id>/alunos', methods=['GET'])(alunos_do_curso)
