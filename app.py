from pathlib import Path
from flask import Flask, render_template, request

app = Flask(__name__)

# مسار المجلد الأساسي للتطبيق
BASE_DIR = Path(__file__).resolve().parent

@app.route("/")
def index():
    """
    الصفحة الرئيسية:
    - توضح إن الموقع يعرض ملفات نصية من مجلد notes
    - تعطي مثال للاعبين يبدأون منه
    """
    example_file = "notes/intro.txt"
    return render_template("index.html", example_file=example_file)


@app.route("/view")
def view_file():
    """
    مسار عرض الملفات:
    يأخذ باراميتر ?file= من الـ URL
    ويقرأ الملف مباشرة بدون أي تحقق أمني (هنا الثغرة)
    """
    filename = request.args.get("file", "")

    if not filename:
        return render_template("view.html", filename=None, content="No file specified.")

    # ⚠️ هنا الضعف: ما فيه أي فلترة لمسار الملف
    target_path = BASE_DIR / filename

    try:
        # نقرأ الملف كنص
        content = target_path.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        content = "File not found."
    except IsADirectoryError:
        content = "Cannot read a directory."
    except Exception as e:
        content = f"Error reading file: {e}"

    return render_template("view.html", filename=filename, content=content)


if __name__ == "__main__":
    # للتجربة المحلية
    app.run(host="0.0.0.0", port=5000, debug=True)
