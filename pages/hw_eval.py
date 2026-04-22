"""硬件评估 HWEval - 芯片Benchmark+算法适配+BOM成本+国产化率"""
import streamlit as st, json, subprocess, re, time, random
from datetime import datetime

# ─── LLM ───
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

def _llm_json(system_prompt, user_prompt):
    raw=_llm_raw(system_prompt,user_prompt)
    if not raw: return None
    for fn in [lambda s:json.loads(s),
               lambda s:json.loads(re.search(r'```(?:json)?\s*\n?(.*?)\n?```',s,re.DOTALL).group(1)),
               lambda s:json.loads(re.search(r'\{.*\}',s,re.DOTALL).group(0))]:
        try: return fn(raw)
        except: pass
    return None

# ─── 芯片数据库（模拟） ───
CHIP_DB = [
    {"name":"瑞芯微 RK3588","vendor":"瑞芯微","npu":"6 TOPS","cpu":"4xA76+4xA55","gpu":"Mali-G610","mem":"LPDDR4x","power":"5-10W","price":"¥180-250","localization":"95%","process":"8nm","interface":"PCIe 3.0/USB 3.0","fit":["边缘计算","NVR","机器人","AI盒子"]},
    {"name":"瑞芯微 RK3588M","vendor":"瑞芯微","npu":"6 TOPS","cpu":"4xA76+4xA55","gpu":"Mali-G610","mem":"LPDDR4x","power":"3-8W","price":"¥200-280","localization":"95%","process":"8nm","interface":"PCIe 3.0/USB 3.0","fit":["AI Pin","智能音箱","车载"]},
    {"name":"全志 T507","vendor":"全志科技","npu":"1 TOPS","cpu":"4xA53","gpu":"Mali-G31","mem":"LPDDR3","power":"2-5W","price":"¥40-60","localization":"90%","process":"55nm","interface":"USB 2.0/SDIO","fit":["IoT","智能家电","简单AI设备"]},
    {"name":"寒武纪 MLU220","vendor":"寒武纪","npu":"8 TOPS","cpu":"ARM Cortex-A35","gpu":"无","mem":"LPDDR4x","power":"8-15W","price":"¥300-500","localization":"100%","process":"16nm","interface":"PCIe 3.0","fit":["边缘推理","视频分析","工业检测"]},
    {"name":"地平线旭日X3","vendor":"地平线","npu":"5 TOPS","cpu":"4xA53","gpu":"无","mem":"LPDDR4","power":"2.5W","price":"¥80-120","localization":"100%","process":"28nm","interface":"MIPI CSI/USB","fit":["智能摄像头","ADAS","机器人视觉"]},
    {"name":"昇腾310","vendor":"华为","npu":"22 TOPS","cpu":"ARM Cortex-A73","gpu":"无","mem":"DDR4","power":"8W","price":"¥500-800","localization":"100%","process":"12nm","interface":"PCIe 4.0","fit":["边缘服务器","智慧城市","工业AI"]},
    {"name":"算能 SE5","vendor":"算能科技","npu":"17.6 TOPS","cpu":"ARM","gpu":"无","mem":"DDR4","power":"6-12W","price":"¥200-350","localization":"85%","process":"12nm","interface":"PCIe 3.0/USB 3.0","fit":["视频分析","边缘推理","AI盒子"]},
    {"name":"瑞芯微 RV1126","vendor":"瑞芯微","npu":"2 TOPS","cpu":"4xA7","gpu":"Mali-G52","mem":"DDR3","power":"1-3W","price":"¥30-50","localization":"95%","process":"12nm","interface":"MIPI CSI/USB","fit":["IPC","智能门铃","低功耗AI"]},
    {"name":"高通 QCS6490","vendor":"高通(非国产)","npu":"12 TOPS","cpu":"4xA78+4xA55","gpu":"Adreno 643","mem":"LPDDR5","power":"5-12W","price":"¥300-450","localization":"0%","process":"6nm","interface":"PCIe/USB 3.1/WiFi6","fit":["AI Pin","AR眼镜","高端IoT"]},
    {"name":"联发科 Genio 700","vendor":"联发科(非国产)","npu":"4 TOPS","cpu":"2xA78+6xA55","gpu":"Mali-G57","mem":"LPDDR5","power":"5-8W","price":"¥150-220","localization":"0%","process":"6nm","interface":"PCIe/USB 3.2/WiFi6","fit":["智能音箱","机器人","AIoT"]},
]

# ─── BOM模板（按产品形态） ───
BOM_TEMPLATES = {
    "AI Pin": {
        "components": [
            {"name":"主控SoC","cost_range":"80-300","localization":"60%"},
            {"name":"麦克风阵列(2-4麦)","cost_range":"15-40","localization":"70%"},
            {"name":"扬声器","cost_range":"8-20","localization":"80%"},
            {"name":"触摸屏/LED指示","cost_range":"10-30","localization":"50%"},
            {"name":"WiFi/BT模块","cost_range":"8-15","localization":"40%"},
            {"name":"电池(500-1000mAh)","cost_range":"15-25","localization":"90%"},
            {"name":"IMU传感器","cost_range":"3-8","localization":"30%"},
            {"name":"PCB+被动元件","cost_range":"20-40","localization":"85%"},
            {"name":"外壳(注塑/金属)","cost_range":"15-35","localization":"95%"},
            {"name":"充电座/磁吸","cost_range":"10-20","localization":"90%"},
        ],
        "total_range":"184-533","nre_range":"50-150万","moq":"5000-10000",
    },
    "AI眼镜": {
        "components": [
            {"name":"主控SoC","cost_range":"80-250","localization":"50%"},
            {"name":"Micro OLED/光波导","cost_range":"150-500","localization":"10%"},
            {"name":"摄像头模组","cost_range":"20-50","localization":"60%"},
            {"name":"麦克风阵列","cost_range":"10-25","localization":"70%"},
            {"name":"骨传导扬声器","cost_range":"15-30","localization":"50%"},
            {"name":"电池(300-600mAh)","cost_range":"10-18","localization":"90%"},
            {"name":"WiFi/BT模块","cost_range":"8-15","localization":"40%"},
            {"name":"PCB+柔性电路","cost_range":"25-50","localization":"80%"},
            {"name":"镜框/镜腿","cost_range":"30-80","localization":"95%"},
        ],
        "total_range":"348-1018","nre_range":"100-300万","moq":"3000-5000",
    },
    "端侧AI盒子": {
        "components": [
            {"name":"主控SoC(高算力)","cost_range":"150-500","localization":"70%"},
            {"name":"DDR内存(4-8GB)","cost_range":"30-80","localization":"40%"},
            {"name":"eMMC/SSD存储","cost_range":"20-60","localization":"50%"},
            {"name":"摄像头模组(1-4路)","cost_range":"30-120","localization":"60%"},
            {"name":"WiFi/4G/5G模块","cost_range":"30-80","localization":"30%"},
            {"name":"电源模块","cost_range":"15-30","localization":"90%"},
            {"name":"散热系统","cost_range":"10-25","localization":"95%"},
            {"name":"外壳(铝合金)","cost_range":"20-50","localization":"95%"},
            {"name":"PCB+接口","cost_range":"25-50","localization":"85%"},
        ],
        "total_range":"330-995","nre_range":"30-80万","moq":"1000-3000",
    },
    "AI开发板/模组": {
        "components": [
            {"name":"SoC模组","cost_range":"100-400","localization":"65%"},
            {"name":"DDR+存储","cost_range":"30-80","localization":"45%"},
            {"name":"接口电路","cost_range":"15-30","localization":"90%"},
            {"name":"PCB(4-8层)","cost_range":"20-60","localization":"95%"},
            {"name":"散热+外壳","cost_range":"10-25","localization":"95%"},
        ],
        "total_range":"175-595","nre_range":"10-30万","moq":"500-2000",
    },
}

# ─── System Prompt ───
SYSTEM_PROMPT = """你是一位资深的智能体硬件产品评估专家，精通AI算法部署、芯片选型、硬件设计和供应链管理。

## 评估维度
1. **算法-硬件适配性**：算法的计算需求（FLOPs、参数量、内存）与候选芯片的匹配度
2. **国产化可行性**：关键组件的国产替代方案和替代率
3. **BOM成本估算**：基于产品形态的物料成本估算
4. **技术风险**：关键技术难点和风险等级
5. **市场窗口**：产品化的时机和竞争态势

## 输出格式
严格输出JSON，格式如下：
{
    "chip_recommendation": {"primary": "芯片名", "reason": "推荐理由", "alternatives": ["备选1","备选2"]},
    "algorithm_hardware_fit": {"score": 85, "analysis": "适配性分析"},
    "localization": {"rate": 75, "components": [{"name":"组件名","rate":90,"domestic":"国产方案","foreign":"进口方案"}]},
    "bom_estimate": {"low": 200, "high": 500, "breakdown": [{"name":"组件","low":50,"high":100}]},
    "risks": [{"item":"风险项","level":"高/中/低","mitigation":"缓解措施"}],
    "market_window": {"assessment":"窗口期评估","timeline":"建议时间线"},
    "overall_score": 78,
    "suggestion": "综合建议"
}"""

def _build_prompt(form_data):
    return f"""请评估以下智能体硬件方案：

## 基本信息
- 产品形态：{form_data['product_type']}
- 核心功能：{form_data['core_function']}
- 目标场景：{form_data['target_scene']}

## 算法信息
- 模型类型：{form_data['model_type']}
- 模型规模：{form_data['model_size']}
- 推理延迟要求：{form_data['latency_req']}
- 精度要求：{form_data['precision_req']}

## 硬件约束
- 功耗预算：{form_data['power_budget']}
- 尺寸限制：{form_data['size_limit']}
- 成本目标：{form_data['cost_target']}
- 国产化要求：{form_data['localization_req']}

## 补充信息
{form_data.get('extra_info','无')}

请基于以上信息，给出芯片推荐、国产化分析、BOM估算和风险评估。"""

def _sim_eval(form_data):
    """规则引擎降级评估"""
    # 根据NPU需求筛选芯片
    npu_map = {"<2 TOPS":1,"2-6 TOPS":6,"6-15 TOPS":15,"15-25 TOPS":25,">25 TOPS":30}
    power_map = {"<2W":2,"2-5W":5,"5-10W":10,"10-20W":20,">20W":30}
    needed_npu = npu_map.get(form_data['latency_req'], 6)
    needed_power = power_map.get(form_data['power_budget'], 10)

    # 筛选匹配芯片
    matched = []
    for chip in CHIP_DB:
        chip_npu = int(chip['npu'].replace(' TOPS',''))
        chip_power = int(chip['power'].split('-')[0])
        if chip_npu >= needed_npu * 0.7 and chip_power <= needed_power * 1.5:
            score = 100 - abs(chip_npu - needed_npu) * 2 - abs(chip_power - needed_power) * 3
            if form_data['localization_req'] != "无要求" and chip['localization'] != "100%":
                score -= 10
            matched.append((chip, max(50, min(98, score))))

    matched.sort(key=lambda x: -x[1])
    primary = matched[0][0] if matched else CHIP_DB[0]
    alts = [m[0]['name'] for m in matched[1:3]] if len(matched) > 1 else []

    # BOM估算
    bom = BOM_TEMPLATES.get(form_data['product_type'], BOM_TEMPLATES["AI Pin"])
    total_low = sum(int(c['cost_range'].split('-')[0]) for c in bom['components'])
    total_high = sum(int(c['cost_range'].split('-')[1]) for c in bom['components'])

    # 国产化率
    avg_loc = sum(int(c['localization'].replace('%','')) for c in bom['components']) / len(bom['components'])

    return {
        "chip_recommendation": {"primary": primary['name'], "reason": f"NPU {primary['npu']}，功耗 {primary['power']}，国产化率 {primary['localization']}，适配{','.join(primary['fit'][:2])}", "alternatives": alts},
        "algorithm_hardware_fit": {"score": matched[0][1] if matched else 60, "analysis": f"算法需要约{needed_npu} TOPS算力，推荐芯片提供{primary['npu']}，满足推理需求。内存带宽{primary['mem']}可容纳{form_data['model_size']}模型。"},
        "localization": {"rate": round(avg_loc), "components": [{"name":c['name'],"rate":int(c['localization'].replace('%','')),"domestic":"已有国产方案" if int(c['localization'].replace('%',''))>=70 else "需寻找替代","foreign":"进口依赖" if int(c['localization'].replace('%',''))<50 else "可选国产"} for c in bom['components']]},
        "bom_estimate": {"low": total_low, "high": total_high, "nre": bom.get('nre_range','50-150万'), "moq": bom.get('moq','5000'), "breakdown": bom['components']},
        "risks": [{"item":"NPU算力不足","level":"中","mitigation":"模型量化(INT8/INT4)降低算力需求"},{"item":"供应链不稳定","level":"中","mitigation":"关键器件备选2-3家供应商"},{"item":"散热挑战","level":"低","mitigation":"优化PCB布局+散热片设计"},{"item":"国产化率不达标","level":"中","mitigation":"优先选用国产芯片+传感器"}],
        "market_window": {"assessment":"智能体硬件市场处于早期阶段，竞争者较少，建议6-12个月内完成产品化","timeline":"算法验证(1-2月)→芯片选型(1月)→EVT原型(2-3月)→DVT验证(2月)→PVT试产(1-2月)→MP量产(持续)"},
        "overall_score": matched[0][1] if matched else 60,
        "suggestion": f"推荐使用{primary['name']}作为主控芯片，BOM成本约¥{total_low}-{total_high}，国产化率约{round(avg_loc)}%。建议先完成算法在目标芯片上的量化部署验证，再启动硬件设计。",
        "is_simulated": True,
    }

def render():
    st.markdown("# 📊 硬件评估 HWEval")
    st.markdown("""<div class="impossible">
        <div class="before">❌ 以前：不知道算法能不能跑在哪个芯片上、BOM要多少钱、国产化率多少——全靠拍脑袋</div>
        <div class="after">✅ 现在：输入算法参数→输出芯片推荐+BOM成本+国产化率+风险评估，数据驱动决策</div>
    </div>""", unsafe_allow_html=True)
    st.caption("📐 理论支撑：交易成本经济学(Coase) + 搜寻理论(Stigler) + 吸收能力理论(Cohen-Levinthal)")

    tab1, tab2, tab3 = st.tabs(["🔍 新建评估", "📋 评估历史", "🔲 芯片数据库"])

    with tab1:
        with st.form("hw_eval_form"):
            st.markdown("#### 📦 产品定义")
            c1,c2 = st.columns(2)
            with c1:
                product_type = st.selectbox("产品形态 *", ["AI Pin","AI眼镜","端侧AI盒子","AI开发板/模组","其他"])
                core_function = st.text_input("核心功能 *", placeholder="例：语音助手+日程管理+实时翻译")
                target_scene = st.text_input("目标场景 *", placeholder="例：商务人士日常随身AI助理")
            with c2:
                cost_target = st.selectbox("BOM成本目标", ["<¥200","¥200-500","¥500-1000","¥1000-2000",">¥2000"])
                localization_req = st.selectbox("国产化要求", ["无要求",">60%",">80%",">90%","100%"])
                size_limit = st.selectbox("尺寸限制", ["无限制","<50mm圆形","<80mm方形","手机大小","盒子大小"])

            st.markdown("#### 🧠 算法信息")
            c3,c4 = st.columns(2)
            with c3:
                model_type = st.selectbox("模型类型", ["LLM(大语言模型)","视觉模型(ViT/YOLO)","多模态模型","语音模型(ASR/TTS)","Agent框架","其他"])
                model_size = st.selectbox("模型规模", ["<100M参数","100M-1B参数","1B-7B参数","7B-13B参数",">13B参数"])
            with c4:
                latency_req = st.selectbox("推理延迟要求(对应NPU需求)", ["<2 TOPS","2-6 TOPS","6-15 TOPS","15-25 TOPS",">25 TOPS"])
                precision_req = st.selectbox("精度要求", ["FP32","FP16","INT8(量化)","INT4(激进量化)","混合精度"])

            st.markdown("#### ⚡ 硬件约束")
            c5,c6 = st.columns(2)
            with c5:
                power_budget = st.selectbox("功耗预算", ["<2W","2-5W","5-10W","10-20W",">20W"])
            with c6:
                extra_info = st.text_area("补充信息", placeholder="论文链接、专利号、已有验证数据等", height=80)

            submitted = st.form_submit_button("📊 启动硬件评估", type="primary", use_container_width=True)

        if submitted:
            form_data = {k:v for k,v in locals().items() if k in [
                'product_type','core_function','target_scene','cost_target','localization_req',
                'size_limit','model_type','model_size','latency_req','precision_req','power_budget','extra_info']}
            form_data['extra_info'] = extra_info

            with st.spinner("🤖 AI正在评估硬件方案..."):
                result = _llm_json(SYSTEM_PROMPT, _build_prompt(form_data))
                if not result:
                    st.warning("🤖 LLM暂不可用，已切换到智能规则引擎")
                    result = _sim_eval(form_data)

            result["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            result["product_type"] = product_type
            result["model_type"] = model_type
            st.session_state.evaluations.append(result)
            st.rerun()

        if st.session_state.evaluations:
            r = st.session_state.evaluations[-1]
            engine = "🤖 AI" if not r.get("is_simulated") else "📐 规则引擎"
            st.markdown(f"---\n### 📋 评估结果  {engine}")

            # 核心指标
            c1,c2,c3,c4 = st.columns(4)
            with c1:
                color = "#00b894" if r["overall_score"]>=75 else "#fdcb6e" if r["overall_score"]>=60 else "#d63031"
                st.markdown(f"""<div class="metric-box"><div class="num" style="color:{color}">{r['overall_score']}</div><div class="label">📊 综合评分</div></div>""", unsafe_allow_html=True)
            with c2:
                fit = r.get("algorithm_hardware_fit",{})
                st.markdown(f"""<div class="metric-box"><div class="num">{fit.get('score','N/A')}</div><div class="label">🔲 算法-硬件适配</div></div>""", unsafe_allow_html=True)
            with c3:
                loc = r.get("localization",{})
                st.markdown(f"""<div class="metric-box"><div class="num">{loc.get('rate','N/A')}%</div><div class="label">🇨🇳 国产化率</div></div>""", unsafe_allow_html=True)
            with c4:
                bom = r.get("bom_estimate",{})
                st.markdown(f"""<div class="metric-box"><div class="num" style="font-size:1.2rem">¥{bom.get('low','?')}-{bom.get('high','?')}</div><div class="label">💰 BOM成本</div></div>""", unsafe_allow_html=True)

            # 芯片推荐
            chip = r.get("chip_recommendation",{})
            st.markdown("#### 🔲 推荐芯片方案")
            st.success(f"**首选**：{chip.get('primary','N/A')}\n\n{chip.get('reason','')}")
            if chip.get("alternatives"):
                st.info(f"**备选**：{'、'.join(chip['alternatives'])}")

            # BOM明细
            st.markdown("#### 💰 BOM成本明细")
            bom_data = bom.get("breakdown", [])
            if bom_data and isinstance(bom_data[0], dict):
                bom_md = "| 组件 | 成本范围 | 国产化率 |\n|------|---------|--------|\n"
                for c in bom_data:
                    bom_md += f"| {c.get('name','')} | ¥{c.get('cost_range',c.get('low','?')+'-'+c.get('high','?'))} | {c.get('localization',c.get('rate','?')+'%')} |\n"
                st.markdown(bom_md)
            if bom.get("nre"):
                st.caption(f"💡 NRE费用(开模+认证+工具)：{bom['nre']} | 最小起订量：{bom.get('moq','N/A')}")

            # 国产化分析
            loc_comps = loc.get("components",[])
            if loc_comps:
                st.markdown("#### 🇨🇳 国产化分析")
                for c in loc_comps:
                    rate = c.get('rate',0)
                    badge = "green" if rate>=80 else "yellow" if rate>=50 else "red"
                    st.markdown(f"- <span class='status-badge {badge}'>{rate}%</span> **{c.get('name','')}** — {c.get('domestic','')}", unsafe_allow_html=True)

            # 风险
            risks = r.get("risks",[])
            if risks:
                st.markdown("#### ⚠️ 风险评估")
                for risk in risks:
                    level = risk.get('level','中')
                    badge = "red" if level=="高" else "yellow" if level=="中" else "green"
                    st.markdown(f"- <span class='status-badge {badge}'>{level}</span> **{risk.get('item','')}** — 缓解：{risk.get('mitigation','')}", unsafe_allow_html=True)

            st.info(f"💡 **综合建议**：{r.get('suggestion','')}")

            # 导出
            def _to_md(r):
                return f"# 硬件评估报告\n\n## 产品：{r.get('product_type','')} | 算法：{r.get('model_type','')}\n\n### 芯片推荐\n{r.get('chip_recommendation',{})}\n\n### BOM：¥{r.get('bom_estimate',{}).get('low','?')}-{r.get('bom_estimate',{}).get('high','?')}\n\n### 国产化率：{r.get('localization',{}).get('rate','?')}%\n\n### 建议\n{r.get('suggestion','')}"
            st.download_button("📥 导出评估报告", data=_to_md(r), file_name=f"硬件评估_{r['product_type']}_{r['date'][:10]}.md", mime="text/markdown")

    with tab2:
        if not st.session_state.evaluations:
            st.info("暂无评估记录")
        for r in reversed(st.session_state.evaluations):
            with st.expander(f"📊 {r.get('product_type','')} — {r.get('date','')} | 评分:{r.get('overall_score','')}"):
                st.write(f"芯片：{r.get('chip_recommendation',{}).get('primary','N/A')} | BOM：¥{r.get('bom_estimate',{}).get('low','?')}-{r.get('bom_estimate',{}).get('high','?')} | 国产化：{r.get('localization',{}).get('rate','?')}%")

    with tab3:
        st.markdown("#### 🔲 国产化AI芯片数据库")
        st.caption("涵盖主流国产NPU芯片，支持筛选和对比")
        filter_npu = st.selectbox("NPU算力", ["全部","<2 TOPS","2-6 TOPS","6-15 TOPS",">15 TOPS"])
        filter_loc = st.selectbox("国产化率", ["全部",">80%",">90%","100%"])

        chips = CHIP_DB[:]
        if filter_npu != "全部":
            npu_val = int(filter_npu.replace('>','').replace(' TOPS','').replace('<',''))
            if '<' in filter_npu: chips = [c for c in chips if int(c['npu'].replace(' TOPS','')) < npu_val]
            elif '>' in filter_npu: chips = [c for c in chips if int(c['npu'].replace(' TOPS','')) > npu_val]
            else:
                low,high = [int(x) for x in filter_npu.replace(' TOPS','').split('-')]
                chips = [c for c in chips if low <= int(c['npu'].replace(' TOPS','')) <= high]
        if filter_loc != "全部":
            threshold = int(filter_loc.replace('>','').replace('%',''))
            chips = [c for c in chips if int(c['localization'].replace('%','')) >= threshold]

        chip_md = "| 芯片 | 厂商 | NPU | 功耗 | 制程 | 国产化 | 价格 | 适配场景 |\n|------|------|-----|------|------|--------|------|----------|\n"
        for c in chips:
            chip_md += f"| **{c['name']}** | {c['vendor']} | {c['npu']} | {c['power']} | {c['process']} | {c['localization']} | {c['price']} | {','.join(c['fit'][:2])} |\n"
        st.markdown(chip_md)
