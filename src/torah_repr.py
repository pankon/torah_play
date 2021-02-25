from src.letter import Letter


class TorahRepr:
    def __init__(self, filename: str):
        with open(filename, "r", encoding="utf-8") as fp:
            data = fp.read()

        self.letters = []
        for letter in data:
            current_letter = Letter(letter)
            #print(current_letter.value)
            self.letters.append(current_letter)

        self.used = set()

    def read(self, start, grouping, column_size, max_read, do_spacing=True):
        idx = start
        first_idx = -1
        length = len(self.letters)
        out = []
        n_added = 0

        # do not allow starting from an already visited letter
        if start in self.used:
            return ''.join(out), first_idx, n_added, idx

        while idx < length and len(out) < max_read:
            self.pretty_format(column_size, do_spacing, grouping, n_added, out)

            current = self.letters[idx]
            #if idx not in self.used:
            if current.letter in Letter.alt_letter_lookup:
                out.append(Letter.alt_letter_lookup[current.letter])
            else:
                out.append(current.letter)
            n_added += 1
            self.used.add(idx)

            if first_idx == -1:
                first_idx = current.value

            idx += current.value
        return ''.join(out), first_idx, n_added, idx

    def pretty_format(self, column_size, do_spacing, grouping, n_added, out):
        if do_spacing and out and n_added and n_added % grouping == grouping - 1:
            if out[-1] in Letter.reverse_alt_letter_lookup:
                out[-1] = Letter.reverse_alt_letter_lookup[out[-1]]

            if n_added % (grouping * column_size) == (grouping * column_size) - 1:
                out.append("\n")
            else:
                out.append(" ")


if __name__ == "__main__":
    torah_repr = TorahRepr("data/torah.txt")
    out = []
    max = len(torah_repr.letters)
    start_idx = 6
    required_identical = 5
    finish = ["אשרעשהמשהלעיניכלישראל"]
    checksums = ["מכרשובאתנלחההאש"]
    last = None
    min = 300000

    show_diff = False
    show_equal_section = False
    create_output_files = False

    for start_idx in range(0, len(torah_repr.letters)):
        combo, new_idx, n_added, idx = torah_repr.read(start_idx, 3, 50, max, do_spacing=False)
        if not n_added:
            continue

        if not last:
            last = combo
            continue
        else:
            equals_idx = 1
            buffer = []
            while combo[-equals_idx] == last[-equals_idx]:
                buffer.append(combo[-equals_idx])
                equals_idx += 1
                if equals_idx > len(combo) or equals_idx > len(last):
                    break

            if show_diff:
                print("diff:", last[:-equals_idx])

            if show_equal_section:
                print("equal section:", ''.join(buffer))

            last = combo

        if create_output_files:
            with open("data/out_{}.txt".format(start_idx), "w", encoding="utf-8") as fp:
                fp.write(combo)

        last_value = Letter.convert_hebrew_letter(combo[-1])
        test = ''.join(letter.letter for letter in torah_repr.letters[idx - last_value - 1:])
        if test not in finish:
            finish.append(test)
            #print(start_idx, test)

        current_checksum = combo[-(3*required_identical):]
        if current_checksum not in checksums:
            #print("extra:", ''.join(letter.letter for letter in torah_repr.letters[start_idx:]))
            #print("read_text:", combo)
            print("checksum:", current_checksum, start_idx)
            checksums.append(current_checksum)
            required_identical -= 1
            if required_identical <= 0:
                required_identical = 1

            # 289,426 letter
            break

