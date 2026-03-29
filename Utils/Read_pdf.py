import pandas as pd
import pdfplumber as pp


class R_PDF:
    def __init__(self):
        pdf_file = pp.open("C:\\Users\\srira\\Downloads\\4430249274.pdf")
        self.pages = pdf_file.pages
        self.value = []
        self.section = []

    def get_text_properties(self, cropped_page, parameter: []):
        results = []
        for char in cropped_page.chars:
            props = {"text": char["text"], "fontname": char["fontname"], "size": char["size"],
                     "color": char["non_stroking_color"],
                     "is_bold": "Bold" in char["fontname"],
                     "is_italic": any(tag in char["fontname"] for tag in ["Italic", "Oblique"]),
                     "is_underlined": any(abs(line["top"] - char["bottom"]) < 2 for line in cropped_page.lines)}
            results.append(props)
        return {"word": parameter[0], "page_no": parameter[1], "table_num": parameter[2], "row_num": parameter[3],
                "property": results}

    def get_page_details(self):
        for page in self.pages:
            self.tables = page.find_tables()
            for table_num, table in enumerate(self.tables):
                if len(self.tables) == 1:
                    coordinates = []
                    coordinates.append([[0, 0, page.width, table.bbox[1]], f"Above_table_{table_num}"])
                    for row_num, row in enumerate(table.rows):
                        coordinates.append([list(row.bbox), row_num])
                    if table.bbox[-1] <= page.height:
                        coordinates.append([[0, table.bbox[-1], page.width, page.height], f"Below_table_{table_num}"])

                    for coo in coordinates:
                        if all(i > 0 for i in coo[0]):
                            if coo[0][2] > page.width:
                                coo[0][2] = page.width
                            if coo[0][3] > page.height:
                                coo[0][-1] = page.height
                        else:
                            if coo[0][0] < 0:
                                coo[0][0] = 0
                            if coo[0][1] < 0:
                                coo[0][1] = 0
                            if coo[0][2] < 0:
                                coo[0][2] = page.width
                            if coo[0][3] < 0:
                                coo[0][3] = page.height
                        if page.crop(tuple(coo[0])).extract_words():
                            for l in page.crop(tuple(coo[0])).extract_words():
                                res = self.get_text_properties(page.crop((l['x0'], l['top'], l['x1'], l['bottom'])),
                                                               [l['text'], page.page_number, table_num, coo[1]])
                                res["font_size"] = res["property"][0]["size"]
                                res["Is_bold"] = res["property"][0]["is_bold"]
                                res.__delitem__("property")
                                self.value.append(res)
        #print(self.value)
        return self.value

    def convert_to_data(self):
        a = pd.DataFrame(self.value)
        b = a[a["font_size"] == a.groupby(["page_no", "table_num", "row_num"])["font_size"].transform("max")]
        b["words_concat"] = (b.groupby(["page_no", "table_num", "row_num"])["word"].transform(lambda x: "/".join(x)))
        c = b[['page_no', 'table_num', 'row_num', 'words_concat']].drop_duplicates()
        #print(c.to_dict(orient='records'))
        return c.to_dict(orient='records')

    def semantic(self, value):
        a = pd.DataFrame(self.value)
        b = a[["word", "page_no", "table_num", "row_num"]]
        for i in value:
            self.section.append(
                {"section": "Read_from_PDF", "page": i['page_no'], "table": i['table_num'], "ROW": i['row_num'],
                 "heading": i['words_concat'],
                 "section_details":" ".join(b[
                     (i["page_no"] == b["page_no"]) & (b["page_no"] == i["page_no"]) & (b["row_num"] == i["row_num"])][
                     "word"].reset_index(drop=True).tolist())})
        return self.section

    def run(self):
        obj = R_PDF()
        obj.get_page_details()
        zz = obj.convert_to_data()
        obj.semantic(zz)
if __name__ == "__main__":
    r=R_PDF()
    r.run()











