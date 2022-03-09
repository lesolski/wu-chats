# project/main/routes.py

from flask import Blueprint, render_template, send_from_directory, request, current_app
from project.models import FAQs, News

main = Blueprint('main', __name__)

@main.route('/')
def home():
	return render_template('home.html')

@main.route('/news')
def news():
	news = News.query.order_by(News.published_at.desc()).all()
	return render_template('news.html', news=news)

@main.route('/faqs_links')
def faq():

	faqs = FAQs.query.all()
	return render_template('faq_links.html', faqs=faqs)

@main.route('/robots.txt')
@main.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])