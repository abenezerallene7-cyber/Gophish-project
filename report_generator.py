import io
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
from collections import Counter

def generate_pdf(scan, findings):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']

    elements = []
    elements.append(Paragraph("VulnScope Security Report", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Target: {scan.target}", normal_style))
    elements.append(Paragraph(f"Date: {scan.created_at.strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    elements.append(Paragraph(f"Risk Score: {scan.risk_score} ({scan.risk_level})", normal_style))
    elements.append(Spacer(1, 12))

    # Risk category breakdown chart
    categories = [f.category for f in findings]
    cat_counts = Counter(categories)
    if cat_counts:
        plt.figure(figsize=(6,4))
        plt.pie(cat_counts.values(), labels=cat_counts.keys(), autopct='%1.1f%%')
        plt.title('Findings by Category')
        plt.tight_layout()
        chart_buffer = io.BytesIO()
        plt.savefig(chart_buffer, format='png')
        plt.close()
        chart_buffer.seek(0)
        img = Image(chart_buffer, width=400, height=250)
        elements.append(img)
        elements.append(Spacer(1, 12))

    elements.append(Paragraph("Findings", heading_style))
    data = [['Issue', 'Severity', 'Category', 'Description', 'Recommendation']]
    for f in findings:
        data.append([
            f.issue_name,
            f.severity,
            f.category,
            f.description or '',
            f.recommendation or ''
        ])
    table = Table(data, colWidths=[90, 70, 70, 160, 160])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer