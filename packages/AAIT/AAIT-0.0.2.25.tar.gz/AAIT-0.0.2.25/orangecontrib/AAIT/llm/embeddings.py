import copy
from sentence_transformers import SentenceTransformer

from Orange.data import Domain, ContinuousVariable, Table


def create_embeddings(table, model_path):
    if table is None:
        raise Exception("No input data")

    # Copy of input data
    data = copy.deepcopy(table)
    attr_dom = list(data.domain.attributes)
    metas_dom = list(data.domain.metas)
    class_dom = list(data.domain.class_vars)

    # Load model
    try:
        model = SentenceTransformer(model_path)
    except ValueError as e:
        raise Exception("An error occurred when trying to load embeddings LLM:", e)

    # Generate embeddings on column named "content"
    try:
        embeddings = None
        rows = []
        for i, row in enumerate(data):
            features = list(data[i])
            metas = list(data.metas[i])
            embeddings = model.encode(row["content"].value, show_progress_bar=False)
            features += list(embeddings)
            rows.append(features + metas)
    except ValueError as e:
        raise Exception("An error occurred when trying to encode columns:", e)

    # Generate new Domain to add to data
    n_columns = len(embeddings)
    embeddings_doms = [ContinuousVariable(f"embedding_{i}") for i in range(n_columns)]

    # Create and return table
    domain = Domain(attributes=attr_dom + embeddings_doms, metas=metas_dom, class_vars=class_dom)
    out_data = Table.from_list(domain=domain, rows=rows)
    return out_data
