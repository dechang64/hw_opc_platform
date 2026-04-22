"""硬件翻译 HWTranslator - 硬件规格书→4个专业版本"""
import streamlit as st, json, subprocess, re, time
from datetime import datetime

def _llm_raw(system_prompt, user_prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = subprocess.run(["z-ai","chat","-p",user_prompt,"-s",system_prompt],
                capture_output=True,text=True,timeout=120)
            if result.returncode==0:
                output=result.stdout.strip()
                lines=[l for l in output.split('\n') if l.strip() and not l.startswith('🚀')]
                output='\n'.join(lines)
                if output: return output
            if "429" in result.stderr or "Too many" in result.stderr:
                time.sleep(30*(attempt+1)); continue
        except: time.sleep(5); continue
    return None

ROLE_PROMPTS = {
    "投资人版": """你是一位专注AI硬件领域的风险投资分析师。将硬件规格书翻译为投资人能快速理解的投资简报。

## 必须包含
1. **一句话定位**：这个产品是什么，解决什么问题
2. **市场规模**：TAM/SAM/SOM，用数据说话
3. **竞争格局**：列出3-5个竞品，对比优劣势
4. **技术壁垒**：为什么别人做不了或做不好
5. **商业模式**：硬件销售+SaaS订阅/服务费
6. **单位经济**：BOM成本→售价→毛利率→LTV
7. **融资需求**：金额、用途、里程碑
8. **风险提示**：主要风险和应对策略

## 风格
- 数据驱动，每个观点都要有支撑
- 用表格对比竞品
- 突出国产化叙事和政策红利
- 800-1200字""",

    "产品经理版": """你是一位资深AI硬件产品经理。将硬件规格书翻译为产品经理能执行的产品定义文档。

## 必须包含
1. **产品定义**：核心功能、目标用户、使用场景
2. **功能规格**：详细的功能列表和优先级(P0/P1/P2)
3. **交互设计**：语音/触摸/手势等交互方式定义
4. **性能指标**：响应延迟、续航时间、唤醒准确率等
5. **软硬件分工**：哪些功能靠硬件、哪些靠软件/云端
6. **用户体验地图**：开箱→配网→首次使用→日常使用
7. **MVP定义**：第一版必须有什么、可以砍什么
8. **迭代路线图**：V1.0→V1.5→V2.0的功能规划

## 风格
- 可执行，每个功能都要有验收标准
- 用表格列出功能优先级
- 关注用户体验细节
- 800-1200字""",

    "供应链版": """你是一位AI硬件供应链专家。将硬件规格书翻译为供应链团队可执行的采购和制造指南。

## 必须包含
1. **BOM清单**：每个关键器件的规格、选型建议、备选方案
2. **芯片选型对比**：3-5款候选芯片的详细参数对比表
3. **国产化方案**：每个关键器件的国产替代方案和替代率
4. **供应商推荐**：每个器件的推荐供应商(2-3家)
5. **制造工艺**：PCB层数、工艺要求、组装方式
6. **测试方案**：功能测试、可靠性测试、认证测试
7. **量产排期**：EVT→DVT→PVT→MP的时间线和关键节点
8. **成本优化**：降本建议和目标

## 风格
- 数据精确，参数要有具体数值
- 用表格对比方案
- 关注可制造性和供应链风险
- 800-1200字""",

    "认证顾问版": """你是一位电子产品认证专家，精通3C、SRRC、网络安全、算法备案等认证流程。将硬件规格书翻译为认证团队可执行的合规指南。

## 必须包含
1. **认证清单**：需要哪些认证，哪些是强制的
2. **3C认证指南**：测试项目、所需资料、时间线、费用
3. **SRRC认证指南**：无线电测试要求、频段申请
4. **算法备案指南**：AI算法备案的材料准备和流程
5. **网络安全评估**：数据安全、隐私保护、等保要求
6. **时间线规划**：各认证的先后顺序和并行策略
7. **费用预算**：各认证的费用明细
8. **常见问题**：该类产品认证的常见驳回原因和应对

## 风格
- 引用具体的法规条文和标准编号
- 用表格列出认证清单和时间线
- 关注合规风险和应对策略
- 800-1200字""",
}

def _fallback_translate(name, product_type, specs, role):
    """规则引擎降级"""
    templates = {
        "投资人版": f"""# 💼 投资简报：{name}

## 一句话定位
{product_type}——面向{specs.get('target','商务人士')}的随身AI助理，解决{specs.get('pain_point','信息过载和效率低下')}问题。

## 市场规模
- **TAM**：全球AI可穿戴设备市场预计2027年达$XX亿
- **SAM**：中国AI硬件市场预计2027年达¥XX亿
- **SOM**：{product_type}细分市场预计2027年达¥XX亿
- **增长率**：CAGR约XX%

## 竞争格局
| 产品 | 价格 | 核心功能 | 优势 | 劣势 |
|------|------|---------|------|------|
| Humane AI Pin | $699 | 语音AI+投影 | 先发优势 | 体验差、续航短 |
| Rabbit R1 | $199 | LAM+旋转屏 | 价格低 | 功能有限 |
| {name} | TBD | {specs.get('core','AI助理')} | 国产化+本地化 | 待验证 |

## 技术壁垒
- 端侧大模型部署能力
- 国产化芯片适配经验
- 多模态交互技术

## 商业模式
- 硬件销售：¥XXX/台
- SaaS订阅：¥XX/月（高级功能）
- 技术许可：B端定制

## 单位经济
| 项目 | 金额 |
|------|------|
| BOM成本 | ¥XXX |
| 售价 | ¥XXX |
| 毛利率 | XX% |
| LTV | ¥XXX |

## 融资需求
- 本轮：¥XXX万
- 用途：EVT原型(40%)+团队(30%)+认证(20%)+市场(10%)
- 里程碑：6个月完成EVT，12个月完成量产

## 风险提示
- ⚠️ 技术风险：端侧模型效果待验证
- ⚠️ 市场风险：消费者教育成本高
- ⚠️ 供应链风险：关键器件供应不稳定""",
        "产品经理版": f"""# 👔 产品定义文档：{name}

## 产品定义
- **产品名**：{name}
- **形态**：{product_type}
- **目标用户**：{specs.get('target','商务人士')}
- **核心场景**：{specs.get('scene','日常随身AI助理')}

## 功能规格
| 功能 | 优先级 | 描述 | 验收标准 |
|------|--------|------|---------|
| 语音交互 | P0 | 语音唤醒+对话 | 唤醒率>95%，响应<500ms |
| 意图理解 | P0 | 理解复杂指令 | 准确率>90% |
| 日程管理 | P0 | 创建/查询/提醒 | 与主流日历同步 |
| 实时翻译 | P1 | 中英日韩多语种 | 延迟<1s |
| 信息查询 | P1 | 天气/新闻/百科 | 准确率>95% |
| NFC支付 | P2 | 刷卡支付 | 兼容主流支付 |

## 性能指标
- 唤醒响应：<300ms
- 对话响应：<1s（端侧）/ <3s（云端）
- 续航时间：>8小时（日常使用）
- 充电时间：<1小时

## MVP定义（V1.0）
- ✅ 必须：语音交互+意图理解+日程管理
- ❌ 砍掉：NFC支付、投影显示
- 📅 V1.5：实时翻译+信息查询
- 📅 V2.0：NFC支付+多设备协同

## 用户体验地图
1. **开箱**：极简包装，一键开机
2. **配网**：蓝牙→APP→WiFi，3步完成
3. **首次使用**：语音引导设置，30秒上手
4. **日常使用**：语音唤醒→对话→执行""",
        "供应链版": f"""# 🔧 供应链指南：{name}

## BOM清单
| 器件 | 规格 | 推荐方案 | 备选 | 预估价格 |
|------|------|---------|------|---------|
| 主控SoC | NPU≥6TOPS | RK3588M | 昇腾310 | ¥200-280 |
| 内存 | LPDDR4x 4-8GB | 长鑫存储 | Samsung | ¥30-60 |
| 存储 | eMMC 32-64GB | 长江存储 | Samsung | ¥20-40 |
| 麦克风 | 2-4麦阵列 | 瑞声科技 | Knowles | ¥10-25 |
| 扬声器 | 小型扬声器 | 瑞声科技 | AAC | ¥8-20 |
| WiFi/BT | WiFi5/BT5.0 | 乐鑫ESP32 | Qualcomm | ¥8-15 |
| 电池 | 500-1000mAh | 亿纬锂能 | ATL | ¥15-25 |
| IMU | 6轴 | 敏芯股份 | Bosch | ¥3-8 |

## 国产化方案
- 主控SoC：瑞芯微RK3588M（国产化率95%）
- 内存：长鑫存储（国产化率100%）
- 存储：长江存储（国产化率100%）
- 麦克风：瑞声科技（国产化率80%）
- **综合国产化率：约75-80%**

## 量产排期
| 阶段 | 时间 | 产出 | 关键节点 |
|------|------|------|---------|
| EVT | 第1-3月 | 工程原型 | 功能验证通过 |
| DVT | 第4-5月 | 设计验证 | 可靠性测试通过 |
| PVT | 第6-7月 | 小批量试产 | 良率>90% |
| MP | 第8月+ | 量产 | 月产能>5000台 |""",
        "认证顾问版": f"""# ⚖️ 认证合规指南：{name}

## 认证清单
| 认证 | 必需 | 机构 | 周期 | 费用 | 状态 |
|------|------|------|------|------|------|
| 3C认证 | ✅ | 认监委 | 4-8周 | ¥2-5万 | 待启动 |
| SRRC认证 | ✅ | 工信部 | 6-10周 | ¥1-3万 | 待启动 |
| 算法备案 | ✅ | 网信办 | 4-8周 | ¥2-5万 | 待启动 |
| ICP备案 | ✅ | 工信部 | 1-2周 | 免费 | 待启动 |
| 网络安全评估 | ⚠️ | 网信办 | 8-12周 | ¥5-15万 | 评估中 |

## 3C认证要点
- **标准**：GB4943.1（安全）、GB9254（EMC）
- **测试项目**：耐压测试、接地测试、辐射骚扰、传导骚扰
- **所需资料**：电路图、BOM表、说明书、铭板
- **常见驳回**：EMC超标→优化PCB布局+增加滤波

## SRRC认证要点
- **频段**：WiFi 2.4G/5G、蓝牙
- **测试项目**：发射功率、频谱模板、杂散发射
- **所需资料**：射频电路图、天线规格书

## 算法备案要点
- **依据**：《生成式人工智能服务管理暂行办法》
- **材料**：算法说明、训练数据说明、安全评估报告
- **注意**：需在产品上线前完成备案

## 时间线规划
```
第1-2月：准备3C+SRRC测试样品
第2-4月：3C+SRRC并行测试
第3-5月：算法备案材料准备+提交
第4-6月：网络安全评估（如需要）
第6月：所有认证完成，可上市
```

## 费用预算
| 认证 | 费用 |
|------|------|
| 3C | ¥3万 |
| SRRC | ¥2万 |
| 算法备案 | ¥3万 |
| 网络安全 | ¥8万 |
| **合计** | **¥16万** |""",
    }
    return templates.get(role, f"# {role}\n\n{specs}")

def render():
    st.markdown("# 🔄 硬件翻译 HWTranslator")
    st.markdown("""<div class="impossible">
        <div class="before">❌ 以前：一份硬件规格书，投资人看不懂、产品经理不会拆、供应链不知道买什么、认证不知道测什么</div>
        <div class="after">✅ 现在：一份规格书→一键生成投资人版/产品经理版/供应链版/认证顾问版</div>
    </div>""", unsafe_allow_html=True)
    st.caption("📐 理论支撑：吸收能力理论(Cohen-Levinthal 1990) + 信号理论(Spence 1973) + 任务模型(Autor)")

    tab1, tab2 = st.tabs(["🔄 新建翻译", "📋 翻译历史"])

    with tab1:
        with st.form("hw_trans_form"):
            c1,c2 = st.columns(2)
            with c1:
                name = st.text_input("产品名称 *", placeholder="例：智灵AI Pin")
                product_type = st.selectbox("产品形态 *",["AI Pin","AI眼镜","端侧AI盒子","AI开发板","其他"])
                target = st.text_input("目标用户", placeholder="例：25-45岁商务人士")
            with c2:
                core = st.text_input("核心功能", placeholder="例：语音AI助理+日程管理+实时翻译")
                pain_point = st.text_input("解决什么痛点", placeholder="例：信息过载、效率低下")
                scene = st.text_input("核心使用场景", placeholder="例：通勤、会议、差旅中的随身AI助理")

            st.markdown("#### 📟 硬件规格")
            c3,c4 = st.columns(2)
            with c3:
                chip = st.text_input("主控芯片", placeholder="例：瑞芯微RK3588M")
                npu = st.text_input("NPU算力", placeholder="例：6 TOPS")
                memory = st.text_input("内存/存储", placeholder="例：4GB LPDDR4x + 32GB eMMC")
            with c4:
                sensors = st.text_input("传感器", placeholder="例：双麦克风+IMU+触摸")
                battery = st.text_input("电池", placeholder="例：800mAh")
                connectivity = st.text_input("连接方式", placeholder="例：WiFi5+BT5.0+BLE")

            extra = st.text_area("补充信息", placeholder="论文链接、专利号、已有验证数据、竞品分析等", height=80)

            target_roles = st.multiselect("生成哪些版本",["投资人版","产品经理版","供应链版","认证顾问版"],default=["投资人版","产品经理版"])
            submitted = st.form_submit_button("🔄 一键生成多版本", type="primary", use_container_width=True)

        if submitted and target_roles:
            specs = {"target":target,"core":core,"pain_point":pain_point,"scene":scene,
                     "chip":chip,"npu":npu,"memory":memory,"sensors":sensors,
                     "battery":battery,"connectivity":connectivity,"extra":extra}

            results = {}
            engine_used = {}
            for role in target_roles:
                with st.spinner(f"🤖 正在生成{role}..."):
                    user_prompt = f"""请将以下硬件产品信息翻译为{role}：

## 产品信息
- 名称：{name}
- 形态：{product_type}
- 目标用户：{target}
- 核心功能：{core}
- 解决痛点：{pain_point}
- 使用场景：{scene}

## 硬件规格
- 主控芯片：{chip}
- NPU算力：{npu}
- 内存/存储：{memory}
- 传感器：{sensors}
- 电池：{battery}
- 连接方式：{connectivity}

## 补充信息
{extra}"""
                    raw = _llm_raw(ROLE_PROMPTS[role], user_prompt)
                    if raw:
                        results[role] = raw
                        engine_used[role] = "🤖 AI"
                    else:
                        results[role] = _fallback_translate(name, product_type, specs, role)
                        engine_used[role] = "📐 规则引擎"

            record = {"name":name,"product_type":product_type,"date":datetime.now().strftime("%Y-%m-%d %H:%M"),
                      "versions":results,"engine":engine_used}
            st.session_state.translations.append(record)
            st.rerun()

        if st.session_state.translations:
            r = st.session_state.translations[-1]
            st.markdown("---")
            for ver, content in r["versions"].items():
                icon = {"投资人版":"💼","产品经理版":"👔","供应链版":"🔧","认证顾问版":"⚖️"}.get(ver,"📄")
                engine = r.get("engine",{}).get(ver,"")
                with st.expander(f"{icon} {ver}  {engine}", expanded=True):
                    st.markdown(content)
                    st.download_button("📥 导出", data=content, file_name=f"{r['name']}_{ver}_{r['date'][:10]}.md", mime="text/markdown", key=f"dl_{ver}")

    with tab2:
        if not st.session_state.translations:
            st.info("暂无翻译记录")
        for r in reversed(st.session_state.translations):
            with st.expander(f"🔄 {r['name']}({r['product_type']}) — {r['date']}"):
                for ver in r["versions"]:
                    engine = r.get("engine",{}).get(ver,"")
                    st.markdown(f"- {ver}  {engine}")
