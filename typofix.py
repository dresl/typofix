# copyright DR
import sys, os, re


def regex_replace_tie(char, line, match_pattern, replace_pattern):
    """
    Replaces space by tie.
    Match pattern is used for match in regex, replace for replasing that match pattern.
    """
    return re.subn(
        f"{match_pattern}{char}",
        "{}{}".format(replace_pattern, char.replace(" ", "~").replace("\\.", ".")),
        line,
    )


class TypoFixer:

    STANDALONE_CHARSET = [
        r"K ",
        r"k ",
        r"S ",
        r"s ",
        r"V ",
        r"v ",
        r"Z ",
        r"z ",
        r"O ",
        r"o ",
        r"U ",
        r"u ",
        r"A ",
        r"a ",
        r"I ",
        r"i ",
    ]

    SHORTCUTS_AND_PHRASES = [
        r"j\. č\.",
        r"mn\. č\.",
        r"př\. n\. l\.",
        r"s\. r\. o\.",
        r"n\. l\.",
        r"č\. p\.",
        r"t\. r\.",
        r"t\. č\.",
        r"v\. r\.",
        r"V\. r\.",
        r"n\. m\.",
        r"tj\. ",
        r"tzv\. ",
        r"s\. ",
        r"č\. ",
        r"r\. o\.",
        r"a\. s\.",
        r"k\. s\.",
        r"v\. o\. s\.",
        r"voj\. ",
        r"čet\. ",
        r"rtm\. ",
        r"por\. ",
        r"kpt\. ",
        r"plk\. ",
        r"gen\. ",
        r"Bc\. ",
        r"BcA\. ",
        r"doc\. ",
        r"dr\. h\. c\. ",
        r"Ing\. arch\. ",
        r"Ing\. ",
        r"JUDr\. ",
        r"MDDr\. ",
        r"MgA\. ",
        r"Mgr\. ",
        r"MUDr\. ",
        r"MVDr\. ",
        r"PharmDr\. ",
        r"PhDr\. ",
        r"prof\. ",
        r"RNDr\. ",
        r"Th\.D\. ",
        r"ThDr\. ",
        r"ThLic\. ",
    ]

    ACADEMIC_DEGREES_AFTER_SURNARE = [
        r" DiS\.",
        r" Ph\.D\.",
        r" Dr\.",
        r" Th\.D\.",
        r" CSc\.",
        r" DrSc\.",
        r" DSc\.",
    ]

    UNITS = [
        r"nm",
        r"mm",
        r"cm",
        r"dm",
        r"m",
        r"km",
        r"%",
        r"g",
        r"mg",
        r"dkg",
        r"kg",
        r"t",
    ]

    def __init__(self, params, *args, **kwargs):
        if not self._check_params(params):
            exit(1)
        self.file = params[1]

    def _check_params(self, params):
        """
        Checks program params
        """
        if len(params) != 2:
            self.show_help()
            return False
        if params[1] in ["-h", "typofix.py"]:
            self.show_help()
            return False
        if not os.path.isfile(params[1]):
            print(f"File '{params[1]}' does not exist.")
            return False
        return True

    @staticmethod
    def show_help():
        """
        Program helper
        """
        print("Typofixer help:")
        print("  -h     show this help")
        print("  usage: python typofix.py file_to_fix")

    def start(self):
        print(f"\033[93mstarting typography fixing for file '{self.file}' ...\033[0m")
        with open(self.file, "r") as original_file:
            with open(
                self.file.rsplit(".", 1)[0]
                + "_converted."
                + self.file.rsplit(".", 1)[1],
                "w+",
            ) as conv_file:
                fixes = 0
                for line in original_file.readlines():
                    _line = line
                    # standalone chars
                    _line, line_fixes = self.parse_standalone_charset(_line)
                    fixes += line_fixes
                    # phrases
                    _line, line_fixes = self.parse_shortcuts_and_phrases(_line)
                    fixes += line_fixes
                    # academic degrees
                    _line, line_fixes = self.parse_academic_degrees_after_surname(_line)
                    fixes += line_fixes
                    # brackets
                    _line, line_fixes = self.repair_brackets(_line)
                    fixes += line_fixes
                    # units
                    _line, line_fixes = self.repair_units(_line)
                    fixes += line_fixes
                    conv_file.write(_line)
                print(f"There were {fixes} changes.")
            conv_file.close()
        original_file.close()

    def parse_standalone_charset(self, line):
        fixes = 0
        for char in self.STANDALONE_CHARSET:
            line, num = regex_replace_tie(char, line, " ", " ")
            fixes += num
            # if num != 0:
            #     print(line, fixes)
            # beginning of line
            line, num = regex_replace_tie(char, line, "^", "")
            fixes += num
            # if num != 0:
            #     print(line, fixes)
        return line, fixes

    def parse_shortcuts_and_phrases(self, line):
        """
        Fix common phrases
        """
        fixes = 0
        for char in self.SHORTCUTS_AND_PHRASES:
            line, num = regex_replace_tie(char, line, " ", " ")
            fixes += num
            if num != 0:
                print(line, fixes)
            # beginning of line
            line, num = regex_replace_tie(char, line, "^", "")
            fixes += num
            if num != 0:
                print(line, fixes)
            # after tie
            line, num = regex_replace_tie(char, line, "~", "~")
            fixes += num
            if num != 0:
                print(line, fixes)
            # in the beginning of bracket
            line, num = regex_replace_tie(char, line, r"\(", "(")
            fixes += num
            if num != 0:
                print(line, fixes)
        return line, fixes

    def parse_academic_degrees_after_surname(self, line):
        fixes = 0
        for char in self.ACADEMIC_DEGREES_AFTER_SURNARE:
            line, num = regex_replace_tie(char, line, "", "")
            fixes += num
            if num != 0:
                print(line, fixes)
        return line, fixes

    def repair_brackets(self, line):
        fixes = 0
        line, num = re.subn(r" \( ", " (", line)
        fixes += num
        if num != 0:
            print(line, fixes)
        line, num = re.subn(r" \) ", ") ", line)
        fixes += num
        if num != 0:
            print(line, fixes)
        line, num = re.subn(r" \)\.", ").", line)
        fixes += num
        if num != 0:
            print(line, fixes)
        line, num = re.subn(r" ÷ ", "~÷~", line)
        fixes += num
        if num != 0:
            print(line, fixes)
        line, num = re.subn(r" × ", "~×~", line)
        fixes += num
        if num != 0:
            print(line, fixes)
        return line, fixes

    def repair_units(self, line):
        fixes = 0
        if not line.startswith(("\\newpage", "\\begin", "\\emptypage")):
            for char in self.UNITS:
                line, num = re.subn(
                    f" {char}(?![a-zA-Z0-9žščřďťňěéíáýůúóöŽŠČŘĎŤŇĚÉÍÁÝŮÚÓÖ])",
                    "~{}".format(char.replace(" ", "~").replace("\\.", ".")),
                    line,
                )
                fixes += num
                if num != 0:
                    print(line, fixes)
        return line, fixes


if __name__ == "__main__":
    typofix = TypoFixer(sys.argv)
    typofix.start()
