import json
from html import escape
from pathlib import Path

import streamlit as st


st.set_page_config(
	page_title="Crochetly | Learn at your own pace",
	page_icon="🧶",
	layout="wide",
)


# Warm, crochet-inspired visual system.
st.markdown(
	"""
	<style>
	:root {
		--cream: #fbf7f0;
		--paper: #fffdf9;
		--ink: #332b27;
		--muted: #786d65;
		--rose: #b96358;
		--rose-dark: #965047;
		--sage: #788675;
		--line: #e9dfd3;
	}
	.stApp { background: var(--cream); color: var(--ink); }
	[data-testid="stHeader"] { background: transparent; }
	[data-testid="stMainBlockContainer"] { max-width: 1120px; padding-top: 2rem; }
	h1, h2, h3 { color: var(--ink); letter-spacing: 0; }
	h1 { font-size: clamp(2rem, 4vw, 3.15rem); line-height: 1.08; }
	h2 { font-size: 1.7rem; }
	p, li { color: var(--muted); line-height: 1.65; }
	[data-testid="stVerticalBlockBorderWrapper"] {
		background: var(--paper);
		border: 1px solid var(--line);
		border-radius: 14px;
		box-shadow: 0 8px 24px rgba(68, 48, 35, 0.045);
		height: 100%;
	}
	[data-testid="stVerticalBlockBorderWrapper"] > div { padding: 1.15rem; }
	.brand { color: var(--rose-dark); font-weight: 700; font-size: 1.05rem; }
	.eyebrow { color: var(--rose-dark); font-size: .76rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; }
	.hero-copy { max-width: 650px; font-size: 1.08rem; }
	.project-icon { font-size: 2rem; line-height: 1; margin-bottom: .7rem; }
	.project-title { color: var(--ink); font-size: 1.2rem; font-weight: 700; line-height: 1.3; min-height: 3.1rem; }
	.project-description { min-height: 4.8rem; }
	.meta-line { color: var(--muted); font-size: .88rem; margin: .25rem 0 .8rem; }
	.pill { display: inline-block; background: #f3e8df; color: #754d43; border-radius: 999px; padding: .28rem .65rem; font-size: .78rem; font-weight: 650; }
	.material-name { color: var(--ink); font-weight: 700; font-size: 1rem; }
	.material-quantity { color: var(--rose-dark); font-size: .82rem; font-weight: 650; }
	.glossary-list { border-top: 1px solid var(--line); }
	.glossary-row { display: grid; grid-template-columns: minmax(4.5rem, .28fr) minmax(0, 1fr); gap: 1rem; padding: .85rem .35rem; border-bottom: 1px solid var(--line); }
	.glossary-abbr { color: var(--rose-dark); font-size: 1rem; font-weight: 750; }
	.glossary-name { color: var(--ink); font-weight: 650; }
	.glossary-description { color: var(--muted); font-size: .9rem; line-height: 1.5; margin-top: .15rem; }
	.lesson-step { color: var(--rose-dark); font-weight: 700; }
	.lesson-project-header { display: flex; align-items: center; gap: .9rem; margin: .8rem 0 1.2rem; }
	.lesson-project-emoji { font-size: 2.5rem; line-height: 1; }
	.lesson-project-title { color: var(--ink); font-size: 1.45rem; font-weight: 700; line-height: 1.25; }
	.lesson-progress-label { color: var(--rose-dark); font-size: .82rem; font-weight: 700; margin-bottom: .35rem; }
	.completion-mark { font-size: 3rem; line-height: 1; margin-bottom: .8rem; }
	.completion-copy { color: var(--muted); font-size: 1.05rem; }
	.quiet-note { border-left: 3px solid #c98a78; padding: .7rem 1rem; color: var(--muted); background: #f7eee6; border-radius: 0 8px 8px 0; }
	div.stButton > button {
		border-radius: 9px;
		min-height: 2.7rem;
		padding: .65rem 1.1rem;
		transition: background-color .15s ease, border-color .15s ease;
	}
	div.stButton > button[kind="primary"] { background: var(--rose); border-color: var(--rose); color: #fff !important; font-weight: 700; }
	div.stButton > button[kind="primary"] p { color: #fff !important; font-weight: 700; }
	div.stButton > button[kind="primary"]:hover { background: var(--rose-dark); border-color: var(--rose-dark); color: #fff !important; }
	div.stButton > button:not([kind="primary"]) { border-color: var(--line); color: var(--ink); background: var(--paper); }
	[data-testid="stExpander"] { background: var(--paper); border: 1px solid #e5d5c5; border-radius: 12px; overflow: hidden; }
	[data-testid="stExpander"] details { background: var(--paper); }
	[data-testid="stExpander"] details > summary { background: #efe3d6; color: var(--ink); padding: .7rem 1rem; }
	[data-testid="stExpander"] details > summary:hover { background: #e9d9c9; color: var(--ink); }
	[data-testid="stExpander"] details[open] > summary { background: #efe3d6; color: var(--ink); border-bottom: 1px solid #e5d5c5; }
	[data-testid="stExpander"] details > summary p { color: var(--ink); font-weight: 650; }
	[data-testid="stExpander"] details > summary svg { color: var(--ink); fill: var(--ink); }
	[data-testid="stExpander"] [data-testid="stExpanderDetails"] { background: var(--paper); color: var(--ink); padding: .55rem 1rem .8rem; }
	[data-testid="stExpander"] [data-testid="stExpanderDetails"] p,
	[data-testid="stExpander"] [data-testid="stExpanderDetails"] li { color: var(--ink); font-size: .98rem; line-height: 1.6; }
	[data-testid="stExpander"] [data-testid="stExpanderDetails"] li { margin-bottom: .55rem; }
	[data-testid="stProgressBar"] > div > div { background: var(--rose); }
	@media (max-width: 700px) {
		[data-testid="stMainBlockContainer"] { padding: 1rem 1rem 2rem; }
		.project-title, .project-description { min-height: 0; }
		.glossary-row { grid-template-columns: minmax(3.5rem, .3fr) minmax(0, 1fr); gap: .7rem; }
		.lesson-project-title { font-size: 1.2rem; }
	}
	</style>
	""",
	unsafe_allow_html=True,
)


# Keep project data loading independent from the rendered views.
def load_projects():
	project_file = Path(__file__).parent / "data" / "project.json"
	with project_file.open(encoding="utf-8") as file:
		data = json.load(file)
	projects = data.get("projects", []) if isinstance(data, dict) else []
	return [project for project in projects if isinstance(project, dict)]


def text(value, fallback=""):
	return escape(str(value if value is not None else fallback))


def project_description(project):
	description = project.get("description")
	if description:
		return description
	steps = project.get("steps") or []
	first_step = steps[0] if steps and isinstance(steps[0], dict) else {}
	first_name = first_step.get("name")
	if first_name:
		return f"Start with {first_name.lower()}, then build your project one small step at a time."
	return f"A guided, step-by-step {project.get('craft_type', 'crochet')} project for your next quiet making moment."


def render_project_card(project):
	project_id = text(project.get("project_id", "project"))
	with st.container(border=True):
		st.markdown(
			f"""
			<div class="project-icon">{text(project.get('emoji'), '🧶')}</div>
			<div class="project-title">{text(project.get('title'), 'Crochet project')}</div>
			<div class="meta-line"><span class="pill">{text(project.get('difficulty'), 'Beginner')}</span>
			&nbsp; {text(project.get('estimated_time'), 'Time varies')}</div>
			<p class="project-description">{text(project_description(project))}</p>
			""",
			unsafe_allow_html=True,
		)
		if st.button("Start learning →", key=f"select_{project_id}", type="primary", use_container_width=True):
			st.session_state.selected_project_id = project.get("project_id")
			st.session_state.lesson_started = False
			st.session_state.show_stuck = False
			st.rerun()


def render_material_card(material, key):
	if not isinstance(material, dict):
		return
	with st.container(border=True):
		st.markdown(
			f"""
			<div class="material-name">{text(material.get('item'), 'Material')}</div>
			<p>{text(material.get('detail'), 'No extra detail provided.')}</p>
			<div class="material-quantity">{text(material.get('quantity'), 'As needed')}</div>
			""",
			unsafe_allow_html=True,
		)


def render_glossary(entries):
	entries = [entry for entry in entries if isinstance(entry, dict)]
	if not entries:
		st.caption("No stitch terms listed for this project yet.")
		return
	rows = []
	for entry in entries:
		rows.append(
			f'<div class="glossary-row"><div class="glossary-abbr">{text(entry.get("abbreviation"), "Term")}</div>'
			f'<div><div class="glossary-name">{text(entry.get("name"), "Crochet stitch")}</div>'
			f'<div class="glossary-description">{text(entry.get("description"), "No definition provided yet.")}</div></div></div>'
		)
	st.markdown(f'<div class="glossary-list">{"".join(rows)}</div>', unsafe_allow_html=True)


def render_progress(step_index, step_count):
	progress = (step_index + 1) / step_count if step_count else 0
	st.markdown(f'<div class="lesson-progress-label">STEP {step_index + 1} OF {step_count}</div>', unsafe_allow_html=True)
	st.progress(progress)


def build_step_context(project, step, user_question):
	common_mistakes = step.get("common_mistakes")
	return {
		"project_title": project.get("title"),
		"step_number": step.get("step_number"),
		"step_name": step.get("name"),
		"instruction": step.get("instruction"),
		"stitch_count": step.get("stitch_count"),
		"expected_result": step.get("expected_result"),
		"common_mistakes": common_mistakes if isinstance(common_mistakes, list) else [],
		"ai_help_context": step.get("ai_help_context"),
		"user_question": user_question.strip(),
	}


def render_lesson_step(step):
	instruction = step.get("instruction")
	expected_result = step.get("expected_result")
	mistakes = step.get("common_mistakes")
	mistakes = [mistake for mistake in mistakes if isinstance(mistake, str) and mistake.strip()] if isinstance(mistakes, list) else []

	if expected_result:
		instruction_column, result_column = st.columns([1.6, 1], gap="large")
	else:
		instruction_column = st.container()
		result_column = None

	with instruction_column:
		with st.container(border=True):
			st.markdown("#### Your next move")
			if instruction:
				st.markdown(text(instruction))
			if step.get("stitch_count") is not None:
				st.markdown(f'<span class="pill">Stitch count: {text(step.get("stitch_count"))}</span>', unsafe_allow_html=True)
			if mistakes:
				with st.expander("A couple of things to watch for"):
					for mistake in mistakes:
						st.markdown(f"- {text(mistake)}")

	if result_column is not None:
		with result_column:
			with st.container(border=True):
				st.markdown("#### What you should have now")
				st.markdown(text(expected_result))


try:
	projects = load_projects()
except (OSError, json.JSONDecodeError) as error:
	st.error(f"Crochetly couldn't load its project library: {error}")
	st.stop()

if not projects:
	st.warning("There are no projects in the project library yet.")
	st.stop()

st.session_state.setdefault("selected_project_id", None)
st.session_state.setdefault("lesson_started", False)
st.session_state.setdefault("lesson_progress", {})
st.session_state.setdefault("lesson_completed", {})
st.session_state.setdefault("show_stuck", False)
st.session_state.setdefault("pending_help_context", None)

project_by_id = {project.get("project_id"): project for project in projects}
selected_project = project_by_id.get(st.session_state.selected_project_id)
if st.session_state.selected_project_id and not selected_project:
	st.session_state.selected_project_id = None
	st.session_state.lesson_started = False


# Home: project selection.
if selected_project is None:
	st.markdown('<div class="brand">🧶 Crochetly</div>', unsafe_allow_html=True)
	st.write("")
	st.markdown('<div class="eyebrow">A little more confidence, one stitch at a time</div>', unsafe_allow_html=True)
	st.title("Learn crochet without getting lost.")
	st.markdown(
		'<p class="hero-copy">Follow a project one friendly step at a time, with clear guidance for the moments a tutorial leaves you wondering what to do next.</p>',
		unsafe_allow_html=True,
	)
	st.write("")
	st.subheader("What do you want to make?")
	project_columns = st.columns(min(3, len(projects)), gap="large")
	for index, project in enumerate(projects):
		with project_columns[index % len(project_columns)]:
			render_project_card(project)
	st.write("")
	st.markdown(
		'<div class="quiet-note">Made for those moments when a tutorial makes you pause and think, “Wait... where does the hook go?”</div>',
		unsafe_allow_html=True,
	)

# Project overview: materials, glossary, and a clear start point.
elif not st.session_state.lesson_started:
	nav_left, nav_right = st.columns([1, 5])
	with nav_left:
		if st.button("← Back to projects", key="back_to_projects"):
			st.session_state.selected_project_id = None
			st.session_state.show_stuck = False
			st.session_state.pending_help_context = None
			st.rerun()
	with nav_right:
		st.markdown('<div class="brand">🧶 Crochetly</div>', unsafe_allow_html=True)

	st.write("")
	st.markdown(f'<div class="project-icon">{text(selected_project.get("emoji"), "🧶")}</div>', unsafe_allow_html=True)
	st.title(text(selected_project.get("title"), "Crochet project"))
	st.markdown(
		f'<p><span class="pill">{text(selected_project.get("difficulty"), "Beginner")}</span> &nbsp; {text(selected_project.get("estimated_time"), "Time varies")}</p>',
		unsafe_allow_html=True,
	)
	st.markdown(f'<p class="hero-copy">{text(project_description(selected_project))}</p>', unsafe_allow_html=True)

	st.write("")
	st.subheader("You'll need")
	materials = selected_project.get("materials") or []
	if materials:
		material_columns = st.columns(min(2, len(materials)), gap="medium")
		for index, material in enumerate(materials):
			with material_columns[index % len(material_columns)]:
				render_material_card(material, index)
	else:
		st.caption("No materials listed for this project yet.")

	st.write("")
	st.subheader("Stitch glossary")
	render_glossary(selected_project.get("stitch_glossary") or [])

	st.write("")
	if st.button("Start the lesson →", key="start_lesson", type="primary"):
		st.session_state.lesson_started = True
		st.session_state.show_stuck = False
		st.rerun()

# Lesson: one focused instruction at a time, ready for contextual help later.
else:
	project_id = selected_project.get("project_id")
	steps = [step for step in (selected_project.get("steps") or []) if isinstance(step, dict)]
	top_left, top_right = st.columns([1, 5])
	with top_left:
		if st.button("← Back to project", key="back_to_overview"):
			st.session_state.lesson_started = False
			st.session_state.show_stuck = False
			st.session_state.pending_help_context = None
			st.rerun()
	with top_right:
		st.markdown('<div class="brand">🧶 Crochetly</div>', unsafe_allow_html=True)

	if not steps:
		st.info("Lesson steps haven't been added for this project yet.")
	elif st.session_state.lesson_completed.get(project_id, False):
		st.write("")
		with st.container(border=True):
			st.markdown('<div class="completion-mark">🎉</div>', unsafe_allow_html=True)
			st.title("You finished!")
			st.markdown(f'<p class="completion-copy">You just completed: <strong>{text(selected_project.get("title"), "this project")}</strong></p>', unsafe_allow_html=True)
			st.markdown('<p class="completion-copy">Nice work. Your project is officially done.</p>', unsafe_allow_html=True)
		completion_back, review_column = st.columns([1, 1])
		with completion_back:
			if st.button("← Back to projects", key="completion_back_to_projects"):
				st.session_state.selected_project_id = None
				st.session_state.lesson_started = False
				st.session_state.show_stuck = False
				st.session_state.pending_help_context = None
				st.rerun()
		with review_column:
			if st.button("Review lesson", key=f"review_{project_id}"):
				st.session_state.lesson_completed[project_id] = False
				st.session_state.lesson_progress[project_id] = 0
				st.session_state.show_stuck = False
				st.session_state.pending_help_context = None
				st.rerun()
	else:
		saved_index = st.session_state.lesson_progress.get(project_id, 0)
		step_index = max(0, min(saved_index, len(steps) - 1))
		step = steps[step_index]
		st.write("")
		st.markdown(
			f'<div class="lesson-project-header"><div class="lesson-project-emoji">{text(selected_project.get("emoji"), "🧶")}</div>'
			f'<div class="lesson-project-title">{text(selected_project.get("title"), "Crochet project")}</div></div>',
			unsafe_allow_html=True,
		)
		render_progress(step_index, len(steps))
		st.markdown(f'<div class="lesson-step">STEP {step_index + 1:02d}</div>', unsafe_allow_html=True)
		st.title(text(step.get("name"), f"Step {step_index + 1}"))

		render_lesson_step(step)

		if st.session_state.show_stuck:
			with st.container(border=True):
				st.markdown("#### I'm Stuck")
				st.markdown("Tell Crochetly what went wrong and we'll help you figure it out.")
				question = st.text_area(
					"What went wrong?",
					placeholder="e.g. I only have 7 stitches instead of 10. What did I do wrong?",
					key=f"stuck_question_{project_id}_{step_index}",
				)
				if st.button("Get help", key=f"get_help_{project_id}_{step_index}"):
					if question.strip():
						st.session_state.pending_help_context = build_step_context(selected_project, step, question)
						st.rerun()
					st.warning("Add a little detail about what happened, and Crochetly can help you work it out.")
				pending_context = st.session_state.pending_help_context
				if pending_context and pending_context.get("user_question") == question.strip():
					st.info("Your question is ready. Step-aware help will be connected here next.")

		stuck_col, spacer_col, previous_col, next_col = st.columns([1.5, 2.4, 1, 1])
		with stuck_col:
			if st.button("💡 I'm Stuck", key=f"stuck_{project_id}_{step_index}"):
				st.session_state.show_stuck = not st.session_state.show_stuck
				st.rerun()
		with previous_col:
			if st.button("← Previous", key=f"previous_{project_id}_{step_index}", disabled=step_index == 0):
				st.session_state.lesson_progress[project_id] = step_index - 1
				st.session_state.show_stuck = False
				st.session_state.pending_help_context = None
				st.rerun()
		with next_col:
			if step_index < len(steps) - 1:
				if st.button("Next →", key=f"next_{project_id}_{step_index}", type="primary"):
					st.session_state.lesson_progress[project_id] = step_index + 1
					st.session_state.show_stuck = False
					st.session_state.pending_help_context = None
					st.rerun()
			else:
				if st.button("Finish project ✓", key=f"finish_{project_id}", type="primary"):
					st.session_state.lesson_completed[project_id] = True
					st.session_state.show_stuck = False
					st.session_state.pending_help_context = None
					st.rerun()
