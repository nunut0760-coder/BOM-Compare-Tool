import re
import pandas as pd
import os
import json
import threading

import tkinter as tk

from tkinter import (
    filedialog,
    messagebox,
    ttk
)


OUTPUT_FOLDER = "BOM_COMPARE_RESULT"
CONFIG_FOLDER = "Config"

os.makedirs(
    CONFIG_FOLDER,
    exist_ok=True
)

IGNORE_WORDS_FILE = os.path.join(
    CONFIG_FOLDER,
    "ignore_words.json"
)

DEFAULT_IGNORE_WORDS = [

    "CERAMIC CAPACITOR",
    "WERAMIC CAPACITOR",
    "HF CHOKE",
    "PBFREE",
    "RESISTOR",
    "CHIP RESISTOR",
    "INDUCTOR",
    "METAL-FILM RESISTOR",
    "0603",
    "METAL-FILM",
    "X7S 0201",
    "SN",
    "C",
    "0805",
    "080",
    "0402",
    "1206",
    "02",
    "50V",

]

# ================IGNORE WORD STORAGE===============

def load_ignore_words():

    if not os.path.exists(
        IGNORE_WORDS_FILE
    ):

        data = []

        for word in DEFAULT_IGNORE_WORDS:

            data.append({

                "word": word,

                "enabled": True

            })

        save_ignore_words(
            data
        )

        return data

    try:

        with open(
            IGNORE_WORDS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        data = []

        for word in DEFAULT_IGNORE_WORDS:

            data.append({

                "word": word,

                "enabled": True

            })

        return data


def save_ignore_words(data):

    with open(
        IGNORE_WORDS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


def get_active_ignore_words():

    data = load_ignore_words()

    return [

        x["word"]

        for x in data

        if x.get(
            "enabled",
            True
        )
    ]

#========================= GUI =======================
class BOMCompareGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "BOM Compare Tool (V1.5.4 by LyShao)"
        )

        self.root.geometry(
            "850x800"
        )

        self.root.minsize(
            800,
            650
        )

        self.file1_var = tk.StringVar()

        self.file2_var = tk.StringVar()

        self.ignore_data = (
            load_ignore_words()
        )

        self.build_ui()

    def bind_mousewheel(self):

        def _on_mousewheel(event):

            self.canvas.yview_scroll(
                int(-event.delta / 120),
                "units"
            )

        # self.canvas.bind_all(
        #     "<MouseWheel>",
        #     _on_mousewheel
        # )

    def build_ui(self):

        top_frame = ttk.LabelFrame(
            self.root,
            text="Input Files"
        )

        top_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            top_frame,
            text="File1"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        ttk.Entry(
            top_frame,
            textvariable=self.file1_var,
            width=90
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Button(
            top_frame,
            text="Browse",
            command=self.select_file1
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

        ttk.Label(
            top_frame,
            text="File2"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        ttk.Entry(
            top_frame,
            textvariable=self.file2_var,
            width=90
        ).grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Button(
            top_frame,
            text="Browse",
            command=self.select_file2
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5
        )

        ignore_frame = ttk.LabelFrame(
            self.root,
            text="Ignore Words"
        )

        ignore_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.canvas = tk.Canvas(
            ignore_frame
        )

        scrollbar = ttk.Scrollbar(
            ignore_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scroll_frame = ttk.Frame(
            self.canvas
        )

        self.scroll_frame.bind(
            "<Configure>",
            lambda e:
            self.canvas.configure(
                scrollregion=
                self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=
            scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.canvas.bind(
            "<Enter>",
            self.bind_mousewheel
        )

        self.canvas.bind(
            "<Leave>",
            self.unbind_mousewheel
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.checkbox_vars = []

        self.refresh_ignore_ui()

        add_frame = ttk.Frame(
            self.root
        )

        add_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ttk.Label(
            add_frame,
            text="Keyword"
        ).pack(
            side="left",
            padx=5
        )

        self.new_word_var = (
            tk.StringVar()
        )

        ttk.Entry(
            add_frame,
            textvariable=
            self.new_word_var,
            width=50
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            add_frame,
            text="Add",
            command=
            self.add_ignore_word
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            add_frame,
            text="Delete Selected",
            command=
            self.delete_selected
        ).pack(
            side="left",
            padx=5
        )

        # self.compare_btn = ttk.Button(
        #     self.root,
        #     text="Compare BOM",
        #     command=
        #     self.start_compare
        # )
        self.compare_btn = tk.Button(
            self.root,
            text="Start BOM Comparison",
            command=self.start_compare,

            bg="#28A745",          
            fg="white",            

            activebackground="#28A745", 
            activeforeground="white",

            font=("Microsoft YaHei UI", 14),

            width=18,
            height=1,

            relief="raised",
            bd=3,

            cursor="hand2"
        )

        self.compare_btn.pack(
            pady=10
        )

        log_frame = ttk.LabelFrame(
            self.root,
            text="Log"
        )

        log_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.log_text = tk.Text(
            log_frame,
            height=10
        )

        self.log_text.pack(
            fill="both",
            expand=True
        )


    def select_file1(self):

        filename = filedialog.askopenfilename(

            title="Select File1",

            filetypes=[
                ("TXT File", "*.txt"),
                ("All Files", "*.*")
            ]

        )

        if filename:

            self.file1_var.set(filename)


    def select_file2(self):

        filename = filedialog.askopenfilename(

            title="Select File2",

            filetypes=[
                ("TXT File", "*.txt"),
                ("All Files", "*.*")
            ]

        )

        if filename:

            self.file2_var.set(filename)

    def bind_mousewheel(self, event):

        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )


    def unbind_mousewheel(self, event):

        self.canvas.unbind_all(
            "<MouseWheel>"
        )


    def on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-event.delta / 120),
            "units"
        )

    def refresh_ignore_ui(self):

        for widget in self.scroll_frame.winfo_children():

            widget.destroy()

        self.checkbox_vars.clear()

        for index, item in enumerate(self.ignore_data):

            var = tk.BooleanVar(

                value=item.get(
                    "enabled",
                    True
                )

            )

            frame = ttk.Frame(
                self.scroll_frame
            )

            frame.pack(
                fill="x",
                padx=5,
                pady=2
            )

            chk = ttk.Checkbutton(

                frame,

                text=item["word"],

                variable=var

            )

            chk.pack(
                side="left",
                anchor="w"
            )

            self.checkbox_vars.append(

                {

                    "var": var,

                    "item": item

                }

            )


    def add_ignore_word(self):

        word = self.new_word_var.get().strip()

        if not word:

            return

        for item in self.ignore_data:

            if item["word"].upper() == word.upper():

                messagebox.showinfo(

                    "Info",

                    "Keyword already exists."

                )

                return

        self.ignore_data.append(

            {

                "word": word,

                "enabled": True

            }

        )

        save_ignore_words(
            self.ignore_data
        )

        self.refresh_ignore_ui()

        self.new_word_var.set("")


    def delete_selected(self):

        result = []

        for cb in self.checkbox_vars:

            item = cb["item"]

            enabled = cb["var"].get()

            item["enabled"] = enabled

            result.append(item)

        save_ignore_words(result)

        delete_list = []

        for cb in self.checkbox_vars:

            if cb["var"].get():

                delete_list.append(
                    cb["item"]
                )

        if not delete_list:

            messagebox.showinfo(

                "Info",

                "Please check the keywords to delete."

            )

            return

        if not messagebox.askyesno(

            "Confirm",

            "Delete selected keywords?"

        ):

            return

        for item in delete_list:

            if item in self.ignore_data:

                self.ignore_data.remove(item)

        save_ignore_words(
            self.ignore_data
        )

        self.refresh_ignore_ui()


    def save_checkbox_status(self):

        for cb in self.checkbox_vars:

            cb["item"]["enabled"] = cb["var"].get()

        save_ignore_words(
            self.ignore_data
        )


    def write_log(self, text):

        self.log_text.insert(

            tk.END,

            text + "\n"

        )

        self.log_text.see(
            tk.END
        )

        self.root.update()


    def start_compare(self):

        if not self.file1_var.get():

            messagebox.showerror(

                "Error",

                "Please select File1."

            )

            return

        if not self.file2_var.get():

            messagebox.showerror(

                "Error",

                "Please select File2."

            )

            return

        self.save_checkbox_status()

        self.compare_btn.config(

            state="disabled"

        )

        threading.Thread(

            target=self.run_compare,

            daemon=True

        ).start()


    def run_compare(self):

        global FILE1
        global FILE2

        FILE1 = self.file1_var.get()
        FILE2 = self.file2_var.get()

        try:

            self.write_log("")
            self.write_log("===================================")
            self.write_log("Start Comparing...")
            self.write_log("")

            self.write_log("Parsing File1...")
            bom1, dup1 = parse_bom(FILE1)

            self.write_log(
                f"File1 RefDes : {len(bom1)}"
            )

            self.write_log("")

            self.write_log("Parsing File2...")
            bom2, dup2 = parse_bom(FILE2)

            self.write_log(
                f"File2 RefDes : {len(bom2)}"
            )

            self.write_log("")

            self.write_log("Comparing...")

            diff_df = compare_bom(
                bom1,
                bom2
            )

            self.write_log(
                f"Differences : {len(diff_df)}"
            )

            dup1_df = pd.DataFrame(
                dup1
            )

            dup2_df = pd.DataFrame(
                dup2
            )

            self.write_log(
                "Exporting Excel..."
            )

            output_file = export_excel(

                diff_df,

                dup1_df,

                dup2_df

            )

            self.write_log("")
            self.write_log("Finished.")
            self.write_log(
                f"Output : {output_file}"
            )

            messagebox.showinfo(

                "Finished",

                f"Compare Finished!\n\nOutput:\n{output_file}"

            )

        except Exception as e:

            messagebox.showerror(

                "Error",

                str(e)

            )

            self.write_log("")
            self.write_log("ERROR")
            self.write_log(str(e))

        finally:

            self.compare_btn.config(

                state="normal"

            )


def read_file(filepath):

    encodings = [
        "utf-8",
        "utf-8-sig",
        "gbk",
        "cp1252",
        "latin1"
    ]

    for enc in encodings:

        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.readlines()

        except:
            pass

    raise Exception(f"Cannot read file: {filepath}")


def is_header(line):

    return bool(
        re.match(
            r'^\s*\d+\.\d+',
            line
        )
    )


def extract_part_number(line):

    tokens = line.split()

    candidates = []

    for token in tokens:

        if token.count(".") >= 2:

            candidates.append(token)

    if not candidates:
        return None

    candidates.sort(
        key=len,
        reverse=True
    )

    return candidates[0]


def extract_description(line, part_number):

    if not part_number:
        return ""

    pos = line.find(part_number)

    if pos < 0:
        return ""

    desc = line[pos + len(part_number):]

    desc = " ".join(desc.split())

    return desc.strip()


def clean_description(desc):

    if not desc:

        return ""

    xx_pos = desc.find("XX")

    if xx_pos != -1:

        desc = desc[:xx_pos]

    desc = desc.strip()

    desc_upper = desc.upper()

    ignore_words = get_active_ignore_words()

    for word in sorted(

        ignore_words,

        key=len,

        reverse=True

    ):

        pattern = r'(?<![A-Z0-9])' + re.escape(word) + r'(?![A-Z0-9])'

        desc = re.sub(
            pattern,
            "",
            desc,
            flags=re.IGNORECASE
        )

    desc = re.sub(

        r"\s{2,}",

        " ",

        desc

    )

    desc = re.sub(

        r";\s*;",

        ";",

        desc

    )

    desc = desc.strip(" ;")

    return desc


def normalize_value(value):

    if not value:
        return ""

    value = value.upper()

    value = value.replace("µF", "UF")
    value = value.replace("ΜF", "UF")      
    value = value.replace("μF", "UF")


    def uf_to_nf(match):

        num = float(match.group(1))

        nf = num * 1000

        if nf.is_integer():
            nf = int(nf)

        return f"{nf}NF"

    value = re.sub(
        r'(\d+\.?\d*)UF',
        uf_to_nf,
        value
    )

    value = re.sub(
        r'(\d+)K(\d+)',
        r'\1.\2K',
        value
    )

    return value.strip()


def extract_refdes(line):

    line = line.strip()

    m = re.search(
        r'([A-Z]{1,5}\d+)\s*$',
        line
    )

    if m:
        return m.group(1)

    return None


def parse_bom(filepath):

    lines = read_file(filepath)

    blocks = []

    current_block = None

    for line in lines:

        line = line.rstrip()

        if not line:
            continue


        if is_header(line):

            pn = extract_part_number(line)

            raw_desc = extract_description(

                line,

                pn

            )

            clean_desc = clean_description(

                raw_desc

            )

            current_block = {

                "part_number": pn,

                "description": clean_desc,

                "refs":[]
            }

            blocks.append(
                current_block
            )

            continue

        ref = extract_refdes(line)

        if ref and current_block:

            current_block["refs"].append(
                ref
            )

    ref_index = {}

    duplicates = []

    for block in blocks:

        pn = block["part_number"]
        desc = block["description"]

        for ref in block["refs"]:

            if ref in ref_index:

                duplicates.append({
                    "RefDes": ref,
                    "PartNumber": pn,
                    "Description": desc
                })

            ref_index[ref] = {
                "part_number": pn,
                "description": desc
            }

    return ref_index, duplicates


def compare_bom(bom1, bom2):

    rows = []

    all_refs = sorted(
        set(bom1.keys()) |
        set(bom2.keys())
    )

    for ref in all_refs:

        if ref not in bom2:

            rows.append({
                "RefDes": ref,
                "Status": "ONLY_IN_FILE1",

                "PartNumber_File1":
                    bom1[ref]["part_number"],

                "PartNumber_File2": "",

                "Value_File1":
                    bom1[ref]["description"],

                "Value_File2": ""
            })

            continue

        if ref not in bom1:

            rows.append({
                "RefDes": ref,
                "Status": "ONLY_IN_FILE2",

                "PartNumber_File1": "",

                "PartNumber_File2":
                    bom2[ref]["part_number"],

                "Value_File1": "",

                "Value_File2":
                    bom2[ref]["description"]
            })

            continue

        pn1 = bom1[ref]["part_number"]
        pn2 = bom2[ref]["part_number"]

        raw_val1 = bom1[ref]["description"]
        raw_val2 = bom2[ref]["description"]

        norm_val1 = normalize_value(raw_val1)
        norm_val2 = normalize_value(raw_val2)

        value_changed = (
            norm_val1 != norm_val2
        )

        part_changed = (
            str(pn1).strip()
            !=
            str(pn2).strip()
        )

        if not part_changed and not value_changed:
            continue

        rows.append({
            "RefDes": ref,

            "Part_Changed":
                "YES" if part_changed else "NO",

            "Value_Changed":
                "YES" if value_changed else "NO",

            "PartNumber_File1": pn1,
            "PartNumber_File2": pn2,

            "Value_File1": raw_val1,
            "Value_File2": raw_val2
        })

    df = pd.DataFrame(rows)

    columns = [
        "RefDes",
        "Status",
        "PartNumber_File1",
        "PartNumber_File2",
        "Value_File1",
        "Value_File2",
        "Part_Changed",
        "Value_Changed"
    ]

    df = df.reindex(columns=columns)

    return df


def get_output_filename():

    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )

    index = 1

    while True:

        filename = os.path.join(

            OUTPUT_FOLDER,

            f"BOM_COMPARE_RESULT_{index}.xlsx"

        )

        if not os.path.exists(filename):

            return filename

        index += 1


def export_excel(
        diff_df,
        dup1_df,
        dup2_df):
    output_file = get_output_filename()
    file1_name = os.path.splitext(os.path.basename(FILE1))[0]
    file2_name = os.path.splitext(os.path.basename(FILE2))[0]

    diff_df = diff_df.rename(
        columns={
            "PartNumber_File1": f"{file1_name}_PartNumber",
            "PartNumber_File2": f"{file2_name}_PartNumber",
            "Value_File1": f"{file1_name}_Value",
            "Value_File2": f"{file2_name}_Value"
        }
    )

    with pd.ExcelWriter(
            output_file,
            engine="openpyxl"
    ) as writer:

        diff_df.to_excel(
        writer,
        sheet_name="Differences",
        index=False
    )

    if not dup1_df.empty:
        dup1_df.to_excel(
        writer,
        sheet_name="Duplicate_File1",
        index=False
    )

    if not dup2_df.empty:
        dup2_df.to_excel(
        writer,
        sheet_name="Duplicate_File2",
        index=False
    )

    return output_file


def main():

    root = tk.Tk()

    app = BOMCompareGUI(root)

    root.mainloop()


if __name__ == "__main__":

    main()