#!/usr/bin/env python3
"""
Script to add missing translation keys back to the optimized en.json file.
"""
import json

# Load optimized and backup files
with open('/home/bob/Projects/frontend/i18n/locales/en.json', 'r', encoding='utf-8') as f:
    en_optimized = json.load(f)

with open('/home/bob/Projects/frontend/i18n/locales/en.json.backup', 'r', encoding='utf-8') as f:
    en_backup = json.load(f)

# Add missing sections
en_optimized['microscope'] = en_backup['microscope']
en_optimized['breakthroughs'] = en_backup['breakthroughs']
en_optimized['newsletter'] = en_backup['newsletter']
en_optimized['cta'] = en_backup['cta']
en_optimized['leadingResearch'] = en_backup['leadingResearch']

# Add missing common keys
en_optimized['common']['learnMore'] = "Learn More"
en_optimized['common']['offers'] = "What We Offer"
en_optimized['common']['lookingFor'] = "What We're Looking For"
en_optimized['common']['milestones'] = "Our journey"

# Add missing footer keys
en_optimized['footer']['stories'] = "Stories"

# Add pages section
en_optimized['pages'] = {
    "methodology": "Methodology"
}

# Add about section
en_optimized['about'] = {
    "meta": {
        "title": "About The Socioscope"
    },
    "hero": {
        "title": "About The Socioscope",
        "subtitle": "Understanding what truly drives sustainable change"
    },
    "mission": {
        "title": "Our Mission",
        "paragraph1": "The Socioscope is a transformative qualitative research project that maps how behaviours, norms, and communities influence the transition toward sustainable food systems.",
        "paragraph2": "The Socioscope serves as a comprehensive observatory of these efforts, making knowledge accessible to researchers, policymakers, and practitioners worldwide."
    },
    "whatWeDo": {
        "title": "What We Do",
        "paragraph1": "The Socioscope explores how sustainable change happens on the ground, with a focus on food systems. We document local solutions, speak with practitioners, and analyse insights using AI to reveal the patterns behind impactful innovation.",
        "paragraph2": "Through systematic research and community engagement, we identify, document, and analyze initiatives that embody sustainable transformation principles."
    },
    "methodology": {
        "title": "Our Methodology",
        "subtitle": "Combining academic rigor with participatory research approaches"
    },
    "values": {
        "title": "Our Values"
    },
    "cta": {
        "title": "Get Involved",
        "description": "Whether you're a researcher, practitioner, or community organizer, there are many ways to engage with The Socioscope.",
        "submitButton": "Submit an Initiative",
        "contactButton": "Contact Us"
    }
}

# Add products section  
en_optimized['products'] = {
    "meta": {
        "title": "Products & Solutions - The Socioscope"
    },
    "hero": {
        "title": "Products & Solutions",
        "subtitle": "Discover sustainable food products and services from our global community of practitioners"
    },
    "intro": {
        "title": "Sustainable Products & Services",
        "description": "Support initiatives driving sustainable change in food systems."
    },
    "visitWebsite": "Visit Website",
    "cta": {
        "title": "Want to Feature Your Product?",
        "description": "If you're part of our network and have sustainable food products or services to share, we'd love to showcase them here.",
        "submitButton": "Submit Your Product",
        "learnMoreButton": "Learn More"
    }
}

# Extend projects.submit section
en_optimized['projects']['submit'] = {
    "title": "Submit Your Initiative",
    "subtitle": "Share your sustainable food system transformation project",
    "name": "Initiative Name",
    "location": "Location",
    "description": "Description",
    "email": "Contact Email",
    "button": "Submit Initiative"
}

# Extend resources section
if 'categoryLabels' not in en_optimized['resources']:
    en_optimized['resources']['categoryLabels'] = {
        "article": "Article",
        "book": "Book",
        "event": "Event",
        "funding": "Funding",
        "organization": "Organization",
        "policy": "Policy Brief"
    }

if 'cta' not in en_optimized['resources']:
    en_optimized['resources']['cta'] = {
        "title": "Have a Resource to Share?",
        "subtitle": "Help us build the most comprehensive collection of sustainable food systems resources.",
        "button": "Submit Your Resource"
    }

if 'modal' not in en_optimized['resources']:
    en_optimized['resources']['modal'] = {
        "title": "Submit a Resource",
        "successMessage": "Thank you! Your resource has been submitted successfully.",
        "resourceInfo": "Resource Information",
        "resourceInfoSubtitle": "Tell us about the resource you'd like to share",
        "yourInfo": "Your Information",
        "yourInfoSubtitle": "We'll use this to contact you if needed",
        "submitButton": "Submit Resource",
        "fields": {
            "type": "Resource Type",
            "selectType": "Select a type",
            "title": "Resource Title",
            "authors": "Author(s) / Organization",
            "description": "Description / Abstract",
            "url": "URL / Link",
            "yourName": "Your Name",
            "yourEmail": "Your Email"
        }
    }

if 'noResults' not in en_optimized['resources']:
    en_optimized['resources']['noResults'] = "No resources found matching your criteria."

# Save the updated file
with open('/home/bob/Projects/frontend/i18n/locales/en.json', 'w', encoding='utf-8') as f:
    json.dump(en_optimized, f, ensure_ascii=False, indent=2)

print("✅ Successfully added missing translation keys to en.json!")
print("📋 Added sections: microscope, breakthroughs, newsletter, cta, leadingResearch, about, products")
print("🔄 Run optimize_translations.py again to update other language files.")
