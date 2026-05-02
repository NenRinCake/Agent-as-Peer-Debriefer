import os
from typing import Dict, Tuple, Any, List
import openai
import json
from prompt import *
import pdb
import re
from thefuzz import fuzz
from openai import OpenAI


datasets_name = "Scrum_RQ1"  # Scrum_RQ1  Scrum_RQ2  UCSB_code  UCSB_subtheme  UCSB_theme
api_key = "your_api_key"
trial_num = 1

research_questions = []
clustering_style = []
coding_style = []
conceptualizing_style = []
number_clusters = []
raw_text_data = []
ground_truth = []
generate_code = []
total_count = 0
use_count = 0
data_num = 0


def get_data(data_name):
    if data_name == "Scrum_RQ1":
        return r"data\Software_Quality_RQ1.jsonl"
    elif data_name == "Scrum_RQ1":
        return r"data\Software_Quality_RQ2.jsonl"
    elif data_name == "UCSB_code" or data_name == "UCSB_subtheme" or data_name == "UCSB_theme":
        return r"data\UCSB.jsonl"
    else:
        print("Error DataName")
        return


data_path = get_data(datasets_name)
with open(r"data\Software_Quality_RQ2.jsonl", encoding='utf-8') as f:
    for line in f:
        record = json.loads(line.strip())
        raw_text_data.append(record["analyze_text"])
        research_questions.append(record["research_question"])
        number_clusters.append(record["number_cluster"])
        clustering_style.append('')
        coding_style.append('')
        conceptualizing_style.append('')
        data_num += 1

with open(r"data\ground_truth.jsonl", encoding='utf-8') as f:
    for line in f:
        record = json.loads(line.strip())
        if record["name"] == datasets_name:
            ground_truth = record["ground_truth"]

stage_prompt_name = ['code_prompt',
                     'subtheme_prompt',
                     'theme_prompt',
                     'display_report_prompt',
                     'display_graph_prompt',
                     'code_applied_agent_prompt',
                     'code_theory_agent_prompt',
                     'code_data_agent_prompt',
                     'code_self_refine_prompt',
                     'subtheme_applied_agent_prompt',
                     'subtheme_theory_agent_prompt',
                     'subtheme_data_agent_prompt',
                     'subtheme_self_refine_prompt',
                     'theme_applied_agent_prompt',
                     'theme_theory_agent_prompt',
                     'theme_data_agent_prompt',
                     'theme_self_refine_prompt']


def call_qwen_api(prompt, model="qwen3.5-plus", temperature=1):
    """
    Sends a prompt to the specified OpenAI model and returns the text response.
    """
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=8192*8,
    )
    # print(response.model_dump_json())
    if response.choices and len(response.choices) > 0:
        return response.choices[0].message.content
    else:
        return ""


def purify_str(item):
    cleaned = re.sub(r"^```.*$", "", item, flags=re.MULTILINE)
    return cleaned


def load_json(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)


def cache_or_call(output_name, call_prompt):
    if os.path.exists(output_name):
        print('cache %s' % output_name)
        with open(output_name, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print('call %s' % output_name)
        output_response = purify_str(call_qwen_api(call_prompt))
        print(output_response)
        with open(output_name, "w", encoding="utf-8") as f:
            f.write(output_response)
        return output_response


def extract_json_from_str(json_str: str) -> Tuple[str, str, str]:
    """
    Split LLM qualitative analysis output into:
    1) main data (without metadata)
    2) what_llm_did
    3) self_reflection
    (all returned as JSON strings)
    """
    data: Dict[str, Any] = json.loads(json_str)

    metadata = data.get("metadata", {})
    what_llm_did = metadata.get("what_llm_did", {})
    self_reflection = metadata.get("self_reflection", {})

    # Remove metadata from main data
    main_data = {k: v for k, v in data.items() if k != "metadata"}

    return (
        json.dumps(main_data, ensure_ascii=False, indent=2),
        json.dumps(what_llm_did, ensure_ascii=False, indent=2),
        json.dumps(self_reflection, ensure_ascii=False, indent=2),
    )


def extract_json_from_agent_str(json_str: str) -> Tuple[str, str]:
    """
    Split LLM qualitative analysis output into:
    1) main data (without modification_summary)
    2) modification_summary
    (all returned as JSON strings)
    """
    data: Dict[str, Any] = json.loads(json_str)

    modification_summary = data.get("modification_summary", {})

    # Remove metadata from main data
    main_data = {k: v for k, v in data.items() if k != "modification_summary"}

    return (
        json.dumps(main_data, ensure_ascii=False, indent=2),
        json.dumps(modification_summary, ensure_ascii=False, indent=2),
    )


def extract_code_names_from_agent_str(json_str: str) -> List[str]:
    """
    从 LLM qualitative 输出中提取所有 Code 层的 name
    """

    data: Dict[str, Any] = json.loads(json_str)

    names = []

    def traverse(obj):
        if isinstance(obj, dict):
            # 只有同时存在 name 和 chunks 才认为是 Code
            if "name" in obj and "chunks" in obj:
                names.append(obj["name"])

            for v in obj.values():
                traverse(v)

        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(data)

    return names


def extract_subtheme_names_from_agent_str(json_str: str) -> List[str]:
    """
    从 LLM qualitative 输出中提取所有 Sub-Theme 层的 name
    """

    data: Dict[str, Any] = json.loads(json_str)

    names: List[str] = []

    for key, value in data.items():
        if key.startswith("Sub-Theme") and isinstance(value, dict):
            if "name" in value:
                names.append(value["name"])

    return names


def extract_theme_names_from_agent_str(json_str: str) -> List[str]:
    """
    从 LLM qualitative 输出中提取所有 Theme 层的 name
    """

    data: Dict[str, Any] = json.loads(json_str)

    names: List[str] = []

    for value in data.values():
        if isinstance(value, dict) and "subthemes" in value and "name" in value:
            names.append(value["name"])

    return names


def fetch_data(perspective):
    global generate_code, total_count, use_count
    if perspective not in ['applied', 'theory', 'data', 'refine']:
        print('No such analytical perspective exists')
        return

    code_agent_prompt = ""
    subtheme_agent_prompt = ""
    theme_agent_prompt = ""
    if perspective == 'applied':
        code_agent_prompt = code_applied_agent_prompt
        subtheme_agent_prompt = subtheme_applied_agent_prompt
        theme_agent_prompt = theme_applied_agent_prompt
    elif perspective == 'theory':
        code_agent_prompt = code_theory_agent_prompt
        subtheme_agent_prompt = subtheme_theory_agent_prompt
        theme_agent_prompt = theme_theory_agent_prompt
    elif perspective == 'data':
        code_agent_prompt = code_data_agent_prompt
        subtheme_agent_prompt = subtheme_data_agent_prompt
        theme_agent_prompt = theme_data_agent_prompt
    elif perspective == 'refine':
        code_agent_prompt = code_self_refine_prompt
        subtheme_agent_prompt = subtheme_self_refine_prompt
        theme_agent_prompt = theme_self_refine_prompt
    else:
        return
    print(perspective)
    for i in range(data_num):
        for j in range(trial_num):
            total_count += count_characters(raw_text_data[i])
            code_str = code_prompt.replace("{inputData}", raw_text_data[i]).replace("{researchQuestions}",
                                                                                    research_questions[i]).replace(
                "{numberOfTopicClusters}", str(number_clusters[i])).replace("{clusteringStyle}",
                                                                            str(clustering_style[i]))

            # code
            output_name = f"../output/qwen3.5p-{datasets_name}-output/data%d_trial%d_code_output.json" % (i, j)
            code_response = cache_or_call(output_name, code_str)
            code_response, code_explanation, code_self_criticize = extract_json_from_str(code_response)

            # code_agent
            output_name = f"../output/qwen3.5p-{datasets_name}-output/data%d_trial%d_{perspective}_agent_code_output.json" % (
            i, j)
            code_agent_str = code_agent_prompt.replace("{inputData}", code_response).replace("{researchQuestions}",
                                                                                             research_questions[
                                                                                                 i]).replace(
                "{explanation}", code_explanation).replace("{self_criticize}", code_self_criticize)
            # print(code_agent_str)
            code_agent_response = cache_or_call(output_name, code_agent_str)
            code_response, code_agent_modification_summary = extract_json_from_agent_str(code_agent_response)
            generate_code.extend(extract_code_names_from_agent_str(code_response))
            use_count += deduplicate_chunks_from_str(code_response)

            # sub-theme
            output_name = f"../output/qwen3.5p-{datasets_name}-output/data%d_trial%d_{perspective}_subtheme_output.json" % (
            i, j)
            sub_theme_str = subtheme_prompt.replace("{inputData}", code_response).replace("{numberOfTopicClusters}",
                                                                                          str(number_clusters[
                                                                                                  i])).replace(
                "{codingStyle}", str(coding_style[i]))
            sub_theme_response = cache_or_call(output_name, sub_theme_str)
            sub_theme_response, sub_theme_explanation, sub_theme_self_criticize = extract_json_from_str(
                sub_theme_response)

            # sub-theme_agent
            output_name = f"../output/qwen3.5p-{datasets_name}-output/data%d_trial%d_{perspective}_agent_subtheme_output.json" % (
            i, j)
            sub_theme_agent_str = subtheme_agent_prompt.replace("{inputData}", sub_theme_response).replace(
                "{researchQuestions}", research_questions[i]).replace("{explanation}", sub_theme_explanation).replace(
                "{self_criticize}", sub_theme_self_criticize)
            # print(sub_theme_agent_str)
            sub_theme_agent_response = cache_or_call(output_name, sub_theme_agent_str)
            sub_theme_response, sub_theme_agent_modification_summary = extract_json_from_agent_str(
                sub_theme_agent_response)
            # generate_code.extend(extract_subtheme_names_from_agent_str(sub_theme_response))

            # theme
            output_name = f"../output/qwen3.5p-{datasets_name}-output/data%d_trial%d_{perspective}_theme_output.json" % (i, j)
            theme_str = theme_prompt.replace("{inputData}", sub_theme_response).replace("{researchQuestions}",
                                                                                        research_questions[i]).replace(
                "{conceptualizingStyle}", str(conceptualizing_style[i]))
            theme_response = cache_or_call(output_name, theme_str)
            theme_response, theme_explanation, theme_self_criticize = extract_json_from_str(theme_response)

            # theme_agent
            output_name = f"../output/qwen3.5p-{datasets_name}-output/data%d_trial%d_{perspective}_agent_theme_output.json" % (i, j)
            theme_agent_str = theme_agent_prompt.replace("{inputData}", theme_response).replace("{researchQuestions}",
                                                                                                research_questions[
                                                                                                    i]).replace(
                "{explanation}", theme_explanation).replace("{self_criticize}", theme_self_criticize)
            theme_agent_response = cache_or_call(output_name, theme_agent_str)
            # theme_response, theme_agent_modification_summary = extract_json_from_agent_str(theme_agent_response)
            # generate_code.extend(extract_theme_names_from_agent_str(theme_response))

            # output_name = "./output/data%d_trial%d_display_report_output.json"%(i,j)
            # display_report_str = display_report_prompt.replace("{inputData}", theme_response).replace("{researchQuestions}", research_questions[i])
            # display_report_response = cache_or_call(output_name, display_report_str)
            # # print(display_report_response)
            #
            #
            # output_name = "./output/data%d_trial%d_display_graph_output.json"%(i,j)
            # display_graph_str = display_graph_prompt.replace("{inputData}", theme_response).replace("{researchQuestions}", research_questions[i])
            # display_graph_response = cache_or_call(output_name, display_graph_str)


import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel


def count_characters(text: str) -> int:
    """
    统计字符串的字符总数（包含空格和标点）
    """
    if not isinstance(text, str):
        raise TypeError("输入必须是字符串")

    return len(text.strip())


def deduplicate_chunks_from_str(json_str):
    """
    参数:
        json_str: JSON格式的字符串

    返回:
        deduplicated_data (dict),
        total_char_count (int)
    """

    # 1️⃣ 解析字符串
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError("输入不是合法的 JSON 字符串") from e

    seen = set()
    duplicates = []
    total_char_count = 0

    # 2️⃣ 遍历所有 Code
    for key, value in data.items():
        if not key.startswith("Code"):
            continue

        new_chunks = []

        for chunk in value.get("chunks", []):
            clean_chunk = chunk.strip()

            if clean_chunk in seen:
                duplicates.append(clean_chunk)
            else:
                seen.add(clean_chunk)
                new_chunks.append(chunk)
                total_char_count += len(clean_chunk)

        value["chunks"] = new_chunks

    return total_char_count


def get_embeddings(texts, model, tokenizer, device="cpu"):
    inputs = tokenizer(
        texts,
        padding=True,
        truncation=True,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        last_hidden = outputs.last_hidden_state  # (B, T, H)

    # mean pooling
    attention_mask = inputs["attention_mask"].unsqueeze(-1)
    summed = torch.sum(last_hidden * attention_mask, dim=1)
    counts = torch.clamp(attention_mask.sum(dim=1), min=1e-9)
    mean_pooled = summed / counts

    # L2 归一化
    return F.normalize(mean_pooled, p=2, dim=1)


def match_codes(gt_list, pred_list, threshold=0.7, device="cpu"):
    tokenizer = AutoTokenizer.from_pretrained(
        r"sentence-transformers/all-MiniLM-L6-v2"
    )
    model = AutoModel.from_pretrained(
        r"sentence-transformers/all-MiniLM-L6-v2"
    ).to(device)
    model.eval()

    gt_emb = get_embeddings(gt_list, model, tokenizer, device)
    pred_emb = get_embeddings(pred_list, model, tokenizer, device)

    # 余弦相似度矩阵
    sim_matrix = torch.matmul(gt_emb, pred_emb.T)
    sim_matrix = (sim_matrix + 1) / 2
    result = {}
    for j, pred in enumerate(pred_list):
        scores = sim_matrix[:, j]  # 所有gt与这个pred的相似度
        max_score, max_idx = torch.max(scores, dim=0)
        if max_score.item() >= threshold:
            gt_matched = gt_list[max_idx]
            if gt_matched not in result:
                result[gt_matched] = []
            result[gt_matched].append(pred)

    return result


def self_match(pred_list, threshold=0.7, device="cpu"):
    tokenizer = AutoTokenizer.from_pretrained(
        r"sentence-transformers/all-MiniLM-L6-v2"
    )
    model = AutoModel.from_pretrained(
        r"sentence-transformers/all-MiniLM-L6-v2"
    ).to(device)
    model.eval()

    # 获取 embedding
    pred_emb = get_embeddings(pred_list, model, tokenizer, device)

    # 归一化（确保是 cosine）
    pred_emb = torch.nn.functional.normalize(pred_emb, p=2, dim=1)

    # 计算相似度矩阵
    sim_matrix = torch.matmul(pred_emb, pred_emb.T)
    sim_matrix = (sim_matrix + 1) / 2  # 映射到 [0,1]

    visited = set()
    clusters = []

    for i in range(len(pred_list)):
        if i in visited:
            continue

        cluster = [i]
        visited.add(i)

        for j in range(i + 1, len(pred_list)):
            if j in visited:
                continue
            if sim_matrix[i, j].item() >= threshold:
                cluster.append(j)
                visited.add(j)

        clusters.append(cluster)

    # 返回剩余数量（cluster数量）
    return len(clusters)


def compute_score(code_match, ground_truth, generate_code, self_num, use_count, total_count):
    matched_codes_count = sum(len(v) for v in code_match.values())
    match_rate = matched_codes_count / len(generate_code)
    recall = len(code_match) / len(ground_truth)
    code_diversity = self_num / len(generate_code)
    text_utilization_rate = use_count / total_count
    print(f"recall:  {round(recall, 3)}")
    print(f"match rate: {round(match_rate, 3)}")
    print(f"code diversity: {round(code_diversity, 3)}")
    print(f"text utilization rate: {round(text_utilization_rate, 3)}")


def extract_chunks(obj):
    gathered = []
    if isinstance(obj, dict):
        # If current object is a dict, check if it has a "chunks" key
        if "chunks" in obj and isinstance(obj["chunks"], list):
            gathered.extend(obj["chunks"])
        # Recursively check all sub-values
        for value in obj.values():
            gathered.extend(extract_chunks(value))
    elif isinstance(obj, list):
        # If current object is a list, recurse on each item
        for item in obj:
            gathered.extend(extract_chunks(item))
    return gathered


def extract_cluster_names(obj, result=None):
    if result is None:
        result = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("Code"):
                # If this is a cluster, get its name if present
                if "name" in v:
                    result.append(v["name"])
            # Recurse deeper
            extract_cluster_names(v, result)
    elif isinstance(obj, list):
        for item in obj:
            extract_cluster_names(item, result)
    return result


def extract_code_names(obj, result=None):
    if result is None:
        result = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("Sub-Theme"):
                # If this is a cluster, get its name if present
                if "name" in v:
                    result.append(v["name"])
            # Recurse deeper
            extract_code_names(v, result)
    elif isinstance(obj, list):
        for item in obj:
            extract_code_names(item, result)
    return result


def extract_concept_names(obj, result=None):
    if result is None:
        result = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("Theme"):
                # If this is a cluster, get its name if present
                if "name" in v:
                    result.append(v["name"])
            # Recurse deeper
            extract_concept_names(v, result)
    elif isinstance(obj, list):
        for item in obj:
            extract_concept_names(item, result)
    return result


def main():
    fetch_data('refine')  #  applied  theory  data  refine
    print(generate_code)
    codes_match = match_codes(ground_truth, generate_code)
    self_num = self_match(generate_code)
    compute_score(codes_match, ground_truth, generate_code, self_num, use_count, total_count)


if __name__ == "__main__":
    main()