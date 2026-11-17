from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models import Project

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('index.html', projects=projects)


@main_bp.route('/projects', methods=['POST'])
def create_project():
    title = (request.form.get('title') or '').strip()
    description = (request.form.get('description') or '').strip()
    technologies = (request.form.get('technologies') or '').strip()
    url = (request.form.get('url') or '').strip()

    if not title or not description:
        flash('Title and description are required.', 'error')
        return redirect(url_for('main.index'))

    project = Project(
        title=title,
        description=description,
        technologies=technologies or 'Python',
        url=url or None,
    )

    db.session.add(project)
    db.session.commit()
    flash('Project added successfully.', 'success')
    return redirect(url_for('main.index'))


@main_bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.title = (request.form.get('title') or '').strip()
        project.description = (request.form.get('description') or '').strip()
        project.technologies = (request.form.get('technologies') or '').strip()
        project.url = (request.form.get('url') or '').strip() or None

        if not project.title or not project.description:
            flash('Title and description are required.', 'error')
            return redirect(url_for('main.edit_project', project_id=project.id))

        db.session.commit()
        flash('Project updated successfully.', 'success')
        return redirect(url_for('main.index'))

    return render_template('edit.html', project=project)


@main_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully.', 'success')
    return redirect(url_for('main.index'))
