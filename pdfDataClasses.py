from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode
import os

class PdfStyle:
        def __init__(self, font='helvetica', fontStyle='', fontSize=14, align='C', textColor=(0,0,0), fillColor=(255,255,255), drawColor=(0,0,0), border=False, height=9):
            self.font = font
            self.fontStyle = fontStyle
            self.fontSize = fontSize
            self.align = align
            self.textColor = textColor
            self.fillColor = fillColor
            self.drawColor = drawColor
            self.border = border
            self.height = height

        def __str__(self):
            return f'Font, FontStyle, FontSize, Alignment, TextColor, FillColor, DrawColor, Border => {self.font}, {self.fontStyle}, {self.fontSize}, {self.align}, {self.textColor}, {self.fillColor}, {self.drawColor}, {self.border}'

class CustomPDF(FPDF):
    def header(self):
        if(self.includeHeader):
            self.image(self.headerImage, 10, 8, 10)

            self.set_font(self.headerStyle.font, self.headerStyle.fontStyle, size=self.headerStyle.fontSize)
            self.set_text_color(*self.headerStyle.textColor)
            self.set_draw_color(*self.headerStyle.drawColor)

            titleWidth = self.get_string_width(self.headerTitle) + 6
            self.set_x((210 - titleWidth) / 2)
            self.set_line_width(.4)

            if(self.headerStyle.fillColor != (255,255,255)):
                self.set_fill_color(*self.headerStyle.fillColor)
                self.cell(titleWidth, self.headerStyle.height, self.headerTitle, border=self.headerStyle.border, new_x="LMARGIN", new_y="NEXT", align='C', fill=True)
            else:
                self.cell(titleWidth, self.headerStyle.height, self.headerTitle, border=self.headerStyle.border, new_x="LMARGIN", new_y="NEXT", align='C', fill=False)
            
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def __init__(self, headerTitle='Test Header Title', headerImage='', headerStyle=None, **args):
        super().__init__(**args)
        self.includeHeader = True
        self.headerTitle = headerTitle
        self.headerImage = headerImage
        self.headerStyle = headerStyle
        self.listPages = []

    def add_customPage(self, page):
        self.listPages.append(page)

    def process_pages(self):
        for page in self.listPages:
            self.add_page()
            page.heading(self)
            page.body(self)
            page.page_image(self)
            page.ending(self)

class PdfTableRecord:
    def __init__(self, dataEntries=[], recordStyle=PdfStyle(fontStyle='', fillColor=(224,235,255), textColor=(0,0,0))):
        self.dataEntries = dataEntries
        self.recordStyle = recordStyle
    
    def add_pdfRecordEntry(self, pdfRecordEntry):
        self.dataEntries.append(pdfRecordEntry)

class PdfSummaryRecord:
    def __init__(self, dataTuple=(), recordStyle=PdfStyle(fontStyle='', fillColor=(224,235,255), textColor=(0,0,0))):
        self.dataTuple = dataTuple
        self.recordStyle = recordStyle

class PdfTableRecordPage:
    def __init__(self, headingText='', headingStyle=None, endingText='', endingStyle=None, bodyStyle=None, pageImage=None):
        self.listPdfTableRecords = []
        self.headingText = headingText
        self.endingText = endingText
        self.headingStyle = headingStyle
        self.endingStyle = endingStyle
        self.bodyStyle = bodyStyle
        self.pageImage = pageImage

    def add_pdfTableRecord(self, pdfTableRecord):
        self.listPdfTableRecords.append(pdfTableRecord)
    
    def heading(self, pdf):
        if(self.headingText != None and self.headingText.strip() != ''):
            pdf.set_font(self.headingStyle.font, self.headingStyle.fontStyle, size=self.headingStyle.fontSize)
            pdf.set_text_color(*self.headingStyle.textColor)
            pdf.set_draw_color(*self.headingStyle.drawColor)

            pdf.set_line_width(0.4)

            if(self.headingStyle.fillColor != (255,255,255)):
                pdf.set_fill_color(*self.headingStyle.fillColor)
                pdf.cell(0, self.headingStyle.height, self.headingText, border=self.headingStyle.border, new_x="LMARGIN", new_y="NEXT", align=self.headingStyle.align, fill=True)
            else:
                pdf.cell(0, self.headingStyle.height, self.headingText, border=self.headingStyle.border, new_x="LMARGIN", new_y="NEXT", align=self.headingStyle.align, fill=False)

            pdf.ln(10)
        
    def body(self, pdf):
        pdf.set_font(self.bodyStyle.font, self.bodyStyle.fontStyle, size=self.bodyStyle.fontSize)
        pdf.set_text_color(*self.bodyStyle.textColor)
        pdf.set_draw_color(*self.bodyStyle.drawColor)
        if(self.bodyStyle.border):
            pdf.set_line_width(0.2)

        if(self.listPdfTableRecords != None and len(self.listPdfTableRecords) != 0):
            tableHeading = self.listPdfTableRecords[0] 
            tableHeadingStyle = FontFace(emphasis=tableHeading.recordStyle.fontStyle, color=tableHeading.recordStyle.textColor, fill_color=tableHeading.recordStyle.fillColor)
            
            with pdf.table(
                borders_layout="NO_HORIZONTAL_LINES",
                cell_fill_color=self.bodyStyle.fillColor,
                cell_fill_mode=TableCellFillMode.ROWS,
                #col_widths=(20, 10, 20, 10),
                headings_style=tableHeadingStyle,
                line_height=self.bodyStyle.height,
                text_align=(self.bodyStyle.align,)*len(tableHeading.dataEntries),
                width=190,
            ) as table:             
                for i, pdfTableRecord in enumerate(self.listPdfTableRecords):
                    row = table.row()
                    if(i != 0):
                        if(self.bodyStyle.fontStyle != pdfTableRecord.recordStyle.fontStyle or self.bodyStyle.textColor != pdfTableRecord.recordStyle.textColor or self.bodyStyle.fillColor != pdfTableRecord.recordStyle.fillColor): 
                            pdfRecordStyle = FontFace(emphasis=pdfTableRecord.recordStyle.fontStyle, color=pdfTableRecord.recordStyle.textColor, fill_color=pdfTableRecord.recordStyle.fillColor)
                            row.style = pdfRecordStyle
                    for dataCell in pdfTableRecord.dataEntries:
                        row.cell(dataCell)
    def page_image(self, pdf):
        if(self.pageImage != None):
            pdf.image(self.pageImage, w=pdf.epw)

    def ending(self, pdf):
        pdf.set_font(self.endingStyle.font, self.endingStyle.fontStyle, size=self.endingStyle.fontSize)
        pdf.cell(190,10,self.endingText, align=self.endingStyle.align, new_x="LMARGIN", new_y="NEXT")

class PdfSummaryPage:
    def __init__(self, headingText='', headingStyle=None, endingText='', endingStyle=None, bodyStyle=None, pageImage=None):
        self.listPdfSummaryRecords = []
        self.headingText = headingText
        self.endingText = endingText
        self.headingStyle = headingStyle
        self.endingStyle = endingStyle
        self.bodyStyle = bodyStyle
        self.pageImage = pageImage

    def add_pdfSummaryRecord(self, summaryRecord):
        self.listPdfSummaryRecords.append(summaryRecord)

    def heading(self, pdf):
        if(self.headingText != None and self.headingText.strip() != ''):
            pdf.set_font(self.headingStyle.font, self.headingStyle.fontStyle, size=self.headingStyle.fontSize)
            pdf.set_text_color(*self.headingStyle.textColor)
            pdf.set_draw_color(*self.headingStyle.drawColor)

            pdf.set_line_width(0.4)

            if(self.headingStyle.fillColor != (255,255,255)):
                pdf.set_fill_color(*self.headingStyle.fillColor)
                pdf.cell(0, self.headingStyle.height, self.headingText, border=self.headingStyle.border, new_x="LMARGIN", new_y="NEXT", align=self.headingStyle.align, fill=True)
            else:
                pdf.cell(0, self.headingStyle.height, self.headingText, border=self.headingStyle.border, new_x="LMARGIN", new_y="NEXT", align=self.headingStyle.align, fill=False)
        
    def body(self, pdf):
        pdf.set_font(self.bodyStyle.font, self.bodyStyle.fontStyle, size=self.bodyStyle.fontSize)
        pdf.set_text_color(*self.bodyStyle.textColor)
        row = None
        if(self.bodyStyle.border):
            pdf.set_line_width(0.2)
            pdf.set_draw_color(*self.bodyStyle.drawColor)

        if(self.listPdfSummaryRecords != None and len(self.listPdfSummaryRecords) != 0):
            tableHeading = self.listPdfSummaryRecords[0] 
            tableHeadingStyle = FontFace(emphasis=tableHeading.recordStyle.fontStyle, color=tableHeading.recordStyle.textColor, fill_color=tableHeading.recordStyle.fillColor)
            
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                cell_fill_color=self.bodyStyle.fillColor,
                cell_fill_mode=TableCellFillMode.COLUMNS,
                #col_widths=(20, 10, 20, 10),
                headings_style=tableHeadingStyle,
                line_height=self.bodyStyle.height,
                text_align=(self.bodyStyle.align,)*4,
                width=190,
            ) as table:
                row=table.row()             
                for i, pdfSummaryRecord in enumerate(self.listPdfSummaryRecords):
                    if(i % 2 == 0):
                        row = table.row()
                        
                    item, value = pdfSummaryRecord.dataTuple
                    itemStyle = pdfSummaryRecord.recordStyle
                
                    if(self.bodyStyle.fontStyle != itemStyle.fontStyle or self.bodyStyle.textColor != itemStyle.textColor or self.bodyStyle.fillColor != itemStyle.fillColor): 
                        pdfRecordStyle = FontFace(emphasis=itemStyle.fontStyle, color=itemStyle.textColor, fill_color=itemStyle.fillColor)
                        row.cell(item, style=pdfRecordStyle)
                        row.cell(value, style=pdfRecordStyle)
                    else:
                        row.cell(item, style = FontFace(emphasis=self.bodyStyle.fontStyle + 'B', color=self.bodyStyle.textColor, fill_color=self.bodyStyle.fillColor))
                        row.cell(value, style = FontFace(emphasis=self.bodyStyle.fontStyle, color=self.bodyStyle.textColor, fill_color=(255,245,245)))
    
    def page_image(self, pdf):
        if(self.pageImage != None):
            pdf.image(self.pageImage, w=pdf.epw)

    def ending(self, pdf):
        pdf.set_font(self.endingStyle.font, self.endingStyle.fontStyle, size=self.endingStyle.fontSize)
        pdf.cell(190,10,self.endingText, align=self.endingStyle.align, new_x="LMARGIN", new_y="NEXT")


if __name__ == '__main__':
    headerStyle = PdfStyle(font='helvetica', fontStyle='B', fontSize=15, align='C',textColor=(220, 50, 50), fillColor=(230, 230, 0), drawColor=(0,80,180),border=True,height=9)
    customPdf = CustomPDF(headerImage=(str(os.getcwd()) + '\\railwaylogo.ico').replace('\\', '/'), headerTitle='SPM Analyis Report', headerStyle=headerStyle)

    headingStyle = PdfStyle(font='helvetica', fontStyle='B', fontSize=12, align='L',textColor=(0,0,0), fillColor=(200,220,255), drawColor=(0,80,180),border=False,height=6)
    endingStyle = PdfStyle(font='helvetica', fontStyle='B', fontSize=8, align='C',textColor=(0,0,0), fillColor=(255,255,255), drawColor=(255,255,255),border=False,height=6)
    bodyStyle = PdfStyle(font='helvetica', fontStyle='', fontSize=7, align='C',textColor=(0,0,0), fillColor=(224, 235, 255), drawColor=(255, 0, 0),border=True,height=6)
    
    srPage = PdfTableRecordPage(headingText='Gradient Report',headingStyle=headingStyle, endingText='***End of Gradient Report***', endingStyle=endingStyle, bodyStyle=bodyStyle)
    
    srHeadingData = ['S.No','SR From', 'SR To', 'From Km', 'To Km', 'Distance', 'SR Speed', 'SR Type', 'Entry Speed', 'Exit Speed', 'Max Speed', 'Min Speed', 'Complied']
    srHeadingStyle = PdfStyle(font='helvetica', fontStyle='B', fontSize=7, align='C',textColor=(0,0,0), fillColor=(255, 100, 0), drawColor=(255, 0, 0),border=True,height=6)
    srHeading = PdfTableRecord(srHeadingData, srHeadingStyle)
    
    srRecordStyle = PdfStyle(fontStyle='',textColor=(0,0,0), fillColor=(224, 235, 255))
    srRecordData = ['1','149/10','150/11','149.567','150.465','1.3','70','PSR','80','90','50','70','No']
    srRecord = PdfTableRecord(srRecordData, srRecordStyle)
    
    srRecordStyle2 = PdfStyle(fontStyle='BI', textColor=(255,0,0), fillColor=(255, 255, 0))
    srRecordData2 = ['1','149/10','150/11','149.567','150.465','1.3','70','PSR','80','90','50','70','No']
    srRecord2 = PdfTableRecord(srRecordData2, srRecordStyle2)

    srPage.add_pdfTableRecord(srHeading)
    srPage.add_pdfTableRecord(srRecord)
    srPage.add_pdfTableRecord(srRecord)
    srPage.add_pdfTableRecord(srRecord)
    srPage.add_pdfTableRecord(srRecord)
    srPage.add_pdfTableRecord(srRecord2)
    srPage.add_pdfTableRecord(srRecord)
    srPage.add_pdfTableRecord(srRecord)

    bodyStyle = PdfStyle(font='helvetica', fontStyle='', fontSize=10, align='L',textColor=(0,0,0), fillColor=(224, 235, 255), drawColor=(255, 0, 0),border=False,height=10)
    headingStyle = PdfStyle(font='helvetica', fontStyle='B', fontSize=12, align='L',textColor=(0,0,0), fillColor=(200,220,255), drawColor=(0,80,180),border=False,height=10)
    summaryPage = PdfSummaryPage(headingText='Summary Report',headingStyle=headingStyle, endingText='***End of Summary Report***', endingStyle=endingStyle, bodyStyle=bodyStyle)
    
    summaryRecordStyle = PdfStyle(fontStyle='',textColor=(0,0,0), fillColor=(224, 235, 255))
    summaryRecordTuple = ('LP Name', 'ABCD')
    summaryRecord = PdfSummaryRecord(summaryRecordTuple, summaryRecordStyle)

    summaryRecordStyle2 = PdfStyle(fontStyle='BI', textColor=(255,0,0), fillColor=(255, 255, 0))
    summaryRecordTuple2 = ('LP Name', 'ABCD')
    summaryRecord2 = PdfSummaryRecord(summaryRecordTuple2, summaryRecordStyle2)

    summaryPage.add_pdfSummaryRecord(summaryRecord=summaryRecord)
    summaryPage.add_pdfSummaryRecord(summaryRecord=summaryRecord)
    summaryPage.add_pdfSummaryRecord(summaryRecord=summaryRecord)
    summaryPage.add_pdfSummaryRecord(summaryRecord=summaryRecord2)
    summaryPage.add_pdfSummaryRecord(summaryRecord=summaryRecord)
    summaryPage.add_pdfSummaryRecord(summaryRecord=summaryRecord)
    summaryPage.add_pdfSummaryRecord(summaryRecord=summaryRecord)

    customPdf.add_customPage(summaryPage)
    customPdf.add_customPage(srPage)
    
    customPdf.process_pages()
    customPdf.output("D:/testReport.pdf")

