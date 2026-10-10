
import streamlit as st

from matcher import (
    fetch_jobs,
    filter_jobs,
    extract_resume_text,
    build_resume_profile,
)

st.set_page_config(
    page_title="AI Career Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Modern colorful theme ----------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            135deg, #f5f3ff 0%, #f8fafc 55%, #eef6ff 100%
        );
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(
            120deg, #312e81, #6d28d9, #2563eb
        );
        padding: 32px;
        border-radius: 22px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px #4338ca25;
    }

    .hero h1 {
        color: white !important;
        font-size: 36px !important;
        margin-bottom: 8px;
    }

    .hero p {
        color: #ede9fe;
        font-size: 16px;
    }

    .section-title {
        color: #312e81;
        font-size: 23px;
        font-weight: 750;
        margin: 18px 0 12px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.96);
        border: 1px solid #e0e7ff;
        border-radius: 18px;
        box-shadow: 0 5px 18px #312e8110;
        padding: 12px;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(100deg, #6d28d9, #2563eb);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        min-height: 48px;
    }

    .stButton > button[kind="primary"]:hover {
        border: 1px solid #6d28d9;
        box-shadow: 0 5px 16px #6d28d933;
    }

    .stLinkButton a {
        background: linear-gradient(
            100deg, #6d28d9, #2563eb
        ) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 10px;
        border-color: #c7d2fe;
    }

    .job-title {
        color: #312e81;
        font-size: 21px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .company {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 12px;
    }

    .pill {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin: 3px 5px 7px 0;
    }

    .green {
        background: #dcfce7;
        color: #166534;
    }

    .yellow {
        background: #fef3c7;
        color: #92400e;
    }

    .red {
        background: #fee2e2;
        color: #991b1b;
    }

    .blue {
        background: #dbeafe;
        color: #1d4ed8;
    }

    .purple {
        background: #ede9fe;
        color: #5b21b6;
    }

    .metric {
        background: white;
        padding: 16px;
        border-radius: 15px;
        border: 1px solid #e0e7ff;
        text-align: center;
    }

    .metric-label {
        color: #64748b;
        font-size: 13px;
    }

    .metric-value {
        color: #4f46e5;
        font-size: 26px;
        font-weight: 800;
    }

    .footer {
        color: #64748b;
        text-align: center;
        padding: 25px 0 5px;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Hero ----------
st.markdown(
    """
    <div class="hero">
        <h1>🌍 AI Career Agent</h1>
        <p>
            Your gateway to international opportunities.
            Find jobs, compare them with your CV, check sponsorship
            evidence, and access employer information.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- CV Upload ----------
st.markdown(
    '<div class="section-title">📄 1. Your CV</div>',
    unsafe_allow_html=True,
)

resume_profile = None

with st.container(border=True):
    cv = st.file_uploader(
        "Upload your CV (PDF or DOCX)",
        type=["pdf", "docx"],
        help=(
            "The app extracts text from your CV for matching. "
            "Check your app configuration and privacy practices "
            "before uploading sensitive information."
        ),
        key="cv_uploader",
    )

    if cv is not None:
        try:
            with st.spinner("📄 Reading your CV..."):
                resume_text = extract_resume_text(cv)
                resume_profile = build_resume_profile(resume_text)

            st.session_state["resume_profile"] = resume_profile

            st.success(f"✓ CV read successfully: {cv.name}")

            skills = resume_profile.get("skills", [])

            if skills:
                st.markdown("**🧠 Skills detected**")
                st.write(" · ".join(skills))
            else:
                st.info(
                    "No recognised skills were detected. "
                    "You can still search by job title."
                )

            experience = resume_profile.get("experience", {})
            st.write(
                "**🎓 Experience:**",
                experience.get("label", "Not determined"),
            )

            with st.expander("Preview extracted CV text"):
                st.text(resume_text[:5000])

        except Exception as error:
            resume_profile = None
            st.session_state.pop("resume_profile", None)
            st.error(f"Could not read this CV: {error}")

    else:
        st.session_state.pop("resume_profile", None)
        st.caption(
            "Upload your CV to personalise job matching, "
            "or search without a CV."
        )

# ---------- Job Search Form ----------
st.markdown(
    '<div class="section-title">'
    '🔎 2. Find your next opportunity</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        position = st.text_input(
            "Job position",
            value="Data Analyst",
            placeholder="e.g. Junior Data Analyst",
        )

        country = st.selectbox(
            "🌎 Target country",
            [
                "Germany",
                "Ireland",
                "Japan",
                "United Kingdom",
                "United States",
                "Netherlands",
                "Canada",
                "Australia",
                "Singapore",
                "India",
            ],
        )

    with col2:
        job_type = st.selectbox(
            "💼 Work arrangement",
            ["Any", "Remote", "Hybrid", "On-site"],
        )

        visa_filter = st.selectbox(
            "🛂 Visa sponsorship",
            [
                "Any",
                "Sponsorship explicitly mentioned",
                "Sponsorship unclear",
                "No sponsorship / existing work permit",
            ],
        )

    experience_filter = st.selectbox(
        "🎓 Experience level",
        ["Any", "Entry-level / 0-2 years"],
    )

    search_clicked = st.button(
        "🔍 FIND JOBS",
        type="primary",
        use_container_width=True,
    )

# ---------- Search ----------
if search_clicked:
    if not position.strip():
        st.warning("Please enter a job position.")
    else:
        try:
            with st.spinner(
                "🌐 Searching job boards for opportunities..."
            ):
                jobs, errors = fetch_jobs(
                    position=position.strip(),
                    country=country,
                    include_remote=(job_type != "On-site"),
                )

                results = filter_jobs(
                    jobs=jobs,
                    job_type=job_type,
                    visa_filter=visa_filter,
                    experience_filter=experience_filter,
                    resume_profile=resume_profile,
                )

            st.session_state["job_results"] = results
            st.session_state["job_errors"] = errors
            st.session_state["search_country"] = country
            st.session_state["search_position"] = position.strip()

        except Exception as error:
            st.error(f"Job search failed: {error}")

            st.session_state["job_results"] = []
            st.session_state["job_errors"] = [str(error)]
            st.session_state["search_country"] = country
            st.session_state["search_position"] = position.strip()

# ---------- Results ----------
if "job_results" in st.session_state:
    results = st.session_state["job_results"]
    errors = st.session_state.get("job_errors", [])

    search_country = st.session_state.get(
        "search_country", country
    )
    search_position = st.session_state.get(
        "search_position", position
    )

    st.markdown("---")

    st.markdown(
        f'<div class="section-title">✨ Job opportunities for '
        f'{search_position} · {search_country}</div>',
        unsafe_allow_html=True,
    )

    # Summary metrics
    a, b, c = st.columns(3)

    sponsorship_count = sum(
        job.get("visa") == "Sponsorship explicitly mentioned"
        for job in results
    )

    remote_count = sum(
        bool(job.get("remote", False))
        for job in results
    )

    metrics = [
        (a, "LISTINGS FOUND", len(results)),
        (b, "SPONSORSHIP MENTIONED", sponsorship_count),
        (c, "REMOTE LISTINGS", remote_count),
    ]

    for col, label, value in metrics:
        with col:
            st.markdown(
                f'<div class="metric">'
                f'<div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.write("")

    if errors:
        with st.expander("⚠️ Search source warnings"):
            for error in errors:
                st.write(error)

    if not results:
        st.info(
            "No matching listings found. Try the sponsorship "
            "filter set to Any, or change the job title or country."
        )

    # ---------- Individual Job Cards ----------
    for i, job in enumerate(results, start=1):
        with st.container(border=True):
            left, right = st.columns([5, 1])

            with left:
                title = job.get("title", "Untitled position")
                company = job.get("company", "Company not listed")
                location = job.get("location", "Location not listed")

                st.markdown(
                    f'<div class="job-title">{title}</div>'
                    f'<div class="company">🏢 {company}'
                    f' &nbsp; · &nbsp; 📍 {location}</div>',
                    unsafe_allow_html=True,
                )

            with right:
                st.markdown(
                    f'<span class="pill purple">JOB #{i}</span>',
                    unsafe_allow_html=True,
                )

            # Sponsorship badge
            visa = job.get("visa", "Unclear - confirm with employer")

            if visa == "Sponsorship explicitly mentioned":
                visa_class = "green"
                visa_label = "✓ Sponsorship mentioned"
            elif visa in (
                "Unclear - confirm with employer",
                "Sponsorship unclear",
            ):
                visa_class = "yellow"
                visa_label = "? Sponsorship unclear"
            else:
                visa_class = "red"
                visa_label = "! Check work permit requirements"

            remote_label = (
                "🌐 Remote"
                if job.get("remote", False)
                else "🏢 On-site / unspecified"
            )

            st.markdown(
                f'<span class="pill {visa_class}">{visa_label}</span>'
                f'<span class="pill blue">{remote_label}</span>'
                f'<span class="pill purple">💼 '
                f'{job.get("experience", "Not specified")}</span>',
                unsafe_allow_html=True,
            )

            # Salary and source
            d1, d2 = st.columns(2)

            with d1:
                st.write(
                    f"**Salary:** {job.get('salary', 'Not disclosed')}"
                )

            with d2:
                st.write(
                    f"**Source:** {job.get('source', 'Not specified')}"
                )

            # Personalised CV-to-job match
            profile_match = job.get("profile_match")

            if profile_match:
                st.markdown("**🎯 Your CV match**")

                match_score = profile_match.get("match_score", 0)
                match_score = max(0, min(100, int(match_score)))

                st.progress(
                    match_score / 100,
                    text=f"{match_score}% keyword overlap",
                )

                matched_skills = profile_match.get(
                    "matched_skills", []
                )
                missing_skills = profile_match.get(
                    "missing_skills", []
                )

                if matched_skills:
                    st.write(
                        "**Matching skills:**",
                        ", ".join(matched_skills),
                    )

                if missing_skills:
                    st.write(
                        "**Skills to review:**",
                        ", ".join(missing_skills),
                    )

                if profile_match.get("seniority_warning"):
                    st.warning(
                        profile_match["seniority_warning"]
                    )

                st.caption(
                    profile_match.get(
                        "score_note",
                        "This is a keyword-based estimate, "
                        "not a guarantee of job suitability.",
                    )
                )

            elif resume_profile:
                st.caption(
                    "A CV match score was not provided for this listing."
                )

            # Sponsorship evidence
            visa_details = job.get("visa_details", {})

            with st.expander(
                "🛂 Sponsorship evidence and verification"
            ):
                st.write("**Classification:**", visa)

                st.write(
                    visa_details.get(
                        "verification",
                        "Unverified — confirm sponsorship directly "
                        "with the employer.",
                    )
                )

                st.write(
                    visa_details.get(
                        "evidence",
                        "No clear sponsorship statement detected.",
                    )
                )

            # Company website
            company_url = job.get("company_url")

            if company_url:
                st.markdown(
                    f"🌐 [Company website]({company_url})"
                )

            # Job description
            with st.expander("📋 View job description"):
                description = job.get("description", "")

                if description:
                    st.write(description[:5000])
                else:
                    st.caption(
                        "Description not provided by the source."
                    )

            # Public contact details
            contact = job.get("contact", {})

            with st.expander("📧 Company contact details"):
                emails = contact.get("emails", [])
                phones = contact.get("phones", [])

                if emails:
                    for email in emails:
                        st.markdown(f"- [{email}](mailto:{email})")

                if phones:
                    for phone in phones:
                        st.write(f"📞 {phone}")

                if not emails and not phones:
                    st.info(
                        "No public contact details were found in "
                        "this listing. Check the official company "
                        "website or careers page."
                    )

            # Application link
            job_url = job.get("url")

            if job_url:
                st.link_button(
                    "🚀 VIEW JOB / APPLY",
                    job_url,
                    use_container_width=True,
                )
            else:
                st.warning(
                    "No application URL was supplied by the source."
                )

# ---------- Footer ----------
st.markdown(
    """
    <div class="footer">
        AI Career Agent · Verify job details and visa requirements
        directly with the employer before applying.
    </div>
    """,
    unsafe_allow_html=True,
)
