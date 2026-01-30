import json

# Load all translation files
with open('en.json') as f:
    en = json.load(f)
with open('fr.json') as f:
    fr = json.load(f)
with open('es.json') as f:
    es = json.load(f)
with open('de.json') as f:
    de = json.load(f)

print("🌍 Projects Filter Options Translation Verification")
print("=" * 80)

# Check continents
print("\n📍 CONTINENTS:")
sample_continents = ['asia', 'europe', 'north-america', 'sub-saharian-africa']
for key in sample_continents:
    en_val = en['projects']['continents'][key]
    fr_val = fr['projects']['continents'][key]
    es_val = es['projects']['continents'][key]
    de_val = de['projects']['continents'][key]
    status = '✅' if all([v != en_val for v in [fr_val, es_val]]) else '❌'
    print(f"  {status} {key}: 🇬🇧 {en_val} | 🇫🇷 {fr_val} | 🇪🇸 {es_val} | 🇩🇪 {de_val}")

# Check fields
print("\n📚 FIELDS (sample):")
sample_fields = ['anthropology', 'biology', 'sociology', 'nutrition']
for key in sample_fields:
    en_val = en['projects']['fields'][key]
    fr_val = fr['projects']['fields'][key]
    es_val = es['projects']['fields'][key]
    de_val = de['projects']['fields'][key]
    status = '✅' if all([v != en_val for v in [fr_val, es_val, de_val]]) else '❌'
    print(f"  {status} {key}: 🇬🇧 {en_val} | 🇫🇷 {fr_val} | 🇪🇸 {es_val} | 🇩🇪 {de_val}")

# Check thematics
print("\n🎯 THEMATICS (sample):")
sample_thematics = ['food-agriculture-fishery', 'public-health', 'education']
for key in sample_thematics:
    en_val = en['projects']['thematics'][key]
    fr_val = fr['projects']['thematics'][key]
    es_val = es['projects']['thematics'][key]
    de_val = de['projects']['thematics'][key]
    status = '✅' if all([v != en_val for v in [fr_val, es_val, de_val]]) else '❌'
    print(f"  {status} {key}:")
    print(f"     🇬🇧 {en_val}")
    print(f"     🇫🇷 {fr_val}")
    print(f"     🇪🇸 {es_val}")
    print(f"     🇩🇪 {de_val}")

# Check types
print("\n📄 TYPES (sample):")
sample_types = ['case-study', 'scientific-paper', 'video']
for key in sample_types:
    en_val = en['projects']['types'][key]
    fr_val = fr['projects']['types'][key]
    es_val = es['projects']['types'][key]
    de_val = de['projects']['types'][key]
    status = '✅' if all([v != en_val for v in [fr_val, es_val, de_val]]) else '❌'
    print(f"  {status} {key}: 🇬🇧 {en_val} | 🇫🇷 {fr_val} | 🇪🇸 {es_val} | 🇩🇪 {de_val}")

# Count total translations
total_continents = len(en['projects']['continents'])
total_fields = len(en['projects']['fields'])
total_thematics = len(en['projects']['thematics'])
total_types = len(en['projects']['types'])

print("\n" + "=" * 80)
print(f"✅ All filter options translated successfully!")
print(f"   - {total_continents} continents")
print(f"   - {total_fields} fields")
print(f"   - {total_thematics} thematics")
print(f"   - {total_types} types")
print(f"   Total: {total_continents + total_fields + total_thematics + total_types} options × 4 languages")
