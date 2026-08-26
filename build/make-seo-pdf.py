#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the SEO summary PDF for Mike.

Written in Colson's voice, for a client who runs a grounds care crew and not a
web team. Jargon is either avoided or explained in the same breath.
"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, HRFlowable)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "Cline-SEO-Summary.pdf")

FOREST = colors.HexColor("#1B3324")
AMBER  = colors.HexColor("#A8501F")
GOLD   = colors.HexColor("#8C651D")
MUTED  = colors.HexColor("#5C6656")
RULE   = colors.HexColor("#D6CDB8")
PAPER  = colors.HexColor("#FCFAF4")
INK    = colors.HexColor("#12160F")

S = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=26, leading=30,
                            textColor=FOREST, spaceAfter=4),
    "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=11, leading=15,
                          textColor=MUTED, spaceAfter=18),
    "eyebrow": ParagraphStyle("eyebrow", fontName="Helvetica-Bold", fontSize=8, leading=11,
                              textColor=AMBER, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=15, leading=19,
                         textColor=FOREST, spaceBefore=18, spaceAfter=7),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11, leading=14,
                         textColor=INK, spaceBefore=11, spaceAfter=4),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.5,
                           textColor=INK, spaceAfter=8, alignment=TA_LEFT),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=9, leading=13,
                            textColor=MUTED, spaceAfter=6),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=10, leading=14.5,
                             textColor=INK, leftIndent=14, bulletIndent=3, spaceAfter=4),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9.5, leading=13,
                           textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
                            textColor=FOREST),
    "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
                            textColor=PAPER),
}


def P(t, s="body"):
    return Paragraph(t, S[s])


def bullets(items, style="bullet"):
    return [Paragraph(t, S[style], bulletText="•") for t in items]


def rule(space_before=6, space_after=10):
    return HRFlowable(width="100%", thickness=0.75, color=RULE,
                      spaceBefore=space_before, spaceAfter=space_after)


def table(rows, widths, header=True):
    data = []
    for i, r in enumerate(rows):
        st = "cellh" if (header and i == 0) else "cell"
        data.append([Paragraph(c, S[st]) for c in r])
    t = Table(data, colWidths=widths, hAlign="LEFT")
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, RULE),
        ("BOX", (0, 0), (-1, -1), 0.75, RULE),
    ]
    if header:
        cmds += [("BACKGROUND", (0, 0), (-1, 0), FOREST)]
    t.setStyle(TableStyle(cmds))
    return t


def priority_block(num, title, why, what):
    """A numbered action card."""
    inner = [
        Paragraph(f'<font color="#A8501F"><b>{num}</b></font>&nbsp;&nbsp;<b>{title}</b>',
                  ParagraphStyle("pt", fontName="Helvetica", fontSize=12, leading=16,
                                 textColor=FOREST, spaceAfter=5)),
        Paragraph(f'<i>{why}</i>', S["small"]),
    ] + bullets(what)
    t = Table([[inner]], colWidths=[6.6 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return KeepTogether([t, Spacer(1, 10)])


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = LETTER
    canvas.setFillColor(FOREST)
    canvas.rect(0, h - 0.32 * inch, w, 0.32 * inch, stroke=0, fill=1)
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 0.32 * inch, 1.7 * inch, 0.32 * inch, stroke=0, fill=1)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.9 * inch, 0.45 * inch, "Cline Property Management - website and SEO summary")
    canvas.drawRightString(w - 0.9 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=LETTER,
        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
        topMargin=0.85 * inch, bottomMargin=0.8 * inch,
        title="Cline Property Management - Website and SEO Summary",
        author="Colson Rice",
        subject="What is live, and what I need from you",
    )
    st = []

    # ---- cover ----
    st.append(P("PREPARED FOR MIKE CLINE", "eyebrow"))
    st.append(P("Your website is live.", "title"))
    st.append(P("Here is what I built, what it is already doing for you in Google, "
                "and the handful of things only you can do to make it work harder.", "sub"))
    st.append(rule(0, 14))

    st.append(P("clinepropertymgmt.com", "h3"))
    st.append(P("The site is live, secure, and open to Google. Everything below is already "
                "done and running unless I have flagged it as something I need from you.", "body"))

    # ---- what is live ----
    st.append(P("What is on the site", "h2"))
    st.append(table([
        ["", ""],
        ["11 service pages", "A page for each service, plus home, gallery, about and contact. "
                     "Each service page is written to be found on its own."],
        ["10 communities", "Your service area is spelled out, including the part people get wrong: "
                           "mowing is Whitestown, Zionsville and West Carmel only, while your other "
                           "ten services cover all ten."],
        ["Project gallery", "Real project photos stay grouped by service, before-and-after sets stay "
                            "together, and newer service examples appear under the right filters."],
        ["3 video clips", "Short, silent, and they do not load until someone scrolls to them, so "
                          "they never slow the site down."],
    ], [1.35 * inch, 5.0 * inch], header=False))

    # ---- what I did for SEO ----
    st.append(P("What I did so people can find you", "h2"))
    st.append(P("SEO is mostly unglamorous plumbing. Here is the plain-English version of what "
                "is in place.", "body"))

    st.append(P("A real address of your own", "h3"))
    st.append(P("The site sits on clinepropertymgmt.com with a security certificate, so browsers "
                "show it as safe. Google will not seriously rank a site that lives on a borrowed "
                "address, so this had to come first.", "body"))

    st.append(P("A page per service, per town", "h3"))
    st.append(P("Someone searching \"lawn mowing Zionsville\" and someone searching \"snow removal \"\n"
                "commercial lot\" are two different customers. Each service has its own page with "
                "its own title and description, so Google has something specific to show each of "
                "them instead of dumping everyone on the home page.", "body"))

    st.append(P("Machine-readable business details", "h3"))
    st.append(P("Behind the scenes, every page carries structured data - a summary Google reads "
                "directly rather than guessing at. It states your business type, your services, "
                "your service area, your phone number and your FAQs. This is what lets Google "
                "show extra detail under your listing instead of a plain blue link.", "body"))

    st.append(P("A map of the site, submitted to Google", "h3"))
    st.append(P("There is a sitemap listing every public page and its key images so they can turn "
                "up in Google Images. For a business whose work is "
                "this visual, image search is a real way to get found. I have also verified the "
                "site with Google Search Console, which is the dashboard that reports how you are "
                "doing in search.", "body"))

    st.append(P("Fast, and works properly on a phone", "h3"))
    st.append(P("Most people will see this on a phone, standing in their own yard. The site is "
                "built as plain fast pages with compressed images, and I have checked the layout "
                "and colour contrast on phone, tablet and desktop. Google measures speed and "
                "mobile usability directly, so this counts twice: better for your customers, and "
                "better for ranking.", "body"))

    st.append(P("A summary file for AI assistants", "h3"))
    st.append(P("More people are asking ChatGPT and similar tools for recommendations. I have "
                "added a file that hands those tools a clean summary of your services and service "
                "area, so if one is asked who mows in Zionsville it has accurate information "
                "rather than a guess. Being straight with you: this is a new convention and no "
                "search engine promises to use it. It cost nothing to add and it may pay off.", "body"))

    # ---- what I need ----
    st.append(P("What I need from you", "h2"))
    st.append(P("This is the honest part. The site is built about as well as a site can be "
                "built. What is left is the things that have to come from you, and between them "
                "they are worth more than everything above.", "body"))

    st.append(priority_block(
        "1", "Switch the contact form on - this week",
        "Until you do this, every enquiry from the website is thrown away.",
        ["Someone submits the form once. That first one does not reach you - it triggers "
         "a confirmation email instead.",
         "You will get an email asking you to confirm. Check spam and the Promotions tab, "
         "it often lands there.",
         "Click the link. That is it, once and for all.",
         "Then submit the form again to check a real enquiry arrives. Try hitting reply on "
         "it too - it should go straight back to the customer.",
         "Every enquiry has [Cline Web] in the subject, so one Gmail filter catches them all."]))

    st.append(priority_block(
        "2", "Set up your Google Business Profile - this week",
        "This is worth more than everything else on this page put together.",
        ["Go to business.google.com and search your business name first, in case a listing "
         "already exists that you can claim.",
         "Set it up as a service-area business, not a shopfront. List all ten communities.",
         "Main category: Lawn Care Service. Add Snow Removal Service and Pressure Washing "
         "Service as extras.",
         "Use exactly the same business name, phone number and website address as the site. "
         "Google cross-checks these and mismatches count against you.",
         "You will have to verify it is really you, usually by postcard or phone. Only you "
         "can do this part."]))

    st.append(P("Why this one matters most: when somebody searches \"lawn mowing near me\", "
                "Google shows a map with three businesses on it before any normal results. "
                "That map is fed by Business Profiles, not by websites. Without one you are "
                "invisible in the place most local customers actually look.", "small"))

    st.append(priority_block(
        "3", "Get me three to five reviews - this month",
        "The single biggest gap on the site, and it affects your ranking as well.",
        ["Ask customers you have looked after for years. They are usually glad to.",
         "First name and town is plenty - \"Sarah M., Zionsville\".",
         "Google reviews are worth more than anything written on the site, because they "
         "count towards where you appear on that map.",
         "There are no reviews anywhere on the site right now. I left that space empty on "
         "purpose rather than write something you did not say."]))

    st.append(priority_block(
        "4", "Real photographs still worth collecting",
        "The gallery is much stronger now, but two kinds of real project photos would build more trust.",
        ["Snow: one driveway or lot, photographed covered in snow and then again once you "
         "have cleared it, from the same spot both times. That pairing is the strongest "
         "possible advert for snow work and it drops straight into the site.",
         "You, your crew, or a truck with your name on it while work is underway. A clear, "
         "branded crew photo is one of the strongest trust signals for a trade business.",
         "Keep taking matched before-and-after photos from the same position. They make the "
         "result immediately clear and are easy to keep together on the site."]))

    st.append(priority_block(
        "5", "Details only you can confirm",
        "The site states these as fact. If any is wrong, tell me and I will change it.",
        ["Are you insured, and can you produce a certificate on request? Property managers "
         "ask for this before you set foot on site.",
         "Snow: is two inches your actual trigger depth? Same for commercial and residential?",
         "Do you offer both seasonal snow contracts and per-event billing?",
         "Does gutter cleanout include downspout flushing, or debris removal only? The service "
         "now has its own page and the scope should stay exact.",
         "Municipal work - do you contract directly, or through a general contractor?",
         "Your business hours would strengthen the site and can be added once confirmed."]))

    # ---- expectations ----
    st.append(P("What to expect, and when", "h2"))
    st.append(table([
        ["When", "What happens"],
        ["First 1 to 2 weeks", "Google finds and files the pages. Do not read an empty "
                               "Search Console as a problem - a brand new address takes time."],
        ["Weeks 2 to 6", "You start appearing for specific searches, usually your business "
                         "name first, then service-plus-town phrases."],
        ["Month 2 onward", "Rankings build slowly. This is where the Business Profile and "
                           "reviews do the heavy lifting, not the website."],
    ], [1.55 * inch, 4.8 * inch]))

    st.append(Spacer(1, 8))
    st.append(P("SEO is not a switch. It is a slow accumulation, and the things that move it "
                "fastest for a local trade business are a Business Profile, real reviews, and a "
                "site that loads fast and says clearly what you do and where. Three of those four "
                "are done.", "body"))

    st.append(rule(12, 10))
    st.append(P("Anything on this list you would rather I handled, send it over and I will do it. "
                "The four items above are the ones that genuinely have to come from you.", "small"))
    st.append(P("Colson", "h3"))

    doc.build(st, onFirstPage=header_footer, onLaterPages=header_footer)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
