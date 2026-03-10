"""
Ejemplo: LlamaAdapter (axonium-sdk) + cerebellum-architecture

Muestra cómo conectar el LLM local con los componentes cognitivos.

Variables de entorno requeridas (archivo .env):
    LLM_BASE_URL=http://localhost:8080
    LLM_USERNAME=tu_usuario
    LLM_PASSWORD=tu_contraseña
"""
import asyncio

from dotenv import load_dotenv

load_dotenv()


from cerebellum.infraestructure import LLMClient
from cerebellum.cognition import LLMPlanner
from cerebellum.cognition import LLMReasoner



async def main():
    # 1. Crear el cliente LLM local usando axonium
    llm = LLMClient(
        model="Mixtral-7B-Instruct-v0.1.Q4_0.gguf",
        timeout=60.0,
    )

    # 2. Planner LLM: genera un plan a partir del goal
    planner = LLMPlanner(llm_client=llm)
    plan = await planner.create_plan(
        goal="Analizar el mercado de IA en LATAM para 2026"
    )
    print("=== Plan generado ===")
    print(plan)

    # 3. Reasoner LLM: ejecuta cada paso del plan
    reasoner = LLMReasoner(llm_client=llm)

    results = await reasoner.execute(plan=plan, memory={}, tools={})
    print("\n=== Resultados del razonamiento ===")
    for step, result in zip(plan.steps, results):
        print(f"\n[Paso {step.step}] {step.action} → {step.goal}")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())


# === Plan generado ===
# steps=[PlanStep(step=1, action='search_market_data', goal='Identify key players and their market share in the AI market of LATAM as of 2021'), PlanStep(step=2, action='analyze_trends', goal='Determine the current trends and growth factors in the AI market of LATAM'), PlanStep(step=3, action='forecast_technology_adoption', goal='Forecast the adoption of AI technologies in LATAM by 2026'), PlanStep(step=4, action='project_market_size', goal='Project the market size of the AI market in LATAM for the year 2026')]

# === Resultados del razonamiento ===

# [Paso 1] search_market_data → Identify key players and their market share in the AI market of LATAM as of 2021
# To execute the step 'search_market_data' for identifying key players and their market share in the AI market of LATAM (Latin America) as of 2021, we would typically follow these steps:

# 1. **Define Key Terms**: Ensure we know what "AI market" and "LATAM" mean in this context.
# 2. **Search for Reliable Sources**: Look for reports, articles, and studies from reputable market research firms that cover the AI market in LATAM.
# 3. **Analyze Findings**: Identify the key players and their market share based on the data found.

# Since I cannot perform an actual web search, I will provide a hypothetical scenario based on typical findings:

# ### Hypothetical Scenario

# **Key Players and Market Share in the AI Market of LATAM as of 2021:**

# 1. **IBM**: IBM has a significant presence in LATAM, offering a wide range of AI solutions and services. They are often cited as one of the largest players in the region.

# 2. **Microsoft**: Microsoft has been expanding its AI offerings in LATAM, particularly in areas like cloud computing and AI-powered tools. They have strong market share due to their global influence and local partnerships.

# 3. **Amazon Web Services (AWS)**: AWS has gained a substantial market share in LATAM, especially in cloud services and AI solutions. They have been expanding their presence through local partnerships and acquisitions.

# 4. **Google Cloud**: Google Cloud has been actively expanding its AI services in LATAM, focusing on cloud-based AI solutions and partnerships with local businesses.

# 5. **SAP**: SAP has a strong market presence in LATAM, offering AI-driven business solutions and services. They have been investing in local talent and partnerships to enhance their market share.

# 6. **Intel**: Intel has been involved in the AI ecosystem in LATAM, particularly through its partnerships with local tech companies and universities to promote AI research and development.

# 7. **Local Players**: Various local companies have also been active in the AI market, focusing on specific industries such as finance, healthcare, and retail. While they may not have the global reach of the above-mentioned companies, they play a significant role in the regional market.

# ### Market Share

# - **IBM**: Approximately 20-25%
# - **Microsoft**: Around 20-25%
# - **AWS**: Around 15-20%
# - **Google Cloud**: About 10-15%
# - **SAP**: Approximately 10-15%
# - **Intel**: Around 5-10%
# - **Local Players**: Varies, but generally around 5-10%

# These figures are hypothetical and based on typical findings from market research reports. For precise data, it would be necessary to consult the latest reports from reliable market research firms.

# [Paso 2] analyze_trends → Determine the current trends and growth factors in the AI market of LATAM
# To analyze trends and growth factors in the AI market of LATAM, we need to consider several key aspects:

# 1. **Government Policies and Initiatives**: Many governments in LATAM have started to implement policies and initiatives to foster the development of the AI industry. For example, Brazil has launched several initiatives to promote AI research and development. Understanding these policies can give insights into the regulatory environment and potential for growth.

# 2. **Investment and Funding**: Analyzing the amount and sources of investments in AI startups and established companies in LATAM can provide insights into the market's growth potential. Venture capital, private equity, and government funding can all play significant roles.

# 3. **Tech Company Presence**: The presence and activities of major tech companies in the region can significantly influence the AI market. Companies like IBM, Microsoft, and Google have made significant investments in LATAM, which can drive innovation and create new market opportunities.

# 4. **Startups and Entrepreneurs**: The number and success of AI startups and entrepreneurs can indicate the level of innovation and entrepreneurial activity in the region. Startups that are solving specific local problems using AI can be particularly promising.

# 5. **Academic and Research Institutions**: The level of research and development activity in universities and research institutions can provide a glimpse into the talent pool and future growth of the AI market. Collaboration between these institutions and industry can also drive innovation.

# 6. **Consumer and Business Adoption**: Understanding the degree to which businesses and consumers are adopting AI technologies can provide insights into the market's maturity and potential for growth. This can be assessed through surveys, case studies, and market research reports.

# 7. **Technology Infrastructure**: The availability and quality of technology infrastructure, such as broadband internet, cloud services, and data centers, can significantly impact the AI market. Countries with better infrastructure can support more advanced AI applications.

# 8. **Data Availability and Privacy Laws**: Access to large datasets and the implementation of data privacy laws can influence the development and adoption of AI technologies. Countries with robust data protection frameworks may face challenges, but they can also drive innovation in compliance solutions.

# 9. **Sectors Focusing on AI**: Identifying which sectors are focusing on AI (such as healthcare, finance, retail, and agriculture) can provide insights into the areas where AI is likely to see significant growth. For example, healthcare is a rapidly growing sector in LATAM due to aging populations and the need for more efficient healthcare delivery.

# 10. **Challenges and Barriers**: Identifying the key challenges and barriers to AI development and adoption in LATAM, such as skill shortages, regulatory uncertainty, and cost, can help in formulating strategies to overcome these obstacles.

# By synthesizing information from these areas, we can develop a comprehensive understanding of the current trends and growth factors in the AI market of LATAM. This analysis can be further refined with specific data points and case studies from the region.

# [Paso 3] forecast_technology_adoption → Forecast the adoption of AI technologies in LATAM by 2026
# To forecast the adoption of AI technologies in LATAM (Latin America) by 2026, we would need to follow a structured approach. However, since we don't have access to specific data and research, I will outline the steps and key considerations for such a forecast:

# 1. **Define Key Metrics**: Identify what exactly we are forecasting (e.g., percentage of companies using AI, number of AI projects, etc.).

# 2. **Historical Data**: Gather historical data on AI adoption in LATAM, if available. This could come from business reports, industry surveys, or government data.

# 3. **Trends Analysis**: Analyze trends in AI adoption across different sectors and countries in LATAM. Factors like economic growth, tech investment, and regulatory environment play a role.

# 4. **Macroeconomic and Industry Factors**: Consider broader economic conditions and technological developments. For example, growth in tech startups, investment in R&D, and government policies promoting tech adoption.

# 5. **Quantitative Models**: Use statistical models to project future adoption based on past data and trends. Techniques like regression analysis or time-series forecasting might be used.

# 6. **Qualitative Inputs**: Incorporate expert opinions and qualitative insights from industry reports, interviews with key stakeholders, and trend analysis.

# 7. **Scenario Planning**: Develop different scenarios based on varying levels of technological advancement, economic conditions, and regulatory environments.

# 8. **Validation and Refinement**: Validate the forecast against expert opinion and existing data, and refine the model as needed.

# Given the lack of specific data, a hypothetical forecast might look something like this:

# - **Base Scenario**: By 2026, 30% of companies in LATAM could be using AI technologies.
# - **Pessimistic Scenario**: Only 20% of companies might adopt AI.
# - **Optimistic Scenario**: 40% of companies could adopt AI by 2026.

# Each scenario would be based on a combination of historical data, expert opinions, and macroeconomic trends. Without specific data, these numbers are speculative, but they provide a framework for understanding the potential range of outcomes.

# [Paso 4] project_market_size → Project the market size of the AI market in LATAM for the year 2026
# To project the market size of the AI market in LATAM (Latin America) for the year 2026, we would need to follow these steps:

# 1. **Gather Historical Data**: Collect data on the growth of the AI market in LATAM for previous years (e.g., 2015-2022).
# 2. **Identify Key Trends**: Analyze the growth patterns, factors driving growth, and any challenges or inhibitors.
# 3. **Use Forecasting Techniques**: Apply regression analysis, time series forecasting, or other statistical methods to predict future growth.
# 4. **Consider External Factors**: Account for economic conditions, technological advancements, government policies, and market trends in LATAM.
# 5. **Calculate the Projection**: Use the chosen forecasting method to estimate the market size for 2026.

# Since I don't have access to real-time data and specific historical figures, I'll provide a hypothetical example based on common growth rates.

# ### Hypothetical Example

# Let's assume the AI market in LATAM grew at an annual compound growth rate (CAGR) of 15% from 2015 to 2022. Here's the step-by-step projection:

# 1. **Historical Data**:
#    - 2015: $100 million
#    - 2022: $500 million (15% CAGR over 7 years)

# 2. **Forecasting**:
#    - Using the CAGR of 15%, the market size for 2023 would be:
#      \[
#      500 \times 1.15 = 575 \text{ million}
#      \]
#    - For 2024:
#      \[
#      575 \times 1.15 = 661.25 \text{ million}
#      \]
#    - For 2025:
#      \[
#      661.25 \times 1.15 = 760.44 \text{ million}
#      \]
#    - For 2026:
#      \[
#      760.44 \times 1.15 = 884.51 \text{ million}
#      \]

# ### Final Projection

# Based on the hypothetical growth rate of 15%, the projected market size of the AI market in LATAM for the year 2026 is approximately **$884.51 million**.

# Please note that this is a simplified example and the actual projection would require more detailed analysis and data.