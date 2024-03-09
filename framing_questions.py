import spacy


def custom_ner(text):
    nlp_ner = spacy.load("model-best")

    doc = nlp_ner(text)

    # Extract entities from the document
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Display extracted entities
    print("Extracted Entities:", entities)

    return entities





def generate_questions_for_entities(entities):

    full1 = []

    medicine_questions = []
    medical_condition_questions = []

    for entity, label in entities:
        # Check the label of the entity
        if label == 'MEDICINE':
            # Level 1: Remembering
            full1.append(f"What is {entity}?")

            # Level 2: Understanding
            full1.append(f"How does {entity} work?")

            # Level 3: Application
            full1.append(f"In what cases is {entity} commonly used?")

        elif label == 'MEDICALCONDITION':
            # Level 1: Remembering
            full1.append(f"What is {entity}?")

            # Level 2: Understanding
            full1.append(f"How does {entity} affect the body?")

            # Level 3: Application
            full1.append(f"What are the common treatments for {entity}?")

    return full1


# define entities
entities = custom_ner(text)

# Generate questions for 'MEDICINE' and 'MEDICALCONDITION'
medicine_questions, medical_condition_questions = generate_questions_for_entities(entities)



# # Display generated questions
# print("\nMedicine-related Questions:")
# for question in medicine_questions:
#     print(question)

# print("\nMedical Condition-related Questions:")
# for question in medical_condition_questions:
#     print(question)