# Portfolio Django - Cheikhna Ely Cheikh Ndiaye

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
