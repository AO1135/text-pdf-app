from flask import Flask, render_template, request, send_file
import qrcode
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
from reportlab.lib.pagesizes import A4
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]

        if len(text) > 2000:
            return "文字数が多すぎます（2000文字以内）"

        # QRコード生成（メモリ上）
        qr = qrcode.make(text)
        qr_buffer = BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)

        # PDF生成（メモリ上）
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        elements = []

        img = Image(qr_buffer, width=250, height=250)
        elements.append(Spacer(1, 100))
        elements.append(img)

        doc.build(elements)
        pdf_buffer.seek(0)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="qr_code.pdf",
            mimetype="application/pdf"
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run()