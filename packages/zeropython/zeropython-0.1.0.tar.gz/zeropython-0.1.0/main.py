start = int(input("start:"))
end = (tmp_end := int(input("end:"))) + (start < tmp_end or -1)
step = start < end or -1

for n in range(start, end, step):
    # SPECIAL
    BALROG = (n % 666 == 0)
    str_n = str(n)
    NARCISSE = (n == sum(int(digit) ** len(str_n) for digit in str_n if digit != '-'))

    if BALROG:
        print("Balrog!")
        continue
    if NARCISSE:
        print("Narciss")
        continue

    # BASIC
    MULTIPLE_3 = (n % 3 == 0)
    MULTIPLE_5 = (n % 5 == 0)
    MULTIPLE_4 = (n % 4 == 0)
    MULTIPLE_7 = (n % 7 == 0)
    MULTIPLE_10 = (n % 10 == 0)

    # First part
    FLASH = MULTIPLE_3 and MULTIPLE_7
    FIZZ = MULTIPLE_3 and not FLASH

    # Second part
    LIGHT = MULTIPLE_4 and not MULTIPLE_10

    # Third part
    BUZZ = MULTIPLE_5

    predicate_txt_pairs = (
        (FLASH, "Flash"),
        (FIZZ, "Fizz"),
        (LIGHT, "Light"),
        (BUZZ, "Buzz"),
    )

    print("".join(txt for predicate, txt in predicate_txt_pairs if predicate) or n)
