from numpy import mean, std
from tensorflow.keras import Sequential
from tensorflow.python.keras.layers import Conv1D, Dropout, MaxPooling1D, Flatten, Dense
from tensorflow.python.keras.utils.np_utils import to_categorical


def load_dataset_group(param, param1):
    return None, None


def load_dataset(prefix=""):
    # load all train
    train_x, train_y = load_dataset_group("train", f"{prefix}/HARDataset/")
    print(train_x.shape, train_y.shape)
    # load all test
    test_x, test_y = load_dataset_group("test", f"{prefix}/HARDataset/")
    print(test_x.shape, test_y.shape)
    # zero-offset class values
    train_y = train_y - 1
    test_y = test_y - 1
    # one hot encode y
    train_y = to_categorical(train_y)
    test_y = to_categorical(test_y)
    print(train_x.shape, train_y.shape, test_x.shape, test_y.shape)
    return train_x, train_y, test_x, test_y


def evaluate_model(train_x, train_y, test_x, test_y):
    verbose, epochs, batch_size = 0, 10, 32
    n_timesteps, n_features, n_outputs = train_x.shape[1], train_x.shape[2], train_y.shape[1]
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=3, activation="relu", input_shape=(n_timesteps, n_features)))
    model.add(Conv1D(filters=64, kernel_size=3, activation="relu"))
    model.add(Dropout(0.5))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(100, activation="relu"))
    model.add(Dense(n_outputs, activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    # fit network
    model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=verbose)
    # evaluate model
    _, accuracy = model.evaluate(test_x, test_y, batch_size=batch_size, verbose=0)
    return accuracy


def summarize_results(scores):
    print(scores)
    m, s = mean(scores), std(scores)
    print(f"Accuracy: {m:.3f} (+/-{s:.3f})")


# run an experiment
def run_experiment(repeats=10):
    # load data
    train_x, train_y, test_x, test_y = load_dataset()
    # repeat experiment
    scores = list()
    for r in range(repeats):
        score = evaluate_model(train_x, train_y, test_x, test_y)
        score = score * 100.0
        print(f">#{r + 1}: {score:.3f}")
        scores.append(score)
    # summarize results
    summarize_results(scores)


def main():
    # run the experiment
    run_experiment()
