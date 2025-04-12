import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
import os

# Load products data
products = pd.read_csv("products.csv")

def generate_order_form(company_name, address, contact_person, contact_number, email, website, product_names, description, total_cost, production_date, delivery_date):
    selected_products = products[products['product_id'].isin(product_ids)]
    if len(selected_products) != len(quantities):
        st.error("Mismatch between selected products and quantities")
        return None
    
    pdf = FPDF()
    pdf.add_page()
   
    # Header
    pdf.set_fill_color(0, 51, 153)  # Dark blue header
    pdf.rect(0, 0, 210, 40, style='F')
    pdf.image("toplogo1.png", x=10, y=10, w=30)
    pdf.set_text_color(255, 255, 255)
    pdf.image("logo.png", x=85, y=10, w=60)
    
    # Move cursor below logo
    pdf.set_y(45)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, "4-B, 3rd Floor, V.K. Complex, Opp. Gurudwara,", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 3, "Odhav, Ahmedabad-382415. Gujaarat, India.", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, "PROFESSIONAL SYMBOLS & LOGO DESIGNER", ln=True, align='C')
    pdf.cell(200, 3, "www.dixacreation.com", ln=True, align='C')
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    
    # Order Form Title
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "ORDER FORM", ln=True, align='L')
    pdf.ln(5)
    
    # Order Details
    pdf.set_font("Arial", '', 12)
    pdf.cell(95, 8, f"Company Name: {company_name}", ln=True)
    pdf.cell(95, 8, f"Address: {address}", ln=True)
    pdf.cell(95, 8, f"Contact Person: {contact_person}", ln=True)
    pdf.cell(95, 8, f"Contact Number: {contact_number}", ln=True)
    pdf.cell(95, 8, f"Email: {email}", ln=True)
    pdf.cell(95, 8, f"Website: {website}", ln=True)
    pdf.ln(5)
    
    # Product Details
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, "Product Details", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(95, 8, f"Product Name: {product_names}", ln=True)
    pdf.multi_cell(0, 8, f"Description: {description}")
    pdf.ln(5)
    
    # Payment & Delivery
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, "Payment & Delivery", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(95, 8, f"Total Cost: rs:{total_cost:.2f}", ln=True)
    pdf.cell(95, 8, "Payment: 100% Advance", ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, "After Design Conformation", ln=True)
    pdf.cell(95, 8, f"Production Date: {production_date}", ln=True)
    pdf.cell(95, 8, f"Delivery Date: {delivery_date}", ln=True)
    pdf.ln(5)
    
    # Signatures
    pdf.cell(135, 40, "Party Signature: ___________________")
    pdf.cell(135, 40, "For, DIXA CREATION", ln=True)
    
    # Table Header
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(60, 10, txt="Product", border=1)
    pdf.cell(60, 10, txt="Description", border=1)
    pdf.cell(20, 10, txt="Qty", border=1)
    pdf.cell(30, 10, txt="Unit Price", border=1)
    pdf.cell(30, 10, txt="Total", border=1)
    pdf.ln()
    
    # Table Rows
    total = 0
    pdf.set_font("Arial", size=12)
    for i, product in selected_products.iterrows():
        quantity = quantities[product_ids.index(product['product_id'])]
        line_total = product['price'] * quantity
        total += line_total
        pdf.cell(60, 10, txt=product['product_name'], border=1)
        pdf.cell(60, 10, txt=product['description'], border=1)
        pdf.cell(20, 10, txt=str(quantity), border=1)
        pdf.cell(30, 10, txt=f"${product['price']}", border=1)
        pdf.cell(30, 10, txt=f"${line_total}", border=1)
        pdf.ln()
    
    # Total Row
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(170, 10, txt="Total", border=1)
    pdf.cell(30, 10, txt=f"${total}", border=1)
    
    filename = "Order_Form.pdf"
    pdf.output(filename)
    return filename

def main():
    st.title("Dixa Creation Order Form")
    st.sidebar.header("Fill Order Details")

    company_name = st.sidebar.text_input("Company Name")
    address = st.sidebar.text_area("Address")
    contact_person = st.sidebar.text_input("Contact Person")
    contact_number = st.sidebar.text_input("Contact Number")
    email = st.sidebar.text_input("Email")
    website = st.sidebar.text_input("Website")
    product_names = products['product_name'].tolist()
    selected_products = st.sidebar.multiselect("Products", product_names)
    global product_ids, quantities
    product_ids = products[products['product_name'].isin(selected_products)]['product_id'].tolist()

    quantities = []
    for product in selected_products:
        quantity = st.sidebar.number_input(f"Quantity of {product}", min_value=1, max_value=100, value=1)
        quantities.append(quantity)

    description = st.sidebar.text_area("Description")
    total_cost = st.sidebar.number_input("Total Cost", min_value=0.0, format="%.2f")
    production_date = st.sidebar.date_input("Production Date")
    delivery_date = st.sidebar.date_input("Delivery Date")

    if st.sidebar.button("Generate Order Form"):
        filename = generate_order_form(company_name, address, contact_person, contact_number, email, website, 
                                    ", ".join(selected_products), description, total_cost, production_date, delivery_date)

        if filename:
            # Create download button
            with open(filename, 'rb') as f:
                st.download_button(
                    label="Download Order Form",
                    data=f,
                    file_name=filename,
                    mime="application/pdf",
                )
            
            # Display PDF preview
            with open(filename, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

if __name__ == "__main__":
    main()