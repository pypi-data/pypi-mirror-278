import copy
try:
    from llama_cpp import Llama
    use_gpu = True
except ModuleNotFoundError:
    use_gpu = False

from gpt4all import GPT4All

from Orange.data import Domain, StringVariable, Table


def generate_answers(table, model_path):
    if table is None:
        raise Exception("No input data")

    # Copy of input data
    data = copy.deepcopy(table)
    attr_dom = list(data.domain.attributes)
    metas_dom = list(data.domain.metas)
    class_dom = list(data.domain.class_vars)

    # Load model
    try:
        model = load_model(model_path, n_gpu_layers=0)
    except ValueError as e:
        raise Exception("An error occurred when trying to load query LLM:", e)

    # Generate answers on column named "prompt"
    try:
        rows = []
        for i, row in enumerate(data):
            features = list(data[i])
            metas = list(data.metas[i])
            answer = run_query(row["prompt"].value, model=model)
            metas += [answer]
            rows.append(features + metas)
    except ValueError as e:
        raise Exception("An error occurred when trying to generate an answer:", e)

    # Generate new Domain to add to data
    answer_dom = [StringVariable("Answer")]

    # Create and return table
    domain = Domain(attributes=attr_dom, metas=metas_dom + answer_dom, class_vars=class_dom)
    out_data = Table.from_list(domain=domain, rows=rows)
    return out_data


def load_model(path, n_gpu_layers=0):
    if use_gpu:
        model = Llama(path,
                      n_ctx=4096,
                      n_gpu_layers=n_gpu_layers)
    else:
        model = GPT4All(model_path=path,
                        model_name=path,
                        n_ctx=4096,
                        allow_download=False)
    return model


def query_cpu(prompt, model, max_tokens=4096, temperature=0, top_p=0.95, top_k=40, repeat_penalty=1.1):
    output = model.generate(prompt,
                            max_tokens=max_tokens,
                            temp=temperature,
                            top_p=top_p,
                            top_k=top_k,
                            repeat_penalty=repeat_penalty)
    return output


def query_gpu(prompt, model, max_tokens=4096, temperature=0, top_p=0.95, top_k=40, repeat_penalty=1.1):
    output = model(prompt,
                   max_tokens=max_tokens,
                   temperature=temperature,
                   top_p=top_p,
                   top_k=top_k,
                   repeat_penalty=repeat_penalty)["choices"][0]["text"]
    return output


def run_query(prompt, model, max_tokens=4096, temperature=0, top_p=0.95, top_k=40, repeat_penalty=1.1):
    if use_gpu:
        return query_gpu(prompt, model, max_tokens, temperature, top_p, top_k, repeat_penalty)
    else:
        return query_cpu(prompt, model, max_tokens, temperature, top_p, top_k, repeat_penalty)

