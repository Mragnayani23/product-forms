from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/generate-pdf")
async def generate_pdf(
    contract_no: str = Form(...),
    date: str = Form(...),
    seller: str = Form(...),
    notify_party1: str = Form(...),
    notify_party2: str = Form(...),
    product: str = Form(...),
    quantity: str = Form(...),
    price_cif: str = Form(...),
    amount_cif: str = Form(...),
    packing: str = Form(...),
    loading_port: str = Form(...),
    destination_port: str = Form(...),
    shipment: str = Form(...),
    documents: str = Form(...),
    payment_terms: str = Form(...),
    seller_bank: str = Form(...),
    account_no: str = Form(...),
):
    file_path = "sales_contract.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Set image paths
    background_path = r"C:\Users\Lenovo\OneDrive\Desktop\agreement\background.jpg"
    signature_path = r"C:\Users\Lenovo\OneDrive\Desktop\agreement\signature.jpg"
    logo_path = r"C:\Users\Lenovo\OneDrive\Desktop\agreement\headerimg.jpg"

    # Draw background image
    if os.path.exists(background_path):
        c.drawImage(background_path, 0, 0, width=width, height=height, preserveAspectRatio=True, mask='auto')

    # Set margins
    left_margin = 30
    right_margin = 30
    top_margin = 30
    line_height = 14

    # Current y position starting from top of page
    y = height - top_margin

    # Website and Impex Name
    c.setFont("Helvetica", 8)
    c.drawString(left_margin, y - 20, "Website: www.shraddhalmpex.in")
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.blue)
    c.drawRightString(width - right_margin, y - 20, "SHRADDHA IMPEX")
    c.setFillColor(colors.black)
    y -= 40

    # Add logo image centered above the title
    if os.path.exists(logo_path):
        logo_width = 100
        logo_height = 40
        c.drawImage(logo_path, (width - logo_width)/2, y - logo_height, 
                   width=logo_width, height=logo_height, preserveAspectRatio=True)
        y -= logo_height + 10

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, y - 20, "SALES CONTRACT")
    y -= 30

    # Contract No and Date
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y - 15, f"Contract No: {contract_no}")
    c.setFont("Helvetica", 9)
    c.drawRightString(width - right_margin, y - 15, f"Date: {date}")
    y -= 30

    # Seller, Consignee, Notify Party sections
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y - 15, "SELLER")
    c.drawString(width / 3, y - 15, "CONSIGNEE | NOTIFY PARTY 1")
    c.drawString(2 * width / 3, y - 15, "NOTIFY PARTY 2")
    y -= 15

    # Seller address
    c.setFont("Helvetica", 8)
    text = c.beginText(left_margin, y - 15)
    for line in seller.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Consignee address
    text = c.beginText(width / 3, y - 15)
    for line in notify_party1.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Notify Party 2 address
    text = c.beginText(2 * width / 3, y - 15)
    for line in notify_party2.split('\n'):
        text.textLine(line)
    c.drawText(text)
    
    # Calculate lowest point of addresses to position next section
    seller_lines = len(seller.split('\n'))
    consignee_lines = len(notify_party1.split('\n'))
    notify_lines = len(notify_party2.split('\n'))
    max_lines = max(seller_lines, consignee_lines, notify_lines)
    y -= max_lines * line_height + 20

    # Contract intro text
    c.setFont("Helvetica", 8)
    c.drawString(left_margin, y - 15, "This sales contract made between above firms, for the following goods under the terms & conditions mentioned here as:")
    y -= 30

    # Improved table structure
    table_top = y - 20
    table_bottom = y - 60
    table_width = width - left_margin - right_margin
    
    # Draw main table border
    c.rect(left_margin, table_bottom, table_width, table_top - table_bottom)
    
    # Draw vertical lines
    c.line(left_margin + 130, table_bottom, left_margin + 130, table_top)
    c.line(left_margin + 260, table_bottom, left_margin + 260, table_top)
    c.line(left_margin + 390, table_bottom, left_margin + 390, table_top)
    
    # Draw horizontal line separating headers from content
    header_line_y = table_top - 20
    c.line(left_margin, header_line_y, left_margin + table_width, header_line_y)
    
    # Table headers
    c.setFont("Helvetica-Bold", 8)
    c.drawString(left_margin + 5, table_top - 15, "Product")
    c.drawString(left_margin + 135, table_top - 15, "Quantity")
    c.drawString(left_margin + 265, table_top - 15, "Price (CIF), Colombo")
    c.drawString(left_margin + 395, table_top - 15, "Amount(CIF)")
    
    # Table content
    c.setFont("Helvetica", 8)
    content_y = table_top - 35
    
    # Draw product details in the table cells
    c.drawString(left_margin + 5, content_y, product)
    c.drawString(left_margin + 135, content_y, quantity)
    c.drawString(left_margin + 265, content_y, price_cif)
    c.drawString(left_margin + 395, content_y, amount_cif)
    
    y = table_bottom - 20

    # Contract details
    details = [
        ("Packing", packing),
        ("Loading Port", loading_port),
        ("Destination Port", destination_port),
        ("Shipment", shipment),
        ("Documents", documents),
        ("Payment Terms", payment_terms),
        ("Seller's Bank", seller_bank),
        ("Account No.", account_no),
    ]

    for label, value in details:
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left_margin, y - 15, f"{label}:")
        c.setFont("Helvetica", 8)
        
        if '\n' in value:
            text = c.beginText(left_margin + 80, y - 15)
            for line in value.split('\n'):
                text.textLine(line)
            c.drawText(text)
            y -= (value.count('\n') + 1) * line_height
        else:
            c.drawString(left_margin + 80, y - 15, value)
            y -= line_height
        
        y -= 5

    # Arbitration clause
    y -= 10
    c.setFont("Helvetica-Bold", 8)
    c.drawString(left_margin, y - 15, "Arbitration:")
    c.setFont("Helvetica", 8)
    arbitration_text = [
        "In the event of any dispute between the parties arising out of this contract, all disputes shall be",
        "settled by the way of arbitration through a sole arbitration to be appointed by M/S Shraddha Impex.",
        "The place of arbitration shall be in Indore, M.P. and the laws of India with regards to arbitration",
        "shall be applicable to this Arbitration Clause."
    ]
    for line in arbitration_text:
        c.drawString(left_margin + 10, y - 30, line)
        y -= line_height
    y -= 10

    # Terms & Conditions
    c.setFont("Helvetica-Bold", 8)
    c.drawString(left_margin, y - 15, "Terms & Conditions:")
    c.setFont("Helvetica", 8)
    terms_text = [
        "1) In case of port congestion/ skippance of vessel or any other port related disturbances, supplier or exporter will not be liable for any claim.",
        "2) Quality approved at load port by independent surveyors is final, and to be acceptable by both the parties and the seller will not ",
        "be liable for anyclaim at destination port."
    ]
    for line in terms_text:
        c.drawString(left_margin + 10, y - 30, line)
        y -= line_height
    y -= 40

    # Signature section
    if os.path.exists(signature_path):
        c.drawImage(signature_path, left_margin, y - 50, width=100, height=40, preserveAspectRatio=True)

    # Company names below signature section
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, y - 60, "SHRADDHA IMPEX")
    c.drawString(width / 3, y - 60, "SMART DRAGON LANKA PVT LTD")
    c.drawString(2 * width / 3, y - 60, "DEVI GLOBAL HK LTD")

    # "For" labels
    c.setFont("Helvetica", 8)
    c.drawString(left_margin, y - 80, "For, Seller")
    c.drawString(width / 3, y - 80, "For, Consignee")
    c.drawString(2 * width / 3, y - 80, "For, Notify Party")
    
    # Footer
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.white)
    c.drawCentredString(width / 2, 30, "308 Third Floor, Fortune Business Center, 165 R.N.T. Marg, Indore 452001, M.P., India")
    c.drawCentredString(width / 2, 20, "Tel.: (+91) 731 2515151 • Fax: (+91) 731 4096348 • E-Mail : shradhalmpex@yahoo.com")

    c.save()
    return FileResponse(file_path, media_type='application/pdf', filename="sales_contract.pdf")
