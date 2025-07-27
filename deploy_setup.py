"""
Script de configuration pour le déploiement sur Vercel
"""
import os
import subprocess
import sqlite3
from pathlib import Path

def setup_for_deployment():
    """Prépare le projet pour le déploiement"""
    print("🚀 Configuration pour le déploiement Vercel...")
    
    # Créer les répertoires nécessaires
    static_build_dir = Path('staticfiles_build')
    static_build_dir.mkdir(exist_ok=True)
    
    media_dir = static_build_dir / 'media'
    media_dir.mkdir(exist_ok=True)
    
    static_dir = static_build_dir / 'static'
    static_dir.mkdir(exist_ok=True)
    
    print("✅ Répertoires créés")
    
    # Créer la base de données et les migrations
    try:
        print("📊 Application des migrations...")
        subprocess.run(['python', 'manage.py', 'makemigrations'], check=True)
        subprocess.run(['python', 'manage.py', 'migrate'], check=True)
        print("✅ Migrations appliquées")
        
        # Collecter les fichiers statiques
        print("📁 Collection des fichiers statiques...")
        subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("✅ Fichiers statiques collectés")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la configuration: {e}")
        return False
    
    print("🎉 Configuration terminée avec succès!")
    return True

def create_sample_data():
    """Crée des données d'exemple pour le portfolio"""
    print("📝 Création de données d'exemple...")
    
    # Importer Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
    import django
    django.setup()
    
    from portfolio.models import Profile, Project, Skill, Experience
    
    try:
        # Créer le profil
        profile, created = Profile.objects.get_or_create(
            defaults={
                'name': 'Cheikhna Ely Cheikh Ndiaye',
                'title': 'Développeur Fullstack',
                'bio': 'Développeur passionné avec une expertise en Django, React et technologies modernes.',
                'location': 'France',
                'email': 'cheikhna.ndiaye1@gmail.com',
                'linkedin_url': 'https://www.linkedin.com/in/cheikhna-ndiaye-ba0007163',
                'github_url': 'https://github.com/Ely724',
                'is_available_for_work': True,
            }
        )
        
        if created:
            print("✅ Profil créé")
        
        # Créer quelques compétences
        skills_data = [
            {'name': 'Python', 'category': 'backend', 'proficiency': 90},
            {'name': 'Django', 'category': 'backend', 'proficiency': 85},
            {'name': 'JavaScript', 'category': 'frontend', 'proficiency': 80},
            {'name': 'React', 'category': 'frontend', 'proficiency': 75},
            {'name': 'HTML/CSS', 'category': 'frontend', 'proficiency': 90},
            {'name': 'PostgreSQL', 'category': 'database', 'proficiency': 80},
        ]
        
        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
            if created:
                print(f"✅ Compétence '{skill.name}' créée")
        
        # Créer un projet d'exemple
        project, created = Project.objects.get_or_create(
            title="Portfolio Django",
            defaults={
                'short_description': 'Portfolio moderne avec Django et Tailwind CSS',
                'description': 'Un portfolio complet développé avec Django, intégrant une interface d\'administration, un système de contact par email, et un design responsive moderne.',
                'technologies': 'Django, Python, Tailwind CSS, JavaScript, HTML/CSS',
                'github_url': 'https://github.com/Ely724',
                'is_featured': True,
            }
        )
        
        if created:
            print("✅ Projet d'exemple créé")
        
        print("🎉 Données d'exemple créées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données: {e}")

if __name__ == "__main__":
    print("🔧 SETUP DE DÉPLOIEMENT VERCEL")
    print("=" * 50)
    
    if setup_for_deployment():
        create_sample_data()
        print("\n🚀 Projet prêt pour le déploiement sur Vercel!")
        print("\nÉtapes suivantes:")
        print("1. Installez Vercel CLI: npm i -g vercel")
        print("2. Connectez-vous: vercel login")
        print("3. Déployez: vercel --prod")
    else:
        print("\n❌ Échec de la configuration")