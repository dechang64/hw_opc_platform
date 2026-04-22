"""硬件雷达 HWRadar - 芯片路线图+传感器价格+国产替代进度"""
import streamlit as st
from datetime import datetime

def render():
    st.markdown("# 📡 硬件雷达 HWRadar")
    st.markdown("""<div class="impossible">
        <div class="before">❌ 以前：不知道国产芯片什么时候追上、传感器价格什么时候降、哪个器件还没有国产替代</div>
        <div class="after">✅ 现在：实时追踪芯片制程/NPU算力/传感器价格/国产替代进度，辅助选型决策</div>
    </div>""", unsafe_allow_html=True)
    st.caption("📐 理论支撑：创造性破坏(Aghion) + GPT理论(Bresnahan) + 技术扩散S曲线(Rogers)")

    tab1,tab2,tab3,tab4 = st.tabs(["🔲 芯片路线图","📡 传感器价格","🇨🇳 国产替代进度","📋 技术窗口期"])

    with tab1:
        st.markdown("### 🔲 国产AI芯片路线图")
        st.markdown("""
        <div style="overflow-x:auto">
        <table style="width:100%;font-size:.82rem;border-collapse:collapse">
        <tr style="background:#f0f4ff">
            <th style="padding:.5rem">厂商</th>
            <th>最新芯片</th>
            <th>NPU算力</th>
            <th>制程</th>
            <th>功耗</th>
            <th>价格</th>
            <th>下一代</th>
            <th>预计时间</th>
        </tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**华为昇腾**</td><td>昇腾310B</td><td>16-24 TOPS</td><td>7nm</td><td>8W</td><td>¥300-500</td><td>昇腾320</td><td>2025 Q4</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**瑞芯微**</td><td>RK3588M</td><td>6 TOPS</td><td>8nm</td><td>3-8W</td><td>¥180-250</td><td>RK3688</td><td>2025 Q3</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**地平线**</td><td>旭日X5</td><td>10 TOPS</td><td>8nm</td><td>2.5W</td><td>¥80-150</td><td>旭日X6</td><td>2026 Q1</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**寒武纪**</td><td>MLU220</td><td>8 TOPS</td><td>7nm</td><td>5W</td><td>¥200-350</td><td>MLU230</td><td>2026 Q2</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**全志科技**</td><td>MR813</td><td>2.5 TOPS</td><td>12nm</td><td>1.5W</td><td>¥40-80</td><td>MR823</td><td>2025 Q4</td></tr>
        <tr><td style="padding:.5rem">**壁仞科技**</td><td>BR104</td><td>32 TOPS</td><td>7nm</td><td>15W</td><td>¥500-800</td><td>BR200</td><td>2026 Q3</td></tr>
        </table>
        </div>""", unsafe_allow_html=True)

        st.markdown("#### 📈 NPU算力趋势")
        st.markdown("""
        ```
        TOPS
        40 |                                          ● 壁仞BR200(2026)
        30 |                              ● 昇腾320(2025)
        20 |              ● 昇腾310B(2024)
        15 |                          ● 旭日X6(2026)
        10 |              ● 旭日X5(2024)     ● MLU230(2026)
         6 |  ● RK3588M(2023)
         3 |                              ● MR823(2025)
         2 |  ● MR813(2023)
           +----+----+----+----+----+----+----+----+→
           2022 2023 2024 2025 2026 2027 2028
        ```
        """)

    with tab2:
        st.markdown("### 📡 关键传感器价格趋势")
        st.markdown("""
        <table style="width:100%;font-size:.82rem;border-collapse:collapse">
        <tr style="background:#f0f4ff">
            <th style="padding:.5rem">器件</th>
            <th>2023均价</th>
            <th>2024均价</th>
            <th>2025预估</th>
            <th>趋势</th>
            <th>驱动因素</th>
        </tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">IMU(6轴)</td><td>¥8-15</td><td>¥5-12</td><td>¥3-8</td><td>📉 -30%</td><td>国产替代+规模效应</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">MEMS麦克风</td><td>¥5-10</td><td>¥3-8</td><td>¥2-6</td><td>📉 -25%</td><td>TWS+AI设备需求</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">微型摄像头</td><td>¥25-50</td><td>¥20-40</td><td>¥15-30</td><td>📉 -20%</td><td>车载+IoT需求</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">微型显示屏</td><td>¥80-200</td><td>¥60-150</td><td>¥40-100</td><td>📉 -25%</td><td>AR/VR+AI眼镜</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">WiFi/BT芯片</td><td>¥10-20</td><td>¥8-15</td><td>¥5-12</td><td>📉 -20%</td><td>乐鑫等国产方案</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">NPU SoC</td><td>¥200-500</td><td>¥150-400</td><td>¥100-300</td><td>📉 -25%</td><td>国产替代+竞争加剧</td></tr>
        <tr><td style="padding:.5rem">锂电池(500mAh)</td><td>¥15-25</td><td>¥12-20</td><td>¥10-18</td><td>📉 -15%</td><td>产能过剩</td></tr>
        </table>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("### 🇨🇳 国产替代进度追踪")
        st.markdown("""
        <table style="width:100%;font-size:.82rem;border-collapse:collapse">
        <tr style="background:#f0f4ff">
            <th style="padding:.5rem">器件类别</th>
            <th>国产化率(2023)</th>
            <th>国产化率(2024)</th>
            <th>目标(2025)</th>
            <th>进度</th>
            <th>主要国产厂商</th>
        </tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**主控SoC**</td><td>30%</td><td>45%</td><td>60%</td><td>🟡 加速中</td><td>瑞芯微、全志、地平线</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**内存**</td><td>15%</td><td>25%</td><td>40%</td><td>🟡 加速中</td><td>长鑫存储</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**存储**</td><td>20%</td><td>35%</td><td>50%</td><td>🟡 加速中</td><td>长江存储、兆易创新</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**MEMS麦克风**</td><td>60%</td><td>70%</td><td>80%</td><td>🟢 进展良好</td><td>瑞声科技、歌尔微</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**IMU**</td><td>40%</td><td>50%</td><td>65%</td><td>🟡 加速中</td><td>敏芯股份、明皜传感</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**摄像头**</td><td>50%</td><td>60%</td><td>70%</td><td>🟢 进展良好</td><td>舜宇光学、欧菲光</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**显示屏**</td><td>55%</td><td>65%</td><td>75%</td><td>🟢 进展良好</td><td>京东方、维信诺</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**WiFi/BT**</td><td>30%</td><td>40%</td><td>55%</td><td>🟡 加速中</td><td>乐鑫、恒玄</td></tr>
        <tr><td style="padding:.5rem;border-bottom:1px solid #eee">**电源管理**</td><td>35%</td><td>45%</td><td>55%</td><td>🟡 加速中</td><td>矽力杰、芯朋微</td></tr>
        <tr><td style="padding:.5rem">**电池**</td><td>70%</td><td>80%</td><td>85%</td><td>🟢 基本完成</td><td>亿纬锂能、欣旺达</td></tr>
        </table>""", unsafe_allow_html=True)

        st.markdown("""
        **综合国产化率趋势**：
        ```
        %
        100 |                                            🎯 目标
         80 |                              ● 2025预估(65%)
         60 |                  ● 2024(52%)
         40 |      ● 2023(40%)
         20 |
          0 +----+----+----+----+----+----+----+----+→
          2021 2022 2023 2024 2025 2026 2027 2028
        ```
        """)

    with tab4:
        st.markdown("### 📋 技术窗口期分析")
        st.markdown("""
        <div class="card" style="border-left:4px solid var(--success)">
            <h4>🟢 窗口期充裕（>18个月）</h4>
            <p>**端侧AI盒子**：国产芯片算力已满足需求，供应链成熟，认证路径清晰。建议立即启动。</p>
        </div>
        <div class="card" style="border-left:4px solid var(--warning)">
            <h4>🟡 窗口期有限（12-18个月）</h4>
            <p>**AI Pin**：市场教育成本高，竞品已先行，但国产化+端侧AI是差异化机会。建议6个月内出EVT。</p>
        </div>
        <div class="card" style="border-left:4px solid var(--danger)">
            <h4>🔴 窗口期紧迫（<12个月）</h4>
            <p>**AI眼镜**：Meta/苹果/字节等巨头已入场，窗口期快速关闭。除非有极强的技术差异化，否则不建议新进入。</p>
        </div>
        """)
