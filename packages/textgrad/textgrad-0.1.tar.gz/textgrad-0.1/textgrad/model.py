from typing import List
from functools import partial
from textgrad.variable import Variable
from textgrad.autograd import LLMCall
from textgrad.autograd.function import Module
from textgrad.autograd.llm_backward_ops import _backward_through_search
from textgrad.engine import EngineLM

from textgrad.autograd.llm_ops import FormattedLLMCall


class BlackboxLLM(Module):
    def __init__(self, engine: EngineLM, system_prompt: Variable = None):
        """
        Initialize the LLM module.

        :param engine: The language model engine to use.
        :type engine: EngineLM
        :param system_prompt: The system prompt variable, defaults to None.
        :type system_prompt: Variable, optional
        """
        self.engine = engine
        self.system_prompt = system_prompt
        self.llm_call = LLMCall(self.engine, self.system_prompt)

    def parameters(self):
        """
        Get the parameters of the blackbox LLM.

        :return: A list of parameters.
        :rtype: list
        """
        params = []
        if self.system_prompt:
            params.append(self.system_prompt)
        return params

    def forward(self, x: Variable) -> Variable:
        """
        Perform an LLM call.

        :param x: The input variable.
        :type x: Variable
        :return: The output variable.
        :rtype: Variable
        """
        return self.llm_call(x)


class SearchEngine(Module):
    def __init__(self, search_engine_api):
        self.search_engine_api = search_engine_api
        self.engine_name = search_engine_api.name
    
    def __call__(self, query: Variable):
        results_text = self.search_engine_api.search(query.value)
        if results_text == "":
            results_text = f"NOTHING WAS FOUND ON {self.engine_name.upper()}"
        results = Variable(results_text,
                           requires_grad=True,
                           role_description=f"aggregated search results from {self.engine_name}",
                           predecessors=[query])
        
        results.set_grad_fn(
                partial(
                    _backward_through_search,
                    variables=results.predecessors,
                    results=results,
                    query=query.value,
                    engine_name=self.engine_name
                )
            )
        return results
    
    


class SelfEnsemble(Module):
    def __init__(self, 
                 engine: EngineLM,
                evaluation_instruction: Variable,
                system_prompt: Variable):
        self.evaluation_instruction = evaluation_instruction
        self.system_prompt = system_prompt
        self.engine = engine
        
        self.format_string = "{Instruction}\nQuestion: {Question}\nPredictions: {Potential solution strategies and predictions}"
        self.fields = {"Instruction": self.evaluation_instruction, "Potential solution strategies and predictions": None, "Question": None}
        self.formatted_llm_call = FormattedLLMCall(engine=self.engine,
                                                   format_string=self.format_string,
                                                   fields=self.fields,
                                                   system_prompt=self.system_prompt)

        self.parameters = [self.evaluation_instruction, self.system_prompt]

    def forward(self, 
                question: Variable,
                predictions: List[Variable]):

        #predictions_concat = tg.sum(predictions)
        
        prediction_string = "\n".join([f"Prediction - {i+1}: {p.value}" for i, p in enumerate(predictions)])
        prediction_variable = Variable(prediction_string, 
                                       requires_grad=True, 
                                       role_description="Potential solution strategies and predictions")
        inputs = {"Instruction": self.evaluation_instruction, 
                  "Potential solution strategies and predictions": prediction_variable, 
                  "Question": question}

        
        return self.formatted_llm_call(inputs=inputs,
                                       response_role_description=f"ensembled prediction")
