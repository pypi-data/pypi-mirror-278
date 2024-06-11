import logging

import dhuolib as dhuolib

model_name = "model_decision_tree"
tag = "1.0.1"
model = dhuolib.load_model(model_name, tag)


def prediction(inputs):
    data_transformed = None  # transform(inputs)
    predictions = model.predict(data_transformed)
    return predictions


def main():

    # seria interessante essa transformação chamar esse arquivo e passar os inputs como parametro
    inputs = dhuolib.read_from_bucket("s3://bucket1/inputs_encoded.csv")
    predictions = prediction(inputs)

    filename_predictions = "predictions.csv"

    predictions_result = dhuolib.save_predictions(
        filename_predictions, inputs, predictions, model_name, tag
    )

    logging.info(predictions_result)


if __name__ == "__main__":
    main()
