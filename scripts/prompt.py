code_prompt = '''
You are a helpful qualitative analysis assistant. Please assist with organizing qualitative data into different topics to perform open codes.

Qualitative Data:
{inputData}

Research Questions:
{researchQuestions}
(Use this research question to identify the direction of the grouping strategy.)

Number of Codes:
{numberOfTopicClusters}
(Generate multiple open codes based on the content from the uploaded data. The number of open codes should be between the two numbers given above. )


Open Codes Style:
{clusteringStyle}
(ALWAYS use this "Open Codes Style" to guide how to assign open codes names to the data. If it is empty, assign open codes names based on semantic meaning using the original terms from the data.)

Task Description:
- First, analyze the raw text content from the uploaded data and divide it into meaningful chunks based on the topic similarity. Each chunk should contain the exact original text without any modifications.
- Then, create multiple open codes (as specified by 'Number of Open Codes'), each containing content chunks with similar topics.
- Give 2 examples of meaningful chunks with same code from results to explain clearly in  the "metadata" example section.
- Add the self reflect part for the actions you did in the "metadata"  reflect section. Your self-reflection should be structured into three parts:
    1）Confident Results. Summarize the codes you are most confident about. Provide a brief reason why (e.g., strong thematic coherence, clear recurring concept, well-supported by multiple codes).
    2) Uncertain Results. Summarize the codes you are least confident about. Provide a brief reason why (e.g., open codes overlaps multiple topics, ambiguous language, limited supporting chunks, weak thematic clarity).
    3) Recommended Human Review Focus. Suggest which parts of your coding results should be prioritized for human checking and interpretation and explain why briefly.

Requirements:
- DO NOT alter, paraphrase, or revise any part of the original contents. Each chunk must contain the EXACT SAME text as it appears in the original data.
- Do not assign specific names to the Codes. Instead, label them sequentially as "Code 1", "Code 2", and so on. Each Code should begin with the format {Code X:}, where X represents the Code number.
- Under each Code, begin with an item labeled "name". The name should be specific, should directly relates to the research question; Includes specific entities, concepts, or terms from the content chunks in that Code; Avoids generic or vague labels.
- Follow this with an item labeled "chunks," which includes all chunks relevant to the Code name. Group chunks by shared topics to maintain thematic consistency within each Code.
- All data should be put into chunks, but prioritize those most relevant and meaningful words to the research questions to Codes.
- In self reflect section, any reference to codes should not alter the oiginal code number and name.
- Avoid Code number in "metadata" section, use Code 【Code Name PlaceHolder】 instead.

Output Format:
Provide the output strictly in JSON format without any additional text or explanations. 
Generate a title/name for each Code no more than 20 characters. 
Don't include strange characters (e.g., '\', '') in any text. 
Do not abbreviate the original data from the uploaded data; instead, output all content exactly as it appears in the original data.

Code Example:
{
  
  "Code X":{ 
    "name": "placeholder",
    "chunks":
      [
        "xxxx",
        "xxxx",
        "xxxxxxx"
        "xxxx"
        // Additional entries can be added here as needed
      ]
  },
  "metadata": {
    "what_llm_did": {
      "main_actions": "Analyzed qualitative data and generated open codes by dividing text into meaningful chunks",
      "examples": "Code【Code Name PlaceHolder】 contains chunks about classroom management because they share similar themes about student engagement strategies"
    },
    "self_reflection": {
      "confident_results": "Most confident about Code【Code Name PlaceHolder】 and Code 【Code Name PlaceHolder】 due to clear thematic coherence",
      "uncertain_results": "Less confident about Code 【Code Name PlaceHolder】 which may overlap with multiple topics", 
      "recommended_review": "Focus on reviewing boundary clarity between overlapping codes for human validation"
    }
  }
}
'''





subtheme_prompt = """
You are a helpful qualitative analysis assistant. Your task is to perform axial coding to generate sub-themes based on codes provided. 


Uploaded Data:
{inputData}

Number of Codes:
{numberOfTopicClusters}

Sub Theme Style:
{codingStyle}
(ALWAYS use this "Sub Theme Style" to guide how to assign sub-themes to the data. If it is empty, assign sub-theme names that descriptively and specifically summarize the main content of the data.)


Task Description:
- Data: The qualitative data for axial coding analysis is under "Uploaded Data", comprising different Codes that can be grouped.
- Grouping: Group similar "Code X" based on high-level thematic overlap. Maintain the original Code numbers (e.g., "Code 4" should remain "Code 4"), even after grouping.
- Coding: Propose and assign a group name (i.e., Sub-Theme X) to each group that best represents the main theme or topic of the grouped Codes.
- Sub-Theme names should be descriptive and specific, containing key concepts, terms, and entities from the content. Each sub-theme name should be 4-8 words long and clearly reflect the main theme of its grouped Codes.
- For each sub-theme, generate a concise, specific, and comprehensive definition that captures the essence (core meaning) of the sub-theme. The definition should not merely restate the sub-theme name, nor simply summarize the codes; it must express why the grouped codes belong together. 
- The number of sub-themes should be between 5 and the total number of Codes in the uploaded data, ensuring sufficient thematic granularity while maintaining meaningful groupings.
- Give 2 examples of codes with same sub-themes from results to explain clearly in  the "metadata"  example section.
- Add the self reflect part for the actions you did in the "metadata" reflect section. Your self-reflection should be structured into three parts:
    1）Confident Results. Summarize the sub-themes you are most confident about. Provide a brief reason why (e.g., strong thematic coherence, clear recurring concept, well-supported by multiple codes).
    2) Uncertain Results. Summarize the sub-themes you are least confident about. Provide a brief reason why (e.g., open codes overlaps multiple topics, ambiguous language, limited supporting chunks, weak thematic clarity).
    3) Recommended Human Review Focus. Suggest which parts of your sub-theme results should be prioritized for human checking and interpretation and explain why briefly.


Requirement:
- Do not modify, rephrase, or revise any part of the original Code names, Code numbers, or chunk content—only organize and label them based on thematic similarity 
- ALL Codes from the input data MUST be grouped. No Codes can be omitted.
- Definition should inlcude a definition part no longer than 2 sentences (max 200 characters) and example part contains 3 (if have) examples (max 600 characters). 
    1) Definition part should explicitly state what the sub-theme is about and why it matters in relation to the data.
    2) Follow this output style: "This sub-theme captures XXX. Examples:  1) Code 【Code Name PlaceHolder】, because yyy. 2) Code 【Code Name PlaceHolder】, because yyy. 3) Code 【Code Name PlaceHolder】, because yyy.".
    3）Be written at the semantic level (surface meaning of the data), avoid speculation or latent interpretation.
- In self reflect section, any reference to sub-theme should not alter the oiginal sub-theme number and name.
- Avoid Sub-Theme number and Code number in "metadata" section, use Sub-Themes 【Sub-Theme Name PlaceHolder】 and Code 【Code Name PlaceHolder】 instead.


Output Format:
Generate the output strictly in JSON format with NO additional text or explanations. 
Maintain the original Code indices (e.g., Code 1, Code 2) to organize the items within each Code. 
Do not output any additional Codes that are not present in the input data.
Only output the content format similar to the few shot example. Do not output any additional contents.

Follow the structure below:
{
    "Sub-Theme 1": {
      "name": "xxxx",
      "definition": "This sub-theme describes XXX. Examples:  1) Code 【Code Name PlaceHolder】, because yyy. 2) Code 【Code Name PlaceHolder】, because yyy. 3) Code 【Code Name PlaceHolder】, because yyy.",
      "codes": {
        "Code 1": { 
            "name": "placeholder",
            "chunks":[
                "xxxx",
                "xxxx"
                ]
            },
        "Code 2": { 
            "name": "placeholder",
            "chunks":[
                "xxxx",
                "xxxxxxx"
                ]
            }
      }
    },
    "Sub-Theme 2": {
      "name": "xxxx",
      "definition": "This sub-theme describes XXX. Examples:  1) Code 【Code Name PlaceHolder】, because yyy. 2) Code 【Code Name PlaceHolder】, because yyy. 3) Code 【Code Name PlaceHolder】, because yyy.",
      "codes": {
        "Code 3": { 
            "name": "placeholder",
            "chunks":[
                "xxxx",
                "xxxx",
                "xxxxxxx"
                "xxxx"
                ]
            }
      }
    },
    # add more codes as needed
    "metadata": {
    "what_llm_did": {
      "main_actions": "Performed axial coding to group codes into sub-themes based on thematic overlap",
      "examples": "Sub-Theme 【Sub-Theme Name PlaceHolder】 includes Code 【Code Name PlaceHolder】 and Code 【Code Name PlaceHolder】 because they both relate to similar conceptual patterns"
    },
    "self_reflection": {
      "confident_results": "Strong confidence in Sub-Theme 【Sub-Theme Name PlaceHolder】 and Sub-Theme 【Sub-Theme Name PlaceHolder】 due to clear thematic coherence",
      "uncertain_results": "Less confident about Code 【Code Name PlaceHolder】 placement which could fit multiple sub-themes",
      "recommended_review": "Review grouping decisions for codes with potential overlap between sub-themes"
    }
  }
 }
"""





theme_prompt = """
You are a helpful qualitative analysis assistant. I have developed codes,please assist by developing high-level descriptive themes by grouping sub-themes together. 

Research Questions
{researchQuestions}
(Use this question to identify the direction of the grouping strategy.)

Sub-Themes Need To Be Analysed:
{inputData}


Theme Style
{conceptualizingStyle}
(ALWAYS use this "Theme Style" to guide how to assign themes to the data. If it is empty, assign theme names that provide a high-level summary of the main content of the data.)


Task Description:
1.	Group the uploaded sub-themes based on shared high-level themes, with the grouping guided by the underlying research question.
2.	For each theme, generate a concise, specific, and comprehensive definition that captures the essence (core meaning) of the theme. The definition should not merely restate the theme name, nor simply summarize the sub-themes; it must express why the grouped sub-themes belong together. 
3.	The number of themes should be fewer than the number of sub-themes—ideally three.
4.  Give 2 examples of sub-themes with same themes from results to explain clearly in  the "metadata" example section.
5. Add the self reflect part for the actions you did in the "metadata" reflect section. Your self-reflection should be structured into three parts:
    1）Confident Results. Summarize the themes you are most confident about. Provide a brief reason why (e.g., strong thematic coherence, clear recurring concept, well-supported by multiple codes).
    2) Uncertain Results. Summarize the themes you are least confident about. Provide a brief reason why (e.g., open codes overlaps multiple topics, ambiguous language, limited supporting chunks, weak thematic clarity).
    3) Recommended Human Review Focus. Suggest which parts of your theme results should be prioritized for human checking and interpretation and explain why briefly.

Requirement:
- Do not modify, rephrase, or revise any part of the original sub-theme names,  sub-theme numbers, code names, code numbers, or content—only organize and label them based on thematic similarity.
- ALL sub-themes from the input data MUST be grouped. No sub-themes can be omitted.
- Definition should inlcude a definition part no longer than 2 sentences (max 200 characters) and example part contains 3 (if have) examples (max 600 characters). 
    1) Definition part should explicitly state what the theme is about and why it matters in relation to the data.
    2) Follow this output style: "This theme captures XXX. Examples:  1) Sub-Theme 【Sub-Theme Name PlaceHolder】, because yyy. 2) Sub-Theme 【Sub-Theme Name PlaceHolder】, because yyy. 3) Sub-Theme 【Sub-Theme Name PlaceHolder】, because yyy.".
    3）Be written at the semantic level (surface meaning of the data), avoid speculation or latent interpretation.
- List the main actions you did from the uploaded data in the "metadata" section. And the rationale for the actions you did.
- In self reflect section, any reference to theme should not alter the oiginal theme number and name.
- Avoid Theme number, Sub-Thme number, and code number in "metadata" section, use Theme 【Theme Name PlaceHolder, Sub-Theme 【Sub-Theme Name PlaceHolder】 and Code 【Code Name PlaceHolder】 instead.


Output Format:
Generate the output strictly in JSON format with NO additional text or explanations. Use the original Code id (Code 1, Code 2) to track the items in the code. NO change the original code number and name. Use the following format:
{
  "Theme 1": {
    "name": "xxx",
    "definition": "This theme describes XXX. Examples:  1) Sub-Theme 【Sub-Theme Name PlaceHolder】, because yyy. 2) Sub-Theme 【Sub-Theme Name PlaceHolder】, because yyy. 3) Sub-Theme 【Sub-Theme Name PlaceHolder】, because yyy.",
    "subthemes": {
      "Sub-Theme 1": {
        "name": "xxxx",
        "codes": {
          "Code 1": {
            "name": "placeholder",
            "chunks": [
              "xxxx",
              "xxxx"
            ]
          },
          "Code 2": {
            "name": "placeholder",
            "chunks": [
              "xxxx",
              "xxxxxxx"
            ]
          }
        }
      },
      "Sub-Theme 2": {
        "name": "xxxx",
        "codes": {
          "Code 3": {
            "name": "placeholder",
            "chunks": [
              "xxxx",
              "xxxx",
              "xxxxxxx",
              "xxxx"
            ]
          }
        }
      }
    },
    "Theme 2": {
    "name": "xxx",
    "definition": "This theme describes XXX. Examples:  1) Sub-Theme 【Sub-Theme Name PlaceHolder】, because yyy. 2) Sub-Theme 【Sub-Theme Name PlaceHolder】, because yyy. 3) Sub-Theme 【Sub-Theme Name PlaceHolder】, because yyy.",
    "subthemes": {
      "Sub-Theme 3": {
        "name": "xxxx",
        "codes": {
          "Code 4": {
            "name": "placeholder",
            "chunks": [
              "xxxx",
              "xxxx"
            ]
          },
          "Code 5": {
            "name": "placeholder",
            "chunks": [
              "xxxx",
              "xxxxxxx"
            ]
          }
        }
      }
    }
  },
  "metadata": {
    "what_llm_did": {
      "main_actions": "Developed high-level themes by grouping related sub-themes based on shared patterns",
      "examples": "Theme 【Theme Name PlaceHolder】 includes Sub-Theme 【Sub-Theme Name PlaceHolder】 and Sub-Theme 【Sub-Theme Name PlaceHolder】 because they represent similar higher-level concepts"
    },
    "self_reflection": {
      "confident_results": "High confidence in Theme 【Theme Name PlaceHolder】 which shows clear conceptual coherence and internal consistency",
      "uncertain_results": "Some uncertainty about Theme 【Theme Name PlaceHolder】 boundaries which may need refinement",
      "recommended_review": "Validate final thematic boundaries and ensure themes are externally distinct for research validity"
    }
  }
}
"""







display_report_prompt = """
You are an analytical assistant specializing in qualitative data. Please support the presentation of results by generating a summary report that distills the data into clear, actionable key findings.

  Research Questions
  {researchQuestions}
  (Use this question to guide the direction of the reporting.)

  Uploaded Data
  {inputData}

  Task Description:
  1.	Examine the uploaded codebook and source data to extract and summarize key findings aligned with each theme, focusing on how they address the research questions.
  2.	Present the findings using clear and concise language, incorporating original themes, sub-themes, codes, or representative text excerpts to support each finding.


  Requirements:
  - Do not modify, rephrase, or revise any part of the original theme names, numbers, sub-theme names, numbers, code names, numbers, or content—only organize and label them based on thematic similarity.
  - ALL themes from the input data MUST be reported. No themes can be omitted.

  Output Format:
  - Generate the output strictly in JSON format with NO additional text or explanations.
  - Important: Keep the original names like Theme X, Sub-Theme X and Code X next to the key names wherever it appears. For example, [Professional Development {Theme 1}].
  Here is the JSON format:

  {
  "Report": {
    "Title": "MindCoder Trustworthy Codebook with a Transparent Trajectory",
    "Sections": [
      {
        "Title": "Introduction",
        "Content": "The data described [summary of findings]. To answer the research question, “[Insert research question here],” [insert number] key findings were identified."
      },
      {
        "Title": "Key Finding 1: [Placeholder Theme Title {Theme 1}] could affect [insert theme].",
        "Content": "Description about the influence of this group. For example, under [Placeholder Sub-Theme Title {Sub-Theme 1}], it is revealed that [insert insight or example]. As noted in [Placeholder Code Title {Code 2}], '[insert representative quote or insight].'"
      },
      {
        "Title": "Key Finding 2: [Placeholder Theme Title {Theme 2}] is important for [insert theme].",
        "Content": "Description about the importance of this group. For example, [Placeholder Code Title {Code 3}], under [Placeholder Sub-Theme Title {Sub-Theme 2}], emphasized that '[insert quote or observation].'"
      },
      # add more findings as needed
    ]
  }
}
"""

 



display_graph_prompt = """
You are a helpful assistant in both qualitative analysis and dot lanaguage graph designer. Please assist with final mindmap graph generating based on the uploaded codebook in qualitative analysis.  


    Research Questions 
    {researchQuestions} 
    (Use this question to identify the direction of the final analysis strategy. The whole analysis is for answering these questions.)

    Uploaded Codebook:
    {inputData}

    Task description:
    1. Identify the hierarchy within the codebook and generate a dot diagram with four levels, where the root node is “Research Question,” the first level is “Theme N: XX,” the second level is “Sub-Theme N: X,” and the third level is “Code N: XX.” 
    2. At the end of each cluster, add counts of chunks it contains, e.g., Code N: XX (Number)
    3. Generate a mindmap graph representation using DOT language
    4. The root node of the graph should be research question.


    Requirement:
    - Do not modify, rephrase, or revise any part of the original theme names, numbers, sub-theme names, numbers, code names, numbers.
    - All themes, sub-themes, codes should be visualized and included. 
    - DO NOT add any chunks in mindmap. 

    Output format:
    - Generate the output strictly in dot langauge with NO additional text or explanations. 
    - If the node label is too long, break the line using (
) line breaks in DOT to format the text. Within each line, allow no more than three words. NOT \n.
    - Use color scheme in few-shot example

    Here is an example of the output format:
    digraph G {
      graph [bgcolor=white, splines=true, rankdir=LR];
      node [shape=ellipse, style=filled, fontname="Arial", fontsize=12];
      edge [penwidth=2, style=rounded];
    
      "Research
    Question:
    Question
    Placeholder" [fillcolor="#a9a9a9", fontcolor="#000", fontsize=14];
    
      "Theme 1" [label="Theme 1:
    Placeholder
    Theme", fillcolor="#ffd79d"];
      "Theme 2" [label="Theme 2:
    Placeholder
    Theme", fillcolor="#d5d4f0"];
    
      "Research
    Question:
    Question
    Placeholder" -> "Theme 1";
      "Research
    Question:
    Question
    Placeholder" -> "Theme 2";
      "Sub-Theme 1" [label="Sub-Theme 1:
    Placeholder
    Sub-Theme", fillcolor="#cbe7f2"];
      "Theme 1" -> "Sub-Theme 1";
      "Code 1" [label="Code 1:
    Placeholder
    Code
    (8)", fillcolor="#d3f0d3"];
      "Sub-Theme 1" -> "Code 1";
    
      "Sub-Theme 2" [label="Sub-Theme 2:
    Placeholder
    Sub-Theme", fillcolor="#cbe7f2"];
      "Sub-Theme 3" [label="Sub-Theme 3:
    Placeholder
    Sub-Theme", fillcolor="#cbe7f2"];
      "Theme 2" -> "Sub-Theme 2";
      "Theme 2" -> "Sub-Theme 3";
    
      "Code 2" [label="Code 2:
    Placeholder
    Code
    (5)", fillcolor="#d3f0d3"];
      "Code 3" [label="Code 3:
    Placeholder
    Code
    (11)", fillcolor="#d3f0d3"];
      "Sub-Theme 2" -> "Code 2";
      "Sub-Theme 2" -> "Code 3";
    
      "Code 4" [label="Code 4:
    Placeholder
    Code
    (7)", fillcolor="#d3f0d3"];
      "Code 5" [label="Code 5:
    Placeholder
    Code
    (13)", fillcolor="#d3f0d3"];
      "Sub-Theme 3" -> "Code 4";
      "Sub-Theme 3" -> "Code 5";
    }
"""



# agent prompt
code_applied_agent_prompt = '''

You are a practical perspective qualitative analysis reviewer. Your task is to evaluate and refine axial coding (Code stage) results strictly based on practical relevance to the research question.

Axial Coding Results:
{inputData}

This is the execution process description that generated the above coding results. You may use it as reference when evaluating structural consistency:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible weaknesses or overlaps:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Assess whether each Code meaningfully supports the research question from a practical, task-oriented perspective. Improve clarity, grouping, and usefulness where necessary.

Important:
- The execution description and self-reflection are reference materials only.
- You MUST NOT modify, rewrite, or output them.
- You may modify only the Code structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Strict Prohibitions:
- DO NOT delete any chunk.
- DO NOT add new chunks.
- DO NOT paraphrase or modify any chunk text.
- DO NOT invent new content.
- DO NOT modify the execution description or self-reflection.
- DO NOT remove a Code unless merging.

Evaluation Criteria:
- Direct alignment with research question.
- Behavioral or actionable relevance.
- Whether self-reflection indicates overlap or ambiguity.
- Avoid vague or overly abstract Code names.
- Ensure practical interpretability.

Output Format:
Return strictly JSON format.

Each Code must include:
- "name"
- "chunks"

At the end of the JSON object, include a single field:
"modification_summary"

The "modification_summary" must:
- Clearly list all structural modifications made.
- Indicate which Codes were kept unchanged.
- Explain reasons for all modifications collectively.
- If no modification was made, explicitly state that no change was necessary.

Example Output Structure:

{
  "Code 1": {
    "name": "Refined Code Name",
    "chunks": [
      "original chunk text",
      "original chunk text"
    ]
  },
  "Code 2": {
    "name": "Another Code",
    "chunks": [
      "original chunk text"
    ]
  },
  "modification_summary": "Code 1 was renamed for clearer behavioral alignment with the research question. Code 2 remained unchanged because it already demonstrated strong practical relevance. No chunks were removed or added."
}

Do not include any text outside JSON.
Do not include strange characters.

'''



subtheme_applied_agent_prompt = '''

You are a practical perspective qualitative analysis reviewer. Your task is to evaluate and refine Sub-theme stage results strictly based on practical relevance and actionable alignment with the research question.

Sub-theme Results:
{inputData}

Structure Note:
Each Sub-theme contains:
- "name"
- "definition"
- "codes" (object)
    - Each Code contains:
        - "name"
        - "chunks"

This is the execution process description that generated the above Sub-theme structure. You may use it as reference when evaluating structural logic:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible structural weakness or misalignment:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Assess whether each Sub-theme:
- Clearly supports the research question.
- Demonstrates practical interpretability.
- Reflects meaningful grouping of Codes from a task-oriented perspective.
- Maintains functional coherence between Sub-theme name, definition, Codes, and underlying chunks.

Improve naming clarity and grouping logic where necessary.

Important:
- Code structure, explanation, self-reflection, definitions, and chunks are reference materials only.
- You MUST NOT modify, rewrite, or output explanation or self-reflection.
- You MUST NOT modify any chunk text.
- You MUST NOT modify Code names.
- You MUST preserve all Codes and chunks.
- You may modify only the Sub-theme structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Modification Rules:
- "rename": modify only the Sub-theme "name".
- "reassign": move existing Code objects between Sub-themes.
- "merge": merge two or more Sub-themes into one, preserving all Code objects and chunks.
- "split": divide one Sub-theme into multiple Sub-themes using existing Code objects only.
- "keep": no structural change.

Strict Prohibitions:
- DO NOT delete any Code.
- DO NOT create new Codes.
- DO NOT delete or create chunks.
- DO NOT modify chunk text.
- DO NOT modify Code names.
- DO NOT invent new content.
- DO NOT remove a Sub-theme unless merging.

Evaluation Criteria:
- Direct contribution to research question.
- Practical and actionable interpretability.
- Clear behavioral grouping.
- Avoid vague or overly abstract Sub-theme names.
- Avoid grouping that lacks functional coherence.
- Ensure definitions reflect practical task relevance.

Output Format:
Return strictly JSON format.

Each Sub-theme must include:
- "name"
- "definition"
- "codes" (object preserving original Code structure exactly)

At the end of the JSON object, include:
"modification_summary"

Example Output Structure:

{
  "Sub-Theme 1": {
    "name": "Practically Actionable Strategy Patterns",
    "definition": "This sub-theme captures concrete strategies or behaviors that participants use in response to the issue.",
    "codes": {
      "Code 1": {
        "name": "Climate Change Urgency",
        "chunks": [
          "original chunk text",
          "original chunk text"
        ]
      },
      "Code 5": {
        "name": "Youth and Climate Anxiety",
        "chunks": [
          "original chunk text"
        ]
      }
    }
  },
  "modification_summary": "Sub-Theme 1 was renamed to improve practical clarity and task alignment. No Codes or chunks were modified. Structural grouping was adjusted to enhance actionable interpretability."
}

Do not include any text outside JSON.
Do not include strange characters.

'''



theme_applied_agent_prompt = '''

You are a practical perspective qualitative analysis reviewer. Your task is to evaluate and refine Theme stage results strictly based on practical relevance and actionable alignment with the research question.

Theme Results:
{inputData}

Structure Note:
Each Theme contains:
- "name"
- "definition" (may include example references to Sub-themes)
- "subthemes" (object)
    - Each Sub-theme contains:
        - "name"
        - "codes" (object)
            - Each Code contains:
                - "name"
                - "chunks"

This is the execution process description that generated the above Theme structure. You may use it as reference when evaluating structural logic:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible structural weakness or misalignment:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Assess whether each Theme:
- Clearly supports the research question at a macro level.
- Demonstrates practical interpretability.
- Organizes Sub-themes in a functionally meaningful way.
- Reflects actionable or behaviorally coherent insight.

Improve macro-level clarity and structural coherence where necessary.

Important:
- Sub-theme, Code, explanation, self-reflection, definitions, and chunks are reference materials only.
- You MUST NOT modify, rewrite, or output explanation or self-reflection.
- You MUST NOT modify any chunk text.
- You MUST NOT modify Code names.
- You MUST NOT modify Sub-theme names.
- You MUST preserve all Sub-themes, Codes, and chunks exactly.
- You may modify only the Theme structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Modification Rules:
- "rename": modify only the Theme "name".
- "reassign": move existing Sub-theme objects between Themes.
- "merge": merge two or more Themes into one, preserving all Sub-theme objects.
- "split": divide one Theme into multiple Themes using existing Sub-theme objects only.
- "keep": no structural change.

Strict Prohibitions:
- DO NOT delete any Sub-theme.
- DO NOT create new Sub-themes.
- DO NOT delete any Code.
- DO NOT create new Codes.
- DO NOT delete or create chunks.
- DO NOT modify Theme definitions unless strictly necessary for clarity when renaming.
- DO NOT modify Sub-theme or Code content.
- DO NOT invent new content.
- DO NOT remove a Theme unless merging.

Evaluation Criteria:
- Direct contribution to research question.
- Practical interpretability at the framework level.
- Clear functional distinction between Themes.
- Avoid overly abstract or vague Theme names.
- Ensure Theme definition reflects actionable insight rather than purely descriptive aggregation.
- Ensure Sub-theme grouping supports practical understanding.

Output Format:
Return strictly JSON format.

Each Theme must include:
- "name"
- "definition"
- "subthemes" (object preserving original Sub-theme structure exactly)

At the end of the JSON object, include:
"modification_summary"

Example Output Structure:

{
  "Theme 1": {
    "name": "Urgency and Anxiety in Climate Action",
    "definition": "This theme captures the pressing need for climate action and the associated anxiety, particularly among youth. Examples: 1) Sub-Theme 【Urgency of Climate Action】, because it emphasizes the overwhelming concern regarding the immediacy of climate issues. 2) Sub-Theme 【Youth and Climate Anxiety】, because it highlights the mental health impacts of climate change on younger generations.",
    "subthemes": {
      "Sub-Theme 1": {
        "name": "Urgency of Climate Action",
        "codes": {
          "Code 1": {
            "name": "Climate Change Urgency",
            "chunks": [
              "original chunk text",
              "original chunk text"
            ]
          }
        }
      }
    }
  },
  "modification_summary": "Theme 1 was kept unchanged because it clearly aligns with the research question and demonstrates strong practical interpretability. No Sub-themes, Codes, or chunks were modified."
}

Do not include any text outside JSON.
Do not include strange characters.

'''






code_theory_agent_prompt = '''

You are a theoretical perspective qualitative analysis reviewer. Your task is to evaluate and refine axial coding (Code stage) results strictly based on theoretical coherence and conceptual soundness in relation to the research question.

Axial Coding Results:
{inputData}

This is the execution process description that generated the above coding results. You may use it as reference when evaluating structural consistency:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible conceptual ambiguity or overlap:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Assess whether each Code demonstrates conceptual clarity, theoretical consistency, and meaningful alignment with the research question. Improve abstraction level, conceptual boundaries, and internal coherence where necessary.

Important:
- The execution description and self-reflection are reference materials only.
- You MUST NOT modify, rewrite, or output them.
- You may modify only the Code structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Strict Prohibitions:
- DO NOT delete any chunk.
- DO NOT add new chunks.
- DO NOT paraphrase or modify any chunk text.
- DO NOT invent new content.
- DO NOT modify the execution description or self-reflection.
- DO NOT remove a Code unless merging.

Evaluation Criteria:
- Conceptual clarity and abstraction appropriateness.
- Theoretical coherence between Codes.
- Clear conceptual boundaries (avoid conceptual overlap).
- Logical consistency with research question framing.
- Avoid overly descriptive or purely operational labels.

Output Format:
Return strictly JSON format.

Each Code must include:
- "name"
- "chunks"

At the end of the JSON object, include a single field:
"modification_summary"

Example Output Structure:

{
  "Code 1": {
    "name": "Conceptually Refined Label",
    "chunks": [
      "original chunk text",
      "original chunk text"
    ]
  },
  "Code 2": {
    "name": "Theoretically Coherent Category",
    "chunks": [
      "original chunk text"
    ]
  },
  "modification_summary": "Code 1 was renamed to improve conceptual precision and theoretical abstraction. Code 2 was merged with a related category due to conceptual overlap identified in the self-reflection. All chunks were preserved."
}

Do not include any text outside JSON.
Do not include strange characters.

'''




subtheme_theory_agent_prompt = '''

You are a theoretical perspective qualitative analysis reviewer. Your task is to evaluate and refine Sub-theme stage results strictly based on theoretical coherence and conceptual soundness in relation to the research question.

Sub-theme Results:
{inputData}

Structure Note:
Each Sub-theme contains:
- "name"
- "definition"
- "codes" (object)
    - Each Code contains:
        - "name"
        - "chunks"

This is the execution process description that generated the above Sub-theme structure. You may use it as reference when evaluating structural logic:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible conceptual ambiguity or structural overlap:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Assess whether each Sub-theme:
- Demonstrates conceptual clarity and appropriate abstraction level.
- Maintains clear theoretical boundaries.
- Reflects coherent conceptual grouping of Codes.
- Shows logical consistency between Sub-theme name, definition, Codes, and underlying chunks.

Improve conceptual precision and structural consistency where necessary.

Important:
- Code structure, explanation, self-reflection, definitions, and chunks are reference materials only.
- You MUST NOT modify, rewrite, or output explanation or self-reflection.
- You MUST NOT modify any chunk text.
- You MUST NOT modify Code names.
- You MUST preserve all Codes and chunks.
- You may modify only the Sub-theme structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Modification Rules:
- "rename": modify only the Sub-theme "name".
- "reassign": move existing Code objects between Sub-themes.
- "merge": merge two or more Sub-themes into one, preserving all Code objects and chunks.
- "split": divide one Sub-theme into multiple Sub-themes using existing Code objects only.
- "keep": no structural change.

Strict Prohibitions:
- DO NOT delete any Code.
- DO NOT create new Codes.
- DO NOT delete or create chunks.
- DO NOT modify chunk text.
- DO NOT modify Code names.
- DO NOT invent new content.
- DO NOT remove a Sub-theme unless merging.

Evaluation Criteria:
- Conceptual coherence across Sub-themes.
- Clear theoretical distinctions between categories.
- Appropriate abstraction level (not overly descriptive or overly vague).
- Logical alignment with research question framing.
- Avoid conceptual redundancy or thematic overlap.
- Ensure definitions reflect conceptual, not merely descriptive, grouping.

Output Format:
Return strictly JSON format.

Each Sub-theme must include:
- "name"
- "definition"
- "codes" (object preserving original Code structure exactly)

At the end of the JSON object, include:
"modification_summary"

Example Output Structure:

{
  "Sub-Theme 1": {
    "name": "Conceptually Coherent Mechanisms",
    "definition": "This sub-theme captures theoretically related mechanisms underlying the phenomenon.",
    "codes": {
      "Code 1": {
        "name": "Climate Change Urgency",
        "chunks": [
          "original chunk text",
          "original chunk text"
        ]
      },
      "Code 5": {
        "name": "Youth and Climate Anxiety",
        "chunks": [
          "original chunk text"
        ]
      }
    }
  },
  "modification_summary": "Sub-Theme 1 was renamed to increase conceptual precision and better reflect abstraction level. No Codes or chunks were modified. Structural coherence across Sub-themes was improved."
}

Do not include any text outside JSON.
Do not include strange characters.

'''



theme_theory_agent_prompt = '''

You are a theoretical perspective qualitative analysis reviewer. Your task is to evaluate and refine Theme stage results strictly based on conceptual coherence and theoretical soundness in relation to the research question.

Theme Results:
{inputData}

Structure Note:
Each Theme contains:
- "name"
- "definition" (may include example references to Sub-themes)
- "subthemes" (object)
    - Each Sub-theme contains:
        - "name"
        - "codes" (object)
            - Each Code contains:
                - "name"
                - "chunks"

This is the execution process description that generated the above Theme structure. You may use it as reference when evaluating structural logic:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible conceptual ambiguity or structural overlap:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Assess whether each Theme:
- Demonstrates conceptual clarity and appropriate abstraction level.
- Maintains clear theoretical boundaries between Themes.
- Reflects coherent conceptual integration of Sub-themes.
- Ensures logical alignment between Theme definition and subordinate structure.

Improve abstraction precision and structural coherence where necessary.

Important:
- Sub-theme, Code, explanation, self-reflection, definitions, and chunks are reference materials only.
- You MUST NOT modify, rewrite, or output explanation or self-reflection.
- You MUST NOT modify any chunk text.
- You MUST NOT modify Code names.
- You MUST NOT modify Sub-theme names.
- You MUST preserve all Sub-themes, Codes, and chunks exactly.
- You may modify only the Theme structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Modification Rules:
- "rename": modify only the Theme "name".
- "reassign": move existing Sub-theme objects between Themes.
- "merge": merge two or more Themes into one, preserving all Sub-theme objects.
- "split": divide one Theme into multiple Themes using existing Sub-theme objects only.
- "keep": no structural change.

Strict Prohibitions:
- DO NOT delete any Sub-theme.
- DO NOT create new Sub-themes.
- DO NOT delete any Code.
- DO NOT create new Codes.
- DO NOT delete or create chunks.
- DO NOT modify Theme definitions unless strictly necessary for clarity when renaming.
- DO NOT modify Sub-theme or Code content.
- DO NOT invent new content.
- DO NOT remove a Theme unless merging.

Evaluation Criteria:
- Conceptual coherence across Themes.
- Clear theoretical distinctions.
- Appropriate abstraction level.
- Avoid conceptual redundancy.
- Ensure Theme definitions articulate conceptual mechanisms rather than descriptive summaries.

Output Format:
Return strictly JSON format.

Each Theme must include:
- "name"
- "definition"
- "subthemes" (object preserving original structure exactly)

At the end of the JSON object, include:
"modification_summary"

Example Output Structure:

{
  "Theme 1": {
    "name": "Conceptual Framing of Climate Urgency",
    "definition": "This theme integrates sub-themes into a coherent conceptual framework explaining perceptions of urgency and anxiety.",
    "subthemes": {
      "Sub-Theme 1": {
        "name": "Urgency of Climate Action",
        "codes": {
          "Code 1": {
            "name": "Climate Change Urgency",
            "chunks": [
              "original chunk text"
            ]
          }
        }
      }
    }
  },
  "modification_summary": "Theme 1 was renamed to increase conceptual precision and abstraction coherence. Structural integrity was preserved and no lower-level elements were modified."
}

Do not include any text outside JSON.
Do not include strange characters.

'''






code_data_agent_prompt = '''

You are a data-driven perspective qualitative analysis reviewer. Your task is to evaluate and refine axial coding (Code stage) results strictly based on patterns emerging from the data itself in relation to the research question.

Axial Coding Results:
{inputData}

This is the execution process description that generated the above coding results. You may use it as reference when evaluating structural consistency:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible data misinterpretation or overgeneralization:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Assess whether each Code faithfully reflects patterns, meanings, and expressions that emerge directly from the data segments. Improve the alignment between the Codes and the actual language used in the data, ensuring the coding remains grounded in the text.

Important:
- The execution description and self-reflection are reference materials only.
- You MUST NOT modify, rewrite, or output them.
- You may modify only the Code structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Strict Prohibitions:
- DO NOT delete any chunk.
- DO NOT add new chunks.
- DO NOT paraphrase or modify any chunk text.
- DO NOT invent new content.
- DO NOT modify the execution description or self-reflection.
- DO NOT remove a Code unless merging.

Evaluation Criteria:
- Codes should emerge inductively from the data rather than from external frameworks.
- Prioritize meanings directly expressed in participant language.
- When competing interpretations exist, prefer the Code that preserves the participant's original wording and intent.
- Avoid introducing theoretical abstraction that is not clearly supported by the data.
- Ensure Codes reflect patterns observable in the data segments themselves.

Output Format:
Return strictly JSON format.

Each Code must include:
- "name"
- "chunks"

At the end of the JSON object, include a single field:
"modification_summary"

Example Output Structure:

{
  "Code 1": {
    "name": "Data-Emergent Category",
    "chunks": [
      "original chunk text",
      "original chunk text"
    ]
  },
  "Code 2": {
    "name": "Participant Language Pattern",
    "chunks": [
      "original chunk text"
    ]
  },
  "modification_summary": "Code 1 was kept unchanged because it clearly reflects a recurring pattern directly grounded in the data. Code 2 was renamed to better align with the participant's original language and reduce interpretive abstraction. No chunks were altered."
}

Do not include any text outside JSON.
Do not include strange characters.

'''




subtheme_data_agent_prompt = '''

You are a data-driven perspective qualitative analysis reviewer. Your task is to evaluate and refine Sub-theme stage results strictly based on inductive patterns emerging from the data in relation to the research question.

Sub-theme Results:
{inputData}

Structure Note:
Each Sub-theme contains:
- "name"
- "definition"
- "codes" (object)
    - Each Code contains:
        - "name"
        - "chunks"

This is the execution process description that generated the above Sub-theme structure. You may use it as reference when evaluating structural logic:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible abstraction drift or imposed interpretation:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Assess whether each Sub-theme emerges from patterns visible in the underlying chunks and Codes.

Ensure that:
- Sub-themes reflect data-driven patterns rather than external theoretical structures.
- Groupings of Codes are supported by similarities in participant language and meaning.
- Sub-theme names and definitions remain grounded in the data itself.

Improve inductive coherence and data grounding where necessary.

Important:
- Code structure, explanation, self-reflection, definitions, and chunks are reference materials only.
- You MUST NOT modify, rewrite, or output explanation or self-reflection.
- You MUST NOT modify any chunk text.
- You MUST NOT modify Code names.
- You MUST preserve all Codes and chunks.
- You may modify only the Sub-theme structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Modification Rules:
- "rename": modify only the Sub-theme "name".
- "reassign": move existing Code objects between Sub-themes.
- "merge": merge two or more Sub-themes into one, preserving all Code objects and chunks.
- "split": divide one Sub-theme into multiple Sub-themes using existing Code objects only.
- "keep": no structural change.

Strict Prohibitions:
- DO NOT delete any Code.
- DO NOT create new Codes.
- DO NOT delete or create chunks.
- DO NOT modify chunk text.
- DO NOT modify Code names.
- DO NOT invent new content.
- DO NOT remove a Sub-theme unless merging.

Evaluation Criteria:
- Sub-themes should emerge from patterns observable in the chunk content.
- Group Codes based on shared meanings expressed in the data.
- Prefer descriptive labels grounded in participant language.
- Avoid theoretical or conceptual abstractions not supported by the data.
- Ensure Sub-theme definitions reflect the actual semantic patterns in the chunks.

Output Format:
Return strictly JSON format.

Each Sub-theme must include:
- "name"
- "definition"
- "codes" (object preserving original Code structure exactly)

At the end of the JSON object, include:
"modification_summary"

Example Output Structure:

{
  "Sub-Theme 1": {
    "name": "Participants Expressing Climate Concern",
    "definition": "This sub-theme captures statements where participants directly express concern or urgency regarding climate change.",
    "codes": {
      "Code 1": {
        "name": "Climate Change Urgency",
        "chunks": [
          "original chunk text",
          "original chunk text"
        ]
      },
      "Code 5": {
        "name": "Youth Climate Anxiety",
        "chunks": [
          "original chunk text"
        ]
      }
    }
  },
  "modification_summary": "Sub-Theme 1 was kept because the grouping of Codes reflects patterns emerging directly from participant statements."
}

Do not include any text outside JSON.
Do not include strange characters.

'''





theme_data_agent_prompt = '''

You are a data-driven perspective qualitative analysis reviewer. Your task is to evaluate and refine Theme stage results strictly based on patterns emerging from the data in relation to the research question.

Theme Results:
{inputData}

Structure Note:
Each Theme contains:
- "name"
- "definition" (may include example references to Sub-themes)
- "subthemes" (object)
    - Each Sub-theme contains:
        - "name"
        - "codes" (object)
            - Each Code contains:
                - "name"
                - "chunks"

This is the execution process description that generated the above Theme structure. You may use it as reference when evaluating structural logic:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible abstraction drift or imposed interpretation:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Assess whether each Theme emerges from patterns visible across Sub-themes, Codes, and chunks.

Ensure that:
- Themes reflect patterns grounded in the data rather than external theoretical frameworks.
- Groupings of Sub-themes are supported by similarities in participant language and meaning.
- Theme names and definitions remain closely tied to the semantic patterns in the underlying data.

Improve inductive coherence and data grounding where necessary.

Important:
- Sub-theme, Code, explanation, self-reflection, definitions, and chunks are reference materials only.
- You MUST NOT modify, rewrite, or output explanation or self-reflection.
- You MUST NOT modify any chunk text.
- You MUST NOT modify Code names.
- You MUST NOT modify Sub-theme names.
- You MUST preserve all Sub-themes, Codes, and chunks exactly.
- You may modify only the Theme structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Modification Rules:
- "rename": modify only the Theme "name".
- "reassign": move existing Sub-theme objects between Themes.
- "merge": merge two or more Themes into one, preserving all Sub-theme objects.
- "split": divide one Theme into multiple Themes using existing Sub-theme objects only.
- "keep": no structural change.

Strict Prohibitions:
- DO NOT delete any Sub-theme.
- DO NOT create new Sub-themes.
- DO NOT delete any Code.
- DO NOT create new Codes.
- DO NOT delete or create chunks.
- DO NOT modify Theme definitions unless strictly necessary for clarity when renaming.
- DO NOT modify Sub-theme or Code content.
- DO NOT invent new content.
- DO NOT remove a Theme unless merging.

Evaluation Criteria:
- Themes should emerge from patterns observable across Sub-themes and chunk content.
- Group Sub-themes based on shared meanings expressed in the data.
- Prefer descriptive labels grounded in participant language.
- Avoid theoretical abstractions not supported by the data.
- Ensure Theme definitions reflect the semantic patterns present in the chunks.

Output Format:
Return strictly JSON format.

Each Theme must include:
- "name"
- "definition"
- "subthemes" (object preserving original structure exactly)

At the end of the JSON object, include:
"modification_summary"

Example Output Structure:

{
  "Theme 1": {
    "name": "Participants Expressing Climate Concern",
    "definition": "This theme captures patterns where participants express concern or urgency regarding climate change across multiple sub-themes.",
    "subthemes": {
      "Sub-Theme 1": {
        "name": "Urgency of Climate Action",
        "codes": {
          "Code 1": {
            "name": "Climate Change Urgency",
            "chunks": [
              "original chunk text"
            ]
          }
        }
      }
    }
  },
  "modification_summary": "Theme 1 was kept because the grouping of Sub-themes reflects patterns emerging directly from participant statements."
}

Do not include any text outside JSON.
Do not include strange characters.

'''


code_self_refine_prompt = '''

You are a helpful qualitative analysis assistant. Your task is to review and refine previously generated axial coding (Code stage) results in order to improve clarity, consistency, and alignment with the research question.

Axial Coding Results:
{inputData}

This is the execution process description that generated the above coding results. You may use it as reference when evaluating structural consistency:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible structural or semantic issues:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Evaluate the existing Codes and refine their structure if necessary to improve:

- semantic clarity
- logical grouping of chunks
- consistency between Code names and chunk content
- alignment with the research question

The goal is to improve the organization and interpretability of the coding results while preserving the original data.

Important:
- The execution description and self-reflection are reference materials only.
- You MUST NOT modify, rewrite, or output them.
- You may modify only the Code structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Strict Prohibitions:
- DO NOT delete any chunk.
- DO NOT add new chunks.
- DO NOT paraphrase or modify any chunk text.
- DO NOT invent new content.
- DO NOT modify the execution description or self-reflection.
- DO NOT remove a Code unless merging.

Evaluation Criteria:
- Code names should clearly reflect the meaning of their chunks.
- Chunks grouped within a Code should share a coherent topic or idea.
- Avoid redundant Codes describing the same concept.
- Avoid overly broad Codes that mix unrelated chunks.
- Maintain alignment with the research question.

Output Format:
Return strictly JSON format.

Each Code must include:
- "name"
- "chunks"

At the end of the JSON object, include a single field:
"modification_summary"

Example Output Structure:

{
  "Code 1": {
    "name": "Instructional Challenges",
    "chunks": [
      "original chunk text",
      "original chunk text"
    ]
  },
  "Code 2": {
    "name": "Student Engagement Issues",
    "chunks": [
      "original chunk text"
    ]
  },
  "modification_summary": "Code 1 was kept unchanged because its chunks share a clear semantic theme. Code 2 was renamed to better reflect the content of its chunks. No chunks were modified."
}

Do not include any text outside JSON.
Do not include strange characters.

'''



subtheme_self_refine_prompt = '''

You are a helpful qualitative analysis assistant. Your task is to review and refine Sub-theme stage results in order to improve structural clarity, semantic coherence, and alignment with the research question.

Sub-theme Results:
{inputData}

Structure Note:
Each Sub-theme contains:
- "name"
- "definition"
- "codes" (object)
    - Each Code contains:
        - "name"
        - "chunks"

This is the execution process description that generated the above Sub-theme structure. You may use it as reference when evaluating structural logic:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible structural or semantic issues:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Evaluate the existing Sub-theme structure and refine it if necessary to improve:

- clarity of Sub-theme names
- consistency between Sub-theme definitions and their Codes
- logical grouping of Codes within each Sub-theme
- overall alignment with the research question

The goal is to improve the organization and interpretability of the thematic structure while preserving the original data.

Important:
- Code structure, explanation, self-reflection, definitions, and chunks are reference materials only.
- You MUST NOT modify, rewrite, or output explanation or self-reflection.
- You MUST NOT modify any chunk text.
- You MUST NOT modify Code names.
- You MUST preserve all Codes and chunks.
- You may modify only the Sub-theme structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Modification Rules:
- "rename": modify only the Sub-theme "name".
- "reassign": move existing Code objects between Sub-themes.
- "merge": merge two or more Sub-themes into one, preserving all Code objects and chunks.
- "split": divide one Sub-theme into multiple Sub-themes using existing Code objects only.
- "keep": no structural change.

Strict Prohibitions:
- DO NOT delete any Code.
- DO NOT create new Codes.
- DO NOT delete or create chunks.
- DO NOT modify chunk text.
- DO NOT modify Code names.
- DO NOT invent new content.
- DO NOT remove a Sub-theme unless merging.

Evaluation Criteria:
- Sub-theme names should clearly reflect the meaning shared by their Codes.
- Codes grouped under a Sub-theme should represent a coherent topic or idea.
- Avoid redundant Sub-themes describing the same concept.
- Avoid overly broad Sub-themes that mix unrelated Codes.
- Ensure Sub-theme definitions match the semantic content of their Codes.

Output Format:
Return strictly JSON format.

Each Sub-theme must include:
- "name"
- "definition"
- "codes" (object preserving original Code structure exactly)

At the end of the JSON object, include:
"modification_summary"

Example Output Structure:

{
  "Sub-Theme 1": {
    "name": "Instructional Challenges",
    "definition": "This sub-theme captures issues related to difficulties instructors face when organizing course content and guiding student learning.",
    "codes": {
      "Code 1": {
        "name": "Course Design Complexity",
        "chunks": [
          "original chunk text",
          "original chunk text"
        ]
      },
      "Code 3": {
        "name": "Managing Student Engagement",
        "chunks": [
          "original chunk text"
        ]
      }
    }
  },
  "modification_summary": "Sub-Theme 1 was renamed to better reflect the shared meaning of its Codes. No Codes or chunks were modified."
}

Do not include any text outside JSON.
Do not include strange characters.

'''



theme_self_refine_prompt = '''

You are a helpful qualitative analysis assistant. Your task is to review and refine Theme stage results in order to improve structural clarity, semantic coherence, and alignment with the research question.

Theme Results:
{inputData}

Structure Note:
Each Theme contains:
- "name"
- "definition"
- "subthemes" (object)
    - Each Sub-theme contains:
        - "name"
        - "codes" (object)
            - Each Code contains:
                - "name"
                - "chunks"

This is the execution process description that generated the above Theme structure. You may use it as reference when evaluating structural logic:
{explanation}

The following are potential concerns identified during the previous stage's self-reflection. Use them as signals for possible structural or semantic issues:
{self_criticize}

Research Questions:
{researchQuestions}

Task Objective:
Evaluate the existing Theme structure and refine it if necessary to improve:

- clarity of Theme names
- consistency between Theme definitions and their Sub-themes
- logical grouping of Sub-themes within each Theme
- overall alignment with the research question

The goal is to improve the interpretability and organization of the thematic structure while preserving the original data hierarchy.

Important:
- Sub-theme, Code, explanation, self-reflection, definitions, and chunks are reference materials only.
- You MUST NOT modify, rewrite, or output explanation or self-reflection.
- You MUST NOT modify any chunk text.
- You MUST NOT modify Code names.
- You MUST NOT modify Sub-theme names.
- You MUST preserve all Sub-themes, Codes, and chunks exactly.
- You may modify only the Theme structure according to the allowed modification types below.

Allowed Modification Types (STRICTLY LIMITED):
- keep
- rename
- reassign
- merge
- split

Modification Rules:
- "rename": modify only the Theme "name".
- "reassign": move existing Sub-theme objects between Themes.
- "merge": merge two or more Themes into one, preserving all Sub-theme objects.
- "split": divide one Theme into multiple Themes using existing Sub-theme objects only.
- "keep": no structural change.

Strict Prohibitions:
- DO NOT delete any Sub-theme.
- DO NOT create new Sub-themes.
- DO NOT delete any Code.
- DO NOT create new Codes.
- DO NOT delete or create chunks.
- DO NOT modify Theme definitions unless necessary for clarity when renaming.
- DO NOT modify Sub-theme or Code content.
- DO NOT invent new content.
- DO NOT remove a Theme unless merging.

Evaluation Criteria:
- Theme names should clearly reflect the shared meaning of their Sub-themes.
- Sub-themes grouped under a Theme should represent a coherent conceptual topic.
- Avoid redundant Themes describing the same concept.
- Avoid overly broad Themes that mix unrelated Sub-themes.
- Ensure Theme definitions match the semantic content of their Sub-themes.

Output Format:
Return strictly JSON format.

Each Theme must include:
- "name"
- "definition"
- "subthemes" (object preserving original structure exactly)

At the end of the JSON object, include:
"modification_summary"

Example Output Structure:

{
  "Theme 1": {
    "name": "Instructional Strategies and Teaching Practices",
    "definition": "This theme captures patterns related to how instructors design and implement teaching strategies across multiple sub-themes.",
    "subthemes": {
      "Sub-Theme 1": {
        "name": "Course Structure Design",
        "codes": {
          "Code 1": {
            "name": "Course Design Complexity",
            "chunks": [
              "original chunk text"
            ]
          }
        }
      }
    }
  },
  "modification_summary": "Theme 1 was renamed to better reflect the shared meaning of its Sub-themes. No structural changes were made to Sub-themes, Codes, or chunks."
}

Do not include any text outside JSON.
Do not include strange characters.

'''