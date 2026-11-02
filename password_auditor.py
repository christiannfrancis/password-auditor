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