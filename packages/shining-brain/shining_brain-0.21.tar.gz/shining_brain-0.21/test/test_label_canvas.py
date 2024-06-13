from reportlab.lib.pagesizes import A4

from shining_brain.label_canvas import LabelCanvas


def test_label_creation():
    components = [{
        "pagesize": A4,
        "elements": [
            {
                "id": "1001",
                "name": "rect",
                "type": "rect",
                "parameter": {
                    "x": 153.637795,
                    "y": 205.194881,
                    "width": 288,
                    "height": 431.5,
                    "line-width": 0.1,
                    "stroke-color": (0.66, 0.66, 0.66)
                }
            }, {
                "id": "1002",
                "name": "assembly",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 215.194881,
                    "font-name": "Helvetica",
                    "font-size": 9,
                    "text": "Assembled In Malaysia"
                }
            }, {
                "id": "1003",
                "name": "line1",
                "type": "line",
                "parameter": {
                    "x1": 158.637795,
                    "y1": 226.194881,
                    "x2": 436.637795,
                    "y2": 226.194881,
                    "line-width": 1,
                    "stroke-color": (0, 0, 0)
                }
            }, {
                "id": "1004",
                "name": "carton-number",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 230.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Carton No.                                    1 of 1"
                }
            }, {
                "id": "1005",
                "name": "line2",
                "type": "line",
                "parameter": {
                    "x1": 158.637795,
                    "y1": 239.194881,
                    "x2": 436.637795,
                    "y2": 239.194881,
                    "line-width": 1,
                    "stroke-color": (0, 0, 0)
                }
            }, {
                "id": "1006",
                "name": "quantity-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 243.194881,
                    "width": 30,
                    "height": 16,
                    "text": "10"
                }
            }, {
                "id": "1007",
                "name": "quantity",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 264.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "10"
                }
            }, {
                "id": "1008",
                "name": "quantity-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 275.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Quantity"
                }
            }, {
                "id": "1009",
                "name": "esm-reference-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 286.194881,
                    "width": 120,
                    "height": 16,
                    "text": "CI2402210003"
                }
            }, {
                "id": "1010",
                "name": "esm-reference",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 307.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "CI2402210003"
                }
            }, {
                "id": "1011",
                "name": "esm-reference-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 318.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "ESM Reference"
                }
            }, {
                "id": "1012",
                "name": "invoice-number-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 329.194881,
                    "width": 75,
                    "height": 16,
                    "text": "NA"
                }
            }, {
                "id": "1013",
                "name": "invoice-number",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 350.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "NA"
                }
            }, {
                "id": "1014",
                "name": "invoice-number-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 361.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Invoice Number"
                }
            }, {
                "id": "1015",
                "name": "purchase-order_number-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 372.194881,
                    "width": 150,
                    "height": 16,
                    "text": "385166"
                }
            }, {
                "id": "1016",
                "name": "purchase-order_number",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 393.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "385166"
                }
            }, {
                "id": "1017",
                "name": "purchase-order_number-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 404.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Purchase Order Number"
                }
            }, {
                "id": "1018",
                "name": "manufacturing-part-no-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 415.194881,
                    "width": 170,
                    "height": 16,
                    "text": "10IC102277"
                }
            }, {
                "id": "1019",
                "name": "manufacturing-part-no",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 436.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "10IC102277"
                }
            }, {
                "id": "1020",
                "name": "manufacturing-part-no-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 447.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Manufacturing Part No."
                }
            }, {
                "id": "1021",
                "name": "part_number-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 458.194881,
                    "width": 180,
                    "height": 16,
                    "text": "1130-776-01"
                }
            }, {
                "id": "1022",
                "name": "part_number",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 479.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "1130-776-01"
                }
            }, {
                "id": "1023",
                "name": "part_number-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 490.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Part Number"
                }
            }, {
                "id": "1024",
                "name": "line3",
                "type": "line",
                "parameter": {
                    "x1": 158.637795,
                    "y1": 501.194881,
                    "x2": 436.637795,
                    "y2": 501.194881,
                    "line-width": 2,
                    "stroke-color": (0, 0, 0)
                }
            }, {
                "id": "1025",
                "name": "tel",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 506.194881,
                    "font-name": "Helvetica",
                    "font-size": 8.5,
                    "text": "TEL: (65) 6681 7406"
                }
            }, {
                "id": "1026",
                "name": "attn",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 516.694881,
                    "font-name": "Helvetica",
                    "font-size": 8.5,
                    "text": "ATTN : Shirley Ng"
                }
            }, {
                "id": "1027",
                "name": "address1",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 527.194881,
                    "font-name": "Helvetica",
                    "font-size": 8.5,
                    "text": "Singapore 738100 Singapore"
                }
            }, {
                "id": "1028",
                "name": "address2",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 537.694881,
                    "font-name": "Helvetica",
                    "font-size": 8.5,
                    "text": "18 Woodlands Loop"
                }
            }, {
                "id": "1029",
                "name": "address3",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 548.194881,
                    "font-name": "Helvetica",
                    "font-size": 8.5,
                    "text": "Ichor System Singapore Pte Ltd"
                }
            }, {
                "id": "1030",
                "name": "address4",
                "type": "text",
                "parameter": {
                    "x": 163.637795,
                    "y": 558.694881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 11.5,
                    "text": "Del To: SICS01"
                }
            }, {
                "id": "1031",
                "name": "line4",
                "type": "line",
                "parameter": {
                    "x1": 158.637795,
                    "y1": 572.194881,
                    "x2": 436.637795,
                    "y2": 572.194881,
                    "line-width": 0.2,
                    "stroke-color": (0, 0, 0)
                }
            }, {
                "id": "1032",
                "name": "ess-crn",
                "type": "text",
                "parameter": {
                    "x": 200.637795,
                    "y": 575.394881,
                    "font-name": "Helvetica",
                    "font-size": 8.2,
                    "text": "Co.Reg. No.: 199407 196G GST Reg. No.: M2-01282323-2"
                }
            }, {
                "id": "1033",
                "name": "address6",
                "type": "text",
                "parameter": {
                    "x": 200.637795,
                    "y": 585.894881,
                    "font-name": "Helvetica",
                    "font-size": 8.2,
                    "text": "Tel: 67421930 (2 lines) WEBSITE: http://www.esynergies.com.sg"
                }
            }, {
                "id": "1034",
                "name": "address7",
                "type": "text",
                "parameter": {
                    "x": 200.637795,
                    "y": 595.394881,
                    "font-name": "Helvetica",
                    "font-size": 8.2,
                    "text": "Enuos Techpark. Singapore 415979"
                }
            }, {
                "id": "1035",
                "name": "address8",
                "type": "text",
                "parameter": {
                    "x": 200.637795,
                    "y": 604.894881,
                    "font-name": "Helvetica",
                    "font-size": 8.2,
                    "text": "60, Kaki Bukit Place #08-01"
                }
            }, {
                "id": "1036",
                "name": "address8",
                "type": "text",
                "parameter": {
                    "x": 200.637795,
                    "y": 616.394881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 12.5,
                    "text": "Electronic Synergies (S) Pte Ltd"
                }
            }
        ]
    },{
        "pagesize": A4,
        "elements": [
            {
                "id": "1001",
                "name": "rect",
                "type": "rect",
                "parameter": {
                    "x": 153.637795,
                    "y": 205.194881,
                    "width": 288,
                    "height": 431.5,
                    "line-width": 0.1,
                    "stroke-color": (0.66, 0.66, 0.66)
                }
            }, {
                "id": "1002",
                "name": "assembly",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 215.194881,
                    "font-name": "Helvetica",
                    "font-size": 9,
                    "text": "Assembled In Malaysia"
                }
            }, {
                "id": "1003",
                "name": "line1",
                "type": "line",
                "parameter": {
                    "x1": 158.637795,
                    "y1": 226.194881,
                    "x2": 436.637795,
                    "y2": 226.194881,
                    "line-width": 1,
                    "stroke-color": (0, 0, 0)
                }
            }, {
                "id": "1004",
                "name": "carton-number",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 230.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Carton No.                                    1 of 1"
                }
            }, {
                "id": "1005",
                "name": "line2",
                "type": "line",
                "parameter": {
                    "x1": 158.637795,
                    "y1": 239.194881,
                    "x2": 436.637795,
                    "y2": 239.194881,
                    "line-width": 1,
                    "stroke-color": (0, 0, 0)
                }
            }, {
                "id": "1006",
                "name": "quantity-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 243.194881,
                    "width": 30,
                    "height": 16,
                    "text": "10"
                }
            }, {
                "id": "1007",
                "name": "quantity",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 264.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "10"
                }
            }, {
                "id": "1008",
                "name": "quantity-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 275.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Quantity"
                }
            }, {
                "id": "1009",
                "name": "esm-reference-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 286.194881,
                    "width": 120,
                    "height": 16,
                    "text": "CI2402210003"
                }
            }, {
                "id": "1010",
                "name": "esm-reference",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 307.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "CI2402210003"
                }
            }, {
                "id": "1011",
                "name": "esm-reference-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 318.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "ESM Reference"
                }
            }, {
                "id": "1012",
                "name": "invoice-number-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 329.194881,
                    "width": 75,
                    "height": 16,
                    "text": "NA"
                }
            }, {
                "id": "1013",
                "name": "invoice-number",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 350.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "NA"
                }
            }, {
                "id": "1014",
                "name": "invoice-number-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 361.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Invoice Number"
                }
            }, {
                "id": "1015",
                "name": "purchase-order_number-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 372.194881,
                    "width": 150,
                    "height": 16,
                    "text": "385166"
                }
            }, {
                "id": "1016",
                "name": "purchase-order_number",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 393.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "385166"
                }
            }, {
                "id": "1017",
                "name": "purchase-order_number-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 404.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Purchase Order Number"
                }
            }, {
                "id": "1018",
                "name": "manufacturing-part-no-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 415.194881,
                    "width": 170,
                    "height": 16,
                    "text": "10IC102277"
                }
            }, {
                "id": "1019",
                "name": "manufacturing-part-no",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 436.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "10IC102277"
                }
            }, {
                "id": "1020",
                "name": "manufacturing-part-no-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 447.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Manufacturing Part No."
                }
            }, {
                "id": "1021",
                "name": "part_number-barcode",
                "type": "barcode",
                "parameter": {
                    "x": 193.637795,
                    "y": 458.194881,
                    "width": 180,
                    "height": 16,
                    "text": "1130-776-01"
                }
            }, {
                "id": "1022",
                "name": "part_number",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 479.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "1130-776-01"
                }
            }, {
                "id": "1023",
                "name": "part_number-label",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 490.194881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 9,
                    "text": "Part Number"
                }
            }, {
                "id": "1024",
                "name": "line3",
                "type": "line",
                "parameter": {
                    "x1": 158.637795,
                    "y1": 501.194881,
                    "x2": 436.637795,
                    "y2": 501.194881,
                    "line-width": 2,
                    "stroke-color": (0, 0, 0)
                }
            }, {
                "id": "1025",
                "name": "tel",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 506.194881,
                    "font-name": "Helvetica",
                    "font-size": 8.5,
                    "text": "TEL: (65) 6681 7406"
                }
            }, {
                "id": "1026",
                "name": "attn",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 516.694881,
                    "font-name": "Helvetica",
                    "font-size": 8.5,
                    "text": "ATTN : Shirley Ng"
                }
            }, {
                "id": "1027",
                "name": "address1",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 527.194881,
                    "font-name": "Helvetica",
                    "font-size": 8.5,
                    "text": "Singapore 738100 Singapore"
                }
            }, {
                "id": "1028",
                "name": "address2",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 537.694881,
                    "font-name": "Helvetica",
                    "font-size": 8.5,
                    "text": "18 Woodlands Loop"
                }
            }, {
                "id": "1029",
                "name": "address3",
                "type": "text",
                "parameter": {
                    "x": 193.637795,
                    "y": 548.194881,
                    "font-name": "Helvetica",
                    "font-size": 8.5,
                    "text": "Ichor System Singapore Pte Ltd"
                }
            }, {
                "id": "1030",
                "name": "address4",
                "type": "text",
                "parameter": {
                    "x": 163.637795,
                    "y": 558.694881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 11.5,
                    "text": "Del To: SICS01"
                }
            }, {
                "id": "1031",
                "name": "line4",
                "type": "line",
                "parameter": {
                    "x1": 158.637795,
                    "y1": 572.194881,
                    "x2": 436.637795,
                    "y2": 572.194881,
                    "line-width": 0.2,
                    "stroke-color": (0, 0, 0)
                }
            }, {
                "id": "1032",
                "name": "ess-crn",
                "type": "text",
                "parameter": {
                    "x": 200.637795,
                    "y": 575.394881,
                    "font-name": "Helvetica",
                    "font-size": 8.2,
                    "text": "Co.Reg. No.: 199407 196G GST Reg. No.: M2-01282323-2"
                }
            }, {
                "id": "1033",
                "name": "address6",
                "type": "text",
                "parameter": {
                    "x": 200.637795,
                    "y": 585.894881,
                    "font-name": "Helvetica",
                    "font-size": 8.2,
                    "text": "Tel: 67421930 (2 lines) WEBSITE: http://www.esynergies.com.sg"
                }
            }, {
                "id": "1034",
                "name": "address7",
                "type": "text",
                "parameter": {
                    "x": 200.637795,
                    "y": 595.394881,
                    "font-name": "Helvetica",
                    "font-size": 8.2,
                    "text": "Enuos Techpark. Singapore 415979"
                }
            }, {
                "id": "1035",
                "name": "address8",
                "type": "text",
                "parameter": {
                    "x": 200.637795,
                    "y": 604.894881,
                    "font-name": "Helvetica",
                    "font-size": 8.2,
                    "text": "60, Kaki Bukit Place #08-01"
                }
            }, {
                "id": "1036",
                "name": "address8",
                "type": "text",
                "parameter": {
                    "x": 200.637795,
                    "y": 616.394881,
                    "font-name": "Helvetica-Bold",
                    "font-size": 12.5,
                    "text": "Electronic Synergies (S) Pte Ltd"
                }
            }
        ]
    }]
    lc = LabelCanvas(components=components)
    print(lc.save())
