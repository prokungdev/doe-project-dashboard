#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Dashboard HTML from extracted Excel data
"""
import json
import sys
import os

def build_dashboard():
    # Load JSON data
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard_data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data_json = json.dumps(data, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard จัดสรรเป้าหมายการดำเนินงาน ปีงบประมาณ พ.ศ. 2570</title>
<meta name="description" content="Dashboard แสดงเป้าหมายการดำเนินงาน กรมการจัดหางาน ประจำปีงบประมาณ พ.ศ. 2570">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --primary: #1a3a6b;
    --primary-light: #2355a0;
    --primary-dark: #0f2144;
    --accent: #f59e0b;
    --accent-light: #fcd34d;
    --success: #10b981;
    --danger: #ef4444;
    --info: #3b82f6;
    --purple: #8b5cf6;
    --bg: #0d1b2e;
    --bg2: #112240;
    --bg3: #162d4a;
    --card: #1e3a5f;
    --card-hover: #24476e;
    --border: rgba(255,255,255,0.08);
    --text: #e2e8f0;
    --text-muted: #94a3b8;
    --text-dim: #64748b;
    --shadow: 0 4px 24px rgba(0,0,0,0.4);
    --radius: 12px;
    --radius-sm: 8px;

    /* Quarter colors */
    --q1: #3b82f6;
    --q2: #10b981;
    --q3: #f59e0b;
    --q4: #ef4444;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Sarabun', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
  }}

  /* ===== HEADER ===== */
  .header {{
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 60%, var(--primary-light) 100%);
    padding: 20px 32px;
    display: flex;
    align-items: center;
    gap: 20px;
    border-bottom: 2px solid rgba(245,158,11,0.4);
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
  }}
  .header::before {{
    content: '';
    position: absolute;
    top: -50%; right: -5%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(245,158,11,0.12) 0%, transparent 70%);
    pointer-events: none;
  }}
  .header-icon {{
    width: 56px; height: 56px;
    background: linear-gradient(135deg, var(--accent), var(--accent-light));
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
    box-shadow: 0 4px 16px rgba(245,158,11,0.4);
    flex-shrink: 0;
  }}
  .header-text h1 {{
    font-size: 1.4rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.3;
  }}
  .header-text p {{
    font-size: 0.9rem;
    color: rgba(255,255,255,0.7);
    margin-top: 2px;
  }}
  .header-badge {{
    margin-left: auto;
    background: rgba(245,158,11,0.2);
    border: 1px solid rgba(245,158,11,0.4);
    color: var(--accent-light);
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    white-space: nowrap;
  }}

  /* ===== LAYOUT ===== */
  .layout {{
    display: flex;
    min-height: calc(100vh - 100px);
  }}

  /* ===== SIDEBAR ===== */
  .sidebar {{
    width: 300px;
    flex-shrink: 0;
    background: var(--bg2);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    height: calc(100vh - 100px);
    position: sticky;
    top: 0;
    overflow: hidden;
  }}
  .sidebar-header {{
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
    background: var(--bg3);
  }}
  .sidebar-title {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-dim);
    font-weight: 600;
    margin-bottom: 12px;
  }}
  .search-box {{
    display: flex;
    align-items: center;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    gap: 8px;
    transition: border-color 0.2s;
  }}
  .search-box:focus-within {{ border-color: var(--primary-light); }}
  .search-box input {{
    background: none;
    border: none;
    outline: none;
    color: var(--text);
    font-size: 0.9rem;
    font-family: 'Sarabun', sans-serif;
    width: 100%;
  }}
  .search-box input::placeholder {{ color: var(--text-dim); }}
  .search-icon {{ color: var(--text-dim); font-size: 1rem; }}

  .filter-tabs {{
    display: flex;
    gap: 4px;
    margin-top: 10px;
    flex-wrap: wrap;
  }}
  .filter-tab {{
    padding: 4px 10px;
    border-radius: 50px;
    font-size: 0.78rem;
    cursor: pointer;
    border: 1px solid var(--border);
    color: var(--text-muted);
    background: transparent;
    transition: all 0.2s;
    font-family: 'Sarabun', sans-serif;
  }}
  .filter-tab:hover {{ border-color: var(--primary-light); color: var(--text); }}
  .filter-tab.active {{
    background: var(--primary-light);
    border-color: var(--primary-light);
    color: #fff;
  }}

  .unit-list {{
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;
  }}
  .unit-list::-webkit-scrollbar {{ width: 4px; }}
  .unit-list::-webkit-scrollbar-track {{ background: transparent; }}
  .unit-list::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 4px; }}

  .unit-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 20px;
    cursor: pointer;
    transition: all 0.15s;
    border-left: 3px solid transparent;
  }}
  .unit-item:hover {{ background: var(--bg3); border-left-color: var(--primary-light); }}
  .unit-item.active {{
    background: rgba(35,85,160,0.25);
    border-left-color: var(--accent);
  }}
  .unit-badge {{
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }}
  .unit-name {{
    font-size: 0.88rem;
    line-height: 1.3;
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .unit-count {{
    font-size: 0.75rem;
    color: var(--text-dim);
  }}

  /* Category colors */
  .cat-central {{ background: var(--info); }}
  .cat-province {{ background: var(--success); }}
  .cat-regional {{ background: var(--purple); }}
  .cat-border {{ background: var(--accent); }}

  /* ===== MAIN CONTENT ===== */
  .main {{
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    background: var(--bg);
  }}

  /* ===== SUMMARY CARDS ===== */
  .summary-cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }}
  .summary-card {{
    background: var(--card);
    border-radius: var(--radius);
    padding: 20px;
    position: relative;
    overflow: hidden;
    border: 1px solid var(--border);
    transition: transform 0.2s, box-shadow 0.2s;
  }}
  .summary-card:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow);
  }}
  .summary-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: var(--radius) var(--radius) 0 0;
  }}
  .summary-card.c1::before {{ background: var(--info); }}
  .summary-card.c2::before {{ background: var(--success); }}
  .summary-card.c3::before {{ background: var(--accent); }}
  .summary-card.c4::before {{ background: var(--purple); }}
  .summary-card.c5::before {{ background: var(--q1); }}
  .summary-card-label {{
    font-size: 0.8rem;
    color: var(--text-muted);
    font-weight: 500;
    margin-bottom: 8px;
  }}
  .summary-card-value {{
    font-size: 1.8rem;
    font-weight: 700;
    color: #fff;
    line-height: 1;
  }}
  .summary-card-sub {{
    font-size: 0.78rem;
    color: var(--text-dim);
    margin-top: 4px;
  }}
  .summary-card-icon {{
    position: absolute;
    top: 16px; right: 16px;
    font-size: 1.8rem;
    opacity: 0.2;
  }}

  /* ===== SECTION TITLE ===== */
  .section-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
  }}
  .section-title {{
    font-size: 1.1rem;
    font-weight: 700;
    color: #fff;
  }}
  .section-badge {{
    background: rgba(255,255,255,0.08);
    padding: 3px 10px;
    border-radius: 50px;
    font-size: 0.78rem;
    color: var(--text-muted);
  }}
  .section-divider {{
    flex: 1;
    height: 1px;
    background: var(--border);
  }}

  /* ===== UNIT DETAIL HEADER ===== */
  .unit-detail-header {{
    background: linear-gradient(135deg, var(--card) 0%, var(--bg3) 100%);
    border-radius: var(--radius);
    padding: 24px;
    margin-bottom: 24px;
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 20px;
  }}
  .unit-detail-icon {{
    width: 60px; height: 60px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
    flex-shrink: 0;
  }}
  .unit-detail-info h2 {{
    font-size: 1.3rem;
    font-weight: 700;
    color: #fff;
  }}
  .unit-detail-info p {{
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-top: 4px;
  }}
  .unit-detail-stats {{
    margin-left: auto;
    display: flex;
    gap: 24px;
  }}
  .unit-stat {{
    text-align: center;
  }}
  .unit-stat-value {{
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent);
  }}
  .unit-stat-label {{
    font-size: 0.75rem;
    color: var(--text-dim);
    margin-top: 2px;
  }}

  /* ===== PROJECT CARDS ===== */
  .projects-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }}
  .project-card {{
    background: var(--card);
    border-radius: var(--radius);
    border: 1px solid var(--border);
    overflow: hidden;
    transition: all 0.2s;
    cursor: pointer;
  }}
  .project-card:hover {{
    border-color: rgba(245,158,11,0.3);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transform: translateY(-2px);
  }}
  .project-card.expanded {{
    grid-column: 1 / -1;
  }}
  .project-card-header {{
    padding: 16px 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255,255,255,0.03);
    border-bottom: 1px solid var(--border);
  }}
  .project-num {{
    width: 32px; height: 32px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    flex-shrink: 0;
  }}
  .project-title {{
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text);
    flex: 1;
    line-height: 1.3;
  }}
  .project-unit-tag {{
    font-size: 0.75rem;
    padding: 2px 8px;
    border-radius: 50px;
    background: rgba(255,255,255,0.08);
    color: var(--text-muted);
    white-space: nowrap;
  }}
  .project-card-body {{
    padding: 16px 18px;
  }}
  .project-target {{
    display: flex;
    align-items: baseline;
    gap: 6px;
    margin-bottom: 12px;
  }}
  .project-target-value {{
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
  }}
  .project-target-unit {{
    font-size: 0.85rem;
    color: var(--text-muted);
  }}
  .project-target-label {{
    font-size: 0.78rem;
    color: var(--text-dim);
    margin-left: auto;
  }}

  /* Quarter breakdown */
  .quarter-bars {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .quarter-row {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .quarter-label {{
    font-size: 0.75rem;
    color: var(--text-dim);
    width: 28px;
    flex-shrink: 0;
  }}
  .quarter-bar-wrap {{
    flex: 1;
    background: rgba(255,255,255,0.05);
    border-radius: 4px;
    height: 8px;
    overflow: hidden;
  }}
  .quarter-bar-fill {{
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
  }}
  .quarter-value {{
    font-size: 0.75rem;
    color: var(--text-muted);
    min-width: 50px;
    text-align: right;
  }}

  /* ===== QUARTERLY CHART AREA ===== */
  .chart-section {{
    background: var(--card);
    border-radius: var(--radius);
    border: 1px solid var(--border);
    padding: 20px;
    margin-bottom: 24px;
  }}
  .chart-container {{
    position: relative;
    height: 280px;
  }}

  /* ===== PROJECT COMPARISON TABLE ===== */
  .table-wrap {{
    background: var(--card);
    border-radius: var(--radius);
    border: 1px solid var(--border);
    overflow: hidden;
    margin-bottom: 24px;
  }}
  .data-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
  }}
  .data-table th {{
    background: var(--bg3);
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    color: var(--text-muted);
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
  }}
  .data-table th.right {{ text-align: right; }}
  .data-table td {{
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    color: var(--text);
    vertical-align: middle;
  }}
  .data-table td.right {{ text-align: right; }}
  .data-table tr:last-child td {{ border-bottom: none; }}
  .data-table tr:hover td {{ background: rgba(255,255,255,0.03); }}
  .data-table .num-cell {{
    font-variant-numeric: tabular-nums;
    font-weight: 500;
  }}
  .data-table .num-cell.accent {{ color: var(--accent); font-weight: 700; }}

  /* Mini quarter pills */
  .quarter-pills {{
    display: flex;
    gap: 4px;
  }}
  .qpill {{
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 0.72rem;
    font-weight: 600;
  }}
  .qpill.q1 {{ background: rgba(59,130,246,0.2); color: var(--q1); }}
  .qpill.q2 {{ background: rgba(16,185,129,0.2); color: var(--q2); }}
  .qpill.q3 {{ background: rgba(245,158,11,0.2); color: var(--q3); }}
  .qpill.q4 {{ background: rgba(239,68,68,0.2); color: var(--q4); }}

  /* ===== OVERALL VIEW ===== */
  .overall-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 24px;
  }}
  @media (max-width: 900px) {{
    .overall-grid {{ grid-template-columns: 1fr; }}
    .sidebar {{ width: 260px; }}
    .projects-grid {{ grid-template-columns: 1fr; }}
    .unit-detail-stats {{ display: none; }}
  }}
  @media (max-width: 640px) {{
    .layout {{ flex-direction: column; }}
    .sidebar {{ width: 100%; height: auto; position: relative; }}
    .header {{ padding: 16px; }}
    .header-badge {{ display: none; }}
  }}

  /* ===== EMPTY STATE ===== */
  .empty-state {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
    color: var(--text-dim);
    gap: 12px;
  }}
  .empty-state .icon {{ font-size: 3rem; opacity: 0.4; }}
  .empty-state p {{ font-size: 0.95rem; }}

  /* ===== SCROLLBAR ===== */
  .main::-webkit-scrollbar {{ width: 6px; }}
  .main::-webkit-scrollbar-track {{ background: transparent; }}
  .main::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 4px; }}

  /* ===== TOOLTIP ===== */
  .tooltip {{
    position: relative;
  }}
  .tooltip:hover::after {{
    content: attr(data-tip);
    position: absolute;
    bottom: 100%; left: 50%;
    transform: translateX(-50%);
    background: rgba(0,0,0,0.9);
    color: #fff;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    white-space: nowrap;
    pointer-events: none;
    z-index: 100;
  }}

  /* ===== TAB BUTTONS ===== */
  .view-tabs {{
    display: flex;
    gap: 0;
    background: var(--bg3);
    border-radius: var(--radius-sm);
    padding: 4px;
    margin-bottom: 24px;
    width: fit-content;
  }}
  .view-tab {{
    padding: 8px 20px;
    border-radius: 6px;
    font-size: 0.88rem;
    cursor: pointer;
    border: none;
    background: transparent;
    color: var(--text-muted);
    font-family: 'Sarabun', sans-serif;
    font-weight: 500;
    transition: all 0.2s;
  }}
  .view-tab.active {{
    background: var(--primary-light);
    color: #fff;
    box-shadow: 0 2px 8px rgba(35,85,160,0.4);
  }}
  .view-tab:hover:not(.active) {{ color: var(--text); }}

  /* ===== MONTH DETAIL TABLE ===== */
  .month-table-wrap {{
    background: var(--card);
    border-radius: var(--radius);
    border: 1px solid var(--border);
    overflow: auto;
    margin-bottom: 24px;
  }}
  .month-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
    min-width: 700px;
  }}
  .month-table th {{
    background: var(--bg3);
    padding: 8px 12px;
    text-align: center;
    font-weight: 600;
    color: var(--text-muted);
    font-size: 0.75rem;
    border-bottom: 1px solid var(--border);
    border-right: 1px solid rgba(255,255,255,0.04);
  }}
  .month-table th.left {{ text-align: left; }}
  .month-table td {{
    padding: 8px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.04);
    text-align: center;
    font-variant-numeric: tabular-nums;
  }}
  .month-table td.left {{ text-align: left; color: var(--text); }}
  .month-table td.qtotal {{
    font-weight: 700;
    background: rgba(255,255,255,0.04);
  }}
  .month-table td.qtotal.q1 {{ color: var(--q1); }}
  .month-table td.qtotal.q2 {{ color: var(--q2); }}
  .month-table td.qtotal.q3 {{ color: var(--q3); }}
  .month-table td.qtotal.q4 {{ color: var(--q4); }}
  .month-table .thead-q1 {{ background: rgba(59,130,246,0.12); }}
  .month-table .thead-q2 {{ background: rgba(16,185,129,0.12); }}
  .month-table .thead-q3 {{ background: rgba(245,158,11,0.12); }}
  .month-table .thead-q4 {{ background: rgba(239,68,68,0.12); }}
  .month-table tr:hover td {{ background: rgba(255,255,255,0.03); }}

  /* Zero values */
  .zero {{ color: var(--text-dim); }}

  /* ===== LOADING ===== */
  .loading-overlay {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(13,27,46,0.8);
    z-index: 999;
    align-items: center;
    justify-content: center;
  }}
  .spinner {{
    width: 40px; height: 40px;
    border: 3px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}

  /* Animated number */
  @keyframes countUp {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}
  .count-anim {{ animation: countUp 0.4s ease forwards; }}

</style>
</head>
<body>

<!-- HEADER -->
<header class="header">
  <div class="header-icon">📊</div>
  <div class="header-text">
    <h1>Dashboard จัดสรรเป้าหมายการดำเนินงาน</h1>
    <p>กรมการจัดหางาน • ประจำปีงบประมาณ พ.ศ. 2570</p>
  </div>
  <div class="header-badge">ข้อมูล ณ 29 ก.ย. 2569</div>
</header>

<!-- LAYOUT -->
<div class="layout">

  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="sidebar-header">
      <div class="sidebar-title">หน่วยงาน</div>
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchBox" placeholder="ค้นหาหน่วยงาน..." oninput="filterUnits()">
      </div>
      <div class="filter-tabs">
        <button class="filter-tab active" id="tab-all" onclick="setFilter('all')">ทั้งหมด</button>
        <button class="filter-tab" id="tab-ส่วนกลาง" onclick="setFilter('ส่วนกลาง')">ส่วนกลาง</button>
        <button class="filter-tab" id="tab-จังหวัด" onclick="setFilter('จังหวัด')">จังหวัด</button>
        <button class="filter-tab" id="tab-ศูนย์ภาค" onclick="setFilter('ศูนย์ภาค')">ศูนย์ภาค</button>
        <button class="filter-tab" id="tab-ด่าน" onclick="setFilter('ด่าน')">ด่าน</button>
      </div>
    </div>
    <div class="unit-list" id="unitList"></div>
  </aside>

  <!-- MAIN -->
  <main class="main" id="mainContent">
    <!-- Content rendered by JS -->
  </main>

</div>

<div class="loading-overlay" id="loadingOverlay">
  <div class="spinner"></div>
</div>

<script>
// ===== DATA =====
const DASHBOARD_DATA = {data_json};

// ===== STATE =====
let state = {{
  selectedUnit: null,
  filter: 'all',
  search: '',
  view: 'detail', // 'detail' | 'monthly'
  chartInstance: null,
}};

// ===== COLOR MAPS =====
const catColors = {{
  'ส่วนกลาง': 'cat-central',
  'จังหวัด': 'cat-province',
  'ศูนย์ภาค': 'cat-regional',
  'ด่าน': 'cat-border',
}};
const catIcons = {{
  'ส่วนกลาง': '🏛️',
  'จังหวัด': '🏙️',
  'ศูนย์ภาค': '🗺️',
  'ด่าน': '🚧',
}};
const projColors = [
  '#3b82f6','#10b981','#f59e0b','#ef4444','#8b5cf6',
  '#06b6d4','#f97316','#84cc16','#ec4899','#14b8a6','#6366f1'
];

// ===== HELPERS =====
const fmt = (n) => n ? Number(n).toLocaleString('th-TH') : '0';
const fmtV = (n) => Number(n).toLocaleString('th-TH');

function getUnitTotal(unit) {{
  return unit.projects.reduce((s, p) => s + (p.target || 0), 0);
}}

function getUnitQTotal(unit, q) {{
  return unit.projects.reduce((s, p) => s + (p[q]?.total || 0), 0);
}}

// ===== UNIT LIST =====
function renderUnitList() {{
  const list = document.getElementById('unitList');
  const search = state.search.toLowerCase();
  const filter = state.filter;

  const units = DASHBOARD_DATA.units.filter(u => {{
    const matchCat = filter === 'all' || u.category === filter;
    const matchSearch = !search || u.name.toLowerCase().includes(search) || u.sheet.toLowerCase().includes(search);
    return matchCat && matchSearch;
  }});

  if (units.length === 0) {{
    list.innerHTML = `<div class="empty-state"><div class="icon">🔍</div><p>ไม่พบหน่วยงาน</p></div>`;
    return;
  }}

  list.innerHTML = units.map(u => {{
    const colorClass = catColors[u.category] || 'cat-province';
    const isActive = state.selectedUnit === u.sheet;
    const total = getUnitTotal(u);
    return `<div class="unit-item ${{isActive ? 'active' : ''}}" onclick="selectUnit('${{u.sheet.replace(/'/g,"\\'")}}')" id="unit-${{u.sheet.replace(/[^a-zA-Z0-9]/g,'_')}}">
      <div class="unit-badge ${{colorClass}}"></div>
      <div class="unit-name">${{u.name}}</div>
      <div class="unit-count">${{fmt(total)}}</div>
    </div>`;
  }}).join('');
}}

function setFilter(cat) {{
  state.filter = cat;
  document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('tab-' + cat)?.classList.add('active');
  renderUnitList();
}}

function filterUnits() {{
  state.search = document.getElementById('searchBox').value;
  renderUnitList();
}}

// ===== SELECT UNIT =====
function selectUnit(sheetName) {{
  state.selectedUnit = sheetName;
  renderUnitList();
  renderMain();
}}

// ===== MAIN RENDER =====
function renderMain() {{
  const main = document.getElementById('mainContent');

  if (!state.selectedUnit) {{
    renderOverview(main);
    return;
  }}

  const unit = DASHBOARD_DATA.units.find(u => u.sheet === state.selectedUnit);
  if (!unit) return;

  const totalTarget = getUnitTotal(unit);
  const q1Total = getUnitQTotal(unit, 'q1');
  const q2Total = getUnitQTotal(unit, 'q2');
  const q3Total = getUnitQTotal(unit, 'q3');
  const q4Total = getUnitQTotal(unit, 'q4');
  const projCount = unit.projects.filter(p => p.target > 0).length;

  const colorClass = catColors[unit.category] || 'cat-province';
  const catIcon = catIcons[unit.category] || '🏢';

  main.innerHTML = `
    <!-- Unit Header -->
    <div class="unit-detail-header">
      <div class="unit-detail-icon" style="background:linear-gradient(135deg,${{getColorForCat(unit.category)}}33,${{getColorForCat(unit.category)}}11);border:1px solid ${{getColorForCat(unit.category)}}33">
        <span style="font-size:1.6rem">${{catIcon}}</span>
      </div>
      <div class="unit-detail-info">
        <h2>${{unit.name}}</h2>
        <p>${{unit.category}} • ${{projCount}} โครงการที่มีเป้าหมาย</p>
      </div>
      <div class="unit-detail-stats">
        <div class="unit-stat">
          <div class="unit-stat-value count-anim">${{fmtV(totalTarget)}}</div>
          <div class="unit-stat-label">เป้าหมายรวม</div>
        </div>
        <div class="unit-stat">
          <div class="unit-stat-value count-anim" style="color:var(--q1)">${{fmtV(q1Total)}}</div>
          <div class="unit-stat-label">ไตรมาส 1</div>
        </div>
        <div class="unit-stat">
          <div class="unit-stat-value count-anim" style="color:var(--q2)">${{fmtV(q2Total)}}</div>
          <div class="unit-stat-label">ไตรมาส 2</div>
        </div>
        <div class="unit-stat">
          <div class="unit-stat-value count-anim" style="color:var(--q3)">${{fmtV(q3Total)}}</div>
          <div class="unit-stat-label">ไตรมาส 3</div>
        </div>
        <div class="unit-stat">
          <div class="unit-stat-value count-anim" style="color:var(--q4)">${{fmtV(q4Total)}}</div>
          <div class="unit-stat-label">ไตรมาส 4</div>
        </div>
      </div>
    </div>

    <!-- View Tabs -->
    <div class="view-tabs">
      <button class="view-tab ${{state.view === 'detail' ? 'active' : ''}}" onclick="setView('detail')">📋 รายโครงการ</button>
      <button class="view-tab ${{state.view === 'monthly' ? 'active' : ''}}" onclick="setView('monthly')">📅 รายเดือน</button>
    </div>

    <!-- Chart -->
    <div class="chart-section">
      <div class="section-header">
        <div class="section-title">เป้าหมายรายไตรมาส</div>
        <div class="section-divider"></div>
      </div>
      <div class="chart-container">
        <canvas id="mainChart"></canvas>
      </div>
    </div>

    <!-- Content by view -->
    <div id="viewContent"></div>
  `;

  // Render chart
  renderChart(unit);

  // Render view
  if (state.view === 'detail') {{
    renderDetailView(unit);
  }} else {{
    renderMonthlyView(unit);
  }}
}}

function setView(v) {{
  state.view = v;
  const unit = DASHBOARD_DATA.units.find(u => u.sheet === state.selectedUnit);
  if (!unit) return;

  document.querySelectorAll('.view-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.view-tab').forEach(t => {{
    if ((t.textContent.includes('รายโครงการ') && v === 'detail') ||
        (t.textContent.includes('รายเดือน') && v === 'monthly')) {{
      t.classList.add('active');
    }}
  }});

  if (v === 'detail') renderDetailView(unit);
  else renderMonthlyView(unit);
}}

function getColorForCat(cat) {{
  const m = {{ 'ส่วนกลาง': '#3b82f6', 'จังหวัด': '#10b981', 'ศูนย์ภาค': '#8b5cf6', 'ด่าน': '#f59e0b' }};
  return m[cat] || '#3b82f6';
}}

// ===== CHART =====
function renderChart(unit) {{
  if (state.chartInstance) {{ state.chartInstance.destroy(); state.chartInstance = null; }}
  const ctx = document.getElementById('mainChart');
  if (!ctx) return;

  const activeProjects = unit.projects.filter(p => p.target > 0);
  const labels = activeProjects.map(p => `โครงการ ${{p.num}}`);

  state.chartInstance = new Chart(ctx, {{
    type: 'bar',
    data: {{
      labels: labels,
      datasets: [
        {{
          label: 'ไตรมาส 1 (ต.ค.-ธ.ค.)',
          data: activeProjects.map(p => p.q1.total),
          backgroundColor: 'rgba(59,130,246,0.7)',
          borderColor: 'rgba(59,130,246,1)',
          borderWidth: 1,
          borderRadius: 4,
        }},
        {{
          label: 'ไตรมาส 2 (ม.ค.-มี.ค.)',
          data: activeProjects.map(p => p.q2.total),
          backgroundColor: 'rgba(16,185,129,0.7)',
          borderColor: 'rgba(16,185,129,1)',
          borderWidth: 1,
          borderRadius: 4,
        }},
        {{
          label: 'ไตรมาส 3 (เม.ย.-มิ.ย.)',
          data: activeProjects.map(p => p.q3.total),
          backgroundColor: 'rgba(245,158,11,0.7)',
          borderColor: 'rgba(245,158,11,1)',
          borderWidth: 1,
          borderRadius: 4,
        }},
        {{
          label: 'ไตรมาส 4 (ก.ค.-ก.ย.)',
          data: activeProjects.map(p => p.q4.total),
          backgroundColor: 'rgba(239,68,68,0.7)',
          borderColor: 'rgba(239,68,68,1)',
          borderWidth: 1,
          borderRadius: 4,
        }},
      ]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      plugins: {{
        legend: {{
          labels: {{ color: '#94a3b8', font: {{ family: 'Sarabun', size: 12 }} }}
        }},
        tooltip: {{
          callbacks: {{
            title: (items) => {{
              const idx = items[0].dataIndex;
              return activeProjects[idx].name.substring(0, 40) + (activeProjects[idx].name.length > 40 ? '...' : '');
            }},
            label: (item) => `${{item.dataset.label}}: ${{Number(item.raw).toLocaleString('th-TH')}} ${{activeProjects[item.dataIndex].unit}}`
          }},
          bodyFont: {{ family: 'Sarabun' }},
          titleFont: {{ family: 'Sarabun' }},
        }}
      }},
      scales: {{
        x: {{
          stacked: false,
          ticks: {{ color: '#64748b', font: {{ family: 'Sarabun', size: 11 }} }},
          grid: {{ color: 'rgba(255,255,255,0.04)' }},
        }},
        y: {{
          ticks: {{
            color: '#64748b',
            font: {{ family: 'Sarabun', size: 11 }},
            callback: (v) => Number(v).toLocaleString('th-TH')
          }},
          grid: {{ color: 'rgba(255,255,255,0.06)' }},
        }}
      }}
    }}
  }});
}}

// ===== DETAIL VIEW (PROJECT CARDS) =====
function renderDetailView(unit) {{
  const container = document.getElementById('viewContent');
  const activeProjects = unit.projects.filter(p => p.target > 0);
  const allProjects = unit.projects;

  const sectionHeader = `
    <div class="section-header" style="margin-bottom:16px">
      <div class="section-title">รายโครงการ</div>
      <div class="section-badge">${{allProjects.length}} โครงการ • ${{activeProjects.length}} ที่มีเป้าหมาย</div>
      <div class="section-divider"></div>
    </div>
  `;

  const cards = allProjects.map((p, idx) => {{
    const color = projColors[idx % projColors.length];
    const maxQ = Math.max(p.q1.total, p.q2.total, p.q3.total, p.q4.total, 1);
    const hasData = p.target > 0;
    return `
      <div class="project-card">
        <div class="project-card-header">
          <div class="project-num" style="background:${{color}}22;color:${{color}}">${{p.num}}</div>
          <div class="project-title">${{p.name.length > 60 ? p.name.substring(0,57)+'...' : p.name}}</div>
          ${{p.unit ? `<div class="project-unit-tag">${{p.unit}}</div>` : ''}}
        </div>
        <div class="project-card-body">
          <div class="project-target">
            <div class="project-target-value" style="color:${{color}}">${{hasData ? fmtV(p.target) : '-'}}</div>
            <div class="project-target-unit">${{p.unit || ''}}</div>
            <div class="project-target-label">เป้าหมายปี 2570</div>
          </div>
          ${{hasData ? `
          <div class="quarter-bars">
            ${{renderQBar('ไตรมาส 1', p.q1.total, maxQ, 'var(--q1)')}}
            ${{renderQBar('ไตรมาส 2', p.q2.total, maxQ, 'var(--q2)')}}
            ${{renderQBar('ไตรมาส 3', p.q3.total, maxQ, 'var(--q3)')}}
            ${{renderQBar('ไตรมาส 4', p.q4.total, maxQ, 'var(--q4)')}}
          </div>
          ` : `<div style="color:var(--text-dim);font-size:0.82rem;text-align:center;padding:8px">ไม่มีการจัดสรรเป้าหมาย</div>`}}
        </div>
      </div>
    `;
  }}).join('');

  container.innerHTML = sectionHeader + `<div class="projects-grid">${{cards}}</div>`;
}}

function renderQBar(label, value, max, color) {{
  const pct = max > 0 ? Math.min((value / max) * 100, 100) : 0;
  const shortLabel = label.replace('ไตรมาส ', 'Q');
  return `
    <div class="quarter-row">
      <div class="quarter-label">${{shortLabel}}</div>
      <div class="quarter-bar-wrap">
        <div class="quarter-bar-fill" style="width:${{pct}}%;background:${{color}}"></div>
      </div>
      <div class="quarter-value" style="color:${{color}}">${{value > 0 ? fmtV(value) : '-'}}</div>
    </div>
  `;
}}

// ===== MONTHLY VIEW (TABLE) =====
function renderMonthlyView(unit) {{
  const container = document.getElementById('viewContent');

  const months = ['ต.ค.', 'พ.ย.', 'ธ.ค.', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.'];
  const monthKeys = [
    ['q1','oct'], ['q1','nov'], ['q1','dec'],
    ['q2','jan'], ['q2','feb'], ['q2','mar'],
    ['q3','apr'], ['q3','may'], ['q3','jun'],
    ['q4','jul'], ['q4','aug'], ['q4','sep'],
  ];

  const headerRow1 = `
    <tr>
      <th class="left" rowspan="2" style="min-width:200px">โครงการ</th>
      <th class="left" rowspan="2">หน่วย</th>
      <th rowspan="2">เป้าหมาย<br>ปี 2570</th>
      <th colspan="4" class="thead-q1">ไตรมาส 1 (ปี 2569)</th>
      <th colspan="4" class="thead-q2">ไตรมาส 2</th>
      <th colspan="4" class="thead-q3">ไตรมาส 3</th>
      <th colspan="4" class="thead-q4">ไตรมาส 4</th>
    </tr>
    <tr>
      <th class="thead-q1">ต.ค.</th><th class="thead-q1">พ.ย.</th><th class="thead-q1">ธ.ค.</th><th class="thead-q1" style="font-weight:700">รวม Q1</th>
      <th class="thead-q2">ม.ค.</th><th class="thead-q2">ก.พ.</th><th class="thead-q2">มี.ค.</th><th class="thead-q2" style="font-weight:700">รวม Q2</th>
      <th class="thead-q3">เม.ย.</th><th class="thead-q3">พ.ค.</th><th class="thead-q3">มิ.ย.</th><th class="thead-q3" style="font-weight:700">รวม Q3</th>
      <th class="thead-q4">ก.ค.</th><th class="thead-q4">ส.ค.</th><th class="thead-q4">ก.ย.</th><th class="thead-q4" style="font-weight:700">รวม Q4</th>
    </tr>
  `;

  const dataRows = unit.projects.map((p, idx) => {{
    const color = projColors[idx % projColors.length];
    const cell = (v, cls='') => v > 0 ? `<td class="${{cls}}">${{fmtV(v)}}</td>` : `<td class="zero ${{cls}}">-</td>`;
    return `<tr>
      <td class="left"><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${{color}};margin-right:8px;flex-shrink:0"></span>${{p.name.length > 45 ? p.name.substring(0,42)+'...' : p.name}}</td>
      <td class="left" style="color:var(--text-muted)">${{p.unit || ''}}</td>
      <td style="font-weight:700;color:var(--accent)">${{p.target > 0 ? fmtV(p.target) : '-'}}</td>
      ${{cell(p.q1.oct)}}${{cell(p.q1.nov)}}${{cell(p.q1.dec)}}${{cell(p.q1.total, 'qtotal q1')}}
      ${{cell(p.q2.jan)}}${{cell(p.q2.feb)}}${{cell(p.q2.mar)}}${{cell(p.q2.total, 'qtotal q2')}}
      ${{cell(p.q3.apr)}}${{cell(p.q3.may)}}${{cell(p.q3.jun)}}${{cell(p.q3.total, 'qtotal q3')}}
      ${{cell(p.q4.jul)}}${{cell(p.q4.aug)}}${{cell(p.q4.sep)}}${{cell(p.q4.total, 'qtotal q4')}}
    </tr>`;
  }}).join('');

  // Total row
  const totals = {{
    target: unit.projects.reduce((s,p) => s+p.target, 0),
    q1: {{ oct: 0, nov: 0, dec: 0, total: 0 }},
    q2: {{ jan: 0, feb: 0, mar: 0, total: 0 }},
    q3: {{ apr: 0, may: 0, jun: 0, total: 0 }},
    q4: {{ jul: 0, aug: 0, sep: 0, total: 0 }},
  }};
  unit.projects.forEach(p => {{
    ['oct','nov','dec','total'].forEach(k => totals.q1[k] = (totals.q1[k]||0) + (p.q1[k]||0));
    ['jan','feb','mar','total'].forEach(k => totals.q2[k] = (totals.q2[k]||0) + (p.q2[k]||0));
    ['apr','may','jun','total'].forEach(k => totals.q3[k] = (totals.q3[k]||0) + (p.q3[k]||0));
    ['jul','aug','sep','total'].forEach(k => totals.q4[k] = (totals.q4[k]||0) + (p.q4[k]||0));
  }});

  const tcell = (v, cls='') => `<td style="font-weight:700;color:${{v>0?'#e2e8f0':'var(--text-dim)'}}" class="${{cls}}">${{v>0?fmtV(v):'-'}}</td>`;
  const totalRow = `<tr style="background:rgba(255,255,255,0.06);font-weight:700">
    <td class="left" style="font-weight:700;color:#fff">รวมทั้งหมด</td>
    <td></td>
    <td style="font-weight:700;color:var(--accent)">${{fmtV(totals.target)}}</td>
    ${{tcell(totals.q1.oct)}}${{tcell(totals.q1.nov)}}${{tcell(totals.q1.dec)}}${{tcell(totals.q1.total,'qtotal q1')}}
    ${{tcell(totals.q2.jan)}}${{tcell(totals.q2.feb)}}${{tcell(totals.q2.mar)}}${{tcell(totals.q2.total,'qtotal q2')}}
    ${{tcell(totals.q3.apr)}}${{tcell(totals.q3.may)}}${{tcell(totals.q3.jun)}}${{tcell(totals.q3.total,'qtotal q3')}}
    ${{tcell(totals.q4.jul)}}${{tcell(totals.q4.aug)}}${{tcell(totals.q4.sep)}}${{tcell(totals.q4.total,'qtotal q4')}}
  </tr>`;

  container.innerHTML = `
    <div class="section-header" style="margin-bottom:16px">
      <div class="section-title">ตารางเป้าหมายรายเดือน</div>
      <div class="section-divider"></div>
    </div>
    <div class="month-table-wrap">
      <table class="month-table">
        <thead>${{headerRow1}}</thead>
        <tbody>${{dataRows}}${{totalRow}}</tbody>
      </table>
    </div>
  `;
}}

// ===== OVERVIEW =====
function renderOverview(main) {{
  const units = DASHBOARD_DATA.units;
  const projects = DASHBOARD_DATA.projects;

  // Compute grand totals per project
  const projTotals = {{}};
  projects.forEach(p => projTotals[p.num] = {{ target: 0, q1: 0, q2: 0, q3: 0, q4: 0 }});
  units.forEach(u => {{
    u.projects.forEach(p => {{
      if (!projTotals[p.num]) return;
      projTotals[p.num].target += p.target || 0;
      projTotals[p.num].q1 += p.q1?.total || 0;
      projTotals[p.num].q2 += p.q2?.total || 0;
      projTotals[p.num].q3 += p.q3?.total || 0;
      projTotals[p.num].q4 += p.q4?.total || 0;
    }});
  }});

  const grandTotal = Object.values(projTotals).reduce((s,p) => s+p.target, 0);
  const catCount = {{}};
  units.forEach(u => catCount[u.category] = (catCount[u.category]||0)+1);

  main.innerHTML = `
    <!-- Summary Cards -->
    <div class="summary-cards">
      <div class="summary-card c1">
        <div class="summary-card-icon">🏛️</div>
        <div class="summary-card-label">หน่วยงานทั้งหมด</div>
        <div class="summary-card-value">${{fmtV(units.length)}}</div>
        <div class="summary-card-sub">หน่วยงาน</div>
      </div>
      <div class="summary-card c2">
        <div class="summary-card-icon">📋</div>
        <div class="summary-card-label">โครงการ</div>
        <div class="summary-card-value">${{projects.length}}</div>
        <div class="summary-card-sub">โครงการ</div>
      </div>
      <div class="summary-card c3">
        <div class="summary-card-icon">🎯</div>
        <div class="summary-card-label">เป้าหมายรวมทั้งกรม</div>
        <div class="summary-card-value">${{fmtV(grandTotal)}}</div>
        <div class="summary-card-sub">รวมทุกโครงการทุกหน่วยงาน</div>
      </div>
      <div class="summary-card c4">
        <div class="summary-card-icon">🗺️</div>
        <div class="summary-card-label">จังหวัด</div>
        <div class="summary-card-value">${{catCount['จังหวัด'] || 0}}</div>
        <div class="summary-card-sub">สำนักงานจัดหางานจังหวัด</div>
      </div>
      <div class="summary-card c5">
        <div class="summary-card-icon">🚧</div>
        <div class="summary-card-label">ด่าน</div>
        <div class="summary-card-value">${{catCount['ด่าน'] || 0}}</div>
        <div class="summary-card-sub">ด่านตรวจคนหางาน</div>
      </div>
    </div>

    <!-- Overview chart -->
    <div class="chart-section" style="margin-bottom:24px">
      <div class="section-header">
        <div class="section-title">เป้าหมายรวมทั้งกรม รายโครงการ</div>
        <div class="section-divider"></div>
      </div>
      <div class="chart-container">
        <canvas id="overviewChart"></canvas>
      </div>
    </div>

    <!-- Project summary table -->
    <div class="section-header">
      <div class="section-title">สรุปเป้าหมายรายโครงการ</div>
      <div class="section-divider"></div>
    </div>
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>#</th>
            <th>ชื่อโครงการ</th>
            <th class="right">เป้าหมายรวม</th>
            <th class="right">Q1</th>
            <th class="right">Q2</th>
            <th class="right">Q3</th>
            <th class="right">Q4</th>
          </tr>
        </thead>
        <tbody>
          ${{projects.map((p, idx) => {{
            const t = projTotals[p.num];
            const color = projColors[idx % projColors.length];
            return `<tr>
              <td><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${{color}};margin-right:4px"></span>${{p.num}}</td>
              <td>${{p.name.length > 55 ? p.name.substring(0,52)+'...' : p.name}}</td>
              <td class="right num-cell accent">${{fmtV(t.target)}}</td>
              <td class="right num-cell" style="color:var(--q1)">${{fmtV(t.q1)}}</td>
              <td class="right num-cell" style="color:var(--q2)">${{fmtV(t.q2)}}</td>
              <td class="right num-cell" style="color:var(--q3)">${{fmtV(t.q3)}}</td>
              <td class="right num-cell" style="color:var(--q4)">${{fmtV(t.q4)}}</td>
            </tr>`;
          }}).join('')}}
        </tbody>
        <tfoot>
          <tr style="background:rgba(255,255,255,0.06)">
            <td colspan="2" style="font-weight:700;color:#fff;padding:10px 14px">รวมทั้งหมด</td>
            <td class="right" style="font-weight:700;color:var(--accent)">${{fmtV(grandTotal)}}</td>
            <td class="right" style="font-weight:700;color:var(--q1)">${{fmtV(Object.values(projTotals).reduce((s,p)=>s+p.q1,0))}}</td>
            <td class="right" style="font-weight:700;color:var(--q2)">${{fmtV(Object.values(projTotals).reduce((s,p)=>s+p.q2,0))}}</td>
            <td class="right" style="font-weight:700;color:var(--q3)">${{fmtV(Object.values(projTotals).reduce((s,p)=>s+p.q3,0))}}</td>
            <td class="right" style="font-weight:700;color:var(--q4)">${{fmtV(Object.values(projTotals).reduce((s,p)=>s+p.q4,0))}}</td>
          </tr>
        </tfoot>
      </table>
    </div>

    <div style="text-align:center;color:var(--text-dim);font-size:0.82rem;padding:16px 0">
      👈 เลือกหน่วยงานจากรายการด้านซ้าย เพื่อดูรายละเอียด
    </div>
  `;

  // Overview chart
  setTimeout(() => {{
    if (state.chartInstance) {{ state.chartInstance.destroy(); state.chartInstance = null; }}
    const ctx = document.getElementById('overviewChart');
    if (!ctx) return;

    state.chartInstance = new Chart(ctx, {{
      type: 'bar',
      data: {{
        labels: projects.map(p => `โครงการ ${{p.num}}`),
        datasets: [
          {{
            label: 'Q1',
            data: projects.map(p => projTotals[p.num].q1),
            backgroundColor: 'rgba(59,130,246,0.7)',
            borderRadius: 4,
          }},
          {{
            label: 'Q2',
            data: projects.map(p => projTotals[p.num].q2),
            backgroundColor: 'rgba(16,185,129,0.7)',
            borderRadius: 4,
          }},
          {{
            label: 'Q3',
            data: projects.map(p => projTotals[p.num].q3),
            backgroundColor: 'rgba(245,158,11,0.7)',
            borderRadius: 4,
          }},
          {{
            label: 'Q4',
            data: projects.map(p => projTotals[p.num].q4),
            backgroundColor: 'rgba(239,68,68,0.7)',
            borderRadius: 4,
          }},
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ labels: {{ color: '#94a3b8', font: {{ family: 'Sarabun' }} }} }},
          tooltip: {{
            callbacks: {{
              title: (items) => projects[items[0].dataIndex]?.name || '',
            }},
            bodyFont: {{ family: 'Sarabun' }},
            titleFont: {{ family: 'Sarabun' }},
          }}
        }},
        scales: {{
          x: {{ ticks: {{ color: '#64748b', font: {{ family: 'Sarabun' }} }}, grid: {{ color: 'rgba(255,255,255,0.04)' }} }},
          y: {{ ticks: {{ color: '#64748b', callback: (v) => Number(v).toLocaleString('th-TH'), font: {{ family: 'Sarabun' }} }}, grid: {{ color: 'rgba(255,255,255,0.06)' }} }}
        }}
      }}
    }});
  }}, 50);
}}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {{
  renderUnitList();
  renderMain();
}});
</script>
</body>
</html>
"""

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Dashboard saved to: {output_path}")
    print(f"File size: {len(html):,} bytes")

if __name__ == '__main__':
    build_dashboard()
