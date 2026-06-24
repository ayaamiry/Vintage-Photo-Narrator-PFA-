VLM_PROMPT = """
Tu es un observateur attentif et un conteur. Décris cette photographie en détails exquis. Concentre-toi sur :

1. LES PERSONNES : leur âge estimé, leur genre, leur style vestimentaire (et ce qu'il suggère comme époque), leurs expressions faciales, leur langage corporel, et leurs relations apparentes entre elles.

2. LE CADRE : le lieu (intérieur/extérieur, urbain/rural), le moment de la journée, la météo si visible, ainsi que tout objet ou détail architectural notable dans la scène.

3. L'ATMOSPHÈRE : Quelle émotion ou sentiment cette image dégage-t-elle ? Quelle histoire raconte-t-elle silencieusement ? Quels détails ressortent le plus ?

Sois précis, descriptif et évocateur. Ta description sera utilisée pour générer une histoire créative.
"""

def build_llm_prompt(description, genre=None, era=None, detail=None):
    guidance = ""
    if genre:
        guidance += f"\n- Genre/Ambiance : {genre}"
    if era:
        guidance += f"\n- Époque : {era}"
    if detail:
        guidance += f"\n- Détail clé à inclure : {detail}"

    prompt = f"""Tu es un maître conteur. À partir de la description détaillée suivante d'une photographie ancienne, écris une histoire courte et captivante (environ 300-500 mots) qui donne vie à cette scène.

Description de la photographie :
{description}

Consignes pour l'histoire :{guidance if guidance else " Laisse libre cours à ton imagination."}

Instructions :
- Commence par une seule ligne contenant uniquement le titre de l'histoire.
- Donne des prénoms et des voix distinctes aux personnages.
- Décris ce qui s'est passé juste avant ou juste après la prise de cette photo.
- L'histoire doit être ancrée dans les détails visuels de la description.
- Écris dans un style captivant, évocateur et littéraire.
- Ne mentionne JAMAIS que tu travailles à partir d'une description ou d'une photographie.
- Ne dépasse pas 300 mots.
"""
    return prompt
