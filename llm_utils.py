"""LLM 工具模块 - 统一调用接口
v0.4 - 支持真实LLM调用 + 智能降级 + 会话缓存
"""
import subprocess, json, re, time, random
from datetime import datetime
from typing import Optional

# ─── LLM 调用 ───
def llm_chat(system_prompt: str, user_prompt: str, max_retries: int = 2, timeout: int = 60) -> Optional[str]:
    """通过 z-ai CLI 调用 LLM，含指数退避重试"""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ["z-ai", "chat", "-p", user_prompt, "-s", system_prompt],
                capture_output=True, text=True, timeout=timeout
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                lines = [l for l in output.split('\n') if l.strip() and not l.startswith('🚀')]
                output = '\n'.join(lines)
                if output:
                    return output
            if "429" in result.stderr or "Too many" in result.stderr:
                wait = 5 * (attempt + 1)
                time.sleep(wait)
                continue
        except subprocess.TimeoutExpired:
            continue
        except Exception:
            time.sleep(2)
            continue
    return None


def llm_json(system_prompt: str, user_prompt: str, fallback: dict = None) -> dict:
    """调用 LLM 并解析 JSON 响应，失败返回 fallback"""
    raw = llm_chat(system_prompt, user_prompt)
    if raw:
        try:
            json_match = re.search(r'\{[\s\S]*\}', raw)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    return fallback or {}


def parse_json_response(raw: str, fallback: dict = None) -> dict:
    """从 LLM 原始输出中提取 JSON"""
    if not raw:
        return fallback or {}
    try:
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            return json.loads(json_match.group())
    except json.JSONDecodeError:
        pass
    return fallback or {}


def llm_list(system_prompt: str, user_prompt: str, fallback: list = None) -> list:
    """调用 LLM 并解析 JSON 数组响应"""
    raw = llm_chat(system_prompt, user_prompt)
    if raw:
        try:
            json_match = re.search(r'\[[\s\S]*\]', raw)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    return fallback or []


# ─── 模拟数据生成器（LLM 不可用时的高质量 fallback） ───
class SimData:
    """模拟数据生成器 - 基于输入参数生成合理的演示数据"""

    @staticmethod
    def blindbox(tech_name, tech_field="", trl_level="TRL4"):
        return {
            "name": tech_name, "score": random.randint(65, 88), "trl": trl_level,
            "market_size": "10-50亿", "target_customers": "制造业/医疗/金融",
            "competition_level": "中等", "time_to_market": "1-2年", "risk_level": "中等",
            "strengths": ["技术壁垒高", "市场需求明确", "政策支持"],
            "weaknesses": ["产业化周期长", "人才稀缺"],
            "opportunities": ["国产替代需求", "AI+行业融合", "新质生产力政策"],
            "threats": ["国际竞争加剧", "技术迭代快"],
            "suggestion": f"建议先完成中试验证，锁定1-2个垂直场景快速落地「{tech_name}」。"
        }

    @staticmethod
    def fedmatch(field="人工智能"):
        pool = {
            "人工智能": [
                {"name":"基于联邦学习的医疗影像AI诊断","school":"清华大学","trl":"TRL 5","score":92,"patent":"CN202310XXXXXX","brief":"在3家三甲医院完成临床验证，诊断准确率96.3%","highlights":["已获3项发明专利","临床验证数据充分"],"risk":["需要大量标注数据"],"budget":"许可费200-500万/年"},
                {"name":"多模态大模型高效推理框架","school":"北京大学","trl":"TRL 4","score":85,"patent":"CN202410XXXXXX","brief":"推理速度提升3-5倍，显存占用降低60%","highlights":["开源社区Star 2.3k","多篇顶会论文"],"risk":["技术迭代快"],"budget":"技术许可+联合开发"},
                {"name":"基于强化学习的智能调度系统","school":"浙江大学","trl":"TRL 6","score":78,"patent":"CN202310XXXXXX","brief":"已在3家工厂部署，产能提升15%","highlights":["已有落地案例","ROI可量化"],"risk":["行业定制化需求强"],"budget":"许可费50-150万/年"},
            ],
            "生物医药": [
                {"name":"新型mRNA递送脂质纳米颗粒","school":"复旦大学","trl":"TRL 4","score":89,"patent":"CN202410XXXXXX","brief":"递送效率提升40%，已在动物模型中验证","highlights":["递送效率显著提升","专利壁垒高"],"risk":["临床前数据有限"],"budget":"许可费300-800万+里程碑"},
                {"name":"AI辅助药物分子生成平台","school":"中国科学技术大学","trl":"TRL 3","score":76,"patent":"CN202310XXXXXX","brief":"已生成3个候选分子进入体外验证","highlights":["AI+制药交叉","生成效率高"],"risk":["候选分子需进一步验证"],"budget":"合作开发+里程碑付款"},
            ],
        }
        default = [
            {"name":"高效能量存储复合材料","school":"南京大学","trl":"TRL 5","score":82,"patent":"CN202410XXXXXX","brief":"能量密度提升35%，循环寿命2000次以上","highlights":["性能指标领先","制备工艺成熟"],"risk":["规模化生产待验证"],"budget":"许可费100-300万/年"},
            {"name":"工业废水深度处理技术","school":"同济大学","trl":"TRL 6","score":75,"patent":"CN202310XXXXXX","brief":"处理成本降低50%，已在2个工业园区示范","highlights":["已有示范工程","处理效果好"],"risk":["适用场景有限"],"budget":"许可费80-200万/年"},
        ]
        results = pool.get(field, default)
        random.shuffle(results)
        return results

    @staticmethod
    def tech_radar(name, field="", current_trl="TRL 4"):
        window = random.randint(12, 60)
        threat_level = random.choice(["🟢 低", "🟡 中", "🔴 高"])
        disruptor = random.choice(["Transformer架构", "扩散模型", "大语言模型", "量子计算", "类脑计算"])
        trend = random.choice(["📈 上升期", "📊 平台期", "📉 衰退期"])
        return {
            "window_months": window, "threat_level": threat_level,
            "disruptor": disruptor, "trend": trend,
            "score": random.randint(40, 90),
            "patent_growth": f"{random.randint(15, 45)}%",
            "competitors": random.randint(2, 8),
            "paper_growth": f"{random.randint(20, 60)}%",
        }

    @staticmethod
    def hw_eval(tech_name, target_chip=""):
        return {
            "name": tech_name,
            "chip_benchmark": {"recommended": "RK3588 / 算能BM1684", "performance": "满足端侧推理需求", "power": "5-15W"},
            "algorithm_fit": {"score": 72, "bottleneck": "模型量化精度损失", "optimization": "INT8量化+剪枝"},
            "bom_cost": {"estimate": "500-2000元/台", "breakdown": {"chip": "200-800元", "sensor": "100-300元", "pcb": "50-150元", "assembly": "100-300元", "other": "50-450元"}},
            "localization_rate": 65, "risk_level": "中等",
            "suggestion": "建议优先验证RK3588适配性，同步评估国产替代方案。"
        }


# ─── 会话状态初始化 ───
def init_session_state():
    """初始化所有模块的 session_state"""
    defaults = {
        "evaluations": [], "translations": [], "analyses": [],
        "matches": [], "radar_scans": [], "bp_records": [],
        "posts": [], "deals": [], "hw_evals": [], "hw_translations": [],
        "hw_analyses": [], "proto_projects": [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ─── 延迟导入（避免循环依赖） ───
import streamlit as st
