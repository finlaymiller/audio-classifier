# Classifier

## To Do

* Add support for real-time classification
* Add csv support
* Update to tensorflow 2 (probably not possible/realistic)

## How to use

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
4. I _think_ that's all the files we need. To classify:
   1. To classify files being added to a folder in real-time run `python classify_live.py ./drop_audio_here`. You can replace `./drop_audio_here` with the name of any folder you like.
   2. To classify all audio files in a directory recursively run `python classify_recursive.py {PATH TO FOLDER} {OUTPUT FILE NAME}`.
5. If you're classifying folder in real time, you can now begin to add files to the folder specified in step 4.1.

If you're classifying a folder, all classifications will be written to a `.json` document with the audio filename, sample rate, number of samples, and classifier predictions saved. Otherwise, the predictions will just be displayed in the terminal.
