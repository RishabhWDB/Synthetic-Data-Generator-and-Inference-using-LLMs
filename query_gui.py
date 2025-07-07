import sys
import pandas as pd
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QTextEdit, QPushButton, QMessageBox
)

class QueryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Synthetic Data Query Interface")
        self.setGeometry(300, 300, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Enter your question:")
        layout.addWidget(self.label)

        self.query_input = QTextEdit()
        layout.addWidget(self.query_input)

        self.result_label = QLabel("LLM Response:")
        layout.addWidget(self.result_label)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        self.button = QPushButton("Run Query")
        self.button.clicked.connect(self.run_query)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def run_query(self):
        try:
            query = self.query_input.toPlainText().strip()
            if not query:
                QMessageBox.warning(self, "Empty Query", "Please enter a question.")
                return

            df = pd.read_csv("synthetic_data.csv")
            df_excerpt = df.head(100).to_csv(index=False)

            with open("prompts/query.txt") as f:
                template = f.read()

            prompt = template.format(data=df_excerpt, query=query)

            result = subprocess.run(
                ["ollama", "run", "llama3.1:8b-instruct-q4_K_M"],
                input=prompt,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )


            self.result_output.setText(result.stdout.strip())

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QueryApp()
    window.show()
    sys.exit(app.exec_())
