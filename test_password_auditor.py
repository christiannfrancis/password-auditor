import csv
import io
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import password_auditor as auditor


def main():
    common = auditor.load_words("common_passwords.txt")
    words = auditor.load_words("dictionary_words.txt")
    results = []

    def record(name, expected, actual):
        status = "PASS" if expected == actual else "FAIL"
        results.append([name, expected, actual, status])

    original_samples = [
        ("abc", 1),
        ("ABC", 1),
        ("123456", 1),
        ("!!!!!!!!!!!!", 2),
        ("abcdefghijkl", 2),
        ("Abcdefghijkl", 3),
        ("Abcdefghijk1", 4),
        ("Abcdefghij1!", 5),
        ("Abc1!", 4),
        ("Password123!", 5)
    ]

    for password, expected in original_samples:
        result = auditor.analyze_password(password, common, words)
        record("Original checks: " + password, expected, result["passed"])

    pattern_tests = [
        ("Common uppercase", "PASSWORD123", "common", True),
        ("Not listed", "vR8!mT2#zK6?", "common", False),
        ("Added digits and symbol", "Password123!", "decorated_common", True),
        ("Exact common match", "password", "decorated_common", False),
        ("Word inside password", "MyFootball9!", "dictionary_words", ["football"]),
        ("Letter substitutions", "P@ssw0rd123!", "dictionary_words", ["password"]),
        ("No listed words", "vR8!mT2#zK6?", "dictionary_words", []),
        ("Triple character", "aaaB7!", "repeated", True),
        ("Repeated whole password", "abcabcabc", "repeated", True),
        ("Repeated inner chunk", "xyABAB9!", "repeated", True),
        ("Only two identical letters", "aaB7!", "repeated", False),
        ("Separated chunks", "abXabY", "repeated", False),
        ("Digit sequence", "X1234!z", "sequence", True),
        ("Reverse digits", "X4321!z", "sequence", True),
        ("Alphabet sequence", "xABCD!9", "sequence", True),
        ("Reverse alphabet", "xDCBA!9", "sequence", True),
        ("Keyboard sequence", "Qwerty!9", "sequence", True),
        ("Below sequence threshold", "abc!9", "sequence", False),
        ("Empty repetition check", "", "repeated", False),
        ("Single character", "a", "repeated", False)
    ]

    for name, password, check, expected in pattern_tests:
        result = auditor.analyze_password(password, common, words)
        record(name, expected, result[check])

    entropy_tests = [
        ("", 0.0),
        ("a", 4.7),
        ("1234", 13.29),
        ("Aa1!", 26.22),
        ("a ", 9.51),
        ("é", None)
    ]

    for password, expected in entropy_tests:
        actual = auditor.estimate_entropy(password)
        record("Entropy: " + repr(password), expected, actual)

    for password in ["", "   ", "x" * 257]:
        output = io.StringIO()

        with redirect_stdout(output):
            auditor.check_password(password, common, words)

        record(
            "Invalid input, length " + str(len(password)),
            True,
            "Please" in output.getvalue()
        )

    with tempfile.TemporaryDirectory() as directory:
        with patch.object(auditor, "FOLDER", Path(directory)):
            output = io.StringIO()

            with redirect_stdout(output):
                auditor.main()

            record(
                "Missing word lists",
                True,
                "Could not load" in output.getvalue()
            )

            for filename in ["common_passwords.txt", "dictionary_words.txt"]:
                (Path(directory) / filename).write_text("", encoding="utf-8")

            output = io.StringIO()

            with redirect_stdout(output):
                auditor.main()

            record("Empty word lists", True, "empty" in output.getvalue())

    output = io.StringIO()

    with patch("builtins.input", side_effect=["invalid", "1", "Password123!", "2"]):
        with redirect_stdout(output):
            auditor.main()

    record("Invalid menu option", True, "Please enter 1 or 2" in output.getvalue())
    record(
        "Menu checks a password",
        True,
        "Common password with numbers" in output.getvalue()
    )

    with open(
        auditor.FOLDER / "week2_test_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["test", "expected", "actual", "result"])
        writer.writerows(results)

    passed = 0

    for row in results:
        if row[3] == "PASS":
            passed += 1
        else:
            print("FAILED:", row)

    print(str(passed) + "/" + str(len(results)) + " tests passed.")
    print("Results saved to week2_test_results.csv.")

    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())