# JEE Study Materials Directory

This directory should contain PDF files of JEE study materials to be ingested into the RAG system.

## Directory Structure

```
documents/
├── physics/
│   ├── ncert_class11_physics_chapter1.pdf
│   ├── ncert_class11_physics_chapter2.pdf
│   └── ...
├── chemistry/
│   ├── ncert_class11_chemistry_part1.pdf
│   ├── ncert_class11_chemistry_part2.pdf
│   └── ...
└── math/
    ├── ncert_class11_math.pdf
    ├── ncert_class12_math_part1.pdf
    └── ...
```

## Recommended Content

### Physics
- NCERT Class 11 Physics (All chapters)
- NCERT Class 12 Physics (All chapters)
- HC Verma Concepts of Physics (Optional)
- Previous year JEE Physics papers

### Chemistry
- NCERT Class 11 Chemistry Part 1 & 2
- NCERT Class 12 Chemistry Part 1 & 2
- NCERT Exemplar Chemistry (Optional)
- Previous year JEE Chemistry papers

### Mathematics
- NCERT Class 11 Mathematics
- NCERT Class 12 Mathematics Part 1 & 2
- RD Sharma (Optional)
- Previous year JEE Math papers

## Where to Get Materials

### Free Sources:
1. **NCERT Textbooks** (Official, Free)
   - https://ncert.nic.in/textbook.php
   - Choose subject → Download PDF

2. **NCERT Exemplar** (Free)
   - https://ncert.nic.in/exemplar-problems.php

3. **JEE Previous Year Papers** (Free)
   - https://jeemain.nta.nic.in/

### Paid Sources (Optional):
- Coaching institute materials
- Reference books (HC Verma, RD Sharma, etc.)

## File Naming Convention

Use clear, descriptive names:
- ✅ Good: `ncert_class11_physics_mechanics.pdf`
- ✅ Good: `jee_mains_2023_physics.pdf`
- ❌ Bad: `book1.pdf`
- ❌ Bad: `download.pdf`

## Notes

1. **Copyright**: Ensure you have the right to use these materials
2. **File Size**: Each PDF should be < 50MB for optimal processing
3. **Language**: Currently supports English only
4. **Format**: PDF only (no scanned images - OCR not implemented)

## Processing

Once PDFs are placed in the appropriate folders, run:

```bash
cd backend
python load_documents.py
```

This will:
1. Extract text from PDFs
2. Split into chunks (500 tokens each)
3. Generate embeddings (Gemini API)
4. Store in MongoDB with vector index

**Time**: ~5-10 minutes for 10-15 books

## Verification

After loading, check:
```bash
curl http://localhost:8001/api/v1/doubt/stats
```

Should show:
```json
{
  "total_chunks": 1500,
  "subjects": ["Physics", "Chemistry", "Mathematics"]
}
```

---

**Start with 1-2 PDFs to test, then add more content gradually.**
