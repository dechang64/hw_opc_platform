"""打样工坊 Prototyping - EVT→DVT→PVT→MP 全流程管理"""
import streamlit as st
from datetime import datetime, timedelta

def render():
    st.markdown("# 🏭 打样工坊 Prototyping")
    st.markdown("""<div class="impossible">
        <div class="before">❌ 以前：不知道EVT/DVT/PVT/MP每个阶段要做什么、花多少钱、找谁做、多久能完成</div>
        <div class="after">✅ 现在：AI辅助规划打样全流程，自动生成里程碑、成本预算、风险评估</div>
    </div>""", unsafe_allow_html=True)
    st.caption("📐 理论支撑：互补资产理论(Teece) + 交易成本经济学(Coase) + 供应链管理")

    tab1,tab2,tab3 = st.tabs(["📋 打样规划","💰 成本估算","📊 项目管理"])

    with tab1:
        st.markdown("### 📋 硬件产品化四阶段")
        st.markdown("""
        <div style="overflow-x:auto">
        <table style="width:100%;font-size:.82rem;border-collapse:collapse">
        <tr style="background:#f0f4ff">
            <th style="padding:.5rem">阶段</th>
            <th>目标</th>
            <th>数量</th>
            <th>周期</th>
            <th>费用</th>
            <th>关键产出</th>
            <th>风险</th>
        </tr>
        <tr style="background:#fff3e0">
            <td style="padding:.5rem;border-bottom:1px solid #eee"><strong>🔧 EVT</strong><br><span style="font-size:.7rem">工程验证</span></td>
            <td>验证技术可行性</td>
            <td>20-50台</td>
            <td>4-8周</td>
            <td>¥5-15万</td>
            <td>功能验证报告<br>硬件Bug清单<br>PCB改版建议</td>
            <td>芯片不兼容<br>PCB设计缺陷<br>散热不达标</td>
        </tr>
        <tr style="background:#e3f2fd">
            <td style="padding:.5rem;border-bottom:1px solid #eee"><strong>📐 DVT</strong><br><span style="font-size:.7rem">设计验证</span></td>
            <td>验证设计可靠性</td>
            <td>100-200台</td>
            <td>4-6周</td>
            <td>¥10-25万</td>
            <td>可靠性测试报告<br>认证测试样机<br>模具T1</td>
            <td>可靠性不达标<br>认证测试失败<br>模具问题</td>
        </tr>
        <tr style="background:#e8f5e9">
            <td style="padding:.5rem;border-bottom:1px solid #eee"><strong>🏭 PVT</strong><br><span style="font-size:.7rem">小批量试产</span></td>
            <td>验证量产能力</td>
            <td>500-2000台</td>
            <td>4-6周</td>
            <td>¥20-50万</td>
            <td>生产工艺文件<br>良率报告<br>首批成品</td>
            <td>良率不达标<br>供应链不稳定<br>产能不足</td>
        </tr>
        <tr style="background:#fce4ec">
            <td style="padding:.5rem"><strong>📦 MP</strong><br><span style="font-size:.7rem">量产</span></td>
            <td>规模化生产</td>
            <td>>5000台/月</td>
            <td>持续</td>
            <td>按BOM</td>
            <td>批量产品<br>质量管控体系<br>售后体系</td>
            <td>品质波动<br>物料缺货<br>需求变化</td>
        </tr>
        </table>
        </div>""", unsafe_allow_html=True)

        st.markdown("### 📅 里程碑甘特图")
        st.markdown("""
        ```
        阶段    W1  W2  W3  W4  W5  W6  W7  W8  W9  W10 W11 W12 W13 W14 W15 W16
        ─────────────────────────────────────────────────────────────────────────
        EVT     ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        DVT     ░░░░░░░░░░░░████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        PVT     ░░░░░░░░░░░░░░░░░░░░░░░░████████████░░░░░░░░░░░░░░░░░░░░░░░░░
        MP      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████████████████████████
        认证    ████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ─────────────────────────────────────────────────────────────────────────
                ▲EVT启动    ▲DVT启动    ▲PVT启动    ▲MP启动
        ```
        """)

    with tab2:
        st.markdown("### 💰 打样成本估算")
        product_type = st.selectbox("产品类型", ["AI Pin","AI眼镜","端侧AI盒子","AI开发板","智能音箱"])
        target_qty = st.number_input("目标量产数量(台/月)", value=5000, min_value=1000, step=1000)

        cost_data = {
            "AI Pin": {"evt":"¥8-15万","dvt":"¥15-25万","pvt":"¥30-50万","tooling":"¥20-40万","cert":"¥16万","bom_unit":"¥350-500","total":"¥89-146万"},
            "AI眼镜": {"evt":"¥10-20万","dvt":"¥20-35万","pvt":"¥40-60万","tooling":"¥30-50万","cert":"¥16万","bom_unit":"¥500-800","total":"¥116-181万"},
            "端侧AI盒子": {"evt":"¥5-10万","dvt":"¥10-18万","pvt":"¥20-35万","tooling":"¥10-20万","cert":"¥12万","bom_unit":"¥300-450","total":"¥57-95万"},
            "AI开发板": {"evt":"¥3-8万","dvt":"¥8-15万","pvt":"¥15-25万","tooling":"¥5-10万","cert":"¥8万","bom_unit":"¥200-350","total":"¥39-66万"},
            "智能音箱": {"evt":"¥5-12万","dvt":"¥12-20万","pvt":"¥25-40万","tooling":"¥15-30万","cert":"¥12万","bom_unit":"¥150-250","total":"¥69-114万"},
        }

        cost = cost_data.get(product_type, cost_data["AI Pin"])
        st.markdown(f"""
        <div class="card">
            <h3>💰 {product_type} 成本估算</h3>
            <table style="width:100%;font-size:.85rem;border-collapse:collapse">
            <tr style="background:#f0f4ff"><th style="padding:.5rem;text-align:left">项目</th><th>费用</th></tr>
            <tr><td style="padding:.5rem;border-bottom:1px solid #eee">🔧 EVT工程验证</td><td>{cost['evt']}</td></tr>
            <tr><td style="padding:.5rem;border-bottom:1px solid #eee">📐 DVT设计验证</td><td>{cost['dvt']}</td></tr>
            <tr><td style="padding:.5rem;border-bottom:1px solid #eee">🏭 PVT小批量试产</td><td>{cost['pvt']}</td></tr>
            <tr><td style="padding:.5rem;border-bottom:1px solid #eee">🔩 开模费用</td><td>{cost['tooling']}</td></tr>
            <tr><td style="padding:.5rem;border-bottom:1px solid #eee">📋 认证费用</td><td>{cost['cert']}</td></tr>
            <tr><td style="padding:.5rem;border-bottom:1px solid #eee">📦 单台BOM成本</td><td>{cost['bom_unit']}</td></tr>
            <tr style="background:#e8f5e9;font-weight:700"><td style="padding:.5rem">📊 产品化总投入(到MP)</td><td>{cost['total']}</td></tr>
            </table>
        </div>""", unsafe_allow_html=True)

        st.info(f"💡 目标量产{target_qty}台/月，BOM成本{cost['bom_unit']}，建议售价BOM的3-5倍（{cost['bom_unit'].replace('¥','').split('-')[0]}×3={int(cost['bom_unit'].replace('¥','').split('-')[0])*3}-{int(cost['bom_unit'].replace('¥','').split('-')[-1])*5}元）")

    with tab3:
        st.markdown("### 📊 项目风险管理")
        st.markdown("""
        <table style="width:100%;font-size:.82rem;border-collapse:collapse">
        <tr style="background:#f0f4ff">
            <th style="padding:.5rem">风险</th>
            <th>阶段</th>
            <th>概率</th>
            <th>影响</th>
            <th>应对策略</th>
        </tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">🔴 芯片不兼容</td><td>EVT</td><td>中</td><td>高</td><td>提前在评估板验证，准备2-3款备选芯片</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">🔴 EMC测试失败</td><td>DVT</td><td>中</td><td>高</td><td>EVT阶段预测试，预留PCB改版空间</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">🟡 模具问题</td><td>DVT/PVT</td><td>中</td><td>中</td><td>选择有经验的模具厂，T1/T2试模</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">🟡 供应链不稳定</td><td>PVT/MP</td><td>高</td><td>中</td><td>关键器件备选供应商，安全库存</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">🟡 良率不达标</td><td>PVT</td><td>中</td><td>中</td><td>逐步提升产能，分析不良原因</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">🟡 算法备案驳回</td><td>认证</td><td>低</td><td>高</td><td>提前准备材料，咨询专业机构</td></tr>
        <tr><td style="padding:.5rem">🟢 需求变化</td><td>全阶段</td><td>高</td><td>低</td><td>敏捷开发，模块化设计</td></tr>
        </table>""", unsafe_allow_html=True)
