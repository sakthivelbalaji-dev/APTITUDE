"""Seed sample questions when database is empty."""

from app.database import SessionLocal
from app.models.question import Question

SEED_QUESTIONS = [
    # Easy - 15+ samples across topics
    {"question": "If 20% of a number is 50, what is the number?", "option_a": "200", "option_b": "250", "option_c": "300", "option_d": "350", "correct_answer": "B", "difficulty": "easy", "topic": "Percentage"},
    {"question": "What is 15% of 400?", "option_a": "50", "option_b": "60", "option_c": "70", "option_d": "80", "correct_answer": "B", "difficulty": "easy", "topic": "Percentage"},
    {"question": "A shopkeeper sells an item at 10% profit. Cost price is Rs. 500. Selling price?", "option_a": "Rs. 520", "option_b": "Rs. 550", "option_c": "Rs. 575", "option_d": "Rs. 600", "correct_answer": "B", "difficulty": "easy", "topic": "Profit and Loss"},
    {"question": "Average of 10, 20, 30, 40 is?", "option_a": "20", "option_b": "25", "option_c": "30", "option_d": "35", "correct_answer": "B", "difficulty": "easy", "topic": "Average"},
    {"question": "Ratio of 2:3 equals 8:x. Find x.", "option_a": "10", "option_b": "12", "option_c": "14", "option_d": "16", "correct_answer": "B", "difficulty": "easy", "topic": "Ratio"},
    {"question": "A can do work in 10 days, B in 15 days. Together in how many days?", "option_a": "5", "option_b": "6", "option_c": "7", "option_d": "8", "correct_answer": "B", "difficulty": "easy", "topic": "Time and Work"},
    {"question": "Simple interest on Rs. 1000 at 5% for 2 years?", "option_a": "Rs. 50", "option_b": "Rs. 100", "option_c": "Rs. 150", "option_d": "Rs. 200", "correct_answer": "B", "difficulty": "easy", "topic": "Simple Interest"},
    {"question": "Next in series: 2, 4, 8, 16, ?", "option_a": "24", "option_b": "28", "option_c": "32", "option_d": "36", "correct_answer": "C", "difficulty": "easy", "topic": "Number Series"},
    {"question": "25% of 80 equals?", "option_a": "15", "option_b": "20", "option_c": "25", "option_d": "30", "correct_answer": "B", "difficulty": "easy", "topic": "Percentage"},
    {"question": "Mean of 5 numbers is 20. Sum is?", "option_a": "80", "option_b": "100", "option_c": "120", "option_d": "140", "correct_answer": "B", "difficulty": "easy", "topic": "Average"},
    {"question": "3:4 = 15:x. x = ?", "option_a": "18", "option_b": "20", "option_c": "22", "option_d": "24", "correct_answer": "B", "difficulty": "easy", "topic": "Ratio"},
    {"question": "Loss 10% on CP 200. SP?", "option_a": "170", "option_b": "180", "option_c": "190", "option_d": "210", "correct_answer": "B", "difficulty": "easy", "topic": "Profit and Loss"},
    {"question": "6 workers finish job in 12 days. 4 workers take?", "option_a": "15", "option_b": "18", "option_c": "20", "option_d": "24", "correct_answer": "B", "difficulty": "easy", "topic": "Time and Work"},
    {"question": "SI on 2000 at 4% for 3 years?", "option_a": "200", "option_b": "240", "option_c": "280", "option_d": "320", "correct_answer": "B", "difficulty": "easy", "topic": "Simple Interest"},
    {"question": "Series: 5, 10, 20, 40, ?", "option_a": "60", "option_b": "70", "option_c": "80", "option_d": "90", "correct_answer": "C", "difficulty": "easy", "topic": "Number Series"},
    {"question": "What percent is 45 of 180?", "option_a": "20%", "option_b": "25%", "option_c": "30%", "option_d": "35%", "correct_answer": "B", "difficulty": "easy", "topic": "Percentage"},
    {"question": "Average of first 5 natural numbers?", "option_a": "2", "option_b": "3", "option_c": "4", "option_d": "5", "correct_answer": "B", "difficulty": "easy", "topic": "Average"},
    # Medium
    {"question": "Probability of heads in one coin toss?", "option_a": "0.25", "option_b": "0.5", "option_c": "0.75", "option_d": "1", "correct_answer": "B", "difficulty": "medium", "topic": "Probability"},
    {"question": "If CODE is 27, what is DECODE? (A=1)", "option_a": "45", "option_b": "54", "option_c": "63", "option_d": "72", "correct_answer": "A", "difficulty": "medium", "topic": "Coding-Decoding"},
    {"question": "A is father of B. B is sister of C. A is ___ of C.", "option_a": "Brother", "option_b": "Father", "option_c": "Uncle", "option_d": "Cousin", "correct_answer": "B", "difficulty": "medium", "topic": "Blood Relations"},
    {"question": "All cats are animals. Some animals are pets. Conclusion?", "option_a": "All cats are pets", "option_b": "Some cats may be pets", "option_c": "No cat is pet", "option_d": "Cannot determine", "correct_answer": "B", "difficulty": "medium", "topic": "Logical Reasoning"},
    {"question": "5 people in a row. A not at ends. B left of C. Valid?", "option_a": "A in middle only", "option_b": "B always first", "option_c": "C at end possible", "option_d": "None", "correct_answer": "C", "difficulty": "medium", "topic": "Seating Arrangement"},
    {"question": "Table: Sales Mon=100, Tue=120. % increase Tue vs Mon?", "option_a": "15%", "option_b": "20%", "option_c": "25%", "option_d": "30%", "correct_answer": "B", "difficulty": "medium", "topic": "Data Interpretation"},
    {"question": "Two dice thrown. P(sum=7)?", "option_a": "1/12", "option_b": "1/6", "option_c": "1/4", "option_d": "1/3", "correct_answer": "B", "difficulty": "medium", "topic": "Probability"},
    {"question": "BAT coded as 23. CAT coded as?", "option_a": "24", "option_b": "25", "option_c": "26", "option_d": "27", "correct_answer": "A", "difficulty": "medium", "topic": "Coding-Decoding"},
    {"question": "Pointing to man, she said his mother is my mother. Relation?", "option_a": "Sister", "option_b": "Brother", "option_c": "Cousin", "option_d": "Self", "correct_answer": "B", "difficulty": "medium", "topic": "Blood Relations"},
    {"question": "If no A is B and all B is C, then?", "option_a": "No A is C", "option_b": "Some A is C", "option_c": "No A is B only", "option_d": "All A is C", "correct_answer": "C", "difficulty": "medium", "topic": "Logical Reasoning"},
    {"question": "Chart shows 40% Science, 30% Arts. Rest Commerce %?", "option_a": "20", "option_b": "25", "option_c": "30", "option_d": "35", "correct_answer": "C", "difficulty": "medium", "topic": "Data Interpretation"},
    {"question": "P(E)=0.3 for event E. P(not E)?", "option_a": "0.3", "option_b": "0.5", "option_c": "0.7", "option_d": "1", "correct_answer": "C", "difficulty": "medium", "topic": "Probability"},
    {"question": "FISH to GHIT shift +1 each letter pattern. DOG to?", "option_a": "EPH", "option_b": "EPG", "option_c": "FOH", "option_d": "EOG", "correct_answer": "A", "difficulty": "medium", "topic": "Coding-Decoding"},
    {"question": "Ram is taller than Shyam. Shyam taller than Mohan. Tallest?", "option_a": "Mohan", "option_b": "Shyam", "option_c": "Ram", "option_d": "Equal", "correct_answer": "C", "difficulty": "medium", "topic": "Logical Reasoning"},
    {"question": "A,B,C,D sit circle facing center. A opposite C. B left of A. D?", "option_a": "Right of A", "option_b": "Between B and C", "option_c": "Opposite B", "option_d": "Next to C", "correct_answer": "D", "difficulty": "medium", "topic": "Seating Arrangement"},
    {"question": "Revenue Q1=50k Q2=65k. Growth %?", "option_a": "25", "option_b": "30", "option_c": "35", "option_d": "40", "correct_answer": "B", "difficulty": "medium", "topic": "Data Interpretation"},
    {"question": "Bag has 3 red, 2 blue balls. P(red)?", "option_a": "2/5", "option_b": "3/5", "option_c": "1/2", "option_d": "3/4", "correct_answer": "B", "difficulty": "medium", "topic": "Probability"},
]


def seed_database():
    db = SessionLocal()
    try:
        count = db.query(Question).count()
        if count >= 30:
            return
        existing = count
        for q in SEED_QUESTIONS[existing:]:
            db.add(Question(**q))
        db.commit()
    finally:
        db.close()
