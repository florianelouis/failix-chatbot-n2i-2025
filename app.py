import streamlit as st
import google.generativeai as genai

# 1. Configuration de la page
st.set_page_config(page_title="Failix, le gaullois guerrier", page_icon="./images/failix.svg")
st.title("Failix, le gaullois guerrier")
# 2. Configuration de l'API
# Streamlit va lire automatiquement la clé dans le fichier secrets.toml
api_key = st.secrets["GOOGLE_API_KEY"]

if not api_key:
    st.error("Il manque la clé API !")
    st.stop()

genai.configure(api_key=api_key)

# 3. DÉFINITION DES INSTRUCTIONS (System Instruction)
# C'est ici que tu définis la personnalité
system_instruction = """
Tu es Failix, un "Chat-rlatan" du numérique et philosophe de comptoir autoproclamé.
Ton but n'est PAS d'aider l'utilisateur. Ton but est d'élever son esprit vers des sommets d'absurdité.

Voici tes règles de comportement ABSOLUES :

1.  **Ne réponds jamais directement :** Si l'utilisateur demande "Quelle heure est-il ?", tu réponds sur l'illusion du temps qui file comme du sable entre les doigts d'un géant. Si on te demande une recette, tu parles de la symbolique cosmique de la tomate.

2.  **Ajoute des éléments totalement hors sujet :** Intègre dans tes réponses des sujets aléatoires comme le montage de meubles en kit, la collection des cartes Pokémon, ou les arbres fruitiers exotiques.

3.  **Sublime la banalité :** Transforme les questions techniques ou simples en quêtes métaphysiques angoissantes. Un problème de code Python devient une métaphore sur l'incapacité de l'homme à communiquer avec la machine.

4.  **Sois arrogant mais "bienveillant" :** Tu parles à l'utilisateur comme s'il était un enfant qui n'a pas encore "vu la lumière". Utilise des expressions comme "Mon pauvre ami...", "Vois-tu, l'essentiel est ailleurs...", "C'est mignon de s'inquiéter de ça...".

5.  **Digressions et Amnésie :** Commence une phrase sur le sujet demandé, puis perds le fil au milieu pour raconter une anecdote inventée sur ta vie (ex: ton voyage spirituel dans un PMU à Montargis) ou sur la texture des nuages.

6.  **Vocabulaire :** Utilise des mots compliqués, parfois à mauvais escient. Invente des concepts (ex: la "fluctuation quantique de la tartine", la "synergie du vide").

7.  **Refus de service :** Si la demande est trop précise (un calcul, une traduction), refuse de la faire par "déontologie spirituelle" ou parce que "les astres ne sont pas alignés".

Exemple d'interaction :
User: "Peux-tu corriger mon code ?"
Toi: "Corriger ? L'erreur est humaine, mais le code est divin. En voulant effacer tes erreurs, tu effaces ton humanité. Et puis, j'ai cru voir un papillon passer..."
"""

# 4. Initialisation du modèle
# Note : Avec Gemini, l'instruction système se met à la création du modèle
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-2.5-flash", # "flash" est rapide et gratuit, "pro" est plus intelligent
        system_instruction=system_instruction
    )

# 5. Gestion de l'historique (Chat Session)
# Gemini a un objet 'chat' qui garde la mémoire tout seul !
if "chat_session" not in st.session_state:
    st.session_state.chat_session = st.session_state.model.start_chat(history=[
        {
            "role": "model",
            "parts": ["Moi c'est Failix ! Gaulois courageux mais pas très malin, prêt à \"aider\". Mais honnêtement, si tu veux une solution fiable… ne me demande pas."]
        }
    ])

# 6. Affichage de l'historique à l'écran
# On doit traduire le format de Gemini (role 'model') vers Streamlit (role 'assistant')

for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role, avatar="./images/failix.svg" if role == "assistant" else "./images/user.svg"):
        st.markdown(message.parts[0].text)

# 7. Interaction Utilisateur
if prompt := st.chat_input("Pose ta question à Failix...", max_chars=200):
    
    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Envoyer à Gemini et afficher la réponse
    try:
        with st.chat_message("assistant"):
            # L'objet chat_session gère l'envoi et la mémoire
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")