

class Letter:
    letters = "אבגדהוזחטיכלמנסעפצקרשת"
    alt_letters = "מםפףכךצץנן"
    all_letters = set(letters + alt_letters)
    gematria = [1, 2, 3, 4, 5, 6, 7, 8, 9,
                10, 20, 30, 40, 50, 60, 70, 80, 90,
                100, 200, 300, 400]

    alt_letter_lookup = dict()
    reverse_alt_letter_lookup = dict()
    gematria_lookup = dict()

    def __init__(self, hebrew_letter):
        self.letter = hebrew_letter
        self.value = Letter.convert_hebrew_letter(hebrew_letter)

    @classmethod
    def convert_hebrew_letter(cls, hebrew_letter):
        if not cls.gematria_lookup:
            idx = 0
            while idx < len(cls.alt_letters):
                cls.alt_letter_lookup[cls.alt_letters[idx + 1]] = cls.alt_letters[idx]
                cls.reverse_alt_letter_lookup[cls.alt_letters[idx]] = cls.alt_letters[idx + 1]
                #print(cls.alt_letters[idx: idx+2])
                idx += 2

            for letter, value in zip(cls.letters, cls.gematria):
                cls.gematria_lookup[letter] = value

            for alt_letter, normal_letter in cls.alt_letter_lookup.items():
                cls.gematria_lookup[alt_letter] = cls.gematria_lookup[normal_letter]

        return cls.gematria_lookup[hebrew_letter]



