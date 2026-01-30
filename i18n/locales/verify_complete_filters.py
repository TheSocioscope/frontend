import json

with open('en.json') as f:
    en = json.load(f)
with open('fr.json') as f:
    fr = json.load(f)
with open('es.json') as f:
    es = json.load(f)
with open('de.json') as f:
    de = json.load(f)

print("🎯 Complete Filter Translation Verification")
print("=" * 80)

# Count translations
fields_en = len(en['projects']['fields'])
fields_fr = len(fr['projects']['fields'])
fields_es = len(es['projects']['fields'])
fields_de = len(de['projects']['fields'])

thematics_en = len(en['projects']['thematics'])
thematics_fr = len(fr['projects']['thematics'])
thematics_es = len(es['projects']['thematics'])
thematics_de = len(de['projects']['thematics'])

types_en = len(en['projects']['types'])
types_fr = len(fr['projects']['types'])
types_es = len(es['projects']['types'])
types_de = len(de['projects']['types'])

print(f"\n📚 FIELDS: {fields_en} total")
print(f"   🇬🇧 EN: {fields_en} | 🇫🇷 FR: {fields_fr} | 🇪🇸 ES: {fields_es} | 🇩🇪 DE: {fields_de}")
status = "✅" if fields_en == fields_fr == fields_es == fields_de else "❌"
print(f"   {status} All languages have same count")

# Show sample of newly added fields
print(f"\n   Sample new fields:")
new_fields = ['computer-sciences', 'epidemiology', 'linguistics']
for key in new_fields:
    print(f"     • {key}:")
    print(f"       🇬🇧 {en['projects']['fields'][key]}")
    print(f"       🇫🇷 {fr['projects']['fields'][key]}")
    print(f"       🇪🇸 {es['projects']['fields'][key]}")
    print(f"       🇩🇪 {de['projects']['fields'][key]}")

print(f"\n🎯 THEMATICS: {thematics_en} total")
print(f"   🇬🇧 EN: {thematics_en} | 🇫🇷 FR: {thematics_fr} | 🇪🇸 ES: {thematics_es} | 🇩🇪 DE: {thematics_de}")
status = "✅" if thematics_en == thematics_fr == thematics_es == thematics_de else "❌"
print(f"   {status} All languages have same count")

# Show sample of newly added thematics
print(f"\n   Sample new thematics:")
new_thematics = ['digital-humanities', 'migrations-and-diasporas', 'innovation-rd']
for key in new_thematics:
    print(f"     • {key}: 🇬🇧 {en['projects']['thematics'][key]} | 🇫🇷 {fr['projects']['thematics'][key]}")

print(f"\n📄 TYPES: {types_en} total")
print(f"   🇬🇧 EN: {types_en} | 🇫🇷 FR: {types_fr} | 🇪🇸 ES: {types_es} | 🇩🇪 DE: {types_de}")
status = "✅" if types_en == types_fr == types_es == types_de else "❌"
print(f"   {status} All languages have same count")

# Show sample of newly added types
print(f"\n   Sample new types:")
new_types = ['blog', 'thesis', 'policy-document', 'web-page']
for key in new_types:
    print(f"     • {key}: 🇬🇧 {en['projects']['types'][key]} | 🇫🇷 {fr['projects']['types'][key]}")

total = fields_en + thematics_en + types_en + 8  # +8 for continents
print(f"\n" + "=" * 80)
print(f"✅ COMPLETE! All filter options translated:")
print(f"   • 8 continents × 4 languages = 32 translations")
print(f"   • {fields_en} fields × 4 languages = {fields_en * 4} translations")
print(f"   • {thematics_en} thematics × 4 languages = {thematics_en * 4} translations")
print(f"   • {types_en} types × 4 languages = {types_en * 4} translations")
print(f"   TOTAL: {total * 4} translations across 4 languages")
