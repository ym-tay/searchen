import json

# Function to generate the use case diagram .mdj file with layout and views
def generate_hospital_use_case_diagram(file_name):
    # Logical structure (actors, use cases)
    elements = [
        {"_type": "UMLActor", "_id": "actor1", "name": "Directeur général", "layout": {"x": 100, "y": 100}},
        {"_type": "UMLActor", "_id": "actor2", "name": "Médecin", "layout": {"x": 200, "y": 100}},
        {"_type": "UMLActor", "_id": "actor3", "name": "Chef de service", "layout": {"x": 300, "y": 100}},
        {"_type": "UMLActor", "_id": "actor4", "name": "Infirmière", "layout": {"x": 400, "y": 100}},
        {"_type": "UMLActor", "_id": "actor5", "name": "Secrétaire médicale", "layout": {"x": 500, "y": 100}},
        {"_type": "UMLActor", "_id": "actor6", "name": "Patient", "layout": {"x": 600, "y": 100}},
        {"_type": "UMLUseCase", "_id": "usecase1", "name": "Initialiser un dossier médical", "layout": {"x": 100, "y": 300}},
        {"_type": "UMLUseCase", "_id": "usecase2", "name": "Mettre à jour un dossier médical", "layout": {"x": 200, "y": 300}},
        {"_type": "UMLUseCase", "_id": "usecase3", "name": "Attribuer une chambre", "layout": {"x": 300, "y": 300}},
        {"_type": "UMLUseCase", "_id": "usecase4", "name": "Enregistrer une visite médicale", "layout": {"x": 400, "y": 300}},
        {"_type": "UMLUseCase", "_id": "usecase5", "name": "Gérer les soins", "layout": {"x": 500, "y": 300}},
        {"_type": "UMLUseCase", "_id": "usecase6", "name": "Consulter le dossier médical", "layout": {"x": 600, "y": 300}}
    ]

    # Diagram with views
    diagram_views = []
    for element in elements:
        view = {
            "_type": f"{element['_type']}View",
            "_id": f"{element['_id']}View",
            "model": {"$ref": element["_id"]},
            "left": element["layout"]["x"],
            "top": element["layout"]["y"],
            "width": 100,
            "height": 50
        }
        diagram_views.append(view)

    # Full project structure
    data = {
        "_type": "Project",
        "_id": "project1",
        "name": "Diagramme de cas d'utilisation - Gestion d'une structure hospitalière",
        "ownedElements": [
            {
                "_type": "UMLPackage",
                "_id": "pkg1",
                "name": "Use Case Diagram",
                "ownedElements": [
                    {
                        "_type": "UMLUseCaseDiagram",
                        "_id": "ucd1",
                        "name": "Gestion Hospitalière",
                        "ownedViews": diagram_views,  # Visual representation
                        "ownedElements": elements  # Logical elements
                    }
                ]
            }
        ]
    }

    # Write the .mdj file
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Fichier '{file_name}' généré avec succès !")

# Generate the .mdj file for the use case diagram
generate_hospital_use_case_diagram("2567.mdj")

