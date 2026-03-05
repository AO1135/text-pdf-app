import os
import qrcode
from io import BytesIO
from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
from reportlab.lib.pagesizes import A4

app = Flask(__name__)

# =========================
# QRコードをメモリ上で生成
# =========================
def generate_qr_image(text):
    qr = qrcode.make(text)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


# =========================
# ① 入力ページ
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]

        if len(text) > 2000:
            return "文字数が多すぎます（2000文字以内）"

        # QRを一時的にセッション代わりにhiddenで渡す
        return render_template("preview.html", text=text)

    return render_template("index.html")


# =========================
# ② PDFダウンロード処理
# =========================
@app.route("/download", methods=["POST"])
def download():
    text = request.form["text"]

    # QR生成
    qr_buffer = generate_qr_image(text)

    # PDF生成
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


if __name__ == "__main__":
    app.run()