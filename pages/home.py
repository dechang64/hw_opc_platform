"""首页 - 国产化智能体硬件技术转移全链条"""
import streamlit as st

def render():
    st.markdown("""<div class="main-header">
    <h1>🔧 HW-OPC 国产化智能体硬件平台</h1>
    <p class="subtitle">从论文到产品 · 从算法到硬件 · 全链条AI赋能技术转移</p>
    <div class="chips">
        <span class="chip hot">🔥 国产替代</span>
        <span class="chip hot">🔥 新质生产力</span>
        <span class="chip">端侧大模型</span>
        <span class="chip">NPU适配</span>
        <span class="chip">智能体硬件</span>
        <span class="chip">AI Pin / AI眼镜 / 端侧盒子</span>
        <span class="chip">算法备案</span>
        <span class="chip">3C认证</span>
    </div>
</div>""", unsafe_allow_html=True)

    # 全链路流程
    st.markdown("### 🔄 智能体硬件产品化全链路")
    st.markdown("""<div class="pipeline">
        <span class="step">🧠 算法评估</span><span class="arrow">→</span>
        <span class="step">🔲 芯片选型</span><span class="arrow">→</span>
        <span class="step">🔗 供应链匹配</span><span class="arrow">→</span>
        <span class="step">🔄 多版本翻译</span><span class="arrow">→</span>
        <span class="step">🧬 四角色协同</span><span class="arrow">→</span>
        <span class="step">📡 技术雷达</span><span class="arrow">→</span>
        <span class="step">📋 认证导航</span><span class="arrow">→</span>
        <span class="step">🏭 打样量产</span><span class="arrow">→</span>
        <span class="step active">💰 交易成交</span>
    </div>""", unsafe_allow_html=True)

    # 产业链深度
    st.markdown("### 🏗️ 七层产业链 · 每层都有技术转移痛点")
    layers = [
        ("🧠", "算法层", "端侧模型压缩、多模态感知、意图理解、Agent框架", "高校有论文→不会部署到硬件"),
        ("🔲", "芯片层", "NPU架构、存算一体、国产替代方案选型", "算法团队不懂芯片→选错NPU", True),
        ("📟", "硬件层", "PCB设计、天线、传感器选型、热设计、ID设计", "算法团队不会画板子→找不到ODM", True),
        ("💻", "系统层", "RTOS/嵌入式Linux、驱动开发、OTA升级", "高校不教嵌入式→系统适配难"),
        ("🤖", "应用层", "Agent技能编排、语音交互、场景适配", "技术好但体验差→产品没人用"),
        ("📦", "产品层", "工业设计、开模、量产、3C/SRRC认证", "从原型到量产的死亡之谷", True),
        ("🏪", "市场层", "渠道、品牌、开发者生态、售后服务", "技术出身不会卖→好产品死在仓库"),
    ]
    for icon, name, desc, pain, *hot in layers:
        border = "border-left:3px solid var(--accent)" if hot else ""
        st.markdown(f"""<div class="card" style="{border}">
            <h3>{icon} {name}</h3>
            <p><strong>内容</strong>：{desc}</p>
            <p><strong>痛点</strong>：{pain}</p>
        </div>""", unsafe_allow_html=True)

    # 九大功能模块
    st.markdown("### 🧩 九大专用功能模块")
    st.caption("每个模块都深入到智能体硬件领域，不是通用工具，而是领域专家系统")

    features = [
        ("📊", "硬件评估 HWEval", "芯片Benchmark+算法适配+BOM成本+国产化率",
         "输入算法参数→输出芯片推荐+成本估算+国产化率", "P0"),
        ("🔗", "供应链图谱 SupplyChain", "算法→芯片→ODM→认证 全链路可视化",
         "自动补链：有算法→推荐芯片→匹配ODM→规划认证", "P0"),
        ("🔄", "硬件翻译 HWTranslator", "硬件规格书→4个专业版本",
         "投资人版/产品经理版/供应链版/认证版", "P0"),
        ("🧬", "四角色工作台 QuadHelix", "算法专家+硬件PM+供应链专家+认证顾问",
         "四Agent协同分析同一硬件项目", "P0"),
        ("📡", "硬件雷达 HWRadar", "芯片路线图+NPU趋势+传感器价格+国产替代进度",
         "告诉OPC'现在做这个硬件的最佳时机'", "P1"),
        ("📋", "认证导航 CertNav", "3C/SRRC/网安/算法备案 全流程",
         "自动生成认证清单+文档模板+费用估算", "P1"),
        ("🏭", "打样工坊 Prototyping", "EVT→DVT→PVT→MP 全流程管理",
         "成本估算+排期规划+风险预警+资源共享", "P1"),
        ("🌐", "社交交易 SocialTrade", "硬件开发者社区+供应链对接+交易管理",
         "AI撮合+全流程Deal追踪+收益分配", "P1"),
        ("🌡️", "产业温度计", "实时测量国产化智能体硬件产业健康度",
         "反哺政策制定，自动生成产业报告", "P2"),
    ]

    cols = st.columns(3)
    for i, (icon, name, desc, detail, priority) in enumerate(features):
        with cols[i % 3]:
            pcolor = {"P0":"var(--danger)","P1":"var(--warning)","P2":"var(--hw-blue)"}.get(priority,"var(--muted)")
            st.markdown(f"""<div class="feature-card">
                <div class="icon">{icon}</div>
                <h4>{name}</h4>
                <p>{desc}</p>
                <p style="font-size:.75rem">{detail}</p>
                <span class="tag" style="background:{pcolor};color:#fff">{priority}</span>
            </div>""", unsafe_allow_html=True)

    # 与通用平台的区别
    st.markdown("### ⚔️ 与通用技术转移平台的本质区别")
    st.markdown("""<div class="card">
    <table style="width:100%;font-size:.82rem;border-collapse:collapse">
    <tr style="background:#f0f4ff"><th style="padding:.5rem;text-align:left">维度</th><th>通用平台</th><th style="background:#e8f5e9;font-weight:700">HW-OPC专用平台</th></tr>
    <tr><td style="padding:.5rem;border-bottom:1px solid #eee">评估维度</td><td>通用SWOT+打分</td><td style="background:#e8f5e9">芯片TOPS/功耗/算法FLOPs/BOM成本/国产化率</td></tr>
    <tr><td style="padding:.5rem;border-bottom:1px solid #eee">匹配逻辑</td><td>关键词匹配专利</td><td style="background:#e8f5e9">算法→芯片兼容性→ODM能力→认证要求</td></tr>
    <tr><td style="padding:.5rem;border-bottom:1px solid #eee">翻译版本</td><td>投资人/CEO/院长</td><td style="background:#e8f5e9">投资人/产品经理/供应链/认证顾问</td></tr>
    <tr><td style="padding:.5rem;border-bottom:1px solid #eee">角色协同</td><td>教授+CEO+律师</td><td style="background:#e8f5e9">算法专家+硬件PM+供应链专家+认证顾问</td></tr>
    <tr><td style="padding:.5rem;border-bottom:1px solid #eee">技术雷达</td><td>通用技术生命周期</td><td style="background:#e8f5e9">芯片制程/NPU算力/传感器价格/国产替代进度</td></tr>
    <tr><td style="padding:.5rem;border-bottom:1px solid #eee">认证支持</td><td>❌</td><td style="background:#e8f5e9">✅ 3C/SRRC/网安/算法备案全流程</td></tr>
    <tr><td style="padding:.5rem;border-bottom:1px solid #eee">量产支持</td><td>❌</td><td style="background:#e8f5e9">✅ EVT→DVT→PVT→MP全流程</td></tr>
    <tr><td style="padding:.5rem">壁垒</td><td>功能可被抄</td><td style="background:#e8f5e9;font-weight:700">领域Know-how抄不走</td></tr>
    </table></div>""", unsafe_allow_html=True)
