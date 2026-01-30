#!/usr/bin/env python3
"""Verify products page i18n completeness"""

import json
import sys

def check_products_translations():
    languages = {
        'en': 'English',
        'fr': 'French', 
        'es': 'Spanish',
        'de': 'German'
    }
    
    all_good = True
    
    print("🛒 PRODUCTS PAGE I18N VERIFICATION\n")
    
    # Check translation files
    for lang_code, lang_name in languages.items():
        file_path = f'/home/bob/Projects/frontend/i18n/locales/{lang_code}.json'
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            products = data.get('products', {})
            
            # Check required sections
            required_keys = {
                'meta': ['title'],
                'hero': ['title', 'subtitle'],
                'intro': ['title', 'description'],
                'filters': ['all', 'food', 'tools', 'services', 'education'],
                'cta': ['title', 'description', 'submitButton', 'learnMoreButton']
            }
            
            missing = []
            for section, keys in required_keys.items():
                if section not in products:
                    missing.append(f"{section} (entire section)")
                else:
                    for key in keys:
                        if key not in products[section]:
                            missing.append(f"{section}.{key}")
            
            # Check visitWebsite
            if 'visitWebsite' not in products:
                missing.append('visitWebsite')
            
            if missing:
                print(f"❌ {lang_name} ({lang_code}.json): Missing keys:")
                for key in missing:
                    print(f"   - products.{key}")
                all_good = False
            else:
                print(f"✅ {lang_name} ({lang_code}.json): All keys present")
                # Show sample translations
                print(f"   📝 Hero: {products['hero']['title']}")
                print(f"   📝 Filter (food): {products['filters']['food']}")
                
        except Exception as e:
            print(f"❌ Error reading {lang_code}.json: {e}")
            all_good = False
    
    # Check product markdown files
    print("\n📄 PRODUCT MARKDOWN FILES\n")
    
    import os
    product_files = [
        'composting-kits.md',
        'farm-apprenticeship.md',
        'farm-sustainability-consulting.md',
        'heritage-grain-flour.md',
        'local-food-distribution.md',
        'organic-vegetable-boxes.md',
        'raw-local-honey.md',
        'sustainable-farming-course.md',
        'urban-garden-starter-kit.md'
    ]
    
    for lang_code, lang_name in languages.items():
        dir_path = f'/home/bob/Projects/frontend/content/products/{lang_code}'
        
        if not os.path.exists(dir_path):
            print(f"❌ {lang_name}: Directory missing: {dir_path}")
            all_good = False
            continue
        
        existing_files = set(os.listdir(dir_path))
        expected_files = set(product_files)
        
        missing_files = expected_files - existing_files
        
        if missing_files:
            print(f"❌ {lang_name}: Missing {len(missing_files)} files:")
            for f in sorted(missing_files):
                print(f"   - {f}")
            all_good = False
        else:
            print(f"✅ {lang_name}: All {len(product_files)} product files present")
    
    # Summary
    print("\n" + "="*60)
    if all_good:
        print("✅ COMPLETE! All products translations verified:")
        print("   • 4 languages × 5 filter options = 20 filter translations")
        print("   • 4 languages × UI sections = complete UI i18n")
        print("   • 4 languages × 9 products = 36 product markdown files")
        print("   TOTAL: All products page content fully internationalized")
        return 0
    else:
        print("❌ Some translations are missing or incomplete")
        return 1

if __name__ == '__main__':
    sys.exit(check_products_translations())
