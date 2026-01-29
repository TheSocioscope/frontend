# Project Duplicates Analysis Report

## Summary

Analyzed 734 project files and identified **26 potential duplicate groups**.

## Obvious Duplicates (Safe to Merge)

These are duplicates with 100% name match, same contact, and same location. The merge script will handle these automatically:

### 1. **Mulino Terrevive** (6 duplicates)

- **Keep:** 431352.json
- **Merge:** 432052.json, 432352.json, 430952.json, 430452.json, 432252.json
- Same company, same contact (Marco Bigolin), Italy

### 2. **Flenexa** (3 duplicates)

- **Keep:** 439452.json
- **Merge:** 439852.json, 430052.json
- Same company, Czech Republic

### 3. **Caresà Agricultural Cooperative** (2 duplicates)

- **Keep:** 431252.json
- **Merge:** 430552.json
- 89.66% name similarity, Italy

### 4. **Sensitive Agriculture by Marck Pépin** (2 duplicates)

- **Keep:** 443552.json (Agroforestry)
- **Merge:** 431152.json (Vineyards and nurseries)
- Same author, 87.39% similarity, France - appear to be different aspects of same project

### 5. **Mother Earth Farm** (2 duplicates)

- **Keep:** 437452.json
- **Merge:** 430252.json
- 100% match, Italy

### 6. **Aquaponia** (2 duplicates)

- **Keep:** 439352.json
- **Merge:** 439952.json
- 100% match, Czech Republic

### 7. **Riz-banane** (2 duplicates)

- **Keep:** 432652.json
- **Merge:** 431952.json
- 100% match, same contact (Boris LHIE), Polynésie Française

### 8. **Villa Rabelais** (2 duplicates)

- **Keep:** 439652.json
- **Merge:** 439252.json
- 100% match, same contact (Francis Chevrier), France

### 9. **Avana Vetiver** (2 duplicates)

- **Keep:** 431852.json
- **Merge:** 432752.json
- 100% match, same contact (Andy Kirkwood)

## Needs Manual Review

These groups need your confirmation as they involve multiple projects from the same contact/organization but may be distinct projects:

### A. **Food Socioscope (IEA)** - 465 projects!

This is a MASSIVE group. All projects have the same contact "Food Socioscope (IEA)" but appear to be **distinct projects** across different countries (Argentina, France, Kenya, Colombia, Peru, Spain, etc.).

**Recommendation:** These should NOT be merged as they are separate projects documented by the same organization. This is the Paris IAS managing the website as you mentioned.

### B. **Sophie Nicklaus (INRAE)** - 16 projects in Dijon

All related to "ProDij 2030" sustainable food initiative in Dijon, France. These appear to be **sub-projects** of a larger initiative.

**Question for you:** Should these remain separate or be consolidated under one main ProDij 2030 entry with the others as components?

### C. **Yves Cabannes** - 23 projects total

- 14 via RUAF (Urban Agriculture Magazine issues)
- 9 via University College London (various urban agriculture projects)

**Recommendation:** The magazine issues could potentially be consolidated into one "RUAF Urban Agriculture Magazine" entry with issue numbers, but the research projects should remain separate.

### D. **David Kanter (New York University)** - 6-8 projects

Research papers on nitrogen pollution and sustainable agriculture.

**Recommendation:** These appear to be distinct research outputs and should remain separate.

### E. **City of Ghent initiatives** - 9 projects

Various sustainable food initiatives in Ghent, Belgium.

**Recommendation:** These are distinct programs and should remain separate.

### F. **Phenix (Jean Moreau)** - 5 projects

Different tools/features of the Phenix anti-waste platform.

**Question for you:** Should these be merged into one Phenix entry, or kept as separate features?

### G. **Smartway** - 4 projects

Four components of their "Food Waste Management System" (smartdetection, smartdecision, smartdiscount, smartdonation).

**Question for you:** Merge into one system or keep as separate modules?

### H. Other smaller groups (2-3 projects each):

- Christophe Lavelle (CNRS) - 3 publications
- Catherine Bassani (Nantes) - 3 Nantes food initiatives
- Raúl Matta - 6-9 food heritage research papers
- Marck Pépin - 2 aspects of sensitive agriculture
- Niko Romito - 2 cooking research papers
- Various others

## Action Items

1. **Review the merge script preview:**

   ```bash
   cd /home/bob/Projects/frontend/content/projects
   python3 merge_duplicates.py
   ```

2. **Confirm which groups in "Needs Manual Review" should be merged**

3. **Execute the obvious merges:**

   ```bash
   python3 merge_duplicates.py --execute
   ```

4. **Let me know your decisions on the manual review items**, and I can create additional merge groups for those.

## Questions for You

1. Should multi-component projects (like Phenix, Smartway) be merged or kept separate?
2. Should research publication series (Yves Cabannes magazines, Raúl Matta papers) be consolidated?
3. Should sub-projects of larger initiatives (ProDij 2030, Ghent initiatives) remain separate?
4. Any other criteria you'd like to apply for determining duplicates?

## Statistics

- **Total projects:** 734
- **Obvious duplicates to merge:** 9 groups (18 files will be merged into 9)
- **Projects needing manual review:** ~17 groups
- **Estimated duplicates after review:** Could be 50-100+ files depending on your criteria
