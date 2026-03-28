from openai import OpenAI
import json

class C_rag():
    def __init__(self):
        self.client = OpenAI()

    def RAG(self, value,value2):
        prompt = f"""Role : You are a experienced content summarizer and extractor in few words based on MCP given {json.dumps(value.MCP, indent=2)}"""
        value.rag_result = self.client.responses.create(model="gpt-4.1-mini", input=prompt,text={"format":{"type":"json_object"}}).output[0].content[0].text
        #value.rag_result = subprocess.run(["ollama", "run", "mixtral", prompt] ,capture_output=True,text=True).stdout.strip()
        value.rag_result=json.loads(value.rag_result)
        value.log.info(f"LLM result  ->  {value.rag_result}")
        self.mm(value,value2)
        return value

    def mm(self,value,value2):
        for i in  value.rag_result:
            value.L_json_result.setdefault(value2.current_rag,{})[i]=0 if value.rag_result[i] is None else value.rag_result[i]
        value.log.info(f"Combined Result -> {value.L_json_result}")