#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Dashboard HTML v3
Fixes: monthly tab, sidebar scroll, table view, project allocation page
"""
import json, os

def build():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard_data.json')
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    dj = json.dumps(data, ensure_ascii=False)

    html = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard จัดสรรเป้าหมายการดำเนินงาน ปีงบประมาณ พ.ศ. 2570</title>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root {
  --sb:240px; --sb-c:62px; --th:56px;
  --dark:#1e2139; --dark2:#262b47; --purple:#6c63ff; --purple2:#8b85ff;
  --amber:#f59e0b; --teal:#14b8a6; --rose:#f43f5e; --blue:#3b82f6;
  --green:#10b981; --orange:#f97316;
  --page:#f0f4f8; --card:#fff; --border:#e2e8f0;
  --text:#1e2139; --text2:#4a5568; --muted:#8896a4; --light:#b0bec5;
  --r:12px; --shadow:0 2px 12px rgba(0,0,0,.07); --shadow2:0 8px 28px rgba(0,0,0,.12);
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Sarabun',sans-serif;background:var(--page);color:var(--text2);display:flex;min-height:100vh}

/* SIDEBAR */
.sidebar{width:var(--sb);background:var(--dark);position:fixed;top:0;left:0;bottom:0;
  display:flex;flex-direction:column;z-index:200;transition:width .3s;overflow:hidden}
.sidebar.mini{width:var(--sb-c)}
.sidebar.resizing, .wrapper.resizing{transition:none !important}
.sb-resizer{position:absolute;top:0;right:0;width:6px;height:100%;cursor:col-resize;z-index:250;transition:background .2s}
.sb-resizer:hover, .sb-resizer.active{background:var(--purple)}

.sb-brand{height:var(--th);display:flex;align-items:center;gap:10px;padding:0 14px;
  border-bottom:1px solid rgba(255,255,255,.06);flex-shrink:0}
.sb-logo{width:34px;height:34px;border-radius:9px;
  background:linear-gradient(135deg,var(--purple),var(--purple2));
  display:flex;align-items:center;justify-content:center;
  color:#fff;font-size:.95rem;flex-shrink:0;box-shadow:0 4px 12px rgba(108,99,255,.4)}
.sb-txt{overflow:hidden;white-space:nowrap}
.sb-title{font-size:.88rem;font-weight:700;color:#fff}
.sb-sub{font-size:.62rem;color:rgba(255,255,255,.4);margin-top:1px}
.sidebar.mini .sb-txt{display:none}

.sb-toggle{margin:8px 10px;height:30px;border-radius:8px;background:rgba(255,255,255,.06);
  border:none;color:rgba(255,255,255,.55);cursor:pointer;
  display:flex;align-items:center;justify-content:center;gap:6px;
  font-size:.78rem;font-family:'Sarabun',sans-serif;transition:all .2s;flex-shrink:0;white-space:nowrap}
.sb-toggle:hover{background:rgba(255,255,255,.12);color:#fff}
.sidebar.mini .sb-toggle{justify-content:center}
.sidebar.mini .sb-toggle .tl{display:none}

/* Nav scroll */
.sb-nav{flex:1;padding:6px 8px;overflow-y:auto;overflow-x:hidden}
.sb-nav::-webkit-scrollbar{width:3px}
.sb-nav::-webkit-scrollbar-thumb{background:rgba(255,255,255,.15);border-radius:3px}

.sb-lbl{font-size:.58rem;text-transform:uppercase;letter-spacing:.1em;
  color:rgba(255,255,255,.22);padding:8px 8px 3px;white-space:nowrap}
.sidebar.mini .sb-lbl{visibility:hidden;height:0;padding:0;margin:0}

.sb-item{display:flex;align-items:center;gap:9px;padding:8px 9px;border-radius:9px;
  cursor:pointer;color:rgba(255,255,255,.62);transition:all .2s;
  margin-bottom:2px;white-space:nowrap;overflow:hidden;border:1px solid transparent;position:relative}
.sb-item:hover{background:rgba(255,255,255,.07);color:#fff}
.sb-item.active{background:linear-gradient(135deg,var(--purple),var(--purple2));
  color:#fff;box-shadow:0 4px 14px rgba(108,99,255,.35)}
.sb-ico{width:30px;height:30px;border-radius:8px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:.85rem;
  background:rgba(255,255,255,.07);transition:background .2s}
.sb-item.active .sb-ico{background:rgba(255,255,255,.2)}
.sb-item:hover .sb-ico{background:rgba(255,255,255,.12)}
.sb-lname{font-size:.85rem;font-weight:500;flex:1}
.sb-cnt{background:rgba(255,255,255,.16);border-radius:50px;
  padding:1px 7px;font-size:.68rem;font-weight:700;flex-shrink:0}
.sb-item.active .sb-cnt{background:rgba(255,255,255,.25)}

.sidebar.mini .sb-item{justify-content:center;padding:8px 0}
.sidebar.mini .sb-lname,.sidebar.mini .sb-cnt{display:none}
.sidebar.mini .sb-item::after{content:attr(data-tip);position:absolute;
  left:calc(var(--sb-c) + 6px);top:50%;transform:translateY(-50%);
  background:#1e2139;color:#fff;padding:5px 11px;border-radius:7px;
  font-size:.8rem;white-space:nowrap;pointer-events:none;opacity:0;
  box-shadow:0 4px 14px rgba(0,0,0,.3);z-index:999;transition:opacity .15s}
.sidebar.mini .sb-item:hover::after{opacity:1}

/* Sub-menu (expandable in sidebar for units) */
.sb-sub-menu{overflow:hidden;transition:max-height .3s ease;max-height:0}
.sb-sub-menu.open{max-height:2000px}
.sb-sub-item{display:flex;align-items:center;gap:8px;padding:6px 9px 6px 20px;
  border-radius:8px;cursor:pointer;color:rgba(255,255,255,.5);
  transition:all .2s;font-size:.8rem;margin-bottom:1px;white-space:nowrap;overflow:hidden}
.sb-sub-item:hover{background:rgba(255,255,255,.06);color:#fff}
.sb-sub-item.active{color:var(--purple2);font-weight:600}
.sb-sub-item .dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;background:currentColor;opacity:.6}
.sidebar.mini .sb-sub-menu{display:none}

/* WRAPPER */
.wrapper{margin-left:var(--sb);flex:1;display:flex;flex-direction:column;
  transition:margin-left .3s;min-height:100vh}
body.mini-mode .wrapper{margin-left:var(--sb-c)}

/* TOPBAR */
.topbar{height:var(--th);background:var(--card);border-bottom:1px solid var(--border);
  display:flex;align-items:center;padding:0 20px;gap:14px;
  position:sticky;top:0;z-index:100;box-shadow:0 1px 4px rgba(0,0,0,.04)}
.bc{display:flex;align-items:center;gap:5px;font-size:.83rem}
.bc-item{color:var(--muted);cursor:pointer;transition:color .15s}
.bc-item:hover{color:var(--purple)}
.bc-item.cur{color:var(--text);font-weight:600;cursor:default}
.bc-sep{color:var(--light);font-size:.65rem}
.ts{flex:1;max-width:260px;margin-left:auto;position:relative}
.ts input{width:100%;padding:7px 12px 7px 32px;border:1px solid var(--border);
  border-radius:9px;font-size:.83rem;font-family:'Sarabun',sans-serif;
  outline:none;background:var(--page);color:var(--text);transition:all .2s}
.ts input:focus{border-color:var(--purple);background:#fff;box-shadow:0 0 0 3px rgba(108,99,255,.1)}
.ts i{position:absolute;left:10px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:.78rem}
.tb-date{font-size:.75rem;color:var(--purple);font-weight:600;padding:5px 10px;
  background:rgba(108,99,255,.08);border:1px solid rgba(108,99,255,.2);border-radius:8px}

/* CONTENT */
.content{flex:1;padding:20px;overflow-y:auto}
.content::-webkit-scrollbar{width:5px}
.content::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}

/* Search drop */
#sdrop{display:none;position:fixed;top:var(--th);right:20px;width:300px;
  background:#fff;border-radius:11px;box-shadow:0 8px 28px rgba(0,0,0,.14);
  z-index:500;border:1px solid var(--border);max-height:380px;overflow-y:auto}

/* PAGE HEADER */
.ph{margin-bottom:18px}
.pt{font-size:1.25rem;font-weight:700;color:var(--text)}
.ps{font-size:.82rem;color:var(--muted);margin-top:2px}

/* KPI */
.kpi-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-bottom:20px}
.kpi{background:var(--card);border-radius:var(--r);padding:16px 18px;box-shadow:var(--shadow);
  display:flex;align-items:center;gap:12px;transition:all .2s;position:relative;overflow:hidden}
.kpi:hover{box-shadow:var(--shadow2);transform:translateY(-1px)}
.kpi::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:var(--r) var(--r) 0 0}
.kpi.kp::before{background:var(--purple)} .kpi.ka::before{background:var(--amber)}
.kpi.kt::before{background:var(--teal)}   .kpi.kr::before{background:var(--rose)}
.kpi.kb::before{background:var(--blue)}
.kpi-ico{width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0}
.kpi.kp .kpi-ico{background:rgba(108,99,255,.12);color:var(--purple)}
.kpi.ka .kpi-ico{background:rgba(245,158,11,.12);color:var(--amber)}
.kpi.kt .kpi-ico{background:rgba(20,184,166,.12);color:var(--teal)}
.kpi.kr .kpi-ico{background:rgba(244,63,94,.12);color:var(--rose)}
.kpi.kb .kpi-ico{background:rgba(59,130,246,.12);color:var(--blue)}
.kpi-v{font-size:1.5rem;font-weight:700;color:var(--text);line-height:1}
.kpi-l{font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:3px}
.kpi-s{font-size:.7rem;color:var(--light);margin-top:2px}

/* SECTION LABEL */
.slbl{font-size:.88rem;font-weight:700;color:var(--text);margin-bottom:12px;
  display:flex;align-items:center;gap:8px}
.slbl::after{content:'';flex:1;height:1px;background:var(--border)}
.sbadge{background:rgba(108,99,255,.1);color:var(--purple);padding:2px 9px;border-radius:50px;font-size:.7rem;font-weight:600}

/* CARD */
.card{background:var(--card);border-radius:var(--r);box-shadow:var(--shadow);overflow:hidden;transition:box-shadow .2s}
.card:hover{box-shadow:var(--shadow2)}
.ch{display:flex;align-items:center;padding:13px 16px;border-bottom:1px solid var(--border);gap:8px}
.ct{font-size:.9rem;font-weight:700;color:var(--text);flex:1}
.cs{font-size:.73rem;color:var(--muted);margin-top:2px}
.cb{padding:16px}
.cbox{position:relative;height:220px}

/* GRIDS */
.g2{display:grid;grid-template-columns:3fr 2fr;gap:16px;margin-bottom:18px}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:18px}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:18px}

/* TABLES */
.tw{background:var(--card);border-radius:var(--r);box-shadow:var(--shadow);overflow:auto;margin-bottom:18px}
table{width:100%;border-collapse:collapse;font-size:.82rem}
thead th{background:var(--page);padding:9px 12px;font-size:.7rem;font-weight:600;color:var(--muted);
  text-transform:uppercase;letter-spacing:.04em;border-bottom:1px solid var(--border);
  white-space:nowrap;text-align:left;border-right:1px solid rgba(0,0,0,.03);position:sticky;top:0}
thead th.r{text-align:right}
thead th.c{text-align:center}
tbody td{padding:9px 12px;border-bottom:1px solid rgba(0,0,0,.04);color:var(--text2);
  border-right:1px solid rgba(0,0,0,.02);vertical-align:middle}
tbody td.r{text-align:right;font-variant-numeric:tabular-nums}
tbody td.c{text-align:center}
tbody td.bold{font-weight:600;color:var(--text)}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover td{background:rgba(108,99,255,.025)}
tfoot td{background:var(--page);font-weight:700;color:var(--text);
  border-top:2px solid var(--border);padding:9px 12px}
tfoot td.r{text-align:right;font-variant-numeric:tabular-nums}

/* Quarter headers */
th.q1{background:rgba(59,130,246,.06)!important;color:var(--blue)!important}
th.q2{background:rgba(20,184,166,.06)!important;color:var(--teal)!important}
th.q3{background:rgba(245,158,11,.06)!important;color:var(--amber)!important}
th.q4{background:rgba(244,63,94,.06)!important;color:var(--rose)!important}
td.qt1{color:var(--blue);font-weight:600}
td.qt2{color:var(--teal);font-weight:600}
td.qt3{color:var(--amber);font-weight:600}
td.qt4{color:var(--rose);font-weight:600}
.qpill{display:inline-block;padding:1px 7px;border-radius:4px;font-size:.68rem;font-weight:600}
.qpill.q1{background:rgba(59,130,246,.1);color:var(--blue)}
.qpill.q2{background:rgba(20,184,166,.1);color:var(--teal)}
.qpill.q3{background:rgba(245,158,11,.1);color:var(--amber)}
.qpill.q4{background:rgba(244,63,94,.1);color:var(--rose)}

/* HERO banner */
.hero{background:linear-gradient(135deg,var(--dark) 0%,#2c3366 100%);
  border-radius:var(--r);padding:20px 24px;margin-bottom:18px;
  display:flex;align-items:center;gap:16px;
  box-shadow:0 4px 18px rgba(30,33,57,.3);position:relative;overflow:hidden}
.hero::after{content:'';position:absolute;top:-50px;right:-30px;
  width:160px;height:160px;background:rgba(108,99,255,.1);border-radius:50%}
.hero-ico{width:48px;height:48px;border-radius:12px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:1.3rem;
  background:rgba(108,99,255,.22);border:2px solid rgba(108,99,255,.35)}
.hero-name{font-size:1.1rem;font-weight:700;color:#fff}
.hero-sub{font-size:.8rem;color:rgba(255,255,255,.55);margin-top:2px}
.hero-stats{margin-left:auto;display:flex;gap:24px;flex-shrink:0}
.hs{text-align:center}
.hs-v{font-size:1.2rem;font-weight:700}
.hs-l{font-size:.65rem;color:rgba(255,255,255,.45);margin-top:2px}

/* SPARKLINE card */
.spark{background:linear-gradient(135deg,var(--purple),var(--purple2));
  border-radius:var(--r);padding:18px;color:#fff;
  box-shadow:0 6px 20px rgba(108,99,255,.35);position:relative;overflow:hidden}
.spark::after{content:'';position:absolute;top:-25px;right:-15px;
  width:90px;height:90px;background:rgba(255,255,255,.07);border-radius:50%}
.spark-ico{width:36px;height:36px;border-radius:8px;background:rgba(255,255,255,.2);
  display:flex;align-items:center;justify-content:center;font-size:.9rem;margin-bottom:8px}
.spark-v{font-size:1.9rem;font-weight:700;line-height:1}
.spark-l{font-size:.78rem;opacity:.8;margin-bottom:10px}
.spark-box{position:relative;height:60px}
.spark-qs{display:flex;gap:8px;margin-top:8px;font-size:.7rem;color:rgba(255,255,255,.75)}
.sq{flex:1;display:flex;flex-direction:column;gap:1px}
.sq-l{opacity:.6}
.sq-v{font-weight:700}

/* VIEW TABS */
.vtabs{display:flex;gap:3px;background:var(--page);border:1px solid var(--border);
  border-radius:9px;padding:3px;width:fit-content;margin-bottom:14px}
.vtab{padding:6px 14px;border-radius:7px;font-size:.8rem;font-weight:500;cursor:pointer;
  border:none;background:transparent;color:var(--muted);
  font-family:'Sarabun',sans-serif;transition:all .2s;display:flex;align-items:center;gap:5px}
.vtab.active{background:var(--card);color:var(--purple);box-shadow:0 2px 8px rgba(0,0,0,.08)}
.vtab:hover:not(.active){color:var(--text)}

/* FILTER BAR */
.fbar{display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.fsearch{flex:1;min-width:180px;max-width:300px;position:relative}
.fsearch input{width:100%;padding:7px 10px 7px 30px;border:1px solid var(--border);
  border-radius:9px;font-size:.82rem;font-family:'Sarabun',sans-serif;
  outline:none;background:var(--card);color:var(--text);transition:all .2s}
.fsearch input:focus{border-color:var(--purple);box-shadow:0 0 0 3px rgba(108,99,255,.1)}
.fsearch i{position:absolute;left:9px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:.75rem}
.fsort{display:flex;gap:3px}
.fsort-btn{padding:6px 12px;border-radius:8px;font-size:.78rem;cursor:pointer;
  border:1px solid var(--border);background:var(--card);color:var(--muted);
  font-family:'Sarabun',sans-serif;transition:all .2s}
.fsort-btn.active{background:var(--purple);border-color:var(--purple);color:#fff}
.fsort-btn:hover:not(.active){border-color:var(--purple);color:var(--purple)}
.rcnt{font-size:.78rem;color:var(--muted);margin-left:auto}

/* PROJECT SELECT */
.proj-select-wrap{display:flex;align-items:center;gap:10px;margin-bottom:18px;flex-wrap:wrap}
.proj-select{padding:9px 14px;border:1px solid var(--border);border-radius:var(--r);
  font-size:.88rem;font-family:'Sarabun',sans-serif;color:var(--text);
  background:var(--card);outline:none;cursor:pointer;min-width:360px;
  transition:all .2s}
.proj-select:focus{border-color:var(--purple);box-shadow:0 0 0 3px rgba(108,99,255,.1)}
.proj-stat-bar{display:flex;gap:12px;flex-wrap:wrap}
.pstat{padding:7px 14px;border-radius:9px;font-size:.82rem;font-weight:600;
  display:flex;align-items:center;gap:6px}

/* CAT filter pills */
.cpills{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap}
.cpill{padding:5px 14px;border-radius:50px;font-size:.78rem;font-weight:600;
  cursor:pointer;border:1.5px solid transparent;transition:all .2s}
.cpill:hover{opacity:.85}

/* Num badge */
.nbadge{display:inline-flex;width:22px;height:22px;border-radius:5px;
  align-items:center;justify-content:center;font-weight:700;font-size:.7rem}

/* Fade */
@keyframes fadeUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.fi{animation:fadeUp .3s ease forwards}

/* Responsive */
@media(max-width:1100px){.g2{grid-template-columns:1fr}.g3{grid-template-columns:1fr 1fr}.hero-stats{display:none}}
@media(max-width:768px){
  .sidebar{width:var(--sb-c)}.wrapper{margin-left:var(--sb-c)}
  .g3,.g4{grid-template-columns:1fr}.ts{display:none}
}
</style>
</head>
<body>
<!-- SIDEBAR -->
<aside class="sidebar" id="sidebar">
  <div class="sb-resizer" id="sbResizer" title="คลิกลากเพื่อปรับความกว้างเมนู"></div>
  <div class="sb-brand">
    <div class="sb-logo"><i class="fas fa-briefcase"></i></div>
    <div class="sb-txt">
      <div class="sb-title">DOE Dashboard</div>
      <div class="sb-sub">กรมการจัดหางาน</div>
    </div>
  </div>

  <button class="sb-toggle" onclick="toggleSidebar()">
    <i class="fas fa-bars"></i><span class="tl"> ย่อเมนู</span>
  </button>

  <nav class="sb-nav" id="sbNav">
    <div class="sb-lbl">เมนูหลัก</div>
    <div class="sb-item active" id="nav-ov" onclick="go('overview')" data-tip="ภาพรวมทั้งกรม">
      <div class="sb-ico"><i class="fas fa-chart-pie"></i></div>
      <span class="sb-lname">ภาพรวมทั้งกรม</span>
    </div>
    <div class="sb-item" id="nav-proj" onclick="go('project')" data-tip="จัดสรรรายโครงการ">
      <div class="sb-ico"><i class="fas fa-diagram-project"></i></div>
      <span class="sb-lname">จัดสรรรายโครงการ</span>
    </div>

    <div class="sb-lbl" style="margin-top:6px">หน่วยงาน</div>

    <!-- Category with expandable sub-menus -->
    <div class="sb-item" id="nav-central" onclick="toggleCat('central','ส่วนกลาง')" data-tip="ส่วนกลาง">
      <div class="sb-ico"><i class="fas fa-building-columns"></i></div>
      <span class="sb-lname">หน่วยงานส่วนกลาง</span>
      <span class="sb-cnt" id="cnt-central">-</span>
    </div>
    <div class="sb-sub-menu" id="sub-central"></div>

    <div class="sb-item" id="nav-province" onclick="toggleCat('province','จังหวัด')" data-tip="จังหวัด">
      <div class="sb-ico"><i class="fas fa-city"></i></div>
      <span class="sb-lname">สำนักงานจัดหางานจังหวัด</span>
      <span class="sb-cnt" id="cnt-province">-</span>
    </div>
    <div class="sb-sub-menu" id="sub-province"></div>

    <div class="sb-item" id="nav-regional" onclick="toggleCat('regional','ศูนย์ภาค')" data-tip="ศูนย์ภาค">
      <div class="sb-ico"><i class="fas fa-map-location-dot"></i></div>
      <span class="sb-lname">ศูนย์บริการจัดหางาน</span>
      <span class="sb-cnt" id="cnt-regional">-</span>
    </div>
    <div class="sb-sub-menu" id="sub-regional"></div>

    <div class="sb-item" id="nav-border" onclick="toggleCat('border','ด่าน')" data-tip="ด่านตรวจ">
      <div class="sb-ico"><i class="fas fa-shield-halved"></i></div>
      <span class="sb-lname">ด่านตรวจคนหางาน</span>
      <span class="sb-cnt" id="cnt-border">-</span>
    </div>
    <div class="sb-sub-menu" id="sub-border"></div>
  </nav>
</aside>

<!-- WRAPPER -->
<div class="wrapper" id="wrapper">
  <div class="topbar">
    <div class="bc" id="bc">
      <span class="bc-item" onclick="go('overview')">DOE</span>
      <span class="bc-sep"><i class="fas fa-chevron-right" style="font-size:.58rem"></i></span>
      <span class="bc-item cur" id="bc2">ภาพรวมทั้งกรม</span>
    </div>
    <div class="ts">
      <i class="fas fa-search"></i>
      <input type="text" id="tsInput" placeholder="ค้นหาหน่วยงาน..." oninput="tsSearch(this.value)">
    </div>
    <div class="tb-date">📅 29 ก.ย. 2569</div>
  </div>
  <main class="content" id="content"></main>
</div>

<div id="sdrop"></div>

<script>
const D = """ + dj + r""";
D.units.forEach((u,i) => { u.id = i; });

// State
const S = {
  mini: false, page:'overview', cat:null, unit:null, openCat:null,
  cs:'', csort:'td', projNum:1, pcat:'all', psearch:'', pview:'quarter', charts:[]
};

// Colors
const PC=['#6c63ff','#f59e0b','#14b8a6','#f43f5e','#3b82f6','#10b981','#f97316','#8b5cf6','#06b6d4','#ec4899','#84cc16'];
const CC={'ส่วนกลาง':'#6c63ff','จังหวัด':'#10b981','ศูนย์ภาค':'#8b5cf6','ด่าน':'#f59e0b'};
const CI={'ส่วนกลาง':'fa-building-columns','จังหวัด':'fa-city','ศูนย์ภาค':'fa-map-location-dot','ด่าน':'fa-shield-halved'};
const QC=['#3b82f6','#14b8a6','#f59e0b','#f43f5e'];

const fmt = n => (n||0).toLocaleString('th-TH');
const uT = u => u.projects.reduce((s,p)=>s+(p.target||0),0);
const uQ = (u,q) => u.projects.reduce((s,p)=>s+(p[q]?.total||0),0);

// Charts
function kc() { S.charts.forEach(c=>{try{c.destroy()}catch(e){}}); S.charts=[]; }
function ac(c) { if(c) S.charts.push(c); }

// Sidebar toggle & resizer
function toggleSidebar(){
  S.mini=!S.mini;
  document.getElementById('sidebar').classList.toggle('mini',S.mini);
  document.body.classList.toggle('mini-mode',S.mini);
}

function initResizer(){
  const resizer = document.getElementById('sbResizer');
  const sidebar = document.getElementById('sidebar');
  const wrapper = document.getElementById('wrapper');
  if(!resizer) return;
  let isResizing = false;

  const saved = localStorage.getItem('doe_sb_w');
  if(saved && !S.mini){
    document.documentElement.style.setProperty('--sb', saved + 'px');
  }

  resizer.addEventListener('mousedown', e => {
    isResizing = true;
    resizer.classList.add('active');
    sidebar.classList.add('resizing');
    wrapper.classList.add('resizing');
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
    if(S.mini) toggleSidebar();
    e.preventDefault();
  });

  document.addEventListener('mousemove', e => {
    if(!isResizing) return;
    let w = e.clientX;
    if(w < 180) w = 180;
    if(w > 520) w = 520;
    document.documentElement.style.setProperty('--sb', w + 'px');
    localStorage.setItem('doe_sb_w', w);
  });

  document.addEventListener('mouseup', () => {
    if(isResizing){
      isResizing = false;
      resizer.classList.remove('active');
      sidebar.classList.remove('resizing');
      wrapper.classList.remove('resizing');
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    }
  });
}

// Build sidebar sub-menus
function initSidebar(){
  const map = {central:'ส่วนกลาง', province:'จังหวัด', regional:'ศูนย์ภาค', border:'ด่าน'};
  Object.entries(map).forEach(([k,v])=>{
    const units = D.units.filter(u=>u.category===v);
    document.getElementById('cnt-'+k).textContent = units.length;
    const color = CC[v]||'#6c63ff';
    document.getElementById('sub-'+k).innerHTML = units.map(u=>{
      const t = uT(u);
      const sn = u.name.length>22 ? u.name.slice(0,20)+'...' : u.name;
      return `<div class="sb-sub-item" id="sub-u-${u.id}"
        onclick="event.stopPropagation();pickUnit(${u.id})">
        <div class="dot"></div>
        <span style="flex:1">${sn}</span>
        ${t>0?`<span style="font-size:.65rem;color:${color};opacity:.8">${fmt(t)}</span>`:''}
      </div>`;
    }).join('');
  });
}

let catOpen = null;
function toggleCat(key, catName){
  const sub = document.getElementById('sub-'+key);
  const navItem = document.getElementById('nav-'+key);
  // Close previous
  if(catOpen && catOpen!==key){
    document.getElementById('sub-'+catOpen)?.classList.remove('open');
    document.getElementById('nav-'+catOpen)?.classList.remove('active');
  }
  if(catOpen===key){
    sub.classList.remove('open');
    navItem.classList.remove('active');
    catOpen=null;
  } else {
    sub.classList.add('open');
    setActiveNav('nav-'+key);
    catOpen=key;
  }
  // Show category page
  S.cat = catName;
  go('cat');
}

function pickUnit(id){
  const u = typeof id === 'number' ? D.units[id] : D.units.find(x=>x.id===id || x.sheet===id || x.name===id);
  if(!u) return;
  S.unit = u.id; S.cat = u.category;
  // Highlight sub item
  document.querySelectorAll('.sb-sub-item').forEach(e=>e.classList.remove('active'));
  document.getElementById('sub-u-'+u.id)?.classList.add('active');
  go('unit');
}

function setActiveNav(id){
  document.querySelectorAll('.sb-item').forEach(e=>e.classList.remove('active'));
  document.getElementById(id)?.classList.add('active');
}

// Routing
function go(page){
  kc();
  S.page = page;
  if(page==='overview'){
    document.querySelectorAll('.sb-item').forEach(e=>e.classList.remove('active'));
    document.getElementById('nav-ov').classList.add('active');
    setBc([{t:'ภาพรวมทั้งกรม'}]);
    renderOverview();
  } else if(page==='project'){
    setActiveNav('nav-proj');
    setBc([{t:'จัดสรรรายโครงการ'}]);
    renderProject();
  } else if(page==='cat'){
    setBc([{t:S.cat,f:()=>{S.unit=null;go('cat')}}]);
    renderCat();
  } else if(page==='unit'){
    const u = typeof S.unit === 'number' ? D.units[S.unit] : D.units.find(x=>x.id===S.unit || x.sheet===S.unit);
    setBc([
      {t:S.cat, f:()=>{S.unit=null;go('cat')}},
      {t:u?.name||'รายละเอียดหน่วยงาน'}
    ]);
    renderUnit(u);
  }
}

function setBc(items){
  let html = `<span class="bc-item" onclick="go('overview')">DOE</span>`;
  items.forEach((item,i)=>{
    html += `<span class="bc-sep"><i class="fas fa-chevron-right" style="font-size:.58rem"></i></span>`;
    if(item.f)
      html += `<span class="bc-item" onclick="(${item.f.toString()})()">${item.t}</span>`;
    else
      html += `<span class="bc-item cur">${item.t}</span>`;
  });
  document.getElementById('bc').innerHTML = html;
}

// Search
function tsSearch(q){
  const drop = document.getElementById('sdrop');
  q = q.trim().toLowerCase();
  if(!q){ drop.style.display='none'; return; }
  const res = D.units.filter(u=>u.name.toLowerCase().includes(q)).slice(0,8);
  if(!res.length){ drop.style.display='none'; return; }
  drop.style.display='block';
  drop.innerHTML = res.map(u=>{
    const c=CC[u.category]||'#6c63ff';
    return `<div onclick="pickUnit(${u.id});document.getElementById('tsInput').value=''"
      style="padding:9px 12px;cursor:pointer;border-bottom:1px solid #f0f4f8;display:flex;align-items:center;gap:8px"
      onmouseover="this.style.background='#f7f9fc'" onmouseout="this.style.background='#fff'">
      <div style="width:26px;height:26px;border-radius:7px;background:${c}18;color:${c};display:flex;align-items:center;justify-content:center;font-size:.72rem;flex-shrink:0">
        <i class="fas ${CI[u.category]||'fa-building'}"></i></div>
      <div><div style="font-size:.83rem;font-weight:600;color:#1e2139">${u.name}</div>
        <div style="font-size:.7rem;color:#8896a4">${u.category} • ${fmt(uT(u))}</div></div>
    </div>`;
  }).join('');
}
function tsPickUnit(sheet){
  document.getElementById('sdrop').style.display='none';
  pickUnit(sheet);
}
document.addEventListener('click',e=>{
  if(!e.target.closest('#sdrop')&&!e.target.closest('#tsInput'))
    document.getElementById('sdrop').style.display='none';
});

// ============================================================
// OVERVIEW
// ============================================================
function renderOverview(){
  const units=D.units, projs=D.projects;
  const PT={};
  projs.forEach(p=>PT[p.num]={target:0,q1:0,q2:0,q3:0,q4:0});
  units.forEach(u=>u.projects.forEach(p=>{
    if(!PT[p.num]) return;
    PT[p.num].target+=p.target||0;
    ['q1','q2','q3','q4'].forEach(q=>PT[p.num][q]+=(p[q]?.total||0));
  }));
  const grand=Object.values(PT).reduce((s,p)=>s+p.target,0);
  const catC={};
  units.forEach(u=>catC[u.category]=(catC[u.category]||0)+1);
  const top=projs.map((p,i)=>{const t=PT[p.num];return{...t,name:p.name,num:p.num,color:PC[i%PC.length]};}).sort((a,b)=>b.target-a.target);
  const mx=top[0]?.target||1;

  document.getElementById('content').innerHTML=`<div class="fi">
<div class="ph"><div class="pt">ภาพรวมทั้งกรม</div><div class="ps">เป้าหมายการดำเนินงาน ประจำปีงบประมาณ พ.ศ. 2570</div></div>
<div class="kpi-row">
  <div class="kpi kp"><div class="kpi-ico"><i class="fas fa-building"></i></div><div><div class="kpi-l">หน่วยงาน</div><div class="kpi-v">${fmt(units.length)}</div><div class="kpi-s">หน่วย</div></div></div>
  <div class="kpi ka"><div class="kpi-ico"><i class="fas fa-folder-open"></i></div><div><div class="kpi-l">โครงการ</div><div class="kpi-v">${projs.length}</div><div class="kpi-s">โครงการ</div></div></div>
  <div class="kpi kt"><div class="kpi-ico"><i class="fas fa-bullseye"></i></div><div><div class="kpi-l">เป้าหมายรวม</div><div class="kpi-v">${fmt(grand)}</div><div class="kpi-s">ทุกโครงการ</div></div></div>
  <div class="kpi kr"><div class="kpi-ico"><i class="fas fa-city"></i></div><div><div class="kpi-l">จังหวัด</div><div class="kpi-v">${catC['จังหวัด']||0}</div></div></div>
  <div class="kpi kb"><div class="kpi-ico"><i class="fas fa-shield-halved"></i></div><div><div class="kpi-l">ด่าน</div><div class="kpi-v">${catC['ด่าน']||0}</div></div></div>
</div>
<div class="g2">
  <div class="card">
    <div class="ch"><div><div class="ct">เป้าหมายรายโครงการ (ทั้งกรม)</div><div class="cs">แยก Q1–Q4</div></div></div>
    <div class="cb"><div class="cbox"><canvas id="cvMain"></canvas></div></div>
  </div>
  <div class="card">
    <div class="ch"><div class="ct">สัดส่วนโครงการหลัก</div></div>
    <div class="cb">
      <div style="display:flex;flex-direction:column;gap:12px">
      ${top.slice(0,6).map(p=>`
        <div>
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px">
            <div style="width:7px;height:7px;border-radius:50%;background:${p.color};flex-shrink:0"></div>
            <div style="font-size:.8rem;color:var(--text2);flex:1">${p.name.length>32?p.name.slice(0,30)+'...':p.name}</div>
            <div style="font-size:.82rem;font-weight:700;color:var(--text);font-variant-numeric:tabular-nums">${fmt(p.target)}</div>
          </div>
          <div style="height:5px;background:var(--border);border-radius:3px;overflow:hidden">
            <div style="height:100%;width:${(p.target/mx*100).toFixed(1)}%;background:${p.color};border-radius:3px;transition:width .8s"></div>
          </div>
        </div>`).join('')}
      </div>
    </div>
  </div>
</div>

<div class="slbl">สรุปเป้าหมายรายโครงการ <span class="sbadge">${projs.length} โครงการ</span></div>
<div class="tw"><table>
  <thead><tr>
    <th>#</th><th>ชื่อโครงการ</th>
    <th class="r">เป้าหมายรวม</th>
    <th class="r q1"><span class="qpill q1">Q1</span></th>
    <th class="r q2"><span class="qpill q2">Q2</span></th>
    <th class="r q3"><span class="qpill q3">Q3</span></th>
    <th class="r q4"><span class="qpill q4">Q4</span></th>
  </tr></thead>
  <tbody>
  ${projs.map((p,i)=>{const t=PT[p.num];return`<tr>
    <td><span class="nbadge" style="background:${PC[i%PC.length]}18;color:${PC[i%PC.length]}">${p.num}</span></td>
    <td class="bold">${p.name}</td>
    <td class="r bold">${fmt(t.target)}</td>
    <td class="r qt1">${fmt(t.q1)}</td>
    <td class="r qt2">${fmt(t.q2)}</td>
    <td class="r qt3">${fmt(t.q3)}</td>
    <td class="r qt4">${fmt(t.q4)}</td>
  </tr>`;}).join('')}
  </tbody>
  <tfoot><tr>
    <td colspan="2">รวม</td>
    <td class="r">${fmt(grand)}</td>
    <td class="r" style="color:var(--blue)">${fmt(Object.values(PT).reduce((s,p)=>s+p.q1,0))}</td>
    <td class="r" style="color:var(--teal)">${fmt(Object.values(PT).reduce((s,p)=>s+p.q2,0))}</td>
    <td class="r" style="color:var(--amber)">${fmt(Object.values(PT).reduce((s,p)=>s+p.q3,0))}</td>
    <td class="r" style="color:var(--rose)">${fmt(Object.values(PT).reduce((s,p)=>s+p.q4,0))}</td>
  </tr></tfoot>
</table></div>
</div>`;

  setTimeout(()=>{
    ac(new Chart(document.getElementById('cvMain'),{
      type:'bar',
      data:{labels:projs.map(p=>`P${p.num}`),datasets:[
        {label:'Q1',data:projs.map(p=>PT[p.num].q1),backgroundColor:'rgba(59,130,246,.8)',borderRadius:4},
        {label:'Q2',data:projs.map(p=>PT[p.num].q2),backgroundColor:'rgba(20,184,166,.8)',borderRadius:4},
        {label:'Q3',data:projs.map(p=>PT[p.num].q3),backgroundColor:'rgba(245,158,11,.8)',borderRadius:4},
        {label:'Q4',data:projs.map(p=>PT[p.num].q4),backgroundColor:'rgba(244,63,94,.8)',borderRadius:4},
      ]},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{labels:{color:'#4a5568',font:{family:'Sarabun',size:11}}},
          tooltip:{callbacks:{title:items=>D.projects[items[0].dataIndex]?.name||''},bodyFont:{family:'Sarabun'},titleFont:{family:'Sarabun'}}},
        scales:{x:{ticks:{color:'#8896a4',font:{family:'Sarabun'}},grid:{color:'rgba(0,0,0,.04)'}},
          y:{ticks:{color:'#8896a4',callback:v=>Number(v).toLocaleString('th-TH'),font:{family:'Sarabun'}},grid:{color:'rgba(0,0,0,.06)'}}}}
    }));
  },50);
}

// ============================================================
// CATEGORY PAGE
// ============================================================
function renderCat(){
  let units=D.units.filter(u=>u.category===S.cat);
  const color=CC[S.cat]||'#6c63ff';
  const ico=CI[S.cat]||'fa-building';
  const total=units.reduce((s,u)=>s+uT(u),0);
  const q1=units.reduce((s,u)=>s+uQ(u,'q1'),0);
  const q2=units.reduce((s,u)=>s+uQ(u,'q2'),0);
  const q3=units.reduce((s,u)=>s+uQ(u,'q3'),0);
  const q4=units.reduce((s,u)=>s+uQ(u,'q4'),0);

  document.getElementById('content').innerHTML=`<div class="fi">
<div class="hero">
  <div class="hero-ico" style="background:${color}22;border-color:${color}44">
    <i class="fas ${ico}" style="color:rgba(255,255,255,.9)"></i></div>
  <div>
    <div class="hero-name">${S.cat}</div>
    <div class="hero-sub">เป้าหมายการดำเนินงาน ปีงบประมาณ พ.ศ. 2570</div>
  </div>
  <div class="hero-stats">
    <div class="hs"><div class="hs-v" style="color:var(--amber)">${fmt(total)}</div><div class="hs-l">เป้าหมายรวม</div></div>
    <div class="hs"><div class="hs-v" style="color:#7eb8ff">${fmt(q1)}</div><div class="hs-l">Q1</div></div>
    <div class="hs"><div class="hs-v" style="color:#5fffd8">${fmt(q2)}</div><div class="hs-l">Q2</div></div>
    <div class="hs"><div class="hs-v" style="color:#ffd87e">${fmt(q3)}</div><div class="hs-l">Q3</div></div>
    <div class="hs"><div class="hs-v" style="color:#ff8fa3">${fmt(q4)}</div><div class="hs-l">Q4</div></div>
  </div>
</div>
<div class="fbar">
  <div class="fsearch"><i class="fas fa-search"></i>
    <input type="text" placeholder="ค้นหาหน่วยงาน..." oninput="catFilter(this.value)" id="catQ">
  </div>
  <div class="fsort">
    <button class="fsort-btn active" id="fs-td" onclick="catSort('td')">เป้าหมาย ↓</button>
    <button class="fsort-btn" id="fs-ta" onclick="catSort('ta')">เป้าหมาย ↑</button>
    <button class="fsort-btn" id="fs-nm" onclick="catSort('nm')">ชื่อ A-Z</button>
  </div>
  <div class="rcnt" id="catCnt">${units.length} หน่วยงาน</div>
</div>
<div class="tw" id="catTable"></div>
</div>`;

  renderCatTable();
}

function catFilter(q){ S.cs=q; renderCatTable(); }
function catSort(m){
  S.csort=m;
  ['td','ta','nm'].forEach(k=>document.getElementById('fs-'+k)?.classList.remove('active'));
  document.getElementById('fs-'+m)?.classList.add('active');
  renderCatTable();
}
function renderCatTable(){
  let units=D.units.filter(u=>u.category===S.cat);
  if(S.cs) units=units.filter(u=>u.name.toLowerCase().includes(S.cs.toLowerCase()));
  if(S.csort==='td') units.sort((a,b)=>uT(b)-uT(a));
  else if(S.csort==='ta') units.sort((a,b)=>uT(a)-uT(b));
  else units.sort((a,b)=>a.name.localeCompare(b.name,'th'));
  document.getElementById('catCnt').textContent=units.length+' หน่วยงาน';
  const color=CC[S.cat]||'#6c63ff';
  document.getElementById('catTable').innerHTML=`<table>
    <thead><tr>
      <th>#</th><th>ชื่อหน่วยงาน</th>
      <th class="r">เป้าหมายรวม</th>
      <th class="r q1">Q1</th><th class="r q2">Q2</th>
      <th class="r q3">Q3</th><th class="r q4">Q4</th>
      <th class="c">รายละเอียด</th>
    </tr></thead>
    <tbody>
    ${units.map((u,i)=>{
      const t=uT(u);
      return `<tr>
        <td style="color:var(--muted);font-size:.75rem">${i+1}</td>
        <td class="bold">${u.name}</td>
        <td class="r bold" style="color:${color}">${t>0?fmt(t):'-'}</td>
        <td class="r qt1">${uQ(u,'q1')>0?fmt(uQ(u,'q1')):'-'}</td>
        <td class="r qt2">${uQ(u,'q2')>0?fmt(uQ(u,'q2')):'-'}</td>
        <td class="r qt3">${uQ(u,'q3')>0?fmt(uQ(u,'q3')):'-'}</td>
        <td class="r qt4">${uQ(u,'q4')>0?fmt(uQ(u,'q4')):'-'}</td>
        <td class="c">
          <button onclick="pickUnit(${u.id});"
            style="padding:4px 12px;border-radius:6px;border:1px solid ${color};color:${color};
            background:${color}0d;cursor:pointer;font-size:.75rem;font-family:'Sarabun',sans-serif;
            transition:all .2s" onmouseover="this.style.background='${color}22'" onmouseout="this.style.background='${color}0d'">
            ดูรายละเอียด <i class="fas fa-arrow-right" style="font-size:.65rem"></i>
          </button>
        </td>
      </tr>`;
    }).join('')}
    </tbody>
    <tfoot><tr>
      <td colspan="2">รวม ${units.length} หน่วยงาน</td>
      <td class="r">${fmt(units.reduce((s,u)=>s+uT(u),0))}</td>
      <td class="r" style="color:var(--blue)">${fmt(units.reduce((s,u)=>s+uQ(u,'q1'),0))}</td>
      <td class="r" style="color:var(--teal)">${fmt(units.reduce((s,u)=>s+uQ(u,'q2'),0))}</td>
      <td class="r" style="color:var(--amber)">${fmt(units.reduce((s,u)=>s+uQ(u,'q3'),0))}</td>
      <td class="r" style="color:var(--rose)">${fmt(units.reduce((s,u)=>s+uQ(u,'q4'),0))}</td>
      <td></td>
    </tr></tfoot>
  </table>`;
}

// ============================================================
// UNIT DETAIL
// ============================================================
let _u = null;
function renderUnit(unit){
  _u = unit;
  const t=uT(unit);
  const q1=uQ(unit,'q1'),q2=uQ(unit,'q2'),q3=uQ(unit,'q3'),q4=uQ(unit,'q4');
  const color=CC[unit.category]||'#6c63ff';
  const ico=CI[unit.category]||'fa-building';

  document.getElementById('content').innerHTML=`<div class="fi">
<div class="hero">
  <div class="hero-ico"><i class="fas ${ico}" style="color:rgba(255,255,255,.9)"></i></div>
  <div>
    <div class="hero-name">${unit.name}</div>
    <div class="hero-sub">${unit.category} • ${unit.projects.filter(p=>p.target>0).length} โครงการที่มีเป้าหมาย</div>
  </div>
  <div class="hero-stats">
    <div class="hs"><div class="hs-v" style="color:var(--amber)">${fmt(t)}</div><div class="hs-l">เป้าหมายรวม</div></div>
    <div class="hs"><div class="hs-v" style="color:#7eb8ff">${fmt(q1)}</div><div class="hs-l">Q1</div></div>
    <div class="hs"><div class="hs-v" style="color:#5fffd8">${fmt(q2)}</div><div class="hs-l">Q2</div></div>
    <div class="hs"><div class="hs-v" style="color:#ffd87e">${fmt(q3)}</div><div class="hs-l">Q3</div></div>
    <div class="hs"><div class="hs-v" style="color:#ff8fa3">${fmt(q4)}</div><div class="hs-l">Q4</div></div>
  </div>
</div>

<div class="g2">
  <div class="card">
    <div class="ch"><div><div class="ct">เป้าหมายรายโครงการ</div><div class="cs">แยกตามไตรมาส</div></div></div>
    <div class="cb"><div class="cbox"><canvas id="cvU"></canvas></div></div>
  </div>
  <div class="spark">
    <div class="spark-ico"><i class="fas fa-bullseye"></i></div>
    <div class="spark-v">${fmt(t)}</div>
    <div class="spark-l">เป้าหมายรวมทั้งปี</div>
    <div class="spark-box"><canvas id="cvSp"></canvas></div>
    <div class="spark-qs">
      <div class="sq"><div class="sq-l">Q1 ต.ค.–ธ.ค.</div><div class="sq-v">${fmt(q1)}</div></div>
      <div class="sq"><div class="sq-l">Q2 ม.ค.–มี.ค.</div><div class="sq-v">${fmt(q2)}</div></div>
      <div class="sq"><div class="sq-l">Q3 เม.ย.–มิ.ย.</div><div class="sq-v">${fmt(q3)}</div></div>
      <div class="sq"><div class="sq-l">Q4 ก.ค.–ก.ย.</div><div class="sq-v">${fmt(q4)}</div></div>
    </div>
  </div>
</div>

<div class="vtabs">
  <button class="vtab active" id="vt-proj" onclick="switchUnitView('proj')"><i class="fas fa-table-list"></i> รายโครงการ</button>
  <button class="vtab" id="vt-month" onclick="switchUnitView('month')"><i class="fas fa-calendar-alt"></i> ตารางรายเดือน</button>
</div>
<div id="uArea"></div>
</div>`;

  setTimeout(()=>{
    // Bar chart
    const ap=unit.projects.filter(p=>p.target>0);
    ac(new Chart(document.getElementById('cvU'),{
      type:'bar',
      data:{labels:ap.map(p=>`P${p.num}`),datasets:[
        {label:'Q1',data:ap.map(p=>p.q1.total),backgroundColor:'rgba(59,130,246,.8)',borderRadius:4},
        {label:'Q2',data:ap.map(p=>p.q2.total),backgroundColor:'rgba(20,184,166,.8)',borderRadius:4},
        {label:'Q3',data:ap.map(p=>p.q3.total),backgroundColor:'rgba(245,158,11,.8)',borderRadius:4},
        {label:'Q4',data:ap.map(p=>p.q4.total),backgroundColor:'rgba(244,63,94,.8)',borderRadius:4},
      ]},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{labels:{color:'#4a5568',font:{family:'Sarabun',size:11}}},
          tooltip:{callbacks:{title:items=>ap[items[0].dataIndex]?.name||''},bodyFont:{family:'Sarabun'},titleFont:{family:'Sarabun'}}},
        scales:{x:{ticks:{color:'#8896a4',font:{family:'Sarabun'}},grid:{color:'rgba(0,0,0,.04)'}},
          y:{ticks:{color:'#8896a4',callback:v=>Number(v).toLocaleString('th-TH'),font:{family:'Sarabun'}},grid:{color:'rgba(0,0,0,.06)'}}}}
    }));
    // Spark
    ac(new Chart(document.getElementById('cvSp'),{
      type:'line',
      data:{labels:['Q1','Q2','Q3','Q4'],datasets:[{data:[q1,q2,q3,q4],borderColor:'rgba(255,255,255,.7)',backgroundColor:'rgba(255,255,255,.1)',tension:.4,pointRadius:3,pointBackgroundColor:'#fff',fill:true}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{display:false},y:{display:false}}}
    }));
    renderProjTable();
  },50);
}

function switchUnitView(v){
  document.getElementById('vt-proj')?.classList.toggle('active',v==='proj');
  document.getElementById('vt-month')?.classList.toggle('active',v==='month');
  if(v==='proj') renderProjTable();
  else renderMonthTable();
}

function renderProjTable(){
  const unit=_u; if(!unit) return;
  document.getElementById('uArea').innerHTML=`
<div class="slbl">รายโครงการ <span class="sbadge">${unit.projects.length} โครงการ</span></div>
<div class="tw"><table>
  <thead><tr>
    <th>#</th><th>ชื่อโครงการ</th><th>หน่วย</th>
    <th class="r">เป้าหมายรวม</th>
    <th class="r q1">Q1</th><th class="r q2">Q2</th><th class="r q3">Q3</th><th class="r q4">Q4</th>
  </tr></thead>
  <tbody>
  ${unit.projects.map((p,i)=>`<tr>
    <td><span class="nbadge" style="background:${PC[i%PC.length]}18;color:${PC[i%PC.length]}">${p.num}</span></td>
    <td class="bold">${p.name}</td>
    <td style="color:var(--muted)">${p.unit||''}</td>
    <td class="r bold" style="color:${p.target>0?PC[i%PC.length]:'var(--light)'}">${p.target>0?fmt(p.target):'-'}</td>
    <td class="r qt1">${p.q1.total>0?fmt(p.q1.total):'-'}</td>
    <td class="r qt2">${p.q2.total>0?fmt(p.q2.total):'-'}</td>
    <td class="r qt3">${p.q3.total>0?fmt(p.q3.total):'-'}</td>
    <td class="r qt4">${p.q4.total>0?fmt(p.q4.total):'-'}</td>
  </tr>`).join('')}
  </tbody>
  <tfoot><tr>
    <td colspan="3">รวม</td>
    <td class="r">${fmt(uT(unit))}</td>
    <td class="r" style="color:var(--blue)">${fmt(uQ(unit,'q1'))}</td>
    <td class="r" style="color:var(--teal)">${fmt(uQ(unit,'q2'))}</td>
    <td class="r" style="color:var(--amber)">${fmt(uQ(unit,'q3'))}</td>
    <td class="r" style="color:var(--rose)">${fmt(uQ(unit,'q4'))}</td>
  </tr></tfoot>
</table></div>`;
}

function renderMonthTable(){
  const unit=_u; if(!unit) return;
  const cv=(v,cls='')=>`<td class="${cls}" style="${v>0?'':'color:#cdd5df'}">${v>0?fmt(v):'-'}</td>`;
  const rows=unit.projects.map((p,i)=>`<tr>
    <td><span class="nbadge" style="background:${PC[i%PC.length]}18;color:${PC[i%PC.length]}">${p.num}</span></td>
    <td class="bold">${p.name.length>40?p.name.slice(0,38)+'...':p.name}</td>
    <td style="color:var(--muted)">${p.unit||''}</td>
    <td class="r bold">${p.target>0?fmt(p.target):'-'}</td>
    ${cv(p.q1.oct)}${cv(p.q1.nov)}${cv(p.q1.dec)}${cv(p.q1.total,'r qt1')}
    ${cv(p.q2.jan)}${cv(p.q2.feb)}${cv(p.q2.mar)}${cv(p.q2.total,'r qt2')}
    ${cv(p.q3.apr)}${cv(p.q3.may)}${cv(p.q3.jun)}${cv(p.q3.total,'r qt3')}
    ${cv(p.q4.jul)}${cv(p.q4.aug)}${cv(p.q4.sep)}${cv(p.q4.total,'r qt4')}
  </tr>`).join('');
  const T={t:0,q1:{oct:0,nov:0,dec:0,total:0},q2:{jan:0,feb:0,mar:0,total:0},q3:{apr:0,may:0,jun:0,total:0},q4:{jul:0,aug:0,sep:0,total:0}};
  unit.projects.forEach(p=>{
    T.t+=p.target||0;
    ['oct','nov','dec','total'].forEach(k=>T.q1[k]+=(p.q1[k]||0));
    ['jan','feb','mar','total'].forEach(k=>T.q2[k]+=(p.q2[k]||0));
    ['apr','may','jun','total'].forEach(k=>T.q3[k]+=(p.q3[k]||0));
    ['jul','aug','sep','total'].forEach(k=>T.q4[k]+=(p.q4[k]||0));
  });
  const tc=v=>`<td class="r" style="font-weight:700">${fmt(v)}</td>`;
  document.getElementById('uArea').innerHTML=`
<div class="slbl">ตารางเป้าหมายรายเดือน</div>
<div class="tw" style="overflow:auto"><table style="min-width:900px">
  <thead>
    <tr>
      <th rowspan="2">#</th><th rowspan="2" class="l">โครงการ</th><th rowspan="2">หน่วย</th><th rowspan="2" class="r">เป้าหมาย</th>
      <th colspan="4" class="c q1">ไตรมาส 1 (ปี 2569)</th>
      <th colspan="4" class="c q2">ไตรมาส 2</th>
      <th colspan="4" class="c q3">ไตรมาส 3</th>
      <th colspan="4" class="c q4">ไตรมาส 4</th>
    </tr>
    <tr>
      <th class="c q1">ต.ค.</th><th class="c q1">พ.ย.</th><th class="c q1">ธ.ค.</th><th class="c q1" style="font-weight:800">รวม</th>
      <th class="c q2">ม.ค.</th><th class="c q2">ก.พ.</th><th class="c q2">มี.ค.</th><th class="c q2" style="font-weight:800">รวม</th>
      <th class="c q3">เม.ย.</th><th class="c q3">พ.ค.</th><th class="c q3">มิ.ย.</th><th class="c q3" style="font-weight:800">รวม</th>
      <th class="c q4">ก.ค.</th><th class="c q4">ส.ค.</th><th class="c q4">ก.ย.</th><th class="c q4" style="font-weight:800">รวม</th>
    </tr>
  </thead>
  <tbody>${rows}</tbody>
  <tfoot><tr>
    <td colspan="3">รวม</td><td class="r">${fmt(T.t)}</td>
    ${tc(T.q1.oct)}${tc(T.q1.nov)}${tc(T.q1.dec)}<td class="r" style="color:var(--blue);font-weight:700">${fmt(T.q1.total)}</td>
    ${tc(T.q2.jan)}${tc(T.q2.feb)}${tc(T.q2.mar)}<td class="r" style="color:var(--teal);font-weight:700">${fmt(T.q2.total)}</td>
    ${tc(T.q3.apr)}${tc(T.q3.may)}${tc(T.q3.jun)}<td class="r" style="color:var(--amber);font-weight:700">${fmt(T.q3.total)}</td>
    ${tc(T.q4.jul)}${tc(T.q4.aug)}${tc(T.q4.sep)}<td class="r" style="color:var(--rose);font-weight:700">${fmt(T.q4.total)}</td>
  </tr></tfoot>
</table></div>`;
}

// ============================================================
// PROJECT ALLOCATION PAGE
// ============================================================
function renderProject(){
  const projs=D.projects;
  document.getElementById('content').innerHTML=`<div class="fi">
<div class="ph">
  <div class="pt">จัดสรรเป้าหมายรายโครงการ</div>
  <div class="ps">แสดงการจัดสรรเป้าหมายของแต่ละโครงการให้กับหน่วยงานและจังหวัดต่างๆ ทั่วประเทศ</div>
</div>
<div class="proj-select-wrap">
  <select class="proj-select" id="projSel" onchange="changeProjSel(this.value)">
    ${projs.map(p=>`<option value="${p.num}" ${S.projNum==p.num?'selected':''}>โครงการ ${p.num}: ${p.name}</option>`).join('')}
  </select>
</div>
<div class="fbar">
  <div class="cpills" id="catPills" style="margin-bottom:0">
    <div class="cpill ${S.pcat==='all'?'active':''}" style="background:var(--purple);color:#fff;border-color:var(--purple)" data-c="all" onclick="setProjCat('all')">ทั้งหมด</div>
    <div class="cpill ${S.pcat==='จังหวัด'?'active':''}" style="background:rgba(16,185,129,.12);color:var(--green);border-color:rgba(16,185,129,.35)" data-c="จังหวัด" onclick="setProjCat('จังหวัด')">📍 เฉพาะจังหวัด (76 จังหวัด)</div>
    <div class="cpill ${S.pcat==='ส่วนกลาง'?'active':''}" style="background:rgba(108,99,255,.12);color:var(--purple);border-color:rgba(108,99,255,.35)" data-c="ส่วนกลาง" onclick="setProjCat('ส่วนกลาง')">ส่วนกลาง</div>
    <div class="cpill ${S.pcat==='ศูนย์ภาค'?'active':''}" style="background:rgba(139,92,246,.12);color:#8b5cf6;border-color:rgba(139,92,246,.35)" data-c="ศูนย์ภาค" onclick="setProjCat('ศูนย์ภาค')">ศูนย์ภาค</div>
    <div class="cpill ${S.pcat==='ด่าน'?'active':''}" style="background:rgba(245,158,11,.12);color:var(--amber);border-color:rgba(245,158,11,.35)" data-c="ด่าน" onclick="setProjCat('ด่าน')">ด่าน</div>
  </div>
  <div class="fsearch" style="margin-left:auto">
    <i class="fas fa-search"></i>
    <input type="text" id="pSearchInput" placeholder="ค้นหาจังหวัด หรือหน่วยงาน..." value="${S.psearch}" oninput="setProjSearch(this.value)">
  </div>
  <div class="vtabs" style="margin-bottom:0">
    <button class="vtab ${S.pview==='quarter'?'active':''}" id="pvt-q" onclick="setProjView('quarter')"><i class="fas fa-chart-simple"></i> ไตรมาส</button>
    <button class="vtab ${S.pview==='month'?'active':''}" id="pvt-m" onclick="setProjView('month')"><i class="fas fa-calendar-alt"></i> รายเดือน (12 เดือน)</button>
  </div>
</div>
<div id="projContent"></div>
</div>`;
  renderProjAlloc();
}

function changeProjSel(num){ S.projNum=parseInt(num); renderProjAlloc(); }
function setProjCat(cat){
  S.pcat=cat;
  document.querySelectorAll('#catPills .cpill').forEach(el=>{
    const c=el.getAttribute('data-c');
    const col=c==='จังหวัด'?'var(--green)':(CC[c]||'var(--purple)');
    if(c===cat){
      el.style.background=c==='all'?'var(--purple)':col;
      el.style.color='#fff';
      el.style.borderColor=c==='all'?'var(--purple)':col;
    } else {
      el.style.background=c==='all'?'rgba(108,99,255,.1)':col+'15';
      el.style.color=c==='all'?'var(--purple)':col;
      el.style.borderColor=c==='all'?'rgba(108,99,255,.3)':col+'40';
    }
  });
  renderProjAlloc();
}

function setProjSearch(q){ S.psearch=q.trim(); renderProjAlloc(); }
function setProjView(v){
  S.pview=v;
  document.getElementById('pvt-q')?.classList.toggle('active',v==='quarter');
  document.getElementById('pvt-m')?.classList.toggle('active',v==='month');
  renderProjAlloc();
}

function renderProjAlloc(){
  const pNum=S.projNum;
  const proj=D.projects.find(p=>p.num===pNum);
  if(!proj) return;
  const pIdx=D.projects.indexOf(proj);
  const color=PC[pIdx%PC.length];

  // Collect all units that have this project allocated
  let rawAlloc=D.units.map(u=>{
    const p=u.projects.find(x=>x.num===pNum);
    if(!p || p.target===0) return null;
    return {id:u.id, name:u.name, cat:u.category, target:p.target,
      q1:p.q1?.total||0, q2:p.q2?.total||0, q3:p.q3?.total||0, q4:p.q4?.total||0,
      oct:p.q1?.oct||0, nov:p.q1?.nov||0, dec:p.q1?.dec||0,
      jan:p.q2?.jan||0, feb:p.q2?.feb||0, mar:p.q2?.mar||0,
      apr:p.q3?.apr||0, may:p.q3?.may||0, jun:p.q3?.jun||0,
      jul:p.q4?.jul||0, aug:p.q4?.aug||0, sep:p.q4?.sep||0,
      sheet:u.sheet};
  }).filter(Boolean);

  let alloc=rawAlloc;
  if(S.pcat!=='all') alloc=alloc.filter(a=>a.cat===S.pcat);
  if(S.psearch) alloc=alloc.filter(a=>a.name.toLowerCase().includes(S.psearch.toLowerCase()));
  alloc.sort((a,b)=>b.target-a.target);

  const grand=alloc.reduce((s,a)=>s+a.target,0);
  const gq1=alloc.reduce((s,a)=>s+a.q1,0);
  const gq2=alloc.reduce((s,a)=>s+a.q2,0);
  const gq3=alloc.reduce((s,a)=>s+a.q3,0);
  const gq4=alloc.reduce((s,a)=>s+a.q4,0);
  const provCount=alloc.filter(a=>a.cat==='จังหวัด').length;
  const punit=proj.unit||'';

  const cv=(v,cls='')=>`<td class="${cls}" style="${v>0?'':'color:#cdd5df'}">${v>0?fmt(v):'-'}</td>`;

  let tableHtml = '';
  if(alloc.length===0){
    tableHtml = `<div style="text-align:center;padding:40px;color:var(--light)"><i class="fas fa-inbox" style="font-size:2rem;opacity:.3;margin-bottom:10px;display:block"></i>ไม่พบหน่วยงานหรือจังหวัดที่ตรงตามเงื่อนไข</div>`;
  } else if(S.pview==='quarter'){
    tableHtml = `<div class="tw"><table>
      <thead><tr>
        <th>#</th><th>ชื่อหน่วยงาน / จังหวัด</th><th>ประเภท</th>
        <th class="r">เป้าหมายรวม</th>
        <th class="r q1">Q1</th><th class="r q2">Q2</th><th class="r q3">Q3</th><th class="r q4">Q4</th>
        <th class="c">รายละเอียด</th>
      </tr></thead>
      <tbody>
      ${alloc.map((a,i)=>{
        const cc=CC[a.cat]||'#6c63ff';
        return `<tr>
          <td style="color:var(--muted);font-size:.75rem">${i+1}</td>
          <td class="bold"><a href="javascript:void(0)" onclick="pickUnit(${a.id});"
            style="color:var(--purple);text-decoration:none"
            onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">${a.name}</a></td>
          <td><span style="font-size:.72rem;font-weight:600;padding:2px 8px;border-radius:50px;background:${cc}15;color:${cc}">${a.cat}</span></td>
          <td class="r bold" style="color:${color}">${fmt(a.target)}</td>
          <td class="r qt1">${a.q1>0?fmt(a.q1):'-'}</td>
          <td class="r qt2">${a.q2>0?fmt(a.q2):'-'}</td>
          <td class="r qt3">${a.q3>0?fmt(a.q3):'-'}</td>
          <td class="r qt4">${a.q4>0?fmt(a.q4):'-'}</td>
          <td class="c"><button onclick="pickUnit(${a.id});"
            style="padding:3px 10px;border-radius:6px;border:1px solid ${color};color:${color};background:${color}0d;cursor:pointer;font-size:.73rem;font-family:'Sarabun',sans-serif">
            เปิดดู <i class="fas fa-arrow-right" style="font-size:.65rem"></i>
          </button></td>
        </tr>`;
      }).join('')}
      </tbody>
      <tfoot><tr>
        <td colspan="3">รวม (${alloc.length} รายการ)</td>
        <td class="r">${fmt(grand)}</td>
        <td class="r" style="color:var(--blue)">${fmt(gq1)}</td>
        <td class="r" style="color:var(--teal)">${fmt(gq2)}</td>
        <td class="r" style="color:var(--amber)">${fmt(gq3)}</td>
        <td class="r" style="color:var(--rose)">${fmt(gq4)}</td>
        <td></td>
      </tr></tfoot>
    </table></div>`;
  } else {
    // 12-month table
    const M_TOTAL = {oct:0,nov:0,dec:0,jan:0,feb:0,mar:0,apr:0,may:0,jun:0,jul:0,aug:0,sep:0};
    alloc.forEach(a=>{
      ['oct','nov','dec','jan','feb','mar','apr','may','jun','jul','aug','sep'].forEach(m=>{
        M_TOTAL[m]+=(a[m]||0);
      });
    });
    tableHtml = `<div class="tw" style="overflow:auto"><table style="min-width:1050px">
      <thead>
        <tr>
          <th rowspan="2">#</th><th rowspan="2">ชื่อหน่วยงาน / จังหวัด</th><th rowspan="2">ประเภท</th><th rowspan="2" class="r">เป้าหมาย</th>
          <th colspan="4" class="c q1">ไตรมาส 1 (ปี 2569)</th>
          <th colspan="4" class="c q2">ไตรมาส 2</th>
          <th colspan="4" class="c q3">ไตรมาส 3</th>
          <th colspan="4" class="c q4">ไตรมาส 4</th>
        </tr>
        <tr>
          <th class="c q1">ต.ค.</th><th class="c q1">พ.ย.</th><th class="c q1">ธ.ค.</th><th class="c q1" style="font-weight:800">รวม</th>
          <th class="c q2">ม.ค.</th><th class="c q2">ก.พ.</th><th class="c q2">มี.ค.</th><th class="c q2" style="font-weight:800">รวม</th>
          <th class="c q3">เม.ย.</th><th class="c q3">พ.ค.</th><th class="c q3">มิ.ย.</th><th class="c q3" style="font-weight:800">รวม</th>
          <th class="c q4">ก.ค.</th><th class="c q4">ส.ค.</th><th class="c q4">ก.ย.</th><th class="c q4" style="font-weight:800">รวม</th>
        </tr>
      </thead>
      <tbody>
      ${alloc.map((a,i)=>{
        const cc=CC[a.cat]||'#6c63ff';
        return `<tr>
          <td style="color:var(--muted);font-size:.75rem">${i+1}</td>
          <td class="bold"><a href="javascript:void(0)" onclick="pickUnit(${a.id});"
            style="color:var(--purple);text-decoration:none"
            onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">${a.name}</a></td>
          <td><span style="font-size:.7rem;font-weight:600;padding:2px 7px;border-radius:50px;background:${cc}15;color:${cc}">${a.cat}</span></td>
          <td class="r bold" style="color:${color}">${fmt(a.target)}</td>
          ${cv(a.oct)}${cv(a.nov)}${cv(a.dec)}${cv(a.q1,'r qt1')}
          ${cv(a.jan)}${cv(a.feb)}${cv(a.mar)}${cv(a.q2,'r qt2')}
          ${cv(a.apr)}${cv(a.may)}${cv(a.jun)}${cv(a.q3,'r qt3')}
          ${cv(a.jul)}${cv(a.aug)}${cv(a.sep)}${cv(a.q4,'r qt4')}
        </tr>`;
      }).join('')}
      </tbody>
      <tfoot><tr>
        <td colspan="3">รวม (${alloc.length} รายการ)</td>
        <td class="r">${fmt(grand)}</td>
        <td class="r">${fmt(M_TOTAL.oct)}</td><td class="r">${fmt(M_TOTAL.nov)}</td><td class="r">${fmt(M_TOTAL.dec)}</td>
        <td class="r" style="color:var(--blue);font-weight:700">${fmt(gq1)}</td>
        <td class="r">${fmt(M_TOTAL.jan)}</td><td class="r">${fmt(M_TOTAL.feb)}</td><td class="r">${fmt(M_TOTAL.mar)}</td>
        <td class="r" style="color:var(--teal);font-weight:700">${fmt(gq2)}</td>
        <td class="r">${fmt(M_TOTAL.apr)}</td><td class="r">${fmt(M_TOTAL.may)}</td><td class="r">${fmt(M_TOTAL.jun)}</td>
        <td class="r" style="color:var(--amber);font-weight:700">${fmt(gq3)}</td>
        <td class="r">${fmt(M_TOTAL.jul)}</td><td class="r">${fmt(M_TOTAL.aug)}</td><td class="r">${fmt(M_TOTAL.sep)}</td>
        <td class="r" style="color:var(--rose);font-weight:700">${fmt(gq4)}</td>
      </tr></tfoot>
    </table></div>`;
  }

  document.getElementById('projContent').innerHTML=`
<div class="kpi-row" style="margin-bottom:14px">
  <div class="kpi" style="border-top:3px solid ${color}">
    <div class="kpi-ico" style="background:${color}15;color:${color}"><i class="fas fa-bullseye"></i></div>
    <div><div class="kpi-l">เป้าหมายรวม</div><div class="kpi-v">${fmt(grand)}</div><div class="kpi-s">${punit}</div></div>
  </div>
  <div class="kpi" style="border-top:3px solid var(--green)">
    <div class="kpi-ico" style="background:rgba(16,185,129,.12);color:var(--green)"><i class="fas fa-city"></i></div>
    <div><div class="kpi-l">จังหวัดที่จัดสรร</div><div class="kpi-v" style="color:var(--green)">${provCount}</div><div class="kpi-s">จาก 76 จังหวัด</div></div>
  </div>
  <div class="kpi" style="border-top:3px solid var(--blue)">
    <div class="kpi-ico" style="background:rgba(59,130,246,.12);color:var(--blue)"><i class="fas fa-building"></i></div>
    <div><div class="kpi-l">หน่วยงานทั้งหมดที่ได้รับ</div><div class="kpi-v">${alloc.length}</div><div class="kpi-s">หน่วยงาน</div></div>
  </div>
  <div class="kpi" style="border-top:3px solid var(--blue)">
    <div class="kpi-ico" style="background:rgba(59,130,246,.1);color:var(--blue)"><i class="fas fa-sun"></i></div>
    <div><div class="kpi-l">Q1 (ต.ค.–ธ.ค.)</div><div class="kpi-v" style="color:var(--blue)">${fmt(gq1)}</div></div>
  </div>
  <div class="kpi" style="border-top:3px solid var(--teal)">
    <div class="kpi-ico" style="background:rgba(20,184,166,.1);color:var(--teal)"><i class="fas fa-sun"></i></div>
    <div><div class="kpi-l">Q2 (ม.ค.–มี.ค.)</div><div class="kpi-v" style="color:var(--teal)">${fmt(gq2)}</div></div>
  </div>
  <div class="kpi" style="border-top:3px solid var(--amber)">
    <div class="kpi-ico" style="background:rgba(245,158,11,.1);color:var(--amber)"><i class="fas fa-sun"></i></div>
    <div><div class="kpi-l">Q3 (เม.ย.–มิ.ย.)</div><div class="kpi-v" style="color:var(--amber)">${fmt(gq3)}</div></div>
  </div>
  <div class="kpi" style="border-top:3px solid var(--rose)">
    <div class="kpi-ico" style="background:rgba(244,63,94,.1);color:var(--rose)"><i class="fas fa-sun"></i></div>
    <div><div class="kpi-l">Q4 (ก.ค.–ก.ย.)</div><div class="kpi-v" style="color:var(--rose)">${fmt(gq4)}</div></div>
  </div>
</div>

<div class="slbl">การจัดสรรรายหน่วยงานและจังหวัด <span class="sbadge">${alloc.length} หน่วยงาน</span></div>
${tableHtml}`;
}

// INIT
document.addEventListener('DOMContentLoaded',()=>{
  initSidebar();
  initResizer();
  go('overview');
});
</script>
</body>
</html>""".replace('DASHBOARD_DATA_PLACEHOLDER', dj)

    # Inject data
    html = html.replace('""" + dj + r"""', dj, 1)

    for fn in ['dashboard.html', 'index.html']:
        fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), fn)
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Saved: {fp}")
    print(f"Size: {len(html):,} bytes")

if __name__ == '__main__':
    build()
