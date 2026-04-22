"""供应链图谱 SupplyChain - 算法→芯片→ODM→认证 全链路可视化"""
import streamlit as st, random
from datetime import datetime

# ─── 供应链数据库（模拟） ───
ODM_DB = [
    {"name":"立讯精密","capability":["AI Pin","AI眼镜","TWS","可穿戴"],"moq":"5000","lead_time":"60-90天","certifications":["ISO9001","ISO14001","IATF16949"],"location":"广东/江苏","strength":"精密制造+快速响应","price_level":"中高"},
    {"name":"歌尔股份","capability":["AI眼镜","AR/VR","智能音箱","TWS"],"moq":"3000","lead_time":"45-75天","certifications":["ISO9001","ISO14001"],"location":"山东/江苏","strength":"声学+光学+整机组装","price_level":"中"},
    {"name":"富士康","capability":["AI盒子","服务器","边缘设备"],"moq":"1000","lead_time":"30-60天","certifications":["ISO9001","ISO14001","ISO13485"],"location":"深圳/郑州","strength":"大规模量产+品质管控","price_level":"低"},
    {"name":"比亚迪电子","capability":["AI Pin","智能手机","可穿戴","IoT"],"moq":"5000","lead_time":"60-90天","certifications":["ISO9001","IATF16949"],"location":"深圳","strength":"垂直整合+电池+屏幕","price_level":"中"},
    {"name":"闻泰科技","capability":["AI开发板","IoT模组","边缘设备"],"moq":"2000","lead_time":"30-45天","certifications":["ISO9001","ISO14001"],"location":"浙江/江苏","strength":"半导体+产品集成","price_level":"中低"},
    {"name":"龙旗科技","capability":["AI Pin","智能音箱","IoT"],"moq":"3000","lead_time":"45-60天","certifications":["ISO9001"],"location":"上海/深圳","strength":"智能硬件设计+制造","price_level":"中"},
]

SENSOR_DB = [
    {"type":"IMU","domestic":["敏芯股份","明皜传感"],"foreign":["Bosch","ST","TDK"],"price":"¥3-15","localization":"60%"},
    {"type":"麦克风","domestic":["瑞声科技","歌尔微"],"foreign":["Knowles","Goertek"],"price":"¥2-10","localization":"80%"},
    {"type":"摄像头","domestic":["舜宇光学","欧菲光","丘钛科技"],"foreign":["Sony","Samsung","OmniVision"],"price":"¥15-80","localization":"70%"},
    {"type":"显示屏","domestic":["京东方","维信诺","天马"],"foreign":["Samsung","LG","JDI"],"price":"¥20-200","localization":"75%"},
    {"type":"触觉反馈","domestic":["瑞声科技","汇顶科技"],"foreign":["AAC","TDK"],"price":"¥5-20","localization":"70%"},
    {"type":"WiFi/BT","domestic":["乐鑫科技","恒玄科技"],"foreign":["Qualcomm","Broadcom","Realtek"],"price":"¥5-20","localization":"50%"},
    {"type":"电源管理","domestic":["矽力杰","芯朋微","晶丰明源"],"foreign":["TI","Dialog","Richtek"],"price":"¥3-12","localization":"65%"},
    {"type":"存储","domestic":["长江存储","兆易创新"],"foreign":["Samsung","SK Hynix","Micron"],"price":"¥10-50","localization":"40%"},
]

CERT_DB = [
    {"name":"3C认证","authority":"认监委","duration":"4-8周","cost":"¥2-5万","required":True,"scope":"所有电子产品"},
    {"name":"SRRC认证","authority":"工信部","duration":"6-10周","cost":"¥1-3万","required":True,"scope":"含无线电发射设备"},
    {"name":"NAL认证","authority":"工信部","duration":"4-6周","cost":"¥1-2万","required":True,"scope":"电信设备进网"},
    {"name":"网络安全评估","authority":"网信办","duration":"8-12周","cost":"¥5-15万","required":False,"scope":"联网AI设备"},
    {"name":"算法备案","authority":"网信办","duration":"4-8周","cost":"¥2-5万","required":True,"scope":"含AI算法的产品"},
    {"name":"ICP备案","authority":"工信部","duration":"1-2周","cost":"免费","required":True,"scope":"需联网的设备"},
]

def render():
    st.markdown("# 🔗 供应链图谱 SupplyChain")
    st.markdown("""<div class="impossible">
        <div class="before">❌ 以前：算法团队找不到合适的芯片和ODM，硬件厂不知道做什么产品——供需严重错配</div>
        <div class="after">✅ 现在：输入算法需求→自动推荐芯片→匹配ODM→规划认证→补全全链路</div>
    </div>""", unsafe_allow_html=True)
    st.caption("📐 理论支撑：交易成本经济学(Coase) + 双边市场理论(Rochet & Tirole) + 网络效应(Metcalfe)")

    tab1,tab2,tab3,tab4 = st.tabs(["🔗 供应链匹配","🏭 ODM厂商","📡 传感器/器件","📋 认证机构"])

    with tab1:
        st.markdown("### 🔗 智能体硬件供应链全链路")
        st.markdown("输入产品需求，自动生成完整供应链图谱")

        with st.form("supply_form"):
            c1,c2 = st.columns(2)
            with c1:
                product = st.selectbox("产品形态",["AI Pin","AI眼镜","端侧AI盒子","AI开发板"])
                npu_need = st.selectbox("NPU算力需求",["<2 TOPS","2-6 TOPS","6-15 TOPS",">15 TOPS"])
            with c2:
                localization = st.selectbox("国产化要求",["无要求",">60%",">80%",">90%"])
                cert_needed = st.multiselect("需要的认证",["3C认证","SRRC认证","算法备案","网络安全评估"],default=["3C认证","SRRC认证","算法备案"])

            submitted = st.form_submit_button("🔗 生成供应链图谱", type="primary", use_container_width=True)

        if submitted:
            st.markdown("---")
            st.markdown("#### 📍 您的供应链图谱")

            # 可视化供应链链路
            st.markdown("""
            <div style="overflow-x:auto;padding:1rem 0">
            <div style="display:flex;align-items:center;justify-content:center;gap:.3rem;min-width:900px;flex-wrap:nowrap">
                <div class="chain-node"><div class="dot" style="background:#6c5ce7"></div><div><strong>🧠 算法</strong><br><span style="font-size:.75rem;color:var(--muted)">端侧模型</span></div></div>
                <span class="chain-arrow">→</span>
                <div class="chain-node"><div class="dot" style="background:#0984e3"></div><div><strong>🔲 芯片</strong><br><span style="font-size:.75rem;color:var(--muted)">NPU SoC</span></div></div>
                <span class="chain-arrow">→</span>
                <div class="chain-node"><div class="dot" style="background:#00b894"></div><div><strong>📡 传感器</strong><br><span style="font-size:.75rem;color:var(--muted)">麦克风/IMU/摄像头</span></div></div>
                <span class="chain-arrow">→</span>
                <div class="chain-node"><div class="dot" style="background:#fdcb6e"></div><div><strong>📟 PCB设计</strong><br><span style="font-size:.75rem;color:var(--muted)">原理图/Layout</span></div></div>
                <span class="chain-arrow">→</span>
                <div class="chain-node"><div class="dot" style="background:#e17055"></div><div><strong>🏭 ODM</strong><br><span style="font-size:.75rem;color:var(--muted)">整机组装</span></div></div>
                <span class="chain-arrow">→</span>
                <div class="chain-node"><div class="dot" style="background:#d63031"></div><div><strong>📋 认证</strong><br><span style="font-size:.75rem;color:var(--muted)">3C/SRRC/网安</span></div></div>
                <span class="chain-arrow">→</span>
                <div class="chain-node"><div class="dot" style="background:#2d3436"></div><div><strong>📦 量产</strong><br><span style="font-size:.75rem;color:var(--muted)">MP</span></div></div>
            </div>
            </div>""", unsafe_allow_html=True)

            # 推荐ODM
            st.markdown("#### 🏭 推荐ODM厂商")
            npu_val = int(npu_need.replace('>','').replace('<','').replace(' TOPS',''))
            matched_odm = [o for o in ODM_DB if product in o["capability"]]
            for o in matched_odm[:3]:
                st.markdown(f"""<div class="card" style="border-left:3px solid var(--hw-blue)">
                    <h3>🏭 {o['name']}</h3>
                    <p><strong>能力</strong>：{', '.join(o['capability'])} | <strong>MOQ</strong>：{o['moq']} | <strong>交期</strong>：{o['lead_time']}</p>
                    <p><strong>优势</strong>：{o['strength']} | <strong>价格</strong>：{o['price_level']} | <strong>认证</strong>：{', '.join(o['certifications'])}</p>
                </div>""", unsafe_allow_html=True)

            # 推荐传感器
            st.markdown("#### 📡 关键器件国产化方案")
            for s in SENSOR_DB:
                loc = int(s['localization'].replace('%',''))
                badge = "green" if loc>=70 else "yellow" if loc>=50 else "red"
                st.markdown(f"- <span class='status-badge {badge}'>{loc}%国产</span> **{s['type']}** ¥{s['price']} — 国产：{', '.join(s['domestic'][:2])} | 进口：{', '.join(s['foreign'][:2])}", unsafe_allow_html=True)

            # 认证规划
            st.markdown("#### 📋 认证规划")
            total_cost = 0
            total_time = 0
            for cert_name in cert_needed:
                cert = next((c for c in CERT_DB if c["name"]==cert_name), None)
                if cert:
                    st.markdown(f"- ✅ **{cert['name']}** — {cert['authority']} | {cert['duration']} | ¥{cert['cost']}")
                    total_cost += int(cert['cost'].replace('¥','').replace('万','').split('-')[0])
                    total_time += int(cert['duration'].replace('周','').split('-')[0])
            st.info(f"💡 认证总费用约¥{total_cost}-{total_cost*3}万，总周期约{total_time}-{total_time*2}周（可并行）")

    with tab2:
        st.markdown("#### 🏭 ODM厂商数据库")
        for o in ODM_DB:
            st.markdown(f"""<div class="card">
                <h3>🏭 {o['name']} <span style="font-size:.75rem;color:var(--muted)">📍{o['location']}</span></h3>
                <p><strong>能力</strong>：{', '.join(o['capability'])}</p>
                <p><strong>MOQ</strong>：{o['moq']} | <strong>交期</strong>：{o['lead_time']} | <strong>价格</strong>：{o['price_level']}</p>
                <p><strong>优势</strong>：{o['strength']}</p>
                <p><strong>认证</strong>：{', '.join(o['certifications'])}</p>
            </div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("#### 📡 传感器/器件国产化数据库")
        sensor_md = "| 类型 | 价格 | 国产化率 | 国产方案 | 进口方案 |\n|------|------|---------|---------|----------|\n"
        for s in SENSOR_DB:
            sensor_md += f"| **{s['type']}** | {s['price']} | {s['localization']} | {', '.join(s['domestic'][:2])} | {', '.join(s['foreign'][:2])} |\n"
        st.markdown(sensor_md)

    with tab4:
        st.markdown("#### 📋 认证机构数据库")
        cert_md = "| 认证 | 机构 | 周期 | 费用 | 必需 | 适用范围 |\n|------|------|------|------|------|----------|\n"
        for c in CERT_DB:
            req = "✅ 必需" if c["required"] else "⚠️ 视情况"
            cert_md += f"| **{c['name']}** | {c['authority']} | {c['duration']} | {c['cost']} | {req} | {c['scope']} |\n"
        st.markdown(cert_md)
