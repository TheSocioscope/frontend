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

# Check about section keys
about_keys = [
    "about.hero.title",
    "about.hero.subtitle",
    "about.mission.paragraph1",
    "about.mission.paragraph2",
    "about.values.collaboration.desc",
    "about.cta.submitButton",
    "about.cta.contactButton"
]

print("📊 Translation Check for About Section")
print("=" * 60)

for key in about_keys:
    keys = key.split('.')
    
    en_val = en
    fr_val = fr
    es_val = es
    de_val = de
    
    for k in keys:
        en_val = en_val.get(k, '')
        fr_val = fr_val.get(k, '')
        es_val = es_val.get(k, '')
        de_val = de_val.get(k, '')
    
    print(f"\n{key}:")
    print(f"  🇬🇧 EN: {en_val[:50]}...")
    print(f"  🇫🇷 FR: {fr_val[:50]}... {'✅' if fr_val != en_val else '❌ Same as EN'}")
    print(f"  🇪🇸 ES: {es_val[:50]}... {'✅' if es_val != en_val else '❌ Same as EN'}")
    print(f"  🇩🇪 DE: {de_val[:50]}... {'✅' if de_val != en_val else '❌ Same as EN'}")

print("\n" + "=" * 60)
print("✅ Translation check complete!")
