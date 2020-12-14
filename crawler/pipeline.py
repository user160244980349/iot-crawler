

def run_pipeline(pipeline, data):

    output = data
    for pipe in pipeline:
        output = pipe(output)

    return output
