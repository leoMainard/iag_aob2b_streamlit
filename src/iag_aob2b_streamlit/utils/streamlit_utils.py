import base64, os

def get_icon_svg(filetype):
    icons = {
        "pdf": "src/iag_aob2b_streamlit/img/pdf.png",
        "xlsx": "src/iag_aob2b_streamlit/img/excel.png",
        "docx": "src/iag_aob2b_streamlit/img/docx.png",
        "default": "src/iag_aob2b_streamlit/img/file.png",
    }
    if filetype in ["xls", "xlsm", "xlsb", "csv","ods", "xlsx"]:
        filetype = "xlsx"

    path = icons.get(filetype.lower(), icons["default"])

    ext = os.path.splitext(path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"

    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    return f'<img src="data:{mime};base64,{b64}" width="20" />'