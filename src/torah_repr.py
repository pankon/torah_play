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
        
        if start in self.used:
            return ''.join(out), first_idx, n_added, idx
        """
        while idx < length:
            if idx not in self.used:
                break
            idx += 1
        """

        while idx < length and len(out) < max_read:
            if do_spacing and out and n_added and n_added % grouping == grouping - 1:
                if out[-1] in Letter.reverse_alt_letter_lookup:
                    out[-1] = Letter.reverse_alt_letter_lookup[out[-1]]

                if n_added % (grouping * column_size) == (grouping * column_size) - 1:
                    out.append("\n")
                else:
                    out.append(" ")

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

"""
        out.append(combo)
        for i in range(18):
            combo, new_idx = torah_repr.read(new_idx, 3, 50, max)
            out.append(combo)
    
        idx = 0
        mixed_out = []
        split_segments = [segment.split(" ") for segment in out]
        for idx in range(max):
            for group in split_segments:
                if idx >= len(group):
                    break
                mixed_out.append(group[idx])
        """


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
            #print("equals:", ''.join(buffer))

            #print("diff 1:", last[:-equals_idx])
            #print("diff 2:", combo[:-equals_idx])
            last = combo

        # with open("data/out_{}.txt".format(start_idx), "w", encoding="utf-8") as fp:
        #    fp.write(combo) #" ".join(mixed_out))

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
            break

        #if True:
        #    break


    """
    out_new = []
    for i in range(3):
        for checksum in checksums:
            if len(checksum) > i:
                out_new.append(checksum[i])
            else:
                out_new.append(" ")

    print(''.join(out_new))
    """
