import json
def generate_misuse_case_diagram(file_name):
    elements = [
        {"_type": "UMLActor", "_id": "actor1", "name": "Utilisateur légitime", "layout": {"x": 100, "y": 100}},
        {"_type": "UMLActor", "_id": "actor2", "name": "Attaquant externe", "layout": {"x": 300, "y": 100}},
        {"_type": "UMLUseCase", "_id": "usecase1", "name": "Accéder aux données patient", "layout": {"x": 100, "y": 300}},
        {"_type": "UMLUseCase", "_id": "usecase2", "name": "Modifier les prescriptions", "layout": {"x": 300, "y": 300}},
        {"_type": "UMLUseCase", "_id": "usecase3", "name": "Supprimer un dossier médical", "layout": {"x": 500, "y": 300}},
        {"_type": "UMLUseCase", "_id": "usecase4", "name": "Détournement d’accès", "layout": {"x": 300, "y": 500}}
    ]

    diagram_views = []
    for element in elements:
        view = {
            "_type": f"{element['_type']}View",
            "_id": f"{element['_id']}View",
            "model": {"$ref": element["_id"]},
            "left": element["layout"]["x"],
            "top": element["layout"]["y"],
            "width": 150,
            "height": 100
        }
        diagram_views.append(view)

    data = {
        "_type": "Project",
        "_id": "project7",
        "name": "Diagramme de cas d'abus - Gestion hospitalière",
        "ownedElements": [
            {
                "_type": "UMLPackage",
                "_id": "pkg7",
                "name": "MisUse Case Diagram",
                "ownedElements": [
                    {
                        "_type": "UMLUseCaseDiagram",
                        "_id": "ucd2",
                        "name": "Cas d'abus",
                        "ownedViews": diagram_views,
                        "ownedElements": elements
                    }
                ]
            }
        ]
    }

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Fichier '{file_name}' généré avec succès !")

generate_misuse_case_diagram("misuse_case_diagram.mdj")





