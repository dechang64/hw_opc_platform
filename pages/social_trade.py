"""社交交易 SocialTrade - 硬件开发者社区+供应链对接+交易管理"""
import streamlit as st, random
from datetime import datetime

def render():
    st.markdown("# 🌐 社交交易 SocialTrade")
    st.markdown("""<div class="impossible">
        <div class="before">❌ 以前：做AI硬件的人找不到芯片供应商、ODM找不到算法团队、投资人找不到好项目</div>
        <div class="after">✅ 现在：硬件开发者社区+供应链智能对接+全流程交易管理，一个平台搞定所有连接</div>
    </div>""", unsafe_allow_html=True)
    st.caption("📐 理论支撑：网络效应(Metcalfe) + 双边市场(Rochet & Tirole) + 声誉机制(Spence)")

    tab1,tab2,tab3,tab4 = st.tabs(["🧑‍🤝‍🧑 社区动态","🔗 供需对接","💰 交易管理","📊 数据看板"])

    with tab1:
        st.markdown("### 🧑‍🤝‍🧑 硬件开发者社区")

        # 发布动态
        with st.expander("✏️ 发布动态", expanded=False):
            post_type = st.selectbox("类型", ["📊 评估分享","💡 经验分享","🆘 寻求合作","📢 项目进展","🔧 技术讨论"])
            content = st.text_area("内容", placeholder="分享你的AI硬件开发经验、寻求合作、展示项目进展...")
            if st.button("发布", use_container_width=True):
                st.success("动态已发布！")

        # 模拟社区动态
        posts = [
            {"author":"张工@瑞芯微","avatar":"🧑‍💻","type":"🔧 技术讨论","time":"2小时前",
             "content":"RK3588M跑7B量化模型实测：INT4下推理速度12 tokens/s，内存占用3.2GB。INT8下8 tokens/s但精度更好。建议端侧场景用INT4+投机解码。","likes":23,"comments":8},
            {"author":"李总@立讯精密","avatar":"👨‍💼","type":"📢 项目进展","time":"5小时前",
             "content":"我们刚完成一款AI Pin的PVT，良率92%。关键经验：1)天线设计要预留调试空间 2)热设计用石墨烯膜比均热板效果好 3)NPU功耗管理需要软硬件协同。","likes":45,"comments":15},
            {"author":"王博士@清华","avatar":"👨‍🔬","type":"📊 评估分享","time":"1天前",
             "content":"用HW-OPC评估了我们实验室的端侧多模态模型，综合评分87。平台建议的芯片选型(RK3588M)和我们的实测结果一致。下一步准备启动EVT。","likes":67,"comments":22},
            {"author":"陈总@某VC","avatar":"💼","type":"🆘 寻求合作","time":"1天前",
             "content":"我们基金专注AI硬件早期投资，已投3个AI Pin/眼镜项目。正在寻找：1)有差异化算法的团队 2)国产芯片适配方案 3)供应链资源。欢迎联系。","likes":89,"comments":34},
            {"author":"赵工@歌尔","avatar":"🧑‍🔧","type":"💡 经验分享","time":"2天前",
             "content":"AI眼镜的光学方案对比：Birdbath方案成本低(¥50-80)但体积大，光波导方案体积小但成本高(¥200-500)。建议MVP用Birdbath，V2.0切光波导。","likes":56,"comments":19},
        ]

        for p in posts:
            st.markdown(f"""<div class="card">
                <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem">
                    <span style="font-size:1.5rem">{p['avatar']}</span>
                    <div>
                        <span style="font-weight:600">{p['author']}</span>
                        <span style="color:var(--muted);font-size:.8rem;margin-left:.5rem">{p['type']} · {p['time']}</span>
                    </div>
                </div>
                <p style="margin:0;font-size:.9rem;line-height:1.6">{p['content']}</p>
                <div style="margin-top:.5rem;display:flex;gap:1rem;font-size:.8rem;color:var(--muted)">
                    <span>👍 {p['likes']}</span>
                    <span>💬 {p['comments']}</span>
                    <span>🔄 转发</span>
                    <span>🔖 收藏</span>
                </div>
            </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🔗 供需智能对接")
        st.markdown("#### 📤 我要发布需求")
        demand_type = st.selectbox("需求类型", ["🔲 寻找芯片方案","🏭 寻找ODM/代工","🧠 寻找算法团队","📋 寻找认证服务","💰 寻找投资"])
        demand_desc = st.text_area("需求描述", placeholder="详细描述你的需求...")
        if st.button("发布需求", use_container_width=True):
            st.success("需求已发布！系统将智能匹配并推荐。")

        st.markdown("---")
        st.markdown("#### 📋 最新供需信息")
        demands = [
            {"type":"🧠 寻找算法团队","desc":"端侧语音Agent算法，需要支持离线唤醒+多轮对话+意图理解，目标芯片RK3588M","budget":"¥20-50万","location":"北京","time":"3小时前"},
            {"type":"🔲 寻找芯片方案","desc":"AI眼镜主控芯片，需要NPU>6TOPS，功耗<3W，支持双目摄像头","budget":"待定","location":"深圳","time":"6小时前"},
            {"type":"🏭 寻找ODM","desc":"AI Pin量产，月产5000台，需要精密组装+天线调试能力","budget":"¥30-50万(开模)","location":"广东","time":"1天前"},
            {"type":"📋 寻找认证服务","desc":"AI硬件产品3C+SRRC+算法备案一站式服务","budget":"¥10-20万","location":"全国","time":"1天前"},
            {"type":"💰 寻找投资","desc":"国产化端侧AI盒子，已完成EVT，寻求天使轮/Pre-A","budget":"500-1000万","location":"上海","time":"2天前"},
        ]
        for d in demands:
            st.markdown(f"""<div class="card">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <span style="font-weight:600">{d['type']}</span>
                    <span style="font-size:.75rem;color:var(--muted)">{d['time']}</span>
                </div>
                <p style="margin:.3rem 0">{d['desc']}</p>
                <div style="display:flex;gap:1rem;font-size:.8rem;color:var(--muted)">
                    <span>💰 {d['budget']}</span>
                    <span>📍 {d['location']}</span>
                    <span style="color:var(--hw-blue)">💬 联系</span>
                    <span style="color:var(--hw-blue)">🔖 收藏</span>
                </div>
            </div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("### 💰 交易管理")
        st.markdown("#### 📋 交易流水线")
        st.markdown("""
        ```
        意向接触 → 需求确认 → 方案报价 → 合同签署 → 里程碑付款 → 交付验收 → 结算完成
        ```
        """)

        deals = [
            {"name":"端侧语音Agent算法授权","party":"清华NLP实验室","stage":"合同签署","amount":"¥35万","progress":60},
            {"name":"AI Pin ODM代工","party":"立讯精密","stage":"方案报价","amount":"¥45万","progress":30},
            {"name":"3C+SRRC认证服务","party":"某认证机构","stage":"交付验收","amount":"¥8万","progress":90},
        ]
        for d in deals:
            stage_colors = {"意向接触":"#dfe6e9","需求确认":"#74b9ff","方案报价":"#a29bfe","合同签署":"#fd79a8","里程碑付款":"#fdcb6e","交付验收":"#55efc4","结算完成":"#00b894"}
            color = stage_colors.get(d["stage"], "#dfe6e9")
            st.markdown(f"""<div class="card">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <span style="font-weight:600">{d['name']}</span>
                        <span style="font-size:.8rem;color:var(--muted);margin-left:.5rem">← {d['party']}</span>
                    </div>
                    <span style="font-weight:700;color:var(--hw-blue)">{d['amount']}</span>
                </div>
                <div style="margin-top:.5rem">
                    <div style="background:#eee;border-radius:999px;height:8px;overflow:hidden">
                        <div style="background:{color};height:100%;width:{d['progress']}%;border-radius:999px"></div>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:.75rem;color:var(--muted);margin-top:.2rem">
                        <span>{d['stage']}</span>
                        <span>{d['progress']}%</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    with tab4:
        st.markdown("### 📊 平台数据看板")
        c1,c2,c3,c4,c5 = st.columns(5)
        with c1:
            st.markdown(f"""<div class="metric-box" style="background:linear-gradient(135deg,#0984e3,#74b9ff)">
                <div class="num" style="color:#fff">2,847</div><div class="label" style="color:rgba(255,255,255,.8)">👥 注册开发者</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="metric-box" style="background:linear-gradient(135deg,#6c5ce7,#a29bfe)">
                <div class="num" style="color:#fff">156</div><div class="label" style="color:rgba(255,255,255,.8)">📦 活跃项目</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="metric-box" style="background:linear-gradient(135deg,#00b894,#55efc4)">
                <div class="num" style="color:#fff">89</div><div class="label" style="color:rgba(255,255,255,.8)">🤝 成功匹配</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="metric-box" style="background:linear-gradient(135deg,#e17055,#fab1a0)">
                <div class="num" style="color:#fff">23</div><div class="label" style="color:rgba(255,255,255,.8)">💰 成交交易</div></div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""<div class="metric-box" style="background:linear-gradient(135deg,#fdcb6e,#ffeaa7)">
                <div class="num" style="color:#fff">¥2.3亿</div><div class="label" style="color:rgba(255,255,255,.8)">📊 交易总额</div></div>""", unsafe_allow_html=True)

        st.markdown("#### 📈 月度趋势")
        st.markdown("""
        | 月份 | 新增用户 | 新增项目 | 匹配数 | 成交数 | 交易额 |
        |------|---------|---------|--------|--------|--------|
        | 2025-01 | 180 | 12 | 5 | 1 | ¥800万 |
        | 2025-02 | 220 | 15 | 8 | 2 | ¥1,500万 |
        | 2025-03 | 310 | 22 | 12 | 3 | ¥2,200万 |
        | 2025-04 | 450 | 28 | 18 | 5 | ¥3,800万 |
        | 2025-05 | 580 | 35 | 24 | 7 | ¥5,100万 |
        """)
