"""
HW-OPC 国产化智能体硬件技术转移专用平台 v1.0
从论文到产品 · 从算法到硬件 · 全链条AI赋能
"""
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="HW-OPC 国产化智能体硬件平台", page_icon="🔧", layout="wide", initial_sidebar_state="expanded")

# ─── 全局CSS ───
st.markdown("""<style>
:root{--primary:#0f3460;--accent:#e94560;--bg:#f8f9fa;--card:#fff;--text:#2d3436;--muted:#636e72;--border:#dfe6e9;--success:#00b894;--warning:#fdcb6e;--danger:#d63031;--hw-blue:#0984e3;--hw-purple:#6c5ce7;--hw-orange:#e17055;--hw-green:#00b894}
.stApp{background:var(--bg)}
.main-header{background:linear-gradient(135deg,#0f3460 0%,#16213e 40%,#1a1a2e 100%);padding:2rem 2.5rem;border-radius:0 0 1.5rem 1.5rem;margin:-1rem -1rem 1.5rem;color:#fff;position:relative;overflow:hidden}
.main-header::after{content:'';position:absolute;top:-50%;right:-10%;width:300px;height:300px;background:radial-gradient(circle,rgba(233,69,96,.15),transparent 70%);border-radius:50%}
.main-header h1{font-size:2rem;font-weight:800;margin:0 0 .2rem;letter-spacing:-.5px}
.main-header .subtitle{opacity:.85;margin:0 0 .6rem;font-size:.95rem}
.main-header .chips{display:flex;flex-wrap:wrap;gap:.3rem}
.chip{display:inline-block;padding:.2rem .7rem;border-radius:999px;font-size:.7rem;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08)}
.chip.hot{border-color:rgba(233,69,96,.5);background:rgba(233,69,96,.15)}
.card{background:var(--card);border-radius:1rem;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,.06);border:1px solid var(--border);margin-bottom:1rem}
.card h3{margin:0 0 .5rem;font-size:1.05rem}
.metric-box{background:var(--card);border-radius:1rem;padding:1.2rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.04);border:1px solid var(--border)}
.metric-box .num{font-size:1.8rem;font-weight:800;color:var(--primary)}
.metric-box .label{font-size:.75rem;color:var(--muted);margin-top:.2rem}
.impossible{background:linear-gradient(135deg,#ff6b6b,#ee5a24);color:#fff;border-radius:.8rem;padding:1rem 1.2rem;margin:.8rem 0}
.impossible .before{opacity:.7;text-decoration:line-through;font-size:.85rem}
.impossible .after{font-weight:700;font-size:1rem;margin-top:.3rem}
.pipeline{display:flex;align-items:center;justify-content:center;gap:.3rem;padding:1rem 0;flex-wrap:wrap}
.step{background:var(--primary);color:#fff;padding:.4rem .8rem;border-radius:.5rem;font-size:.8rem;font-weight:600;white-space:nowrap}
.arrow{color:var(--muted);font-weight:700}
.step.active{background:var(--accent);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(233,69,96,.4)}50%{box-shadow:0 0 0 8px rgba(233,69,96,0)}}
.feature-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem}
.feature-card{background:var(--card);border-radius:1rem;padding:1.2rem;border:1px solid var(--border);transition:all .2s}
.feature-card:hover{border-color:var(--accent);box-shadow:0 4px 16px rgba(233,69,96,.1)}
.feature-card .icon{font-size:1.8rem;margin-bottom:.5rem}
.feature-card h4{margin:0 0 .3rem;font-size:.95rem}
.feature-card p{color:var(--muted);font-size:.8rem;margin:0 0 .5rem}
.feature-card .tag{display:inline-block;font-size:.65rem;padding:.1rem .4rem;border-radius:4px;background:#f0f4ff;color:var(--primary)}
.status-badge{display:inline-block;padding:.15rem .5rem;border-radius:999px;font-size:.7rem;font-weight:600}
.status-badge.green{background:#e8f5e9;color:#2e7d32}
.status-badge.yellow{background:#fff8e1;color:#f57f17}
.status-badge.red{background:#ffebee;color:#c62828}
.status-badge.blue{background:#e3f2fd;color:#1565c0}
.chain-node{display:inline-flex;align-items:center;gap:.5rem;background:var(--card);border:1px solid var(--border);border-radius:.8rem;padding:.6rem 1rem;margin:.3rem}
.chain-node .dot{width:10px;height:10px;border-radius:50%}
.chain-arrow{color:var(--muted);font-size:1.2rem;margin:0 .2rem}
</style>""", unsafe_allow_html=True)

# ─── Session State ───
for k in ["evaluations","matches","translations","analyses","deals","cert_apps","proto_projects"]:
    if k not in st.session_state:
        st.session_state[k] = []

# ─── 侧边栏 ───
with st.sidebar:
    st.markdown("### 🔧 HW-OPC")
    st.caption("国产化智能体硬件<br>技术转移专用平台")
    st.markdown("---")
    nav = st.radio("导航", [
        "🏠 总览",
        "📊 硬件评估 HWEval",
        "🔗 供应链图谱 SupplyChain",
        "🔄 硬件翻译 HWTranslator",
        "🧬 四角色工作台 QuadHelix",
        "📡 硬件雷达 HWRadar",
        "📋 认证导航 CertNav",
        "🏭 打样工坊 Prototyping",
        "🌐 社交交易 SocialTrade",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""
    <div style="font-size:.8rem;color:var(--muted)">
    <strong>产业链覆盖</strong><br>
    🧠 算法层<br>
    🔲 芯片层<br>
    📟 硬件层<br>
    💻 系统层<br>
    🤖 应用层<br>
    📦 产品层<br>
    🏪 市场层
    </div>""", unsafe_allow_html=True)
    st.caption(f"v1.0 · {datetime.now().strftime('%Y-%m-%d')}")

# ─── 路由 ───
modules = {
    "总览": "pages.home",
    "硬件评估": "pages.hw_eval",
    "供应链图谱": "pages.supply_chain",
    "硬件翻译": "pages.hw_translator",
    "四角色工作台": "pages.quad_helix",
    "硬件雷达": "pages.hw_radar",
    "认证导航": "pages.cert_nav",
    "打样工坊": "pages.prototyping",
    "社交交易": "pages.social_trade",
}
for key, mod in modules.items():
    if key in nav:
        parts = mod.rsplit(".", 1)
        m = __import__(parts[0], fromlist=[parts[1]])
        getattr(m, parts[1]).render()
        break
