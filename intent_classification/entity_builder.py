import json

entity_map = json.load(open('entity_map.json', 'r'))
subject_values = entity_map['[SUBJECT_MATTER]']['values']

entity_values = []
for subject in subject_values:
    entity_values.append({
      "value": subject,
      "synonyms": subject_values[subject]
    })

with open("./CSC466Bot/entities/SUBJECT_MATTER_entries_en.json", 'w+') as f_out:
    json.dump(entity_values, f_out)
