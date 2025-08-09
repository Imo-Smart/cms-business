from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image

from src.models.user import User, db
from src.models.content import Page, Post, Category, Tag, Media, Setting

content_bp = Blueprint('content', __name__)

# Utilitários
def allowed_file(filename):
    """Verifica se o arquivo é permitido"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_slug(title):
    """Gera um slug a partir do título"""
    import re
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug.strip('-')

# ROTAS DE PÁGINAS
@content_bp.route('/pages', methods=['GET'])
def get_pages():
    """Listar todas as páginas"""
    try:
        pages = Page.query.order_by(Page.order_index, Page.created_at.desc()).all()
        return jsonify([page.to_dict() for page in pages]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/pages', methods=['POST'])
@jwt_required()
def create_page():
    """Criar nova página"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('title'):
            return jsonify({'error': 'Título é obrigatório'}), 400
        
        # Gerar slug se não fornecido
        slug = data.get('slug') or generate_slug(data['title'])
        
        # Verificar se slug já existe
        if Page.query.filter_by(slug=slug).first():
            return jsonify({'error': 'Slug já existe'}), 400
        
        page = Page(
            title=data['title'],
            slug=slug,
            content=data.get('content', ''),
            excerpt=data.get('excerpt', ''),
            meta_title=data.get('meta_title', ''),
            meta_description=data.get('meta_description', ''),
            featured_image=data.get('featured_image', ''),
            author_id=current_user_id,
            status=data.get('status', 'draft'),
            template=data.get('template', ''),
            order_index=data.get('order_index', 0),
            is_homepage=data.get('is_homepage', False)
        )
        
        if data.get('status') == 'published' and not page.published_at:
            page.published_at = datetime.utcnow()
        
        db.session.add(page)
        db.session.commit()
        
        return jsonify(page.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/pages/<int:page_id>', methods=['GET'])
def get_page(page_id):
    """Obter página específica"""
    try:
        page = Page.query.get_or_404(page_id)
        return jsonify(page.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/pages/<int:page_id>', methods=['PUT'])
@jwt_required()
def update_page(page_id):
    """Atualizar página"""
    try:
        page = Page.query.get_or_404(page_id)
        data = request.get_json()
        
        # Atualizar campos
        if 'title' in data:
            page.title = data['title']
        if 'slug' in data and data['slug'] != page.slug:
            # Verificar se novo slug já existe
            if Page.query.filter(Page.slug == data['slug'], Page.id != page_id).first():
                return jsonify({'error': 'Slug já existe'}), 400
            page.slug = data['slug']
        if 'content' in data:
            page.content = data['content']
        if 'excerpt' in data:
            page.excerpt = data['excerpt']
        if 'meta_title' in data:
            page.meta_title = data['meta_title']
        if 'meta_description' in data:
            page.meta_description = data['meta_description']
        if 'featured_image' in data:
            page.featured_image = data['featured_image']
        if 'status' in data:
            page.status = data['status']
            if data['status'] == 'published' and not page.published_at:
                page.published_at = datetime.utcnow()
        if 'template' in data:
            page.template = data['template']
        if 'order_index' in data:
            page.order_index = data['order_index']
        if 'is_homepage' in data:
            page.is_homepage = data['is_homepage']
        
        page.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(page.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/pages/<int:page_id>', methods=['DELETE'])
@jwt_required()
def delete_page(page_id):
    """Deletar página"""
    try:
        page = Page.query.get_or_404(page_id)
        db.session.delete(page)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ROTAS DE POSTS
@content_bp.route('/posts', methods=['GET'])
def get_posts():
    """Listar todos os posts"""
    try:
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return jsonify([post.to_dict() for post in posts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    """Criar novo post"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('title'):
            return jsonify({'error': 'Título é obrigatório'}), 400
        
        # Gerar slug se não fornecido
        slug = data.get('slug') or generate_slug(data['title'])
        
        # Verificar se slug já existe
        if Post.query.filter_by(slug=slug).first():
            return jsonify({'error': 'Slug já existe'}), 400
        
        post = Post(
            title=data['title'],
            slug=slug,
            content=data.get('content', ''),
            excerpt=data.get('excerpt', ''),
            meta_title=data.get('meta_title', ''),
            meta_description=data.get('meta_description', ''),
            featured_image=data.get('featured_image', ''),
            author_id=current_user_id,
            category_id=data.get('category_id'),
            status=data.get('status', 'draft'),
            is_featured=data.get('is_featured', False),
            allow_comments=data.get('allow_comments', True)
        )
        
        if data.get('status') == 'published' and not post.published_at:
            post.published_at = datetime.utcnow()
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify(post.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Obter post específico"""
    try:
        post = Post.query.get_or_404(post_id)
        # Incrementar contador de visualizações
        post.view_count += 1
        db.session.commit()
        return jsonify(post.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """Atualizar post"""
    try:
        post = Post.query.get_or_404(post_id)
        data = request.get_json()
        
        # Atualizar campos
        if 'title' in data:
            post.title = data['title']
        if 'slug' in data and data['slug'] != post.slug:
            # Verificar se novo slug já existe
            if Post.query.filter(Post.slug == data['slug'], Post.id != post_id).first():
                return jsonify({'error': 'Slug já existe'}), 400
            post.slug = data['slug']
        if 'content' in data:
            post.content = data['content']
        if 'excerpt' in data:
            post.excerpt = data['excerpt']
        if 'meta_title' in data:
            post.meta_title = data['meta_title']
        if 'meta_description' in data:
            post.meta_description = data['meta_description']
        if 'featured_image' in data:
            post.featured_image = data['featured_image']
        if 'category_id' in data:
            post.category_id = data['category_id']
        if 'status' in data:
            post.status = data['status']
            if data['status'] == 'published' and not post.published_at:
                post.published_at = datetime.utcnow()
        if 'is_featured' in data:
            post.is_featured = data['is_featured']
        if 'allow_comments' in data:
            post.allow_comments = data['allow_comments']
        
        post.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(post.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """Deletar post"""
    try:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ROTAS DE CATEGORIAS
@content_bp.route('/categories', methods=['GET'])
def get_categories():
    """Listar todas as categorias"""
    try:
        categories = Category.query.order_by(Category.name).all()
        return jsonify([category.to_dict() for category in categories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    """Criar nova categoria"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        # Gerar slug se não fornecido
        slug = data.get('slug') or generate_slug(data['name'])
        
        # Verificar se slug já existe
        if Category.query.filter_by(slug=slug).first():
            return jsonify({'error': 'Slug já existe'}), 400
        
        category = Category(
            name=data['name'],
            slug=slug,
            description=data.get('description', ''),
            parent_id=data.get('parent_id')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify(category.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ROTAS DE UPLOAD
@content_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    """Upload de arquivos"""
    try:
        current_user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and allowed_file(file.filename):
            # Gerar nome único para o arquivo
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # Salvar arquivo
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Obter informações do arquivo
            file_size = os.path.getsize(file_path)
            mime_type = file.content_type
            
            # Se for imagem, obter dimensões
            width = height = None
            if mime_type and mime_type.startswith('image/'):
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                except Exception:
                    pass
            
            # Salvar no banco de dados
            media = Media(
                filename=unique_filename,
                original_name=filename,
                file_path=f"/uploads/{unique_filename}",
                file_size=file_size,
                mime_type=mime_type,
                width=width,
                height=height,
                uploaded_by=current_user_id
            )
            
            db.session.add(media)
            db.session.commit()
            
            return jsonify(media.to_dict()), 201
        
        return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/media', methods=['GET'])
@jwt_required()
def get_media():
    """Listar arquivos de mídia"""
    try:
        media_files = Media.query.order_by(Media.created_at.desc()).all()
        return jsonify([media.to_dict() for media in media_files]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

