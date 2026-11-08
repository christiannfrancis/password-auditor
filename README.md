# Password Strength and Policy Auditor

ECE 2260 Group Project

## Purpose
Build a Python program that checks passwords and explains their weaknesses.

## Current Features
- Checks length, uppercase, lowercase, numbers, and symbols
- Checks a list of common passwords
- Finds listed dictionary words
- Detects some letter substitutions, such as @ for a
- Flags common passwords with numbers or symbols added
- Detects repeated characters and chunks
- Detects alphabet, number, and keyboard sequences
- Estimates entropy
- Handles empty input and missing word-list files

## Run
py password_auditor.py

Keep common_passwords.txt and dictionary_words.txt in the same folder
as password_auditor.py. No additional packages are needed yet.

## Testing
py test_password_auditor.py

The test script runs 43 checks and creates week2_test_results.csv.
These tests check specific examples and errors, not overall accuracy
on every possible password.

## Entropy
The estimate uses password length multiplied by log2 of the inferred
character pool. It assumes characters were chosen randomly.
Predictable words and patterns can make the estimate misleading.
This model supports printable ASCII characters.

## Limitations
The word lists are small starter lists, not a full dictionary or a
database of leaked passwords. The pattern checks can miss weaknesses
or flag harmless patterns. Passing the checks does not guarantee
a strong password. Use made-up sample passwords for testing.

## Next Steps
- Strength scoring and improvement suggestions
- CSV batch analysis and export
- NumPy summaries and charts
- Larger sample dataset and performance measurements
- Final report and presentation for November 30