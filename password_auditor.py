def is_common_password(password):
    with open("common_passwords.txt", "r") as file:
        for line in file:
            if password.lower() == line.strip().lower():
                return True
    return False


def has_repeated_pattern(password):
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            return True

    for size in range(1, len(password) // 2 + 1):
        pattern = password[:size]
        repeats = len(password) // size

        if pattern * repeats == password:
            return True

    return False

def check_password(password):
    has_upper = False
    has_lower = False
    has_number = False
    has_symbol = False

    for character in password:
        if character.isupper():
            has_upper = True
        elif character.islower():
            has_lower = True
        elif character.isdigit():
            has_number = True
        elif not character.isspace():
            has_symbol = True

    checks = {
        "At least 12 characters": len(password) >= 12,
        "Uppercase letter": has_upper,
        "Lowercase letter": has_lower,
        "Number": has_number,
        "Symbol": has_symbol
    }

    print("\nPassword check results:")
    passed = 0

    for requirement, result in checks.items():
        if result:
            print(requirement + ": PASS")
            passed += 1
        else:
            print(requirement + ": FAIL")

    print("\nChecks passed:", passed, "out of", len(checks))

    if is_common_password(password):
        print("Warning: This is a common password.")

    if has_repeated_pattern(password):
        print("Warning: This password contains a repeated pattern.")


def main():
    while True:
        print("\nPassword Policy Auditor")
        print("1. Check a sample password")
        print("2. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            password = input("Enter a made-up test password: ")
            check_password(password)
        elif choice == "2":
            break
        else:
            print("Please enter 1 or 2.")


main()