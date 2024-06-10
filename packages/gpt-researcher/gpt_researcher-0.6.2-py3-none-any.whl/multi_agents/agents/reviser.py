'''
self.prompt = SystemMessagePromptTemplate.from_template(
            "You are an expert writer. "
            "You have been tasked by your editor with revising the following draft, which was written by a non-expert. "
            "You may follow the editor's notes or not, as you see fit."
        ) + "Draft:\n\n{draft}" + "Editor's notes:\n\n{notes}"
'''