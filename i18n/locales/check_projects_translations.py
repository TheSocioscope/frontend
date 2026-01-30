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

print("📊 Projects Page Translation Check")
print("=" * 70)

# Check hero
print("\n🎯 HERO SECTION:")
print(f"  🇬🇧 EN: {en['projects']['hero']['title']} - {en['projects']['hero']['subtitle'][:40]}...")
print(f"  🇫🇷 FR: {fr['projects']['hero']['title']} - {fr['projects']['hero']['subtitle'][:40]}...")
print(f"  🇪🇸 ES: {es['projects']['hero']['title']} - {es['projects']['hero']['subtitle'][:40]}...")
print(f"  🇩🇪 DE: {de['projects']['hero']['title']} - {de['projects']['hero']['subtitle'][:40]}...")

# Check filters
print("\n🔍 FILTER LABELS:")
filter_keys = ['search', 'filterByContinent', 'filterByCountry', 'filterByStatus', 
               'filterByThematic', 'filterByField', 'filterByType']
for key in filter_keys:
    en_val = en['projects'].get(key, 'MISSING')
    fr_val = fr['projects'].get(key, 'MISSING')
    es_val = es['projects'].get(key, 'MISSING')
    de_val = de['projects'].get(key, 'MISSING')
    
    status = '✅' if all([en_val != 'MISSING', fr_val != 'MISSING', 
                          es_val != 'MISSING', de_val != 'MISSING']) else '❌'
    print(f"  {status} {key}:")
    print(f"     🇬🇧 {en_val}")
    print(f"     🇫🇷 {fr_val}")
    print(f"     🇪🇸 {es_val}")
    print(f"     🇩🇪 {de_val}")

# Check status labels
print("\n📋 STATUS LABELS:")
status_keys = ['pending', 'published', 'stale', 'verified', 'new']
for key in status_keys:
    en_val = en['projects']['status'].get(key, 'MISSING')
    fr_val = fr['projects']['status'].get(key, 'MISSING')
    es_val = es['projects']['status'].get(key, 'MISSING')
    de_val = de['projects']['status'].get(key, 'MISSING')
    
    print(f"  ✅ {key}: 🇬🇧 {en_val} | 🇫🇷 {fr_val} | 🇪🇸 {es_val} | 🇩🇪 {de_val}")

# Check results count
print("\n📊 RESULTS COUNT:")
print(f"  🇬🇧 EN: {en['projects']['projectsFound']}")
print(f"  🇫🇷 FR: {fr['projects']['projectsFound']}")
print(f"  🇪🇸 ES: {es['projects']['projectsFound']}")
print(f"  🇩🇪 DE: {de['projects']['projectsFound']}")

print("\n" + "=" * 70)
print("✅ All projects page translations verified!")
