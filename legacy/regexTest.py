import re

def extract_question_data(text):
    points_pattern = r"(\d+)\s+point\(s\)"

    # Find the points
    match = re.search(points_pattern, text)
    print(match)
    # If a match is found, extract the points
    if match:
        allocated_points = match.group(1)
        text = re.sub(points_pattern, '', text).strip()

    # Regex to capture the question after the question number (e.g., "18. Question")
    question_pattern = r"\d+\.\s*Question\s*(.*?)(?=\n\s*\d+\.\s)"
    question_match = re.search(question_pattern, text, re.DOTALL)
    
    question = ""
    if question_match:
        question = question_match.group(1).strip()
        text = text[question_match.end():]  # Remove the extracted question from the text

    # Regex to find the correct answer
    correct_answer_pattern = r"(\d\.\s.*?)(?=\s✔|\s)"
    correct_answer_match = re.search(correct_answer_pattern, text)
    
    correct_answer = ""
    if correct_answer_match:
        correct_answer = correct_answer_match.group(1).strip()

    # Regex to capture the options
    options_pattern = r"(\d\.\s.*?)(?=\n\s*\d\.|\n\s*(?:CORRECT|INCORRECT))"

    options = re.findall(options_pattern, text, re.DOTALL)
    
    if options:
        last_option_match = re.search(options[-1], text, re.DOTALL)
        if last_option_match:
            text = text[last_option_match.end():]  # Remove the extracted options from the text

    
    # Regex to capture the justification/explanation
    justification_pattern = r"(CORRECT|INCORRECT)\s?(.*)"
    justification_match = re.search(justification_pattern, text, re.DOTALL)
    
    justification = ""
    if justification_match:
        justification = justification_match.group(2).strip()
        text = text[justification_match.end():]  # Remove the extracted justification from the text

    return {
        "question": question,
        "options": options,
        "allocated_points": allocated_points,
        "correct_answer": correct_answer,
        "justification": justification
    }

# Sample text extraction
pdf_text = """
 51. Question 1 point(s)
 A 56-year-old man presents himself to a walk-in clinic complaining about tiredness, muscle weakness,
 polyuria, and nocturia. The triage nurse finds his blood pressure is 220/125 mm Hg. Recognizing a
 potential medical emergency, she immediately introduces him to the physician on duty. That physician
 treats him with nitroglycerine, which brings the readings down to 175/90 mm Hg. He also gives him a few
 extra nitroglycerine pills, plus prescriptions for hydrochlorothiazide and verapamil and tells him to make an
 appointment with a physician who can treat him on a regular basis because he suspects that he may be
 suffering from a serious condition. Taking his advice, the patient makes an appointment at a local free
 clinic. At this time, his sense of muscle weakness has increased, as has his general feeling of fatigue. In
 addition to the symptoms above, he now also suffers from muscle cramps and constipation. His new
 physician finds his blood pressure to be 190/95 mm Hg, and he also notes a mild cardiac arrhythmia; blood
 serum analysis was normal except for his serum K
 1.  Essential hypertension 
 + level, which is 3.1 mm/L. The patient claims he has been taking the pills
 prescribed by the doctor at the walk-in clinic on a regular basis. Which of the following conditions does this patient most likely suffer from?
2.  Conn syndrome 
 3.  Addison disease
 4.  Cushing syndrome
 5.  Pheochromocytoma
 INCORRECT 
 The correct answer is 2. 
Conn syndrome is an important example of a secondary hypertension, in this case caused by
 aldosteronism. Although some studies suggest it is a rare condition, careful studies find it to be the
 cause of up to 15% of the cases of hypertension and should be suspected in all cases resistant to
 treatment or accompanied by low serum K levels. It is caused by either an adenoma (a
 nonmalignant aldosterone-producing tumor in one of the adrenals), or by bilateral adrenal
 hyperplasia. The former is readily treated by surgery, while the latter generally may be treated with
 spironolactone, an aldosterone antagonist. The condition is diagnosed by measuring serum
 aldosterone and renin levels. In Conn syndrome, aldosterone concentration is elevated while the
 renin level is not in fact, it usually is very low.
 As people age, their blood pressure tends to increase. In fact, in the 1940s, normal systolic blood
 pressure was regarded to be 100 mm Hg plus a person's age. Now, normal pressure is defined in
 terms of the risk for organ damage. Thus, normal pressure for otherwise healthy adults is defined as
 shown in the following table:
 Systolic Diastolic
 Normal <120 And <80
 Prehypertension 120-139 Or 80-89
 High blood
 pressure
 Stage 1 140-159 Or 90-99
 +
Stage 2
 ≥160
 Or
 ≥100
 (Choice 1) For persons with diabetes or chronic renal disease, high blood pressure is defined as
 greater than 130/80 mm Hg because of the greater potential for end-organ damage. Roughly about
 30% of adults over the age of 18 years have hypertension as defined in this table. In most cases,
 there is no specific cause for these higher-than-normal values, and this is called essential
 hypertension. In general, essential hypertension can be distinguished from Conn syndrome by the
 observations that (a) the degree to which the pressure is raised is not as great as in Conn syndrome,
 +
 (b) the pressure responds more readily to medication, and (c) the serum K level stays within normal
 limits. Thus, patients with essential hypertension are less likely to have symptoms due to serum K
 deficiency.
 (Choice 3) is caused by the underproduction of adrenal gland hormones, usually due to an
 +
 autoimmune reaction. Symptoms usually develop gradually and include low blood pressure, muscle
 weakness, bronzing of the skin, weight loss, and fatigue.
 (Choice 4) is caused by chronic exposure of the body to excess cortisol. It sometimes occurs as a
 consequence of long-term treatment of various conditions with cortisol; when it occurs
 spontaneously, it is due to a pituitary adenoma in 70% of the cases. These benign tumors secrete
 excess adrenocorticotropic hormone (ACTH). Usually, a single tumor is present, and the disorder is
 called Cushing disease. The syndrome may also be caused by ACTH-producing tumors found
 outside the pituitary. These ectopic tumors are found in association with small-cell lung cancers
 more than half the time, but may also be caused by thymomas, medullary carcinomas of the thyroid,
 and pancreatic islet cell cancers. Excess cortisol may also arise from carcinoid cells, essentially
 developmentally misplaced adrenal tissue. Cushing syndrome also may arise from an adrenal
 adenoma; these nonmalignant tumors are approximately five times more common in females than
 males and usually first appear at about the age of 40 years. Malignant adrenal cortical tumors are
 the least common cause of Cushing syndrome. In addition to secreting very high levels of cortisol,
 such tumors also usually secret adrenal androgens.
 (Choice 5) Unlike the other choices, a pheochromocytoma is a tumor located in the adrenal medulla
 rather than the cortex; consequently, these tumors secrete excess amounts of the catecholamines
 (epinephrine, norepinephrine, and dopamine) and their metabolic products. Symptoms of a
 pheochromocytoma are those expected to be caused by excess levels of circulating catecholamines,
 including high blood pressure, but generally also including other symptoms, such as severe
headaches, tachycardia and palpitations, severe anxiety including feelings of impending death,
 tremors, chest and/or abdominal pain, nausea, weight loss, and heat intolerance. The classical
 diagnosis is analysis of a 24-hour urine sample for excreted catecholamines plus their metabolic
 products. More recently, a blood test has been developed. Although not as sensitive and not as
 widely available, this test is simpler for the patient to take.
"""

# Extract data from the text
result = extract_question_data(pdf_text)
print(result)