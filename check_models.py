import google.generativeai as genai
import os

# ⚠️ Remplace ceci par ta vraie clé API (celle qui est dans secrets.toml)
api_key = "AIzaSyDgOqR7Mn66n5hXO5h9Ekc92CcpUhLMyu4" 

genai.configure(api_key=api_key)

print("🔍 Recherche des modèles disponibles...\n")

try:
    # On demande à Google la liste de tous les modèles
    for m in genai.list_models():
        # On ne garde que ceux qui savent générer du texte (chat)
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            
except Exception as e:
    print(f"Erreur : {e}")