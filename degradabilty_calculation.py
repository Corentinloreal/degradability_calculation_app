import random
import streamlit as st

statuts_biodegradabilite = {
    "Not concerned (Volatil Organic Compound)": {"matiere_organique": 0, "degradabilite": 0},
    "Not concerned (inorganic)": {"matiere_organique": 0, "degradabilite": 0},
    "No data": {"matiere_organique": 100, "degradabilite": 0},
    "Organic, biodegradability not evaluated": {"matiere_organique": 100, "degradabilite": 0},
    "Calculated as not readily biodegradable": {"matiere_organique": 100, "degradabilite": 0},
    "Measured as not inherently biodegradable": {"matiere_organique": 100, "degradabilite": 0},
    "Measured as not readily biodegradable": {"matiere_organique": 100, "degradabilite": 0},
    "UVCB except plant extract": {"matiere_organique": 100, "degradabilite": 0},
    "Fragrance": {"matiere_organique": 100, "degradabilite": 100},
    "Calculated as readily biodegradable": {"matiere_organique": 100, "degradabilite": 0},
    "Natural Organic ingredient": {"matiere_organique": 100, "degradabilite": 100},
    "Measured as inherently biodegradable": {"matiere_organique": 100, "degradabilite": 100},
    "Not Persistent": {"matiere_organique": 100, "degradabilite": 100},
    "Measured as readily biodegradable without respecting the 10/14-day window": {"matiere_organique": 100, "degradabilite": 100},
    "Measured as readily biodegradable": {"matiere_organique": 100, "degradabilite": 100},
    "Natural biodegradable": {"matiere_organique": 100, "degradabilite": 100},
}

st.title("Calcul du % de dégradabilité des MP")

nb_matiere_premiere = None
nb_matiere_premiere = st.selectbox("Nombre de matières premières à générer \U0001F9EA", [0, 1, 2, 3, 4, 5], index= None, placeholder="Selectionnez un nombre de matière première", key="nb_mp")
st.write("-"*50)

matieres_premieres = []
if type(nb_matiere_premiere) is int:
    for i in range(nb_matiere_premiere):
        key_1 = f"widget_ing_{i}"
        composition = []
        MP = 1 + i
        i += 1
        nb_ingredients = st.selectbox(f"Nombre d'ingrédient de MP_{i} \U0001F52C : ", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index= None, placeholder="Selectionnez un nombre d'ingrédient", key=key_1)
        if type(nb_ingredients) is int:
            ponderations = random.choices(range(1, 101), k=nb_ingredients)
            total_ponderation = sum(ponderations)
            ponderations = [round(ponderation * 100 / total_ponderation, 2) for ponderation in ponderations]
            for k in range(nb_ingredients):
                key_2 = f"widget_statut_{k+i*10}"
                statut_biodeg = st.selectbox(f"Selectionnez le statut de biodeg de l'ingrédient {k + 1} \U0001F33F : ", ["Not concerned (Volatil Organic Compound)", "Not concerned (inorganic)", "No data", "Organic, biodegradability not evaluated", "Calculated as not readily biodegradable", "Measured as not inherently biodegradable", "Measured as not readily biodegradable", "UVCB except plant extract", "Fragrance", "Calculated as readily biodegradable", "Natural Organic ingredient", "Measured as inherently biodegradable", "Not Persistent", "Measured as readily biodegradable without respecting the 10/14-day window", "Measured as readily biodegradable", "Natural biodegradable"], index= None, placeholder="Selectionnez un statut dans la liste déroulante", key=key_2)
                if type(statut_biodeg) is str:
                    values = statuts_biodegradabilite.get(statut_biodeg)
                    matiere_organique = values["matiere_organique"]
                    degradabilite = values["degradabilite"]
                    ponderation = ponderations.pop(0)
                    composition.append({"statut_biodeg": statut_biodeg, "matiere_organique": matiere_organique, "degradabilite": degradabilite, "ponderation": ponderation})
            matieres_premieres.append({"composition": composition})
            st.write("-"*50)
            st.write()

if st.button("Cliquez ici pour lancer les calculs"):
    for i, matiere_premiere in enumerate(matieres_premieres, 1):
        st.write(f"Calcul dégradabilité MP_{i} :")
    
        for j, ingredient in enumerate(matiere_premiere["composition"], 1):
            statut_biodegradabilite = ingredient["statut_biodeg"]
            matiere_organique = ingredient["matiere_organique"]
            degradabilite = ingredient["degradabilite"]
            ponderation = ingredient.get("ponderation", "Valeur par défaut")
            st.write(f"- \U0001F9EC Ingredient {j} - {statut_biodegradabilite} - Matiere Organique : {matiere_organique} - Dégradabilité : {degradabilite} - Pondération : {ponderation}")
        st.write()
    
        pourcentage_degradabilite = 0
        total_ponderation_organic = sum(ingredient['ponderation'] for ingredient in matiere_premiere["composition"] if ingredient['matiere_organique'] != 0)
        total_ponderation_MP = sum(ingredient['ponderation'] for ingredient in matiere_premiere["composition"])
        if total_ponderation_organic != 0:
            for ingredient in matiere_premiere["composition"]:
                matiere_organique = ingredient['matiere_organique']
                degradabilite = ingredient['degradabilite']
                ponderation = ingredient['ponderation']
                if matiere_organique != 0 :
                    pourcentage_degradabilite += round((matiere_organique * degradabilite * ponderation / 100) / total_ponderation_organic, 2)
        else:
            pourcentage_degradabilite = "0"
        
        st.write(f"Pourcentage de dégradabilité MP_{i} : {pourcentage_degradabilite}% \u2705")
        st.write("-" * 50)
        st.write()
   