"""认证导航 CertNav - 3C/SRRC/算法备案/网安评估 全流程"""
import streamlit as st
from datetime import datetime

CERT_GUIDES = {
    "3C认证": {
        "icon": "📋", "authority": "国家认证认可监督管理委员会(CNCA)",
        "duration": "4-8周", "cost": "¥2-5万", "validity": "5年",
        "required": True,
        "standards": ["GB 4943.1-2022 音视频及类似电子设备安全","GB 9254-2008 信息技术设备无线电骚扰限值","GB/T 17618-2015 信息技术设备抗扰度"],
        "materials": ["电路原理图","PCB layout图","BOM表","产品说明书","铭板设计","安全关键件清单"],
        "tests": ["耐压测试(3000VAC/1min)","接地电阻测试(<0.1Ω)","绝缘电阻测试(>2MΩ)","辐射骚扰(30MHz-1GHz)","传导骚扰(150kHz-30MHz)","静电放电(ESD ±4kV接触/±8kV空气)"],
        "common_issues": ["EMC辐射超标→优化PCB布局+增加滤波电容","安全距离不足→增加隔离带","铭板信息不完整→按GB5296.1标准补充"],
        "timeline": "第1-2周：准备样品和资料\n第3-4周：送样测试\n第5-6周：整改(如有)\n第7-8周：工厂审查+发证",
    },
    "SRRC认证": {
        "icon": "📡", "authority": "工业和信息化部(工信部)",
        "duration": "6-10周", "cost": "¥1-3万", "validity": "5年",
        "required": True,
        "standards": ["YD/T 1484-2023 无线电设备杂散发射","YD/T 3165-2023 短距离无线电设备","GB/T 9254.1-2021 电磁兼容"],
        "materials": ["射频电路图","天线规格书","产品照片(内外)","使用说明书","技术手册","频率范围说明"],
        "tests": ["发射功率测试","频谱模板","杂散发射","占用带宽","频率容限","调制特性"],
        "common_issues": ["发射功率超标→降低PA增益或调整天线","杂散发射超标→增加滤波器","频段使用不规范→确认WiFi/蓝牙频段合规"],
        "timeline": "第1-2周：准备样品和资料\n第3-5周：送样测试\n第6-8周：整改(如有)\n第9-10周：核准发证",
    },
    "算法备案": {
        "icon": "🤖", "authority": "国家互联网信息办公室(网信办)",
        "duration": "4-8周", "cost": "¥2-5万", "validity": "长期",
        "required": True,
        "standards": ["《生成式人工智能服务管理暂行办法》","《互联网信息服务算法推荐管理规定》","《深度合成管理规定》"],
        "materials": ["算法说明文档","训练数据说明","数据标注规则","安全评估报告","算法机制说明","用户协议和隐私政策"],
        "tests": ["算法公平性评估","算法透明度评估","数据安全评估","内容安全评估","用户权益保护评估"],
        "common_issues": ["训练数据来源不清晰→补充数据来源说明","安全评估不充分→增加第三方安全评估","算法机制说明不详细→补充技术白皮书"],
        "timeline": "第1-3周：准备备案材料\n第4-5周：提交备案\n第6-8周：审核+整改(如有)\n通过后获得备案号",
    },
    "网络安全评估": {
        "icon": "🔒", "authority": "网信办+公安部",
        "duration": "8-12周", "cost": "¥5-15万", "validity": "2年",
        "required": False,
        "standards": ["GB/T 35273-2020 个人信息安全规范","GB/T 22239-2019 网络安全等级保护","《数据安全法》","《个人信息保护法》"],
        "materials": ["系统架构图","数据流程图","安全管理制度","等保测评报告","隐私影响评估(PIA)","数据出境评估(如适用)"],
        "tests": ["等保二级/三级测评","渗透测试","漏洞扫描","数据安全审计","隐私合规检查"],
        "common_issues": ["数据分类分级不清晰→建立数据分类分级制度","日志留存不足→确保日志留存6个月以上","应急响应预案缺失→制定网络安全应急预案"],
        "timeline": "第1-3周：等保测评\n第4-6周：整改\n第7-8周：复测\n第9-10周：出具报告\n第11-12周：备案",
    },
    "ICP备案": {
        "icon": "🌐", "authority": "工信部",
        "duration": "1-2周", "cost": "免费", "validity": "长期",
        "required": True,
        "standards": ["《互联网信息服务管理办法》","《非经营性互联网信息服务备案管理办法》"],
        "materials": ["营业执照","法人身份证","域名证书","网站负责人信息","服务器接入信息"],
        "tests": [],
        "common_issues": ["域名未实名认证→先完成域名实名","服务器在境外→需使用境内服务器","信息不一致→确保所有信息准确"],
        "timeline": "第1周：提交备案\n第2周：审核通过",
    },
}

def render():
    st.markdown("# 📋 认证导航 CertNav")
    st.markdown("""<div class="impossible">
        <div class="before">❌ 以前：不知道AI硬件需要哪些认证、每个认证要什么材料、多久能拿到、多少钱</div>
        <div class="after">✅ 现在：一键生成认证清单+材料清单+时间线+费用预算，每个认证都有详细指南</div>
    </div>""", unsafe_allow_html=True)
    st.caption("📐 理论支撑：制度经济学(North) + 交易成本(Coase) + 监管俘获理论(Stigler)")

    tab1,tab2,tab3 = st.tabs(["📋 认证清单","📖 认证详情","⏱️ 时间线规划"])

    with tab1:
        st.markdown("### 📋 AI硬件产品认证清单")
        product_has_wifi = st.checkbox("产品包含WiFi/蓝牙", value=True)
        product_has_ai = st.checkbox("产品包含AI算法", value=True)
        product_has_cloud = st.checkbox("产品连接云端服务", value=True)
        product_has_voice = st.checkbox("产品采集语音数据", value=True)

        st.markdown("---")
        applicable = []
        for name, guide in CERT_GUIDES.items():
            if name == "SRRC" and not product_has_wifi: continue
            if name == "算法备案" and not product_has_ai: continue
            if name == "网络安全评估" and not product_has_cloud: continue
            applicable.append((name, guide))

        total_cost_low = sum(int(g["cost"].replace("¥","").split("-")[0].replace("万","")) for _,g in applicable)
        total_cost_high = sum(int(g["cost"].replace("¥","").split("-")[-1].replace("万","").replace("免费","0")) for _,g in applicable)
        total_weeks = max(int(g["duration"].replace("周","").split("-")[-1]) for _,g in applicable)

        cert_md = "| 认证 | 必需 | 机构 | 周期 | 费用 | 标准 |\n|------|------|------|------|------|------|\n"
        for name, g in applicable:
            req = "✅ 必需" if g["required"] else "⚠️ 建议"
            cert_md += f"| {g['icon']} **{name}** | {req} | {g['authority'][:15]}... | {g['duration']} | {g['cost']} | {g['standards'][0][:20]}... |\n"
        st.markdown(cert_md)

        st.markdown(f"""<div class="card" style="background:linear-gradient(135deg,#f0f4ff,#e8f5e9)">
            <h3>📊 认证总览</h3>
            <p>• 需要认证：<strong>{len(applicable)}项</strong></p>
            <p>• 总费用预估：<strong>¥{total_cost_low}-{total_cost_high}万</strong></p>
            <p>• 总周期预估：<strong>{total_weeks}周（可并行压缩）</strong></p>
            <p>• 并行后预估：<strong>{total_weeks//2}-{total_weeks*2//3}周</strong></p>
        </div>""", unsafe_allow_html=True)

    with tab2:
        selected = st.selectbox("选择认证查看详情", [n for n,_ in applicable] if applicable else list(CERT_GUIDES.keys()))
        if selected and selected in CERT_GUIDES:
            g = CERT_GUIDES[selected]
            st.markdown(f"### {g['icon']} {selected}")
            c1,c2 = st.columns(2)
            with c1:
                st.markdown(f"**机构**：{g['authority']}")
                st.markdown(f"**周期**：{g['duration']}")
                st.markdown(f"**费用**：{g['cost']}")
                st.markdown(f"**有效期**：{g['validity']}")
                st.markdown(f"**必需**：{'✅ 是' if g['required'] else '⚠️ 视情况'}")
            with c2:
                st.markdown("**参考标准**")
                for s in g["standards"]:
                    st.markdown(f"- {s}")

            st.markdown("---")
            c3,c4 = st.columns(2)
            with c3:
                st.markdown("#### 📄 所需材料")
                for m in g["materials"]:
                    st.markdown(f"- [ ] {m}")
            with c4:
                st.markdown("#### 🧪 测试项目")
                for t in g["tests"]:
                    st.markdown(f"- {t}")

            if g["common_issues"]:
                st.markdown("#### ⚠️ 常见问题")
                for issue in g["common_issues"]:
                    st.markdown(f"- {issue}")

            st.markdown("#### ⏱️ 时间线")
            st.code(g["timeline"])

    with tab3:
        st.markdown("### ⏱️ 认证时间线规划（并行策略）")
        st.markdown("""
        ```
        周  1  2  3  4  5  6  7  8  9  10 11 12
        ─────────────────────────────────────
        3C    ████████░░░░░░░░░░░░░░░░░░░░░
        SRRC  ████████████░░░░░░░░░░░░░░░░░
        算法  ░░████████░░░░░░░░░░░░░░░░░░
        网安  ░░░░░░░░████████████░░░░░░░░
        ICP   ██░░░░░░░░░░░░░░░░░░░░░░░░░
        ─────────────────────────────────────
              ▲准备  ▲测试  ▲整改  ▲发证
        ```

        **并行策略**：
        1. **第1周**：同时启动3C+SRRC样品准备+ICP备案
        2. **第2周**：3C+SRRC送样测试，算法备案材料准备
        3. **第3周**：算法备案提交，网络安全评估启动
        4. **第4-6周**：3C+SRRC整改(如有)，算法备案审核
        5. **第8周**：3C+SRRC+算法备案基本完成
        6. **第10-12周**：网络安全评估完成

        **总周期**：12周（并行） vs 30周（串行）→ **节省60%时间**
        """)
