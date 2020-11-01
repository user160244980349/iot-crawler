

def run_pipeline(pipeline, init_data):

    output = init_data
    for pipe in pipeline:
        output = pipe(output)

    return output
