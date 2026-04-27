"""
iNHCES — Beginner Deployment Step-by-Step Guide PDF Generator
Produces O6_15_Step_By_Step_Deployment.pdf

A plain-English, step-by-step guide for deploying iNHCES from a local machine
to GitHub, Supabase, Cloudflare R2, Railway (backend), and Vercel (frontend).
Written for someone who has accounts on all five platforms but has never deployed
a project before.

DATA SOURCE: AMBER — AI-authored guide. Verify button/menu names against current
platform UIs before following.

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "01_literature_review"))

from generate_o1_pdfs import (
    DocPDF, sanitize,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE,
    DARK_GREY, MID_GREY, CODE_BG,
    PAGE_W, LEFT, LINE_H,
)
from datetime import date

OUTPUT_DIR = os.path.join(_ROOT, "nhces-backend")

# Extra colours
STEP_GREEN  = (220, 245, 225)
STEP_AMBER  = (255, 248, 210)
WARN_RED    = (255, 230, 230)
TIP_BLUE    = (225, 240, 255)
PHASE_GOLD  = (255, 245, 195)


class GuidePDF(DocPDF):
    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, "F")
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(PAGE_W, 6, sanitize(
            "iNHCES | TETFund NRF 2025 | ABU Zaria  |  Beginner Deployment Guide"
        ))
        self.set_text_color(*DARK_GREY)
        self.ln(16)

    def footer(self):
        self.set_y(-13)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.4)
        self.line(LEFT, self.get_y(), 198, self.get_y())
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*MID_GREY)
        self.cell(0, 8, sanitize(
            f"O6_15 Beginner Deployment Guide  |  iNHCES TETFund NRF 2025  |  Page {self.page_no()}"
        ), align="C")

    def phase_banner(self, number, title, subtitle=""):
        """Big coloured phase header — Phase 1, Phase 2, etc."""
        self.ln(3)
        self.set_fill_color(*DARK_NAVY)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.set_x(LEFT)
        self.rect(LEFT, self.get_y(), PAGE_W, 11, "F")
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*GOLD)
        self.set_xy(LEFT + 3, self.get_y() + 1.5)
        self.cell(20, 8, sanitize(f"PHASE {number}"), ln=False)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*WHITE)
        self.cell(PAGE_W - 20, 8, sanitize(title), ln=True)
        if subtitle:
            self.set_x(LEFT)
            self.set_fill_color(*PHASE_GOLD)
            self.set_font("Helvetica", "I", 8.5)
            self.set_text_color(*DARK_NAVY)
            self.cell(PAGE_W, 6, sanitize(f"   {subtitle}"), fill=True, ln=True)
        self.set_text_color(*DARK_GREY)
        self.ln(2)

    def step_box(self, number, title, body_lines, cmd=None, tip=None, warning=None):
        """
        Numbered step with optional command block, tip, and warning.
        body_lines: list of strings (bullet points) or single string
        """
        # Step header
        self.ln(2)
        self.set_fill_color(*STEP_GREEN)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        self.set_x(LEFT)
        y0 = self.get_y()
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*DARK_NAVY)
        self.cell(10, 7, sanitize(f"{number}."), border="LTB", fill=True, align="C")
        self.cell(PAGE_W - 10, 7, sanitize(f"  {title}"), border="RTB", fill=True, ln=True)

        # Body
        if isinstance(body_lines, str):
            body_lines = [body_lines]
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*DARK_GREY)
        for line in body_lines:
            self.set_x(LEFT + 4)
            # Use bullet dash
            self.set_font("Helvetica", "", 8.5)
            self.cell(4, 5.5, "-", ln=False)
            self.set_x(LEFT + 8)
            self.multi_cell(PAGE_W - 8, 5.5, sanitize(line))

        # Command block
        if cmd:
            self.set_fill_color(*CODE_BG)
            self.set_draw_color(*MID_GREY)
            self.set_line_width(0.2)
            self.set_x(LEFT + 4)
            self.set_font("Courier", "", 8)
            self.set_text_color(*DARK_NAVY)
            self.multi_cell(PAGE_W - 4, 4.5, sanitize(cmd), border=1, fill=True)

        # Tip
        if tip:
            self.set_fill_color(*TIP_BLUE)
            self.set_draw_color(*GOLD)
            self.set_line_width(0.25)
            self.set_x(LEFT + 4)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*DARK_NAVY)
            self.multi_cell(PAGE_W - 4, 5, sanitize(f"TIP: {tip}"), border=1, fill=True)

        # Warning
        if warning:
            self.set_fill_color(*WARN_RED)
            self.set_draw_color(200, 80, 80)
            self.set_line_width(0.25)
            self.set_x(LEFT + 4)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(160, 30, 30)
            self.multi_cell(PAGE_W - 4, 5, sanitize(f"WARNING: {warning}"), border=1, fill=True)

        self.set_text_color(*DARK_GREY)
        self.ln(1)

    def section_note(self, text):
        self.ln(1)
        self.set_fill_color(*STEP_AMBER)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        self.set_x(LEFT)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(PAGE_W, 5.2, sanitize(text), border=1, fill=True)
        self.ln(2)

    def checklist_row(self, text, done=False):
        box = "[x]" if done else "[ ]"
        self.set_x(LEFT)
        self.set_font("Courier", "B", 8.5)
        self.set_text_color(*DARK_NAVY if done else MID_GREY)
        self.cell(10, 6, box, ln=False)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(PAGE_W - 10, 6, sanitize(text))


def generate():
    pdf = GuidePDF(
        doc_name="O6_15 Beginner Deployment Guide",
        doc_subtitle="Step-by-Step: GitHub → Supabase → R2 → Railway → Vercel",
    )

    # ── Cover ──────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 65, "F")
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 10, sanitize("iNHCES — Deploy It Yourself"), align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(210, 7, sanitize("A Beginner's Step-by-Step Deployment Guide"), align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.cell(210, 6, sanitize("From your laptop to the live internet in 6 phases"), align="C", ln=True)
    pdf.cell(210, 5, sanitize("GitHub  ->  Supabase  ->  Cloudflare R2  ->  Railway  ->  Vercel"), align="C", ln=True)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(30, 88, 180, 88)
    pdf.set_xy(LEFT, 95)
    pdf.set_text_color(*DARK_GREY)
    meta = [
        ("Project:",      "iNHCES -- Intelligent National Housing Cost Estimating System"),
        ("Grant:",        "TETFund NRF 2025 | Dept. of Quantity Surveying, ABU Zaria"),
        ("Accounts needed:", "GitHub, Supabase, Cloudflare, Railway, Vercel (all free tiers)"),
        ("Time needed:",  "Approximately 60-90 minutes for first deployment"),
        ("Date:",         date.today().strftime("%d %B %Y")),
        ("Data Source:",  "AMBER - AI-authored guide; UI details may change slightly"),
    ]
    for label, val in meta:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(44, 6.5, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 44, 6.5, sanitize(val), ln=True)

    # ── Page 2: Overview + checklist ──────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Before You Begin — What You Need")
    pdf.body(
        "You will follow 6 phases in order. Each phase builds on the previous one. "
        "Do NOT skip a phase. The whole process takes about 60-90 minutes the first time."
    )

    pdf.sub_heading("Accounts (you already have these)")
    accounts = [
        ("GitHub",     "github.com",         "Stores your code; triggers automatic deploys"),
        ("Supabase",   "supabase.com",        "Your PostgreSQL database + user authentication"),
        ("Cloudflare", "dash.cloudflare.com", "R2 object storage for ML models and PDF reports"),
        ("Railway",    "railway.app",         "Runs your Python backend (FastAPI) as a web server"),
        ("Vercel",     "vercel.com",          "Hosts your Next.js frontend website"),
    ]
    pdf.set_fill_color(*DARK_NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_x(LEFT)
    for h, w in [("Platform", 28), ("Website", 50), ("What it does", PAGE_W - 78)]:
        pdf.cell(w, LINE_H + 1, h, border=1, fill=True, align="C")
    pdf.ln()
    for plat, site, desc in accounts:
        pdf.set_fill_color(*LIGHT_BLUE)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(28, LINE_H, sanitize(plat), border=1, fill=True)
        pdf.set_font("Courier", "", 7.5)
        pdf.cell(50, LINE_H, sanitize(site), border=1, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 78, LINE_H, sanitize(desc), border=1, fill=True, ln=True)
    pdf.ln(3)

    pdf.sub_heading("Software to install on your laptop first")
    pdf.step_box("A", "Install Git (version control)",
        ["Go to git-scm.com/downloads and download Git for Windows",
         "Run the installer, click Next through all options, then Finish",
         "Open PowerShell and type: git --version  (you should see a version number)"],
        tip="If you see 'git is not recognized', restart PowerShell and try again.")

    pdf.step_box("B", "Install Node.js (for Vercel CLI + frontend)",
        ["Go to nodejs.org and download the LTS version (green button)",
         "Run the installer, click Next through all options",
         "Open PowerShell and type: node --version  (should see v20.x.x or higher)"],
        tip="Node is needed to run the Vercel CLI deploy command.")

    pdf.section_note(
        "PHASE OVERVIEW:\n"
        "Phase 1 -- Push code to GitHub     (5 min)\n"
        "Phase 2 -- Set up Supabase database  (15 min)\n"
        "Phase 3 -- Set up Cloudflare R2      (10 min)\n"
        "Phase 4 -- Deploy backend to Railway (15 min)\n"
        "Phase 5 -- Deploy frontend to Vercel (10 min)\n"
        "Phase 6 -- Set up GitHub Actions auto-deploy (10 min)\n"
        "Final    -- Test everything is working"
    )

    # ── PHASE 1: GitHub ────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.phase_banner(1, "Push Your Code to GitHub",
                     "Create a repository and upload the iNHCES project")

    pdf.step_box("1", "Create a new repository on GitHub",
        ["Open your browser and go to github.com — make sure you are logged in",
         "Click the green 'New' button (top left, next to 'Repositories')",
         "Repository name: type   iNHCES",
         "Set it to Private (this keeps your code secure)",
         "Do NOT tick 'Add a README' or 'Add .gitignore' — leave them blank",
         "Click the green 'Create repository' button"],
        tip="Private repos are free on GitHub. Your Supabase keys will be in environment variables, not in the code — but private is still safer.")

    pdf.step_box("2", "Open PowerShell in the project folder",
        ["In Windows Explorer, navigate to your project folder:",
         "C:\\Users\\MacBook\\Desktop\\BaeSoftIA\\INHCES\\iNHCES",
         "Right-click inside the folder -> 'Open in Terminal' (or 'Open PowerShell window here')",
         "You should see the folder path in the terminal prompt"])

    pdf.step_box("3", "Set up Git and make the first commit",
        ["Type these commands one at a time, pressing Enter after each one:"],
        cmd=(
            "git init\n"
            "git add .\n"
            "git commit -m \"Initial commit: iNHCES full build O6-S14\""
        ),
        tip="The 'git add .' command stages all files. The commit saves a snapshot.")

    pdf.step_box("4", "Connect to your GitHub repository and push",
        ["Replace YOUR_GITHUB_USERNAME with your actual GitHub username",
         "Copy and run these three commands:"],
        cmd=(
            "git branch -M main\n"
            "git remote add origin https://github.com/YOUR_GITHUB_USERNAME/iNHCES.git\n"
            "git push -u origin main"
        ),
        tip="Git will ask for your GitHub username and password. For password, use a Personal Access Token (PAT) from GitHub -> Settings -> Developer Settings -> Personal access tokens.")

    pdf.step_box("5", "Verify the push worked",
        ["Go back to github.com/YOUR_GITHUB_USERNAME/iNHCES in your browser",
         "You should see all your project files listed there",
         "If you see the files -- Phase 1 is complete!"],
        warning="If you see an error about authentication, you need a GitHub Personal Access Token (PAT). Go to github.com -> Click your profile photo -> Settings -> Developer settings -> Personal access tokens -> Tokens (classic) -> Generate new token. Give it 'repo' scope. Use this token as your password.")

    # ── PHASE 2: Supabase ──────────────────────────────────────────────────────
    pdf.add_page()
    pdf.phase_banner(2, "Set Up Your Supabase Database",
                     "Create the database tables, security rules, and seed data")

    pdf.step_box("1", "Create a new Supabase project",
        ["Go to supabase.com and log in",
         "Click 'New Project'",
         "Organisation: select your personal organisation",
         "Name: iNHCES",
         "Database Password: choose a STRONG password and SAVE IT somewhere safe",
         "Region: choose the closest to Nigeria (eu-west-2 London or af-south-1 Cape Town)",
         "Click 'Create new project' and wait 2-3 minutes for it to be ready"],
        warning="Save the database password now -- you cannot recover it later.")

    pdf.step_box("2", "Find your Supabase credentials (you will need these later)",
        ["In your Supabase project, click 'Project Settings' (gear icon in left sidebar)",
         "Click 'API' in the settings menu",
         "Write down (or copy to a text file) these three values:",
         "  -> Project URL  (looks like: https://abcdefgh.supabase.co)",
         "  -> anon public key  (a very long string starting with 'eyJ...')",
         "  -> service_role key  (another very long string -- KEEP THIS SECRET)",
         "Also click 'JWT Settings' and copy the JWT Secret"],
        warning="NEVER share the service_role key or put it in the frontend. It gives full database access.")

    pdf.step_box("3", "Run the database schema (create all tables)",
        ["In your Supabase project, click 'SQL Editor' in the left sidebar",
         "Click 'New query'",
         "Open the file 04_conceptual_models/04_schema.sql in VS Code",
         "Select ALL the text (Ctrl+A), copy it (Ctrl+C)",
         "Paste it into the Supabase SQL Editor (Ctrl+V)",
         "Click the green 'Run' button",
         "You should see 'Success. No rows returned'"])

    pdf.step_box("4", "Apply Row-Level Security (RLS) policies",
        ["Still in the SQL Editor, click 'New query' again",
         "Open 04_conceptual_models/04_rls_policies.sql in VS Code",
         "Copy all content and paste into the SQL Editor",
         "Click 'Run'"],
        tip="RLS ensures each user can only see their own projects and reports.")

    pdf.step_box("5", "Create database functions and indexes",
        ["Repeat the same process for these two files (run each separately):",
         "  -> 04_conceptual_models/04_db_functions.sql",
         "  -> 04_conceptual_models/04_db_indexes.sql",
         "Click 'New query', paste, click 'Run' for each one"])

    pdf.step_box("6", "Add seed data (optional test data)",
        ["Open 04_conceptual_models/04_seed_data.sql in VS Code",
         "Copy and paste into SQL Editor, click 'Run'",
         "This adds 3 test users and some sample macro data"],
        warning="Remove this seed data before any real research use -- it contains synthetic RED-banner data.")

    pdf.step_box("7", "Verify the tables were created",
        ["In the Supabase left sidebar, click 'Table Editor'",
         "You should see tables like: users, projects, predictions, reports, macro_fx, etc.",
         "If you see about 16 tables -- Phase 2 is complete!"])

    # ── PHASE 3: Cloudflare R2 ─────────────────────────────────────────────────
    pdf.add_page()
    pdf.phase_banner(3, "Set Up Cloudflare R2 Storage",
                     "Create a storage bucket for ML models and PDF reports")

    pdf.step_box("1", "Enable R2 on your Cloudflare account",
        ["Go to dash.cloudflare.com and log in",
         "In the left sidebar, click 'R2 Object Storage'",
         "If you see a message about enabling R2, click 'Purchase R2' (it is free up to 10GB/month)",
         "You may need to add a payment method even for the free tier -- add a card"])

    pdf.step_box("2", "Create a storage bucket",
        ["In the R2 dashboard, click 'Create bucket'",
         "Bucket name: nhces-storage  (EXACTLY this name -- lowercase, hyphens only)",
         "Location: Automatic",
         "Click 'Create bucket'"],
        tip="The bucket name 'nhces-storage' is hardcoded in the backend config. Use exactly this name.")

    pdf.step_box("3", "Create R2 API keys (Access Keys)",
        ["In the R2 dashboard, look for 'Manage R2 API Tokens' (right side of the page)",
         "Click 'Create API token'",
         "Token name: iNHCES Backend",
         "Permissions: Object Read & Write",
         "Specify bucket: nhces-storage",
         "Click 'Create API Token'",
         "COPY BOTH values immediately and save them to a text file:",
         "  -> Access Key ID  (looks like: abc123...)",
         "  -> Secret Access Key  (only shown ONCE -- copy it now!)"],
        warning="The Secret Access Key is shown ONLY ONCE. If you close the page without copying it, you must create a new token.")

    pdf.step_box("4", "Find your R2 endpoint URL",
        ["On the R2 dashboard main page, you will see your Account ID (32 characters)",
         "Your R2 endpoint URL is: https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com",
         "Replace YOUR_ACCOUNT_ID with your actual Cloudflare Account ID",
         "Save this URL -- you will need it for Railway"])

    pdf.step_box("5", "Upload the ML champion model to R2",
        ["The champion model file is in your project at:",
         "05_ml_models/models/champion_model.pkl",
         "If this file exists: In the R2 dashboard, open the nhces-storage bucket",
         "Click 'Upload', then 'Upload files'",
         "Create a folder called 'models' first (click 'Create folder')",
         "Upload champion_model.pkl into the models/ folder",
         "The file should appear as: models/champion_model.pkl"],
        tip="If champion_model.pkl does not exist yet, the backend will load a synthetic fallback model on startup -- that is fine for initial testing.")

    # ── PHASE 4: Railway (Backend) ─────────────────────────────────────────────
    pdf.add_page()
    pdf.phase_banner(4, "Deploy the Backend to Railway",
                     "Deploy the FastAPI Python server -- this is the brain of iNHCES")

    pdf.step_box("1", "Create a new Railway project",
        ["Go to railway.app and log in",
         "Click 'New Project'",
         "Click 'Deploy from GitHub repo'",
         "Connect your GitHub account if not already done (click 'Configure GitHub App')",
         "Select your iNHCES repository from the list",
         "Click 'Deploy Now'"],
        tip="Railway will automatically detect the Dockerfile in nhces-backend/ and start building.")

    pdf.step_box("2", "Set the source directory",
        ["Railway may build from the repo root by default. You need to tell it to use nhces-backend/",
         "In your Railway service, click 'Settings'",
         "Find 'Root Directory' and type:  nhces-backend",
         "Railway will re-deploy automatically"])

    pdf.step_box("3", "Add the environment variables (this is the most important step)",
        ["In your Railway service, click 'Variables'",
         "Click 'New Variable' for each one below. Copy the values from your saved text file:",
         "   SUPABASE_URL             = https://YOUR_PROJECT_REF.supabase.co",
         "   SUPABASE_ANON_KEY        = (your anon/public key)",
         "   SUPABASE_SERVICE_KEY     = (your service_role key -- KEEP SECRET)",
         "   SUPABASE_JWT_SECRET      = (your JWT secret from Supabase Auth settings)",
         "   CLOUDFLARE_R2_ENDPOINT   = https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com",
         "   CLOUDFLARE_R2_ACCESS_KEY = (your R2 access key ID)",
         "   CLOUDFLARE_R2_SECRET_KEY = (your R2 secret access key)",
         "   CLOUDFLARE_R2_BUCKET     = nhces-storage",
         "   SECRET_KEY               = (type any long random string -- 40+ characters)",
         "   ENVIRONMENT              = production",
         "   ALLOWED_ORIGINS          = https://YOUR_VERCEL_URL.vercel.app"],
        warning="Do not add quotes around the values. Just paste the value directly into the field.")

    pdf.step_box("4", "Wait for the deployment to finish",
        ["Click 'Deployments' tab in your Railway service",
         "Watch the build logs -- you will see Docker building the image",
         "This takes 3-5 minutes the first time",
         "When you see 'Deployment is live' -- the backend is running!"])

    pdf.step_box("5", "Get your Railway backend URL",
        ["Click 'Settings' in your Railway service",
         "Under 'Networking', click 'Generate Domain'",
         "Railway gives you a URL like: nhces-backend-production.up.railway.app",
         "SAVE THIS URL -- you need it for the frontend and for testing"])

    pdf.step_box("6", "Test that the backend is working",
        ["Open your browser and visit:   YOUR_RAILWAY_URL/health",
         "Example: https://nhces-backend-production.up.railway.app/health",
         "You should see a page with:  {\"status\": \"ok\", \"db\": ...}",
         "Also try:  YOUR_RAILWAY_URL/docs  -- you should see the API documentation page"],
        tip="If you see an error, click 'Deployments' -> click on the latest deployment -> 'View Logs' to see what went wrong.")

    # ── PHASE 5: Vercel (Frontend) ─────────────────────────────────────────────
    pdf.add_page()
    pdf.phase_banner(5, "Deploy the Frontend to Vercel",
                     "Put the Next.js website on the internet")

    pdf.step_box("1", "Import your GitHub repo to Vercel",
        ["Go to vercel.com and log in",
         "Click 'Add New...' -> 'Project'",
         "Click 'Import' next to your iNHCES repository",
         "If you don't see your repo, click 'Adjust GitHub App Permissions'"])

    pdf.step_box("2", "Configure the Vercel project settings",
        ["Before clicking Deploy, configure these settings:",
         "Framework Preset: Next.js  (Vercel usually detects this automatically)",
         "Root Directory: nhces-frontend  (IMPORTANT -- click 'Edit' to change this)",
         "Build Command: npm run build  (leave as default)",
         "Output Directory: .next  (leave as default)"])

    pdf.step_box("3", "Add the environment variables",
        ["Scroll down to find 'Environment Variables' on the configuration page",
         "Add these three variables:",
         "   NEXT_PUBLIC_SUPABASE_URL       = https://YOUR_PROJECT_REF.supabase.co",
         "   NEXT_PUBLIC_SUPABASE_ANON_KEY  = (your Supabase anon/public key)",
         "   NEXT_PUBLIC_API_URL            = https://YOUR_RAILWAY_URL.up.railway.app",
         "For each: type the name in the 'Key' box, paste the value, click 'Add'"],
        warning="Only use the ANON key here, NEVER the service_role key. The frontend is public.")

    pdf.step_box("4", "Update the API rewrite URL in vercel.json",
        ["Open nhces-frontend/vercel.json in VS Code",
         "Find the line that says: 'destination': 'https://nhces-api.up.railway.app/:path*'",
         "Replace nhces-api.up.railway.app with YOUR actual Railway URL",
         "Save the file, then commit and push the change to GitHub:"],
        cmd=(
            "git add nhces-frontend/vercel.json\n"
            "git commit -m \"Update Railway backend URL in vercel.json\"\n"
            "git push"
        ))

    pdf.step_box("5", "Deploy to Vercel",
        ["Go back to Vercel and click the 'Deploy' button",
         "Watch the build log -- it should take 2-3 minutes",
         "When you see 'Congratulations!' -- your frontend is live!",
         "Vercel gives you a URL like: nhces-frontend.vercel.app"])

    pdf.step_box("6", "Update Railway ALLOWED_ORIGINS with your Vercel URL",
        ["Go back to Railway -> Variables",
         "Update ALLOWED_ORIGINS to your actual Vercel URL:",
         "   ALLOWED_ORIGINS = https://nhces-frontend.vercel.app",
         "Railway will automatically redeploy"])

    pdf.step_box("7", "Test the full website",
        ["Visit your Vercel URL in a browser (e.g. https://nhces-frontend.vercel.app)",
         "You should see the iNHCES landing page",
         "Click 'Get Estimate' and fill in the form -- you should get a cost estimate back",
         "If the estimate works -- Phase 5 is complete!"],
        tip="If the estimate fails, open browser Developer Tools (F12) -> Console to see error messages. Usually it means the Railway URL in vercel.json needs updating.")

    # ── PHASE 6: GitHub Actions ────────────────────────────────────────────────
    pdf.add_page()
    pdf.phase_banner(6, "Set Up Automatic Deploys (GitHub Actions)",
                     "After this, every push to GitHub automatically deploys to Railway + Vercel")

    pdf.body(
        "GitHub Actions is already configured in .github/workflows/deploy.yml. "
        "You just need to add 5 secret values to your GitHub repository. "
        "After that, every time you push code to GitHub, it will:"
    )
    pdf.bullet([
        "Run all 73 tests (if any test fails, the deploy is cancelled)",
        "Build the Next.js frontend",
        "Deploy the backend to Railway",
        "Deploy the frontend to Vercel",
    ])
    pdf.ln(2)

    pdf.step_box("1", "Get your Railway API token",
        ["Go to railway.app -> click your profile photo (top right) -> 'Account Settings'",
         "Click 'Tokens' in the left menu",
         "Click 'New Token'",
         "Name: iNHCES GitHub Actions",
         "Click 'Create'",
         "COPY the token value immediately -- save it to your text file"])

    pdf.step_box("2", "Get your Railway Service ID",
        ["In Railway, open your iNHCES project",
         "Click on your backend service (nhces-backend)",
         "Click 'Settings'",
         "Look for 'Service ID' -- it looks like a long code (e.g. abc123de-...)",
         "Copy and save it"])

    pdf.step_box("3", "Get your Vercel tokens and IDs",
        ["Go to vercel.com -> click your profile photo -> 'Settings'",
         "Click 'Tokens' -> 'Create'",
         "Name: iNHCES GitHub Actions, Scope: Full Account -> Create",
         "Copy the token value",
         "",
         "To get your Vercel Org ID and Project ID, run this in PowerShell from nhces-frontend/:"],
        cmd=(
            "cd nhces-frontend\n"
            "npx vercel link\n"
            "# After linking, check the file: nhces-frontend/.vercel/project.json\n"
            "# It contains orgId and projectId"
        ))

    pdf.step_box("4", "Add the 5 secrets to GitHub",
        ["Go to github.com/YOUR_USERNAME/iNHCES",
         "Click 'Settings' tab (at the top of the repo page)",
         "In the left sidebar: 'Secrets and variables' -> 'Actions'",
         "Click 'New repository secret' for each one:",
         "   RAILWAY_TOKEN      = (your Railway API token)",
         "   RAILWAY_SERVICE_ID = (your Railway service ID)",
         "   VERCEL_TOKEN       = (your Vercel token)",
         "   VERCEL_ORG_ID      = (orgId from .vercel/project.json)",
         "   VERCEL_PROJECT_ID  = (projectId from .vercel/project.json)"],
        tip="The secret values are never visible again after you save them -- make sure they are correct before saving.")

    pdf.step_box("5", "Test the automatic deploy pipeline",
        ["Make a small change to any file (e.g. add a space to a comment)",
         "Commit and push to GitHub:"],
        cmd=(
            "git add .\n"
            "git commit -m \"Test GitHub Actions auto-deploy\"\n"
            "git push"
        ))

    pdf.step_box("6", "Watch the pipeline run",
        ["Go to github.com/YOUR_USERNAME/iNHCES",
         "Click the 'Actions' tab",
         "You should see a workflow run called 'iNHCES CI/CD' starting",
         "Click on it to watch it run in real time",
         "All 4 jobs should show green checkmarks after 5-10 minutes",
         "If any job fails, click on it to see the error logs"])

    # ── Final: Test Everything ─────────────────────────────────────────────────
    pdf.add_page()
    pdf.phase_banner("", "Final Check — Test Everything is Working",
                     "Run through this checklist after completing all 6 phases")

    pdf.sub_heading("Final Deployment Checklist")
    checks = [
        ("GitHub",    "Repository is visible at github.com/YOUR_USERNAME/iNHCES"),
        ("GitHub",    "All files are in the repo (not just some)"),
        ("Supabase",  "16 tables visible in Supabase Table Editor"),
        ("Supabase",  "RLS policies show 'RLS Enabled' on each table"),
        ("R2",        "nhces-storage bucket exists in Cloudflare R2"),
        ("R2",        "models/champion_model.pkl uploaded to the bucket"),
        ("Railway",   "Backend /health returns {status: ok}"),
        ("Railway",   "Backend /docs shows the Swagger API documentation page"),
        ("Railway",   "Backend /macro returns macroeconomic variables list"),
        ("Vercel",    "Frontend landing page loads at your Vercel URL"),
        ("Vercel",    "Estimate form submits and returns a cost estimate"),
        ("Vercel",    "No CORS errors in the browser Console (F12)"),
        ("Actions",   "GitHub Actions workflow shows all green checkmarks"),
        ("Actions",   "A new push to GitHub triggers a new automated deploy"),
    ]
    for area, check in checks:
        pdf.set_x(LEFT)
        pdf.set_fill_color(*STEP_AMBER)
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.2)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(22, LINE_H, area, border=1, fill=True, align="C")
        pdf.set_fill_color(252, 252, 252)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(12, LINE_H, "[ ]", border=1, fill=True, align="C")
        pdf.cell(PAGE_W - 34, LINE_H, sanitize(check), border=1, fill=True, ln=True)
    pdf.ln(3)

    pdf.sub_heading("Common Problems and Solutions")
    problems = [
        ("Backend not starting",
         "Check Railway Deploy Logs. Most common cause: a required environment variable is missing. "
         "Make sure all 11 variables in Phase 4 Step 3 are set in Railway."),
        ("CORS error in browser",
         "The ALLOWED_ORIGINS in Railway does not match your Vercel URL. "
         "Update ALLOWED_ORIGINS in Railway Variables to exactly match your Vercel URL (no trailing slash)."),
        ("Estimate returns error 503",
         "The ML model file (champion_model.pkl) was not found. "
         "Upload it to Cloudflare R2 at models/champion_model.pkl as described in Phase 3 Step 5. "
         "The backend will use a synthetic fallback if R2 is not configured."),
        ("Vercel build fails",
         "Check the Vercel build log. Most common cause: environment variables were not added. "
         "Go to Vercel -> Project Settings -> Environment Variables and verify all 3 are set."),
        ("GitHub push asks for password repeatedly",
         "Use a Personal Access Token (PAT) instead of your GitHub password. "
         "Create one at github.com -> Settings -> Developer Settings -> Personal access tokens."),
        ("GitHub Actions workflow fails on 'Deploy Backend'",
         "Check that RAILWAY_TOKEN and RAILWAY_SERVICE_ID secrets are set correctly in GitHub. "
         "The Service ID is in Railway -> Service -> Settings -> Service ID."),
    ]
    for problem, solution in problems:
        pdf.set_fill_color(*WARN_RED)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(160, 30, 30)
        pdf.multi_cell(PAGE_W, 6, sanitize(f"Problem: {problem}"), fill=True)
        pdf.set_fill_color(252, 252, 252)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.multi_cell(PAGE_W, 5.5, sanitize(f"Solution: {solution}"))
        pdf.ln(1)

    pdf.info_box(
        "Congratulations -- if all checkboxes are ticked, iNHCES is live on the internet!\n\n"
        "Your URLs:\n"
        "  Frontend (website):  https://YOUR_PROJECT.vercel.app\n"
        "  Backend  (API):      https://YOUR_SERVICE.up.railway.app\n"
        "  API docs:            https://YOUR_SERVICE.up.railway.app/docs\n\n"
        "DATA SOURCE: AMBER -- AI-authored guide. TETFund NRF 2025 | Dept. of Quantity Surveying, ABU Zaria."
    )

    # Save
    out_path = os.path.join(OUTPUT_DIR, "O6_15_Step_By_Step_Deployment.pdf")
    pdf.output(out_path)
    print(f"[OK] {out_path}")
    print(f"     Pages: {pdf.page}")


if __name__ == "__main__":
    generate()
