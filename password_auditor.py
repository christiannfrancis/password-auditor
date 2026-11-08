import math
import string
from pathlib import Path

FOLDER = Path(__file__).resolve().parent


def load_words(filename):
    words = []

    with open(FOLDER / filename, "r", encoding="utf-8-sig") as file:
        for line in file:
            word = line.strip().lower()

            if word:
                words.append(word)

    return words


def has_repeated_pattern(password):
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            return True

    for size in range(2, len(password) // 2 + 1):
        for i in range(len(password) - 2 * size + 1):
            first = password[i:i + size]
            second = password[i + size:i + 2 * size]

            if first == second:
                return True

    return False


def has_sequence(password):
    password = password.lower()

    sequences = [
        string.ascii_lowercase,
        string.digits,
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]

    for sequence in sequences:
        for order in [sequence, sequence[::-1]]:
            for i in range(len(order) - 3):
                if order[i:i + 4] in password:
                    return True

    return False


def estimate_entropy(password):
    allowed = string.ascii_letters + string.digits + string.punctuation + " "

    for character in password:
        if character not in allowed:
            return None

    pool = 0

    if any(c in string.ascii_lowercase for c in password):
        pool += 26
    if any(c in string.ascii_uppercase for c in password):
        pool += 26
    if any(c in string.digits for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += 32
    if " " in password:
        pool += 1

    if pool == 0:
        return 0.0

    return round(len(password) * math.log2(pool), 2)


def analyze_password(password, common_passwords, dictionary_words):
    checks = {
        "At least 12 characters": len(password) >= 12,
        "Uppercase letter": any(c.isupper() for c in password),
        "Lowercase letter": any(c.islower() for c in password),
        "Number": any(c.isdigit() for c in password),
        "Symbol": any(
            not c.isalnum() and not c.isspace()
            for c in password
        )
    }

    lower = password.lower()
    normalized = lower.replace("@", "a").replace("0", "o")
    normalized = normalized.replace("$", "s").replace("3", "e")

    words_found = []

    for word in dictionary_words:
        if len(word) >= 4:
            if word in lower or word in normalized:
                words_found.append(word)

    base = lower.strip(string.digits + string.punctuation + " ")

    decorated_common = (
        bool(base)
        and base != lower
        and base in common_passwords
    )

    return {
        "checks": checks,
        "passed": sum(checks.values()),
        "common": lower in common_passwords,
        "dictionary_words": words_found,
        "decorated_common": decorated_common,
        "repeated": has_repeated_pattern(password),
        "sequence": has_sequence(password),
        "entropy": estimate_entropy(password)
    }


def check_password(password, common_passwords, dictionary_words):
    if not password or password.isspace():
        print("Please enter a sample password.")
        return

    if len(password) > 256:
        print("Please use at most 256 characters.")
        return

    result = analyze_password(password, common_passwords, dictionary_words)

    print("\nPassword check results:")

    for requirement, passed in result["checks"].items():
        if passed:
            print(requirement + ": PASS")
        else:
            print(requirement + ": FAIL")

    print("\nChecks passed:", result["passed"], "out of 5")

    warnings = []

    if result["common"]:
        warnings.append("Matches our common-password list.")

    if result["dictionary_words"]:
        warnings.append(
            "Contains listed words: "
            + ", ".join(result["dictionary_words"])
        )

    if result["decorated_common"]:
        warnings.append(
            "Common password with numbers or symbols added at the ends."
        )

    if result["repeated"]:
        warnings.append("Contains repeated characters or chunks.")

    if result["sequence"]:
        warnings.append("Contains a predictable sequence.")

    for warning in warnings:
        print("Warning:", warning)

    if not warnings:
        print("No matches found by the current pattern checks.")

    if result["entropy"] is None:
        print("Entropy estimate unavailable for these characters.")
    else:
        print("Random-choice entropy estimate:", result["entropy"], "bits")

    print("This estimate assumes random character choices.")
    print("Words and patterns can make a password easier to guess.")
    print("Passing every check does not guarantee a strong password.")


def main():
    try:
        common_passwords = load_words("common_passwords.txt")
        dictionary_words = load_words("dictionary_words.txt")

        if not common_passwords or not dictionary_words:
            print("A word list is empty. Add words before running.")
            return

    except (OSError, UnicodeError) as error:
        print("Could not load word lists:", error)
        print("Keep both text files beside password_auditor.py.")
        return

    while True:
        print("\nPassword Policy Auditor")
        print("1. Check a sample password")
        print("2. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            password = input("Enter a made-up test password: ")
            check_password(password, common_passwords, dictionary_words)
        elif choice == "2":
            break
        else:
            print("Please enter 1 or 2.")


if __name__ == "__main__":
    main()