# -*- coding: utf-8 -*-
"""Генерирует PDF «200 неправильных глаголов — американский английский» с русским переводом."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer)
from reportlab.lib.styles import ParagraphStyle

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

# (Infinitive, Past Simple, Past Participle, перевод) — американские формы
VERBS = [
    ("arise", "arose", "arisen", "возникать, появляться"),
    ("awake", "awoke", "awoken", "просыпаться; будить"),
    ("babysit", "babysat", "babysat", "сидеть с ребёнком"),
    ("be", "was / were", "been", "быть, являться"),
    ("bear", "bore", "borne", "нести; терпеть; рожать"),
    ("beat", "beat", "beaten", "бить, побеждать"),
    ("become", "became", "become", "становиться"),
    ("begin", "began", "begun", "начинать"),
    ("bend", "bent", "bent", "сгибать(ся)"),
    ("bet", "bet", "bet", "держать пари, ставить"),
    ("bid", "bid", "bid", "предлагать цену"),
    ("bind", "bound", "bound", "связывать"),
    ("bite", "bit", "bitten", "кусать"),
    ("bleed", "bled", "bled", "кровоточить"),
    ("blow", "blew", "blown", "дуть; взрывать"),
    ("break", "broke", "broken", "ломать, разбивать"),
    ("breed", "bred", "bred", "разводить, выращивать"),
    ("bring", "brought", "brought", "приносить"),
    ("broadcast", "broadcast", "broadcast", "транслировать, вещать"),
    ("build", "built", "built", "строить"),
    ("burn", "burned", "burned", "гореть; жечь"),
    ("burst", "burst", "burst", "лопаться, взрываться"),
    ("buy", "bought", "bought", "покупать"),
    ("cast", "cast", "cast", "бросать; отливать (форму)"),
    ("catch", "caught", "caught", "ловить, поймать"),
    ("choose", "chose", "chosen", "выбирать"),
    ("cling", "clung", "clung", "цепляться, прилипать"),
    ("come", "came", "come", "приходить"),
    ("cost", "cost", "cost", "стоить"),
    ("creep", "crept", "crept", "ползти, красться"),
    ("cut", "cut", "cut", "резать"),
    ("deal", "dealt", "dealt", "иметь дело; раздавать"),
    ("dig", "dug", "dug", "копать"),
    ("dive", "dove", "dived", "нырять"),
    ("do", "did", "done", "делать"),
    ("draw", "drew", "drawn", "рисовать; тянуть"),
    ("dream", "dreamed", "dreamed", "мечтать; видеть сны"),
    ("drink", "drank", "drunk", "пить"),
    ("drive", "drove", "driven", "водить (машину); ехать"),
    ("eat", "ate", "eaten", "есть, кушать"),
    ("fall", "fell", "fallen", "падать"),
    ("feed", "fed", "fed", "кормить"),
    ("feel", "felt", "felt", "чувствовать"),
    ("fight", "fought", "fought", "драться, бороться"),
    ("find", "found", "found", "находить"),
    ("fit", "fit", "fit", "подходить (по размеру)"),
    ("flee", "fled", "fled", "убегать, спасаться"),
    ("fling", "flung", "flung", "швырять"),
    ("fly", "flew", "flown", "летать"),
    ("forbid", "forbade", "forbidden", "запрещать"),
    ("forecast", "forecast", "forecast", "прогнозировать"),
    ("foresee", "foresaw", "foreseen", "предвидеть"),
    ("foretell", "foretold", "foretold", "предсказывать"),
    ("forget", "forgot", "forgotten", "забывать"),
    ("forgive", "forgave", "forgiven", "прощать"),
    ("forgo", "forwent", "forgone", "отказываться от"),
    ("freeze", "froze", "frozen", "замерзать; замораживать"),
    ("get", "got", "gotten", "получать, добираться"),
    ("give", "gave", "given", "давать"),
    ("go", "went", "gone", "идти, ехать"),
    ("grind", "ground", "ground", "молоть, точить"),
    ("grow", "grew", "grown", "расти; выращивать"),
    ("hang", "hung", "hung", "висеть; вешать"),
    ("have", "had", "had", "иметь"),
    ("hear", "heard", "heard", "слышать"),
    ("hide", "hid", "hidden", "прятать(ся)"),
    ("hit", "hit", "hit", "ударять, попадать"),
    ("hold", "held", "held", "держать"),
    ("hurt", "hurt", "hurt", "причинять боль; болеть"),
    ("input", "input", "input", "вводить (данные)"),
    ("keep", "kept", "kept", "хранить, продолжать"),
    ("kneel", "knelt", "knelt", "становиться на колени"),
    ("knit", "knit", "knit", "вязать"),
    ("know", "knew", "known", "знать"),
    ("lay", "laid", "laid", "класть, положить"),
    ("lead", "led", "led", "вести, руководить"),
    ("lean", "leaned", "leaned", "наклоняться, опираться"),
    ("leap", "leaped", "leaped", "прыгать, скакать"),
    ("learn", "learned", "learned", "учить(ся), узнавать"),
    ("leave", "left", "left", "уходить; оставлять"),
    ("lend", "lent", "lent", "одалживать (кому-то)"),
    ("let", "let", "let", "позволять"),
    ("lie", "lay", "lain", "лежать"),
    ("light", "lit", "lit", "зажигать, освещать"),
    ("lose", "lost", "lost", "терять; проигрывать"),
    ("make", "made", "made", "делать, создавать"),
    ("mean", "meant", "meant", "значить, иметь в виду"),
    ("meet", "met", "met", "встречать(ся)"),
    ("mislead", "misled", "misled", "вводить в заблуждение"),
    ("misread", "misread", "misread", "неправильно прочитать"),
    ("mistake", "mistook", "mistaken", "ошибаться, путать"),
    ("misunderstand", "misunderstood", "misunderstood", "неправильно понимать"),
    ("mow", "mowed", "mowed", "косить (траву)"),
    ("offset", "offset", "offset", "компенсировать"),
    ("outdo", "outdid", "outdone", "превосходить"),
    ("outgrow", "outgrew", "outgrown", "вырастать из"),
    ("outrun", "outran", "outrun", "обгонять, опережать"),
    ("overcome", "overcame", "overcome", "преодолевать"),
    ("overdo", "overdid", "overdone", "переусердствовать"),
    ("overeat", "overate", "overeaten", "переедать"),
    ("overhear", "overheard", "overheard", "подслушивать"),
    ("override", "overrode", "overridden", "отменять; преобладать"),
    ("oversee", "oversaw", "overseen", "надзирать, контролировать"),
    ("oversleep", "overslept", "overslept", "проспать"),
    ("overtake", "overtook", "overtaken", "обгонять; настигать"),
    ("overthrow", "overthrew", "overthrown", "свергать"),
    ("pay", "paid", "paid", "платить"),
    ("plead", "pled", "pled", "умолять; признавать вину"),
    ("proofread", "proofread", "proofread", "вычитывать (текст)"),
    ("prove", "proved", "proven", "доказывать"),
    ("put", "put", "put", "класть, ставить"),
    ("quit", "quit", "quit", "бросать, увольняться"),
    ("read", "read", "read", "читать"),
    ("rebuild", "rebuilt", "rebuilt", "перестраивать"),
    ("redo", "redid", "redone", "переделывать"),
    ("remake", "remade", "remade", "переделывать, создавать заново"),
    ("repay", "repaid", "repaid", "возвращать долг"),
    ("resell", "resold", "resold", "перепродавать"),
    ("reset", "reset", "reset", "сбрасывать, перезагружать"),
    ("retell", "retold", "retold", "пересказывать"),
    ("rethink", "rethought", "rethought", "переосмысливать"),
    ("rewind", "rewound", "rewound", "перематывать"),
    ("rewrite", "rewrote", "rewritten", "переписывать"),
    ("rid", "rid", "rid", "избавлять"),
    ("ride", "rode", "ridden", "ездить верхом; кататься"),
    ("ring", "rang", "rung", "звонить, звенеть"),
    ("rise", "rose", "risen", "подниматься, вставать"),
    ("run", "ran", "run", "бегать; управлять"),
    ("say", "said", "said", "говорить, сказать"),
    ("see", "saw", "seen", "видеть"),
    ("seek", "sought", "sought", "искать, стремиться"),
    ("sell", "sold", "sold", "продавать"),
    ("send", "sent", "sent", "отправлять"),
    ("set", "set", "set", "устанавливать, ставить"),
    ("sew", "sewed", "sewn", "шить"),
    ("shake", "shook", "shaken", "трясти"),
    ("shed", "shed", "shed", "проливать; сбрасывать"),
    ("shine", "shone", "shone", "светить, сиять"),
    ("shoot", "shot", "shot", "стрелять; снимать (фильм)"),
    ("show", "showed", "shown", "показывать"),
    ("shrink", "shrank", "shrunk", "сжиматься, садиться (о ткани)"),
    ("shut", "shut", "shut", "закрывать"),
    ("sing", "sang", "sung", "петь"),
    ("sink", "sank", "sunk", "тонуть; погружаться"),
    ("sit", "sat", "sat", "сидеть"),
    ("sleep", "slept", "slept", "спать"),
    ("slide", "slid", "slid", "скользить"),
    ("smell", "smelled", "smelled", "пахнуть; нюхать"),
    ("sneak", "snuck", "snuck", "красться, прошмыгнуть"),
    ("sow", "sowed", "sown", "сеять"),
    ("speak", "spoke", "spoken", "говорить, разговаривать"),
    ("speed", "sped", "sped", "мчаться, ускоряться"),
    ("spell", "spelled", "spelled", "писать/произносить по буквам"),
    ("spend", "spent", "spent", "тратить; проводить (время)"),
    ("spill", "spilled", "spilled", "проливать"),
    ("spin", "spun", "spun", "вращать(ся), крутить"),
    ("spit", "spit", "spit", "плевать"),
    ("split", "split", "split", "разделять, раскалывать"),
    ("spoil", "spoiled", "spoiled", "портить; баловать"),
    ("spread", "spread", "spread", "распространять(ся)"),
    ("spring", "sprang", "sprung", "прыгать, вскакивать"),
    ("stand", "stood", "stood", "стоять"),
    ("steal", "stole", "stolen", "красть"),
    ("stick", "stuck", "stuck", "приклеивать; застревать"),
    ("sting", "stung", "stung", "жалить"),
    ("stink", "stank", "stunk", "вонять"),
    ("strike", "struck", "struck", "ударять; бастовать"),
    ("string", "strung", "strung", "нанизывать, натягивать"),
    ("strive", "strove", "striven", "стремиться, стараться"),
    ("swear", "swore", "sworn", "клясться; ругаться"),
    ("sweep", "swept", "swept", "подметать"),
    ("swell", "swelled", "swollen", "опухать, раздуваться"),
    ("swim", "swam", "swum", "плавать"),
    ("swing", "swung", "swung", "качать(ся), размахивать"),
    ("take", "took", "taken", "брать, взять"),
    ("teach", "taught", "taught", "учить, преподавать"),
    ("tear", "tore", "torn", "рвать"),
    ("tell", "told", "told", "рассказывать, говорить"),
    ("think", "thought", "thought", "думать"),
    ("throw", "threw", "thrown", "бросать"),
    ("thrust", "thrust", "thrust", "толкать, совать"),
    ("tread", "trod", "trodden", "ступать, наступать"),
    ("undergo", "underwent", "undergone", "подвергаться, переносить"),
    ("understand", "understood", "understood", "понимать"),
    ("undertake", "undertook", "undertaken", "предпринимать"),
    ("undo", "undid", "undone", "отменять, расстёгивать"),
    ("unwind", "unwound", "unwound", "разматывать; расслабляться"),
    ("uphold", "upheld", "upheld", "поддерживать, отстаивать"),
    ("upset", "upset", "upset", "расстраивать"),
    ("wake", "woke", "woken", "просыпаться; будить"),
    ("wear", "wore", "worn", "носить (одежду)"),
    ("weave", "wove", "woven", "ткать, плести"),
    ("weep", "wept", "wept", "плакать, рыдать"),
    ("wet", "wet", "wet", "мочить, смачивать"),
    ("win", "won", "won", "выигрывать, побеждать"),
    ("wind", "wound", "wound", "заводить (часы); виться"),
    ("withdraw", "withdrew", "withdrawn", "снимать (деньги); отступать"),
    ("withhold", "withheld", "withheld", "удерживать, скрывать"),
    ("withstand", "withstood", "withstood", "выдерживать, противостоять"),
    ("write", "wrote", "written", "писать"),
]

assert len(VERBS) == 200, f"Ожидалось 200 глаголов, получено {len(VERBS)}"
assert len({v[0] for v in VERBS}) == 200, "Есть дубликаты"

OUT = "200-american-irregular-verbs.pdf"

INK = colors.HexColor("#1d3557")
RED = colors.HexColor("#e63946")
GREEN = colors.HexColor("#2a9d8f")
PAPER = colors.HexColor("#fdfbf4")
STRIPE = colors.HexColor("#eef4f8")

title_style = ParagraphStyle("t", fontName="DejaVu-Bold", fontSize=20,
                             leading=24, textColor=INK, alignment=1,
                             spaceAfter=6)
sub_style = ParagraphStyle("s", fontName="DejaVu", fontSize=10.5,
                           textColor=colors.HexColor("#5a6a7a"), alignment=1,
                           spaceAfter=14)

doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=14*mm, rightMargin=14*mm,
                        topMargin=14*mm, bottomMargin=16*mm,
                        title="200 неправильных глаголов — американский английский",
                        author="Irregular Verbs")

header = ["№", "Infinitive (V1)", "Past Simple (V2)", "Past Participle (V3)", "Перевод"]
rows = [header]
for i, (v1, v2, v3, ru) in enumerate(VERBS, 1):
    rows.append([str(i), v1, v2, v3, ru])

col_widths = [11*mm, 33*mm, 33*mm, 37*mm, 68*mm]

table = Table(rows, colWidths=col_widths, repeatRows=1)
style = [
    ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),
    ("FONTSIZE", (0, 0), (-1, 0), 9.5),
    ("BACKGROUND", (0, 0), (-1, 0), INK),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 1), (-1, -1), "DejaVu"),
    ("FONTSIZE", (0, 1), (-1, -1), 8.6),
    ("FONTNAME", (1, 1), (1, -1), "DejaVu-Bold"),
    ("TEXTCOLOR", (0, 1), (-1, -1), INK),
    ("TEXTCOLOR", (2, 1), (3, -1), RED),
    ("TEXTCOLOR", (4, 1), (4, -1), GREEN),
    ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b9c8d4")),
    ("TOPPADDING", (0, 0), (-1, -1), 2.6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
]
for r in range(1, len(rows)):
    if r % 2 == 0:
        style.append(("BACKGROUND", (0, r), (-1, r), STRIPE))
table.setStyle(TableStyle(style))


def on_page(canvas, doc_):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canvas.setFont("DejaVu", 8)
    canvas.setFillColor(colors.HexColor("#8a97a5"))
    canvas.drawCentredString(A4[0] / 2, 8*mm, f"— {canvas.getPageNumber()} —")
    canvas.restoreState()


story = [
    Paragraph("200 неправильных глаголов", title_style),
    Paragraph("Американский английский (US) · с переводом на русский", sub_style),
    table,
    Spacer(1, 8),
    Paragraph(
        "В таблице даны формы, принятые в США: get — got — <b>gotten</b>, "
        "dive — <b>dove</b>, sneak — <b>snuck</b>, learn — <b>learned</b>, "
        "burn — <b>burned</b>, spell — <b>spelled</b> и т.д. "
        "Британские варианты (got, learnt, burnt, spelt) не включены.",
        ParagraphStyle("n", fontName="DejaVu", fontSize=8.5,
                       textColor=colors.HexColor("#5a6a7a"), leading=12)),
]

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"OK: {OUT}, {len(VERBS)} глаголов")
