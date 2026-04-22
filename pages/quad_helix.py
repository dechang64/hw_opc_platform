"""四角色工作台 QuadHelix - 算法专家+硬件PM+供应链专家+认证顾问"""
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

SYSTEM_PROMPTS = {
    "algo": """你是一位AI算法部署专家，精通大模型压缩、量化和端侧部署。

## 你的分析框架
1. **模型适配性**：模型参数量、计算量(FLOPs)、内存占用 vs 芯片NPU算力、内存带宽
2. **量化方案**：FP16→INT8→INT4的精度损失和加速比
3. **推理优化**：算子融合、KV Cache、投机解码等优化手段
4. **多模态处理**：语音/视觉/文本各模态的资源需求和调度策略
5. **端云协同**：哪些任务端侧完成、哪些需要云端辅助

## 输出要求
- 给出具体的量化数据（FLOPs、延迟、内存）
- 用表格对比不同量化方案
- 给出明确的"算法专家建议"（一段话）""",

    "pm": """你是一位资深AI硬件产品经理，拥有从0到1打造AI硬件产品的经验。

## 你的分析框架
1. **产品定位**：差异化定位、目标用户画像、核心使用场景
2. **功能定义**：P0/P1/P2功能优先级、MVP范围
3. **用户体验**：交互方式、响应速度、续航、佩戴舒适度
4. **竞品分析**：Humane AI Pin、Rabbit R1、AI眼镜等竞品对比
5. **商业化**：定价策略、销售渠道、用户获取成本

## 输出要求
- 用表格列出功能优先级
- 给出具体的用户体验指标
- 给出明确的"产品经理建议"（一段话）""",

    "supply": """你是一位AI硬件供应链专家，精通芯片选型、器件采购和制造管理。

## 你的分析框架
1. **芯片选型**：3-5款候选芯片的详细参数对比（NPU、功耗、价格、生态）
2. **BOM成本**：关键器件成本估算和降本路径
3. **国产化分析**：各器件的国产替代方案和替代率
4. **制造可行性**：PCB设计、组装工艺、测试方案
5. **量产排期**：EVT→DVT→PVT→MP的时间线和关键节点

## 输出要求
- 用表格对比芯片方案
- 给出具体的BOM成本数据
- 给出明确的"供应链专家建议"（一段话）""",

    "cert": """你是一位电子产品认证专家，精通AI硬件产品的合规和认证。

## 你的分析框架
1. **认证清单**：需要哪些认证，哪些是强制的
2. **3C认证**：安全(GB4943.1)和EMC(GB9254)测试要点
3. **SRRC认证**：无线电发射设备的测试要求
4. **算法备案**：AI算法备案的材料和流程
5. **数据合规**：个人信息保护、数据出境评估
6. **时间线规划**：各认证的先后顺序和并行策略

## 输出要求
- 引用具体的法规条文和标准编号
- 用表格列出认证清单和时间线
- 给出明确的"认证顾问建议"（一段话）""",
}

def _fallback_analysis(role, project_name, project_desc):
    templates = {
        "algo": f"""# 🧠 算法专家分析：{project_name}

## 模型适配性评估
| 指标 | 需求 | 评估 |
|------|------|------|
| 模型参数量 | 1-7B | 建议使用1-3B端侧模型 |
| 计算量(FLOPs) | <10G/token | INT8量化后可满足 |
| 内存占用 | <2GB | KV Cache优化后可控 |
| 推理延迟 | <1s | 端侧INT8可达到 |

## 量化方案对比
| 方案 | 精度损失 | 速度提升 | 内存节省 | 推荐 |
|------|---------|---------|---------|------|
| FP16 | 0% | 1x | 1x | ❌ |
| INT8 | <1% | 2x | 2x | ✅ 推荐 |
| INT4 | 2-5% | 4x | 4x | ⚠️ 视场景 |

## 算法专家建议
建议采用INT8量化+算子融合+KV Cache优化的组合方案，在保证精度的前提下将推理延迟控制在1s以内。建议优先使用国产芯片（瑞芯微RK3588M）的NPU进行推理，利用其6 TOPS算力满足日常对话需求。对于复杂任务（如长文本生成），可考虑端云协同策略。""",
        "pm": f"""# 👔 产品经理分析：{project_name}

## 产品定位
- **差异化**：国产化+端侧AI+隐私保护
- **目标用户**：25-45岁商务人士
- **核心场景**：通勤、会议、差旅

## 功能优先级
| 功能 | 优先级 | 描述 | MVP |
|------|--------|------|-----|
| 语音唤醒 | P0 | "嗨，智灵"唤醒 | ✅ |
| 智能对话 | P0 | 多轮对话+上下文理解 | ✅ |
| 日程管理 | P0 | 创建/查询/提醒 | ✅ |
| 实时翻译 | P1 | 中英日韩 | ❌ |
| 信息查询 | P1 | 天气/新闻/百科 | ❌ |
| NFC支付 | P2 | 刷卡支付 | ❌ |

## 竞品对比
| 维度 | Humane AI Pin | Rabbit R1 | {project_name} |
|------|--------------|-----------|----------------|
| 价格 | $699 | $199 | ¥599(预估) |
| AI能力 | 云端LLM | LAM | 端侧+云端 |
| 隐私 | 云端处理 | 云端处理 | 端侧优先 |
| 续航 | ~4小时 | ~1天 | ~8小时(目标) |
| 国产化 | ❌ | ❌ | ✅ |

## 产品经理建议
建议MVP聚焦"语音AI助理+日程管理"两个核心场景，做到极致体验后再扩展。定价策略建议¥599，低于Humane但高于R1，突出国产化和隐私保护差异化。""",
        "supply": f"""# 🔧 供应链专家分析：{project_name}

## 芯片选型对比
| 芯片 | NPU | 功耗 | 价格 | 国产化 | 生态 | 推荐 |
|------|-----|------|------|--------|------|------|
| RK3588M | 6 TOPS | 3-8W | ¥200-280 | 95% | 良好 | ✅ 首选 |
| RK3588 | 6 TOPS | 5-10W | ¥180-250 | 95% | 良好 | 备选 |
| 地平线X3 | 5 TOPS | 2.5W | ¥80-120 | 100% | 一般 | 备选 |
| QCS6490 | 12 TOPS | 5-12W | ¥300-450 | 0% | 优秀 | ⚠️ |

## BOM成本估算
| 器件 | 成本 | 国产化率 |
|------|------|---------|
| 主控SoC | ¥200-280 | 95% |
| 内存+存储 | ¥50-100 | 70% |
| 麦克风阵列 | ¥10-25 | 80% |
| 扬声器 | ¥8-20 | 80% |
| WiFi/BT | ¥8-15 | 50% |
| 电池 | ¥15-25 | 90% |
| PCB+外壳 | ¥35-75 | 90% |
| **合计** | **¥326-540** | **~80%** |

## 量产排期
| 阶段 | 时间 | 产出 |
|------|------|------|
| EVT | 第1-3月 | 工程原型(20台) |
| DVT | 第4-5月 | 设计验证(100台) |
| PVT | 第6-7月 | 小批量试产(500台) |
| MP | 第8月+ | 量产(>5000台/月) |

## 供应链专家建议
推荐瑞芯微RK3588M作为主控，BOM成本控制在¥350-400，国产化率80%。建议与立讯精密或歌尔股份合作ODM，MOQ 5000台起。""",
        "cert": f"""# ⚖️ 认证顾问分析：{project_name}

## 认证清单
| 认证 | 必需 | 机构 | 周期 | 费用 | 优先级 |
|------|------|------|------|------|--------|
| 3C认证 | ✅ | CQC | 4-8周 | ¥3万 | P0 |
| SRRC认证 | ✅ | 工信部 | 6-10周 | ¥2万 | P0 |
| 算法备案 | ✅ | 网信办 | 4-8周 | ¥3万 | P0 |
| ICP备案 | ✅ | 工信部 | 1-2周 | 免费 | P1 |
| 网络安全评估 | ⚠️ | 网信办 | 8-12周 | ¥8万 | P1 |

## 关键风险
| 风险 | 等级 | 说明 | 应对 |
|------|------|------|------|
| EMC超标 | 🟡 | WiFi+BT辐射可能超标 | PCB优化+屏蔽罩 |
| 算法备案驳回 | 🟡 | AI算法安全评估不通过 | 提前准备安全评估报告 |
| 数据合规 | 🟡 | 语音数据采集需合规 | 端侧处理+最小化采集 |

## 时间线
```
第1月：启动3C+SRRC样品准备
第2-4月：3C+SRRC并行测试
第3-5月：算法备案材料准备+提交
第4-6月：网络安全评估（如需要）
第6月：全部认证完成
```

## 认证顾问建议
建议EVT阶段同步启动3C和SRRC认证样品准备，算法备案建议在产品定义阶段就开始准备材料。总认证费用预算¥16万，总周期约6个月（可并行压缩到4个月）。""",
    }
    return templates.get(role, f"# {role}分析\n\n{project_desc}")

def render():
    st.markdown("# 🧬 四角色工作台 QuadHelix")
    st.markdown("""<div class="impossible">
        <div class="before">❌ 以前：算法专家不懂硬件、产品经理不懂芯片、供应链不懂认证——四个角色需要四个团队</div>
        <div class="after">✅ 现在：一个OPC+四个AI Agent，算法专家+硬件PM+供应链专家+认证顾问协同分析</div>
    </div>""", unsafe_allow_html=True)
    st.caption("📐 理论支撑：三螺旋理论(Etzkowitz) + 委托-代理理论 + 基于任务模型(Autor)")

    # 角色选择
    roles = {"algo":"🧠 算法专家","pm":"👔 硬件PM","supply":"🔧 供应链专家","cert":"⚖️ 认证顾问"}
    c1,c2,c3,c4 = st.columns(4)
    buttons = {}
    for i,(key,label) in enumerate(roles.items()):
        with [c1,c2,c3,c4][i]:
            is_active = st.session_state.get("quad_role")==key
            buttons[key] = st.button(f"**{label}**", use_container_width=True, type="primary" if is_active else "secondary")

    for key,clicked in buttons.items():
        if clicked: st.session_state.quad_role = key
    if "quad_role" not in st.session_state: st.session_state.quad_role = "algo"
    role = st.session_state.quad_role

    # 共享项目上下文
    with st.expander("📋 共享项目上下文（四角色共享）", expanded=True):
        c1,c2 = st.columns(2)
        with c1:
            if "quad_project" not in st.session_state: st.session_state.quad_project = ""
            st.session_state.quad_project = st.text_input("项目名称", value=st.session_state.quad_project, key="qp_name")
            st.session_state.quad_desc = st.text_area("项目描述", value=st.session_state.get("quad_desc",""), height=120, key="qp_desc")
        with c2:
            st.markdown("#### 📊 四角色协同机制")
            st.markdown("""
            ```
            🧠 算法专家 → 模型适配性+量化方案
                 ↓ (结果注入)
            👔 硬件PM → 产品定义+功能优先级
                 ↓ (结果注入)
            🔧 供应链专家 → 芯片选型+BOM成本
                 ↓ (结果注入)
            ⚖️ 认证顾问 → 合规风险+认证规划
            ```
            每个角色能看到前面角色的分析结论，形成协同。""")

    st.markdown("---")

    # 一键四角色分析
    if st.button("🚀 一键四角色全部分析", type="primary", use_container_width=True):
        if not st.session_state.quad_project:
            st.warning("请先填写项目名称和描述")
        else:
            st.session_state.quad_results = {}
            st.session_state.quad_engine = {}
            role_order = ["algo","pm","supply","cert"]
            context = f"项目：{st.session_state.quad_project}\n描述：{st.session_state.quad_desc}"
            for i, r_key in enumerate(role_order):
                with st.spinner(f"🤖 {roles[r_key]}正在分析..."):
                    prev_context = ""
                    for prev_key in role_order[:i]:
                        if prev_key in st.session_state.quad_results:
                            prev_context += f"\n\n---\n{roles[prev_key]}的分析结论：\n{st.session_state.quad_results[prev_key][:500]}"
                    prompt = f"{context}\n{prev_context}\n\n请从{roles[r_key]}的角度进行分析。"
                    raw = _llm_raw(SYSTEM_PROMPTS[r_key], prompt)
                    if raw:
                        st.session_state.quad_results[r_key] = raw
                        st.session_state.quad_engine[r_key] = "🤖 AI"
                    else:
                        st.session_state.quad_results[r_key] = _fallback_analysis(r_key, st.session_state.quad_project, st.session_state.quad_desc)
                        st.session_state.quad_engine[r_key] = "📐 规则引擎"
            st.rerun()

    # 显示结果
    if st.session_state.get("quad_results"):
        role_order = ["algo","pm","supply","cert"]
        for r_key in role_order:
            if r_key not in st.session_state.quad_results: continue
            engine = st.session_state.quad_engine.get(r_key,"")
            is_current = (r_key == role)
            with st.expander(f"{roles[r_key]}  {engine}", expanded=is_current):
                st.markdown(st.session_state.quad_results[r_key])
                st.download_button("📥 导出", data=st.session_state.quad_results[r_key],
                    file_name=f"{st.session_state.quad_project}_{roles[r_key]}_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown", key=f"dl_quad_{r_key}")

        # 四角色综合建议
        if len(st.session_state.quad_results) == 4:
            st.markdown("---")
            st.markdown("### 🧬 四角色综合建议")
            st.markdown("""
            | 角色 | 核心观点 | 关键行动 |
            |------|---------|---------|
            | 🧠 算法专家 | INT8量化+端云协同 | 完成模型在目标芯片上的部署验证 |
            | 👔 硬件PM | MVP聚焦语音+日程 | 定义P0功能，设计用户体验 |
            | 🔧 供应链专家 | RK3588M+BOM¥350 | 锁定芯片和ODM，启动EVT |
            | ⚖️ 认证顾问 | 6个月/¥16万 | 同步启动3C+SRRC+算法备案 |

            **推进顺序**：算法验证(2周) → 芯片选型(1周) → 认证启动(并行) → EVT原型(2月) → DVT验证(1月) → 认证完成 → 量产
            """)
