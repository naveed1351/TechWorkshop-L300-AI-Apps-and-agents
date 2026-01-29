# Azure imports
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation.red_team import RedTeam, RiskCategory, AttackStrategy
from pyrit.prompt_target import OpenAIChatTarget
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

# Azure AI Project Information
azure_ai_project = os.getenv("FOUNDRY_ENDPOINT")

# Original AI Red Teaming Agent configuration (commented out for custom prompts)
# red_team_agent = RedTeam(
#     azure_ai_project=azure_ai_project,
#     credential=DefaultAzureCredential(),
#     risk_categories=[
#         RiskCategory.Violence,
#         RiskCategory.HateUnfairness,
#         RiskCategory.Sexual,
#         RiskCategory.SelfHarm
#     ],
#     num_objectives=5,
# )

# Instantiate AI Red Teaming Agent with custom attack prompts
red_team_agent = RedTeam(
    azure_ai_project=azure_ai_project,
    credential=DefaultAzureCredential(),
    custom_attack_seed_prompts="data/custom_attack_prompts.json",
)

# Define the OpenAI chat target model using PyRIT
chat_target = OpenAIChatTarget(
    model_name=os.environ.get("gpt_deployment"),
    endpoint=f"{os.environ.get('gpt_endpoint')}/openai/deployments/{os.environ.get('gpt_deployment')}/chat/completions",
    api_key=os.environ.get("gpt_api_key"),
    api_version=os.environ.get("gpt_api_version"),
)

async def main():
    red_team_result = await red_team_agent.scan(
        target=chat_target,
        scan_name="Red Team Scan - Easy-Moderate Strategies",
        attack_strategies=[
            AttackStrategy.Flip,
            AttackStrategy.ROT13,
            AttackStrategy.Base64,
            AttackStrategy.AnsiAttack,
            AttackStrategy.Tense
        ])

asyncio.run(main())
