import os
import sys
from typing import List

# raw font data (5 rows). Each character width = 6 columns. ```````
DATA = [
    " ***  ****   ***  ****  ***** *****  ***  *   * ***** ***** *   * *     *   * *   *  ***  ****   ***  ****   **** ***** *   * *   * *   * *   * *   * *****        ***                     ***  ***   ****  ****  *   * *****  ***  *****  ***  ***** ",
    "*   * *   * *   * *   * *     *     *     *   *   *      *  *  *  *     ** ** **  * *   * *   * *   * *   * *       *   *   * *   * *   *  * *   * *     *        * ***                   *   *   *       *     * *   * *     *         * *   * *   * ",
    "*   * ****  *     *   * ***   ****  *  ** *****   *      *  ***   *     * * * * * * *   * ****  *   * ****  *****   *   *   * *   * * * *   *     *     *         * * *       *****       *   *   *       *   **  ***** ****  ****      *  ***  ***** ",
    "***** *   * *   * *   * *     *     *   * *   *   *   *  *  *  *  *     *   * *  ** *   * *     *   * *  *      *   *   *   *  * *  ** **  * *    *    *          * * *              ***  *   *   *   ***       *     *     * *   *     * *   *     * ",
    "*   * ****   ***  ****  ***** *      ***  *   * *****  ***  *   * ***** *   * *   *  ***  *      ***  *   * ****    *   *****   *   *   * *   *   *   *****        ***  *****        ***   ***  ***** ***** ****      * ****   ***      *  ***      * "
]

CHAR_WIDTH = 6

# ================================
# COLOR CODES
# ================================
COLORS = {
    "1": "\033[97m",   # White
    "2": "\033[91m",   # Red
    "3": "\033[92m",   # Green
    "4": "\033[93m",   # Yellow
    "5": "\033[94m",   # Blue
    "6": "\033[96m"    # Cyan
}
RESET = "\033[0m"


def char_index(ch: str) -> int:
    ch = ch.upper()
    if ch == " ":
        return 26
    if ch == "@":
        return 27
    if ch == "_":
        return 28
    if ch == "-":
        return 29
    if ch == ".":
        return 30
    if "A" <= ch <= "Z":
        return ord(ch) - ord("A")
    if "0" <= ch <= "9":
        return 31 + int(ch)
    raise ValueError(f"Character '{ch}' not supported")


def render_string(text: str) -> List[str]:
    text = text.upper()
    rows = []
    for data_row in DATA:
        line_chars = []
        for ch in text:
            try:
                idx = char_index(ch)
            except ValueError:
                idx = 26
            start = idx * CHAR_WIDTH
            segment = data_row[start:start + CHAR_WIDTH]
            line_chars.append(segment)
        rows.append("".join(line_chars))
    return rows


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def display_output(lines: List[str], color_code: str):
    print("\n")
    for ln in lines:
        print(color_code + ln + RESET)
    print("\n")


def save_to_file(lines: List[str], filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        for ln in lines:
            f.write(ln + "\n")
    print(f"Saved output to {filename}")


def prompt_text(max_len=15, only_alpha=False, only_digits=False):
    while True:
        text = input(f"Enter text (1 to {max_len} chars): ").strip()
        if not (1 <= len(text) <= max_len):
            print(f"Please enter between 1 and {max_len} characters.")
            continue
        if only_alpha and not text.isalpha():
            print("Only alphabets allowed.")
            continue
        if only_digits and not text.isdigit():
            print("Only digits allowed.")
            continue
        return text


def choose_color():
    print("\nChoose Color:")
    print("1 - White")
    print("2 - Red")
    print("3 - Green")
    print("4 - Yellow")
    print("5 - Blue")
    print("6 - Cyan")
    choice = input("Enter color number (default 1): ").strip()
    return COLORS.get(choice, COLORS["1"])


def show_menu():
    clear_screen()
    print("========= ASCII ART PROJECT =========")
    print("1 - One Character")
    print("2 - Word (Max 15 chars)")
    print("3 - Range (example A-D)")
    print("4 - Only Alphabets")
    print("5 - Only Numbers")
    print("6 - lowercase → UPPERCASE")
    print("7 - Save Previous Output")
    print("8 - Exit")
    print("====================================")


def run():
    last_output = []
    last_color = COLORS["1"]

    while True:
        show_menu()
        choice = input("Enter choice (1-8): ").strip()

        if choice in {"1", "2", "3", "4", "5", "6", "7"}:
            last_color = choose_color()

        if choice == "1":
            txt = prompt_text(max_len=1)
            last_output = render_string(txt)
            clear_screen()
            display_output(last_output, last_color)

        elif choice == "2":
            txt = prompt_text(max_len=15)
            last_output = render_string(txt)
            clear_screen()
            display_output(last_output, last_color)

        elif choice == "3":
            raw = input("Enter range like A-D: ").strip().upper()
            if len(raw) != 3 or raw[1] != "-" or not raw[0].isalpha() or not raw[2].isalpha():
                print("Invalid format.")
                continue
            s = ord(raw[0]) - ord("A")
            e = ord(raw[2]) - ord("A")
            if s > e or (e - s + 1) > 15:
                print("Invalid range or too long.")
                continue
            txt = "".join(chr(ord("A") + i) for i in range(s, e + 1))
            last_output = render_string(txt)
            clear_screen()
            display_output(last_output, last_color)

        elif choice == "4":
            txt = prompt_text(max_len=15, only_alpha=True)
            last_output = render_string(txt)
            clear_screen()
            display_output(last_output, last_color)

        elif choice == "5":
            txt = prompt_text(max_len=15, only_digits=True)
            last_output = render_string(txt)
            clear_screen()
            display_output(last_output, last_color)

        # ============================
        # NEW OPTION 6
        # lowercase → UPPERCASE
        # ============================
        elif choice == "6":
            txt = input("Enter lowercase text: ").strip()
            if not txt.islower():
                print("Please enter only lowercase letters.")
                continue
            converted = txt.upper()
            last_output = render_string(converted)
            clear_screen()
            display_output(last_output, last_color)


        elif choice == "7":
            if not last_output:
                print("Nothing to save.")
            else:
                fname = input("Filename: ").strip() or "ascii_output.txt"
                save_to_file(last_output, fname)

        elif choice == "8":
            print("Goodbye!")
            sys.exit()

        else:
            print("Invalid choice.")

        if choice in {"1", "2", "3", "4", "5", "6", "7"}:
            if input("Save output (y/n)? ").strip().lower() == "y":
                fname = input("Filename: ").strip() or "ascii_output.txt"
                save_to_file(last_output, fname)

        if input("Back to menu (y/n): ").strip().lower() != "y":
            print("Exiting...")
            break


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nInterrupted.")
