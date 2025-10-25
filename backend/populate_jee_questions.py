"""
Populate database with JEE (Joint Entrance Examination) style questions
Covers Physics, Chemistry, and Mathematics from past 10 years pattern
"""
import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.models import Content, Base
import json

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# JEE Question Bank (2015-2024 pattern based)
JEE_QUESTIONS = [
    # ==================== PHYSICS ====================
    # Mechanics
    {
        "title": "Projectile Motion - Maximum Height",
        "description": "A projectile is thrown with initial velocity 20 m/s at 60° to horizontal. Find maximum height.",
        "topic": "mechanics",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "A projectile is thrown with velocity 20 m/s at angle 60° to horizontal. What is the maximum height reached? (g = 10 m/s²)",
        "options": json.dumps(["5 m", "10 m", "15 m", "20 m"]),
        "correct_answer": "15 m",
        "explanation": "H_max = (u²sin²θ)/(2g) = (20² × sin²60°)/(2×10) = (400 × 0.75)/20 = 15 m",
        "tags": json.dumps(["projectile", "kinematics", "mechanics", "jee_main"])
    },
    {
        "title": "Newton's Laws - Force and Acceleration",
        "description": "Calculate net force on a system of blocks",
        "topic": "mechanics",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "Two blocks of mass 2 kg and 3 kg are connected by a string over a frictionless pulley. What is the acceleration of the system? (g = 10 m/s²)",
        "options": json.dumps(["2 m/s²", "4 m/s²", "5 m/s²", "6 m/s²"]),
        "correct_answer": "2 m/s²",
        "explanation": "a = (m₂ - m₁)g/(m₁ + m₂) = (3-2)×10/(2+3) = 10/5 = 2 m/s²",
        "tags": json.dumps(["newton_laws", "pulley", "mechanics", "jee_main"])
    },
    {
        "title": "Work Energy Theorem",
        "description": "Application of work-energy principle",
        "topic": "mechanics",
        "difficulty": 8,
        "content_type": "multiple_choice",
        "question_text": "A body of mass 2 kg is moving with velocity 10 m/s. What is the work done to stop it?",
        "options": json.dumps(["-50 J", "-100 J", "-150 J", "-200 J"]),
        "correct_answer": "-100 J",
        "explanation": "W = ΔKE = 0 - ½mv² = -½(2)(10²) = -100 J",
        "tags": json.dumps(["work_energy", "mechanics", "jee_advanced"])
    },
    
    # Electromagnetism
    {
        "title": "Coulomb's Law - Force Between Charges",
        "description": "Calculate electrostatic force between two point charges",
        "topic": "electromagnetism",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "Two charges of +2μC and -3μC are separated by 30 cm. Find the force between them. (k = 9×10⁹ Nm²/C²)",
        "options": json.dumps(["0.3 N", "0.6 N", "0.9 N", "1.2 N"]),
        "correct_answer": "0.6 N",
        "explanation": "F = k|q₁q₂|/r² = (9×10⁹)(2×10⁻⁶)(3×10⁻⁶)/(0.3²) = 0.6 N",
        "tags": json.dumps(["electrostatics", "coulomb_law", "jee_main"])
    },
    {
        "title": "Ohm's Law and Resistance",
        "description": "Calculate current in a circuit",
        "topic": "electromagnetism",
        "difficulty": 5,
        "content_type": "multiple_choice",
        "question_text": "A 12V battery is connected to a 4Ω resistor. What is the current flowing?",
        "options": json.dumps(["2 A", "3 A", "4 A", "6 A"]),
        "correct_answer": "3 A",
        "explanation": "I = V/R = 12/4 = 3 A",
        "tags": json.dumps(["current_electricity", "ohm_law", "jee_main"])
    },
    {
        "title": "Magnetic Force on Moving Charge",
        "description": "Calculate Lorentz force",
        "topic": "electromagnetism",
        "difficulty": 8,
        "content_type": "multiple_choice",
        "question_text": "An electron (q = 1.6×10⁻¹⁹C) moves with velocity 10⁶ m/s perpendicular to magnetic field of 0.5 T. Find the force.",
        "options": json.dumps(["4×10⁻¹⁴ N", "8×10⁻¹⁴ N", "1.6×10⁻¹³ N", "3.2×10⁻¹³ N"]),
        "correct_answer": "8×10⁻¹⁴ N",
        "explanation": "F = qvB sin90° = (1.6×10⁻¹⁹)(10⁶)(0.5) = 8×10⁻¹⁴ N",
        "tags": json.dumps(["magnetism", "lorentz_force", "jee_advanced"])
    },
    
    # Optics
    {
        "title": "Lens Formula - Image Formation",
        "description": "Calculate image distance using lens formula",
        "topic": "optics",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "A convex lens of focal length 20 cm forms an image of object placed 30 cm away. Find image distance.",
        "options": json.dumps(["40 cm", "50 cm", "60 cm", "70 cm"]),
        "correct_answer": "60 cm",
        "explanation": "1/f = 1/v - 1/u → 1/20 = 1/v - 1/(-30) → 1/v = 1/20 - 1/30 = 1/60 → v = 60 cm",
        "tags": json.dumps(["optics", "lens", "ray_optics", "jee_main"])
    },
    {
        "title": "Young's Double Slit Experiment",
        "description": "Calculate fringe width in interference",
        "topic": "optics",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "In YDSE, distance between slits is 0.5 mm, screen distance is 1 m, wavelength 500 nm. Find fringe width.",
        "options": json.dumps(["0.5 mm", "1.0 mm", "1.5 mm", "2.0 mm"]),
        "correct_answer": "1.0 mm",
        "explanation": "β = λD/d = (500×10⁻⁹ × 1)/(0.5×10⁻³) = 1×10⁻³ m = 1.0 mm",
        "tags": json.dumps(["wave_optics", "interference", "jee_advanced"])
    },
    
    # Modern Physics
    {
        "title": "Photoelectric Effect - Einstein's Equation",
        "description": "Calculate kinetic energy of photoelectrons",
        "topic": "modern_physics",
        "difficulty": 8,
        "content_type": "multiple_choice",
        "question_text": "Work function of metal is 2 eV. Light of wavelength 400 nm falls on it. Find max KE of photoelectrons. (h=6.63×10⁻³⁴ Js, c=3×10⁸ m/s)",
        "options": json.dumps(["0.1 eV", "1.1 eV", "2.1 eV", "3.1 eV"]),
        "correct_answer": "1.1 eV",
        "explanation": "E_photon = hc/λ = (6.63×10⁻³⁴ × 3×10⁸)/(400×10⁻⁹) = 3.1 eV, KE_max = E - φ = 3.1 - 2 = 1.1 eV",
        "tags": json.dumps(["modern_physics", "photoelectric", "quantum", "jee_advanced"])
    },
    
    # ==================== CHEMISTRY ====================
    # Physical Chemistry
    {
        "title": "Mole Concept - Avogadro Number",
        "description": "Calculate number of molecules",
        "topic": "physical_chemistry",
        "difficulty": 5,
        "content_type": "multiple_choice",
        "question_text": "How many molecules are present in 4.4 g of CO₂? (Molecular mass of CO₂ = 44)",
        "options": json.dumps(["6.02×10²²", "6.02×10²³", "1.2×10²³", "3.01×10²³"]),
        "correct_answer": "6.02×10²²",
        "explanation": "Moles = 4.4/44 = 0.1 mol, Molecules = 0.1 × 6.02×10²³ = 6.02×10²²",
        "tags": json.dumps(["mole_concept", "physical_chemistry", "jee_main"])
    },
    {
        "title": "Thermodynamics - Enthalpy Change",
        "description": "Calculate heat of reaction",
        "topic": "physical_chemistry",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "For reaction: C + O₂ → CO₂, ΔH = -394 kJ/mol. Heat released when 6g carbon burns completely is:",
        "options": json.dumps(["98.5 kJ", "197 kJ", "394 kJ", "788 kJ"]),
        "correct_answer": "197 kJ",
        "explanation": "Moles of C = 6/12 = 0.5 mol, Heat = 0.5 × 394 = 197 kJ",
        "tags": json.dumps(["thermodynamics", "enthalpy", "jee_main"])
    },
    {
        "title": "Chemical Kinetics - Rate Law",
        "description": "Determine order of reaction",
        "topic": "physical_chemistry",
        "difficulty": 8,
        "content_type": "multiple_choice",
        "question_text": "For reaction A → B, when [A] is doubled, rate becomes 4 times. What is the order?",
        "options": json.dumps(["0", "1", "2", "3"]),
        "correct_answer": "2",
        "explanation": "Rate ∝ [A]ⁿ, If [A] doubles and rate becomes 4×, then 2ⁿ = 4 → n = 2 (Second order)",
        "tags": json.dumps(["kinetics", "rate_law", "jee_advanced"])
    },
    {
        "title": "Electrochemistry - Cell Potential",
        "description": "Calculate EMF of electrochemical cell",
        "topic": "physical_chemistry",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "E°(Zn²⁺/Zn) = -0.76V, E°(Cu²⁺/Cu) = +0.34V. Find E°cell for Zn-Cu cell.",
        "options": json.dumps(["0.42 V", "1.10 V", "1.52 V", "2.20 V"]),
        "correct_answer": "1.10 V",
        "explanation": "E°cell = E°cathode - E°anode = 0.34 - (-0.76) = 1.10 V",
        "tags": json.dumps(["electrochemistry", "cell_potential", "jee_main"])
    },
    
    # Organic Chemistry
    {
        "title": "IUPAC Nomenclature - Alkanes",
        "description": "Name organic compound using IUPAC rules",
        "topic": "organic_chemistry",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "What is the IUPAC name of CH₃-CH(CH₃)-CH₂-CH₃?",
        "options": json.dumps(["2-methylbutane", "3-methylbutane", "isopentane", "2-ethylpropane"]),
        "correct_answer": "2-methylbutane",
        "explanation": "Longest chain has 4 carbons (butane), methyl group at position 2: 2-methylbutane",
        "tags": json.dumps(["organic", "nomenclature", "alkanes", "jee_main"])
    },
    {
        "title": "Isomerism - Structural Isomers",
        "description": "Count number of isomers",
        "topic": "organic_chemistry",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "How many structural isomers of C₅H₁₂ exist?",
        "options": json.dumps(["2", "3", "4", "5"]),
        "correct_answer": "3",
        "explanation": "Three isomers: n-pentane, 2-methylbutane (isopentane), 2,2-dimethylpropane (neopentane)",
        "tags": json.dumps(["organic", "isomerism", "alkanes", "jee_advanced"])
    },
    {
        "title": "Reaction Mechanisms - SN1 vs SN2",
        "description": "Identify reaction mechanism",
        "topic": "organic_chemistry",
        "difficulty": 8,
        "content_type": "multiple_choice",
        "question_text": "Which alkyl halide will undergo SN2 reaction fastest?",
        "options": json.dumps(["CH₃-Cl", "(CH₃)₂CH-Cl", "(CH₃)₃C-Cl", "CH₃CH₂-Cl"]),
        "correct_answer": "CH₃-Cl",
        "explanation": "SN2 rate: Primary > Secondary > Tertiary. CH₃-Cl is methyl halide (most reactive for SN2)",
        "tags": json.dumps(["organic", "reaction_mechanism", "substitution", "jee_advanced"])
    },
    
    # Inorganic Chemistry
    {
        "title": "Periodic Table - Ionization Energy",
        "description": "Predict periodic trends",
        "topic": "inorganic_chemistry",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "Which element has highest first ionization energy?",
        "options": json.dumps(["Li", "Be", "B", "C"]),
        "correct_answer": "Be",
        "explanation": "Ionization energy increases across period. Exception: Be > B due to stable 2s² configuration",
        "tags": json.dumps(["inorganic", "periodic_table", "ionization", "jee_main"])
    },
    {
        "title": "Chemical Bonding - Hybridization",
        "description": "Determine hybridization state",
        "topic": "inorganic_chemistry",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "What is the hybridization of carbon in CH₄?",
        "options": json.dumps(["sp", "sp²", "sp³", "sp³d"]),
        "correct_answer": "sp³",
        "explanation": "4 sigma bonds → 4 hybrid orbitals → sp³ hybridization, tetrahedral geometry",
        "tags": json.dumps(["inorganic", "bonding", "hybridization", "jee_main"])
    },
    {
        "title": "Coordination Compounds - Nomenclature",
        "description": "Name coordination complex",
        "topic": "inorganic_chemistry",
        "difficulty": 8,
        "content_type": "multiple_choice",
        "question_text": "What is the IUPAC name of [Co(NH₃)₆]Cl₃?",
        "options": json.dumps(["Hexaamminecobalt(III) chloride", "Cobalt hexaammine trichloride", "Hexaamine cobaltate(III) chloride", "Trichloridohexaamminecobalt"]),
        "correct_answer": "Hexaamminecobalt(III) chloride",
        "explanation": "Ligands alphabetically, then metal with oxidation state, then counter ion: Hexaamminecobalt(III) chloride",
        "tags": json.dumps(["inorganic", "coordination", "nomenclature", "jee_advanced"])
    },
    
    # ==================== MATHEMATICS ====================
    # Algebra
    {
        "title": "Quadratic Equations - Sum and Product of Roots",
        "description": "Find sum and product of roots",
        "topic": "algebra",
        "difficulty": 5,
        "content_type": "multiple_choice",
        "question_text": "For equation x² - 5x + 6 = 0, find sum of roots.",
        "options": json.dumps(["3", "4", "5", "6"]),
        "correct_answer": "5",
        "explanation": "Sum of roots = -b/a = -(-5)/1 = 5",
        "tags": json.dumps(["algebra", "quadratic", "roots", "jee_main"])
    },
    {
        "title": "Sequences and Series - Arithmetic Progression",
        "description": "Find nth term of AP",
        "topic": "algebra",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "In an AP, if a = 5, d = 3, find 10th term.",
        "options": json.dumps(["29", "32", "35", "38"]),
        "correct_answer": "32",
        "explanation": "aₙ = a + (n-1)d = 5 + (10-1)×3 = 5 + 27 = 32",
        "tags": json.dumps(["algebra", "sequences", "ap", "jee_main"])
    },
    {
        "title": "Complex Numbers - Modulus and Argument",
        "description": "Calculate modulus of complex number",
        "topic": "algebra",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "Find |3 + 4i|",
        "options": json.dumps(["3", "4", "5", "7"]),
        "correct_answer": "5",
        "explanation": "|z| = √(a² + b²) = √(3² + 4²) = √(9 + 16) = √25 = 5",
        "tags": json.dumps(["algebra", "complex_numbers", "modulus", "jee_main"])
    },
    {
        "title": "Matrices - Determinant",
        "description": "Calculate determinant of 2×2 matrix",
        "topic": "algebra",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "Find determinant of matrix [[2,3],[1,4]]",
        "options": json.dumps(["5", "6", "7", "8"]),
        "correct_answer": "5",
        "explanation": "|A| = ad - bc = (2×4) - (3×1) = 8 - 3 = 5",
        "tags": json.dumps(["algebra", "matrices", "determinant", "jee_main"])
    },
    
    # Calculus
    {
        "title": "Limits - Basic Limits",
        "description": "Evaluate limit of function",
        "topic": "calculus",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "Find lim(x→2) (x² - 4)/(x - 2)",
        "options": json.dumps(["0", "2", "4", "undefined"]),
        "correct_answer": "4",
        "explanation": "lim(x→2) (x² - 4)/(x - 2) = lim(x→2) (x+2)(x-2)/(x-2) = lim(x→2) (x+2) = 4",
        "tags": json.dumps(["calculus", "limits", "jee_main"])
    },
    {
        "title": "Differentiation - Power Rule",
        "description": "Find derivative using power rule",
        "topic": "calculus",
        "difficulty": 5,
        "content_type": "multiple_choice",
        "question_text": "Find dy/dx for y = x³",
        "options": json.dumps(["x²", "2x²", "3x²", "4x²"]),
        "correct_answer": "3x²",
        "explanation": "d/dx(xⁿ) = nxⁿ⁻¹, so d/dx(x³) = 3x²",
        "tags": json.dumps(["calculus", "differentiation", "power_rule", "jee_main"])
    },
    {
        "title": "Integration - Indefinite Integral",
        "description": "Evaluate indefinite integral",
        "topic": "calculus",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "Find ∫2x dx",
        "options": json.dumps(["x² + C", "2x² + C", "x²/2 + C", "2x + C"]),
        "correct_answer": "x² + C",
        "explanation": "∫2x dx = 2∫x dx = 2(x²/2) + C = x² + C",
        "tags": json.dumps(["calculus", "integration", "indefinite", "jee_main"])
    },
    {
        "title": "Definite Integration - Area Under Curve",
        "description": "Calculate definite integral",
        "topic": "calculus",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "Evaluate ∫₀² x² dx",
        "options": json.dumps(["4/3", "8/3", "4", "8"]),
        "correct_answer": "8/3",
        "explanation": "∫₀² x² dx = [x³/3]₀² = 8/3 - 0 = 8/3",
        "tags": json.dumps(["calculus", "definite_integral", "jee_advanced"])
    },
    {
        "title": "Differential Equations - First Order",
        "description": "Solve first order differential equation",
        "topic": "calculus",
        "difficulty": 8,
        "content_type": "multiple_choice",
        "question_text": "Solution of dy/dx = y is:",
        "options": json.dumps(["y = x + C", "y = Ceˣ", "y = e^(x+C)", "y = ln(x) + C"]),
        "correct_answer": "y = Ceˣ",
        "explanation": "dy/y = dx → ln|y| = x + C₁ → y = e^(x+C₁) = e^C₁ · eˣ = Ceˣ",
        "tags": json.dumps(["calculus", "differential_equations", "jee_advanced"])
    },
    
    # Coordinate Geometry
    {
        "title": "Straight Line - Slope",
        "description": "Calculate slope of line",
        "topic": "coordinate_geometry",
        "difficulty": 5,
        "content_type": "multiple_choice",
        "question_text": "Find slope of line passing through (1,2) and (3,6)",
        "options": json.dumps(["1", "2", "3", "4"]),
        "correct_answer": "2",
        "explanation": "m = (y₂-y₁)/(x₂-x₁) = (6-2)/(3-1) = 4/2 = 2",
        "tags": json.dumps(["coordinate_geometry", "straight_line", "slope", "jee_main"])
    },
    {
        "title": "Circle - Standard Equation",
        "description": "Find equation of circle",
        "topic": "coordinate_geometry",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "Equation of circle with center (0,0) and radius 5 is:",
        "options": json.dumps(["x² + y² = 5", "x² + y² = 10", "x² + y² = 25", "x + y = 5"]),
        "correct_answer": "x² + y² = 25",
        "explanation": "Standard form: (x-h)² + (y-k)² = r², with h=0, k=0, r=5: x² + y² = 25",
        "tags": json.dumps(["coordinate_geometry", "circle", "jee_main"])
    },
    {
        "title": "Parabola - Focus and Directrix",
        "description": "Properties of parabola",
        "topic": "coordinate_geometry",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "For parabola y² = 4ax, the focus is at:",
        "options": json.dumps(["(a, 0)", "(0, a)", "(2a, 0)", "(0, 2a)"]),
        "correct_answer": "(a, 0)",
        "explanation": "For parabola y² = 4ax, focus is at (a, 0) and directrix is x = -a",
        "tags": json.dumps(["coordinate_geometry", "conic_sections", "parabola", "jee_advanced"])
    },
    
    # Trigonometry
    {
        "title": "Trigonometric Ratios - Basic Values",
        "description": "Find trigonometric ratio",
        "topic": "trigonometry",
        "difficulty": 5,
        "content_type": "multiple_choice",
        "question_text": "Find sin(30°)",
        "options": json.dumps(["0", "1/2", "√3/2", "1"]),
        "correct_answer": "1/2",
        "explanation": "sin(30°) = 1/2 (standard value)",
        "tags": json.dumps(["trigonometry", "ratios", "jee_main"])
    },
    {
        "title": "Trigonometric Identities - Pythagorean Identity",
        "description": "Apply trigonometric identity",
        "topic": "trigonometry",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "If sin(θ) = 3/5, find cos(θ) (θ in first quadrant)",
        "options": json.dumps(["3/5", "4/5", "5/3", "5/4"]),
        "correct_answer": "4/5",
        "explanation": "sin²θ + cos²θ = 1 → (3/5)² + cos²θ = 1 → cos²θ = 1 - 9/25 = 16/25 → cosθ = 4/5",
        "tags": json.dumps(["trigonometry", "identities", "jee_main"])
    },
    {
        "title": "Inverse Trigonometric Functions",
        "description": "Evaluate inverse trig function",
        "topic": "trigonometry",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "Find sin⁻¹(1/2)",
        "options": json.dumps(["π/6", "π/4", "π/3", "π/2"]),
        "correct_answer": "π/6",
        "explanation": "sin⁻¹(1/2) = π/6 (30°), since sin(π/6) = 1/2",
        "tags": json.dumps(["trigonometry", "inverse", "jee_advanced"])
    },
    
    # Vectors and 3D Geometry
    {
        "title": "Vector Addition",
        "description": "Add two vectors",
        "topic": "vectors",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "If a⃗ = 2î + 3ĵ and b⃗ = 4î - ĵ, find |a⃗ + b⃗|",
        "options": json.dumps(["2√10", "√40", "6", "2√5"]),
        "correct_answer": "2√10",
        "explanation": "a⃗ + b⃗ = 6î + 2ĵ, |a⃗ + b⃗| = √(6² + 2²) = √40 = 2√10",
        "tags": json.dumps(["vectors", "addition", "magnitude", "jee_main"])
    },
    {
        "title": "Dot Product of Vectors",
        "description": "Calculate scalar product",
        "topic": "vectors",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "Find a⃗ · b⃗ if a⃗ = î + 2ĵ + 3k̂ and b⃗ = 2î - ĵ + k̂",
        "options": json.dumps(["0", "1", "2", "3"]),
        "correct_answer": "3",
        "explanation": "a⃗ · b⃗ = (1)(2) + (2)(-1) + (3)(1) = 2 - 2 + 3 = 3",
        "tags": json.dumps(["vectors", "dot_product", "jee_main"])
    },
    
    # Probability and Statistics
    {
        "title": "Probability - Basic Probability",
        "description": "Calculate simple probability",
        "topic": "probability",
        "difficulty": 5,
        "content_type": "multiple_choice",
        "question_text": "A die is thrown. What is probability of getting an even number?",
        "options": json.dumps(["1/6", "1/3", "1/2", "2/3"]),
        "correct_answer": "1/2",
        "explanation": "Even numbers: {2,4,6}, P(even) = 3/6 = 1/2",
        "tags": json.dumps(["probability", "basic", "jee_main"])
    },
    {
        "title": "Permutations and Combinations",
        "description": "Calculate number of arrangements",
        "topic": "probability",
        "difficulty": 6,
        "content_type": "multiple_choice",
        "question_text": "How many ways can 5 books be arranged on a shelf?",
        "options": json.dumps(["20", "60", "120", "720"]),
        "correct_answer": "120",
        "explanation": "Number of arrangements = 5! = 5×4×3×2×1 = 120",
        "tags": json.dumps(["probability", "permutations", "jee_main"])
    },
    {
        "title": "Binomial Theorem",
        "description": "Expand binomial expression",
        "topic": "algebra",
        "difficulty": 7,
        "content_type": "multiple_choice",
        "question_text": "Find coefficient of x² in (1+x)⁴",
        "options": json.dumps(["4", "6", "8", "12"]),
        "correct_answer": "6",
        "explanation": "Coefficient of x² in (1+x)⁴ = ⁴C₂ = 4!/(2!×2!) = 6",
        "tags": json.dumps(["algebra", "binomial_theorem", "jee_main"])
    }
]


def populate_database():
    """Populate database with JEE questions"""
    db: Session = SessionLocal()
    
    try:
        print("🎓 Starting JEE Question Database Population...")
        print("=" * 60)
        
        # Check if content already exists
        existing_count = db.query(Content).count()
        if existing_count > 0:
            print(f"⚠️  Database already has {existing_count} questions.")
            response = input("Do you want to add more questions? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("❌ Cancelled. Exiting...")
                return
        
        added_count = 0
        skipped_count = 0
        
        for question_data in JEE_QUESTIONS:
            # Check if question already exists
            existing = db.query(Content).filter(
                Content.title == question_data["title"]
            ).first()
            
            if existing:
                print(f"⏭️  Skipping: {question_data['title']} (already exists)")
                skipped_count += 1
                continue
            
            # Create new content
            content = Content(**question_data)
            db.add(content)
            added_count += 1
            print(f"✅ Added: {question_data['title']} (Difficulty: {question_data['difficulty']}/10)")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("📊 Summary:")
        print(f"   ✅ Added: {added_count} questions")
        print(f"   ⏭️  Skipped: {skipped_count} questions")
        print(f"   📚 Total in DB: {db.query(Content).count()} questions")
        print("=" * 60)
        print("\n🎉 Database population complete!")
        print("\n📋 Question Distribution:")
        
        # Show distribution by topic
        from sqlalchemy import func as sqlfunc, text
        topics = db.execute(text("SELECT topic, COUNT(*) as count FROM content GROUP BY topic")).fetchall()
        for topic, count in topics:
            print(f"   • {topic}: {count} questions")
        
        print("\n🔢 Difficulty Distribution:")
        difficulties = db.execute(text("SELECT difficulty, COUNT(*) as count FROM content GROUP BY difficulty ORDER BY difficulty")).fetchall()
        for diff, count in difficulties:
            print(f"   • Level {diff}/10: {count} questions")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "🎓" * 30)
    print("JEE Question Database Populator")
    print("Past 10 Years Pattern (2015-2024)")
    print("🎓" * 30 + "\n")
    
    populate_database()
