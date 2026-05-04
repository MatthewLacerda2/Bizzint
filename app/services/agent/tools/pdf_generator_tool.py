from weasyprint import HTML


def _render_pdf_bytes(title: str, subtitle: str, body_html: str, css: str) -> bytes:
    """Wraps the agent-provided HTML + CSS into a minimal document and returns PDF bytes."""
    full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{title} — {subtitle}</title>
<style>
{css}
</style>
</head>
<body>
{body_html}
</body>
</html>"""
    return HTML(string=full_html).write_pdf()


# ─── Tool signature (used by Gemini function-calling) ────────────────

def pdf_generator_tool(
    title: str,
    subtitle: str,
    body_html: str,
    css: str = "",
) -> bytes:
    """
    Generates a PDF report from raw HTML and CSS content.
    The report is limited to 5 pages.

    Parameters:
    - title: The report title (used in the document metadata).
    - subtitle: A short description of the report.
    - body_html: The full HTML body of the report. You have complete control
                 over the structure: cover pages, sections, tables, charts, etc.
    - css: The full CSS stylesheet for the report. You have complete control
           over layout, typography, colors, page breaks, etc.
           Use @page rules for margins, page size, headers/footers.
    """
    return _render_pdf_bytes(title, subtitle, body_html, css)
