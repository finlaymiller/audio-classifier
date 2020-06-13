# Classifier

## To Do

* Add csv output option
* Update to tensorflow 2 (probably not possible/realistic)

## How to install

This folder contains all the files needed to run the audio classifier.

1. First, create a conda environment from the `auto_classifier_env.yml` file. For more specific instructions, see [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
2. Navigate to the folder where you've cloned this repo in your terminal.
3. The classifier uses [VGGish](https://github.com/tensorflow/models/tree/master/research/audioset/vggish) to generate features from the audio files, and [Youtube-8M](https://github.com/google/youtube-8m) to do the classification using the generated features.

   To use these models you'll have to download their supporting files using a terminal utility such as `curl`, `wget`, or PowerShell's `Invoke-Webrequest`. They can be downloaded from [https://s3.amazonaws.com/audioanalysis/models.tar.gz](https://s3.amazonaws.com/audioanalysis/models.tar.gz) with something like

    ```bash
    curl -O https://s3.amazonaws.com/audioanalysis/models.tar.gz
    ```

    or

    ```bash
    wget https://s3.amazonaws.com/audioanalysis/models.tar.gz
    ```

   Once downloaded, place the `models/` folder in the same folder as everything else.

## How to run

Supports `.mp3` and `.wav` files in 16-bit PCM.

The file to run is `classify_audio.py`. It supports the following command line flags:

| Full Name   | Shortened | Argument | Required | Description                                                                                                                                  |
|-------------|-----------|----------|----------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `--path`    | `-p`      | Filepath | Yes      | Path to folder containing files to classify                                                                                                  |
| `--outfile` | `-o`      | Filename | No       | Name of file to write classifications to. `.jsonl` is the recommended type, since the classifier writes it output in the [JSON Lines](http://jsonlines.org/) format. If not specified the output file will be named `classifications_[CURRENT_TIMESTAMP].jsonl` where `CURRENT_TIMESTAMP` is, you guessed it, the current date and time.o                                                                                                                                       |
| `--live`    | `-l`      | None     | No       | If specified, a [watchdog](https://pypi.org/project/watchdog/) will be created to classify files that are placed in the specified file path. |
| `--verbose` | `--v`     | None     | None     | Additional information is printed                                                                                                            |
So a couple typical runs might look like the following:

| Command                                                                            | Result                                                                                                                                                         |
|------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `python classify_audio.py -p ./my_audio --verbose`                                 | Classifies all audio files _currently_ in `./my_audio` with some extra prints. Writes output to the automatically-generated file.                              |
| `python classify_audio.py --path ../../Desktop --live -o ./dropped_on_desktop.txt`  | Classifies all audio files dropped onto the Desktop (assuming path is correct) and writes output to a `.txt` file (format will still be in JSON Lines though). |
