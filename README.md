# CDK Pipeline Lite — Déploiement Automatisé d’une Lambda depuis GitHub

Ce projet a été réalisé dans le cadre de mon apprentissage du développement Cloud AWS.  
L’objectif : créer un pipeline CI/CD simple et fonctionnel pour mettre à jour automatiquement une fonction Lambda dès qu’un build est lancé.

L’idée est de comprendre les bases d’un pipeline professionnel tout en restant sur un projet léger et facile à maintenir.

---

## Objectif du projet

Mettre en place une architecture capable de :

- Déployer une **Lambda Python**
- Décrire l’infrastructure avec **AWS CDK**
- Construire un **pipeline CodePipeline + CodeBuild**
- Télécharger le code depuis **GitHub**
- Zipper et déployer automatiquement la Lambda

Ce pipeline me permet de me familiariser avec les concepts CI/CD en entreprise.

---

##  Architecture

```
GitHub Repository
        ↓
AWS CodePipeline
        ↓
AWS CodeBuild (zip du dossier lambda/)
        ↓
AWS Lambda (mise à jour automatique)
```

---

## Services AWS utilisés

### **1. AWS Lambda**
Exécute le code backend (Python).  
Répond simplement :  
```json
{
  "message": "Hello from Lambda - auto deployed!"
}
```

### **2. AWS CDK (Python)**
Décrit l’infrastructure comme du code (IaC).

- *ApplicationStack* → Déploie la Lambda
- *PipelineStack* → Configure le pipeline CodePipeline + CodeBuild

### **3. AWS CodePipeline**
Service CI/CD qui orchestre tout le processus.

### **4. AWS CodeBuild**
Exécute le script `pipeline-template.yaml` pour :
- installer Python
- zipper la Lambda
- mettre à jour son code

---

## 📁 Structure du projet

```
cdk-pipeline-lite/
│
├── app.py                      # Entrée CDK
├── cdk_pipeline_lite/
│   ├── application_stack.py    # Stack Lambda
│   └── pipeline_stack.py       # Stack Pipeline
│
├── lambda/
│   └── handler.py              # Code de la Lambda
│
├── pipeline-template.yaml      # Buildspec utilisé par CodeBuild
├── requirements.txt
└── README.md
```

---

## 🧪 Tests et CI/CD

À chaque exécution du pipeline :

1. CodePipeline clone le repo GitHub  
2. CodeBuild compresse le dossier `lambda/`  
3. Le build met à jour la Lambda automatiquement  
4. Plus besoin de CDK deploy pour mettre à jour le code de la fonction

---

## 📚 Objectifs pédagogiques

Ce projet m’a permis de comprendre :

- La structure d’un projet CDK propre  
- Comment découpler une stack applicative d’un pipeline  
- Comment fonctionne CodePipeline & CodeBuild  
- Comment automatiser un déploiement depuis GitHub  
- Comment structurer une Lambda pour le CI/CD  

Ce projet est volontairement simple pour ancrer les bonnes pratiques avant de passer sur des architectures plus complexes.

---

## 🛠️ Commandes utiles

```bash
cdk synth
cdk deploy
cdk diff
```

---

## 📝 Note personnelle

Je suis en apprentissage et ce dépôt fait partie de mon parcours pour devenir développeur cloud.  
Ce projet me sert de base solide pour comprendre la logique CI/CD et préparer mes futures architectures plus avancées.

---

