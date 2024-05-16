import tkinter as tk
from decimal import Decimal

from src.utils import safe_eval


class Calculator:
    def __init__(self, root) -> None:
        self.first_number = None
        self.last_number = None
        self.operator = None
        self.clear_result = False
        self.islastnumber = False

        self.root = root

        root.title("IOS Calculator")

        self.result = tk.Label(text="", font=("Arial", 30, "bold"))
        self.result.grid(columnspan=5, sticky="e")

        buttons_text = [
            "AC",
            "+/-",
            "%",
            "/",
            "1",
            "2",
            "3",
            "*",
            "4",
            "5",
            "6",
            "-",
            "7",
            "8",
            "9",
            "+",
            "0",
            ".",
            "=",
        ]

        for i, button_text in enumerate(buttons_text):
            button = tk.Button(
                text=button_text,
                width=6,
                height=3,
                bg="orange",
                fg="white",
                font=("Arial", 15, "bold"),
                command=lambda text=button_text: self.button_click(text),
            )
            button.grid(column=i % 4, row=i // 4 + 1)

    def button_click(self, button_text) -> None:
        if button_text == "AC":
            self.clear()
            return

        if self.clear_result and button_text not in ("+", "-", "*", "/", "%"):
            self.result["text"] = ""
            self.clear_result = False

        if button_text == "+/-":
            if self.result["text"].startswith("-"):
                self.result["text"] = self.result["text"].replace("-", "")
            else:
                self.result["text"] = "-" + self.result["text"]

        if button_text == "%":
            self.result["text"] = safe_eval(f"{self.result['text']} / 100")

        if button_text in ("+", "-", "*", "/"):
            self.operator = button_text

            self.first_number = self.result["text"]
            self.clear_result = True
            self.islastnumber = True
            return

        if button_text == "=" and self.operator:
            try:
                self.result["text"] = str(
                    safe_eval(
                        f"{self.first_number} {self.operator} {self.last_number}",
                    ),
                )
                self.result["text"] = str(Decimal(self.result["text"]))  # Fix

                if float(self.result["text"]).is_integer():
                    self.result["text"] = str(int(float(self.result["text"])))

            except ZeroDivisionError:
                self.result["text"] = "ERROR"
                self.clear(clear_text=False)

            self.islastnumber = False

        if button_text in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            self.result["text"] += button_text

        if self.islastnumber:
            self.last_number = self.result["text"]
        else:
            self.first_number = self.result["text"]

    def clear(self, *, clear_text=True) -> None:
        self.first_number = None
        self.last_number = None
        self.operator = None
        self.islastnumber = False

        if clear_text:
            self.result["text"] = ""
            self.clear_result = False
        else:
            self.clear_result = True


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
