from gpt_researcher import GPTResearcher
import asyncio
from colorama import Fore, Style
import json


class ResearchAgent:
    def __init__(self):
        pass

    # TODO: validate the async here when calling the function
    async def research(self, query: str, research_report: str = "research_report", parent_query: str = ""):
        #return """The recent aerial attack by Israel on Iran has elicited a range of international reactions. The United States, while reportedly informed of the Israeli strike in advance, did not endorse the action, emphasizing restraint ([CNN](https://edition.cnn.com/middleeast/live-news/israel-iran-gaza-conflict-news-04-19-24/h_392593efda57c5e8d3fed643c6e85311)). European Union officials, including EU’s top diplomat Josep Borrell, condemned Iran's initial attack against Israel, labeling it an unprecedented escalation and a grave threat to regional security ([Al Jazeera](https://www.aljazeera.com/news/2024/4/14/serious-escalation-world-reacts-to-irans-drone-missile-raids-on-israel)). France echoed this sentiment, with Foreign Minister Stephane Sejourne highlighting Iran's destabilizing actions and the risk of military escalation."""
        # Initialize the researcher
        researcher = GPTResearcher(query=query, report_type=research_report, config_path=None, parent_query=parent_query)
        # Conduct research on the given query
        await researcher.conduct_research()
        # Write the report
        report = await researcher.write_report()

        return report

    async def run_subtopic_research(self, title: str, subtopic: str):
        try:
            report = await self.research(f"{subtopic}", research_report="subtopic_report", parent_query=title)
        except Exception as e:
            print(f"{Fore.RED}Error in researching topic {subtopic}: {e}{Style.RESET_ALL}")
            report = None
        return {subtopic: report}

    async def run_initial_research(self, task: dict):
        query = task.get("query")
        return await self.research(query)

    async def run_depth_research(self, outline: dict):
        title = outline.get("title")
        subheaders = outline.get("subheaders")
        tasks = [self.run_subtopic_research(title, query) for query in subheaders]
        results = await asyncio.gather(*tasks)
        print(results)
        print("\n\n\n\n\n")
        # Convert the results dictionary into a JSON string
        return {"title": title, "research_data": results}
