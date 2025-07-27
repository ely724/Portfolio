"""
Alternative de déploiement via GitHub + Vercel interface web
"""
import os
import subprocess
import json
import stat
from pathlib import Path

def check_git_installation():
    """Vérifie si Git est installé sur le système"""
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Git détecté : {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git n'est pas installé ou non accessible")
        return False

def prepare_github_deployment():
    """Prépare le projet pour déploiement via GitHub"""
    print("📁 Préparation pour déploiement GitHub + Vercel...")
    
    # Vérifier Git
    if not check_git_installation():
        print("\n🔧 INSTALLATION GIT REQUISE :")
        print("=" * 40)
        print("1. Téléchargez Git depuis : https://git-scm.com/download/win")
        print("2. Installez avec les options par défaut")
        print("3. Redémarrez votre terminal/IDE")
        print("4. Relancez ce script")
        
        # Continuer sans Git pour créer les fichiers de config
        print("\n⚠️ Continuons sans Git pour préparer les fichiers...")
        create_deployment_files_only()
        return False
    
    # Vérifier si git est initialisé
    if not Path('.git').exists():
        print("🔧 Initialisation du repository Git...")
        try:
            subprocess.run(['git', 'init'], check=True)
            print("✅ Git initialisé")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'initialisation Git : {e}")
            return False
    
    # Créer les fichiers de configuration
    create_deployment_files()
    
    # Instructions pour GitHub
    show_github_instructions()
    return True

def create_deployment_files():
    """Crée tous les fichiers nécessaires pour le déploiement"""
    
    # .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Static files (will be built on Vercel)
staticfiles/
staticfiles_build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Vercel
.vercel
""".strip()
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    print("✅ .gitignore créé/mis à jour")
    
    # Fichiers de configuration Vercel
    create_vercel_config()
    create_readme_deployment()

def create_deployment_files_only():
    """Crée uniquement les fichiers de configuration sans Git"""
    print("📋 Création des fichiers de configuration...")
    create_deployment_files()
    show_manual_deployment_instructions()

def create_vercel_config():
    """Crée les fichiers de configuration Vercel"""
    
    # Configuration vercel.json
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "portfolio_site/wsgi.py",
                "use": "@vercel/python",
                "config": {"maxLambdaSize": "15mb", "runtime": "python3.9"}
            },
            {
                "src": "build_files.sh",
                "use": "@vercel/static-build",
                "config": {"distDir": "staticfiles_build"}
            }
        ],
        "routes": [
            {"src": "/static/(.*)", "dest": "/static/$1"},
            {"src": "/media/(.*)", "dest": "/media/$1"},
            {"src": "/(.*)", "dest": "portfolio_site/wsgi.py"}
        ]
    }
    
    with open('vercel.json', 'w', encoding='utf-8') as f:
        json.dump(vercel_config, f, indent=2)
    print("✅ vercel.json créé")
    
    # Script de build
    build_script = """#!/bin/bash
# build_files.sh
echo "BUILD START"

# Installer les dépendances Python
python -m pip install -r requirements.txt

# Créer les migrations si nécessaire
python manage.py makemigrations --noinput || echo "No new migrations"

# Appliquer les migrations
python manage.py migrate --noinput

# Collecter les fichiers statiques
python manage.py collectstatic --noinput --clear

echo "BUILD END"
"""
    
    with open('build_files.sh', 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    # Rendre le script exécutable sur Unix
    try:
        st = os.stat('build_files.sh')
        os.chmod('build_files.sh', st.st_mode | stat.S_IEXEC)
    except:
        pass  # Ignore sur Windows
    
    print("✅ build_files.sh créé")

def create_readme_deployment():
    """Crée un README avec instructions de déploiement"""
    
    readme_content = """# Portfolio Django - Cheikhna Ely Cheikh Ndiaye

## 🚀 Portfolio moderne avec Django et Tailwind CSS

Ce portfolio présente mes compétences en développement fullstack avec une interface d'administration complète et un design responsive moderne.

## ✨ Fonctionnalités

- **Interface d'administration** Django pour gérer le contenu
- **Pages responsives** : accueil, à propos, projets, contact
- **Formulaire de contact** avec envoi d'emails automatique
- **Gestion des médias** pour images et fichiers
- **Design moderne** avec Tailwind CSS et animations
- **SEO optimisé** avec meta tags appropriés

## 🛠️ Technologies utilisées

- **Backend** : Django 5.2.4, Python 3.9+
- **Frontend** : Tailwind CSS, JavaScript ES6+, Font Awesome
- **Base de données** : SQLite (dev), Compatible PostgreSQL (prod)
- **Déploiement** : Vercel
- **Gestion des médias** : Pillow

## 🌐 Déploiement sur Vercel

Ce projet est configuré pour un déploiement automatique sur Vercel via GitHub.

### Prérequis
- Compte GitHub
- Compte Vercel (gratuit)
- Git installé localement

### Variables d'environnement requises sur Vercel
```
SECRET_KEY=votre-cle-secrete-django-unique
DEBUG=False
EMAIL_HOST_USER=cheikhna.ndiaye1@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app-gmail
CONTACT_EMAIL=cheikhna.ndiaye1@gmail.com
```

### Étapes de déploiement

1. **Créer un repository GitHub**
   - Allez sur github.com
   - Créez un nouveau repository public
   - Ne pas initialiser avec README (déjà présent)

2. **Pousser le code**
   ```bash
   git add .
   git commit -m "Portfolio Django - Prêt pour déploiement"
   git branch -M main
   git remote add origin https://github.com/Ely724/nom-du-repo.git
   git push -u origin main
   ```

3. **Déployer sur Vercel**
   - Allez sur vercel.com et connectez-vous
   - Cliquez "New Project"
   - Importez votre repository GitHub
   - Configurez les variables d'environnement
   - Déployez !

## 📧 Contact

- **Email** : cheikhna.ndiaye1@gmail.com
- **LinkedIn** : [Cheikhna Ndiaye](https://www.linkedin.com/in/cheikhna-ndiaye-ba0007163)
- **GitHub** : [Ely724](https://github.com/Ely724)

## 🔧 Développement local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver
```

Accédez à l'admin sur `http://127.0.0.1:8000/admin/` pour gérer le contenu.

---
Développé avec ❤️ par Cheikhna Ely Cheikh Ndiaye
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ README.md créé")

def show_github_instructions():
    """Affiche les instructions pour GitHub avec Git installé"""
    print("\n📋 INSTRUCTIONS POUR GITHUB :")
    print("=" * 50)
    print("1. 📁 Créez un nouveau repository sur GitHub :")
    print("   https://github.com/new")
    print("   Nom suggéré : 'portfolio-django'")
    print("   ⚠️ Ne pas initialiser avec README")
    print("\n2. 🔄 Exécutez ces commandes dans votre terminal :")
    print("   git add .")
    print("   git commit -m 'Portfolio Django - Prêt pour déploiement'")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/Ely724/portfolio-django.git")
    print("   git push -u origin main")
    print("\n3. 🌐 Déployez sur Vercel :")
    print("   • Allez sur vercel.com")
    print("   • Cliquez 'New Project'")
    print("   • Sélectionnez votre repository GitHub")
    print("   • Configurez les variables d'environnement")
    print("   • Déployez !")

def show_manual_deployment_instructions():
    """Affiche les instructions manuelles sans Git"""
    print("\n📋 DÉPLOIEMENT MANUEL (sans Git local) :")
    print("=" * 50)
    print("1. 📁 Créez un repository sur GitHub :")
    print("   https://github.com/new")
    print("   Nom : 'portfolio-django'")
    print("   ✅ Initialiser avec README cette fois")
    
    print("\n2. 📤 Uploadez vos fichiers :")
    print("   • Cliquez 'uploading an existing file'")
    print("   • Glissez-déposez tous vos fichiers du projet")
    print("   • Commit avec message : 'Upload portfolio Django'")
    
    print("\n3. 🌐 Déployez sur Vercel :")
    print("   • vercel.com → New Project")
    print("   • Importez depuis GitHub")
    print("   • Configurez les variables d'environnement")
    
    print("\n📝 Variables d'environnement Vercel :")
    print("   SECRET_KEY = django-insecure-abdd)xz4t&+gorkxvl633=j%(6pb_evl!@zsyz_o)3m**=mjdl")
    print("   DEBUG = False")
    print("   EMAIL_HOST_USER = cheikhna.ndiaye1@gmail.com")
    print("   EMAIL_HOST_PASSWORD = zliv tsqj cqud owdx")
    print("   CONTACT_EMAIL = cheikhna.ndiaye1@gmail.com")

def setup_local_for_github():
    """Configuration locale avant push GitHub"""
    print("🔧 Configuration locale...")
    
    # Importer et exécuter le setup de déploiement original
    try:
        from deploy_setup import setup_for_deployment, create_sample_data
        
        if setup_for_deployment():
            create_sample_data()
            return True
        return False
    except ImportError:
        print("⚠️ Module deploy_setup non trouvé, continuons...")
        return True

def create_git_installation_guide():
    """Crée un guide d'installation Git"""
    guide_content = """# Guide d'installation Git pour Windows

## Téléchargement
1. Allez sur : https://git-scm.com/download/win
2. Téléchargez la version 64-bit pour Windows

## Installation
1. Exécutez le fichier téléchargé
2. Acceptez les options par défaut
3. **Important** : Cochez "Git from the command line and also from 3rd-party software"

## Vérification
Ouvrez un nouveau terminal et tapez :
```bash
git --version
```

## Configuration initiale
```bash
git config --global user.name "Cheikhna Ndiaye"
git config --global user.email "cheikhna.ndiaye1@gmail.com"
```

Après installation, relancez le script de déploiement.
"""
    
    with open('INSTALL_GIT.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    print("✅ Guide d'installation Git créé : INSTALL_GIT.md")

if __name__ == "__main__":
    print("🔧 DÉPLOIEMENT ALTERNATIF VIA GITHUB")
    print("=" * 50)
    
    # Configuration locale
    if setup_local_for_github():
        print("✅ Configuration locale terminée")
        
        # Préparation GitHub avec vérification Git
        if prepare_github_deployment():
            print("\n🎉 Projet prêt pour GitHub + Vercel!")
        else:
            print("\n⚠️ Préparation partielle - Installation Git requise")
            create_git_installation_guide()
            
            print("\n📋 ALTERNATIVES SANS GIT :")
            print("=" * 30)
            print("• Utilisez GitHub Desktop (interface graphique)")
            print("• Uploadez manuellement sur github.com")
            print("• Utilisez Visual Studio Code avec extension Git")
            
    else:
        print("❌ Échec de la configuration locale")