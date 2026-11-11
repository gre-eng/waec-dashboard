import pandas as pd
import json

df = pd.read_excel("WAEC_STATISTICS_2019-2021.xlsx", sheet_name="Analysis")

df.columns = [
    "Indicator",
    "NC_2019","NE_2019","NW_2019","Offshore_2019","SE_2019","SS_2019","SW_2019","Total_2019",
    "NC_2020","NE_2020","NW_2020","Offshore_2020","SE_2020","SS_2020","SW_2020","Total_2020",
    "NC_2021","NE_2021","NW_2021","Offshore_2021","SE_2021","SS_2021","SW_2021","Total_2021"
]

df = df.drop([0, 1]).reset_index(drop=True)

df["Indicator"] = [
    "5Credits_EngMaths","Private","Female","Male",
    "Public","Female","Male",
    "5Credits_English","Private","Female","Male",
    "Public","Female","Male",
    "5Credits_Maths","Private","Female","Male",
    "Public","Female","Male",
    "TotalSat","Private","Female","Male",
    "Public","Female","Male"
]

def get_row(indicator, parent=None):
    idx = df[df["Indicator"] == indicator].index.tolist()
    if parent:
        parent_idx = df[df["Indicator"] == parent].index[0]
        idx = [i for i in idx if i > parent_idx]
    return df.loc[idx[0]]

years = [2019, 2020, 2021]

total_sat      = [int(get_row("TotalSat")[f"Total_{y}"]) for y in years]
private_sat    = [int(get_row("Private","TotalSat")[f"Total_{y}"]) for y in years]
public_sat     = [int(get_row("Public","TotalSat")[f"Total_{y}"]) for y in years]
private_pass   = [int(get_row("Private","5Credits_EngMaths")[f"Total_{y}"]) for y in years]
public_pass    = [int(get_row("Public","5Credits_EngMaths")[f"Total_{y}"]) for y in years]
private_male   = [int(get_row("Male","Private")[f"Total_{y}"]) for y in years]
private_female = [int(get_row("Female","Private")[f"Total_{y}"]) for y in years]
public_male    = [int(get_row("Male","Public")[f"Total_{y}"]) for y in years]
public_female  = [int(get_row("Female","Public")[f"Total_{y}"]) for y in years]

private_pass_pct = [round(private_pass[i]/private_sat[i]*100,1) for i in range(3)]
public_pass_pct  = [round(public_pass[i]/public_sat[i]*100,1) for i in range(3)]
overall_pass_pct = [round((private_pass[i]+public_pass[i])/total_sat[i]*100,1) for i in range(3)]

zones     = ["N. Central","N. East","N. West","S. East","S. South","S. West"]
zone_cols = ["NC","NE","NW","SE","SS","SW"]

zone_sat = {
    y: [int(get_row("TotalSat")[f"{c}_{y}"]) for c in zone_cols]
    for y in years
}
zone_pass = {
    y: [
        int(get_row("Private","5Credits_EngMaths")[f"{c}_{y}"]) +
        int(get_row("Public","5Credits_EngMaths")[f"{c}_{y}"])
        for c in zone_cols
    ]
    for y in years
}
zone_pass_pct = {
    y: [round(zone_pass[y][i]/zone_sat[y][i]*100,1) for i in range(6)]
    for y in years
}

states = [
    "Abia","Abuja","Adamawa","Akwa Ibom","Anambra","Bauchi","Bayelsa",
    "Benue","Borno","Cross River","Delta","Ebonyi","Edo","Ekiti","Enugu",
    "Gombe","Imo","Jigawa","Kaduna","Kano","Katsina","Kebbi","Kogi",
    "Kwara","Lagos","Nassarawa","Niger","Ogun","Ondo","Osun","Oyo",
    "Plateau","Rivers","Sokoto","Taraba","Yobe","Zamfara"
]

state_p19 = [94.3,71.5,67.0,78.0,76.4,59.7,77.7,66.2,55.2,74.4,80.6,75.2,
             80.4,75.6,70.9,68.4,87.1,75.0,60.7,80.2,72.5,86.9,61.7,60.0,
             83.5,76.5,65.0,89.0,79.9,66.8,73.4,55.4,87.9,81.4,61.6,39.4,53.4]

state_p20 = [93.7,62.5,65.6,82.9,75.4,38.7,36.2,72.5,52.0,72.2,80.0,69.6,
             86.8,82.2,82.5,60.3,88.6,64.0,64.9,72.5,78.4,92.1,74.1,44.4,
             78.7,66.2,75.5,86.9,72.8,31.7,69.8,64.7,86.0,83.6,67.6,42.3,78.3]

state_p21 = [79.5,84.1,88.8,92.2,92.8,78.0,81.7,91.4,77.5,89.9,92.3,89.2,
             92.2,70.5,91.2,89.0,81.7,79.5,86.6,91.8,71.2,96.7,89.0,71.5,
             87.6,89.2,85.3,93.1,86.9,66.0,79.9,84.2,90.7,97.2,88.9,74.0,36.1]

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WAEC Nigeria 2019-2021</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;500&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#ffffff;color:#111111;font-family:'Inter',sans-serif;font-weight:400;line-height:1.7}
a{color:inherit;text-decoration:none}
.nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:1.5rem 3rem;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e6e6e6;background:#ffffff}
.nav-brand{font-family:'Playfair Display',serif;font-size:18px;letter-spacing:.02em;color:#111111}
.nav-sub{font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#666}
.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:flex-end;padding:0 3rem 4rem;border-bottom:1px solid #e6e6e6}
.hero-label{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#666;margin-bottom:1.5rem}
.hero-title{font-family:'Playfair Display',serif;font-size:clamp(42px,7vw,88px);font-weight:400;line-height:1.05;color:#111111;margin-bottom:2rem;max-width:800px}
.hero-desc{font-size:14px;color:#555555;max-width:520px;line-height:1.8;margin-bottom:3rem}
.hero-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#e6e6e6;border:1px solid #e6e6e6;max-width:720px}
.hero-metric{background:#ffffff;padding:1.5rem;text-align:center}
.hero-metric-year{font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#6b6b6b;margin-bottom:.5rem}
.hero-metric-val{font-family:'Playfair Display',serif;font-size:28px;color:#111111;margin-bottom:.25rem}
.hero-metric-label{font-size:11px;color:#6b6b6b;letter-spacing:.05em}
.section{padding:5rem 3rem;border-bottom:1px solid #e6e6e6}
.section-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:3rem}
.section-num{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#6b6b6b}
.section-title{font-family:'Playfair Display',serif;font-size:clamp(24px,3vw,36px);font-weight:400;color:#111111;margin-top:.5rem}
.section-desc{font-size:13px;color:#666;max-width:360px;text-align:right;line-height:1.7;margin-top:.5rem}
.tabs{display:flex;gap:0;margin-bottom:2.5rem;border-bottom:1px solid #e6e6e6}
.tab{padding:.75rem 1.5rem;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#6b6b6b;cursor:pointer;border:none;background:transparent;border-bottom:1px solid transparent;margin-bottom:-1px;transition:color .2s,border-color .2s}
.tab:hover{color:#111111}
.tab.active{color:#111111;border-bottom-color:#111111}
.panel{display:none}
.panel.active{display:block}
.chart-wrap{position:relative;width:100%}
.chart-label{font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#6b6b6b;margin-bottom:1.5rem}
.legend{display:flex;gap:2rem;margin-bottom:2rem}
.leg{display:flex;align-items:center;gap:.5rem;font-size:12px;color:#666}
.leg-dot{width:8px;height:8px;border-radius:50%}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:3rem}
@media(max-width:640px){.two-col{grid-template-columns:1fr}.nav{padding:1.25rem 1.5rem}.hero{padding:0 1.5rem 3rem}.section{padding:3rem 1.5rem}.hero-metrics{grid-template-columns:repeat(2,1fr)}.tabs{overflow-x:auto}}
.divider{height:1px;background:#e6e6e6;margin:0 3rem}
.dash-hero{padding:5rem 3rem 3rem}
.dash-hero-label{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#6b6b6b;margin-bottom:1rem}
.dash-hero-title{font-family:'Playfair Display',serif;font-size:clamp(28px,4vw,48px);font-weight:400;color:#111111;margin-bottom:1rem}
.dash-hero-desc{font-size:13px;color:#666;max-width:560px;line-height:1.8}
.dash-body{padding:0 3rem 5rem}
.add-row{display:flex;gap:1rem;margin-bottom:2rem;align-items:center}
.add-row input{background:transparent;border:none;border-bottom:1px solid #cccccc;color:#111111;font-family:'Inter',sans-serif;font-size:13px;padding:.5rem 0;width:240px;outline:none;transition:border-color .2s}
.add-row input:focus{border-bottom-color:#111111}
.add-row input::placeholder{color:#777777}
.add-btn{background:transparent;border:1px solid #cccccc;color:#555555;font-family:'Inter',sans-serif;font-size:12px;letter-spacing:.1em;text-transform:uppercase;padding:.6rem 1.25rem;cursor:pointer;transition:color .2s,border-color .2s}
.add-btn:hover{color:#111111;border-color:#111111}
.subj-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:0;background:#ffffff;margin-bottom:2rem;border-top:1px solid #e6e6e6;border-left:1px solid #e6e6e6}
.subj-card{background:#ffffff;padding:1.5rem;border-right:1px solid #e6e6e6;border-bottom:1px solid #e6e6e6}
.subj-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.25rem}
.subj-name{font-size:13px;letter-spacing:.05em;color:#111111}
.subj-right{display:flex;align-items:center;gap:.75rem}
.grade-badge{font-size:11px;font-weight:500;letter-spacing:.1em;padding:.2rem .6rem;border-radius:2px}
.remove-btn{background:none;border:none;color:#777777;font-size:18px;cursor:pointer;line-height:1;transition:color .2s;padding:0}
.remove-btn:hover{color:#111111}
.bar-row{display:flex;align-items:center;gap:.75rem;margin-bottom:.75rem}
.bar-label{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#6b6b6b;width:80px;flex-shrink:0}
.bar-track{flex:1;height:2px;background:#e6e6e6}
.bar-fill{height:2px;transition:width .3s}
.bar-num{font-size:11px;color:#666;width:20px;text-align:right}
.inp-row{display:flex;gap:1rem;margin-top:1rem}
.inp-wrap{flex:1}
.inp-wrap input{width:100%;background:transparent;border:none;border-bottom:1px solid #dddddd;color:#111111;font-family:'Inter',sans-serif;font-size:13px;padding:.4rem 0;text-align:center;outline:none;transition:border-color .2s}
.inp-wrap input:focus{border-bottom-color:#111111}
.inp-wrap label{display:block;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#777777;text-align:center;margin-top:.35rem}
.analyze-btn{background:transparent;border:1px solid #777777;color:#555555;font-family:'Inter',sans-serif;font-size:12px;letter-spacing:.15em;text-transform:uppercase;padding:.8rem 2rem;cursor:pointer;transition:all .2s;margin-bottom:3rem}
.analyze-btn:hover{border-color:#111111;color:#111111}
.results{padding-top:1rem}
.r-metrics{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:0;background:#ffffff;margin-bottom:3rem;border-top:1px solid #e6e6e6;border-left:1px solid #e6e6e6}
.r-metric{background:#ffffff;padding:1.25rem;text-align:center;border-right:1px solid #e6e6e6;border-bottom:1px solid #e6e6e6}
.r-metric-label{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#6b6b6b;margin-bottom:.5rem}
.r-metric-val{font-family:'Playfair Display',serif;font-size:26px;color:#111111}
.r-block{margin-bottom:2.5rem;border-top:1px solid #e6e6e6;padding-top:1.5rem}
.r-block-title{font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#6b6b6b;margin-bottom:1.25rem}
.risk-track{height:2px;background:#e6e6e6;margin:.75rem 0 .5rem}
.risk-fill{height:2px;transition:width .4s}
.r-subj-row{display:flex;justify-content:space-between;align-items:center;padding:.6rem 0;border-bottom:1px solid #eeeeee;font-size:12px;gap:.5rem}
.r-subj-row:last-child{border-bottom:none}
.tip-item{display:flex;gap:1rem;margin-bottom:1.25rem}
.tip-icon{font-size:16px;flex-shrink:0;margin-top:2px}
.tip-text{font-size:13px;color:#444444;line-height:1.6}
.tip-sub{font-size:11px;color:#6b6b6b;margin-top:.3rem}
.heatmap-table{width:100%;border-collapse:collapse;font-size:12px}
.heatmap-table th{text-align:left;padding:.6rem .75rem;border-bottom:1px solid #e6e6e6;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#6b6b6b;font-weight:400}
.heatmap-table th:not(:first-child){text-align:right}
.heatmap-table td{padding:.5rem .75rem;border-bottom:1px solid #f5f5f5;color:#444444}
.heatmap-table td:not(:first-child){text-align:right;font-variant-numeric:tabular-nums}
.heatmap-table tr:hover td{background:#f5f5f5}
.heat-cell{display:inline-block;padding:.15rem .5rem;border-radius:2px;font-weight:500;font-size:11px}
.footer{padding:3rem;border-top:1px solid #e6e6e6;display:flex;justify-content:space-between;align-items:center}
.footer-left{font-size:11px;color:#777777;letter-spacing:.05em}
.footer-right{font-size:11px;color:#999999;letter-spacing:.05em}
</style>
</head>
<body>
"""

html += f"""
<nav class="nav">
  <div class="nav-brand">WAEC Nigeria</div>
  <div class="nav-sub">Statistics 2019 &ndash; 2021</div>
</nav>

<div class="hero">
  <div class="hero-label">NBS Public Dataset &mdash; WASSCE School Candidates</div>
  <h1 class="hero-title">West Africa Examinations Council</h1>
  <p class="hero-desc">A visual analysis of school candidate performance across Nigeria from 2019 to 2021, covering enrolment, pass rates, gender distribution, geo-zones and all 37 states.</p>
  <div class="hero-metrics">
    <div class="hero-metric">
      <div class="hero-metric-year">2019</div>
      <div class="hero-metric-val">{total_sat[0]/1e6:.2f}M</div>
      <div class="hero-metric-label">Total sat</div>
    </div>
    <div class="hero-metric">
      <div class="hero-metric-year">2019</div>
      <div class="hero-metric-val">{overall_pass_pct[0]}%</div>
      <div class="hero-metric-label">Pass rate</div>
    </div>
    <div class="hero-metric">
      <div class="hero-metric-year">2020</div>
      <div class="hero-metric-val">{total_sat[1]/1e6:.2f}M</div>
      <div class="hero-metric-label">Total sat</div>
    </div>
    <div class="hero-metric">
      <div class="hero-metric-year">2020</div>
      <div class="hero-metric-val">{overall_pass_pct[1]}%</div>
      <div class="hero-metric-label">Pass rate</div>
    </div>
    <div class="hero-metric">
      <div class="hero-metric-year">2021</div>
      <div class="hero-metric-val">{total_sat[2]/1e6:.2f}M</div>
      <div class="hero-metric-label">Total sat</div>
    </div>
    <div class="hero-metric">
      <div class="hero-metric-year">2021</div>
      <div class="hero-metric-val">{overall_pass_pct[2]}%</div>
      <div class="hero-metric-label">Pass rate</div>
    </div>
    <div class="hero-metric">
      <div class="hero-metric-year">Private 2021</div>
      <div class="hero-metric-val">{private_pass_pct[2]}%</div>
      <div class="hero-metric-label">Pass rate</div>
    </div>
    <div class="hero-metric">
      <div class="hero-metric-year">Public 2021</div>
      <div class="hero-metric-val">{public_pass_pct[2]}%</div>
      <div class="hero-metric-label">Pass rate</div>
    </div>
  </div>
</div>
"""

html += f"""
<div class="section">
  <div class="section-header">
    <div>
      <div class="section-num">01 &mdash; Charts</div>
      <div class="section-title">Performance at a glance</div>
    </div>
    <div class="section-desc">Five interactive charts covering enrolment, pass rates, gender distribution, geo-zones and state-level performance.</div>
  </div>

  <div class="tabs">
    <button class="tab active" onclick="showTab('enrol',this)">Enrolment</button>
    <button class="tab" onclick="showTab('pass',this)">Pass Rates</button>
    <button class="tab" onclick="showTab('gender',this)">Gender</button>
    <button class="tab" onclick="showTab('zone',this)">Geo-Zones</button>
    <button class="tab" onclick="showTab('heatmap',this)">State Heatmap</button>
  </div>

  <div id="enrol" class="panel active">
    <div class="chart-label">Total candidates sat &mdash; private vs public schools</div>
    <div class="legend">
      <div class="leg"><div class="leg-dot" style="background:#7eb3d8"></div>Private</div>
      <div class="leg"><div class="leg-dot" style="background:#c47b5a"></div>Public</div>
    </div>
    <div class="chart-wrap" style="height:320px"><canvas id="c1"></canvas></div>
  </div>

  <div id="pass" class="panel">
    <div class="chart-label">National pass rate &mdash; 5 credits including English and Mathematics</div>
    <div class="legend">
      <div class="leg"><div class="leg-dot" style="background:#7eb3d8"></div>Private</div>
      <div class="leg"><div class="leg-dot" style="background:#c47b5a"></div>Public</div>
      <div class="leg"><div class="leg-dot" style="background:#555555"></div>Overall</div>
    </div>
    <div class="chart-wrap" style="height:320px"><canvas id="c2"></canvas></div>
  </div>

  <div id="gender" class="panel">
    <div class="two-col">
      <div>
        <div class="chart-label">Private schools &mdash; male vs female</div>
        <div class="legend">
          <div class="leg"><div class="leg-dot" style="background:#7eb3d8"></div>Male</div>
          <div class="leg"><div class="leg-dot" style="background:#c47b5a"></div>Female</div>
        </div>
        <div class="chart-wrap" style="height:280px"><canvas id="c3"></canvas></div>
      </div>
      <div>
        <div class="chart-label">Public schools &mdash; male vs female</div>
        <div class="legend">
          <div class="leg"><div class="leg-dot" style="background:#7eb3d8"></div>Male</div>
          <div class="leg"><div class="leg-dot" style="background:#c47b5a"></div>Female</div>
        </div>
        <div class="chart-wrap" style="height:280px"><canvas id="c4"></canvas></div>
      </div>
    </div>
  </div>

  <div id="zone" class="panel">
    <div class="chart-label">Pass rate by geo-zone &mdash; 5 credits including English and Mathematics</div>
    <div class="legend">
      <div class="leg"><div class="leg-dot" style="background:#4a7c6f"></div>2019</div>
      <div class="leg"><div class="leg-dot" style="background:#7eb3d8"></div>2020</div>
      <div class="leg"><div class="leg-dot" style="background:#c4a35a"></div>2021</div>
    </div>
    <div class="chart-wrap" style="height:320px"><canvas id="c5"></canvas></div>
  </div>

  <div id="heatmap" class="panel">
    <div class="chart-label">Private school pass rate by state &mdash; colour intensity reflects performance</div>
    <div style="overflow-x:auto">
      <table class="heatmap-table">
        <thead>
          <tr>
            <th>State</th>
            <th style="text-align:right">2019</th>
            <th style="text-align:right">2020</th>
            <th style="text-align:right">2021</th>
            <th style="text-align:right">Trend</th>
          </tr>
        </thead>
        <tbody id="htbody"></tbody>
      </table>
    </div>
  </div>

</div>
"""

html += """
<div class="divider"></div>

<div class="dash-hero">
  <div class="dash-hero-label">02 &mdash; Student Tool</div>
  <div class="dash-hero-title">Performance Predictor</div>
  <p class="dash-hero-desc">Enter your CA score out of 30 and your exam score out of 70 for each subject. The tool will predict your grade, calculate your fail risk, and give you personalised improvement tips. There is always room to grow.</p>
</div>

<div class="dash-body">
  <div class="add-row">
    <input type="text" id="newSubj" placeholder="Add a subject" />
    <button class="add-btn" onclick="addSubject()">+ Add</button>
  </div>

  <div class="subj-grid" id="subjGrid"></div>

  <button class="analyze-btn" onclick="analyze()">Analyse My Scores</button>

  <div class="results" id="resultsArea"></div>
</div>

<div class="footer">
  <div class="footer-left">WAEC Nigeria &mdash; NBS Public Dataset &mdash; 2019 to 2021</div>
  <div class="footer-right">5 credits and above including English and Mathematics</div>
</div>
"""

html += f"""
<script>
function showTab(id, el) {{
  document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  el.classList.add("active");
}}

const GRADES = [
  {{min:70,grade:"A",bg:"#e6f4e6",fg:"#1e7a1e",risk:5}},
  {{min:60,grade:"B",bg:"#e3f0f5",fg:"#1b6f8a",risk:15}},
  {{min:50,grade:"C",bg:"#f6f0dc",fg:"#8a6d10",risk:35}},
  {{min:45,grade:"D",bg:"#f8e9e1",fg:"#a4501f",risk:60}},
  {{min:0, grade:"F",bg:"#fbe4e4",fg:"#b32d2d",risk:90}}
];

const TIPS = {{
  A:[
    {{icon:"🏆",text:"Push deeper into past questions from 2015 to 2023 to lock in complete familiarity with question patterns.",sub:"Target: zero surprises on exam day."}},
    {{icon:"👥",text:"Teach this subject to a classmate. Teaching forces you to find gaps you never knew existed.",sub:"30 minutes of teaching equals 2 hours of reading."}},
    {{icon:"⏱",text:"Work on exam speed. Attempt full past papers under strict timed conditions.",sub:"Accuracy without speed will not maximise your score."}}
  ],
  B:[
    {{icon:"🎯",text:"You are close to an A. Identify the exact topics where you lose marks and drill only those.",sub:"Focused revision beats broad re-reading every time."}},
    {{icon:"📝",text:"Make a one-page summary of every tricky topic and review it daily for 5 minutes.",sub:"Spaced repetition turns weak areas into strengths."}},
    {{icon:"📈",text:"Protect your CA by submitting all assignments on time and revising every class test.",sub:"Every CA mark counts toward your final score."}}
  ],
  C:[
    {{icon:"⚠️",text:"You are passing but at risk if your exam performance drops. Raise your CA score first.",sub:"Aim for above 20 out of 30 in your next CA test."}},
    {{icon:"📖",text:"Go back to basics on foundational topics before attempting harder questions.",sub:"Weak foundations cause marks to leak in every question."}},
    {{icon:"📅",text:"Create a daily 45-minute revision block for this subject and keep it for 3 weeks.",sub:"Consistency beats cramming every single time."}}
  ],
  D:[
    {{icon:"🔥",text:"You are close to failing. Focus all revision on topics that appear most in WAEC past papers.",sub:"Prioritise essay and theory questions — they carry the most marks."}},
    {{icon:"🙋",text:"Speak to your teacher this week. Ask exactly what you keep getting wrong and how to fix it.",sub:"One honest conversation can save your grade."}},
    {{icon:"✍️",text:"Practice past questions under exam conditions every day for at least 30 minutes.",sub:"You cannot read your way out of a D. You must practice."}}
  ],
  F:[
    {{icon:"🚨",text:"Failing risk is high. Pick the 3 most important topics and master only those first.",sub:"Three topics done well beats ten topics done poorly."}},
    {{icon:"🤝",text:"Find a study partner or join a lesson group immediately. Isolation makes failing worse.",sub:"Struggling alone is the most common reason students fail."}},
    {{icon:"🔁",text:"Re-read your class notes from the very beginning of term. Most WAEC questions test basic understanding.",sub:"Do not skip to advanced topics before mastering the basics."}}
  ]
}};

const UNIVERSAL = [
  {{icon:"🌙",text:"Sleep 7 to 8 hours the night before any exam. Sleep-deprived students score up to 30 percent lower.",sub:"Your brain consolidates memory during sleep — do not cut it short."}},
  {{icon:"💧",text:"Drink water during revision and in the exam hall. Dehydration reduces concentration noticeably.",sub:"Keep a water bottle on your desk at all times."}},
  {{icon:"🏃",text:"Take a 10-minute walk or stretch every 45 minutes of studying.",sub:"Movement improves blood flow to the brain and resets your focus."}}
];

let subjects = ["English Language","Mathematics","Biology","Chemistry","Physics","Economics"].map(n => ({{name:n,ca:"",exam:""}}));

function getGrade(total) {{
  return GRADES.find(g => total >= g.min) || GRADES[GRADES.length - 1];
}}

function esc(t) {{
  return String(t).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}}

/* Update only the bars and the grade badge of one card.
   The input boxes are NOT rebuilt, so the cursor stays where it is. */
function updateCard(i) {{
  const s = subjects[i];
  const ca = parseFloat(s.ca) || 0;
  const ex = parseFloat(s.exam) || 0;
  const g = getGrade(ca + ex);
  const badge = document.getElementById("badge_" + i);
  if (!badge) return;
  badge.textContent = g.grade;
  badge.style.background = g.bg;
  badge.style.color = g.fg;
  document.getElementById("caBar_" + i).style.width = Math.min(100, (ca / 30) * 100).toFixed(0) + "%";
  document.getElementById("exBar_" + i).style.width = Math.min(100, (ex / 70) * 100).toFixed(0) + "%";
  document.getElementById("caNum_" + i).textContent = ca > 0 ? ca.toFixed(0) : "–";
  document.getElementById("exNum_" + i).textContent = ex > 0 ? ex.toFixed(0) : "–";
}}

/* Runs when the box loses focus: tidy the number, never rebuild the cards */
function enforceRange(el, min, max, i, field) {{
  let val = parseFloat(el.value);
  if (isNaN(val)) {{ subjects[i][field] = ""; el.value = ""; updateCard(i); return; }}
  if (val < min) val = min;
  if (val > max) val = max;
  el.value = val;
  subjects[i][field] = val;
  updateCard(i);
}}

/* Runs on every keystroke: store the value and update the bars only */
function updateScore(i, field, val) {{
  const max = field === "ca" ? 30 : 70;
  let n = parseFloat(val);
  if (!isNaN(n)) {{
    if (n < 0) n = 0;
    if (n > max) n = max;
    subjects[i][field] = n;
  }} else {{
    subjects[i][field] = "";
  }}
  updateCard(i);
}}

/* Full rebuild: only used when a subject is added or removed */
function renderSubjects() {{
  const grid = document.getElementById("subjGrid");
  let html = "";
  subjects.forEach((s, i) => {{
    const ca = parseFloat(s.ca) || 0;
    const ex = parseFloat(s.exam) || 0;
    const g = getGrade(ca + ex);
    const caBar = Math.min(100,(ca/30)*100).toFixed(0);
    const exBar = Math.min(100,(ex/70)*100).toFixed(0);
    html += `
    <div class="subj-card">
      <div class="subj-top">
        <span class="subj-name">${{esc(s.name)}}</span>
        <div class="subj-right">
          <span class="grade-badge" id="badge_${{i}}" style="background:${{g.bg}};color:${{g.fg}}">${{g.grade}}</span>
          <button class="remove-btn" onclick="removeSubj(${{i}})">&#215;</button>
        </div>
      </div>
      <div class="bar-row">
        <span class="bar-label">CA / 30</span>
        <div class="bar-track"><div class="bar-fill" id="caBar_${{i}}" style="width:${{caBar}}%;background:#7eb3d8"></div></div>
        <span class="bar-num" id="caNum_${{i}}">${{ca > 0 ? ca.toFixed(0) : "–"}}</span>
      </div>
      <div class="bar-row">
        <span class="bar-label">Exam / 70</span>
        <div class="bar-track"><div class="bar-fill" id="exBar_${{i}}" style="width:${{exBar}}%;background:#c4a35a"></div></div>
        <span class="bar-num" id="exNum_${{i}}">${{ex > 0 ? ex.toFixed(0) : "–"}}</span>
      </div>
      <div class="inp-row">
        <div class="inp-wrap">
          <input id="ca_${{i}}" type="number" min="0" max="30" step="0.5"
            value="${{s.ca}}" placeholder="0 – 30"
            oninput="updateScore(${{i}},'ca',this.value)"
            onblur="enforceRange(this,0,30,${{i}},'ca')" />
          <label>CA max 30</label>
        </div>
        <div class="inp-wrap">
          <input id="exam_${{i}}" type="number" min="0" max="70" step="0.5"
            value="${{s.exam}}" placeholder="0 – 70"
            oninput="updateScore(${{i}},'exam',this.value)"
            onblur="enforceRange(this,0,70,${{i}},'exam')" />
          <label>Exam max 70</label>
        </div>
      </div>
    </div>`;
  }});
  grid.innerHTML = html;
}}

function removeSubj(i) {{
  subjects.splice(i, 1);
  renderSubjects();
}}

function addSubject() {{
  const inp = document.getElementById("newSubj");
  const name = inp.value.trim();
  if (!name) return;
  subjects.push({{name, ca:"", exam:""}});
  inp.value = "";
  renderSubjects();
}}

function analyze() {{
  const scored = subjects.map(s => {{
    const ca = parseFloat(s.ca) || 0;
    const ex = parseFloat(s.exam) || 0;
    const total = ca + ex;
    return {{...s, ca, ex, total, ...getGrade(total)}};
  }}).filter(s => s.ca > 0 || s.ex > 0);

  if (!scored.length) {{ alert("Please enter at least one score first."); return; }}

  const avgTotal = scored.reduce((a,s) => a + s.total, 0) / scored.length;
  const overallRisk = Math.round(scored.reduce((a,s) => a + s.risk, 0) / scored.length);
  const avgGrade = getGrade(avgTotal);
  const atRisk = scored.filter(s => s.grade === "D" || s.grade === "F");
  const riskColor = overallRisk > 60 ? "#b32d2d" : overallRisk > 35 ? "#8a6d10" : "#1e7a1e";
  const weakest = [...scored].sort((a,b) => a.total - b.total).slice(0,2);
  const strongest = [...scored].sort((a,b) => b.total - a.total).slice(0,1);

  let html = `
  <div class="r-metrics">
    <div class="r-metric">
      <div class="r-metric-label">Average score</div>
      <div class="r-metric-val">${{avgTotal.toFixed(1)}}</div>
    </div>
    <div class="r-metric">
      <div class="r-metric-label">Overall grade</div>
      <div class="r-metric-val">${{avgGrade.grade}}</div>
    </div>
    <div class="r-metric">
      <div class="r-metric-label">Subjects tracked</div>
      <div class="r-metric-val">${{scored.length}}</div>
    </div>
    <div class="r-metric">
      <div class="r-metric-label">At risk</div>
      <div class="r-metric-val" style="color:${{atRisk.length > 0 ? "#b32d2d" : "#1e7a1e"}}">${{atRisk.length}}</div>
    </div>
  </div>

  <div class="r-block">
    <div class="r-block-title">Predicted fail risk</div>
    <div style="display:flex;justify-content:space-between;font-size:12px;color:#6b6b6b">
      <span>Based on current scores</span>
      <span style="color:${{riskColor}}">${{overallRisk}}%</span>
    </div>
    <div class="risk-track"><div class="risk-fill" style="width:${{overallRisk}}%;background:${{riskColor}}"></div></div>
    <div style="font-size:11px;color:#777777;margin-top:.5rem">Based on the WAEC 45 out of 100 pass threshold.</div>
  </div>

  <div class="r-block">
    <div class="r-block-title">Score breakdown</div>
    ${{scored.map(s => `
      <div class="r-subj-row">
        <span style="color:#444444">${{esc(s.name)}}</span>
        <span style="color:#6b6b6b">CA ${{s.ca}}/30 &nbsp;&middot;&nbsp; Exam ${{s.ex}}/70</span>
        <span style="color:#111111;font-weight:500">${{s.total.toFixed(0)}}/100</span>
        <span class="grade-badge" style="background:${{s.bg}};color:${{s.fg}}">${{s.grade}}</span>
      </div>`).join("")}}
  </div>`;

  html += `<div class="r-block"><div class="r-block-title">Improvement tips &mdash; weakest subjects</div>`;
  weakest.forEach(s => {{
    html += `<div style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#6b6b6b;margin:1rem 0 .75rem">${{esc(s.name)}} &mdash; ${{s.total.toFixed(0)}} / 100</div>`;
    TIPS[s.grade].forEach(t => {{
      html += `<div class="tip-item"><span class="tip-icon">${{t.icon}}</span><div><div class="tip-text">${{t.text}}</div><div class="tip-sub">${{t.sub}}</div></div></div>`;
    }});
  }});
  html += `</div>`;

  html += `<div class="r-block"><div class="r-block-title">Even your best subject &mdash; keep climbing</div>`;
  strongest.forEach(s => {{
    html += `<div style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#6b6b6b;margin:1rem 0 .75rem">${{esc(s.name)}} &mdash; ${{s.total.toFixed(0)}} / 100</div>`;
    TIPS[s.grade].forEach(t => {{
      html += `<div class="tip-item"><span class="tip-icon">${{t.icon}}</span><div><div class="tip-text">${{t.text}}</div><div class="tip-sub">${{t.sub}}</div></div></div>`;
    }});
  }});
  html += `</div>`;

  html += `<div class="r-block"><div class="r-block-title">Universal habits &mdash; every student</div>`;
  UNIVERSAL.forEach(t => {{
    html += `<div class="tip-item"><span class="tip-icon">${{t.icon}}</span><div><div class="tip-text">${{t.text}}</div><div class="tip-sub">${{t.sub}}</div></div></div>`;
  }});
  html += `</div>`;

  document.getElementById("resultsArea").innerHTML = html;
}}

renderSubjects();

const gc = "rgba(0,0,0,0.07)";
const tc = "#6b6b6b";
const chartOpts = (yCallback) => ({{
  responsive:true,
  maintainAspectRatio:false,
  plugins:{{legend:{{display:false}}}},
  scales:{{
    x:{{grid:{{color:gc}},ticks:{{color:tc,font:{{size:11}}}},border:{{color:"#dddddd"}}}},
    y:{{grid:{{color:gc}},ticks:{{color:tc,font:{{size:11}},callback:yCallback}},border:{{color:"#dddddd"}}}}
  }}
}});

new Chart(document.getElementById("c1"),{{
  type:"line",
  data:{{
    labels:["2019","2020","2021"],
    datasets:[
      {{label:"Private",data:{json.dumps(private_sat)},borderColor:"#7eb3d8",backgroundColor:"rgba(126,179,216,0.06)",tension:0.4,pointRadius:4,pointBackgroundColor:"#7eb3d8",fill:true}},
      {{label:"Public", data:{json.dumps(public_sat)}, borderColor:"#c47b5a",backgroundColor:"rgba(196,123,90,0.06)",tension:0.4,pointRadius:4,pointBackgroundColor:"#c47b5a",fill:true}}
    ]
  }},
  options:chartOpts(v => (v/1000).toFixed(0)+"K")
}});

new Chart(document.getElementById("c2"),{{
  type:"bar",
  data:{{
    labels:["2019","2020","2021"],
    datasets:[
      {{label:"Private",data:{json.dumps(private_pass_pct)},backgroundColor:"rgba(126,179,216,0.7)"}},
      {{label:"Public", data:{json.dumps(public_pass_pct)}, backgroundColor:"rgba(196,123,90,0.7)"}},
      {{label:"Overall",data:{json.dumps(overall_pass_pct)},backgroundColor:"rgba(150,150,150,0.4)"}}
    ]
  }},
  options:{{...chartOpts(v => v+"%"),scales:{{...chartOpts(v=>v+"%").scales,y:{{...chartOpts(v=>v+"%").scales.y,min:0,max:100}}}}}}
}});

new Chart(document.getElementById("c3"),{{
  type:"bar",
  data:{{
    labels:["2019","2020","2021"],
    datasets:[
      {{label:"Male",  data:{json.dumps(private_male)},  backgroundColor:"rgba(126,179,216,0.7)"}},
      {{label:"Female",data:{json.dumps(private_female)},backgroundColor:"rgba(196,123,90,0.7)"}}
    ]
  }},
  options:{{...chartOpts(v=>(v/1000).toFixed(0)+"K"),scales:{{x:{{stacked:true,grid:{{color:gc}},ticks:{{color:tc}},border:{{color:"#dddddd"}}}},y:{{stacked:true,grid:{{color:gc}},ticks:{{color:tc,callback:v=>(v/1000).toFixed(0)+"K"}},border:{{color:"#dddddd"}}}}}}}}
}});

new Chart(document.getElementById("c4"),{{
  type:"bar",
  data:{{
    labels:["2019","2020","2021"],
    datasets:[
      {{label:"Male",  data:{json.dumps(public_male)},  backgroundColor:"rgba(126,179,216,0.7)"}},
      {{label:"Female",data:{json.dumps(public_female)},backgroundColor:"rgba(196,123,90,0.7)"}}
    ]
  }},
  options:{{...chartOpts(v=>(v/1000).toFixed(0)+"K"),scales:{{x:{{stacked:true,grid:{{color:gc}},ticks:{{color:tc}},border:{{color:"#dddddd"}}}},y:{{stacked:true,grid:{{color:gc}},ticks:{{color:tc,callback:v=>(v/1000).toFixed(0)+"K"}},border:{{color:"#dddddd"}}}}}}}}
}});

new Chart(document.getElementById("c5"),{{
  type:"bar",
  data:{{
    labels:{json.dumps(zones)},
    datasets:[
      {{label:"2019",data:{json.dumps(zone_pass_pct[2019])},backgroundColor:"rgba(74,124,111,0.8)"}},
      {{label:"2020",data:{json.dumps(zone_pass_pct[2020])},backgroundColor:"rgba(126,179,216,0.8)"}},
      {{label:"2021",data:{json.dumps(zone_pass_pct[2021])},backgroundColor:"rgba(196,163,90,0.8)"}}
    ]
  }},
  options:{{...chartOpts(v=>v+"%"),scales:{{...chartOpts(v=>v+"%").scales,y:{{...chartOpts(v=>v+"%").scales.y,min:0,max:90}}}}}}
}});

const states = {json.dumps(states)};
const p19 = {json.dumps(state_p19)};
const p20 = {json.dumps(state_p20)};
const p21 = {json.dumps(state_p21)};

function heatColor(v) {{
  if (v >= 85) return {{bg:"rgba(30,122,30,0.12)",fg:"#1e7a1e"}};
  if (v >= 70) return {{bg:"rgba(27,111,138,0.12)",fg:"#1b6f8a"}};
  if (v >= 55) return {{bg:"rgba(138,109,16,0.12)", fg:"#8a6d10"}};
  return {{bg:"rgba(179,45,45,0.12)",fg:"#b32d2d"}};
}}

const tbody = document.getElementById("htbody");
states.forEach((s,i) => {{
  const trend = p21[i] > p19[i] ? "&#9650;" : p21[i] < p19[i] ? "&#9660;" : "&mdash;";
  const tColor = p21[i] > p19[i] ? "#1e7a1e" : p21[i] < p19[i] ? "#b32d2d" : "#6b6b6b";
  const c19 = heatColor(p19[i]);
  const c20 = heatColor(p20[i]);
  const c21 = heatColor(p21[i]);
  tbody.innerHTML += `<tr>
    <td style="color:#555555">${{s}}</td>
    <td><span class="heat-cell" style="background:${{c19.bg}};color:${{c19.fg}}">${{p19[i].toFixed(1)}}%</span></td>
    <td><span class="heat-cell" style="background:${{c20.bg}};color:${{c20.fg}}">${{p20[i].toFixed(1)}}%</span></td>
    <td><span class="heat-cell" style="background:${{c21.bg}};color:${{c21.fg}}">${{p21[i].toFixed(1)}}%</span></td>
    <td style="color:${{tColor}}">${{trend}}</td>
  </tr>`;
}});
</script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done! Open index.html in your browser.")
