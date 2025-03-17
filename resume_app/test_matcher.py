from matcher import analyze_resume_against_job

resume_text = """
Experienced software engineer skilled in Python development.
Strong knowledge of software engineering principles and problem-solving.
Developed clean, efficient code for multiple projects.
"""

job_text = """
We are looking for a skilled software engineer with experience in Python development.
The ideal candidate will have expertise in software engineering principles, problem-solving,
and writing clean, efficient code. python python python
"""

match_results = analyze_resume_against_job(resume_text, job_text)

print("\n🔹 Keyword Matches in Resume:")
for word, count in match_results["keyword_matches"].items():
    print(f"{word}: {count} occurrences")

print("\n🔹 Bigram Matches in Resume:")
for bigram, count in match_results["bigram_matches"].items():
    print(f"{bigram}: {count} occurrences")

print("\n❌ Missing Important Keywords:")
print(match_results["missing_keywords"])

print("\n❌ Missing Important Bigrams:")
print(match_results["missing_bigrams"])
