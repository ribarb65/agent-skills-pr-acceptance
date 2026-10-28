"""Builds the course project proposal (Word) in the format of the original proposal.

Usage: python report/build_proposal.py report/Project_Proposal.docx
"""
import sys

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

out = sys.argv[1] if len(sys.argv) > 1 else "report/Project_Proposal.docx"
doc = Document()

sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(sec, side, Inches(1))

normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.space_after = Pt(12)
normal.paragraph_format.line_spacing = 1.0


def para(*runs):
    p = doc.add_paragraph()
    for text, bold, underline in runs:
        r = p.add_run(text)
        r.bold, r.underline = bold, underline
    return p


def heading(text):
    para((text, True, False))


def body(text):
    para((text, False, False))


title = para(("Final Project Proposal", True, True))
title.runs[0].font.size = Pt(14)

para(("Dataset: ", True, False),
     ("GitSkills – MSR 2027 Mining Challenge (complemented with AIDev and the GitHub API)", False, False))

heading("Main Objective")
body("Analyze the adoption of agent skills (SKILL.md files) in GitHub repositories, for the purpose of evaluating "
     "its effect, with respect to the acceptance rate of pull requests authored by AI coding agents and how this "
     "effect varies with the match between the pull request’s task and the skill, the compatibility between the "
     "agent and the skill’s location, and the origin of the skill (copied or written locally), from the viewpoint "
     "of open-source maintainers and developers who write or adopt skills for coding agents, in the context of "
     "GitSkills linked with AIDev v5, restricted to repositories that adopted skills from October 2025 onward with "
     "at least five agentic pull requests before adoption, compared at the same dates with repositories that have "
     "not yet adopted skills.")

heading("Research Question 1 (RQ1)")
body("Does adding AI agent skills (SKILL.md files) to a repository change the acceptance rate of pull requests "
     "authored by AI agents?")

heading("Research Question 2 (RQ2)")
body("Does this effect vary with the match between the pull request’s task and the skill, the compatibility "
     "between the agent and the skill’s location, and the origin of the skill (copied from elsewhere or "
     "written locally)?")

cp = doc.core_properties
cp.author = cp.last_modified_by = "Group Atwater"
cp.comments = ""
cp.title = "Final Project Proposal"
doc.save(out)
print("wrote", out)
